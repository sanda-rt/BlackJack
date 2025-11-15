import random
import csv
from pathlib import Path
 
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
        documents = Path.home() / "Documents"
        self.fichier = documents / "data.csv"
    
    def pointage(self, mains: list):
        points = 0
        for x in mains:
            if x[0] == 'A':
                points += 1 if points + 11 > 21 else 11
            elif x[0] in ['J', 'Q', 'K']:
                points += 10
            else:
                points += x[0]
        return points
    def sauvegarder(self, nom: str, argent:int):
        with open(self.fichier, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "argent"])
            writer.writerow([nom, argent])
    def charger(self):
        with open(self.fichier, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for ligne in reader:
                nom = ligne[0]
                argent = int(ligne[1])
                return nom, argent

if __name__ == "__main__":
    j = Jeu()
    j.sauvegarder('Sanda', '6000')
    print(j.charger())