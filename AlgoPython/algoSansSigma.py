# Valentin DEGUIL Master 2 ORO
# Algorithme de construction de planning hospitalier

import random
import numpy as np
from numpy import *

# Données

kappa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
];


# Fonctions

def creerAffectations(size):
    base = []
    for i in range(0, size):
        base.append(i)
    random.shuffle(base)
    return base


def resoudreSemaine(semaine, cardO, kappa):
    #insat = zeros(cardO)
    listeOperateurs = []  # utile pour l'équité dans le remplacement
    for i in range(0, cardO):
        listeOperateurs.append(i)

    incomp = []
    for i in range(0, cardO):
        # l'opérateur i n'est pas compétent pour le poste p
        if kappa[i][semaine[i]] == 0:
            incomp.append(i)
    if len(incomp) == 0:
        stop = True
        # print("Semaine sans erreur")
        #return [semaine, insat]
        return semaine
    else:
        stop = False

    while not stop:
        amelioration = False
        # ici, on vérifie si on peut faire l'échange intelligent
        if len(incomp) >= 2:
            # print(">=2")
            i = 0
            while i < len(incomp) and not amelioration:
                j = i
                while j < len(incomp) and not amelioration:
                    # print("i = ", i, ", j = ", j)
                    # print(incomp)
                    if kappa[incomp[i]][semaine[incomp[j]]] == 1 and kappa[incomp[j]][semaine[incomp[i]]] == 1:
                        # print("on inverse", incomp[i], "et", incomp[j])
                        amelioration = True
                        temp = semaine[incomp[i]]
                        semaine[incomp[i]] = semaine[incomp[j]]
                        semaine[incomp[j]] = temp
                        operateur1 = incomp[i]
                        operateur2 = incomp[j]
                        incomp.remove(operateur1)
                        incomp.remove(operateur2)
                    else:
                        j += 1
                i += 1
        # maintenant, si incomp ne contient qu'un seul opérateur, on permute avec quelqu'un de plus compétent
        if len(incomp) == 1 or (len(incomp) >= 2 and not amelioration):
            # if len(incomp) == 1:
            #    print("cas 1 : == 1")
            # else:
            #    print("cas 2 : >= 2")
            amelioration = False
            randomOpe = 0
            random.shuffle(listeOperateurs)
            while randomOpe < cardO and not amelioration:
                i = listeOperateurs[randomOpe]
                if kappa[i][semaine[incomp[0]]] == 1 and kappa[incomp[0]][semaine[i]]:
                    # print("on inverse", incomp[0], "et", i)
                    amelioration = True
                    temp = semaine[i]
                    semaine[i] = semaine[incomp[0]]
                    semaine[incomp[0]] = temp
                    operateur1 = incomp[0]
                    incomp.remove(operateur1)
                    #insat[i] = insat[i] + 1
                randomOpe += 1

        if len(incomp) == 0:
            # print("== 0")
            stop = True

    #return [semaine, insat]
    return semaine


def calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa):
    scores = np.zeros(cardO)
    for i in range(0,cardO):
        postePrevu = semaineInit[i]
        posteFinal = semaineFinale[i]
        if kappa[i][postePrevu] == 1 and postePrevu != posteFinal:
            scores[i] = scores[i] + 1
    return scores


# Fonction majeure retournant une trame de base pour le planning durant cardS semaines.
# Elle prend en compte les compétences de chaque opérateur
def construireSol(cardO, cardS, kappa, random, semaine1):
    if random:
        affectations = creerAffectations(cardO)
    else:
        affectations = semaine1.copy()

    # Pour chaque affectation, on crée semaine par semaine un emploi du temps
    # Si tout n'est pas compatible, on commence par permuter les compétences complémentaires
    # Si tout n'est pas résolu de cette manière, on fait des échanges

    trameInit = []
    # en fonction de la première affection, on décale de 1 chaque semaine
    for s in range(0, cardS):
        affectSemaine = affectations.copy()
        for p in range(0, cardO):
            affectSemaine[p] = (affectSemaine[p] + s) % cardO
        trameInit.append(affectSemaine.copy())

    trameFinale = []
    insatisfaction = zeros(cardO)
    insatSemaine = []
    # pour chaque semaine, on observe si une personne n'est pas à un poste où elle est compétente
    for s in range(0, cardS):
        semaineInit = trameInit[s].copy()
        semaineFinale = resoudreSemaine(semaineInit.copy(), cardO, kappa)
        # insatSemaine.append(res[1])
        trameFinale.append(semaineFinale)
        insatSemaine = calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa)
        for i in range(0, cardO):
            # print(insatisfaction[i])
            # print(res[1])
            insatisfaction[i] += insatSemaine[i]

    insatisfactionTotale = 0
    for i in range(0, cardO):
        insatisfactionTotale += insatisfaction[i]
    # print("insatisfactionTotale = ", insatisfactionTotale)
    return [insatisfactionTotale, affectations, trameFinale]

