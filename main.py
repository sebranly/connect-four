#VERSION 5 du projet
#06/03/2013
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
                        
                    label1["text"] = 'FIN DE LA PARTIE : Le joueur {} a gagné en {} coups au total !'.format(joueur, nombreDeCoups)

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

                    label1["text"] = 'Au joueur {} de jouer son coup n° {}'.format(joueur,nombreDeCoups // 2 + 1)

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

def initialisation():
    global colonne
    global joueur
    global vainqueur
    global nombreDeCoups
    global ligneJetons
    global colonneJeton
    initialiser_grille(0)
    colonne = 0
    joueur = 2 #2 car dès le début, la fonction changer_informations_et_joueur va la mettre à 1
    vainqueur = 0
    nombreDeCoups = 0
    ligneJeton = 0
    colonneJeton = 0
    changer_informations_et_joueur()
    affichage()

def nouveau_jeu(parametreBool):
    global modeAvecIA
    
    if(modeAvecIA != parametreBool): #Si le nombre de joueurs a changé, il faut mettre à jour les avatars ET modeAvecIA
        modeAvecIA=parametreBool
        if(modeAvecIA==True):
            changer_avatar(2, photoOrdinateur)
            avatar.entryconfigure(1, state=DISABLED)
        else:
            changer_avatar(2, photoSackboy)
            avatar.entryconfigure(1, state=NORMAL)

    initialisation()
    
def modif_couleur(c1, c2, c3, c4):
    global joueur
    global couleurPlateau
    global couleur0
    global couleur1
    global couleur2

    couleurPlateau = c1
    couleur0 = c2
    couleur1 = c3
    couleur2 = c4
        
    can.configure(bg=couleurPlateau)
    if(joueur==1):
        joueur=2
    else:
        joueur=1
    changer_informations_et_joueur()
    affichage()

def changer_avatar(numeroJoueur, fichierImage):
    if(numeroJoueur==1):
        item = canPhoto.create_image(35, 35, image = fichierImage)
    else:
        item = canPhoto.create_image(430-35, 35, image = fichierImage)

def afficher_aide():
    messagebox.showinfo("Principe du jeu Puissance 4", "Le but du Puissance 4 consiste à aligner 4 pions pour gagner avant l'adversaire, que ce soit horizontalement, verticalement, ou en diagonale !\n\nTout se joue avec le clic gauche de la souris, et vous pouvez jouer à 2 ou bien seul contre une IA !")

def afficher_apropos():
    messagebox.showinfo("A propos...", "Jeu réalisé par Sébastien BRANLY et Axel VAINDAL en L1-C1 dans le cadre du Projet MPI de l'année scolaire 2012-2013")

#PROGRAMME PRINCIPAL :
#_____________________

""" Valeurs par défaut """
modeAvecIA = False
couleurPlateau = 'navy'
couleur0 = 'grey'
couleur1 = 'red'
couleur2 = 'yellow'
    
grille = [[0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0]]

fenetre = Tk()

menubar = Menu(fenetre)
nouvelle_partie= Menu(menubar, tearoff=0)
nouvelle_partie.add_command(label="Nouvelle partie à 1 joueur (IA moyenne)", command=lambda: nouveau_jeu(True))
nouvelle_partie.add_command(label="Nouvelle partie à 2 joueurs", command=lambda: nouveau_jeu(False))
nouvelle_partie.add_separator()
nouvelle_partie.add_command(label="Quitter le jeu", command=fenetre.destroy)
menubar.add_cascade(label="Parties", menu=nouvelle_partie)

options= Menu(menubar, tearoff=0)
options.add_command(label="Thème du Puissance 4", command=lambda: modif_couleur('navy', 'grey', 'red', 'yellow'))
options.add_command(label="Thème Jeux de dames", command=lambda: modif_couleur('gold', 'grey', 'black', 'white'))
options.add_separator()

sous_menu1=Menu(menubar, tearoff=0)
sous_menu1.add_command(label="Rouge", command=lambda: modif_couleur(couleurPlateau, couleur0, 'red', couleur2))
sous_menu1.add_command(label="Bleu", command=lambda: modif_couleur(couleurPlateau, couleur0, 'blue', couleur2))
sous_menu1.add_command(label="Marron", command=lambda: modif_couleur(couleurPlateau, couleur0, 'brown', couleur2))
sous_menu1.add_command(label="Noir", command=lambda: modif_couleur(couleurPlateau, couleur0, 'black', couleur2))
options.add_cascade(label="Couleur du joueur 1", menu=sous_menu1)

sous_menu2=Menu(menubar, tearoff=0)
sous_menu2.add_command(label="Jaune", command=lambda: modif_couleur(couleurPlateau, couleur0, couleur1, 'yellow'))
sous_menu2.add_command(label="Cyan", command=lambda: modif_couleur(couleurPlateau, couleur0, couleur1, 'cyan'))
sous_menu2.add_command(label="Vert clair", command=lambda: modif_couleur(couleurPlateau, couleur0, couleur1, 'green'))
sous_menu2.add_command(label="Blanc", command=lambda: modif_couleur(couleurPlateau, couleur0, couleur1, 'white'))
options.add_cascade(label="Couleur du joueur 2", menu=sous_menu2)

menubar.add_cascade(label="Modifier les couleurs", menu=options)

avatar = Menu(menubar, tearoff=0)

sous_menuAvatar1=Menu(menubar, tearoff=0)
sous_menuAvatar1.add_command(label="Mario", command=lambda: changer_avatar(1, photoMario))
sous_menuAvatar1.add_command(label="Pikachu", command=lambda: changer_avatar(1, photoPikachu))
sous_menuAvatar1.add_command(label="Sonic", command=lambda: changer_avatar(1, photoSonic))
avatar.add_cascade(label="Avatar du joueur 1", menu=sous_menuAvatar1)

sous_menuAvatar2=Menu(menubar, tearoff=0)
sous_menuAvatar2.add_command(label="Sackboy", command=lambda: changer_avatar(2, photoSackboy))
sous_menuAvatar2.add_command(label="Kirby", command=lambda: changer_avatar(2, photoKirby))
sous_menuAvatar2.add_command(label="Zelda", command=lambda: changer_avatar(2, photoZelda))
avatar.add_cascade(label="Avatar du joueur 2", menu=sous_menuAvatar2)

menubar.add_cascade(label="Modifier les avatars", menu=avatar)

aide= Menu(menubar, tearoff=0)
aide.add_command(label="Principe du jeu", command=afficher_aide)
aide.add_command(label="A propos...", command=afficher_apropos)
menubar.add_cascade(label="Aide", menu=aide)

can = Canvas(fenetre, width = 430, height = 370, bg = couleurPlateau)
canPhoto = Canvas(fenetre, width = 430, height = 70)
label1 = Label(fenetre, fg = couleur2, bg = 'grey')

photoOrdinateur = PhotoImage(file ='avatarOrdinateur.gif')

photoMario = PhotoImage(file ='avatarMario.gif')
photoPikachu = PhotoImage(file ='avatarPikachu.gif')
photoSonic = PhotoImage(file ='avatarSonic.gif')

photoKirby = PhotoImage(file ='avatarKirby.gif')
photoZelda = PhotoImage(file ='avatarZelda.gif')
photoSackboy = PhotoImage(file ='avatarSackboy.gif')

changer_avatar(1, photoMario)
changer_avatar(2, photoSackboy)

canPhoto.pack()
can.bind('<Button-1>', fonction_evenement) #On attend le clic
fenetre.config(menu=menubar, bg='grey')
fenetre.title("Puissance 4 de Sebas et Axel !")

nouveau_jeu(False)
fenetre.mainloop()
