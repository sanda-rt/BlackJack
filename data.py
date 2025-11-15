from random import shuffle

valeur = ( 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')

symbole = ('♥', '♦', '♣', '♠')

carte = [ (v, s) for v in valeur for s in symbole]

fond = 0

try:
    with open("fond.txt", 'r') as f:
        fond = f.read()
    f.close()

except:
    with open("fond.txt", 'w') as f:
        f.write("10000")
    f.close()

fond = int(fond)