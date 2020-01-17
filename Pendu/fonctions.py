import pickle
import os
import donnees
import binascii as bi


#Variables nécessaires au programme
existant = True # Le compte du joueur est-il existant ?

def afficher_scores():
    """Cette fonction a pour but d'afficher les scores enregistrés par le programme."""

    # Nous vérifions si le fichier de scores existe.
    if os.path.exists("fichier_de_scores"):
        print("\n\nLe fichier de score est existant.\nRécupération des données.")
        
        with open("fichier_de_scores", "rb") as fichier :
            mon_depickler = pickle.Unpickler(fichier)
            scores = mon_depickler.load()
        print ("Les scores sont : {0}\n\n".format(scores))

    else :
        print ("\n\nLe fichier de scores n'existe pas.\n\n")

                    ####################
                    ####################

        
def recuperer_score (pseudo_joueur):
    """Cette fonction a pour but de récupérer les scores enregistré \
        par le programme.
        Elle retourne le dictionnaire de score s'il existe"""
    
    # Nous vérifions si le fichier de scores existe.
    if os.path.exists("fichier_de_scores"):
        print("\n\nLe fichier de score est existant.\n\nRécupération des données.\n\n")
        
        with open("fichier_de_scores", "rb") as fichier :
            mon_depickler = pickle.Unpickler(fichier)
            scores_actuels = mon_depickler.load()
            for cle, valeur in scores_actuels.items() :
                if cle.lower() == pseudo_joueur.lower() :
                    print("\n{0}, votre score est de {1}.\n\n".format(pseudo_joueur, valeur))

    else :
        print ("\n\nAucun score n'est enregistré.\n\n")

    return valeur


                    ####################
                    ####################

 
def enregistrer_score (pseudo_joueur, score):
    """Cette fonction a pour but d'enregistrer un nouveau score
        Elle retourne une variable booléenne indiquant si l'utilisateur existe déjà."""

    score_joueur = {pseudo_joueur : score}
    existant = False

    # Nous vérifions si le fichier de scores existe.
    # A défaut, il sera créé.
    if os.path.exists("fichier_de_scores"):

        # Si le fichier de score existe, vérifions que le joueur n'ait pas déjà un compte.
        print("\nLe fichier de score existe.")
        print("Nous vérifions que vous n'ayez pas déjà un compte.\n")

        # Ouverture du fichier en lecture.
        with open("fichier_de_scores", "rb") as fichier :
            mon_depickler = pickle.Unpickler(fichier)
            scores_actuels = mon_depickler.load()
            liste_scores = list(scores_actuels)

            # Recherche du pseudo du joueur.
            for elt in liste_scores :
                if elt.lower() == pseudo_joueur.lower() :
                    existant = True

        # Si le pseudo n'existe pas, nous l'ajoutons avec le score rentré en paramètre.
        if existant == False :
            print("Vous n'avez pas encore de compte.")
            print("Nous enregistrons le score : {0}\n\n".format(score_joueur))
            
            nouveaux_scores = {**scores_actuels, **score_joueur}
        
            with open("fichier_de_scores","wb") as fichier :
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(nouveaux_scores)

        # Si le pseudo existe déjà, nous avertissons l'utilisateur.        
        else :
            print("\nVous avez déjà un compte.\n\n")
            

    # Création du fichier de scores.    
    else:
        print("Le fichier de score n'existe pas encore.\n")
        print("Nous le créons et enregistrons le score : {0}\n".format(score_joueur))
        with open("fichier_de_scores","wb") as fichier :
            print("On enregistre")
            mon_depickler = pickle.Unpickler(fichier)
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(score_joueur)
            
    return existant


                    ####################
                    ####################


def creation_compte():
    """ Cette fonction ne fait qu'appeler d'autres fonctions pour permettre la création d'un compte.
    Si le compte est déjà existant, elle récupère le score enregistré"""
    pseudo = input("\nEntrez votre pseudonyme.\n\n")
    existant = enregistrer_score(pseudo, 0)
    if existant == True :
        score = recuperer_score(pseudo)
    donnees.pseudonyme = pseudo

                    ####################
                    ####################


def regles():
    """ Cette fonction ne fait qu'afficher les règles du jeu"""

    print("\nLE JEU DU PENDU:\n\n")
    print("Les règles sont simples:\n")
    print("\t- Un mot sera choisi automatiquement\n")
    print("\t- Vous aurez autant de chances que de lettres dans ce mot\n")
    print("\t- A chaque fois que vous devinez une lettre, vous pouvez tenter de deviner le mot complet\n")
    print("\t- Votre score sera le nombre de chances qu'il vous restait au moment de votre victoire\n")



def enregistrer_nouveau_score(pseudo, score):
    """Cette fonction a pour but de modifier le score d'un joueur existant
        Elle retourne une variable stipulant si le compte du joueur existe déjà."""
    
    # Nous vérifions si le fichier de scores existe.
    if os.path.exists("fichier_de_scores"):
        print("\n\nLe fichier de score est existant.\n")
        
        with open("fichier_de_scores", "rb") as fichier :
            mon_depickler = pickle.Unpickler(fichier)
            scores_actuels = mon_depickler.load()
            scores_actuels[pseudo] = score
            print(scores_actuels)

        with open("fichier_de_scores","wb") as fichier :
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(scores_actuels)


                    ####################
                    ####################


def suppression_scores():
    """Cette foction supprime l'ensemble des comptes et scores associés et affiche
    le fichier de score vide"""

    if os.path.exists("fichier_de_scores"):
        print("Le fichier de score existe et va être supprimé.\n")
        
        with open("fichier_de_scores","wb") as fichier :
            mon_pickler = pickle.Pickler(fichier)
            vide = {}
            mon_pickler.dump(vide)

        with open("fichier_de_scores", "rb") as fichier :
            mon_depickler = pickle.Unpickler(fichier)
            scores_actuels = mon_depickler.load()
            print("Les scores sont remis à 0 : {0}\n".format(scores_actuels))
   
    else:
        print("Le fichier de score n'existe pas encore.\n")


def is_one_letter() :
    """ Cette fonction prend en paramètre une chaine de caractère et teste si elle
    est uniquement composée d'une seule lettre"""

    lettre = input("Tapez une lettre: ")
    lettre = lettre.lower()
    if len(lettre)>1 or not lettre.isalpha():
        print("Vous n'avez pas saisi une lettre valide.")
        return is_one_letter()
    else:
        return lettre


def is_in_word(lettre_trouvee, mot_complet):

    mot_masque = ""
    for lettre in mot_complet:
        if lettre in lettre_trouvee:
            mot_masque += lettre
        else:
            mot_masque += "*"
    print(mot_masque)
    return mot_masque


def is_word_correct (mot, test):
    """ Cette fonction vérifie si deux chaines de caractères sont identiques.
    En mettant ces chaines en minuscules, on rend cette fonction insensible à la casse. """
    
    correct = False
    if mot.lower() == test.lower() :
        correct = True
        print ("\n\nVous avez bien deviné le mot\n\n")

    return correct
