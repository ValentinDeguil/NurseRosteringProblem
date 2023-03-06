import random
import numpy as np
import coreFunctions
import methode2opt


# Fonction secondaire retournant une solution issue d'une population initiale, selon la méthode GRASP.
def genere1solutionGRASP(comptage, taillePop, cardO, cardS, kappa, sigma):
    # On crée un ensemble de vecteurs utiles pour générer des solutions équitables entre les opérateurs.
    randomPosition = []
    operateursRestants = []
    sol = []
    for i in range(cardO):
        randomPosition.append(i)
        operateursRestants.append(i)
        sol.append(-1)
    random.shuffle(randomPosition)
    # Ce vecteur nous permet de conserver en mémoire la somme des potentiels restants pour chaque emplacement du roulement.
    cumulRestant = np.ones(cardO)*taillePop

    for i in range(cardO):
        # Pour plus d'équité, on tire au sort un emplacement du roulement aléatoire
        position = randomPosition[i]
        # S'il ne reste pas de données sur le potentiel des opérateurs par rapport à cet emplacement,
        # alors on lui associe un opérateur libre aléatoire,
        if cumulRestant[position] == 0:
            indexOperateur = operateursRestants[random.randint(0, len(operateursRestants)-1)]
        # Sinon, on tire un opérateur au sort à partir du cumul des potentiels restants.
        # Un opérateur avec un plus grand potentiel aura plus de chances d'être sélectionné
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
        # Une fois l'opérateur choisi pour l'emplacement dans le roulement, on supprime son potentiel des autres emplacements.
        for j in range(cardO):
            cumulRetire = comptage[j][indexOperateur]
            cumulRestant[j] = cumulRestant[j] - cumulRetire # On diminue du potentiel total de l'emplacement
            comptage[j][indexOperateur] = 0                 # ainsi que le potentiel de l'opérateur.
        sol[position] = indexOperateur
        # On retire l'opérateur sélectionné de la liste des candidats pour les autres emplacements.
        operateursRestants.remove(indexOperateur)

    return coreFunctions.construireSol(cardO,cardS,kappa,sigma,False,sol.copy())


# Fonction secondaire retournant une population GRASP construite à partir d'une population de solutions aléatoires.
def constructionGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma):
    # On conserve les "taillePop" meilleures solutions parmi les "nbRunInit" générées
    pop = coreFunctions.construirePopulationSolution(taillePop, nbRunInit, cardO, cardS, kappa, sigma)
    pop.sort()

    # On mesure le potentiel de chaque opérateur par rapport à chaque emplacement dans le roulement.
    comptage = np.zeros((cardO,cardO))
    for index in range(taillePop):
        sol = pop[index]
        affectation = sol[1]
        for i in range(cardO):
            comptage[i][affectation[i]] += 1

    cpt = 0
    popFinale = []
    while cpt < taillePop:
        # On génère des solutions GRASP à partir du potentiel mesuré dans la population initiale.
        newSol = genere1solutionGRASP(comptage.copy(), taillePop, cardO, cardS, kappa, sigma).copy()
        if newSol[3]:
            cpt += 1
            popFinale.append(newSol.copy())
    return popFinale

# Fonction principale générant une population avec la méthode GRASP et qui l'améliore avec la méthode 2-opt.
def rechercheLocale2optPopulationGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma):
    # On commence par générer une population GRASP de taille "taillePopFinale" à partir de "taillePopInit" solutions aléatoires
    pop = constructionGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma)
    pop.sort()

    index = 0
    # On améliore tant qu'on peut les solutions générées par GRASP
    while index < taillePop:
        newSol = methode2opt.rechercheLocale2optSolution(pop[index], cardO, cardS, kappa, sigma)
        # si la recherche locale sur la solution donne une meilleure valeur, alors celle-ci est remplacée
        if newSol[0]:
            # l'index ne change pas et on applique à nouveau la recherche locale sur cette nouvelle solution
            pop[index] = newSol[1].copy()
        else:
            index = index + 1
            print("Chargement : ", float(index)/float(taillePop)*100, "%                  ", end='\r')

    pop.sort()
    return pop


# Retourne la somme des valeurs des fonctions objectifs de l'ensemble d'une population de solutions
def sommeInsatisfactionPopulation(pop):
    nbSolution = len(pop)
    res = 0
    for i in range(nbSolution):
        res += pop[i][0]
    return res


# Fonction principale utilisant la méthode 2-opt sur des solutions générées par GRASP
def methode2optGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma):
    # Une population initiale de solutions est créée et son insatisfaction globale est calculée
    popInit = methode2opt.rechercheLocale2optPopulation(taillePop, nbRunInit, cardO, cardS, kappa, sigma)
    insatPop = sommeInsatisfactionPopulation(popInit)
    stop = False
    # À chaque itération, on génère taillePop solutions GRASP à partir de notre population actuelle, puis
    # on les améliore avec la méthode 2 opt, on fusionne ensuite la population initiale et la nouvelle
    while not stop:
        # On mesure le potentiel des opérateurs par rapport aux emplacements dans le roulement.
        # Pour chaque solution de la population, si un opérateur i est présent à l'emplacement r du roulement,
        # alors comptage[i,r] augmente de 1, et i aura plus de chance d'être réaffecté à r plus tard.
        comptage = np.zeros((cardO, cardO))
        for index in range(taillePop):
            sol = popInit[index]
            affectation = sol[1]
            for i in range(cardO):
                comptage[i][affectation[i]] += 1

        # On construit une nouvelle population GRASP à partir de la population actuelle.
        cpt = 0
        popGRASP = []
        while cpt < taillePop: # On continue tant que l'on n'a pas généré assez de solutions faisables.
            newSol = genere1solutionGRASP(comptage.copy(), taillePop, cardO, cardS, kappa, sigma).copy()
            if newSol[3]:
                cpt += 1
                popGRASP.append(newSol.copy())

        # On améliore à l'aide de la méthode 2-opt les solutions générées par la méthode GRASP
        index = 0
        while index < taillePop:
            newSol = methode2opt.rechercheLocale2optSolution(popGRASP[index], cardO, cardS, kappa, sigma)
            # si la recherche locale sur la solution donne une meilleure valeur, alors celle-ci est remplacée
            if newSol[0]:
                # l'index ne change pas et on applique à nouveau la recherche locale sur cette nouvelle solution
                popGRASP[index] = newSol[1].copy()
            else:
                index = index + 1

        # On fusionne la population initiale et la population générée par GRASP et on ne garde que les "taillePop" meilleures
        for i in range(taillePop):
            popInit.append(popGRASP[i].copy())
        popInit.sort()
        popInit = popInit[:taillePop].copy()
        #print("actuel best = ", popInit[0][0], " : ", popInit[0][1])

        # On mesure l'insatisfaction totale de la nouvelle population obtenue, si celle-ci est meilleure,
        # alors on répète le processus, sinon la fonction s'arrête et on obtient la population finale.
        insatNewPop = sommeInsatisfactionPopulation(popInit)
        if insatPop == insatNewPop:
            stop = True
        else:
            insatPop = insatNewPop
            #print("insatNewPop = ", insatNewPop)

    return popInit



