import pickle
import os
import fonctions



# Variables nécessaires au programme
fin = False # Permet de quitter le jeu.
choix = "0" # Permet de choisir une option.
sauvegarde = list() # Liste des parties sauvegardées
existant = False



def enregistrerPartie(nom_partie):
    """Cette fonction a pour but d'enregistrer une nouvelle partie. Elle vérifie tout d'abord si le fichier de sauvegarde existe et le crée sinon.
    Puis, elle vérifie également qu'une partie portant le même nom n'existe pas déjà. Si oui, la partie précédente est écrasée."""

    # Nous vérifions si le fichier de scores existe.
    if os.path.exists("fichier_de_scores"):

        # Si il existe et qu'il est vide, on enregistre directement notre liste de parties en cours dedans.
        if os.path.getsize("fichier_de_scores") == 0 :

            
            with open("fichier_de_scores","wb") as fichier :
                print("On enregistre")
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(sauvegarde)
                
        # S'il n'est pas vide. Nous récupérons son contenu dans une liste et vérifions qu'une partie portant le même nom n'existe pas déjà.    
        else :

            
            with open("fichier_de_scores", "rb") as fichier :
                mon_depickler = pickle.Unpickler(fichier)
                parties_sauvegardees = mon_depickler.load()

            # Vérification qu'une partie portant le même nom que celui choisi par l'utilisateur n'existe pas déjà.
            for elt in parties_sauvegardees :
                if elt._nom == nom_partie :
                    existant = True
                    break
                else :
                    existant = False
                    
            # Si une partie portant le même nom existe, elle est écrasée.
            if existant == True :
                print("\n\nUne partie du même nom existe déjà. Elle est écrasée.\n")

                # Traitement de la liste enregistrée de manière à ne pas conserver deux parties du même nom.
                parties_sauvegardees[:] = [sauvegarde[0] if x._nom == nom_partie else x for x in parties_sauvegardees]
                
                with open("fichier_de_scores", "wb") as fichier :
                    mon_pickler = pickle.Pickler(fichier)
                    mon_pickler.dump(parties_sauvegardees)
                    
            # Sinon, la sauvegarde est créée.    
            else :
                print("\n\nLa partie va être créée.\n")
                parties_sauvegardees.extend(sauvegarde)
                with open("fichier_de_scores", "wb") as fichier :
                    mon_pickler = pickle.Pickler(fichier)
                    mon_pickler.dump(parties_sauvegardees)

    # Si le fichier de score n'existe pas, c'est qu'il a mal été créé dans le main.            
    else :
        print("Le fichier de score n'existe pas. Relancez le jeu.\n")



