# Imports nécessaires au programme
import pickle
import donnees
from fonctions import *
import random


# Variables nécessaires au programme
saisie = True       # Permet de s'assurer que la saisie de la lettre est correcte.
score = 0 # Récupère code du joueur depuis le fichier de scores.
fin = False # Permet de quitter le jeu.
choix = "0" # Permet de choisir une option.


def jouer():
    # Variables nécessaires à la fonction
    mot = donnees.mots[random.randrange(1,5)] # Mot sélectionné aléatoirement dans un dictionnaire de mot du fichier donnees.
    nb_chances = 0 # Détermine le nombre de chances. Autant de chances que de lettres dans le mot.
    correct = False # Permet de déterminer si le mot est entièrement deviné.
    
    # Création du nombre de chances possibles.
    i = 0 # Incrément.
    while i < len(mot):
        nb_chances
        nb_chances +=1
        i += 1

    # Création du mot à compléter par les lettres devinées.
    p = 1 # Incrément.
    mot_converti = ["*"]
    while p < len(mot):
        mot_converti.append("*")
        p += 1
    
    # Boucle du jeu :
    # - Ici, le joueur joue tant qu'il lui reste des chances (limitées par le nombre de lettres du mot).
    # - Mais également tant qu'il n'a pas deviné le mot.
    #   (Le joueur peut donc deviner et saisir le mot avant d'avoir deviné toutes les lettres)
    while nb_chances > 0 and correct == False :

            print ("\n\nVous avez {0} chances.".format(nb_chances))
            # On demande à l'utilisateur de saisir une lettre puis l'on test la lettre via is_one_letter().
            lettre = is_one_letter()

            # Si la saisie est correcte, on retire une chance à l'utilisateur.
            # Puis, on cherche si la lettre appartient au mot à deviner via is_in_word().
            nb_chances -= 1
            mot_masque = is_in_word(lettre, mot)
            # On regarde si le nouveau mot (constitué des lettres devinées) est identique au mot à deviner.
            correct = is_word_correct (mot, mot_masque)

            # Si c'est le cas, il n'est pas nécessaire de demander à l'utilsateur de le saisir. Le jeu est terminé.
            if correct == True :
                continue

            # Si le mot n'est pas encore deviné, l'utilisateur peut tenter de le deviner.
            test = input("\n\nTentez de deviner le mot\n\n")
            correct = is_word_correct(mot, test)
                
            
    if correct == True :
        print("\n\nBravo ! Vous avez deviné le mot\n\n")
        print("\n\nVous aviez encore {0} chances.\n\nVotre score est donc de {0} ! :)".format(nb_chances))
        enregistrer_nouveau_score(donnees.pseudonyme, nb_chances)
        
    else :
        print("\n\nDésolé, réessayez !\n\n")


def quitter():
    global fin
    fin = True



def switch(choix):
    switcher = {
        "1": regles,
        "2": afficher_scores,
        "3": creation_compte,
        "4": suppression_scores,
        "5": jouer,
        "6": quitter,
    }
    function = switcher.get(choix, lambda: "Choix invalide.\n")
    function() # Appelle de la fonction choisie

while fin != True :   
    # Création et affichage du menu d'acceuil.
    print ("Bonjour et bienvenue dans le jeu de pendu !\n\n")
    print ("Tapez 1 :\t Pour consultez les règles du jeu.\n")
    print ("Tapez 2 :\t Pour consultez les comptes et les scores existants.\n")
    print ("Tapez 3 :\t Pour créer ou identifier votre compte.\n")
    print ("Tapez 4 :\t Pour supprimer la totalité des comptes.\n")
    print ("Tapez 5 :\t Pour jouer.\n")
    print ("Tapez 6 :\t Pour quitter.\n")
    choix = input("")

    switch(choix)
