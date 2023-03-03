import random
import numpy as np
def creerAffectations(size):
    base = []
    for i in range(0, size):
        base.append(i)
    random.shuffle(base)
    return base


# Fonction vérifiant si pour une semaine donnée, chaque opérateur peut effectuer le poste qui lui a été attribué
# Dans le cas contraire, on procède à des échanges de postes entre les opérateurs
def resoudreSemaine(semaine, cardO, kappa, sigma):
    succes = True # permet d'obtenir le statut de la réparation de la semaine
    listeOperateurs = []  # sera utilisé plus tard pour l'équité dans le remplacement
    for i in range(0, cardO):
        listeOperateurs.append(i)

    incomp = [] # vecteur contenant les opérateurs i non compétents pour leurs postes actuels
    for i in range(0, cardO):
        if kappa[i][semaine[i]] == 0:
            incomp.append(i)
    if len(incomp) == 0:
        return semaine, succes

    stop = False
    amelioration = False

    while not stop: # on poursuit les permutations s'il reste des gens mal affectés et que la solution reste faisable
        amelioration = False # permet de savoir si un échange intelligent a été trouvé
        if len(incomp) >= 2: # on vérifie si on peut faire un échange intelligent
            i = 0 # ici, i et j représentent les deux opérateurs incompétents que l'on souhaite échanger
            while i < len(incomp) and not amelioration:
                j = i
                while j < len(incomp) and not amelioration:
                    posteI = semaine[incomp[i]]
                    posteJ = semaine[incomp[j]]
                    # si i et j possèdent chacun la compétence de l'autre que ces postes sont sur le même créneau
                    # horaire, alors on les permute
                    if kappa[incomp[i]][posteJ] == 1 and kappa[incomp[j]][posteI] == 1 and sigma[posteI][posteJ] == 1:
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
        # À présent, s'il ne reste plus qu'un seul opérateur incompétent ou s'il en reste plus et
        # qu'aucun échange intelligent n'est possible, on permute un incompétent et un double compétent
        if len(incomp) == 1 or (len(incomp) >= 2 and not amelioration):
            amelioration = False
            randomOpe = 0
            random.shuffle(listeOperateurs) # on mélange la liste des opérateurs pour ne pas toujours sélectionner le même
            while randomOpe < cardO and not amelioration:
                i = listeOperateurs[randomOpe]
                # si l'opérateur choisi aléatoirement possède la compétente manquante à l'incompétent, que l'incompétent
                # possède la compétence pour son poste et que les deux postes sont permutables, alors on échange leurs postes
                if kappa[i][semaine[incomp[0]]] == 1 and kappa[incomp[0]][semaine[i]] and sigma[semaine[incomp[0]]][semaine[i]]:
                    amelioration = True
                    temp = semaine[i]
                    semaine[i] = semaine[incomp[0]]
                    semaine[incomp[0]] = temp
                    operateur1 = incomp[0]
                    incomp.remove(operateur1)
                randomOpe += 1

        # S'il ne reste plus d'opérateur incompétent ou si on ne peut pas réaliser
        # de permutation améliorante, alors on sort de la boucle
        if len(incomp) == 0 or not amelioration:
            stop = True

    # si lors du dernier essai de permutation, nous n'avons pas trouvé de permutation,
    # alors on considère que l'affectation Y_ir des opérateurs au roulement ne peut pas donner de solution valide
    if amelioration:
        return semaine, succes
    else:
        return semaine, not succes


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
        semaineFinale, faisable = resoudreSemaine(semaineInit.copy(), cardO, kappa, sigma)
        if not faisable:
            return [None, None, None, False]
        trameFinale.append(semaineFinale)
        insatSemaine = calculInsatisfaction(semaineInit, semaineFinale, cardO, kappa)
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