def construirePopulationSolution(taillePop, nbRun, cardO, nbSemaines, kappa):

    topSolutions = []
    bestInsat = 9999
    worstInsat = -1

    for i in range(0, taillePop):
        sol = construireSol(cardO, nbSemaines, kappa, True, None)
        topSolutions.append(sol)
        valueSol = sol[0]
        if valueSol < bestInsat:
            bestInsat = valueSol

        if valueSol > worstInsat:
            worstInsat = valueSol


    for i in range(0,nbRun-taillePop):
        sol = construireSol(cardO, nbSemaines, kappa, True, None)
        valueSol = sol[0]
        if valueSol < worstInsat :
            found = False
            i = 0
            while not found and i < taillePop:
                if topSolutions[i][0] > valueSol:
                    found = True
                    topSolutions[i] = sol.copy()
                else:
                    i = i + 1

    return topSolutions

def tabuSearch(solInit, cardO, cardS, kappa):
    found = False
    semaine1Init = solInit[1]
    valueInit = solInit[0]
    i = 0
    while not found and i < (cardO - 1):
        j = i + 1
        while not found and j < cardO:
            newSolSemaine1 = semaine1Init.copy()
            temp = newSolSemaine1[i]
            newSolSemaine1[i] = newSolSemaine1[j]
            newSolSemaine1[j] = temp
            newSol = construireSol(cardO, cardS, kappa, False, newSolSemaine1)
            valueNewSol = newSol[0]
            if valueNewSol < valueInit:
                found = True
            j = j + 1

        i = i + 1
    if found:
        return [True, newSol]
    else:
        return  [False, None]

def test(taillePop, nbRunInit, cardO, cardS, kappa):
    pop = construirePopulationSolution(taillePop, nbRunInit, cardO, cardS, kappa)
    pop.sort()

    print("Avant")
    for i in range(0,taillePop):
        print(pop[i][0], " : ", pop[i][1])

    stop = False
    index = 0
    while not stop and index < taillePop:
        newSol = tabuSearch(pop[index], cardO, cardS, kappa)
        #print("on cherche", index)
        #si on trouve une meilleure solution, on remplace
        if newSol[0]:
            #print("Amélioration")
            pop[index] = newSol[1].copy()
            valueNewSol = newSol[1][0]
            pop.sort()
            foundNewIndex = False
            newIndex = 0
            while not foundNewIndex and newIndex < taillePop:
                if valueNewSol <= pop[newIndex][0]:
                    foundNewIndex = True
                    index = newIndex
                    print(newIndex)
                else:
                    newIndex = newIndex + 1
        else:
            index = index + 1

    print("Après")
    for i in range(0, taillePop):
        print(pop[i][0], " : ", pop[i][1])

    print("verif")


    #print("code")
    #for index in range(0, taillePop):
    #    if pop[index][0] == 4:
    #        res = np.zeros((24,24))
    #        for i in range(0,24):
    #            res[i, pop[index][2][0][i]] = 1
    #        print(res)


test(20, 20, 24, 24, kappa)

# Pour construire une solution et obtenir la matrice des Y_ir
#sol = construireSol(24, 14, kappa, False, [12,7,3,5,17,19,1,15,21,6,18,8,9,13,10,11,20,2,14,23,4,16,22,0])
#print("sol = ", sol[0])
#res = np.zeros((24,24))
#for i in range(0,24):
#    res[i, sol[2][0][i]] = 1
#print(res)
#print(sol[2][0])
#print(sol[1][0])

# Appel de la fonction
#res = trameBase(24, 16, kappa)

#totInsat = 0
#bestInsat = 10000
#nbTest = 10000
#bestRes = []
#nbSemaines = 15
#for i in range(0, nbTest):
#    res = construireSol(24, nbSemaines, kappa)
#    totInsat += res[0]
#    if res[0] < bestInsat:
#        bestInsat = res[0]
#        bestRes = res.copy()
#
#for i in range(0, nbSemaine):
#    print(bestRes[1][i])
#    print(bestRes[2][i])
#    print()
#
#print("moy = ", totInsat / nbTest)
#print("best = ", bestInsat)
