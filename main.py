from tkinter import *

def fonction_evenement(event):
    global colonne
    global joueur
    global vainqueur
    global nombreDeCoups
    global ligneJeton
    global colonneJeton

    if(mode==1 or (mode==2 and joueur==1)): #A l'un des deux joueurs de jouer contre l'autre OU au joueur 1 de jouer contre l'IA
        if(nombreDeCoups<42 and vainqueur==0):
            colonne=(event.x)//60
            
            if(colonne>=6):
                colonne=6
                
            if(ajouter_jeton(colonne, joueur)==1):
                nombreDeCoups+=1
                vainqueur=alignement(joueur, 4)

                if(nombreDeCoups>=42 or vainqueur!=0):
                    label1["text"]='VAINQUEUR : joueur', joueur
                    label1.pack(fill=BOTH)
                    if(joueur==1):
                        label1["fg"]='red'    
                    elif(joueur==2):
                        label1["fg"]='yellow'
                else:        
                    if(joueur==1):
                        joueur=2
                        label1["fg"]='yellow'
                                    
                    elif(joueur==2):
                        joueur=1
                        label1["fg"]='red'

                    label1["text"]='Au joueur', joueur
                    label1.pack(fill=BOTH)

                for x in range(7):
                    for y in range(6):
                        if(grille[y][x]==0):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='grey')
                        elif(grille[y][x]==1):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='red')
                        elif(grille[y][x]==2):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='yellow')
                can.pack(side='top', padx=10, pady=10)
                
    else: #A l'IA de jouer
        dejaJoue=0
        for colonne in range(7):
            if(dejaJoue==0):
                if(ajouter_jeton(colonne, 1)==1):
                    vainqueur=alignement(1, 4)
                    if(vainqueur==1): #Dans ce cas l'ordi doit jouer ici pour se défendre !
                        grille[ligneJeton][colonneJeton]=2
                        nombreDeCoups+=1
                        vainqueur=alignement(joueur, 4)
                        dejaJoue=1
                    else:
                        grille[ligneJeton][colonneJeton]=0
                    
        if(dejaJoue==0):
            for colonne in range(7):
                if(dejaJoue==0):
                    if(ajouter_jeton(colonne, 2)==1):
                        nombreDeCoups+=1
                        vainqueur=alignement(2, 4)
                        dejaJoue=1

        if(nombreDeCoups>=42 or vainqueur!=0):
                    label1["text"]='VAINQUEUR : joueur', joueur
                    label1.pack(fill=BOTH)
                    if(joueur==1):
                        label1["fg"]='red'    
                    elif(joueur==2):
                        label1["fg"]='yellow'
        else:        
                    if(joueur==1):
                        joueur=2
                        label1["fg"]='yellow'
                                    
                    elif(joueur==2):
                        joueur=1
                        label1["fg"]='red'

                    label1["text"]='Au joueur', joueur
                    label1.pack(fill=BOTH)

        for x in range(7):
                for y in range(6):
                    if(grille[y][x]==0):
                        can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='grey')
                    elif(grille[y][x]==1):
                        can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='red')
                    elif(grille[y][x]==2):
                        can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='yellow')
                can.pack(side='top', padx=10, pady=10)       
            
                    
        

"""Commentaire pour la fonction d'affichage TEXTE

#Fonction d'affichage sans return
def afficher_grille():
    for y in range(6):
        print("")
        for x in range(7):
            print("[", grille[y][x], "]", end='')
    print("\n\n")
"""

#Affecte valeur à chaque case de la grille sans return
def initialiser_grille(valeur):         
    for y in range(6):
        for x in range(7):
            grille[y][x]=valeur

#Renvoie 1 si la colonne est vide, 0 sinon
def colonne_vide(colonne): 
    oui=1
    for y in range(6):
        if(grille[y][colonne]!=0):
            oui=0
    return oui

#Renvoie 1 si la colonne est remplie, 0 sinon
def colonne_remplie(colonne):
    oui=1
    for y in range(6):
        if(grille[y][colonne]==0):
            oui=0
    return oui

