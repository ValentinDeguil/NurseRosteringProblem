import numpy as np
import time
import coreFunctions
import methode2opt
import methodeGRASP
import convertSolution
import generateInstance
import readData

def creerSigma(creneaux):
    cardP = len(creneaux)
    sigma = []
    for p in range(cardP):
        ligne = []
        for p2 in range(cardP):
            if creneaux[p] == creneaux[p2]:
                ligne.append(1)
            else:
                ligne.append(0)
        sigma.append(ligne)
    for i in range(cardP):
        print(sigma[i])
    return sigma

def main():
    # Données du problème

    #rho = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0] #Celui avec lequel j'ai toujours travaillé
    #rho = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1] #Le nouveau qui est cohérent avec les données
    kappa, sigma, rho, d, nomsPostes, nomsOperateurs = readData.readData()

    # Construction de la solution
    taillePop = 5
    nbEssais = 100 #nombre de solutions générées, on ne garde que les taillePop meilleures
    start = time.time()
    pop = methode2opt.rechercheLocale2optPopulation(taillePop, nbEssais, 24, 24, kappa, sigma)
    end = time.time()
    print("                                     ") # pour effacer le chargement
    print("Population générée :")
    for i in range(0, taillePop):
        print(pop[i][0], " : ", pop[i][1])
    print("Temps d'exécution :", end - start, "secondes")

    sol = pop[0] # y (affectations rang) et z (affectations aux postes par semaine)
    affect = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d) # x (affectations aux postes par jour)
    if affect[0]:
        print("Solution exportée au format CSV")
        convertSolution.convertSolutionCSV(sol, affect[1], d, nomsPostes, nomsOperateurs)

main()