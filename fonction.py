from data import carte, fond
from random import shuffle

mise = 0

def passer():
    global c
    c = list(carte)
    shuffle(c)

def share():
    return c.pop()

def checking(j : list):
    point = 0
    valeurs = {
        'J': 10,
        'Q': 10,
        'K': 10,
        
    }
    for i in range(len(j) - 1):
        if j[i][0] in ['J', 'Q', 'K']:
            point += 10
        elif j[i][0] == 'A':
            point += 1 if point + j[i + 1] > 20 else 11
        else:
            point += j[0]
    
    return point, j

def tourCroupier(n:list, m:list, mise):
    gain = 0
    pointJoueur = checking(n)
    while True:
        print("Les cartes du croupier :", *m, " Points : " + str(checking(m)))

        pointCroupier = checking(m)

        if pointCroupier == 21 and len(m) == 2:
            print("BlackJack")
            return gain
        if pointCroupier > 21:
            print("Busted !!!")
            gain += mise * 2
            return gain
        if pointCroupier > pointJoueur and pointCroupier < 21:
            print("Player lose !!!")
            return gain
        if pointCroupier == pointJoueur:
            print("Égalité !!!")
            return mise
        m.append(share())
    

def save():
    with open("fond.txt", 'w') as f:
        f.write(str(fond))
    f.close()

def main():
    global fond
    passer()

    print(f"Votre solde : {fond} Ar")
    mise = int(input("Votre mise : "))
    fond -= mise
    print(f"Votre solde : {fond} Ar")

    carteJoueur = [share(), share()]
    carteCroupier = [share(), share()]

    pointJoueur = 0

    print("Les cartes du joueur : ", *carteJoueur, " Votre point : " + str(checking(carteJoueur)))
    print("Les cartes du croupier : {}".format(carteCroupier[0]))

    if checking(carteJoueur) == 21:
        print("BlackJack !!!")
        fond += mise * 1.5
    
    while True:
        q = int(input(
        "1. Hit\n"
        "2. Stand\n"
        "3. Double\n"
        "Entrez votre choix : "
        ))
    
        match q:
            case 1:
                carteJoueur.append(share())
                print("Votre carte : ", *carteJoueur, " Points : " + str(checking(carteJoueur)))

            case 2:
                pointJoueur = checking(carteJoueur)
                fond += tourCroupier(carteJoueur, carteCroupier, mise)
                break
            
            case 3:
                print("Votre carte : ", *carteJoueur, " Votre point : " + str(checking(carteJoueur)))

                fond -= mise
                mise *= 2
                
                fond += tourCroupier(carteJoueur, carteCroupier, mise)
                break

        pointJoueur = checking(carteJoueur)
        if pointJoueur > 21:
            print("Busted !!!")
            break
    print(f"Votre solde : {fond} Ar")
        

if __name__ == "__main__":
    """while True:
        print(f"{'='*12} BlackJack 21 {'='*12}".center(100))
        print("1. Jouer\n2. Quitter")
        choix = int(input("Entrez votre choix : "))

        match choix:
            case 1:
                main()
            case 2:
                save()
                break"""
    print(checking([('A', 'Q'), ('Q', 'Z'), ('J', 'A')]))