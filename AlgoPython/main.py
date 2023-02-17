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

def creerAffectations(size, n):
    res = []
    base = []
    for i in range(0, size):
        base.append(i)
    for i in range(0, n):
        random.shuffle(base)
        res.append(base.copy())

    #TO REMOVE
    #res = [[10, 13, 19, 15, 5, 21, 1, 9, 3, 7, 17, 8, 6, 12, 4, 14, 20, 0, 16, 23, 18, 2, 11, 22]]
    #res = [[12,7,3,5,17,19,1,15,21,6,18,8,9,13,10,11,20,2,14,23,4,16,22,0]]
    return res


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
            while randomOpe < cardO and not amelioration:  # attention, ici, c'est injuste pour les premiers de la liste
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
def trameBase(cardO, cardS, kappa):
    n = 1  # Nombre de permutations testées
    affectations = creerAffectations(cardO, n)

    # Pour chaque affectation, on crée semaine par semaine un emploi du temps
    # Si tout n'est pas compatible, on commence par permuter les compétences complémentaires
    # Si tout n'est pas résolu de cette manière, on fait des échanges

    for iter in range(0, n): # Pas utilisé pour l'instant
        trameInit = []
        # en fonction de la première affection, on décale de 1 chaque semaine
        for s in range(0, cardS):
            affectSemaine = affectations[iter].copy()
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
            #insatSemaine.append(res[1])
            trameFinale.append(semaineFinale)
            insatSemaine = calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa)
            for i in range(0, cardO):
                # print(insatisfaction[i])
                # print(res[1])
                insatisfaction[i] += insatSemaine[i]

        # for s in range(0,cardS):
        #    print(trameInit[s])
        #    print(trameFinale[s])
        #    print()
        #
        # print("insatisfaction = ", insatisfaction)
        insatisfactionTotale = 0
        for i in range(0, cardO):
            insatisfactionTotale += insatisfaction[i]
        # print("insatisfactionTotale = ", insatisfactionTotale)
        return [insatisfactionTotale, trameInit, trameFinale]


# Appel de la fonction
#res = trameBase(24, 16, kappa)

totInsat = 0
bestInsat = 10000
nbTest = 10000
bestRes = []
nbSemaine = 18
for i in range(0, nbTest):
    res = trameBase(24, nbSemaine, kappa)
    totInsat += res[0]
    if res[0] < bestInsat:
        bestInsat = res[0]
        bestRes = res.copy()

for i in range(0, nbSemaine):
    print(bestRes[1][i])
    print(bestRes[2][i])
    print()

print("moy = ", totInsat / nbTest)
print("best = ", bestInsat)
