y = [1, 15, 22, 18, 12, 5, 20, 17, 8, 13, 4, 6, 2, 21, 14, 0, 10, 7, 11, 3, 9, 16, 19, 23]




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