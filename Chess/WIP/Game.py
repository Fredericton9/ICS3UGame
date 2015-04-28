"""
Created by Kevin Leung and Austin Lee for ICS3U


Made on Portable Python 2.7
"""


"""Importing"""
import pygame
from pygame import *
from random import *
import os
import sys
import platform
sys.path.append('modules')
from menu import *


init()
Screen = display.set_mode((750,600))#Resolution

"""Loading Images"""
"""White Chess Pieces"""
WhiteKing = image.load("images/WhiteKing.png").convert_alpha()
WhitePawn = image.load("images/WhitePawn.png").convert_alpha()
WhiteRook = image.load("images/WhiteRook.png").convert_alpha()
WhiteQueen = image.load("images/WhiteQueen.png").convert_alpha()
WhiteBishop = image.load("images/WhiteBishop.png").convert_alpha()
WhiteKnight = image.load("images/WhiteKnight.png").convert_alpha()
"""Black Chess Pieces"""
BlackKing = image.load("images/BlackKing.png").convert_alpha()
BlackPawn = image.load("images/BlackPawn.png").convert_alpha()
BlackRook = image.load("images/BlackRook.png").convert_alpha()
BlackQueen = image.load("images/BlackQueen.png").convert_alpha()
BlackBishop = image.load("images/BlackBishop.png").convert_alpha()
BlackKnight = image.load("images/BlackKnight.png").convert_alpha()
"""Grid System and Text"""
def GridSystem():
    grid_horizontal = font.render("a     b     c     d     e     f     g     h", 0, (0,255,0))
    Game_Menu.blit(grid_horizontal,(120,500))
    gridvert8 = font.render("8", 1, (0,255,0))
    Game_Menu.blit(gridvert8, (80,110))
    gridvert7 = font.render("7", 1, (0,255,0))
    Game_Menu.blit(gridvert7, (80,160))
    gridvert6 = font.render("6", 1, (0,255,0))
    Game_Menu.blit(gridvert6, (80,210))
    gridvert5 = font.render("5", 1, (0,255,0))
    Game_Menu.blit(gridvert5, (80,260))
    gridvert4 = font.render("4", 1, (0,255,0))
    Game_Menu.blit(gridvert4, (80,310))
    gridvert3 = font.render("3", 1, (0,255,0))
    Game_Menu.blit(gridvert3, (80,360))
    gridvert2 = font.render("2", 1, (0,255,0))
    Game_Menu.blit(gridvert2, (80,410))
    gridvert1 = font.render("1", 1, (0,255,0))
    Game_Menu.blit(gridvert1, (80,460))
    Title = font.render("CHESS BATTLE 2015",1,(255,255,255))
    Game_Menu.blit(Title,(275,50))
    MoveLog = font.render("Move Log:",1,(255,255,255))
    Game_Menu.blit(MoveLog,(575,100))

"""
The game works on a grid system.
This grid is based on the fact that a Chess Board is 8x8, 64 spaces. Following the Python syntax, the first grid space starts on 0.
Because we are arranging the pieces onto this grid system, we can use simple mathematics to determine movements.
For example, to move a piece upwards a single space, we simply delete it from it's current grid and the grid that is Game_Board[x+8] gets the piece
This grid system also means that the pieces themselves don't have coordinates or any variables attached, rather, the different keys
on the board dictionary have values attached, which are the pieces, this means we can very freely add pieces, such as in promotions.
Empty spaces are simply listed as None and there is no piece rendered.
"""

"""Assigns the starting positions for the pieces"""
def GameStart(): #Starting positions
    global Game_Board, PlayerTurn
    Deselection()
    PlayerTurn = 1
    Game_Board[0] = 'R1'; Game_Board[7] = 'R1'; Game_Board[-1] = 'R2'; Game_Board[-8] = 'R2'#R1 is Rook for White, R2 is rook for Black, etc
    Game_Board[1] = 'N1'; Game_Board[6] = 'N1'; Game_Board[-2] = 'N2'; Game_Board[-7] = 'N2'
    Game_Board[2] = 'B1'; Game_Board[5] = 'B1'; Game_Board[-3] = 'B2'; Game_Board[-6] = 'B2'
    Game_Board[4] = 'K1'; Game_Board[3] = 'Q1'; Game_Board[-4] = 'Q2'; Game_Board[-5] = 'K2'
    for i in range(8): #Because we are in a grid system, we can use this For loop to create our pawns for both sides
        Game_Board[8+i] = 'P1'
        Game_Board[48+i] = 'P2'
    for i in range(32):
        Game_Board[16+i] = None

