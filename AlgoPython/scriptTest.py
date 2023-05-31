import methode2opt

def main():

    cardO = 36  # nombre d'opérateurs
    cardP = 36  # nombre de postes
    cardR = 36  # longueur du roulement

    # Postes rouleurs (rho[p] = 1 non rouleur, rho[p] = 0 rouleur)
    rho = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1]

    # Creneaux des postes (0=rouleur, 1=7h00, 2=8h00, 3=9h00, 4=10h30, 5=12h45)
    creneaux = [5, 1, 4, 1, 0, 4, 0, 4, 3, 4, 5, 4, 1, 0, 4, 1, 4, 0, 1, 0, 5, 4, 1, 0, 3, 4, 1, 0, 0, 4, 5, 0, 1, 4, 0, 2]

    sigma = []
    for index1 in range(len(creneaux)):
        creneau1 = creneaux[index1]
        ligneSigma = []
        for index2 in range(len(creneaux)):
            creneau2 = creneaux[index2]
            if creneau1 == creneau2 or creneau1 == 0 or creneau2 == 0:
                ligneSigma.append(1)
            else:
                ligneSigma.append(0)
        sigma.append(ligneSigma)

    # postes facultatifs version algorithme (idem)
    fac = [2, 15, 22]

    # kappa (kappa[i][p] = 1 si l'opérateur i a la compétence pour effectuer le poste p, 0 sinon)
    # Compétence de chaque opérateur en fonction du type de poste
    cptBase = [
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]]

    # 0 = Auto, 1 = Dech, 2 = Lav, 3 = Cond, 4 = Lav/Cond, 5 = Sté, 6 = Rec, 7 = rouleur process, 8 = rouleur rec, 9 = Lav2-Rc-10h30, 10 = Cond-12h45
    typesPostes = [1, 0, 6, 4, 8, 3, 7, 6, 6, 1, 10, 6, 1, 7, 9, 3, 5, 7, 2, 8, 0, 6, 3, 7, 6, 3, 2, 7, 7, 6, 5, 8, 5, 2, 7, 6]

    kappa = []
    for i in range(cardO):
        ligne = []
        for p in range(cardP):
            typePoste = typesPostes[p]
            ligne.append(cptBase[i][typePoste])
        kappa.append(ligne)

    cardS = 2  # horizon du planning en semaines

    cumulScores = 0
    nbTest = 3
    for indexTest in range(nbTest):
        pop = methode2opt.rechercheLocale2optPopulation(3, 100, cardO, cardS, kappa, sigma, rho, fac)
        score = pop[0][0]
        print(score, "                          ")
        cumulScores += score
    scoreMoyen = cumulScores/nbTest
    print("cumul = ", cumulScores)
    print("scoremoy = ", scoreMoyen)

main()