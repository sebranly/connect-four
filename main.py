# RULES TO FOLLOW
"""
    (1) Variables should follow this naming convention: variableName
    (2) Functions should follow this naming convention: function_name
    (3) If possible and if it improves the codebase, refactor a function by adding a parameter
    (4) If possible use booleans, instead of variables of type int with 0 or 1 as a value
    (5) Add spaces: before and after signs and operators (=, +, >=, ==, ...). E.g.: age = 18 instead of age=18
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

    if(numberOfMoves < gridNumberOfCells and winner == 0):
            # Determination of the column by handling the edges
            column = int((event.x) // (boardWidth / gridWidth))
            if column < 0:
                column = 0
            elif column > gridWidth - 1:
                column = gridWidth - 1
                
            if(could_add_disc(column)):
                numberOfMoves += 1
                playerHasPlayed = True
                winner = global_alignment(required_discs_aligment)
                update_info_and_player()
                display()

	# If possible, we let the computer make its move right after the player's
    if(numberOfMoves < gridNumberOfCells and winner == 0 and isAIMode and playerHasPlayed):
        alreadyPlayed = False

        # FIRST OF ALL: WIN INSTANTLY IF POSSIBLE
        player = 2
        for column in range(gridWidth):
                if(not alreadyPlayed):
                    if(could_add_disc(column)):
                        winner = global_alignment(required_discs_aligment)
                        
						# In that case, the computer confirms its move as it makes it win the game
                        if(winner == 2):
                            numberOfMoves += 1
                            alreadyPlayed = True
						# We have to remove the computer's disc because we noticed it doesn't make it win the game
                        else:
                            grid[discLign][discColumn] = 0

        # OTHERWISE: THE COMPUTER DEFENDS ITSELF THE BEST WAY IT CAN
		# reversed keyword as the computer is trying to counter the best alignments first
        for alignmentToCounter in reversed(range(required_discs_aligment + 1)):
            for column in range(gridWidth):
                if(not alreadyPlayed):
                    player = 1
                    if(could_add_disc(column)):
                        winnerForSuchAnAlignment = global_alignment(alignmentToCounter)
						# In that case, the computer has to play here to defend itself
                        if(winnerForSuchAnAlignment == 1):
                            player = 2
                            grid[discLign][discColumn] = player
                            numberOfMoves += 1
                            winner = global_alignment(required_discs_aligment)
                            alreadyPlayed = True
                        # We have to remove the player's disc we put while testing this use-case
                        else:
                            grid[discLign][discColumn] = 0

        # Updates         
        update_info_and_player()
        display();

# Displays each disc or empty cell
def display():
    for x in range(gridWidth):
                for y in range(gridHeight):
                        if(grid[y][x] >= 0 and grid[y][x] <= 2):
                            x1 = discOffset + (discSize * x) - complementaryDiscOffset
                            x2 = discOffset + (discSize * x) + complementaryDiscOffset
                            y1 = discOffset + (discSize * y) + complementaryDiscOffset
                            y2 = discOffset + (discSize * y) - complementaryDiscOffset
                            can.create_oval(x1, y1, x2, y2, fill = colors[grid[y][x]])
    can.pack(side = 'top', padx = padX, pady = padY)

# Updates the information banner displayed at the top of the grid
# ALSO UPDATES THE player VARIABLE
def update_info_and_player():
                global player

                # There is a winner
                if(winner != 0):
                    if(player >= 1 and player <= 2):
                        label1["fg"] = colors[player]
                    label1["text"] = 'End of the game: Player {} wins after {} total moves!'.format(player, numberOfMoves)
                # This is a tie
                elif(numberOfMoves >= gridNumberOfCells):
                    label1["text"] = 'End of the game: this is a tie!'
                # The game is not over yet  
                else:        
                    if(player == 1):
                        player = 2
                        label1["fg"] = colors[player]            
                    elif(player == 2):
                        player = 1
                        label1["fg"] = colors[player]
                    label1["text"] = 'Player {} has to play its move number {}'.format(player, numberOfMoves // 2 + 1)
                label1.pack(fill = BOTH)

            
# Sets each cell of the grid to value
def initialize_grid(value): 
    for x in range(gridWidth):
        for y in range(gridHeight):
            grid[y][x] = value

# Returns True if the column is empty, otherwise False
def column_is_empty(column):
    for y in range(gridHeight):
        if(grid[y][column] != 0):
            return False
    return True

# Returns True if the column is full, otherwise False
def column_is_full(column):
    for y in range(gridHeight):
        if(grid[y][column] == 0):
            return False
    return True

# Returns True if the player's disc can be added to the column, otherwise False (i.e. the column is full)
def could_add_disc(column):
    # We need the global keyword because we have to WRITE in these variables
    global discColumn
    global discLign
    
    operationIsPossible = not column_is_full(column)
    discHasBeenAdded = False
    if(operationIsPossible):
        y = gridHeight - 1
        while(y >= 0 and not discHasBeenAdded):
            if(grid[y][column] == 0):
                grid[y][column] = player
                discLign = y
                discColumn = column
                discHasBeenAdded = True
            else:
                y -= 1
        return True
    return False

# Returns True if the coordinates belong to the grid, otherwise False
def coordinates_are_correct(x, y):
    return (x >= 0 and x <= (gridWidth - 1) and y >= 0 and y <= (gridHeight - 1))

# Returns the value contained in player variable (i.e. either 1 or 2) if the new disc enables an alignment of "requiredAlignment" discs in whatever direction, otherwise 0
def global_alignment(requiredAlignment):
    verticalAlignment = alignment_towards_one_way(0, -1) + 1 + alignment_towards_one_way(0, 1);
    horizontalAlignment = alignment_towards_one_way(-1, 0) + 1 + alignment_towards_one_way(1, 0);
    ascendingDiagonalAlignment = alignment_towards_one_way(-1, 1) + 1 + alignment_towards_one_way(1, -1);
    descendingDiagonalAlignment = alignment_towards_one_way(-1, -1) + 1 + alignment_towards_one_way(1, 1);

    if(horizontalAlignment >= requiredAlignment or verticalAlignment >= requiredAlignment or ascendingDiagonalAlignment >= requiredAlignment or descendingDiagonalAlignment >= requiredAlignment):
        return player
    return 0


def alignment_towards_one_way(xVector, yVector):
    currentAlignment = 0;
    x = discColumn + xVector
    y = discLign + yVector
    continueInThatDirection = True
    
    while(continueInThatDirection and coordinates_are_correct(x, y)):
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
	# 2 because at the beginning, update_info_and_player is going to switch it back to 1
    player = 2
    winner = 0
    numberOfMoves = 0
    discLign = 0
    discColumn = 0
    update_info_and_player()
    display()

def new_game(playAgainstAI):
    global isAIMode
    
	# If the number of players has changed (because of the mode), we have to update both the avatars and isAIMode variable
    if(isAIMode != playAgainstAI):
        isAIMode = playAgainstAI
        if(isAIMode):
            change_avatar(2, computerImage)
            avatar.entryconfigure(1, state = DISABLED)
        else:
            change_avatar(2, zeldaImage)
            avatar.entryconfigure(1, state = NORMAL)
    initialization()
    
def edit_color(c1, c2, c3, c4):
    global player
    global boardColor
    global colors

    boardColor = c1
    colors[0] = c2
    colors[1] = c3
    colors[2] = c4
        
    can.configure(bg = boardColor)
    if(player == 1):
        player = 2
    else:
        player = 1
    update_info_and_player()
    display()

def edit_size(newDiscSize):
    global discSize
    global boardWidth
    global boardHeight
    global discOffset
    global complementaryDiscOffset

    discSize = newDiscSize
    boardWidth = gridWidth * discSize + padX
    boardHeight = gridHeight * discSize + padY
    discOffset = discSize // 2 + padX // 2
    complementaryDiscOffset = discSize - discOffset
    display()

def change_avatar(playerNumber, imageFile):
    if(playerNumber == 1):
        item = canPhoto.create_image(imagesOffset, imagesOffset, image = imageFile)
    else:
        item = canPhoto.create_image(boardWidth - imagesOffset, imagesOffset, image = imageFile)

def display_help():
    messagebox.showinfo("Rules of Connect Four Game", "The goal of Connect Four is to align 4 discs before the other player, whether horizontally, vertically, diagonally!\n\nUse the mouse left-click to play against a human or a computer!")

def display_about():
    messagebox.showinfo("About...", "This game was created by Sébastien BRANLY and Axel VAINDAL as freshmen during 2012-2013 School Year")

# MAIN PROGRAM :
#_______________

""" Default values """
isAIMode = False
boardColor = 'navy'
colors = ['grey', 'red', 'yellow']
    
grid = [[0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0]]
gridWidth = len(grid[0])
gridHeight = len(grid)
gridNumberOfCells = gridWidth * gridHeight
padX = 10
padY = 10
discSize = 90
boardWidth = gridWidth * discSize + padX
boardHeight = gridHeight * discSize + padY
imagesOffset = 35
discOffset = discSize // 2 + padX // 2
complementaryDiscOffset = discSize - discOffset

required_discs_aligment = 4

window = Tk()

menubar = Menu(window)
new_game_menu = Menu(menubar, tearoff = 0)
new_game_menu.add_command(label = "New game against the computer (average AI)", command = lambda: new_game(True))
new_game_menu.add_command(label = "New game against another player", command = lambda: new_game(False))
new_game_menu.add_separator()
new_game_menu.add_command(label = "Quit the game", command = window.destroy)
menubar.add_cascade(label = "Games", menu = new_game_menu)

options_menu = Menu(menubar, tearoff = 0)
options_menu.add_command(label = "Connect Four theme", command = lambda: edit_color('navy', 'grey', 'red', 'yellow'))
options_menu.add_command(label = "Checkers theme", command = lambda: edit_color('gold', 'grey', 'black', 'white'))
options_menu.add_separator()

submenu1 = Menu(menubar, tearoff = 0)
submenu1.add_command(label="Red", command = lambda: edit_color(boardColor, colors[0], 'red', colors[2]))
submenu1.add_command(label="Blue", command = lambda: edit_color(boardColor, colors[0], 'blue', colors[2]))
submenu1.add_command(label="Brown", command = lambda: edit_color(boardColor, colors[0], 'brown', colors[2]))
submenu1.add_command(label="Black", command = lambda: edit_color(boardColor, colors[0], 'black', colors[2]))
options_menu.add_cascade(label="Player 1's color", menu = submenu1)

submenu2 = Menu(menubar, tearoff = 0)
submenu2.add_command(label = "Yellow", command = lambda: edit_color(boardColor, colors[0], colors[1], 'yellow'))
submenu2.add_command(label = "Cyan", command = lambda: edit_color(boardColor, colors[0], colors[1], 'cyan'))
submenu2.add_command(label = "Light green", command = lambda: edit_color(boardColor, colors[0], colors[1], 'green'))
submenu2.add_command(label = "White", command = lambda: edit_color(boardColor, colors[0], colors[1], 'white'))
options_menu.add_cascade(label = "Player 2's color", menu = submenu2)

menubar.add_cascade(label = "Edit colors", menu = options_menu)

avatar = Menu(menubar, tearoff = 0)

submenu_avatar_1 = Menu(menubar, tearoff = 0)
submenu_avatar_1.add_command(label = "Mario", command = lambda: change_avatar(1, marioImage))
submenu_avatar_1.add_command(label = "Pikachu", command = lambda: change_avatar(1, pikachuImage))
submenu_avatar_1.add_command(label = "Sonic", command = lambda: change_avatar(1, sonicImage))
avatar.add_cascade(label = "Player 1's avatar", menu = submenu_avatar_1)

submenu_avatar_2 = Menu(menubar, tearoff = 0)
submenu_avatar_2.add_command(label = "Sackboy", command = lambda: change_avatar(2, sackboyImage))
submenu_avatar_2.add_command(label = "Kirby", command = lambda: change_avatar(2, kirbyImage))
submenu_avatar_2.add_command(label = "Zelda", command = lambda: change_avatar(2, zeldaImage))
avatar.add_cascade(label = "Player 2's avatar", menu = submenu_avatar_2)

menubar.add_cascade(label = "Edit avatars", menu = avatar)

help_menu = Menu(menubar, tearoff = 0)
help_menu.add_command(label = "Rules: how to play", command = display_help)
help_menu.add_command(label = "About...", command = display_about)
menubar.add_cascade(label = "Help", menu = help_menu)

can = Canvas(window, width = boardWidth, height = boardHeight, bg = boardColor)
canPhoto = Canvas(window, width = boardWidth, height = 70)
label1 = Label(window, fg = colors[2], bg = 'grey')

computerImage = PhotoImage(file = 'computerAvatar.gif')

marioImage = PhotoImage(file = 'marioAvatar.gif')
pikachuImage = PhotoImage(file = 'pikachuAvatar.gif')
sonicImage = PhotoImage(file = 'sonicAvatar.gif')

kirbyImage = PhotoImage(file = 'kirbyAvatar.gif')
zeldaImage = PhotoImage(file = 'zeldaAvatar.gif')
sackboyImage = PhotoImage(file = 'sackboyAvatar.gif')

change_avatar(1, marioImage)
change_avatar(2, zeldaImage)

canPhoto.pack()
# Waiting for a new click
can.bind('<Button-1>', event_function)
window.config(menu = menubar, bg = 'grey')
window.title("Connect Four!")

new_game(False)
window.mainloop()
