import sys


def rFunction(s, p, cardR):
    return (p - s) % cardR


def main(path, isVerbose, isDebug):
    verbose = isVerbose.lower() == 'true'
    debug = isDebug.lower() == 'true'
    file = open(path, 'r')
    lines = file.readlines()
    cardO = int(lines[0])
    cardP = int(lines[1])
    cardR = int(lines[2])
    cardS = int(lines[3])
    cardJ = 7 * cardS

    if verbose or debug:
        print("cardO = ", cardO)
        print("cardP = ", cardP)
        print("cardR = ", cardR)
        print("cardS = ", cardS)

    rho = []
    dataRho = lines[4]
    for i in range(cardP):
        rho.append(int(dataRho[i]))

    if verbose or debug:
        print("rho = ", rho)

    fac = []
    dataFac = lines[5]
    for p in range(cardP):
        if dataFac[p] == "1":
            fac.append(p)

    if verbose or debug:
        print("fac = ", fac)

    o = []
    dataO = lines[6]
    for i in range(cardJ):
        o.append(int(dataO[i]))

    if debug:
        print("o = ", o)

    H = []
    temp = []
    for index in range(7):
        temp.append(0)
    for i in range(0, cardS):
        H.append(temp.copy())
    for s in range(0, cardS):
        for j in range(7):
            H[s][j] = int(s * 7 + j)

    if debug:
        print("H = ", H)

    cpt = 7
    kappa = []
    for i in range(cardO):
        kappaI = []
        dataKappaI = lines[cpt + i]
        for p in range(0, cardP):
            kappaI.append(int(dataKappaI[p]))
        kappa.append(kappaI)
    cpt += cardO

    if debug:
        print("kappa =")
        for i in range(cardO):
            print(kappa[i])

    sigma = []
    for p in range(cardP):
        sigmaP = []
        dataSigmaP = lines[cpt + p]
        for p2 in range(cardP):
            sigmaP.append(int(dataSigmaP[p2]))
        sigma.append(sigmaP)
    cpt += cardP

    if debug:
        print("sigma = ")
        for p in range(cardP):
            print(sigma[p])

    delta = []
    for i in range(cardO):
        deltaI = []
        dataDeltaI = lines[cpt + i]
        for j in range(0, cardJ):
            deltaI.append(int(dataDeltaI[j]))
        delta.append(deltaI)
    cpt += cardO

    if debug:
        print("delta = ")
        for i in range(cardO):
            print(delta[i])

    poids1 = int(lines[cpt])
    poids2 = int(lines[cpt+1])
    poids3 = int(lines[cpt+2])
    poids4 = int(lines[cpt+3])
    cpt += 4

    if verbose or debug:
        print("poids1 =", poids1)
        print("poids2 =", poids2)
        print("poids3 =", poids3)
        print("poids4 =", poids4)

    x = []
    for i in range(cardO):
        xI = []
        for j in range(cardJ):
            xIJ = []
            dataXIJ = lines[cpt + i * cardJ + j]
            for p in range(cardP):
                xIJ.append(int(dataXIJ[p]))
            xI.append(xIJ)
        x.append(xI)
    cpt += cardO * cardJ

    if debug:
        for index in range(len(x)):
            print("x[i=" + str(index) + "] =", x[index])

    y = []
    for i in range(cardO):
        yI = []
        dataYI = lines[cpt + i]
        for r in range(cardR):
            yI.append(int(dataYI[r]))
        y.append(yI)
    cpt += cardO

    if verbose or debug:
        vectorY = []
        for i in range(cardO):
            for r in range(cardR):
                if y[i][r] == 1:
                    vectorY.append(r)
        print("y =", vectorY)

    if debug:
        for index in range(len(y)):
            print("y[" + str(index) + "] =", y[index])

    z = []
    for i in range(0, cardO):
        zI = []
        for s in range(0, cardS):
            zIS = []
            dataZIS = lines[cpt + i * cardS + s]
            for p in range(0, cardP):
                zIS.append(int(dataZIS[p]))
            zI.append(zIS)
        z.append(zI)
    cpt += cardO * cardS

    if debug:
        for index in range(len(z)):
            print("z[i=" + str(index) + "] =", z[index])

    valueObj = int(lines[cpt])
    cpt += 1

    if verbose or debug:
        print("valueObj =", valueObj)

    test = []
    for index in range(12):
        test.append(True)

    # Test contrainte 0 :
    for i in range(cardO):
        for j in range(cardJ):
            for p in range(cardP):
                if x[i][j][p] > delta[i][j] * kappa[i][p] * o[j]:
                    test[0] = False

    # Test contrainte 1 :
    for i in range(cardO):
        for s in range(cardS):
            for p in range(cardP):
                if z[i][s][p] > kappa[i][p]:
                    test[1] = False

    # Test contrainte 2 :
    for i in range(cardO):
        for s in range(cardS):
            for j in H[s]:
                for p in range(cardP):
                    if x[i][j][p] > z[i][s][p] + sum((1 - rho[p2]) * z[i][s][p2] for p2 in range(cardP)):
                        test[2] = False

    # Test contrainte 3 :
    for i in range(cardO):
        for j in range(cardJ):
            if o[j] == 1 and delta[i][j] == 1:
                if sum(x[i][j][p] for p in range(cardP)) != 1:
                    test[3] = False

    # Test contrainte 4 :
    for p in range(cardP):
        for j in range(cardJ):
            if o[j] == 1 and rho[p] == 1 and p not in fac:
                if sum(x[i][j][p] for i in range(cardO)) != 1:
                    test[4] = False

    # Test contrainte 5 :
    for p in range(cardP):
        for j in range(cardJ):
            if o[j] == 1 and (rho[p] == 0 or p in fac):
                if sum(x[i][j][p] for i in range(cardO)) > 1:
                    test[5] = False

    # Test contrainte 6 :
    for i in range(cardO):
        for s in range(cardS):
            if sum(z[i][s][p] for p in range(cardP)) > 1:
                test[6] = False

    # Test contraintes 7 et 8:
    for p in range(cardP):
        for s in range(cardS):
            if p not in fac:
                if sum(z[i][s][p] for i in range(cardO)) != 1:
                    test[7] = False
            else:
                if sum(z[i][s][p] for i in range(cardO)) > 1:
                    test[8] = False

    # Test contrainte 9 :
    for i in range(cardO):
        if sum(y[i][r] for r in range(cardR)) != 1:
            test[9] = False

    # Test contrainte 10 :
    for r in range(cardR):
        if sum(y[i][r] for i in range(cardO)) != 1:
            test[10] = False

    # Test contrainte 11 (calcul valeur fonction objectif) :
    cptPoids1 = 0
    cptPoids2 = 0
    cptPoids3 = 0
    cptPoids4 = 0
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                for p2 in range(cardP):
                    if p != p2:
                        if sigma[p][p2] == 0:
                            if rho[p] == 1 and rho[p2] == 0:
                                if y[i][rFunction(s, p, cardR)] + z[i][s][p2] - 1 == 1:
                                    cptPoids2 += 1
                                if y[i][rFunction(s, p, cardR)] + z[i][s][p2] - 1 == 1:
                                    cptPoids4 += 1
                            else:
                                if y[i][rFunction(s, p, cardR)] + z[i][s][p2] - 1 == 1:
                                    cptPoids4 += 1
                        else:
                            if rho[p] == 1 and rho[p2] == 0:
                                if y[i][rFunction(s, p, cardR)] + z[i][s][p2] - 1 == 1:
                                    cptPoids2 += 1

    for i in range(cardO):
        for s in range(cardS):
            for p in range(cardP):
                r = rFunction(s, p, cardR)
                if kappa[i][p] + y[i][r] + (1 - z[i][s][p]) - 2 == 1:
                    cptPoids1 += 1

    for p in range(cardP):
        for s in range(cardS):
            if p in fac:
                if 1 - sum(z[i][s][p] for i in range(cardO)) == 1:
                    cptPoids3 += 1

    valeurCalculeeFonctionObj = cptPoids1*poids1 + cptPoids2*poids2 + cptPoids3*poids3 + cptPoids4*poids4
    if valueObj != valeurCalculeeFonctionObj:
        test[11] = False

    echec = False
    for i in range(12):
        if not test[i]:
            print("Echec du test ", i)
            echec = True

    if echec:
        print("La solution n'est pas valide")
    else:
        print("La solution est valide (tous les tests sont validés)")


main(sys.argv[1], sys.argv[2], sys.argv[3])