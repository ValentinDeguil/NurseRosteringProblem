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
    # Le coût vaut 100000 si l'opérateur est associé à un poste non facultatif qu'elle ne maîtrise pas
    # Le coût vaut 0 s'il s'agit du poste prévu pour l'opérateur dans le roulement
    # Le coût vaut 1 si l'opérateur change de poste alors qu'il était compétent pour le sien
    # Le coût vaut 10 si l'opérateur est affecté à un nouveau poste rouleur alors qu'il était non rouleur
    # Le coût vaut 100 si l'opérateur est affecté à un poste facultatif qu'il ne maîtrise pas (poste non assuré)
    # Le coût vaut 1000 si l'opérateur est affecté à un nouveau poste situé sur un créneau horaire différent
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
            if p == posteI:
                if kappa[i][p] == 1:
                    poids = 0
                else:
                    if p in fac:
                        poids = poids3
                    else:
                        poids = 100000
            else:
                if p in fac:
                    if kappa[i][p] == 0:
                        poids = poids3
                    else:
                        # Si l'opérateur est compétent pour son poste initial, alors il est incompétent
                        if kappa[i][posteI] == 1:
                            poids += poids1
                        # Si un opérateur affecté à un poste non rouleur devient rouleur, alors il est insatisfait
                        if rho[p] == 0 and rho[posteI] == 1:
                            poids += poids2
                        # Si l'horaire d'un opérateur est modifié, alors il est insatisfait
                        if sigma[posteI][p] == 0:
                            poids += poids4
                else:
                    # Si le poste est obligatoire et que l'opérateur n'est pas compétent, le coût est "infini"
                    if kappa[i][p] == 0:
                        poids += 100000
                    else:
                        if kappa[i][posteI] == 1:
                            poids += poids1
                        # Si un opérateur affecté à un poste non rouleur devient rouleur, alors il est insatisfait
                        if rho[p] == 0 and rho[posteI] == 1:
                            poids += poids2
                        # Si l'horaire d'un opérateur est modifié, alors il est insatisfait
                        if sigma[posteI][p] == 0:
                            poids += poids4
            ligneI.append(poids)

        matrice.append(ligneI)

    # print("Affichage matrice des coûts")
    # for i in range(cardO):
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

    # Si le poids retourné par l'algorithme hongrois est supérieur à 100000 ("infini"), alors on est dans le cas où
    # il n'est pas possible de trouver une solution au problème sans changer le créneau horaire d'un opérateur ou dans
    # le cas où un poste ne peut être pris en charge par personne.
    if insat < 99999:
        newSemaine = []
        for i in range(cardO):
            newSemaine.append(col_ind[i])
        # Le booléen représente la faisabilité de la solution
        return newSemaine, True
    else:
        return semaine, False  # TODO attention ne pas oublier de remettre


