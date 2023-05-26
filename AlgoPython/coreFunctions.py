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
def resoudreSemaineHongrois(semaine, cardO, kappa, sigma, rho, fac):
    # On crée ici la matrice des coûts de chaque association opérateur/position dans le roulement.
    # Le coût vaut 10000 si la personne est incompétente ou si son poste actuel n'est pas sur le même créneau horaire.
    # Le coût vaut 0 s'il s'agit du poste prévu pour l'opérateur dans le roulement.
    # Le coût vaut 1 s'il s'agit d'un poste dont l'opérateur possède la compétence, situé sur le même créneau horaire
    # et différent de son poste prévu par le roulement.
    #print("resoudre semaine hongrois", semaine)
    poids1 = 1
    poids2 = 10
    poids3 = 100
    poids4 = 1000
    matrice = []
    for i in range(cardO):
        ligneI = []
        posteI = semaine[i]
        for p in range(cardO):
            poids = 0
            #print("début poids = 0")
            if p == posteI:
                #print("même poste")
                if kappa[i][p] == 1:
                    poids = 0
                else:
                    if p in fac:
                        poids = poids3
                    else:
                        poids = 100000
            else:
                #print("poste diff")
                if p in fac:
                    if kappa[i][p] == 0:
                        poids = poids3
                    else:
                        if kappa[i][posteI] == 1:
                            poids += poids1
                        # Si un opérateur affecté à un poste non rouleur devient rouleur, alors il est insatisfait
                        if rho[p] == 0 and rho[posteI] == 1:
                            poids += poids2
                        # Si l'horaire d'un opérateur est modifié, alors il est insatisfait
                        if sigma[posteI][p] == 0:
                            poids += poids4
                else:
                    if kappa[i][p] == 0:
                        #print("pas compétent pour le nouveau poste")
                        poids += 100000
                    else:
                        #print("compétent pour le nouveau poste")
                        if kappa[i][posteI] == 1:
                            poids += poids1
                        # Si un opérateur affecté à un poste non rouleur devient rouleur, alors il est insatisfait
                        if rho[p] == 0 and rho[posteI] == 1:
                            poids += poids2
                        # Si l'horaire d'un opérateur est modifié, alors il est insatisfait
                        if sigma[posteI][p] == 0:
                            poids += poids4
            #print("poids",i,p,poids)
            ligneI.append(poids)

        matrice.append(ligneI)
    #print("MATRICE")
    #for i in range(cardO):
    #    ligne = str(i) + " : "
    #    for i2 in range(36):
    #        ligne += str(matrice[i][i2])
    #        ligne += " "
    #    print(ligne)

    # On appelle la fonction linear_sum_assignment de la librairie scipy, qui utilise l'algorithme hongrois
    # (algorithme de Kuhn-Munkres) afin de résoudre le problème d'affectation de poids minimum.
    cost = np.array(matrice)
    row_ind, col_ind = linear_sum_assignment(cost)
    insat = cost[row_ind, col_ind].sum()

    # Si le poids retourné par l'algorithme hongrois est supérieur à 10000, alors on est dans le cas où il n'est
    # pas possible de trouver une solution au problème sans changer le créneau horaire d'un opérateur ou dans le
    # cas où un poste ne peut être pris en charge par personne.
    if insat < 99999:
        newSemaine = []
        for i in range(cardO):
            newSemaine.append(col_ind[i])
        # Le booléen représente la faisabilité de la solution
        return newSemaine, True
    else:
        # Le booléen représente la faisabilité de la solution
        print(":/")
        #newSemaine = []
        #for i in range(cardO):
        #    newSemaine.append(col_ind[i])
        #return newSemaine, True
        return semaine, False #TODO attention ne pas oublier de remettre



# Fonction secondaire permettant de calculer l'insatisfaction de chaque opérateur à la partir de la
# semaine initiale prévue et de sa version réparée (lorsque des opérateurs étaient incompétents)
def calculObjectif2Semaine(semaineInit, semaineFinale, cardO, kappa, rho, fac, sigma):
    #print("SEMAINE INIT", semaineInit)
    #print("SEMAINE FINA", semaineFinale)
    scores = np.zeros(cardO)
    poids1 = 1
    poids2 = 10
    poids3 = 100
    poids4 = 1000
    for i in range(0,cardO):
        poids = 0
        postePrevu = semaineInit[i]
        posteFinal = semaineFinale[i]
        if postePrevu == posteFinal:
            if kappa[i][postePrevu] == 0:
                poids = 100000
            else:
                poids = 0
        else:
            if kappa[i][posteFinal] == 0:
                poids = poids3
            else:
                # Si le poste de l'opérateur est modifié alors qu'il possédait la compétence, alors il est insatisfait
                if kappa[i][postePrevu] == 1:
                    poids += poids1
                # Si un opérateur affecté à un poste non rouleur devient rouleur, alors il est insatisfait
                if rho[posteFinal] == 0 and rho[postePrevu] == 1:
                    poids += poids2
                # Si l'horaire d'un opérateur est modifié, alors il est insatisfait
                if sigma[postePrevu][posteFinal] == 0:
                    poids += poids4

        scores[i] = poids
    return scores


