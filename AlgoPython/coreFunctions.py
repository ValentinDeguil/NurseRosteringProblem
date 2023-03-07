import random
import numpy as np
from scipy.optimize import linear_sum_assignment

# Retourne une affectation aléatoire des opérateurs aux positions dans le roulement (vecteur y_ir)
def creerAffectations(size):
    base = []
    for i in range(0, size):
        base.append(i)
    random.shuffle(base)
    return base


# Fonction principale permettant de résoudre de manière optimale les problèmes d'opérateurs mal affectés
def resoudreSemaineHongrois(semaine, cardO, kappa, sigma):

    # On crée ici la matrice des coûts de chaque association opérateur/position dans le roulement.
    # Le coût vaut 10000 si la personne est incompétente ou si son poste actuel n'est pas sur le même créneau horaire.
    # Le coût vaut 0 s'il s'agit du poste prévu pour l'opérateur dans le roulement.
    # Le coût vaut 1 s'il s'agit d'un poste dont l'opérateur possède la compétence, situé sur le même créneau horaire
    # et différent de son poste prévu par le roulement.
    matrice = []
    for i in range(cardO):
        ligneI = []
        posteI = semaine[i]
        if kappa[i][posteI] == 0:
            for p in range(cardO):
                if kappa[i][p] == 0 or sigma[posteI][p] == 0:
                    ligneI.append(10000)
                else:
                    ligneI.append(0)
        else:
            for p in range(cardO):
                if kappa[i][p] == 0 or sigma[posteI][p] == 0:
                    ligneI.append(10000)
                elif p == posteI:
                    ligneI.append(0)
                else:
                    ligneI.append(1)

        matrice.append(ligneI)

    # On appelle la fonction linear_sum_assignment de la librairie scipy, qui utilise l'algorithme hongrois
    # (algorithme de Kuhn-Munkres) afin de résoudre le problème d'affectation de poids minimum.
    cost = np.array(matrice)
    row_ind, col_ind = linear_sum_assignment(cost)
    insat = cost[row_ind, col_ind].sum()

    # Si le poids retourné par l'algorithme hongrois est supérieur à 10000, alors on est dans le cas où il n'est
    # pas possible de trouver une solution au problème sans changer le créneau horaire d'un opérateur ou dans le
    # cas où un poste ne peut être pris en charge par personne.
    if insat < 10000:
        newSemaine = []
        for i in range(cardO):
            newSemaine.append(col_ind[i])
        # Le booléen représente la faisabilité de la solution
        return newSemaine, True
    else:
        return semaine, False


# Fonction secondaire permettant de calculer l'insatisfaction de chaque opérateur à la partir de la
# semaine initiale prévue et de sa version réparée (lorsque des opérateurs étaient incompétents)
def calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa):
    scores = np.zeros(cardO)
    for i in range(0,cardO):
        postePrevu = semaineInit[i]
        posteFinal = semaineFinale[i]
        # un opérateur est insatisfait si son poste final est différent de son poste final
        # alors qu'il était compétent pour le premier
        if kappa[i][postePrevu] == 1 and postePrevu != posteFinal:
            scores[i] = scores[i] + 1
    return scores


