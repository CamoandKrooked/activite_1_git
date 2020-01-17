import pickle
import os

#lines[Y][X]
#lines[10][9]


# Classe permettant de crééer la partie.
# Cette classe pourrait hériter d'une classe "Joueur" de manière à pouvoir crééer un profil joueur contenant plusieurs parties ??

class Partie:
    def __init__(self, nom) :
        self._nom = nom
        self._victoire = 0 # Permet de déterminer si la aprtie est terminée.
        self._difficulte = 'facile' # Attribut de la difficulté de la partie.
        self._wanted_X = 0 # Nouvelle position désirée par le joueur.
        self._wanted_Y = 0 # Nouvelle position désirée par le joueur.

        if self._difficulte == 'facile' :
            self._pos_X = 1 # Position de départ du joueur.
            self._pos_Y = 1 # Position de départ du joueur.
            self._pos_Xwin = 0 # Position à atteindre pour gagner la partie. Cet attribut est mis à jour dans fonctions.verifierVictoire().
            self._pos_Ywin = 0 # Position à atteindre pour gagner la partie. Cet attribut est mis à jour dans fonctions.verifierVictoire().
            self._porte = [(2,2), (4,8), (6,8), (9,2)] # Positions des portes de téléportation.


            
    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""

        return "Vous jouez la partie '{5}' en mode {4}.\n\
Le robot est en position x = {0} et y = {1}\n\
Il doit atteindre la position x = {2} et y = {3}" \
                .format(self._pos_X, self._pos_Y, self._pos_Xwin, self._pos_Ywin, self._difficulte, self._nom)



    def verifierPorte(self, carte) :
        """ Cette fonction permet de déterminer si le joueur se trouve sur une porte. Si tel est le cas, il est téléporté à la porte liée. La porte n est liée est à la porte n+1.
        De plus, après le passage par la porte, l'icône est replacée au même endroit."""
        
        i = 0
        for coordonnee in self._porte :
            if coordonnee == (self._pos_Y, self._pos_X) :
                print ("\n\nVous etes sur une porte !\n\n")

                # Si les coordonnées de la porte sont à un indice pair, le joueur est téléporté aux coordonnées de l'indice impair juste supérieur, et inversement.
                if (self._porte.index(coordonnee) % 2 == 0) :
                    #carte[self._pos_Y][self._pos_X] = "."
                    self._pos_Y, self._pos_X = self._porte[i+1]
                    carte[self._pos_Y][self._pos_X] = "X"
                    print (self._pos_Y, self._pos_X)
                if (self._porte.index(coordonnee) % 2 == 1) :
                    #carte[self._pos_Y][self._pos_X] = "."
                    self._pos_Y, self._pos_X = self._porte[i-1]
                    carte[self._pos_Y][self._pos_X] = "X"
                    print (self._pos_Y, self._pos_X)
                # Si une téléportation est effectuée, on sort de la boucle pour éviter d'être téléporté à l'infini.
                break
            i +=1
            
        for coordonnee in self._porte :
            (coordonnee_Y, coordonnee_X) = coordonnee
            if coordonnee != (self._pos_Y, self._pos_X) :
                carte[coordonnee_Y][coordonnee_X] = "."


    def verifierVictoire (self, carte, map) :
        """Cette fonction détermine si le joueur a atteind la sortie du labyrinthe. Si tel est le cas, l'attribut self._victoire est mis à jour, et la partie s'arrête."""

        # Tout d'abord, on détermine la position de la sortie du labyrinthe. Les attributs self._pos_Xwin et self._pos_Ywin sont mis à jour.
        if self._pos_Xwin == 0 :
            p = 0
            for ligne in map :
                if (ligne.find('U') != -1) :
                    self._pos_Xwin = ligne.find('U')
                    self._pos_Ywin = p
                p +=1

        # Si le joueur se trouve sur la position de victoire, l'attribut de victoire est mis à jour.
        if self._pos_Xwin == self._pos_X and self._pos_Ywin == self._pos_Y :
            self._victoire = 1



    def Deplacement(self, pas, carte, map):
        """Cette fonction récupère la liste de liste contenant la carte du labyrinthe
        ainsi que le nombre de pas voulu pour le déplacement. Elle détermine si ce déplacement est possible.
        Si il l'est, la position du robot est mise à jour."""
        
        # On vérifie que la position voulu n'est pas en dehors du labyrinthe.
