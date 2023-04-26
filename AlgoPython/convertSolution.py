import csv
import numpy as np
import datetime
def convertSolutionCSV(solution, affectationsJours, d, nomsPostes, nomsOperateurs):

    cardS = len(solution[2])
    cardJ = 7 * cardS

    #print()
    #print(cardS)
    #print(nomsOperateurs)
    #print(nomsPostes)

    date = datetime.datetime(2023, 9, 4)

    o = np.zeros(cardJ)
    for j in range(0, len(o)):
        if j % 7 <= 4:
            o[j] = 1

    with open('planningFinal.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        jours = ["",""]
        for s in range(0, cardS):
            jours.extend(["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"])
        writer.writerow(jours)

        dates = ["",""]
        for j in range(0, cardJ):
            dates.append(date.strftime("%d")+"/"+date.strftime("%m")+"/"+date.strftime("%y"))
            date += datetime.timedelta(days=1)
        writer.writerow(dates)

        for i in range(0, len(nomsOperateurs)):
            planningPerso = [nomsOperateurs[i][0], nomsOperateurs[i][1]]
            for s in range(0, cardS):
                posteSemaine = solution[2][s][i]
                nomPoste = nomsPostes[posteSemaine]
                for j in range(5):
                    planningPerso.append(nomPoste)
                for j in range(2):
                    planningPerso.append("")

            if d[i] != -1:
                for s in range(cardS):
                    jourRA = (d[i] + s)%5
                    planningPerso[7*s + jourRA + 2] = "RA" #décallage de 2 à cause des noms et prénoms des opérateurs

            index = 0
            while index < len(affectationsJours):
                remplacement = affectationsJours[index]
                if remplacement[1] == i:
                    jourRemplacement = remplacement[0]
                    posteRemplacement = remplacement[2]
                    planningPerso[jourRemplacement + 2] = nomsPostes[posteRemplacement]
                    del affectationsJours[index]
                else:
                    index += 1

            writer.writerow(planningPerso)

# calcul du jour non travaillé pour une semaine donnée d'un opérateur à 80%
# en fonction du jour non travaillé la première semaine
def delta_i(s,d_i):
    return (d_i+s) % 5


def convertSolutionText(solution, affectationsJournalieres, kappa, sigma, rho, d):
    #[valueObjectif2, affectations, trameFinale, True, valueObjectif1]
    affectations = solution[1]
    trameFinale  = solution[2]

    cardO = len(affectations)
    cardP = cardO
    cardR = cardO
    cardS = len(trameFinale)
    cardJ = 7*cardS


    with open("solutionApprochee", "w") as file_object:
        file_object.write(str(cardO) + "\n") #cardO
        file_object.write(str(cardP) + "\n") #cardP
        file_object.write(str(cardR) + "\n") #cardR
        file_object.write(str(cardS) + "\n") #cardS

        ligne = ""
        for p in range(cardP):
            ligne = ligne + str(rho[p])
        file_object.write(ligne + "\n")  # rho

        o = np.zeros(cardJ)
        for j in range(cardJ):
            if j % 7 <= 4:
                o[j] = 1
        ligne = ""
        for j in range(cardJ):
            ligne += str(int(o[j]))
        file_object.write(ligne + "\n")  # o_j

        for i in range(0, cardO):
            ligne = ""
            for p in range(0, cardP):
                ligne = ligne + str(kappa[i][p])
            file_object.write(ligne + "\n")  # kappa_ip

        for p in range(0, cardP):
            ligne = ""
            for p2 in range(0, cardP):
                ligne = ligne + str(sigma[p][p2])
            file_object.write(ligne + "\n")  # sigma_pp'

        delta = np.full((cardO, cardJ), 1)
        for i in range(0, cardO):
            if d[i] != -1:
                d_i = d[i]
                for s in range(0, cardS):
                    d_is = delta_i(s, d_i)  # rang du jour non travaillé la semaine s
                    j_s = 7 * s + d_is  # numéro du jour non travaillé
                    delta[i][j_s] = 0
        for i in range(cardO):
            ligne = ""
            for j in range(cardJ):
                ligne += str(delta[i][j])
            file_object.write(ligne + "\n")  # delta_ij

        x = []
        affect = []
        for p in range(cardP):
            affect.append(0)
        for i in range(cardO):
            ligne = []
            for j in range(cardJ):
                ligne.append(affect.copy())
            x.append(ligne)

        for s in range(cardS):
            affectSemaine = solution[2][s]
            for i in range(cardO):
                posteIS = affectSemaine[i]
                for j in range(7*s, 7*s+5):
                    x[i][j][posteIS] = 1

        for i in range(cardO):
            RA = d[i]
            if RA != -1:
                for s in range(cardS):
                    j = delta_i(s, RA) + s * 7
                    for p in range(cardP):
                        x[i][j][p] = 0

        for c in range(len(affectationsJournalieres[1])):
            changement = affectationsJournalieres[1][c]
            j = changement[0]
            i = changement[1]
            newP = changement[2]
            for p in range(cardP):
                x[i][j][p] = 0
            x[i][j][newP] = 1


        for i in range(0, cardO):
            for j in range(0, cardJ):
                ligne = ""
                for p in range(0, cardP):
                    ligne = ligne + str(x[i][j][p])
                file_object.write(ligne + "\n")  # x_ijp


        for i in range(0, cardO):
            ligne = ""
            for r in range(0, cardR):
                if affectations[i] == r:
                    ligne += "1"
                else:
                    ligne += "0"
            file_object.write(ligne + "\n")

        for i in range(0, cardO):
            for s in range(0, cardS):
                ligne = ""
                for p in range(0, cardP):
                    if trameFinale[s][i] == p:
                        ligne += "1"
                    else:
                        ligne += "0"
                file_object.write(ligne + "\n")  # z_isp

        file_object.write(str(int(solution[0])) + "\n")



