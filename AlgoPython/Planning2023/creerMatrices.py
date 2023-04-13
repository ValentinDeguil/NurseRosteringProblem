import pandas as pd
def creerMatrices():

    cardO = 36
    cardP = 36
    dataOperateurs = pd.read_csv('./data2023/operateursJoli.csv', sep=",")

    kappa = []
    for i in range(cardO):
        ligne = []
        for p in range(cardP):
            if dataOperateurs.iloc[i, p + 3] == 1:
                ligne.append(1)
            else:
                ligne.append(0)
        kappa.append(ligne)

    print()
    print("kappa = [")
    for i in range(len(kappa)-1):
        print(str(kappa[i]) + ",")
    print(str(kappa[len(kappa)-1]) + "]")

creerMatrices()