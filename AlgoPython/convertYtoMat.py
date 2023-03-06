y = [8, 13, 1, 14, 12, 0, 23, 10, 16, 20, 18, 7, 2, 6, 19, 11, 4, 22, 5, 9, 17, 3, 15, 21]

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