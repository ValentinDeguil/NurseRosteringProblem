y = [17, 19, 9, 1, 5, 20, 7, 11, 14, 3, 16, 21, 22, 10, 0, 23, 2, 12, 6, 13, 8, 4, 15, 18]

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