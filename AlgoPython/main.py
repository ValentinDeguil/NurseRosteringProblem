import time
import coreFunctions
import methode2opt
import methodeGRASP

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
    #listeTaillePop = [1]
    ##listeNbRun = [100,500,2500,5000,10000]
    #listeNbRun = [50]
    #nbTest = 30
    #for i in range(len(listeTaillePop)):
    #    for j in range(len(listeNbRun)):
    #        best = 0
    #        start = time.time()
    #        for k in range(nbTest):
    #            pop = methode2opt.rechercheLocale2optPopulation(listeTaillePop[i], listeNbRun[j], 24, 24, kappa, sigma)
    #            best += pop[0][0]
    #        end = time.time()
    #        bestVal = best/nbTest
    #        print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
    #        print("bestVal moyen = ", bestVal, "         ")
    #        print("Temps d'exécution moyen : ", (end - start)/nbTest)
    #        print()

    #test juste grasp
    # listeTaillePop = [10,20,50,100,200]
    # listeTaillePop = [5,10,15,20,25]
    listeTaillePop = [10,20,50]
    # listeNbRun = [100,500,2500,5000,10000]
    listeNbRun = [100,500,1000]
    nbTest = 50
    for i in range(len(listeTaillePop)):
        for j in range(len(listeNbRun)):
            best = 0
            start = time.time()
            for k in range(nbTest):
                pop = methodeGRASP.constructionGRASP(listeTaillePop[i], listeNbRun[j], 24, 24, kappa, sigma)
                best += pop[0][0]
            end = time.time()
            bestVal = best / nbTest
            print("taillePop = ", listeTaillePop[i], "nbRun = ", listeNbRun[j])
            print("bestVal moyen = ", bestVal, "         ")
            print("Temps d'exécution moyen : ", (end - start) / nbTest)
            print()

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