"""
300 lines exist right here for the selection and movement of pieces.
This mostly equates to applying the rules of Chess into mathematics, in terms of moving grid spaces in the game.
The Pawns are seperate for both players because they move in opposite directions.
The Queen does not have her own part in the function because the checks for her movements are done by combining
The Rook and Bishop.
The If statements also write to a list of captures and moves which are then used by the Capture and Movement functions
"""

"""Function to select pieces"""
def PieceSelection(location):
    global selected,moves,captures
    if Game_Board[location] == None or Game_Board[location][1] != str(PlayerTurn):
        return
    selected = location
    moves = []
    captures = []
    # Pawn for player 1
    if Game_Board[selected] == 'P1':#P1 means Pawn for Player 1
        if Game_Board[selected+8] == None:#This checks the space directly above the pawn
            moves.append(selected+8)
            if selected//8 == 1 and Game_Board[selected+16] == None:
                moves.append(selected+16)
        if selected%8 != 0 and ((Game_Board[selected+7] != None and Game_Board[selected+7][1] == '2')):
            captures.append(selected+7)
        if selected%8 != 7 and ((Game_Board[selected+9] != None and Game_Board[selected+9][1] == '2')):
            captures.append(selected+9)
    # Pawn for player 2
    if Game_Board[selected] == 'P2':
        if Game_Board[selected-8] == None:
            moves.append(selected-8)#This checks the space directly below the pawn
            if selected//8 == 6 and Game_Board[selected-16] == None:
                moves.append(selected-16)
        if selected%8 != 7 and ((Game_Board[selected-7] != None and Game_Board[selected-7][1] == '1')):
            captures.append(selected-7)
        if selected%8 != 0 and ((Game_Board[selected-9] != None and Game_Board[selected-9][1] == '1')):
            captures.append(selected-9)
    # Rook and Queen for both players
    if Game_Board[selected][0] in 'RQ':
        x,y = selected%8,selected//8
        for i in range(x+1,8,1):
            if Game_Board[i+y*8] == None:   # Check if no blocking piece
                moves.append(i+y*8)
            elif Game_Board[i+y*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append(i+y*8)
                break
            else:
                break
        for i in range(x-1,-1,-1):
            if Game_Board[i+y*8] == None:
                moves.append(i+y*8)
            elif Game_Board[i+y*8][1] != str(PlayerTurn):
                captures.append(i+y*8)
                break
            else:
                break
        for i in range(y+1,8,1):
            if Game_Board[x+i*8] == None:
                moves.append(x+i*8)
            elif Game_Board[x+i*8][1] != str(PlayerTurn):
                captures.append(x+i*8)
                break
            else:
                break

        for i in range(y-1,-1,-1):
            if Game_Board[x+i*8] == None:
                moves.append(x+i*8)
            elif Game_Board[x+i*8][1] != str(PlayerTurn):
                captures.append(x+i*8)
                break
            else:
                break
    # Bishop and Queen for both
    if Game_Board[selected][0] in 'BQ':
        i = selected+7
        while (i-7)%8 != 0 and (i-7)//8 != 7:   # Check if valid move
            if Game_Board[i] == None:   # Check if no blocking piece
                moves.append(i)
            elif Game_Board[i][1] != str(PlayerTurn): # Check if is attacking
                captures.append(i)
                break
            else:
                break
            i += 7
        i = selected+9
        while (i-9)%8 != 7 and (i-9)//8 != 7:
            if Game_Board[i] == None:
                moves.append(i)
            elif Game_Board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i += 9
        i = selected-7
        while (i+7)%8 != 7 and (i+7)//8 != 0:
            if Game_Board[i] == None:
                moves.append(i)
            elif Game_Board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i -= 7
        i = selected-9
        while (i+9)%8 != 0 and (i+9)//8 != 0:
            if Game_Board[i] == None:
                moves.append(i)
            elif Game_Board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i -= 9
    # Knight for both players
    if Game_Board[selected][0] == 'N':
        x,y = selected%8,selected//8
        if x >= 2 and y <= 6:   # Check if valid move
            if Game_Board[(x-2)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-2)+(y+1)*8)
            elif Game_Board[(x-2)+(y+1)*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append((x-2)+(y+1)*8)
        if x >= 1 and y <= 5:
            if Game_Board[(x-1)+(y+2)*8] == None:
                moves.append((x-1)+(y+2)*8)
            elif Game_Board[(x-1)+(y+2)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y+2)*8)
        if x <= 6 and y <= 5:
            if Game_Board[(x+1)+(y+2)*8] == None:
                moves.append((x+1)+(y+2)*8)
            elif Game_Board[(x+1)+(y+2)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y+2)*8)
        if x <= 5 and y <= 6:
            if Game_Board[(x+2)+(y+1)*8] == None:
                moves.append((x+2)+(y+1)*8)
            elif Game_Board[(x+2)+(y+1)*8][1] != str(PlayerTurn):
                captures.append((x+2)+(y+1)*8)
        if x <= 5 and y >= 1:
            if Game_Board[(x+2)+(y-1)*8] == None:
                moves.append((x+2)+(y-1)*8)
            elif Game_Board[(x+2)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x+2)+(y-1)*8)
        if x <= 6 and y >= 2:
            if Game_Board[(x+1)+(y-2)*8] == None:
                moves.append((x+1)+(y-2)*8)
            elif Game_Board[(x+1)+(y-2)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y-2)*8)
        if x >= 1 and y >= 2:
            if Game_Board[(x-1)+(y-2)*8] == None:
                moves.append((x-1)+(y-2)*8)
            elif Game_Board[(x-1)+(y-2)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y-2)*8)
        if x >= 2 and y >= 1:
            if Game_Board[(x-2)+(y-1)*8] == None:
                moves.append((x-2)+(y-1)*8)
            elif Game_Board[(x-2)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x-2)+(y-1)*8)

    # King for both players, bit more complicated because of checkmate
    if Game_Board[selected][0] == 'K':
        x,y = selected%8,selected//8
        attacked = attacked_spaces(1+PlayerTurn%2,Game_Board)
        if x >= 1 and y <= 6: # Check if valid move
            if Game_Board[(x-1)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-1)+(y+1)*8)
            elif Game_Board[(x-1)+(y+1)*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append((x-1)+(y+1)*8)
        if y <= 6:
            if Game_Board[x+(y+1)*8] == None:
                moves.append(x+(y+1)*8)
            elif Game_Board[x+(y+1)*8][1] != str(PlayerTurn):
                captures.append(x+(y+1)*8)
        if x <= 6 and y <= 6:
            if Game_Board[(x+1)+(y+1)*8] == None:
                moves.append((x+1)+(y+1)*8)
            elif Game_Board[(x+1)+(y+1)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y+1)*8)
        if x <= 6:
            if Game_Board[(x+1)+y*8] == None:
                moves.append((x+1)+y*8)
            elif Game_Board[(x+1)+y*8][1] != str(PlayerTurn):
                captures.append((x+1)+y*8)
        if x <= 6 and y >= 1:
            if Game_Board[(x+1)+(y-1)*8] == None:
                moves.append((x+1)+(y-1)*8)
            elif Game_Board[(x+1)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y-1)*8)
        if y >= 1:
            if Game_Board[x+(y-1)*8] == None:
                moves.append(x+(y-1)*8)
            elif Game_Board[x+(y-1)*8][1] != str(PlayerTurn):
                captures.append(x+(y-1)*8)
        if x >= 1 and y >= 1:
            if Game_Board[(x-1)+(y-1)*8] == None:
                moves.append((x-1)+(y-1)*8)
            elif Game_Board[(x-1)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y-1)*8)
        if x >= 1:
            if Game_Board[(x-1)+y*8] == None:
                moves.append((x-1)+y*8)
            elif Game_Board[(x-1)+y*8][1] != str(PlayerTurn):
                captures.append((x-1)+y*8)

    # Find the player's king
    for i in range(64):
        if Game_Board[i] != None and Game_Board[i][0] == 'K' and Game_Board[i][1] == str(PlayerTurn):
            break

    # Check if a move will result in check
    t_moves = list(moves)
    for j in t_moves:
        t_game = list(Game_Board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if Game_Board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+PlayerTurn%2,t_game):
            moves.remove(j)

    # See if a capture will result in a check
    t_captures = list(captures)
    for j in t_captures:
        t_game = list(Game_Board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if Game_Board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+PlayerTurn%2,t_game):
            captures.remove(j)
    board_buttons[selected].event_on(5)
    for i in moves:
        board_buttons[i].event_on(6)
    for i in captures:
        board_buttons[i].event_on(7)