def chargerPartie(sauvegarde):
    """Cette fonction permet de charger une partie précédement sauvegardée et de la reprendre là où elle s'était arrêtée.
    De plus, elle reprendre la boucle du jeu normale."""

    # L'utilisateur saisi le nom de la partie à charger. Il peut connaitre les noms grâce à la fonction afficherPartie().
    print("\nTappez le nom de la partie que vous souhaitez charger\n")
    nom_partie = input("\n")

    existant = False
    i = 0
    
    # Nous vérifions si le fichier de scores existe.
    if os.path.exists("fichier_de_scores"):

        # Si il existe et qu'il est vide, on enregistre directement notre partie en cours dedans.
        if os.path.getsize("fichier_de_scores") == 0 :
            print("\nLe fichier de score est vide.\n")
                
        # S'il n'est pas vide. Nous récupérons son contenu dans une liste et vérifions qu'une partie portant le même nom n'existe pas déjà.    
        else :
            with open("fichier_de_scores", "rb") as fichier :
                mon_depickler = pickle.Unpickler(fichier)
                parties_sauvegardees = mon_depickler.load()
                
            # Vérification qu'une partie portant le même nom que celui choisi par l'utilisateur n'existe pas déjà.
            for elt in parties_sauvegardees :
                if elt._nom == nom_partie :
                    game = elt
                    existant = True
                    break
                
                else :
                    print("\nCette partie n'existe pas. Êtes-vous certain de l'orthographe utilisé ?\n")

    # Si la partie existe :
    if existant == True :

        # On vérifie que la carte du jeu existe bel et bien.            
        if os.path.exists("cartes\\facile.txt"):
            print("\n\nLa carte est existante.")

            # Si la carte existe, on la récupère sous forme d'une liste de chaine de caractères. Chaque chaine est une ligne du labyrinthe.
            with open("cartes\\facile.txt", "r") as fichier :
                map = fichier.readlines()
                
                Axe_X = []
                carte = []

                # On transforme notre liste de chaine en liste de listes, pour pouvoir travailler sur chaque élément facilement.
                for ligne in map :
                    for caractere in ligne :
                        Axe_X.append(caractere)
                        
                    carte.append(Axe_X)
                    Axe_X = []
                
                # Pour le moment, la carte est dans son état initial. Il nous faut donc lui donner l'état qu'elle avait au moment où la partie s'est arrêtée.
                
                # La position orininelle du joueur est remplacée par un blanc.
                carte[1][1] = ' '
                # La dernière position connue du joueur est mise à jour.
                carte[game._pos_Y][game._pos_X] = 'X'
                # On affiche la carte sous forme de texte.
                for i in range(len(carte)):
                    for j in range(len(carte[i])):
                        print(carte[i][j], end='')
                        
                print() # Un saut de ligne
                
        else :
            print ("\n\nLa carte n'existe pas.\n\n")

        # Reprise normale de la boucle du jeu.
        continuer = True

        while game._victoire != 1 and continuer == True:
            pas = fonctions.Partie.verifierPos(game)
            fonctions.Partie.Deplacement(game, pas, carte, map)
            os.system('cls')
            # On affiche la carte sous forme de texte.
            for i in range(len(carte)):
                for j in range(len(carte[i])):
                    print(carte[i][j], end='')
                    
            sauvegarde.append(game)
            enregistrerPartie(nom_partie)
            sauvegarde.clear()

            print("\n\nVoulez-vous quitter et sauvegarder la partie en cours ? Tappez 'oui'.\n")
            print("\nSinon, tappez 'non'.\n")
            sortir = input("\n")
            if sortir == 'oui' and game._victoire != 1 :
                continuer = False
                
        if game._victoire == 1:
            print("\n\nFélicitations, vous avez trouvé la sortie !\n")
            supprimerPartie(nom_partie)


def quitter():
    """Fonction permettant de quitter le jeu."""

    # La variable globale fin met un terme à la boucle while du main.
    global fin
    fin = True



def regles():
    """Fonction permettant d'afficher les règles du jeu"""

    print("\nLe jeu est très simple.\n\nVotre personnage est représenté par 'X'.")
    print("Les portes sont représentées par '.'.\nLa sortie du labyritnhe est représentée par 'U'.\n")
    print("Vous devez choisir une direction suivie du nombre de pas dans cette direction.\n")


def afficherParties():
    """Fonction permettant d'afficher les parties sauvegardeées."""

    if os.path.exists("fichier_de_scores"):

        # Si il existe et qu'il est vide, on enregistre directement notre partie en cours dedans.
        if os.path.getsize("fichier_de_scores") == 0 :
            print("\nAucune partie n'est enregistrée.\n")

        else :
            with open("fichier_de_scores", "rb") as fichier :
                mon_depickler = pickle.Unpickler(fichier)
                parties_sauvegardees = mon_depickler.load()
                for elt in parties_sauvegardees :
                    print ("\nLa partie '", elt._nom,"' est en mode", elt._difficulte,".\n")
    else :
        print("\nLe fichier de score n'existe pas encore. Jouez une partie pour le créer.\n")


def supprimerPartie(nom_partie):
    """ Cette fonction permet de supprimer une partie une fois qu'elle est terminée."""

    # Nous récupérons son contenu dans une liste et vérifions qu'une partie portant le même nom n'existe pas déjà. 
    with open("fichier_de_scores", "rb") as fichier :
        mon_depickler = pickle.Unpickler(fichier)
        parties_sauvegardees = mon_depickler.load()

    # Traitement de la liste supprimant la partie actuellement nommée dans la variable nom_partie
    parties_sauvegardees[:] = [parties_sauvegardees.remove(x) if x._nom == nom_partie else x for x in parties_sauvegardees]

    # S'il n'y a plus de parties dans parties_sauvegardees, on vide le fichier de scores.
    if len(parties_sauvegardees) == 1 :
        with open("fichier_de_scores", "wb") as fichier :
            pass
    # Si il reste des partie, on enregistre.
    else :
        with open("fichier_de_scores", "wb") as fichier :
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(parties_sauvegardees)


