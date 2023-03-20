import csv
import numpy as np
import pandas as pd
import datetime
def convertSolutionCSV(solution, affectationsJours, d):
    print()
    print("début")
    cardS = len(solution[2])
    cardJ = 7 * cardS
    print(cardS)

    dataOperateurs = pd.read_csv('operateurs.csv', sep=";")
    cardO = len(dataOperateurs.axes[0])
    dataNoms = dataOperateurs.iloc[0:cardO, 0:3]
    cardP = cardO
    noms = []
    for i in range(cardO):
        noms.append(dataNoms.iloc[i, 1] + " " + dataNoms.iloc[i, 2])
    print(noms)

    dataPostes = pd.read_csv('postes.csv', sep=";")
    nomsPostes = dataPostes.iloc[0:cardO, 1]
    print(nomsPostes)

    date = datetime.datetime(2023, 9, 4)

    o = np.zeros(cardJ)
    for j in range(0, len(o)):
        if j % 7 <= 4:
            o[j] = 1

    with open('res.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        jours = [""]
        for s in range(0, cardS):
            jours.extend(["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"])
        writer.writerow(jours)

        dates = [""]
        for j in range(0, cardJ):
            dates.append(date.strftime("%d")+"/"+date.strftime("%m")+"/"+date.strftime("%y"))
            date += datetime.timedelta(days=1)
        writer.writerow(dates)

        for i in range(0, cardO):
            planningPerso = [noms[i]]
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
                    planningPerso[7*s + jourRA + 1] = "RA" #décallage de 1 à cause du nom

            index = 0
            while index < len(affectationsJours):
                remplacement = affectationsJours[index]
                if remplacement[1] == i:
                    jourRemplacement = remplacement[0]
                    posteRemplacement = remplacement[2]
                    planningPerso[jourRemplacement + 1] = nomsPostes[posteRemplacement]
                    del affectationsJours[index]
                else:
                    index += 1

            writer.writerow(planningPerso)


def convertSolutionText(solution, kappa, sigma):
    #[valueObjectif2, affectations, trameFinale, True, valueObjectif1]
    affectations = solution[1]
    trameFinale  = solution[2]

    cardO = len(affectations)
    cardP = cardO
    cardR = cardO
    cardS = len(trameFinale)
    cardJ = 7*cardS


    with open("file", "w") as file_object:
        file_object.write(str(cardO) + "\n") #cardO
        file_object.write(str(cardP) + "\n") #cardP
        file_object.write(str(cardR) + "\n") #cardR
        file_object.write(str(cardS) + "\n") #cardS

        ligne = ""
        for p in range(0, cardP):
            ligne = ligne + "2"                   #TODO
        file_object.write(ligne + "\n")  # rho

        ligne = ""
        for j in range(0, cardJ):
            ligne = ligne + "2"                    #TODO
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

        for i in range(0, cardO):
            ligne = ""
            for j in range(0, cardJ):
                ligne = ligne + "2"             #TODO
            file_object.write(ligne + "\n")  # delta_ij

        for i in range(0, cardO):
            for j in range(0, cardJ):
                ligne = ""
                for p in range(0, cardP):
                    ligne = ligne + "2"          #TODO
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
                file_object.write(ligne + "\n")  # x_ijp

        file_object.write(str(int(solution[0])) + "\n")



