import pandas as pd
def readData():
    data = pd.read_csv('data2020/data2020.csv', sep = ",", header=None)

    nbRow = len(data.axes[0])
    nbCol = len(data.axes[1])

    rho = []
    for i in range(4, nbCol):
        rho.append(int(data.iloc[0,i]))

    creneaux = []
    for i in range(4, nbCol):
        creneaux.append(int(data.iloc[1, i]))

    sigma = []
    for p1 in range(len(creneaux)):
        ligne = []
        for p2 in range(len(creneaux)):
            if creneaux[p1] == creneaux[p2]:
                ligne.append(1)
            else:
                ligne.append(0)
        sigma.append(ligne)

    nomsPostes = []
    for i in range(4, nbCol):
        nomsPostes.append(data.iloc[2,i])

    nomsOperateurs = []
    for j in range(3, nbRow):
        nomsOperateurs.append([data.iloc[j,0], data.iloc[j,1]])

    d = []
    for j in range(3, nbRow):
        if int(data.iloc[j,2]) == 100:
            d.append(-1)
        else:
            if data.iloc[j,3] == 'Lundi':
                d.append(0)
            if data.iloc[j,3] == 'Mardi':
                d.append(1)
            if data.iloc[j,3] == 'Mercredi':
                d.append(2)
            if data.iloc[j,3] == 'Jeudi':
                d.append(3)
            if data.iloc[j,3] == 'Vendredi':
                d.append(4)

    kappa = []
    for i in range(3, nbRow):
        ligne = []
        for j in range(4, nbCol):
            ligne.append(int(data.iloc[i,j]))
        kappa.append(ligne)

    #print(rho)
    #print(creneaux)
    for i in range(len(sigma)):
        a = 0 # pour l'interpreteur
        #print(sigma[i])
    #print(nomsPostes)
    #print(nomsOperateurs)
    #print(d)
    for i in range(len(sigma)):
        a = 0 # pour l'interpreteur
        #print(kappa[i])

    return kappa, sigma, rho, d, nomsPostes, nomsOperateurs