# Fonction principale retournant une trame de base pour le planning durant cardS semaines.
# Elle prend en compte les compétences de chaque opérateur
def construireSol(cardO, cardS, kappa, sigma, isRandom, affectationsRoulement, rho, fac):
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
        semaineFinale, faisable = resoudreSemaineHongrois(semaineInit.copy(), cardO, kappa, sigma, rho, fac)
        if not faisable:
            return [None, None, None, False, None]
        trameFinale.append(semaineFinale)
        insatSemaine = calculObjectif2Semaine(semaineInit, semaineFinale, cardO, kappa, rho, fac, sigma)
        #print("avant :", semaineInit)
        #print("apres :", semaineFinale)
        #print("insatSemaine",s , "=", insatSemaine)
        for i in range(0, cardO):
            insatisfaction[i] += insatSemaine[i]

    valueObjectif1 = max(insatisfaction)
    # On fait la somme de l'insatisfaction de chaque opérateur
    valueObjectif2 = 0
    for i in range(0, cardO):
        valueObjectif2 += insatisfaction[i]

    # La solution retournée est au format [valeur fonction objectif, Y_ir, z_isp, estFaisable]
    return [valueObjectif2, affectations, trameFinale, True, valueObjectif1]

# Fonction principale permettant de construire une population de solutions, ne conservant que les meilleures
def construirePopulationSolution(taillePop, nbRun, cardO, nbSemaines, kappa, sigma, rho, fac):

    # Variables permettant de conserver les solutions actuellement dans la population
    # ainsi que les valeurs de la meilleure et de la pire
    topSolutions = []
    bestInsat = 9999
    worstInsat = -1

    i = 0 # on continue de générer des solutions jusqu'à en avoir le nombre minimum requis
    while i < taillePop:
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None, rho, fac)
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
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None, rho, fac)
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

def getAffectationsJour(sol, kappa, sigma, rho, d):
    #[valueObjectif2, affectations, trameFinale, True, valueObjectif1]
    trameFinale = sol[2]
    cardS = len(trameFinale)
    cardO = len(trameFinale[0])
    insatRA = np.zeros(cardO)
    listeRemplacements = []
    faisable = True

    # On dresse la liste des opérateurs à 80%
    operateursRepos = []
    for i in range(cardO):
        if d[i] != -1:
            operateursRepos.append((i))

    # On s'occupe du remplacement des opérateurs choisis dans un ordre aléatoire
    random.shuffle(operateursRepos)
    for RA in operateursRepos:
        for s in range(cardS):
            #print("trame = ", trameFinale[s])
            affectationSemaine = trameFinale[s]
            posteRA = affectationSemaine[RA]
            # Si l'opérateur en RA est affecté à un poste rouleur, on ne fait rien
            if rho[posteRA] == 1:
                rouleursCandidats = []
                jourRA = (d[RA] + s) % 5 # Jour précis du RA
                #print("Il faut remplacer", RA, "le jour", jourRA)
                for i2 in range(cardO):
                    posteI2 = affectationSemaine[i2]
                    # L'opérateur peut remplacer s'il travaille ce jour, est compétent et est rouleur
                    if (d[i2] == -1 or (d[i2] + s) % 5 != jourRA) and rho[posteI2] == 0 and kappa[i2][posteRA] == 1:
                        rouleursCandidats.append(i2)

                # Une fois que l'on a la liste des rouleurs pouvant remplacer le RA, on choisit celui avec le score le moins élevé
                min = 10000
                rouleurChoisi = -1
                random.shuffle(rouleursCandidats)
                for rouleur in rouleursCandidats:
                    insatRouleur = insatRA[rouleur]
                    if insatRouleur < min:
                        min = insatRouleur
                        rouleurChoisi = rouleur

                if (rouleurChoisi == -1):
                    faisable = False
                listeRemplacements.append([jourRA + 7*s, rouleurChoisi, posteRA])
                insatRA[rouleurChoisi] += 1

    #print()
    #print("insatRA = ", insatRA)
    #print(listeRemplacements)
    return [faisable, listeRemplacements]