"""Deselects pieces"""
def Deselection(): #This is very important because this is one of the most used functions.
    global captures,moves,selected
    if selected != None:#Ensures that no new piece was selected before continuing with resetting the state of selection.
        board_buttons[selected].event_off(5)
        for i in moves:
            board_buttons[i].event_off(6)
        for i in captures:
            board_buttons[i].event_off(7)
        captures = []
        moves = []
        selected = None
"""Moves pieces"""
def move_piece(destination):
    global Game_Board
    if Game_Board[selected][0] == 'P':
        # Open the menu to select promotion
        if destination < 8 and PlayerTurn == 2:# These 2 If statements check if the piece has moved to the entire top row or bottom row, which are >55 and <8 respectively in the grid system
            open_menu(bpromote_menu)
        if destination > 55 and PlayerTurn == 1:
            open_menu(wpromote_menu)
    Game_Board[destination] = Game_Board[selected]
    Game_Board[selected] = None


"""
In order to determine whether a space will be marked as attackable, the piece is checked in a similar way to movement
except different pieces move differently, as well, it checks for an occupying piece.
Attackable spaces are not highlighted because the boxes will block out the rendered chess pieces.
"""
"""Function to figure out attackable spaces"""
def attacked_spaces(player,board):
    attacked = []#The dictionary is re-created each time to ensure it is empty for each selection event
    for i in range(64):#The entire chess board, 64 spaces
        if board[i] == None:#Skips over all the empty spaces, they don't matter in capturing
            continue
        # Pawn for player 1
        if board[i] == 'P1' and player == 1:#This finds the Pawn for player 1 and also checks if the current turn is for player 1
            if i%8 != 0:#Space to the left corner
                attacked.append(i+7)#Lists off that it is attackable, to be rendered as such 
            if i%8 != 7:#Space to the right corner
                attacked.append(i+9)
        # Pawn for player 2
        if board[i] == 'P2' and player == 2:
            if i%8 != 7:
                attacked.append(i-7)
            if i%8 != 0:
                attacked.append(i-9)
