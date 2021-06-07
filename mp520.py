import inspect
import sys
import math

'''
Raise a "not defined" exception as a reminder
'''


def _raise_not_defined():
    print
    "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)


'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit)
'''


def extract_basic_features(digit_data, width, height):
    features=[]
    # digit_data[i][j]: 0 = ' ', 1 = '#', 2 = '+'
    for i in range(width):
        for j in range(height):
            if digit_data[i][j]==0:
                features.append(0)
            else:
                features.append(1)

    #print("this is digit data",len(features))
    return [0 if digit_data[i][j] == 0 else 1 for j in range(width) for i in range(height)]


'''
Extract advanced features that you will come up with
'''


def extract_advanced_features(digit_data, width, height):
    features = []

    def ratio(rows_s=0, rows_e=height):
        left = up = 99999
        right = down = -1
        for i in range(int(rows_s), int(rows_e)):
            for j in range(width):
                if digit_data[i][j] == 1:
                    left = min(left, i)
                    up = min(up, j)
                    right = max(right, i)
                    down = max(down, j)
        ratio = (float(right - left) / max(down - up, 1)) * 5.0  # assume 0 < ratio < 4
        for i in range(20):
            features.append((i > ratio))

    s, e = 0, height / 13
    for i in range(13):
        ratio(s + e * i, s + e * i + e)
    #around , circle and areahere are different features
    around = 0
    circle = 0
    areahere = 0
    for i in range(height):
        first = False
        buf = 0
        for j in range(width):
            if digit_data[i][j] != 0:
                around += buf
                first = True
                buf = 0
                if digit_data[i][j] == 1:
                    areahere += 1
                else:
                    circle += 1
            elif first:
                buf += 1

    features.append(around > 60)
    features.append(circle > 80)
    features.append(areahere > 80)

    #print('features', len(features))
    return features


'''
Extract the final features that you would like to use
'''


def extract_final_features(digit_data, width, height):
    # return extract_basic_features(digit_data, width, height)
    # return extract_advanced_features(digit_data, width, height)
    # return extract_basic_features(digit_data, width, height) + extract_advanced_features(digit_data, width, height)
    result1 = extract_basic_features(digit_data, width, height)
    result2 = extract_advanced_features(digit_data, width, height)

    #print('Len1 :', len(result1), 'Len2', len(result2), 'final_len:', (len(result1) +  len(result2)))

    return result1 + result2


statistics = None
'''
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training.
'''


def compute_statistics(data, label, width, height, feature_extractor, percentage=100):
    global statistics
    statistics = []
    k = 1*10**-6
    n = int(len(data) * percentage / 100.0)
    features = [list() for _ in range(10)]
    # features[num] = [list of prob of features for num from sample] = [[0, 0.1, 0.5, 0, 0, 0.2, ...], [...]]
    for i in range(n):
        features[label[i]].append(feature_extractor(data[i], width, height))
    dim = len(features[0][0])  # list of prob of features for 0 from first sample
    for num in range(10):
        s = [0] * dim
        for i in range(len(features[num])):
            for j in range(dim):
                s[j] += features[num][i][j]
        for i in range(dim):
            s[i] = float(s[i] + k) / (len(features[num]) + 2 * k)
        statistics.append(s)


'''
For the given features for a single digit image, compute the class
'''


def compute_class(features):
    prob = [0] * 10
    dim = len(features)
    for num in range(10):
        prob[num] = math.log(1.0 / 10)
        for i in range(dim):
            if features[i] == 0:
                prob[num] += math.log(1 - statistics[num][i])
            else:
                prob[num] += math.log(statistics[num][i])
    return prob.index(max(prob))


'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''


def classify(data, width, height, feature_extractor):
    return [compute_class(feature_extractor(i, width, height)) for i in data]