# Fonction secondaire permettant de calculer l'insatisfaction de chaque opérateur à la partir de la
# semaine initiale prévue et de sa version réparée (lorsque des opérateurs étaient incompétents)
def calculObjectifSemaine(semaineInit, semaineFinale, cardO, kappa, rho, fac, sigma):
    # print("SEMAINE INIT", semaineInit)
    # print("SEMAINE FINA", semaineFinale)
    scores = np.zeros(cardO)
    poids1 = 1
    poids2 = 10
    poids3 = 100
    poids4 = 1000
    for i in range(0, cardO):
        poids = 0
        postePrevu = semaineInit[i]
        posteFinal = semaineFinale[i]
        if postePrevu == posteFinal:
            if kappa[i][postePrevu] == 0:
                poids = 100000
            else:
                poids = 0
        else:
            # Si l'opérateur n'est pas compétent pour son poste, alors il s'agit obligatoirement d'un poste facultatif
            # sinon, resoudreSemaineHongrois aurait signalé que la solution était infaisable
            if kappa[i][posteFinal] == 0:
                poids = poids3
                print("poids3 calculObjectifSemaine")
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
def construireSol(cardO, cardS, kappa, sigma, isRandom, affectationsRoulement, rho, fac, matriceConges):
    # isRandom est utile pour la recherche locale, on peut ainsi choisir un vecteur Y_ir aléatoire ou non
    if isRandom:
        affectations = creerAffectations(cardO)
    else:
        affectations = affectationsRoulement.copy()

    trameInit = []  # on crée la trame initiale pour toutes les semaines en fonction du vecteur Y_ir (affectations)
    for s in range(0, cardS):
        affectSemaine = affectations.copy()
        for p in range(0, cardO):
            affectSemaine[p] = (affectSemaine[
                                    p] + s) % cardO  # décale de 1 chaque semaine le poste effectué par un opérateur
        trameInit.append(affectSemaine.copy())

    # À partir de la trame de base, on répare les semaines durant lesquelles des opérateurs
    # sont affectés à des postes où ils sont incompétents
    trameFinale = []  # Affectations des opérateurs chaque semaine après réparation des semaines
    insatisfaction = np.zeros(cardO)  # Insatisfaction de chaque opérateur

    # Pour chaque semaine, on observe si une personne est à un poste où elle n'est pas compétente
    # Si pour une semaine donnée, aucune affectation n'est possible, on retourne une solution vide
    for s in range(0, cardS):
        semaineInit = trameInit[s].copy()
        semaineFinale, faisable = resoudreSemaineHongrois(semaineInit.copy(), cardO, kappa, sigma, rho, fac)
        # Une semaine est considérée comme infaisable si on ne peut pas trouver une série de mouvements permettant de
        # résoudre les conflits
        if not faisable:
            return [None, None, None, False, None]

        trameFinale.append(semaineFinale)
        insatSemaine = calculObjectifSemaine(semaineInit, semaineFinale, cardO, kappa, rho, fac, sigma)
        for i in range(0, cardO):
            insatisfaction[i] += insatSemaine[i]

    valueObjectif = 0
    for i in range(0, cardO):
        valueObjectif += insatisfaction[i]

    sol = [valueObjectif, affectations, trameFinale, True, None]
    affectJournaliere = getAffectationsJour(sol, kappa, rho, matriceConges)
    sol[0] += affectJournaliere[1]  # on ajoute le coût des affectations journalières
    sol[4] = affectJournaliere[0]

    # La solution retournée est au format [valeur fonction objectif, Y_ir, z_isp, estFaisable, x_ijp]
    return sol


# Fonction principale permettant de construire une population de solutions, ne conservant que les meilleures
def construirePopulationSolution(taillePop, nbRun, cardO, nbSemaines, kappa, sigma, rho, fac, matriceConges):
    # Variables permettant de conserver les solutions actuellement dans la population
    # ainsi que les valeurs de la meilleure et de la pire
    topSolutions = []
    bestInsat = 999999
    worstInsat = -1

    i = 0  # on continue de générer des solutions jusqu'à en avoir le nombre minimum requis
    while i < taillePop:
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None, rho, fac, matriceConges)

        # Si la solution générée est faisable (par rapport aux compétences des opérateurs),
        # on met à jour les différentes informations
        if sol[3]:
            topSolutions.append(sol)
            valueSol = sol[0]

            if valueSol < bestInsat:
                bestInsat = valueSol

            if valueSol > worstInsat:
                worstInsat = valueSol
            i = i + 1

    topSolutions.sort()

    # On pourrait mettre ça à la place de la suite, sans doute plus optimisé pour de petits nombres de "nbRun"
    # for i in range(0, nbRun - taillePop):
    #    sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None)
    #    if sol[3]:
    #        topSolutions.append(sol.copy())
    # topSolutions.sort()
    # return topSolutions[:taillePop]

    # On a trouvé "taillePop" solutions initiales, si on souhaite en générer plus afin de démarrer l'heuristique avec
    # des solutions de meilleure qualité, alors on continue d'en générer (en revanche, pas de boucle while ici)
    for i in range(0, nbRun - taillePop):
        sol = construireSol(cardO, nbSemaines, kappa, sigma, True, None, rho, fac, matriceConges)
        valueSol = sol[0]
        if sol[3]:  # si la nouvelle solution est faisable...
            if valueSol < worstInsat:  # et meilleure que la pire solution de la solution...
                # alors, on met à jour notre population.
                # Deux cas sont possibles, cas 1 : la solution générée est la nouvelle meilleure
                if bestInsat >= valueSol:
                    bestInsat = valueSol
                    newTopSolutions = [sol.copy()]
                    for k in range(0, taillePop - 1):
                        newTopSolutions.append(topSolutions[k].copy())
                    topSolutions = newTopSolutions.copy()
                else:
                    # cas 2 : la solution générée se situe quelque part au milieu de la population
                    found = False
                    j = taillePop - 1
                    # on effectue la recherche de l'index où insérer la nouvelle solution par la fin,
                    # il est en effet très rare de générer des solutions très bonnes
                    while not found and j >= 0:
                        if topSolutions[j][0] <= valueSol:
                            found = True
                            newTopSolutions = []
                            for k in range(0, j + 1):
                                newTopSolutions.append(topSolutions[k].copy())
                            newTopSolutions.append(sol.copy())
                            for k in range(j + 1, taillePop - 1):
                                newTopSolutions.append(topSolutions[k].copy())
                            topSolutions = newTopSolutions.copy()
                            worstInsat = topSolutions[taillePop - 1][0]
                        else:
                            j += -1
    return topSolutions


