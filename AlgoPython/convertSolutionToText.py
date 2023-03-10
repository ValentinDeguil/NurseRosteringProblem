
def convertSolution(solution, kappa, sigma):
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



