import math
import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from collections import defaultdict
import statistics


def discretize(EEG_data):
    """
    Discretization function finds the bounds of each class, and converts each
    signal value to a class - NEEDS TO BE IMPORVED
    Here the discretization classes are 10 and each value is converted to 0-9
    :param EEG_data: The ndarray to be discretized
    :return: The discretized ndarray
    """

    discr_classes = 10
    bounds = []

    epsilon = int((EEG_data.max() - EEG_data.min()) / discr_classes)
    boundToAdd = EEG_data.min()
    bounds.append(boundToAdd)
    for i in range(discr_classes - 1):
        boundToAdd += epsilon
        bounds.append(boundToAdd)
    bounds.append(EEG_data.max())

    # print("Min: ", EEG_data.min())
    # print("Max: ", EEG_data.max())
    # print(bounds)

    for i in range(len(EEG_data)):
        for j in range(len(EEG_data[0])):
            if bounds[0] <= EEG_data[i][j] < bounds[1]:
                EEG_data[i][j] = 0
            elif bounds[1] <= EEG_data[i][j] < bounds[2]:
                EEG_data[i][j] = 1
            elif bounds[2] <= EEG_data[i][j] < bounds[3]:
                EEG_data[i][j] = 2
            elif bounds[3] <= EEG_data[i][j] < bounds[4]:
                EEG_data[i][j] = 3
            elif bounds[4] <= EEG_data[i][j] < bounds[5]:
                EEG_data[i][j] = 4
            elif bounds[5] <= EEG_data[i][j] < bounds[6]:
                EEG_data[i][j] = 5
            elif bounds[6] <= EEG_data[i][j] < bounds[7]:
                EEG_data[i][j] = 6
            elif bounds[7] <= EEG_data[i][j] < bounds[8]:
                EEG_data[i][j] = 7
            elif bounds[8] <= EEG_data[i][j] < bounds[9]:
                EEG_data[i][j] = 8
            elif bounds[9] <= EEG_data[i][j] <= bounds[10]:
                EEG_data[i][j] = 9

    # unique, counts = np.unique(EEG_data, return_counts=True)
    # print(np.asarray((unique, counts)).T)

    return EEG_data


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

    totalPossiblePatterns = ((len(EEG_data[0]) - 2) * len(EEG_data))

    for row in range(len(EEG_data)):
        patterns.clear()
        for col in range(len(EEG_data[0]) - 2):
            strPattern = str(EEG_data[row][col]) + str(EEG_data[row][col + 1]) + str(EEG_data[row][col + 2])
            patterns[strPattern] += 1

        row_entropy = 0
        for patt, repetitions in patterns.items():
            p_i = repetitions / totalPossiblePatterns
            if p_i > 0:
                row_entropy = row_entropy + -(p_i * math.log(p_i, 2))
        entropies.append(row_entropy)

    return entropies


def EnPlot(enZ, enO, enN, enF, enS):

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
    print(enZ)
    enO = ShEn(O_EEG_data)
    print(enO)
    enN = ShEn(N_EEG_data)
    print(enN)
    enF = ShEn(F_EEG_data)
    print(enF)
    enS = ShEn(S_EEG_data)
    print(enS)
    EnPlot(enZ, enO, enN, enF, enS)


