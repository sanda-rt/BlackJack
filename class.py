import random
 
class Carte:
    def __init__(self):
        self.valeur = ( 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')

        self.symbole = ('♥', '♦', '♣', '♠')

        self._carte = [ (v, s) for v in self.valeur for s in self.symbole]
    
    @property
    def carte(self):
        return self._carte

    def melanger(self):
        return random.shuffle(self.carte)
    
    def partager(self):
        return self.carte.pop()
    
    def restaurer(self):
        self._carte = [ (v, s) for v in self.valeur for s in self.symbole]

class Jeu:
    def __init__(self):
        self.c = Carte()
        self.c.melanger()
        self.joueur = [self.c.partager()]
        self.croupier = [self.c.partager()*2]
    
    def pointage(self, mains: list):
        points = 0
        """mains = reversed(mains)
        print(mains)"""
        for x in mains:
            if x[0] == 'A':
                points += 1 if points + 11 > 20 else 11
            elif x[0] in ['J', 'Q', 'K']:
                points += 10
            else:
                points += x[0]
        return points

if __name__ == "__main__":
    maliste = [(10, 'T'), ('A', 'C'), (10, 'P')]
    j = Jeu()
    print(j.pointage(maliste))