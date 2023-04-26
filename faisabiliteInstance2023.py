# Cette fonction permet de créer des matrices kappa pour l'instance de 2023
# On définit 3 profils types d'opérateurs : Process, Rec et Polyvalent. Chacun possède uniquement les compétences des postes correspondants.
# Ensuite, on peut choisir de convertir un certain nombre de process en polyv et de rec en polyv
def creerKappa():

    opeProcess  = [1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    opePolyv    = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    opeRec      = [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]

    cardPolyv = 5
    for nbProcess in range(0,24): #range(0,23+1) pour tout avoir
        for nbRec in range(0,9):  #range(0,8+1) pour tout avoir
            totalProcess = 23 - nbProcess
            totalPolyv = nbProcess + 5 + nbRec
            totalRec = 8 - nbRec
            print("Instance", nbProcess, nbRec, " au final :", totalProcess, totalPolyv, totalRec)
            kappa = []
            for i in range(totalProcess):
                kappa.append(opeProcess.copy())
            for i in range(totalPolyv):
                kappa.append(opePolyv.copy())
            for i in range(totalRec):
                kappa.append(opeRec.copy())
            print("kappa = [")
            for i in range(len(kappa) - 1):
                print(str(kappa[i]) + ",")
            print(str(kappa[len(kappa) - 1]) + "]")

creerKappa()