#Renvoie 1 si le jeton du joueur peut être ajouté à la colonne, 0 sinon (colonne déjà remplie)
def ajouter_jeton(colonne, joueur):
    #Besoin de global car on doit ECRIRE dans les variables globales
    global colonneJeton
    global ligneJeton
    
    operationPossible = not (colonne_remplie(colonne))
    operationEffectuee=0
    if(operationPossible==1):
        y=5
        while(y>=0 and operationEffectuee==0):
            if(grille[y][colonne]==0):
                grille[y][colonne]=joueur
                ligneJeton=y
                colonneJeton=colonne
                operationEffectuee=1
            else:
                y-=1
        return 1
    else:
        return 0

#Renvoie 1 si les coordonnées sont dans la grille, 0 sinon
def coordonnees_correctes(x, y):
    if(0<=x and x<=6 and 0<=y and y<=5):
        return 1
    else:
        return 0

#Renvoie 1 si le nouveau jeton permet un alignement de "alignementRequis" jetons dans n'importe quelle direction, sinon 0
def alignement(joueur, alignementRequis):
    #1 car le jeton venant d'être posé est "aligné avec lui-même"
    alignementVertical=1
    alignementHorizontal=1
    alignementDiagonaleMontante=1
    alignementDiagonaleDescendante=1

    #Alignement horizontal
        #droite
    x=colonneJeton+1
    y=ligneJeton
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementHorizontal+=1
            x+=1
        else:
            poursuivreDansCetteDirection=0
        #gauche
    x=colonneJeton-1
    y=ligneJeton
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementHorizontal+=1
            x-=1
        else:
            poursuivreDansCetteDirection=0


    #Alignement vertical
        #haut
    x=colonneJeton
    y=ligneJeton-1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementVertical+=1
            y-=1
        else:
            poursuivreDansCetteDirection=0
        #bas
    x=colonneJeton
    y=ligneJeton+1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementVertical+=1
            y+=1
        else:
            poursuivreDansCetteDirection=0

    #Alignement diagonale montante
        #en haut à droite
    x=colonneJeton+1
    y=ligneJeton-1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementDiagonaleMontante+=1
            x+=1
            y-=1
        else:
            poursuivreDansCetteDirection=0
        #en bas à gauche
    x=colonneJeton-1
    y=ligneJeton+1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementDiagonaleMontante+=1
            x-=1
            y+=1
        else:
            poursuivreDansCetteDirection=0

    #Alignement diagonale descendante
        #en bas à droite
    x=colonneJeton+1
    y=ligneJeton+1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementDiagonaleDescendante+=1
            x+=1
            y+=1
        else:
            poursuivreDansCetteDirection=0
        #en haut à gauche
    x=colonneJeton-1
    y=ligneJeton-1
    poursuivreDansCetteDirection=1
    while(poursuivreDansCetteDirection==1 and coordonnees_correctes(x, y)==1):
        if(grille[y][x]==joueur):
            alignementDiagonaleDescendante+=1
            x-=1
            y-=1
        else:
            poursuivreDansCetteDirection=0


    if(alignementHorizontal>=alignementRequis or alignementVertical>=alignementRequis or alignementDiagonaleMontante>=alignementRequis or alignementDiagonaleDescendante>=alignementRequis):
        return joueur
    else:
        return 0

#PROGRAMME PRINCIPAL :
#_____________________

mode=1 #1 pour mode 2 joueurs, 2 pour mode contre IA
    
grille=[[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]]

initialiser_grille(0)
colonne=0
joueur=1
vainqueur=0
nombreDeCoups=0
ligneJeton=0
colonneJeton=0

fenetre=Tk()
can=Canvas(fenetre, width=430, height=370, bg='navy')
label1=Label(fenetre, fg='yellow', bg='black')

for x in range(7):
    for y in range(6):
        if(grille[y][x]==0):
            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='grey')
        elif(grille[y][x]==1):
            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='red')
        elif(grille[x][y]==2):
            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill='yellow')
can.pack(side='top', padx=10, pady=10)

#while (nombreDeCoups<42 and vainqueur==0): #A CORRIGER BIENTOT !!!

can.bind('<Button-1>', fonction_evenement) #On attend le clic
fenetre.mainloop()
