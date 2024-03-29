import coreFunctions


def rechercheLocale2optSolution(solInit, cardO, cardS, kappa, sigma, rho, fac, matriceConges):
    found = False  # la fonction s'arrête dès qu'un meilleur voisin est trouvé
    affectationsInit = solInit[1]
    valueInit = solInit[0]
    # on inverse chaque paire d'opérateur (i, j) dans le roulement initial
    i = 0
    while not found and i < (cardO - 1):
        j = i + 1
        while not found and j < cardO:
            newAffectations = affectationsInit.copy()
            temp = newAffectations[i]
            newAffectations[i] = newAffectations[j]
            newAffectations[j] = temp
            newSol = coreFunctions.construireSol(cardO, cardS, kappa, sigma, False, newAffectations, rho, fac, matriceConges)

            valueNewSol = newSol[0]

            if newSol[3]:  # si la solution générée est faisable...
                if valueNewSol < valueInit:  # et meilleure que la solution initiale
                    found = True  # on a trouvé un meilleur voisin et la fonction s'interrompt
            j = j + 1
        i = i + 1
    # on indique dans le retour si une meilleure solution a été trouvée ou non
    if found:
        return [True, newSol]
    else:
        return [False, None]


# Fonction principale appliquant un algorithme de recherche locale 2-opt sur une population de solutions
def rechercheLocale2optPopulation(taillePop, nbRunInit, cardO, cardS, kappa, sigma, rho, fac, matriceConges):
    # On construit la population de solutions initiale
    pop = coreFunctions.construirePopulationSolution(taillePop, nbRunInit, cardO, cardS, kappa, sigma, rho, fac, matriceConges)
    pop.sort()

    stop = False
    index = 0
    while not stop and index < taillePop:
        # Format de newSol : [faisable, sol]
        newSol = rechercheLocale2optSolution(pop[index], cardO, cardS, kappa, sigma, rho, fac, matriceConges)
        # Si la recherche locale sur la solution donne une meilleure valeur, alors celle-ci est remplacée
        if newSol[0]:
            # L'index ne change pas et on applique à nouveau la recherche locale sur cette nouvelle solution
            pop[index] = newSol[1].copy()
        # Sinon, on tente d'améliorer la solution suivante dans la population
        else:
            index = index + 1
            print("Chargement : ", float(index) / float(taillePop) * 100, "%                  ", end='\r')

    pop.sort()
    return pop
