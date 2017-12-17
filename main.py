# 5th version of the project
# 03/06/2013
# Edited by Sebas

# RULES TO FOLLOW FOR THE PROJECT
"""
    (1) Variables should follow this naming convention: variableName
    (2) Functions should follow this naming convention: function_name
    (3) If possible and if it improves the codebase, refactor a function by adding a parameter
    (4) If possible use booleans, instead of variables of type int with 0 or 1 as a value
    (5) Add spaces: before and after signs and operators (=, +, >=, ==, ...). E.g.: age = 18 instead of age=18
    (6) Write a code that works well (Troll)
"""

from tkinter import *

# Function that is called often (after each click)
def event_function(event):
    global column
    global player
    global winner
    global numberOfMoves
    global discLign
    global discColumn

    playerHasPlayed = False

    if(numberOfMoves < 42 and winner == 0):

            # Calculation of the column by handling the edges
            column = int((event.x) // (430/7))
            if column < 0:
                column = 0
            elif column > 6:
                column = 6
                
            if(add_disc(column) == True):
                numberOfMoves += 1
                playerHasPlayed = True
                winner = global_alignment(4)

                update_info_and_player()
                display()

    if(numberOfMoves < 42 and winner == 0 and isAIMode == True and playerHasPlayed == True): # If possible, we let the computer make its move right after the player's

        alreadyPlayed = False

        # FIRST OF ALL: WIN INSTANTLY IF POSSIBLE
        player = 2
        for column in range(7):
                
                if(alreadyPlayed == False):
                    
                    if(add_disc(column) == True):
                        winner = global_alignment(4)
                        
                        if(winner == 2): # In that case, the computer confirms its move as it makes it win the game
                            numberOfMoves += 1
                            alreadyPlayed = True
                            
                        else: # We have to remove the computer's disc because we noticed it doesn't make it win the game
                            grid[discLign][discColumn] = 0

        # OTHERWISE: THE COMPUTER DEFENDS ITSELF THE BEST WAY IT CAN
        for alignmentToCounter in reversed(range(5)): # reversed because the computer is trying to counter the best alignments first

            for column in range(7):
                
                if(alreadyPlayed == False):
                    
                    player = 1
                    if(add_disc(column) == True):
                        winnerForSuchAnAlignment = global_alignment(alignmentToCounter)
                        
                        if(winnerForSuchAnAlignment == 1): # In that case, the computer has to play here to defend itself
                            player = 2
                            grid[discLign][discColumn] = player
                            numberOfMoves += 1
                            winner = global_alignment(4)
                            alreadyPlayed = True
                            
                        else: # We have to remove the player's disc we put while testing this use-case
                            grid[discLign][discColumn] = 0

        # Updates         
        update_info_and_player()
        display();

# Displays each disc or empty cell
def display():
    for x in range(7):
                for y in range(6):
                        if(grid[y][x] == 0):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = color0)
                        elif(grid[y][x] == 1):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = color1)
                        elif(grid[y][x] == 2):
                            can.create_oval(35+(60*x)-25, 35+(60*y)+25, 35+(60*x)+25, 35+(60*y)-25, fill = color2)
    can.pack(side = 'top', padx = 10, pady = 10)

