import random
import numpy as np


def generate(size):
    # Données à générer pour l'instance
    vecteurChance = []  # Probabilité qu'un opérateur soit capable d'effectuer chaque type de poste
    listePostes = []  # Type de poste de chaque poste
    creneaux = []  # Créneau horaire associé à chaque poste
    rho = []  # Poste roulant ou non (1 = non roulant, 0 = roulant)
    d = []  # RA de chaque opérateur la première semaine (-1 = 100%)
    if size == 12:
        vecteurChance = [16 / 23, 19 / 23, 22 / 23, 23 / 23, 16 / 23]  # Auto, Dech, Lav, Cond, Sté
        listePostes = [0, -1, 2, 3, 0, -1, 4, 3, 2, -1, 1, 4]  # 0 = Auto, 1 = Dech, etc... -1 = rouleur
        creneaux = [1, 0, 2, 1, 3, 0, 1, 2, 1, 0, 3, 2]
        rho = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1]
        d = [-1, -1, 0, -1, -1, 2, -1, 4, -1, 1, -1, -1]
        fac = [7]
        intervalles = [[3, 4], [3, 5], [4, 5]]
    elif size == 25:
        # attention, il y a 25 postes process, mais les statistiques ont été mesurées sur les 23 opérateurs process
        vecteurChance = [16 / 23, 19 / 23, 22 / 23, 23 / 23, 22 / 23, 16 / 23]  # Auto, Dech, Lav, Cond, Lav/Cond, Sté
        listePostes = [1, 0, 4, 3, -1, 1, 3, 1, -1, 2, 3, 5, -1, 2, 0, 3, -1, 3, 2, -1, -1, 5, 5, 2,
                       -1]  # 0 = Auto, 1 = Dech, etc... -1 = rouleur
        creneaux = [3, 1, 1, 2, 0, 2, 3, 1, 0, 2, 1, 2, 0, 1, 3, 1, 0, 2, 1, 0, 0, 3, 1, 2, 0]
        rho = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0]
        d = [-1, -1, 2, 0, -1, -1, -1, 0, -1, -1, 4, -1, -1, -1, 2, 1, -1, -1, -1, -1, 1, -1, 3, -1, -1]
        fac = [3, 10]
        intervalles = [[3, 6], [4, 6], [5, 6]]
    elif size == 36:
        vecteurChance = [21 / size, 23 / size, 26 / size, 31 / size, 26 / size, 21 / size,
                         13 / size]  # Auto, Dech, Lav, Cond, Lav/Cond, Sté, Rec
        listePostes = [1, 0, 6, 4, -1, 3, -1, 6, 6, 1, 3, 6, 1, -1, 2, 3, 5, -1, 2, -1, 0, 6, 3, -1, 6, 3, 2, -1, -1, 6,
                       5, -1, 5, 2, -1, 6]
        creneaux = [5, 1, 4, 1, 0, 4, 0, 4, 3, 4, 5, 4, 1, 0, 4, 1, 4, 0, 1, 0, 5, 4, 1, 0, 3, 4, 1, 0, 0, 4, 5, 0, 1,
                    4, 0, 2]
        rho = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0,
               1]
        d = [-1, -1, -1, -1, 0, -1, -1, 0, -1, 4, -1, 2, -1, 0, -1, 4, -1, -1, 1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 3,
             -1, -1, 1, -1, -1, 3, -1]
        fac = [22, 25, 2]
        intervalles = [[4, 7], [5, 7], [6, 7]]
    else:
        print("Taille d'instance non valide")
        return None

    tempsPleins = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1,
                   1, 1, 1,
                   1, 1, 0]

    conges = [[32, 35, 36, 38, 39, 42, 52, 105, 127, 128, 130, 140, 162, 163, 164, 165],
              [2, 39, 58, 74, 78, 109, 113, 114, 115, 144, 164, 165],
              [37, 43, 44, 45, 46, 78, 86, 98, 99, 100, 102, 123, 140, 154, 156, 157, 158],
              [9, 30, 35, 36, 37, 38, 65, 100, 105, 106, 107, 108],
              [17, 42, 44, 45, 46, 49, 50, 63, 106, 107, 108, 109, 136, 140],
              [8, 42, 43, 44, 46, 80, 81, 84, 122, 140, 141, 143, 144], [8, 24, 140],
              [8, 35, 36, 37, 38, 39, 70, 80, 81, 94, 95, 98, 105, 106, 107, 108, 109, 130, 140, 141, 142, 143,
               144], [7, 18, 21, 46, 56, 70, 71, 72, 73, 74, 113, 114, 115, 116, 128, 147],
              [14, 15, 16, 17, 18, 22, 35, 59, 60, 63, 64, 65, 74, 84, 87, 88, 105, 106, 107, 108, 109, 130,
               140, 142], [10, 11, 39, 58, 63, 84, 85, 86, 87, 88, 116, 141, 142, 143, 144, 151],
              [18, 21, 23, 24, 25, 74, 85, 86, 87, 88, 109, 122, 140],
              [15, 25, 42, 63, 64, 65, 66, 67, 92, 93, 94, 95, 113, 114, 115, 116, 130, 137, 140],
              [0, 1, 16, 28, 35, 36, 43, 77, 87, 92, 102, 140], [14, 43, 44, 45, 46, 86, 95, 98, 99, 100, 102],
              [8, 25, 29, 80, 81, 98, 99, 101, 102, 140, 141],
              [8, 18, 56, 80, 81, 92, 102, 113, 114, 115, 116, 140, 178, 179],
              [25, 56, 57, 58, 59, 60, 77, 106, 126, 130, 133, 134, 135, 136, 137, 140],
              [35, 36, 37, 38, 39, 51, 79, 93, 105, 106, 107, 108, 109, 140, 149, 177],
              [7, 21, 63, 71, 98, 120, 121, 122, 123, 126, 127, 128, 133, 161, 162, 163, 164, 165],
              [0, 11, 28, 29, 30, 31, 32, 42, 67, 70, 71, 72, 73, 74, 80, 116, 130, 133, 134, 135, 136, 137],
              [42, 43, 44, 45, 46, 71, 86, 115, 122, 128, 130, 135, 140, 149],
              [8, 59, 80, 81, 88, 93, 94, 95, 98, 99, 100, 101, 102, 121, 130, 140, 141, 175, 176, 177, 178,
               179], [50, 63, 64, 65, 66, 106, 107, 108, 109, 120, 140, 154, 155, 165],
              [2, 25, 30, 36, 56, 57, 58, 59, 60, 80, 81, 105, 106, 107, 108, 109, 140, 144, 161, 162, 163, 164,
               165, 168, 169, 170, 171, 172, 175, 176, 177, 178, 179],
              [4, 11, 14, 16, 32, 45, 51, 53, 64, 65, 66, 67, 70, 85, 86, 101, 105, 107, 108, 109, 140, 161,
               162, 163, 164, 169, 170, 171, 172, 175, 177, 178, 179],
              [32, 35, 36, 37, 38, 39, 78, 88, 126, 127, 128, 130, 140, 168, 169, 170, 171, 172, 175, 176, 177,
               178, 179], [7, 8, 74, 77, 92, 93, 94, 95, 140], [109, 123, 126, 127, 128, 130, 140, 154, 165],
              [7, 63, 64, 65, 66, 67, 113, 114, 115, 116, 140, 161, 168, 169, 170, 171, 172, 175, 176, 177, 178,
               179], [39, 63, 95, 98, 99, 100, 101, 102, 130, 140, 154], [140],
              [42, 105, 106, 107, 108, 109, 135, 136, 137, 140, 141],
              [9, 23, 42, 43, 44, 45, 46, 58, 84, 86, 98, 99, 100, 101, 102, 130, 140],
              [44, 46, 49, 50, 51, 52, 53, 133, 134, 135, 136, 137, 140],
              [44, 56, 57, 58, 59, 60, 130, 140, 144, 161, 162, 163, 164, 165, 168, 169, 170, 171, 172], [8, 24, 140]]

    for i in range(len(conges)):
        nombreJours = len(conges[i])
        for j in range(nombreJours):
            jour = conges[i][j]
            conges[i].append(jour + 182)

    conges80 = []
    conges100 = []
    for indexConge in range(len(conges)):
        if tempsPleins[indexConge] == 0:
            conges80.append(conges[indexConge])
        else:
            conges100.append(conges[indexConge])

    # print("conges80")
    # for indexConge in range(len(conges80)):
    #   print(conges80[indexConge])
    print("conges100")
    for indexConge in range(len(conges100)):
        print(conges100[indexConge])

    liste100Libres = []
    liste80Libres = []
    for i in range(len(conges100)):
        liste100Libres.append(i)
    for i in range(len(conges80)):
        liste80Libres.append(i)

    vraisConges = []

    for indexConge in range(len(d)):
        if d[indexConge] == -1:  # si on tombe sur un temps on plein, on tire au sort un set de congés parmi les temps pleins
            index100 = random.randint(0, len(liste100Libres) - 1)
            del liste100Libres[index100]
            vraisConges.append(conges100[index100].copy())
        else:
            index80 = random.randint(0, len(liste80Libres) - 1)
            del liste80Libres[index80]
            vraisConges.append(conges80[index80].copy())

    conges01 = []
    for indexConge in range(size):
        ligneOpe = []
        for j in range(size * 7):
            s = j // 7
            if j in vraisConges[indexConge] or (d[indexConge] != -1 and j == ((d[indexConge] + s) % 5) + 7 * s):
                ligneOpe.append(0)
            else:
                ligneOpe.append(1)
        conges01.append(ligneOpe)

    nbInstance = 10
    setKappa = []

    for inter in range(len(intervalles)):
        for indexInstance in range(nbInstance):
            # On génère les compétences de chaque opérateur
            competences = []
            for ope in range(size):
                nbCompetence = random.randint(intervalles[inter][0], intervalles[inter][1])
                competencesOpe = np.zeros(len(vecteurChance), dtype=int)
                cptChoisies = []
                for indexCpt in range(nbCompetence):
                    sommeTaux = 0
                    for index in range(len(vecteurChance)):
                        if index not in cptChoisies:
                            sommeTaux += vecteurChance[index]
                    tirage = random.uniform(0, sommeTaux)
                    newCompetence = -1
                    cumul = 0
                    for index in range(len(vecteurChance)):
                        if index not in cptChoisies:
                            cumul += vecteurChance[index]
                            if cumul > tirage and newCompetence == -1:
                                newCompetence = index
                                cptChoisies.append(index)

                for cpt in cptChoisies:
                    competencesOpe[cpt] = 1

                competences.append(competencesOpe)

            # print("compétences des opérateurs")
            # for ope in range(size):
            #    print(competences[ope])

            # À partir des compétences de chaque opérateur, on génère la matrice kappa
            kappa = []
            if size == 12 or size == 25 or size == 36:
                for ope in range(size):
                    ligneKappa = []
                    for poste in range(len(listePostes)):
                        if listePostes[poste] == -1:  # un opérateur maîtrise forcément les postes rouleurs
                            ligneKappa.append(1)
                        else:
                            ligneKappa.append(competences[ope][listePostes[poste]])
                    kappa.append(ligneKappa)
            else:
                return None

            setKappa.append(kappa)

        # print("kappa", (1+0.1*i)*100, "%")
        # for indexKappa in range(size):
        #    print(kappa[indexKappa])

    # À partir des créneaux horaires, on génère la matrice sigma
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

    delta = np.full((size, size * 7), 1)
    for i in range(size):
        if d[i] != -1:
            d_i = d[i]
            for s in range(size):
                d_is = (d_i + s) % 5
                j_s = 7 * s + d_is  # numéro du jour non travaillé
                delta[i][j_s] = 0

    # print("sigma")
    # for i in range(size):
    #    print(sigma[i])
    ###affichage de controle
    #print("Contrôle setKappa")
    #for i in range(len(setKappa)):
    #    print("kappa")
    #    for i2 in range(size):
    #        print(setKappa[i][i2])
    # print("Instances générées")
    # return [setKappa, sigma, rho, d]
    for index in range(len(intervalles) * nbInstance):
        nomInstance = str(size) + "_" + str(index)
        path = "Instances" + "/" + nomInstance
        with open(path, "w") as file_object:
            file_object.write(str(size) + "\n")

            ligneRho = ""
            for p in range(size):
                ligneRho += str(rho[p])
            file_object.write(ligneRho + "\n")

            # Anciennement, on printait les delta, là, je vais finalement passer le vecteur d en cardO lignes
            # for i in range(size):
            #    ligneDeltaI = ""
            #    for j in range(size*7):
            #        ligneDeltaI += str(delta[i][j])
            #    file_object.write(ligneDeltaI + "\n")

            for i in range(size):
                file_object.write(str(d[i]) + "\n")

            ligneFac = ""
            for p in range(size):
                if p in fac:
                    ligneFac += "1"
                else:
                    ligneFac += "0"
            file_object.write(ligneFac + "\n")

            for i in range(size):
                ligneKappaI = ""
                for p in range(size):
                    ligneKappaI += str(setKappa[index][i][p])
                file_object.write(ligneKappaI + "\n")

            for p1 in range(size):
                ligneSigmaP = ""
                for p2 in range(size):
                    ligneSigmaP += str(sigma[p1][p2])
                file_object.write(ligneSigmaP + "\n")

            for i in range(len(conges01)):
                ligne = ""
                for i2 in range(len(conges01[i])):
                    ligne += str(conges01[i][i2])
                file_object.write(ligne + "\n")

generate(12)
generate(25)
generate(36)
