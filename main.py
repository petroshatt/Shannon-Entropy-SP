"""
CHATZITOULOUSIS PETROS 1579
IOSIFIDIS ANTONIOS 1335

SHANNON ENTROPY
"""

import math
import scipy
import matplotlib.pyplot as plt
from scipy.stats import norm
from collections import defaultdict
import statistics

import warnings
warnings.filterwarnings("ignore")


discr_classes = 10
pattern_length = 3


def discretize(EEG_data):
    """
    Discretization function finds the bounds of each class, and converts each
    signal value to a class - NEEDS TO BE IMPORVED
    Here the discretization classes are 10 and each value is converted to 0-9
    :param EEG_data: The ndarray to be discretized
    :return: The discretized ndarray
    """

    bounds = []

    epsilon = int((EEG_data.max() - EEG_data.min()) / discr_classes)
    boundToAdd = EEG_data.min()
    bounds.append(boundToAdd)
    for i in range(discr_classes - 1):
        boundToAdd += epsilon
        bounds.append(boundToAdd)
    bounds.append(EEG_data.max())

    for i in range(len(EEG_data)):
        for j in range(len(EEG_data[0])):
            counter_class = 0
            for index in range(len(bounds) - 1):
                if bounds[index] <= EEG_data[i][j] <= bounds[index + 1]:
                    EEG_data[i][j] = counter_class
                    break
                else:
                    counter_class += 1

    return EEG_data


def list_to_str(s):
    """
    Coverts list of characters to string
    :param s: list to be converted
    :return: list as string
    """
    new = ""
    for x in s:
        new += str(x)
    return new


def ShEn(EEG_data):
    """
    Shannon Entropy calculation, counting patterns of a specific length using a dict in each row,
    calculating each pattern's probability and using it for the Shannon Entropy formula
    :param EEG_data: The dataset's subset
    :return: List with subset's 100 entropies
    """

    EEG_data = discretize(EEG_data)

    patterns = defaultdict(int)
    entropies = []

    totalPossiblePatterns = ((len(EEG_data[0]) - (pattern_length - 1)) * len(EEG_data))

    for row in range(len(EEG_data)):
        patterns.clear()
        for col in range(len(EEG_data[0]) - (pattern_length - 1)):
            str_pattern = list_to_str(EEG_data[row][col:col+pattern_length])
            patterns[str_pattern] += 1

        row_entropy = 0
        for patt, repetitions in patterns.items():
            p_i = repetitions / totalPossiblePatterns
            if p_i > 0:
                row_entropy = row_entropy + -(p_i * math.log(p_i, 2))
        entropies.append(row_entropy)

    entropies = [round(item, 3) for item in entropies]
    return entropies


def EnPlot(enZ, enO, enN, enF, enS):
    """
    Plot normal distribution of each subset's entropies
    :param enZ: list of subset Z entropies
    :param enO: list of subset O entropies
    :param enN: list of subset N entropies
    :param enF: list of subset F entropies
    :param enS: list of subset S entropies
    :return:
    """

    enZ.sort()
    enO.sort()
    enN.sort()
    enF.sort()
    enS.sort()

    meanZ = statistics.mean(enZ)
    sdZ = statistics.stdev(enZ)
    meanO = statistics.mean(enO)
    sdO = statistics.stdev(enO)
    meanN = statistics.mean(enN)
    sdN = statistics.stdev(enN)
    meanF = statistics.mean(enF)
    sdF = statistics.stdev(enF)
    meanS = statistics.mean(enS)
    sdS = statistics.stdev(enS)

    plt.plot(enZ, norm.pdf(enZ, meanZ, sdZ), 'r', label='enZ')
    plt.plot(enO, norm.pdf(enO, meanO, sdO), 'b', label='enO')
    plt.plot(enN, norm.pdf(enN, meanN, sdN), 'g', label='enN')
    plt.plot(enF, norm.pdf(enF, meanF, sdF), 'y', label='enF')
    plt.plot(enS, norm.pdf(enS, meanS, sdS), 'm', label='enS')
    plt.legend()
    plt.show()


if __name__ == '__main__':

    mat = scipy.io.loadmat('BonnEEGdata.mat')
    Z_EEG_data = mat['Z_EEG_data']
    O_EEG_data = mat['O_EEG_data']
    N_EEG_data = mat['N_EEG_data']
    F_EEG_data = mat['F_EEG_data']
    S_EEG_data = mat['S_EEG_data']

    enZ = ShEn(Z_EEG_data)
    print("EnZ: ", enZ)
    print()
    enO = ShEn(O_EEG_data)
    print("EnO: ", enO)
    print()
    enN = ShEn(N_EEG_data)
    print("EnN: ", enN)
    print()
    enF = ShEn(F_EEG_data)
    print("EnF: ", enF)
    print()
    enS = ShEn(S_EEG_data)
    print("EnS: ", enS)
    print()

    EnPlot(enZ, enO, enN, enF, enS)


