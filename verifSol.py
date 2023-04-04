import sys
import numpy as np

def rFunction(s,p):
    return ((p-s)%24)
def main(path):
    file = open(path, 'r')
    lines = file.readlines()
    cardO = int(lines[0])
    cardP = int(lines[1])
    cardR = int(lines[2])
    cardS = int(lines[3])
    cardJ = 7*cardS

    #print("cardO = ", cardO)
    #print("cardP = ", cardP)
    #print("cardR = ", cardR)
    #print("cardS = ", cardS)

    rho = []
    dataRho = lines[4]
    for i in range(0,cardP):
        rho.append(int(dataRho[i]))
    #print("rho = ", rho)

    o = []
    dataO = lines[5]
    for i in range(0,cardJ):
        o.append(int(dataO[i]))
    #print("o = ", o)

    H = []
    temp = []
    for index in range(0, 7):
        temp.append(0)
    for i in range(0, cardS):
        H.append(temp.copy())
    for s in range(0, cardS):
        for j in range(0, 7):
            H[s][j] = int(s * 7 + j)
    #print(H)

    cpt = 6
    kappa = []
    for i in range(0,cardO):
        kappaI = []
        dataKappaI = lines[cpt + i]
        for p in range(0,cardP):
            kappaI.append(int(dataKappaI[p]))
        kappa.append(kappaI)
    cpt += cardO
    #print("kappa = ", kappa)

    sigma = []
    for p in range(0, cardP):
        sigmaP = []
        dataSigmaP = lines[cpt + p]
        for p2 in range(0, cardP):
            sigmaP.append(int(dataSigmaP[p2]))
        sigma.append(sigmaP)
    cpt += cardP
    #print("sigma = ", sigma)

    delta = []
    for i in range(0,cardO):
        deltaI = []
        dataDeltaI = lines[cpt + i]
        for j in range(0,cardJ):
            deltaI.append(int(dataDeltaI[j]))
        delta.append(deltaI)
    cpt += cardO
    #print("delta = ", delta)

    x = []
    for i in range(0,cardO):
        xI = []
        for j in range(0,cardJ):
            xIJ = []
            dataXIJ = lines[cpt+i*cardJ+j]
            for p in range(0,cardP):
                xIJ.append(int(dataXIJ[p]))
            xI.append(xIJ)
        x.append(xI)
    cpt += cardO*cardJ
    #print("x = ", x)

    y = []
    for i in range(0,cardO):
        yI = []
        dataYI = lines[cpt+i]
        for r in range(0,cardR):
            yI.append(int(dataYI[r]))
        y.append(yI)
    cpt += cardO
    #print("y = ",y)

    z = []
    for i in range(0,cardO):
        zI = []
        for s in range(0,cardS):
            zIS = []
            dataZIS = lines[cpt+i*cardS+s]
            for p in range(0,cardP):
                zIS.append(int(dataZIS[p]))
            zI.append(zIS)
        z.append(zI)
    cpt += cardO*cardS
    #print("z = ", z)

    valueObj = int(lines[cpt])
    cpt += 1

    #print("valueObj = ", valueObj)

    test = [True, True, True, True, True, True, True, True, True, True, True, True]
    # Test 1 :
    for i in range(0, cardO):
        for j in range(0, cardJ):
            for p in range(0, cardP):
                if x[i][j][p] > delta[i][j] * kappa[i][p] * o[j]:
                    print("test0 : i =", i, "j =", j, "p =",p)
                    test[0] = False

    # Test 2 :
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                if z[i][s][p] > kappa[i][p]:
                    test[1] = False

    # Test 3 :
    for i in range(0, cardO):
        for s in range(0, cardS):
            for j in H[s]:
                for p in range(0, cardP):
                    if x[i][j][p] > z[i][s][p] + sum((1 - rho[p2]) * z[i][s][p2] for p2 in range(0, cardP)):
                        test[2] = False

    # Test 4 :
    for i in range(0, cardO):
        for j in range(0, cardJ):
            if o[j] == 1 and delta[i][j] == 1:
                if sum(x[i][j][p] for p in range(0, cardP)) != 1:
                    #print("test3 : i =", i, "j =", j)
                    test[3] = False

    # Test 5 :
    for p in range(0, cardP):
        for j in range(0, cardJ):
            if o[j] == 1 and rho[p] == 1:
                if sum(x[i][j][p] for i in range(0, cardO)) != 1:
                    #print("test4 : p =", p, "j =", j, "et vaut", sum(x[i][j][p] for i in range(0, cardO)))
                    test[4] = False

    # Test 6 :
    for p in range(0, cardP):
        for j in range(0, cardJ):
            if o[j] == 1 and rho[p] == 0:
                if sum(x[i][j][p] for i in range(0, cardO)) > 1:
                    test[5] = False

    # Test 7 :
    for i in range(0, cardO):
        for s in range(0, cardS):
            if sum(z[i][s][p] for p in range(0, cardP)) > 1:
                test[6] = False

    # Test 8 :
    for p in range(0, cardP):
        for s in range(0, cardS):
            if sum(z[i][s][p] for i in range(0, cardO)) != 1:
                test[7] = False

    # Test 9 :
    for i in range(0, cardO):
        if sum(y[i][r] for r in range(0, cardR)) != 1:
            test[8] = False

    # Test 10 :
    for r in range(0, cardR):
        if sum(y[i][r] for i in range(0, cardO)) != 1:
            test[9] = False

    # Test 11 :
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                if z[i][s][p] > sum(sigma[p][p2] * y[i][rFunction(s, p2)] for p2 in range(0, cardP)):
                    print("test 10 faux :",i,s,p)
                    #for index in range(cardP):
                        #print("index",i, "", sigma[p][index] * y[i][rFunction(s, index)])
                    test[10] = False

    # Test 12 :
    sol = 0
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                if kappa[i][p] * rho[p] * y[i][rFunction(s, p)] - z[i][s][p] >= 1:
                    sol += 1
    print("sol =", sol)
    print("valueObj =", valueObj)
    if sol != valueObj:
        test[11] = False

    echec = False
    for i in range(len(test)):
        if not test[i]:
            print("Echec du test ", i)
            echec = True

    if echec:
        print("La solution n'est pas valide")
    else:
        print("La solution est valide (tous les tests sont validés)")
main(sys.argv[1])