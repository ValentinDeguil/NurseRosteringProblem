import numpy as np
import time
import coreFunctions
import methode2opt
import methodeGRASP
import convertSolution

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

#creerSigma([0,2,1,2,0,1,3,1,0,2,1,2,0,1,3,1,0,1,2,1,0,3,1,2,0])

def main():
    # Données du problème

    # kappa est une matrice de taille [nombre d'opérateurs x nombre de postes]
    # kappa[i, p] vaut 1 si l'opérateur i peut effectuer le poste p
    kappa = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    # sigme est une matrice de taille [nombre de postes x nombre de postes]
    # sigma[p, p'] vaut 1 si les postes p et p' sont permutables (donc sur le même créneau horaire)
    sigma = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    #sigma = [[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    #[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #[0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    #[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    #[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]]

    rho = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
    d = [3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    ##listeTaillePop = [10,20,50,100,200]
    ##listeTaillePop = [5,10,15,20,25]
    #listeTaillePop = [10, 20, 50, 100]
    ##listeNbRun = [100,500,2500,5000,10000]
    #listeNbRun = [100, 500, 1000, 2000]
    #nbTest = 50
    #for i in range(len(listeTaillePop)):
    #    for j in range(len(listeNbRun)):
    #        sumObj1 = 0
    #        sumObj2 = 0
    #        start = time.time()
    #        for k in range(nbTest):
    #            pop = methodeGRASP.constructionGRASP(listeTaillePop[i], listeNbRun[j], 24, 24, kappa, sigma)
    #            sumObj2 += pop[0][0]
    #            minObj1 = 1000
    #            for m in range(listeTaillePop[i]):
    #                if pop[0][0] == pop[m][0] and pop[m][4] < minObj1:
    #                    minObj1 = pop[m][4]
    #            sumObj1 += minObj1
    #        end = time.time()
    #        obj2moy = sumObj2/nbTest
    #        obj1moy = sumObj1 / nbTest
    #        print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
    #        print("obj2 moyen = ", obj2moy, "         ")
    #        print("obj1 moyen = ", obj1moy, "         ")
    #        print("Temps d'exécution moyen : ", (end - start)/nbTest)
    #        print()

    ##test verif solution
    #pop = methodeGRASP.constructionGRASP(5, 100, 24, 24, kappa, sigma)
    #convertSolutionToText.convertSolution(pop[0], kappa, sigma)
    #pop = methode2opt.rechercheLocale2optPopulation(20, 50, 24, 24, kappa, sigma)
    #for m in range(20):
    #    print(pop[m][0], " : ", pop[m][1])
    #coreFunctions.getAffectationsJour(pop[0], kappa, sigma, rho, d)

    ## test xijp
    #cpt1 = 0
    #cpt2 = 0
    #for i in range(20000):
    #    sol = coreFunctions.construireSol(24, 24, kappa, sigma, True, None)
    #    if sol[3]:
    #        cpt1 += 1
    #        affect = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d)
    #        if affect[0]:
    #            cpt2 += 1
    #print("cpt1 = ", cpt1)
    #print("cpt2 = ", cpt2)

    #pop = methode2opt.rechercheLocale2optPopulation(20, 500, 24, 24, kappa, sigma)
    #sol = pop[0]
    #print(sol[0], " : ", sol[1]);
    #if sol[3]:
    #    affect = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d)
    #    if affect[0]:
    #        convertSolution.convertSolutionCSV(sol, affect[1], d)

    sol = coreFunctions.construireSol(24, 24, kappa, sigma, False, [0,1,12,2,3,13,17,4,16,5,10,6,7,8,9,11,20,18,14,21,23,15,19,22])
    print(sol[0])
    affect = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d)
    print(affect[1])
    #sol = coreFunctions.construireSol(24, 24, kappa, sigma, False, [6,2,12,3,4,18,0,5,19,7,22,8,9,11,14,15,20,1,16,10,21,17,23,13])
    #print(sol[0])

    #sol = coreFunctions.construireSol(24, 15, kappa, sigma, False, [17,5,3,6,7,4,0,8,19,9,18,10,11,12,13,14,21,1,15,2,22,16,20,23])
    #print(sol[0], " : ", sol[1]);
    #print(sol[1])
    #print()
    #affect = sol[2]
    #for i in range(15):
    #    print(affect[i])

    ##test juste grasp
    ## listeTaillePop = [10,20,50,100,200]
    ## listeTaillePop = [5,10,15,20,25]
    #listeTaillePop = [10]
    ## listeNbRun = [100,500,2500,5000,10000]
    #listeNbRun = [100]
    #nbTest = 1
    #for i in range(len(listeTaillePop)):
    #    for j in range(len(listeNbRun)):
    #        best = 0
    #        start = time.time()
    #        for k in range(nbTest):
    #            pop = methodeGRASP.constructionGRASP(listeTaillePop[i], listeNbRun[j], 24, 24, kappa, sigma)
    #            best += pop[0][0]
    #        end = time.time()
    #        bestVal = best / nbTest
    #        print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
    #        print("bestVal moyen = ", bestVal, "         ")
    #        print("Temps d'exécution moyen : ", (end - start) / nbTest)
    #        print()

    #listeTaillePop = [10]
    ##listeTaillePop = [1, 2, 3, 4, 5]
    #listeNbRun = [50]
    ##listeNbRun = [5, 50, 100]
    #nbTest = 1
    #for i in range(len(listeTaillePop)):
    #    for j in range(len(listeNbRun)):
    #        best = 0
    #        start = time.time()
    #        for k in range(nbTest):
    #            print(k)
    #            pop = methodeGRASP.rechercheLocale2optPopulationGRASP(listeTaillePop[i],listeNbRun[j],24,22,kappa,sigma)
    #            best += pop[0][0]
    #        end = time.time()
    #        bestVal = best / nbTest
    #        print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
    #        print("bestVal moyen = ", bestVal, "         ")
    #        print("Temps d'exécution moyen : ", (end - start)/nbTest)
    #        print()
    #        for m in range(listeTaillePop[i]):
    #            print(pop[m][0], " : ", pop[m][1])

    ####taillePop = 20
    ####start = time.time()
    ####pop = methode2opt.rechercheLocale2optPopulation(taillePop, 100, 24, 22, kappa, sigma)
    ####end = time.time()
    ####for i in range(0, taillePop):
    ####    print(pop[i][0], " : ", pop[i][1])
    ####print("Temps d'exécution : ", end - start)
    ####convertSolution.convertSolutionText(pop[0], coreFunctions.getAffectationsJour(pop[0], kappa, sigma, rho, d), kappa, sigma, rho, d)

    #sol = coreFunctions.construireSol(24, 24, kappa, sigma, True, None)
    #affectationsJournalieres = coreFunctions.getAffectationsJour(sol, kappa, sigma, rho, d)
    #print(sol[0])
    #convertSolution.convertSolutionText(sol, affectationsJournalieres, kappa, sigma, rho, d)

    #pop = coreFunctions.construirePopulationSolution(taillePop, 2000, 24, 10, kappa, sigma)
    #for i in range(0, taillePop):
    #    print(pop[i][0], " : ", pop[i][1])

main()