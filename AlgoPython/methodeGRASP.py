import random
import numpy as np
import coreFunctions
import methode2opt

def genere1solutionGRASP(comptage, taillePop, cardO, cardS, kappa, sigma):
    randomPosition = []
    operateursRestants = []
    sol = []
    for i in range(cardO):
        randomPosition.append(i)
        operateursRestants.append(i)
        sol.append(-1)
    random.shuffle(randomPosition)
    cumulRestant = np.ones(cardO)*taillePop

    for i in range(cardO):
        position = randomPosition[i]
        if cumulRestant[position] == 0:
            indexOperateur = operateursRestants[random.randint(0, len(operateursRestants)-1)]
        else:
            randOperateur = random.randint(1, cumulRestant[position])
            cumul = 0
            j = 0
            indexOperateur = -1
            while j < cardO and cumul < cumulRestant[position]:
                cumul += comptage[position][j]
                if cumul >= randOperateur:
                    indexOperateur = j
                    cumul += taillePop #condition d'arrêt
                j += 1
        for j in range(cardO):
            cumulRetire = comptage[j][indexOperateur]
            cumulRestant[j] = cumulRestant[j] - cumulRetire
            comptage[j][indexOperateur] = 0
        sol[position] = indexOperateur
        operateursRestants.remove(indexOperateur)
    return coreFunctions.construireSol(cardO,cardS,kappa,sigma,False,sol.copy())

def constructionGRASP(taillePopInit, taillePopFinale, nbRunInit, cardO, cardS, kappa, sigma):
    pop = coreFunctions.construirePopulationSolution(taillePopInit, nbRunInit, cardO, cardS, kappa, sigma)
    pop.sort()

    comptage = np.zeros((cardO,cardO))
    for index in range(taillePopInit):
        sol = pop[index]
        affectation = sol[1]
        for i in range(cardO): #la position i, on augmente de 1 à la position de l'opérateur assigné
            comptage[i][affectation[i]] += 1
    #print(comptage)

    #for i in range(0,taillePop):
    #    print(pop[i][0], " : ", pop[i][1])
    print("meilleur = ", pop[0][0])
    print("pire = ", pop[taillePopInit-1][0])

    cpt = 0
    popFinale = []
    while cpt < taillePopFinale:
        newSol = genere1solutionGRASP(comptage.copy(), taillePopInit, cardO, cardS, kappa, sigma).copy()
        if newSol[3]:
            cpt += 1
            popFinale.append(newSol.copy())
    return popFinale

def rechercheLocale2optPopulationGRASP(taillePopInit, taillePopFinale, nbRunInit, cardO, cardS, kappa, sigma):
    # on construit la population de solutions initiale
    pop = constructionGRASP(taillePopInit, taillePopFinale, nbRunInit, cardO, cardS, kappa, sigma)
    pop.sort()

    #print("Avant")
    #for i in range(0,taillePop):
    #    print(pop[i][0], " : ", pop[i][1])

    stop = False
    index = 0
    while not stop and index < taillePopFinale:
        newSol = methode2opt.rechercheLocale2optSolution(pop[index], cardO, cardS, kappa, sigma)
        # si la recherche locale sur la solution donne une meilleure valeur, alors celle-ci est remplacée
        if newSol[0]:
            # l'index ne change pas et on applique à nouveau la recherche locale sur cette nouvelle solution
            pop[index] = newSol[1].copy()
        else:
            index = index + 1
            print("Chargement : ", float(index)/float(taillePopFinale)*100, "%                  ", end='\r')

    pop.sort()
    #print("Après")
    #for i in range(0, taillePop):
    #    print(pop[i][0], " : ", pop[i][1])
    #print()
    return pop


# Retourne la somme des valeurs des fonctions objectifs de l'ensemble d'une population de solutions
def sommeInsatisfactionPopulation(pop):
    nbSolution = len(pop)
    res = 0
    for i in range(nbSolution):
        res += pop[i][0]
    return res

def methode2optGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma):
    popInit = methode2opt.rechercheLocale2optPopulation(taillePop, nbRunInit, cardO, cardS, kappa, sigma)
    insatPop = sommeInsatisfactionPopulation(popInit)
    stop = False
    # À chaque itération, on génère taillePop solutions GRASP à partir de notre population actuelle, puis
    # on les améliore avec la méthode 2 opt, on fusionne ensuite la population initiale et la nouvelle
    while not stop:
        # on compte le potentiel des opérateurs par rapport aux emplacements dans le roulement
        comptage = np.zeros((cardO, cardO))
        for index in range(taillePop):
            sol = popInit[index]
            affectation = sol[1]
            for i in range(cardO):  # la position i, on augmente de 1 à la position de l'opérateur assigné
                comptage[i][affectation[i]] += 1

        # on construit une nouvelle population GRASP à partir de la population actuelle
        cpt = 0
        popGRASP = []
        while cpt < taillePop:
            newSol = genere1solutionGRASP(comptage.copy(), taillePop, cardO, cardS, kappa, sigma).copy()
            if newSol[3]:
                cpt += 1
                popGRASP.append(newSol.copy())

        #stop2opt = False
        index = 0
        while index < taillePop:
            newSol = methode2opt.rechercheLocale2optSolution(popGRASP[index], cardO, cardS, kappa, sigma)
            # si la recherche locale sur la solution donne une meilleure valeur, alors celle-ci est remplacée
            if newSol[0]:
                # l'index ne change pas et on applique à nouveau la recherche locale sur cette nouvelle solution
                popGRASP[index] = newSol[1].copy()
            else:
                index = index + 1

        #print("popInit")
        #for i in range(0, taillePop):
        #    print(popInit[i][0], " : ", popInit[i][1])
        #print("popGRASP")
        #for i in range(0, taillePop):
        #    print(popGRASP[i][0], " : ", popGRASP[i][1])

        for i in range(taillePop):
            popInit.append(popGRASP[i].copy())
        popInit.sort()
        popInit = popInit[:taillePop].copy()
        print("actuel best = ", popInit[0][0], " : ", popInit[0][1])

        #print("newPop")
        #for i in range(0, taillePop):
        #    print(popInit[i][0], " : ", popInit[i][1])

        insatNewPop = sommeInsatisfactionPopulation(popInit)
        if insatPop == insatNewPop:
            stop = True
        else:
            insatPop = insatNewPop
            print("insatNewPop = ", insatNewPop)

    print("newPop")
    for i in range(0, taillePop):
        print(popInit[i][0], " : ", popInit[i][1])

    return popInit



