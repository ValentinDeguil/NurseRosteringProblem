import random
def generate(size):
    # Données à générer pour l'instance
    vecteurChance = []  # Probabilité qu'un opérateur soit capable d'effectuer chaque type de poste
    listePostes = []    # Type de poste de chaque poste
    creneaux = []       # Créneau horaire associé à chaque poste
    rho = []            # Poste roulant ou non (1 = non roulant, 0 = roulant)
    d = []              # RA de chaque opérateur la première semaine (-1 = 100%)

    if size == 12:
        vecteurChance = [18 / 24, 21 / 24, 21 / 24, 21 / 24, 20 / 24, 18 / 24]  # Auto, Dech, Lav, Cond, Lav/Cond, Sté
        listePostes = [0,4,1,-1,2,3,2,-1,3,5,3,-1]
        creneaux = [0,1,1,0,2,1,1,0,1,3,1,0] #j'aurais voulu mettre ça, mais les créneaux 2 et 3 sont uniques -> impossibles à remplacer quand incompétence
        creneaux = [0,1,1,0,2,1,1,0,1,2,1,0]
        rho = [1,1,1,0,1,1,1,0,1,1,1,0]
        d = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    elif size == 24:
        vecteurChance = [18/24, 21/24, 21/24, 21/24, 20/24, 18/24] # Auto, Dech, Lav, Cond, Lav/Cond, Sté
        listePostes = [0,1,4,3,-1,1,3,1,-1,2,3,5,-1,2,0,3,-1,3,2,-1,-1,5,5,2] # 0 = Auto, 1 = Dech, etc... -1 = rouleur
        creneaux = [0,2,1,2,0,1,3,1,0,2,1,2,0,1,3,1,0,1,2,1,0,3,1,2]
        rho = [0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0]
        d = [3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    elif size == 36:
        vecteurChance = [42/72, 69/108, 100/144, 152/180, 26/36, 63/108, 104/288]  # Auto, Dech, Lav, Cond, Lav/Cond, Sté, Rec
        listePostes = [1,0,6,4,-1,3,-1,6,6,1,3,6,1,-1,2,3,5,-1,2,-1,0,6,3,-1,6,3,2,-1,-1,6,5,-1,5,2,-1,6]
        rho = [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,0,1,1,0,1,1,0,1]
    else:
        return None

    # On génère les compétences de chaque opérateur
    competences = []
    for ope in range(size):
        competencesOpe = []
        for indexPoste in range(len(vecteurChance)):
            tirage = random.random()
            if tirage < vecteurChance[indexPoste]:
                competencesOpe.append(1)
            else:
                competencesOpe.append(0)
        competences.append(competencesOpe)

    print("compétences des opérateurs")
    for i in range(size):
        print(competences[i])

    # À partir des compétences de chaque opérateur, on génère la matrice kappa
    kappa = []
    if size == 12 or size == 24:
        for ope in range(size):
            ligneKappa = []
            for poste in range(len(listePostes)):
                if listePostes[poste] == -1:
                    ligneKappa.append(1)
                else:
                    ligneKappa.append(competences[ope][listePostes[poste]])
            kappa.append(ligneKappa)
    else:
        return None

    print("kappa")
    for i in range(size):
        print(kappa[i])

    # À partir des créneaux horaires, on génère la matrice sigma
    sigma = []
    for index1 in range(len(creneaux)):
        creneau1 = creneaux[index1]
        ligneSigma = []
        for index2 in range(len(creneaux)):
            if creneau1 == creneaux[index2]:
                ligneSigma.append(1)
            else:
                ligneSigma.append(0)
        sigma.append(ligneSigma)

    print("sigma")
    for i in range(size):
        print(sigma[i])

    return [kappa, sigma, rho, d]

#generate(36)