def getAffectationsJour(sol, kappa, rho, matriceConges):
    bestAffect = None
    valeurBestAffect = 100000000
    for indexTest in range(10):
        # Format affectJour : [listeRemplacements, nbJoursNonPourvus*10000]
        affectJour = essaiAffectationsJour(sol, kappa, rho, matriceConges)
        valeur = affectJour[1]
        if valeur < valeurBestAffect:
            valeurBestAffect = valeur
            bestAffect = affectJour

    return bestAffect


def essaiAffectationsJour(sol, kappa, rho, matriceConges):
    # [valueObjectif2, affectations, trameFinale, True, affect]
    trameFinale = sol[2]
    cardS = len(trameFinale)
    cardO = len(trameFinale[0])
    insatRA = np.zeros(cardO)
    listeRemplacements = []
    listeIndispos = []
    nbJoursNonPourvus = 0  # nombre de jours où il n'est pas possible de trouver un remplacement

    # On crée une liste des jours pour lesquels trouver des remplacements, on la mélange pour plus d'équité
    joursATraiter = []
    for i in range(cardS * 7):
        if i - (i // 7) * 7 <= 4:
            joursATraiter.append(i)
    random.shuffle(joursATraiter)

    for j in joursATraiter:
        s = j // 7  # semaine correspondante au jour traité
        affectationSemaine = trameFinale[s]

        operateurRepos = []  # liste des opérateurs à remplacer ce jour
        for i in range(cardO):
            if matriceConges[i][j] == 0:
                operateurRepos.append(i)
        random.shuffle(operateurRepos)

        for opeConge in operateurRepos:
            posteRA = affectationSemaine[opeConge]
            rouleursCandidats = []  # on dresse la liste des rouleurs pouvant potentiellement le remplacer ce jour
            for i in range(cardO):
                posteCandidat = affectationSemaine[i]
                # un opérateur peut remplacer la personne s'il est rouleur et disponible ce jour
                if kappa[i][posteRA] == 1 and rho[posteCandidat] == 0 and matriceConges[i][j] == 1 and [i,j] not in listeIndispos:
                    rouleursCandidats.append(i)

            # une fois la liste des candidats obtenue, on choisit celui le moins sollicité
            minInsat = 10000
            rouleurChoisi = -1
            random.shuffle(rouleursCandidats)
            for rouleur in rouleursCandidats:
                insatRouleur = insatRA[rouleur]
                if insatRouleur < minInsat:
                    minInsat = insatRouleur
                    rouleurChoisi = rouleur
            if rouleurChoisi == -1:
                nbJoursNonPourvus += 1
            else:
                listeRemplacements.append([j, rouleurChoisi, posteRA])
                listeIndispos.append([rouleurChoisi, j])
                insatRA[rouleurChoisi] += 1

    return [listeRemplacements, nbJoursNonPourvus*10000]
