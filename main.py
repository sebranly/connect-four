#VERSION 3 du projet
#08/02/2013
#Corrigée par Sébas

#REGLES A REPSECTER POUR LE PROJET
"""
    (1) Nommer les variables comme ça : nomDeVariable
    (2) Nommer les fonctions comme ça : nom_de_fonction
    (3) Factoriser une grosse fonction en lui ajoutant des paramètres (si possible)
    (4) Utiliser les booleens si possible, plutôt que des variables de type int à 0 ou 1
    (5) Espacer les codes : mettre des espaces avant et après les signes (=, +, >=, ==, ...). Exemple : age = 18 plutôt que age=18
    (6) Faire un code qui marche (Troll)
"""

from tkinter import *

#Fonction appelée le plus souvent (à chaque clic)
def fonction_evenement(event):
    global colonne
    global joueur
    global vainqueur
    global nombreDeCoups
    global ligneJeton
    global colonneJeton

    joueurAJoue = False

    if(nombreDeCoups < 42 and vainqueur == 0):

            #Calcul de la colonne avec gestion des bords
            colonne = int((event.x) // (430/7))
            if colonne < 0:
                colonne = 0
            elif colonne > 6:
                colonne = 6
                
            if(ajouter_jeton(colonne) == True):
                nombreDeCoups += 1
                joueurAJoue = True
                vainqueur = alignement_global(4)

                changer_informations_et_joueur()
                affichage()

    if(nombreDeCoups < 42 and vainqueur == 0 and modeAvecIA == True and joueurAJoue == True): #On fait jouer l'ordinateur si possible tout de suite après le joueur 1

        dejaJoue = False

        #PREMIERE TECHNIQUE : GAGNER INSTANTANEMENT
        joueur = 2
        for colonne in range(7):
                
                if(dejaJoue == False):
                    
                    if(ajouter_jeton(colonne) == True):
                        vainqueur = alignement_global(4)
                        
                        if(vainqueur == 2): #Dans ce cas l'ordi laisse son coup gagnant en place !
                            nombreDeCoups += 1
                            dejaJoue = True
                            
                        else: #On doit enlever le jeton de l'ordi car il ne permet pas de gagner !
                            grille[ligneJeton][colonneJeton] = 0

        #DEUXIEME TECHNIQUE : DEFENSIVE
        for alignementAContrer in reversed(range(5)): #reversed car l'ordinateur cherche à contrer les meilleurs alignements d'abord !

            for colonne in range(7):
                
                if(dejaJoue == False):
                    
                    joueur = 1
                    if(ajouter_jeton(colonne) == True):
                        vainqueurPourUnTelAlignement = alignement_global(alignementAContrer)
                        
                        if(vainqueurPourUnTelAlignement == 1): #Dans ce cas l'ordi doit jouer ici pour se défendre !
                            joueur = 2
                            grille[ligneJeton][colonneJeton] = joueur
                            nombreDeCoups += 1
                            vainqueur = alignement_global(4)
                            dejaJoue = True
                            
                        else: #On doit enlever le jeton du joueur 1 que l'on a mis en phase de supposition
                            grille[ligneJeton][colonneJeton] = 0

        #Mises à jour         
        changer_informations_et_joueur()
        affichage();

#Affiche chaque pion ou case vide
def affichage():
    for x in range(7):
                for y in range(6):
                        if(grille[y][x] == 0):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = couleur0)
                        elif(grille[y][x] == 1):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = couleur1)
                        elif(grille[y][x] == 2):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = couleur2)
    can.pack(side = 'top', padx = 10, pady = 10)

#Met à jour la bannière d'informations en bas de l'écran
#MET EGALEMENT A JOUR LA VALEUR joueur
def changer_informations_et_joueur():
                global joueur

                #Il y a un vainqueur
                if(vainqueur != 0):
                    if(joueur == 1):
                        label1["fg"] = couleur1    
                    elif(joueur == 2):
                        label1["fg"] = couleur2
                        
                    label1["text"] = 'FIN DE LA PARTIE : Le joueur', joueur, 'a gagné en', nombreDeCoups, 'coups au total !'

                #Match nul
                elif(nombreDeCoups >= 42):
                    label1["text"] = 'FIN DE LA PARTIE : Match nul !'

                #La partie continue  
                else:        
                    if(joueur == 1):
                        joueur = 2
                        label1["fg"] = couleur2
                                    
                    elif(joueur == 2):
                        joueur = 1
                        label1["fg"] = couleur1

                    label1["text"] = 'Au joueur', joueur, 'de jouer son coup n°', nombreDeCoups // 2 + 1

                label1.pack(fill = BOTH)

            