"""
The Queen in Chess uses a combination of the Rook and Bishop's moves.
In the code this is represented as the code for both Rooks and Bishops
being shared for the Queen

The Rook and Bishop have very simple capture spaces that are similar to their movements
except that in capturing, the space is checked for occupancy by a opponent's piece
"""
        # Rook and half of Queen for both players
        if board[i][0] in 'RQ' and board[i][1] == str(player):#Straight lines, for the rook.
            x,y = i%8,i//8
            for j in range(x+1,8,1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break
            for j in range(x-1,-1,-1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break
            for j in range(y+1,8,1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break
            for j in range(y-1,-1,-1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break
        # Bishop and other half of Queen for both players
        if board[i][0] in 'BQ' and board[i][1] == str(player):#The movements here are in diagonals
            j = i+7
            while (j-7)%8 != 0 and (j-7)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 7
            j = i+9
            while (j-9)%8 != 7 and (j-9)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 9
            j = i-7
            while (j+7)%8 != 7 and (j+7)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 7
            j = i-9
            while (j+9)%8 != 0 and (j+9)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 9
        # Knight for both players
        if board[i][0] == 'N' and board[i][1] == str(player):#The Knight is quite simple, it can only move in an L fashion.
            x,y = i%8,i//8
            if x >= 2 and y <= 6:#The math here involves checking the spaces that are in an L from the current space.
                attacked.append((x-2)+(y+1)*8)
            if x >= 1 and y <= 5:
                attacked.append((x-1)+(y+2)*8)
            if x <= 6 and y <= 5:
                attacked.append((x+1)+(y+2)*8)
            if x <= 5 and y <= 6:
                attacked.append((x+2)+(y+1)*8)
            if x <= 5 and y >= 1:
                attacked.append((x+2)+(y-1)*8)
            if x <= 6 and y >= 2:
                attacked.append((x+1)+(y-2)*8)
            if x >= 1 and y >= 2:
                attacked.append((x-1)+(y-2)*8)
            if x >= 2 and y >= 1:
                attacked.append((x-2)+(y-1)*8)
        #The King for both players
        if board[i][0] == 'K' and board[i][1] == str(player):#The King has the most simplest attackable spaces, 1 space in all directions
            x,y = i%8,i//8
            if x >= 1 and y <= 6:
                attacked.append((x-1)+(y+1)*8)
            if y <= 6:
                attacked.append(x+(y+1)*8)
            if x <= 6 and y <= 6:
                attacked.append((x+1)+(y+1)*8)
            if x <= 6:
                    attacked.append((x+1)+y*8)
            if x <= 6 and y >= 1:
                attacked.append((x+1)+(y-1)*8)
            if y >= 1:
                attacked.append(x+(y-1)*8)
            if x >= 1 and y >= 1:
                attacked.append((x-1)+(y-1)*8)
            if x >= 1:
                attacked.append((x-1)+y*8)
    return attacked
"""Function to determine checkmate victory"""
def is_checkmated():
    for i in range(64):
        PieceSelection(i)
        if moves+captures != []:#This If statement right here prevents a piece from being selected and "checkmates" the player
            Deselection()
            return 0
        Deselection()
    return 1

""" Variables """

PlayerTurn = 1
selected = None
moves = []
captures = []
Game_Board = [None for i in range(64)]

"""Game Board Creation"""
font = pygame.font.Font(None, 36)

win_bg = Surface((250,90))
win_bg.fill((220,20,60))
draw.rect(win_bg,(255,0,0),(5,5,240,80))

layer_Black = Surface((50,50))
layer_Black.fill((90,74,32))
layer_is_move = Surface((50,50),SRCALPHA)
layer_is_move.fill((120,0,120))

new_bg = Surface((100,20))
new_bg.fill((255,0,0))
new_bg2 = Surface((100,20))
new_bg2.fill((0,0,255))

promote_layer = Surface((120,120))
promote_layer.fill((255,0,0))
draw.rect(promote_layer,(220,20,60),(5,5,110,110))
draw.rect(promote_layer,(255,255,255),(10,10,100,100))
draw.line(promote_layer,(255,0,0),(10,60),(110,60),5)
draw.line(promote_layer,(255,0,0),(60,10),(60,110),5)

"""Grid Spaces"""
Game_Menu = make_menu((0,0,800,800),'game',0)
open_menu(Game_Menu)

board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

for i in range(64):
    if (i+i//8)%2 == 0:
        board_buttons[i].add_layer(layer_Black,(0,0),(0,))

add_layer_multi(layer_is_move,(0,0),(-5,6,-7),board_buttons)

add_objects(Game_Menu,board_buttons)

"""Promotion Menus"""
#The buttons for the promotion menus
Wqueen_btn = Button((10,10,50,50),'Q',(0,))
Wknight_btn = Button((60,10,50,50),'N',(0,))
Wrook_btn = Button((10,60,50,50),'R',(0,))
Wbishop_btn = Button((60,60,50,50),'B',(0,))
Bqueen_btn = Button((10,10,50,50),'Q',(0,))
Bknight_btn = Button((60,10,50,50),'N',(0,))
Brook_btn = Button((10,60,50,50),'R',(0,))
Bbishop_btn = Button((60,60,50,50),'B',(0,))
#Rendering the actual pieces onto the buttons
Wqueen_btn.add_layer(WhiteQueen,(0,0),(0,))
Wrook_btn.add_layer(WhiteRook,(0,0),(0,))
Wknight_btn.add_layer(WhiteKnight,(0,0),(0,))
Wbishop_btn.add_layer(WhiteBishop,(0,0),(0,))
Bqueen_btn.add_layer(BlackQueen,(0,0),(0,))
Brook_btn.add_layer(BlackRook,(0,0),(0,))
Bknight_btn.add_layer(BlackKnight,(0,0),(0,))
Bbishop_btn.add_layer(BlackBishop,(0,0),(0,))
#White and Black promotion objects
wpromote_menu = make_menu((240,240,120,120),'wpromote',1)
wpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(wpromote_menu,(Wqueen_btn,Wknight_btn,Wrook_btn,Wbishop_btn))

bpromote_menu = make_menu((240,240,120,120),'bpromote',1)
bpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(bpromote_menu,(Bqueen_btn,Bknight_btn,Brook_btn,Bbishop_btn))

"""Music!!!!!!!!!!!!"""
pygame.mixer.music.load('music/Theme.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(0)
pygame.mixer.music.queue('music/Theme2.mp3')

"""START THE GAME!"""
GameStart()

"""The Main Game Loop"""
running = 1
while running:
    """Acquiring Inputs"""
    chars = ''
    for evnt in event.get():
        if evnt.type == QUIT:
            running = 0
        elif evnt.type == KEYDOWN:
            if evnt.key == K_ESCAPE:
                running = 0
            else:
                chars += evnt.unicode
    lc,rc = mouse.get_pressed()[0:2]
    mx,my = mouse.get_pos()

    """Handling the Inputs and Refreshing"""

    update_menus(mx,my,lc,chars)
    if is_menu_open(wpromote_menu) or is_menu_open(bpromote_menu):  # Promotion menus
        for i in wpromote_menu.get_pressed():   # Check selection
            close_menu(wpromote_menu)
            Game_Board[c] = i+'1'
            Deselection()
            PlayerTurn = 2
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(4)
        for i in bpromote_menu.get_pressed():   # Check selection
            close_menu(bpromote_menu)
            Game_Board[c] = i+'2'
            Deselection()
            PlayerTurn = 1
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(5)

    elif is_menu_open(Game_Menu):
        # Handle the game board and game menu
        for c in Game_Menu.get_pressed():
            if c == 'new':      # Reset game button
                GameStart()
            elif c == 'quit':   # Exit game button
                running = 0
            else:
                if selected == None:    # Select piece that was clicked on
                    PieceSelection(c)
                else:
                    if selected == c:   # Deselect currently selected piece
                        Deselection()
                    else:
                        if c in moves or c in captures: # If the chosen square is an option
                            move_piece(c)

                            if not is_menu_open(wpromote_menu) and not is_menu_open(bpromote_menu):
                                Deselection()
                                PlayerTurn = 1+PlayerTurn%2
                                if is_checkmated():
                                    open_menu(win_menu)
                                    win_menu.event_on(5+PlayerTurn%2)
                            else:
                                break
                        else:
                            Deselection()
                            PieceSelection(c)
    """Drawing all the pieces"""
    update_menu_images()
    if is_menu_open(Game_Menu):
        # Draw the pieces on the game board
        for i in range(64):
            if Game_Board[i] == 'P1':
                Game_Menu.blit(WhitePawn,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'P2':
                Game_Menu.blit(BlackPawn,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'K1':
                Game_Menu.blit(WhiteKing,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'K2':
                Game_Menu.blit(BlackKing,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'Q1':
                Game_Menu.blit(WhiteQueen,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'Q2':
                Game_Menu.blit(BlackQueen,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'R1':
                Game_Menu.blit(WhiteRook,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'R2':
                Game_Menu.blit(BlackRook,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'B1':
                Game_Menu.blit(WhiteBishop,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'B2':
                Game_Menu.blit(BlackBishop,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'N1':
                Game_Menu.blit(WhiteKnight,(100+(i%8)*50,450-(i//8)*50))
            if Game_Board[i] == 'N2':
                Game_Menu.blit(BlackKnight,(100+(i%8)*50,450-(i//8)*50))
    font = pygame.font.Font(None, 36)
    GridSystem()
    Screen.fill((0,0,255))
    draw.rect(Screen,(255,0,0),(100,100,400,400))
    draw_menus(Screen)
    display.flip()
    time.wait(10)
quit()