##    if os.path.getsize("fichier_de_scores") == 0 :
##        print("\n\nFichier vide.\n")
##    else :
##        print("\n\nFichier pas vide.\n")
    
def jeu() :
    """Fonction retournant la boucle du jeu. Nécessaire car on ne peut placer d'arguments dans le switch."""
    
    return jouer(sauvegarde)

def charger():
    """Fonction retournant la boucle du jeu. Nécessaire car on ne peut placer d'arguments dans le switch."""
    
    return chargerPartie(sauvegarde)

def jouer(sauvegarde):
    """Boucle principale du jeu. Cette fonction charge la carte du jeu puis gère la boucle de jeu."""
    
    # On vérifie que la carte du jeu existe bel et bien.            
    if os.path.exists("cartes\\facile.txt"):
        print("\n\nLa carte est existante.")

        # Si la carte existe, on la récupère sous forme d'une liste de chaine de caractères. Chaque chaine est une ligne du labyrinthe.
        with open("cartes\\facile.txt", "r") as fichier :
            map = fichier.readlines()
            
            Axe_X = []
            carte = []

            # On transforme notre liste de chaine en liste de listes, pour pouvoir travailler sur chaque élément facilement.
            for ligne in map :
                for caractere in ligne :
                    Axe_X.append(caractere)
                    
                carte.append(Axe_X)
                Axe_X = []
                
            # On affiche la carte sous forme de texte.
            for i in range(len(carte)):
                for j in range(len(carte[i])):
                    print(carte[i][j], end='')
                    
            print() # Un saut de ligne

            # On affiche la carte sous forme de liste de listes.
##            for i in range(len(carte)):
##                    print(carte[i], end='\n')

    else :
        print ("\n\nLa carte n'existe pas.\n\n")

    continuer = True
    nom_partie = input("Choisissez le nom de cette partie (pour la sauvegarde) :\n") 
    game = fonctions.Partie(nom_partie)

    # Le joueur joue tant qu'il n'a pas gagné ou qu'il ne souhaite pas arrêter.
    while game._victoire != 1 and continuer == True:
        pas = fonctions.Partie.verifierPos(game)
        fonctions.Partie.Deplacement(game, pas, carte, map)
        os.system('cls')
        # On affiche la carte sous forme de texte.
        for i in range(len(carte)):
            for j in range(len(carte[i])):
                print(carte[i][j], end='')

        # Mise à jour des fichiers de sauvegarde.        
        sauvegarde.append(game)
        enregistrerPartie(nom_partie)
        sauvegarde.clear()

        # Demande à l'utilisateur s'il souhaite arrêter de joueur.
        print("\n\nVoulez-vous quitter et sauvegarder la partie en cours ? Tappez 'oui'.\n")
        print("\nSinon, tappez 'non'.\n")
        sortir = input("\n")
        if sortir == 'oui' and game._victoire != 1 :
            continuer = False
            
    # Si le joueur a gagné, on sort de la boucle.        
    if game._victoire == 1:
        print("\n\nFélicitations, vous avez trouvé la sortie !\n")
        supprimerPartie(nom_partie)







                # MAIN



def switch(choix):
    """Fonction permettant de choisir l'action à effectuer."""
    
    switcher = {
        "1": regles,
        "2": jeu,
        "3": charger,
        "4": afficherParties,
        "5": quitter,
    }
    function = switcher.get(choix, lambda: "Choix invalide.\n")
    function() # Appelle de la fonction choisie



# Nous vérifions si le fichier de scores existe.
# A défaut, il sera créé.
if os.path.exists("fichier_de_scores"):
    print("\nLe fichier de score existe.\n")

else :
    print("Le fichier de score n'existe pas encore.\n")
    with open("fichier_de_scores","wb") as fichier :
        pass


while fin != True :
    # Création et affichage du menu d'acceuil.
    print ("\n\nBonjour et bienvenue dans le labyrinthe !\n\n")
    print ("Tapez 1 :\t Pour consultez les règles du jeu.\n")
    print ("Tapez 2 :\t Pour jouer.\n")
    print ("Tapez 3 :\t Pour charger une partie.\n")
    print ("Tapez 4 :\t Pour afficher les parties sauvegardées.\n")
    print ("Tapez 5 :\t Pour quitter.\n")
    choix = input("")

    switch(choix)
