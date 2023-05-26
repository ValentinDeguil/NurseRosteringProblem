#import numpy as np
import time
import coreFunctions
import methode2opt
import methodeGRASP
import convertSolution
#import generateInstance
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

    sigma = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]]

    print("kappa")
    for i in range(len(kappa)):
        print(kappa[i])
    print("sigma")
    for i in range(len(sigma)):
        print(sigma[i])

    fac = [10,15]

    # Construction de la solution
    taillePop = 3
    nbEssais = 100 #nombre de solutions générées, on ne garde que les taillePop meilleures
    start = time.time()
    pop = methode2opt.rechercheLocale2optPopulation(taillePop, nbEssais, 24, 24, kappa, sigma, rho, fac )
    end = time.time()
    print("                                     ") # pour effacer le chargement
    print("Population générée :")
    for i in range(0, taillePop):
        print(pop[i][0], " : ", pop[i][1])
    print("Temps d'exécution :", end - start, "secondes")

    sol = pop[0]
    aff = sol[1]
    tr = sol[2]
    trameInit = []
    for s in range(24):
        affectSemaine = aff.copy()
        for p in range(24):
            affectSemaine[p] = (affectSemaine[p] + s) % 24
        trameInit.append(affectSemaine.copy())

    for sem in range(24):
        print("semaine", sem)
        score = coreFunctions.calculObjectif2Semaine(trameInit[sem], tr[sem], 24, kappa, rho, fac, sigma)
        print(score)
    #[valueObjectif2, affectations, trameFinale, True, valueObjectif1]

    sol = pop[0] # y (affectations rang) et z (affectations aux postes par semaine)
    affect = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d) # x (affectations aux postes par jour)
    if affect[0]:
        print("Solution exportée au format CSV")
        convertSolution.convertSolutionCSV(sol, affect[1], d, nomsPostes, nomsOperateurs)

#main()

def main2():
    print("test")
    kappa = [
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[0,0,0,1,0,1,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[0,0,0,1,0,1,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[1,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,0,0,1,0,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[0,0,0,1,0,1,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[1,0,0,1,0,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0],
[0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
[0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,1,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,0,1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,0,1],
[0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
[0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1]]

    creneaux = [5,1,4,1,0,4,0,4,3,4,5,4,1,0,4,1,4,0,1,0,5,4,1,0,3,4,1,0,0,4,5,0,1,4,0,2]
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

    for i in range(36):
        print(sigma[i])

    rho = [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,0,1,1,0,1,1,0,1]
    fac = [22,15,2]
    cardS = 36
    cardO = 36

    taillePop = 5000
    nbEssais = 10000  # nombre de solutions générées, on ne garde que les taillePop meilleures
    start = time.time()
    #pop = methode2opt.rechercheLocale2optPopulation(taillePop, nbEssais, 36, cardS, kappa, sigma, rho, fac)
    pop = methodeGRASP.constructionGRASP(taillePop,100,cardO,cardS,kappa,sigma,rho,fac)
    end = time.time()
    print("                                     ")  # pour effacer le chargement
    print("Population générée :")
    for i in range(min(taillePop,5)):
        print(pop[i][0], " : ", pop[i][1])
    print("Temps d'exécution :", end - start, "secondes")
    sol = pop[0]
    #[valueObjectif2, affectations, trameFinale, True, valueObjectif1]
    aff = sol[1]
    tr = sol[2]
    trameInit = []
    for s in range(cardS):
        affectSemaine = aff.copy()
        for p in range(36):
            affectSemaine[p] = (affectSemaine[p] + s) % 36
        trameInit.append(affectSemaine.copy())
    #for sem in range(cardS):
    #    print("semaine", sem)
    #    score = coreFunctions.calculObjectif2Semaine(trameInit[sem], tr[sem], cardS, kappa, rho, fac, sigma)
    #    print(score)


    #print("test fixé")
    #aff = [14, 1, 26, 0, 31, 27, 6, 12, 18, 20, 15, 11, 25, 28, 29, 17, 2, 19, 9, 3, 30, 32, 22, 4, 7, 35, 8, 23, 34, 21, 24, 33, 10, 16, 5, 13]
    #solfixe = coreFunctions.construireSol(36, 2, kappa, sigma, False, aff, rho, fac)
    #print(solfixe[0], " : ", solfixe[1])
    #trameInit = []
    #for s in range(2):
    #    affectSemaine = aff.copy()
    #    for p in range(36):
    #        affectSemaine[p] = (affectSemaine[p] + s) % 36
    #    trameInit.append(affectSemaine.copy())
    #for sem in range(2):
    #    print("semaine", sem)
    #    score = coreFunctions.calculObjectif2Semaine(trameInit[sem], solfixe[2][sem], 36, kappa, rho, fac, sigma)
    #    print(score)
    #print(trameInit)

main2()