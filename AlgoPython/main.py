import time
import coreFunctions
import methode2opt
import methodeGRASP
import convertSolutionToText

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
    #pop = methode2opt.rechercheLocale2optPopulation(20, 1000, 24, 15, kappa, sigma)
    #for m in range(5):
    #    print(pop[m][0], " : ", pop[m][1])

    sol = coreFunctions.construireSol(24, 15, kappa, sigma, False, [17,5,3,6,7,4,0,8,19,9,18,10,11,12,13,14,21,1,15,2,22,16,20,23])
    print(sol[0], " : ", sol[1]);
    print(sol[1])
    print()
    affect = sol[2]
    for i in range(15):
        print(affect[i])

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

    #listeTaillePop = [3]
    ##listeTaillePop = [1, 2, 3, 4, 5]
    #listeNbRun = [50]
    ##listeNbRun = [5, 50, 100]
    #nbTest = 50
    #for i in range(len(listeTaillePop)):
    #    for j in range(len(listeNbRun)):
    #        best = 0
    #        start = time.time()
    #        for k in range(nbTest):
    #            print(k)
    #            pop = methodeGRASP.rechercheLocale2optPopulationGRASP(listeTaillePop[i],listeNbRun[j],24,24,kappa,sigma)
    #            best += pop[0][0]
    #        end = time.time()
    #        bestVal = best / nbTest
    #        print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
    #        print("bestVal moyen = ", bestVal, "         ")
    #        print("Temps d'exécution moyen : ", (end - start)/nbTest)
    #        print()
    #        for m in range(listeTaillePop[i]):
    #            print(pop[m][0], " : ", pop[m][1])

    #taillePop = 5
    #start = time.time()
    #pop = methodeGRASP.methode2optGRASP(taillePop, 100, 24, 24, kappa, sigma)
    #end = time.time()
    #for i in range(0, taillePop):
    #    print(pop[i][0], " : ", pop[i][1])
    #print("Temps d'exécution : ", end - start)

    #sol = coreFunctionsAmelioration.construireSol(24, 24, kappa, sigma, True, None)
    #print("sol = ", sol[0], " : ", sol[1])

    ##verif optimilité resoudreSemaine
    #cumul = 0
    #nbTest = 10000
    #start = time.time()
    #for i in range(nbTest):
    #    sol = coreFunctionsAmelioration.construireSol(24, 24, kappa, sigma, False, [1, 19, 10, 18, 22, 6, 12, 9, 13, 23, 0, 4, 2, 21, 3, 20, 17, 16, 14, 11, 7, 5, 8, 15])
    #    #sol = coreFunctionsAmelioration.construireSol(24, 24, kappa, sigma, False, [16, 0, 8, 22, 20, 9, 14, 7, 19, 18, 4, 11, 17, 2, 5, 6, 10, 12, 23, 15, 21, 1, 3, 13])
    #    #print("sol = ",sol[0]," : ", sol[1])
    #    cumul += sol[0]
    #    #print(sol[0])
    #end = time.time()
    ##for i in range(24):
    #    #print("semaine",i,"=",sol[2][i])
    #print(cumul/nbTest)
    #print("Temps d'exécution : ", end - start)

    #pop = coreFunctions.construirePopulationSolution(taillePop, 2000, 24, 10, kappa, sigma)
    #for i in range(0, taillePop):
    #    print(pop[i][0], " : ", pop[i][1])

main()