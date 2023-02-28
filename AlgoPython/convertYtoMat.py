y = [4, 12, 9, 22, 23, 20, 18, 0, 15, 21, 6, 1, 17, 7, 11, 2, 16, 14, 10, 19, 5, 8, 3, 13]

cardO = 24

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