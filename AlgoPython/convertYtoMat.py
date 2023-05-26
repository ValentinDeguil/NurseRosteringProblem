# Ce script me permet simplement de convertir un vecteur d'affectation Y en matrice en deux dimensions.
# Elle peut être réutilisée sous cette forme dans les modèles mathématiques pour vérifier quelles sont les
# réaffectations optimales en fonction d'un Y donné.

y = [4, 1, 19, 14, 5, 13, 18, 15, 0, 8, 6, 9, 11, 3, 2, 7, 16, 21, 23, 17, 20, 12, 10, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

cardO = 36

res = "["

ligne = "["
if y[0]==0:
    ligne = ligne + "1"
else:
    ligne = ligne + "0"
for j in range(1,cardO):
    ligne = ligne + ","
    if y[0] == j:
        ligne = ligne + "1"
    else:
        ligne = ligne + "0"
ligne = ligne + "]"
res = res + ligne

for i in range(1,cardO):
    res = res + ",\n"
    ligne = "["
    if y[i] == 0:
        ligne = ligne + "1"
    else:
        ligne = ligne + "0"
    for j in range(1, cardO):
        ligne = ligne + ","
        if y[i] == j:
            ligne = ligne + "1"
        else:
            ligne = ligne + "0"
    ligne = ligne + "]"
    res = res + ligne

res = res + "]"

print(res)