#Affecte valeur à chaque case de la grille
def initialiser_grille(valeur):         
    for y in range(6):
        for x in range(7):
            grille[y][x] = valeur

#Renvoie True si la colonne est vide, False sinon
def colonne_vide(colonne): 
    booleen = True
    for y in range(6):
        if(grille[y][colonne] != 0):
            booleen = False
    return booleen

#Renvoie True si la colonne est remplie, False sinon
def colonne_remplie(colonne):
    booleen = True
    for y in range(6):
        if(grille[y][colonne] == 0):
            booleen = False
    return booleen

#Renvoie True si le jeton du joueur peut être ajouté à la colonne, False sinon (colonne déjà remplie)
def ajouter_jeton(colonne):
    #Besoin de global car on doit ECRIRE dans les variables globales
    global colonneJeton
    global ligneJeton
    
    operationPossible = not (colonne_remplie(colonne))
    operationEffectuee = False
    if(operationPossible == True):
        y=5
        while(y >= 0 and operationEffectuee == False):
            if(grille[y][colonne] == 0):
                grille[y][colonne] = joueur
                ligneJeton = y
                colonneJeton = colonne
                operationEffectuee = True
            else:
                y -= 1
        return True
    else:
        return False

#Renvoie True si les coordonnées sont dans la grille, False sinon
def coordonnees_correctes(x, y):
    if(0 <= x and x <= 6 and 0 <= y and y <= 5):
        return True
    else:
        return False

#Renvoie la valeur "joueur" si le nouveau jeton permet un alignement de "alignementRequis" jetons dans n'importe quelle direction, sinon 0
def alignement_global(alignementRequis):
    alignementVertical = alignement_dans_un_sens(0, -1) + 1 + alignement_dans_un_sens(0, 1);
    alignementHorizontal = alignement_dans_un_sens(-1, 0) + 1 + alignement_dans_un_sens(1, 0);
    alignementDiagonaleMontante = alignement_dans_un_sens(-1, 1) + 1 + alignement_dans_un_sens(1, -1);
    alignementDiagonaleDescendante = alignement_dans_un_sens(-1, -1) + 1 + alignement_dans_un_sens(1, 1);

    if(alignementHorizontal >= alignementRequis or alignementVertical >= alignementRequis or alignementDiagonaleMontante >= alignementRequis or alignementDiagonaleDescendante >= alignementRequis):
        return joueur
    else:
        return 0


def alignement_dans_un_sens(mouvementX, mouvementY):
    alignementEnCours = 0;
    x = colonneJeton + mouvementX
    y = ligneJeton + mouvementY
    poursuivreDansCetteDirection = True
    
    while(poursuivreDansCetteDirection == True and coordonnees_correctes(x, y) == True):
        if(grille[y][x] == joueur):
            alignementEnCours += 1
            x += mouvementX
            y += mouvementY
        else:
            poursuivreDansCetteDirection = False
    
    return alignementEnCours;

#PROGRAMME PRINCIPAL :
#_____________________

#Les variables suivantes devront être intéractives dans le menu (en inrégrant des valeurs classiques par défaut)
"""modeAvecIA = True
couleurPlateau = 'white'
couleur0 = 'black'
couleur1 = 'yellow'
couleur2 = 'red'"""

""" Valeurs par défaut """
modeAvecIA = False
couleurPlateau = 'white'
couleur0 = 'grey'
couleur1 = 'blue'
couleur2 = 'green'
    
grille = [[0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0]]

initialiser_grille(0)
colonne = 0
joueur = 2 #2 car dès le début, la fonction changer_informations_et_joueur va la mettre à 1
vainqueur = 0
nombreDeCoups = 0
ligneJeton = 0
colonneJeton = 0

fenetre = Tk()
can = Canvas(fenetre, width = 430, height = 370, bg = couleurPlateau)
label1 = Label(fenetre, fg = couleur2, bg = 'black')

joueur = 2
changer_informations_et_joueur()
affichage()

can.bind('<Button-1>', fonction_evenement) #On attend le clic
fenetre.mainloop()
