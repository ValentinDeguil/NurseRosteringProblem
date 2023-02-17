import sys

import pandas as pd
import numpy as np
import csv
import os
from pulp import *

# calcul de la position dans le roulement d'un poste en fonction de la semaine
def rFunction(s,p):
    return ((p-s)%24)

# calcul du numéro de semaine correspondant au jour j
def sFunction(j):
    return j//7

# calcul du jour non travaillé pour une semaine donnée d'un opérateur à 80%
# en fonction du jour non travaillé la première semaine
def delta_i(s,d_i):
    return (d_i+s)%5

def main(cardSInput):
    # operateurs + competences
    dataOperateurs = pd.read_csv('./data/operateurs.csv', sep=";")

    cardO = len(dataOperateurs.axes[0])
    colsDataOperateurs = len(dataOperateurs.axes[1])
    nomsOperateurs = dataOperateurs.iloc[0:cardO, 0:3]
    competencesOperateurs = dataOperateurs.iloc[0:cardO, 3:(colsDataOperateurs + 1)]

    # postes (intitulés + rho)
    dataPostes = pd.read_csv('./data/postes.csv', sep=";")
    cardP = len(dataPostes.axes[0])
    nomsPostes = dataPostes.iloc[0:cardO, 1]
    rho = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]

    # le nombre de semaines <=> nombre de postes <=> nombre d'opérateurs
    # cardS = cardO
    cardS = int(float(cardSInput))
    cardJ = 7 * cardS
    cardR = cardO

    # kappa_ip (opérateur possède la compétence pour le poste)
    # kappa = pd.read_csv('./data/kappa_ip.csv',sep = ";" )
    kappa = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]]

    # sigma_pp' (postes sur le même créneau horaire)
    # sigma = pd.read_csv('./data/sigma_pp.csv',sep = ";" )
    sigma = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]]

    d = [3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    delta = np.full((cardO, cardJ), 1)
    for i in range(0, cardO):
        if d[i] != -1:
            d_i = d[i]
            for s in range(0, cardS):
                d_is = delta_i(s, d_i)  # rang du jour non travaillé la semaine s
                j_s = 7 * s + d_is  # numéro du jour non travaillé
                delta[i][j_s] = 0

    # o_j (jour ouvrés)
    o = np.zeros(cardJ)
    for j in range(0, len(o)):
        if (j % 7 <= 4):
            o[j] = 1

    # H_s (jours de chaque semaine)
    H = []
    for i in range(0, cardS):
        H.append(np.zeros(7))
    for i in range(0, cardS):
        for j in range(0, 7):
            H[i][j] = (i * 7 + j)

    # x_ijp = 1 si l'opérateur prend en charge le poste p le jour j

    # y_ir = 1 si l'opérateur i est position r dans le roulement
    y = {}
    for i in range(0, cardO):
        for r in range(0, cardR):
            y[i, r] = LpVariable(f"y({i, r})", cat=LpBinary)

    # z_isp = 1 si l'opérateur est affecté au poste p la semaine s
    z = {}
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                z[i, s, p] = LpVariable(f"z({i, s, p})", cat=LpBinary)

    # u_is = 1 si l'opérateur i est affecté à un poste différent de celui prévu la semaine s
    u = {}
    for i in range(0, cardO):
        for s in range(0, cardS):
            u[i, s] = LpVariable(f"u({i, s})", cat=LpBinary)
    prob = LpProblem("ModelPlanning", LpMinimize)

    prob += sum(u[i, s] for i in range(0, cardO) for s in range(0, cardS)), "obj"

    # contrainte 1 Un opérateur ne peut prendre un poste que s'il est compétent et disponible sur un jour ouvré

    # contrainte 2 Un opérateur ne peut être affecté à un poste une semaine que s'il en possède la compétence

    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                prob += (z[i, s, p] <= kappa[i][p], f"C2_{i, s, p}")

    # contrainte 3 Chaque jour, l'opérateur est affecté à son poste de la semaine (s'il n'est pas rouleur)

    # contrainte 4 (page 8) Chaque jour, un opérateur est affecté à au plus un poste #MODIF

    # contrainte 5 (page 8) Chaque jour, chaque poste est assuré par un opérateur #MODIF

    # contrainte 6 (page 9) Chaque semaine, chaque opérateur est affecté à un poste

    for i in range(0, cardO):
        for s in range(0, cardS):
            prob += sum(z[i, s, p] for p in range(0, cardP)) == 1, f"C6_{i, s, p}"

    # contrainte 7 (page 9) Chaque semaine, chaque poste est assuré par un opérateur

    for p in range(0, cardP):
        for s in range(0, cardS):
            prob += sum(z[i, s, p] for i in range(0, cardO)) == 1, f"C7_{i, s, p}"

    # contrainte 8 (page 10) Chaque opérateur est affecté à une position dans le roulement

    for i in range(0, cardO):
        prob += sum(y[i, r] for r in range(0, cardR)) == 1, f"C8_{i, r}"

    # contrainte 9 (page 10) Chaque position dans le roulement est associée à un opérateur

    for r in range(0, cardR):
        prob += sum(y[i, r] for i in range(0, cardO)) == 1, f"C9_{i, r}"

    # contrainte 10 (page 11) Un opérateur peut changer de poste si l'horaire de ce dernier est compatible

    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                prob += z[i, s, p] <= sum(
                    sigma[p][p2] * y[i, rFunction(s, p2)] for p2 in range(0, cardP)), f"C10_{i, s, p}"

    # contrainte 11 (page 11) Lorsqu'un jour un opérateur est affecté à un poste A alors qu'il est affecté à un poste B pour cette semaine, cela augmente son score d'insatisfaction
    for i in range(0, cardO):
        for s in range(0, cardS):
            for p in range(0, cardP):
                prob += u[i, s] >= (kappa[i][p] * rho[p] * y[i, rFunction(s, p)] - z[i, s, p]), f"C11_{i, s, p}"

    import time

    prob.writeLP("Model.lp")

    start = time.time()
    prob.solve(CPLEX_PY())
    end = time.time()

    duree = end - start
    print("Temps de résolution : " + str(duree))

    print("objectif =", value(prob.objective))

    x2 = {}
    for i in range(0, cardO):
        for j in range(0, cardJ):
            for p in range(0, cardP):
                x2[i, j, p] = LpVariable(f"x({i, j, p})", cat=LpBinary)

    u2 = {}
    for i in range(0, cardO):
        for s in range(0, cardS):
            u2[i, s] = LpVariable(f"u({i, s})", cat=LpBinary)

    prob2 = LpProblem("ModelPlanning", LpMinimize)

    prob2 += sum(u2[i, s] for i in range(0, cardO) for s in range(0, cardS)), "obj"

    # contrainte 1 Un opérateur ne peut prendre un poste que s'il est compétent et disponible sur un jour ouvré

    for i in range(0, cardO):
        for j in range(0, cardJ):
            for p in range(0, cardP):
                prob2 += (x2[i, j, p] <= delta[i][j] * kappa[i][p] * o[j], f"C1_{i, j, p}")

    # contrainte 3 Chaque jour, l'opérateur est affecté à son poste de la semaine (s'il n'est pas rouleur)
    for i in range(0, cardO):
        for s in range(0, cardS):
            for j in H[s]:
                for p in range(0, cardP):
                    prob2 += x2[i, j, p] <= z[i, s, p].varValue + sum(
                        (1 - rho[p2]) * z[i, s, p2].varValue for p2 in range(0, cardP)), f"C3_{i, s, j, p}"

    # contrainte 4 (page 8) Chaque jour, un opérateur est affecté à au plus un poste #MODIF

    for i in range(0, cardO):
        for j in range(0, cardJ):
            if o[j] == 1 and delta[i][j] == 1:
                prob2 += sum(x2[i, j, p] for p in range(0, cardP)) == 1, f"C4_{i, j, p}"

    # contrainte 5 (page 8) Chaque jour, chaque poste est assuré par un opérateur #MODIF
    for p in range(0, cardP):
        for j in range(0, cardJ):
            if o[j] == 1 and rho[p] == 1:
                prob2 += sum(x2[i, j, p] for i in range(0, cardO)) == 1, f"C5_{i, j, p}"

    # contrainte 5.2 BONUS Chaque jour, un poste roulant est occupé par au plus une personne
    for p in range(0, cardP):
        for j in range(0, cardJ):
            if o[j] == 1 and rho[p] == 0:
                prob2 += sum(x2[i, j, p] for i in range(0, cardO)) <= 1, f"C52_{i, j, p}"

    for i in range(0, cardO):
        for s in range(0, cardS):
            prob2 += u2[i, s] == u[i, s].varValue, f"C6_{i, s}"

    prob2.writeLP("Model2Phase.lp")

    start = time.time()
    prob2.solve(CPLEX_PY())
    end = time.time()

    duree2 = end - start
    print("Temps de résolution : " + str(duree2))
    print("objectif =", value(prob2.objective))

    print("Temps de résolution deux phases : " + str(duree + duree2))

    with open("res2phases", "a+") as file_object:
        file_object.write("\n")
        file_object.write("cardS : " + str(cardS) + "\n")
        file_object.write("phase1 : " + str(duree) + "\n")
        file_object.write("phase2 : " + str(duree2) + "\n")
        file_object.write(("total : " + str(duree + duree2)) + "\n")

main(int(sys.argv[1]))