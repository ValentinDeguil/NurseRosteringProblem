from itertools import permutations as perm
import numpy as np

# Pour tenter de prouver l'infaisabilité de l'instance 2023
def test():
    cardO = 36
    postes7 = [1,3,12,15,18,22,26,32]

    positionsRecSem0 = []
    l = []
    for i in range(7):
        l.append(1)
    for i in range(36-7):
        l.append(0)
    s = set()
    for p in perm(l):
        s.add(p)

    tab = []
    for val in s:
        tab.append(np.asarray(val))
    print(tab)
    print(type([1,2,3]))
    print(type(tab[0]))
test()