# Updates the information banner on the bottom of the window
# ALSO UPDATES THE player VALUE
def update_info_and_player():
                global player

                # There is a winner
                if(winner != 0):
                    if(player == 1):
                        label1["fg"] = color1    
                    elif(player == 2):
                        label1["fg"] = color2
                        
                    label1["text"] = 'End of the game: Player {} wins after {} total moves!'.format(player, numberOfMoves)

                # This is a tie
                elif(numberOfMoves >= 42):
                    label1["text"] = 'End of the game: this is a tie!'

                # The game is not over yet  
                else:        
                    if(player == 1):
                        player = 2
                        label1["fg"] = color2
                                    
                    elif(player == 2):
                        player = 1
                        label1["fg"] = color1

                    label1["text"] = 'Player {} has to play its move number {}'.format(player,numberOfMoves // 2 + 1)

                label1.pack(fill = BOTH)

            
# Sets each cell of the grid to value
def initialize_grid(value):         
    for y in range(6):
        for x in range(7):
            grid[y][x] = value

# Returns True if the column is empty, otherwise False
def empty_column(column): 
    booleen = True
    for y in range(6):
        if(grid[y][column] != 0):
            booleen = False
    return booleen

# Returns True if the column is filled, otherwise False
def filled_column(column):
    booleen = True
    for y in range(6):
        if(grid[y][column] == 0):
            booleen = False
    return booleen

# Returns True if the player's disc can be added to the column, otherwise False (i.e. the column is filled)
def add_disc(column):
    # We need the global keyword because we have to WRITE in these variables
    global discColumn
    global discLign
    
    operationIsPossible = not (filled_column(column))
    operationIsDone = False
    if(operationIsPossible == True):
        y=5
        while(y >= 0 and operationIsDone == False):
            if(grid[y][column] == 0):
                grid[y][column] = player
                discLign = y
                discColumn = column
                operationIsDone = True
            else:
                y -= 1
        return True
    else:
        return False

# Returns True if the coordinates belong to the grid, otherwise False
def correct_coordinates(x, y):
    if(0 <= x and x <= 6 and 0 <= y and y <= 5):
        return True
    else:
        return False

# Returns value contained in player variable if the new disc enables an alignment of "requiredAlignment" discs in whatever direction, otherwise 0
def global_alignment(requiredAlignment):
    verticalAlignment = alignment_towards_one_way(0, -1) + 1 + alignment_towards_one_way(0, 1);
    horizontalAlignment = alignment_towards_one_way(-1, 0) + 1 + alignment_towards_one_way(1, 0);
    ascendingDiagonalAlignment = alignment_towards_one_way(-1, 1) + 1 + alignment_towards_one_way(1, -1);
    descendingDiagonalAlignment = alignment_towards_one_way(-1, -1) + 1 + alignment_towards_one_way(1, 1);

    if(horizontalAlignment >= requiredAlignment or verticalAlignment >= requiredAlignment or ascendingDiagonalAlignment >= requiredAlignment or descendingDiagonalAlignment >= requiredAlignment):
        return player
    else:
        return 0


def alignment_towards_one_way(xVector, yVector):
    currentAlignment = 0;
    x = discColumn + xVector
    y = discLign + yVector
    continueInThatDirection = True
    
    while(continueInThatDirection == True and correct_coordinates(x, y) == True):
        if(grid[y][x] == player):
            currentAlignment += 1
            x += xVector
            y += yVector
        else:
            continueInThatDirection = False
    
    return currentAlignment;

def initialization():
    global column
    global player
    global winner
    global numberOfMoves
    global discLign
    global discColumn
    initialize_grid(0)
    column = 0
    player = 2 # 2 because at the beginning, update_info_and_player is going to switch it back to 1
    winner = 0
    numberOfMoves = 0
    discLign = 0
    discColumn = 0
    update_info_and_player()
    display()

def new_game(booleanParam):
    global isAIMode
    
    if(isAIMode != booleanParam): # If the number of players has changed, we have to update both the avatars and isAIMode
        isAIMode=booleanParam
        if(isAIMode==True):
            change_avatar(2, computerImage)
            avatar.entryconfigure(1, state=DISABLED)
        else:
            change_avatar(2, sackboyImage)
            avatar.entryconfigure(1, state=NORMAL)

    initialization()
    
def edit_color(c1, c2, c3, c4):
    global player
    global boardColor
    global color0
    global color1
    global color2

    boardColor = c1
    color0 = c2
    color1 = c3
    color2 = c4
        
    can.configure(bg=boardColor)
    if(player==1):
        player=2
    else:
        player=1
    update_info_and_player()
    display()

def change_avatar(playerNumber, imageFile):
    if(playerNumber==1):
        item = canPhoto.create_image(35, 35, image = imageFile)
    else:
        item = canPhoto.create_image(430-35, 35, image = imageFile)

def display_help():
    messagebox.showinfo("Rules of Connect Four Game", "The goal of Connect Four is to align 4 discs before the other player, whether horizontally, vertically, diagonally!\n\nUse the mouse left-click to play against a human or a computer!")

def display_about():
    messagebox.showinfo("About...", "This game was created by Sébastien BRANLY and Axel VAINDAL as freshmen during 2012-2013 School Year")

# MAIN PROGRAM :
#_______________

""" Default values """
isAIMode = False
boardColor = 'navy'
color0 = 'grey'
color1 = 'red'
color2 = 'yellow'
    
grid = [[0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0]]

window = Tk()

menubar = Menu(window)
new_game_menu= Menu(menubar, tearoff=0)
new_game_menu.add_command(label="New game against the computer (average AI)", command=lambda: new_game(True))
new_game_menu.add_command(label="New game against another player", command=lambda: new_game(False))
new_game_menu.add_separator()
new_game_menu.add_command(label="Quit the game", command=window.destroy)
menubar.add_cascade(label="Games", menu=new_game_menu)

options_menu= Menu(menubar, tearoff=0)
options_menu.add_command(label="Connect Four theme", command=lambda: edit_color('navy', 'grey', 'red', 'yellow'))
options_menu.add_command(label="Checkers theme", command=lambda: edit_color('gold', 'grey', 'black', 'white'))
options_menu.add_separator()

submenu1=Menu(menubar, tearoff=0)
submenu1.add_command(label="Red", command=lambda: edit_color(boardColor, color0, 'red', color2))
submenu1.add_command(label="Blue", command=lambda: edit_color(boardColor, color0, 'blue', color2))
submenu1.add_command(label="Brown", command=lambda: edit_color(boardColor, color0, 'brown', color2))
submenu1.add_command(label="Black", command=lambda: edit_color(boardColor, color0, 'black', color2))
options_menu.add_cascade(label="Player 1's color", menu=submenu1)

submenu2=Menu(menubar, tearoff=0)
submenu2.add_command(label="Yellow", command=lambda: edit_color(boardColor, color0, color1, 'yellow'))
submenu2.add_command(label="Cyan", command=lambda: edit_color(boardColor, color0, color1, 'cyan'))
submenu2.add_command(label="Light green", command=lambda: edit_color(boardColor, color0, color1, 'green'))
submenu2.add_command(label="White", command=lambda: edit_color(boardColor, color0, color1, 'white'))
options_menu.add_cascade(label="Player 2's color", menu=submenu2)

menubar.add_cascade(label="Edit colors", menu=options_menu)

avatar = Menu(menubar, tearoff=0)

submenu_avatar_1=Menu(menubar, tearoff=0)
submenu_avatar_1.add_command(label="Mario", command=lambda: change_avatar(1, marioImage))
submenu_avatar_1.add_command(label="Pikachu", command=lambda: change_avatar(1, pikachuImage))
submenu_avatar_1.add_command(label="Sonic", command=lambda: change_avatar(1, sonicImage))
avatar.add_cascade(label="Player 1's avatar", menu=submenu_avatar_1)

submenu_avatar_2=Menu(menubar, tearoff=0)
submenu_avatar_2.add_command(label="Sackboy", command=lambda: change_avatar(2, sackboyImage))
submenu_avatar_2.add_command(label="Kirby", command=lambda: change_avatar(2, kirbyImage))
submenu_avatar_2.add_command(label="Zelda", command=lambda: change_avatar(2, zeldaImage))
avatar.add_cascade(label="Player 2's avatar", menu=submenu_avatar_2)

menubar.add_cascade(label="Edit avatars", menu=avatar)

help_menu= Menu(menubar, tearoff=0)
help_menu.add_command(label="Rules: how to play", command=display_help)
help_menu.add_command(label="About...", command=display_about)
menubar.add_cascade(label="Help", menu=help_menu)

can = Canvas(window, width = 430, height = 370, bg = boardColor)
canPhoto = Canvas(window, width = 430, height = 70)
label1 = Label(window, fg = color2, bg = 'grey')

computerImage = PhotoImage(file ='computerAvatar.gif')

marioImage = PhotoImage(file ='marioAvatar.gif')
pikachuImage = PhotoImage(file ='pikachuAvatar.gif')
sonicImage = PhotoImage(file ='sonicAvatar.gif')

kirbyImage = PhotoImage(file ='kirbyAvatar.gif')
zeldaImage = PhotoImage(file ='zeldaAvatar.gif')
sackboyImage = PhotoImage(file ='sackboyAvatar.gif')

change_avatar(1, marioImage)
change_avatar(2, sackboyImage)

canPhoto.pack()
can.bind('<Button-1>', event_function) # Waiting for a new click
window.config(menu=menubar, bg='grey')
window.title("Connect Four!")

new_game(False)
window.mainloop()
