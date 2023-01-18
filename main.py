import scipy


def ShEn(EEG_data):
    return 0

def EnPlot(enZ, enO, enN, enF, enS):
    return 0


if __name__ == '__main__':

    mat = scipy.io.loadmat('BonnEEGdata.mat')
    Z_EEG_data = mat['Z_EEG_data']
    O_EEG_data = mat['O_EEG_data']
    N_EEG_data = mat['N_EEG_data']
    F_EEG_data = mat['F_EEG_data']
    S_EEG_data = mat['S_EEG_data']

    enZ = ShEn(Z_EEG_data)
    enO = ShEn(O_EEG_data)
    enN = ShEn(N_EEG_data)
    enF = ShEn(F_EEG_data)
    enS = ShEn(S_EEG_data)

    EnPlot(enZ, enO, enN, enF, enS)