# Fonction principale retournant une trame de base pour le planning durant cardS semaines.
# Elle prend en compte les compétences de chaque opérateur
def construireSol(cardO, cardS, kappa, sigma, isRandom, affectationsRoulement):
    # isRandom est utile pour la recherche locale, on peut ainsi choisir un vecteur Y_ir aléatoire ou non
    if isRandom:
        affectations = creerAffectations(cardO)
    else:
        affectations = affectationsRoulement.copy()

    trameInit = [] # on crée la trame initiale pour toutes les semaines en fonction du vecteur Y_ir (affectations)
    for s in range(0, cardS):
        affectSemaine = affectations.copy()
        for p in range(0, cardO):
            affectSemaine[p] = (affectSemaine[p] + s) % cardO # décale de 1 chaque semaine le poste effectué par un opérateur
        trameInit.append(affectSemaine.copy())

    # À partir de la trame de base, on répare les semaines où des opérateurs sont affectés à des postes où ils sont incompétents
    trameFinale = []
    insatisfaction = np.zeros(cardO)
    # Pour chaque semaine, on observe si une personne est à un poste où elle n'est pas compétente
    # Si pour une semaine donnée, aucune affectation n'est possible, on retourne une solution vide
    for s in range(0, cardS):
        semaineInit = trameInit[s].copy()
        #print("semaine", s)
        semaineFinale, faisable = resoudreSemaineHongrois(semaineInit.copy(), cardO, kappa, sigma)
        if not faisable:
            return [None, None, None, False]
        trameFinale.append(semaineFinale)
        insatSemaine = calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa)
        #print("avant :", semaineInit)
        #print("apres :", semaineFinale)
        #print("insatSemaine :", insatSemaine)
        for i in range(0, cardO):
            insatisfaction[i] += insatSemaine[i]

    # On fait la somme de l'insatisfaction de chaque opérateur
    insatisfactionTotale = 0
    for i in range(0, cardO):
        insatisfactionTotale += insatisfaction[i]

    # La solution retournée est au format [valeur fonction objectif, Y_ir, z_isp, estFaisable]
    return [insatisfactionTotale, affectations, trameFinale, True]

# Fonction principale permettant de construire une population de solutions, ne conservant que les meilleures
def construirePopulationSolution(taillePop, nbRun, cardO, nbSemaines, kappa, sigma):

    # Variables permettant de conserver les solutions actuellement dans la population
    # ainsi que les valeurs de la meilleure et de la pire
    topSolutions = []
    bestInsat = 9999
    worstInsat = -1

    i = 0 # on continue de générer des solutions jusqu'à en avoir le nombre minimum requis
    while i < taillePop:
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None)
        # si la solution générée est faisable (par rapport aux compétences des opérateurs),
        # on met à jour les différentes informations
        if sol[3]:
            topSolutions.append(sol)
            valueSol = sol[0]
            if valueSol < bestInsat:
                bestInsat = valueSol

            if valueSol > worstInsat:
                worstInsat = valueSol
            i = i+1

    topSolutions.sort()

    # On pourrait mettre ça à la place de la suite, sans doute plus optimisé pour de petits nombres de "nbRun"
    #for i in range(0, nbRun - taillePop):
    #    sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None)
    #    if sol[3]:
    #        topSolutions.append(sol.copy())
    #topSolutions.sort()
    #return topSolutions[:taillePop]

    for i in range(0,nbRun-taillePop):
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None)
        valueSol = sol[0]
        if sol[3]: # si la nouvelle solution est faisable...
            if valueSol < worstInsat: # et meilleure que la pire solution de la solution...
                # alors, on met à jour notre population.
                # Deux cas sont possibles, cas 1 : la solution générée est la nouvelle meilleure
                if bestInsat >= valueSol:
                    bestInsat = valueSol
                    newTopSolutions = [sol.copy()]
                    for k in range(0, taillePop - 1):
                        newTopSolutions.append(topSolutions[k].copy())
                    topSolutions = newTopSolutions.copy()
                else :
                    # cas 2 : la solution générée se situe quelque part au milieu de la population
                    found = False
                    j = taillePop - 1
                    # on effectue la recherche de l'index où insérer la nouvelle solution par la fin
                    # il est en effet très rare de générer des solutions très bonnes
                    while not found and j >= 0:
                        if topSolutions[j][0] <= valueSol:
                            found = True
                            newTopSolutions = []
                            for k in range(0,j+1):
                                newTopSolutions.append(topSolutions[k].copy())
                            newTopSolutions.append(sol.copy())
                            for k in range(j+1,taillePop-1):
                                newTopSolutions.append(topSolutions[k].copy())
                            topSolutions = newTopSolutions.copy()
                            worstInsat = topSolutions[taillePop-1][0]
                        else:
                            j += -1
    return topSolutions