##        if self._wanted_Y < 1 or self._wanted_Y > 9 or self._wanted_X < 1 or self._wanted_X > 8:
##            print("\nVous ne pouvez pas sortir du cadre du labyrinthe ...\n\n")

        
        # Ici, on traite le cas d'un déplacement dans le sens des X croissants.
        if self._wanted_X > self._pos_X :

            # On défile toutes les cas entre notre position actuelle et celle voulue.
            for i in range(self._pos_X +1, self._wanted_X +1) :
 
                if carte[self._pos_Y][i] == 'O' :
                    print("\nUn obstacle vous barre la route !\n\n")
                    break # S'il l'on rencontre un obstacle, où qu'il soit, on arrête la recherche.
                else :
                    print("\nDéplacement\n\n")
                    carte[self._pos_Y][self._pos_X] = " "
                    carte[self._wanted_Y][self._wanted_X] = "X"
                    self._pos_X = self._wanted_X

                    
        # Ici, on traite le cas d'un déplacement dans le sens des X décroissants.
        if self._wanted_X < self._pos_X :
            
            for i in range(self._wanted_X, self._pos_X) :

                if carte[self._pos_Y][i] == 'O' :
                    print("\nUn obstacle vous barre la route !\n\n")
                    break # S'il l'on rencontre un obstacle, où qu'il soit, on arrête la recherche.
                else :
                    print("\nDéplacement\n\n")
                    carte[self._pos_Y][self._pos_X] = " "
                    carte[self._wanted_Y][self._wanted_X] = "X"
                    self._pos_X = self._wanted_X

                    
        # Ici, on traite le cas d'un déplacement dans le sens des Y croissants.
        if self._wanted_Y > self._pos_Y :
            
            for i in range(self._pos_Y +1, self._wanted_Y +1) :

                if carte[i][self._pos_X] == 'O' :
                    print("\nUn obstacle vous barre la route !\n\n")
                    break # S'il l'on rencontre un obstacle, où qu'il soit, on arrête la recherche.
                else :
                    print("\nDéplacement\n\n")
                    carte[self._pos_Y][self._pos_X] = " "
                    carte[self._wanted_Y][self._wanted_X] = "X"
                    self._pos_Y = self._wanted_Y

                    
        # Ici, on traite le cas d'un déplacement dans le sens des Y décroissants.            
        if self._wanted_Y < self._pos_Y :
            
            for i in range(self._wanted_Y, self._pos_Y) :

                if carte[i][self._pos_X] == 'O' :
                    print("\nUn obstacle vous barre la route !\n\n")
                    break # S'il l'on rencontre un obstacle, où qu'il soit, on arrête la recherche.
                else :
                    print("\nDéplacement\n\n")
                    carte[self._pos_Y][self._pos_X] = " "
                    carte[self._wanted_Y][self._wanted_X] = "X"
                    self._pos_Y = self._wanted_Y
                        
        self.verifierPorte(carte)
        print ("Votre position est désormais X = ", self._pos_X, " et Y = ", self._pos_Y, ".\n")
        self.verifierVictoire (carte, map)

        # On remet les positions déisirées à 0, quelque soit le résultat de notre analyse.
        self._wanted_X = 0
        self._wanted_Y = 0




    def verifierPos(self):

        """ Cette fonction récupère le déplacement voulu par l'utilisateur
        et vérifie qu'il est correct. Elle retourne le pas du déplacement."""
        
        print("\nChoisissez votre déplacement de la manière suivante :\n")
        print("\tz : Pour monter\n\ts : Pour descendre\n\tq : Pour la gauche\n\td pour la droite\n\n")

        choix = input() # Variable récupérant la chaine de caractère du choix de l'utilisateur.

        # Le choix doit être composé d'une lettre et d'un chiffre, dans cet ordre.
        while (len(choix) != 2) :
            print("Saisie incorrecte, veuillez recommencer\n")
            choix = input()

        # Le choix doit être composé d'une lettre et d'un chiffre, dans cet ordre.    
        while (choix[0] != 'z') and (choix[0] != 'q') and (choix[0] != 's') and (choix[0] != 'd') or (choix[1].isdigit() == False) or (choix.isalnum() == False):

            print("Saisie incorrecte, veuillez recommencer\n")
            choix = input()

        # Le pas est le ciffre du choix.
        pas = int(choix[1])

        # On fait varier les attributs de positions voulues selon le choix de l'utilisateur.
        if choix[0] == 'z':
            print("\nVous avez demandé un déplacement vers le Nord sur", pas, "cases.\n")
            self._wanted_X = self._pos_X
            self._wanted_Y = self._pos_Y - pas
        if choix[0] == 'q':
            print("\nVous avez demandé un déplacement vers l'Ouest sur", pas, "cases.\n")
            self._wanted_X = self._pos_X - pas
            self._wanted_Y = self._pos_Y
        if choix[0] == 's':
            print("\nVous avez demandé un déplacement vers le Sud sur", pas, "cases.\n")
            self._wanted_X = self._pos_X
            self._wanted_Y = self._pos_Y + pas
        if choix[0] == 'd':
            print("\nVous avez demandé un déplacement vers l'Est sur", pas, "cases.\n")
            self._wanted_X = self._pos_X + pas
            self._wanted_Y = self._pos_Y

        print(self._wanted_X)
        print(self._wanted_Y)

        return pas
