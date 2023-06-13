import random
import numpy as np
import coreFunctions


# Fonction secondaire retournant une solution issue d'une population initiale, selon la méthode GRASP.
def genere1solutionGRASP(comptage, taillePop, cardO, cardS, kappa, sigma, rho, fac, matriceConges):
    # On crée un ensemble de vecteurs utiles pour générer des solutions équitables entre les opérateurs.
    randomPosition = []
    operateursRestants = []
    sol = []
    for i in range(cardO):
        randomPosition.append(i)
        operateursRestants.append(i)
        sol.append(-1)
    random.shuffle(randomPosition)
    # Ce vecteur nous permet de conserver en mémoire la somme des potentiels restants
    # pour chaque emplacement du roulement.
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
                    cumul += taillePop  # condition d'arrêt
                j += 1
        # Une fois l'opérateur choisi pour l'emplacement dans le roulement, on supprime son potentiel
        # des autres emplacements.
        for j in range(cardO):
            cumulRetire = comptage[j][indexOperateur]
            cumulRestant[j] = cumulRestant[j] - cumulRetire  # On diminue du potentiel total de l'emplacement
            comptage[j][indexOperateur] = 0                  # ainsi que le potentiel de l'opérateur.
        sol[position] = indexOperateur
        # On retire l'opérateur sélectionné de la liste des candidats pour les autres emplacements.
        operateursRestants.remove(indexOperateur)

    return coreFunctions.construireSol(cardO,cardS,kappa,sigma,False,sol.copy(),rho,fac, matriceConges)


# Fonction principale retournant une population GRASP construite à partir d'une population de solutions aléatoires.
def constructionGRASP(taillePop, nbRunInit, cardO, cardS, kappa, sigma, rho, fac, matriceConges):
    # On conserve les "taillePop" meilleures solutions parmi les "nbRunInit" générées
    pop = coreFunctions.construirePopulationSolution(taillePop, nbRunInit, cardO, cardS, kappa, sigma, rho, fac, matriceConges)
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
        # On génère des solutions GRASP valides à partir du potentiel mesuré dans la population initiale,
        # jusqu'à obtenir un "taillePop" solutions
        newSol = genere1solutionGRASP(comptage.copy(), taillePop, cardO, cardS, kappa, sigma, rho, fac, matriceConges).copy()
        if newSol[3]:
            cpt += 1
            popFinale.append(newSol.copy())

    popFinale.sort()
    return popFinale
