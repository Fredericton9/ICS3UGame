"""
Created by Kevin Leung and Austin Lee for ICS3U
"""
import pygame
from pygame import *
from random import *
import os
import sys
import platform
sys.path.append('modules')
from menu import *


init()
screen = display.set_mode((750,600))#Resolution

"""Loading Images"""
whiteKing = image.load("images/wking.png").convert_alpha()
blackKing = image.load("images/bking.png").convert_alpha()
whitePawn = image.load("images/wpawn.png").convert_alpha()
blackPawn = image.load("images/bpawn.png").convert_alpha()
whiteRook = image.load("images/wrook.png").convert_alpha()
blackRook = image.load("images/brook.png").convert_alpha()
whiteQueen = image.load("images/wqueen.png").convert_alpha()
blackQueen = image.load("images/bqueen.png").convert_alpha()
whiteBishop = image.load("images/wbishop.png").convert_alpha()
blackBishop = image.load("images/bbishop.png").convert_alpha()
whiteKnight = image.load("images/wknight.png").convert_alpha()
blackKnight = image.load("images/bknight.png").convert_alpha()
"""Grid System and Text"""
def GridSystem():
    grid_horizontal = font.render("a     b     c     d     e     f     g     h", 0, (0,255,0))
    game_menu.blit(grid_horizontal,(120,500))

    gridvert8 = font.render("8", 1, (0,255,0))
    game_menu.blit(gridvert8, (80,110))

    gridvert7 = font.render("7", 1, (0,255,0))
    game_menu.blit(gridvert7, (80,160))

    gridvert6 = font.render("6", 1, (0,255,0))
    game_menu.blit(gridvert6, (80,210))

    gridvert5 = font.render("5", 1, (0,255,0))
    game_menu.blit(gridvert5, (80,260))

    gridvert4 = font.render("4", 1, (0,255,0))
    game_menu.blit(gridvert4, (80,310))

    gridvert3 = font.render("3", 1, (0,255,0))
    game_menu.blit(gridvert3, (80,360))

    gridvert2 = font.render("2", 1, (0,255,0))
    game_menu.blit(gridvert2, (80,410))

    gridvert1 = font.render("1", 1, (0,255,0))
    game_menu.blit(gridvert1, (80,460))

    Title = font.render("CHESS BATTLE 2015",1,(255,255,255))
    game_menu.blit(Title,(275,50))

    MoveLog = font.render("Move Log:",1,(255,255,255))
    game_menu.blit(MoveLog,(575,100))
"""Assigns the starting positions for the pieces"""
def GameStart(): #Starting positions
    global game_board, PlayerTurn
    deselect_piece()
    PlayerTurn = 1
    game_board[0] = 'R1'; game_board[7] = 'R1'; game_board[-1] = 'R2'; game_board[-8] = 'R2'#R1 is Rook for White, R2 is rook for Black, etc
    game_board[1] = 'N1'; game_board[6] = 'N1'; game_board[-2] = 'N2'; game_board[-7] = 'N2'
    game_board[2] = 'B1'; game_board[5] = 'B1'; game_board[-3] = 'B2'; game_board[-6] = 'B2'
    game_board[4] = 'K1'; game_board[3] = 'Q1'; game_board[-4] = 'Q2'; game_board[-5] = 'K2'
    for i in range(8):
        game_board[8+i] = 'P1'
        game_board[48+i] = 'P2'
    for i in range(32):
        game_board[16+i] = None
"""Function to select pieces"""
def select_piece(location):
    global selected,moves,captures
    effect = pygame.mixer.Sound('Sound Effects/Move.mp3')
    effect.play()
    if game_board[location] == None or game_board[location][1] != str(PlayerTurn):
        return
    selected = location
    moves = []
    captures = []
    # Pawn for player 1, seperate because of promotions
    if game_board[selected] == 'P1':
        if game_board[selected+8] == None:
            moves.append(selected+8)
            if selected//8 == 1 and game_board[selected+16] == None:
                moves.append(selected+16)
        if selected%8 != 0 and ((game_board[selected+7] != None and game_board[selected+7][1] == '2') or \
                                (game_board[selected-1] == 'P2' and en_passent == selected-1)):
            captures.append(selected+7)
        if selected%8 != 7 and ((game_board[selected+9] != None and game_board[selected+9][1] == '2') or \
                                (game_board[selected+1] == 'P2' and en_passent == selected+1)):
            captures.append(selected+9)

    # Pawn for player 2
    if game_board[selected] == 'P2':
        if game_board[selected-8] == None:
            moves.append(selected-8)
            if selected//8 == 6 and game_board[selected-16] == None:
                moves.append(selected-16)
        if selected%8 != 7 and ((game_board[selected-7] != None and game_board[selected-7][1] == '1') or \
                                (game_board[selected+1] == 'P1' and en_passent == selected+1)):
            captures.append(selected-7)
        if selected%8 != 0 and ((game_board[selected-9] != None and game_board[selected-9][1] == '1') or \
                                (game_board[selected-1] == 'P1' and en_passent == selected-1)):
            captures.append(selected-9)

    # Rook and Queen for both players
    if game_board[selected][0] in 'RQ':
        x,y = selected%8,selected//8
        for i in range(x+1,8,1):
            if game_board[i+y*8] == None:   # Check if no blocking piece
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append(i+y*8)
                break
            else:
                break
        for i in range(x-1,-1,-1):
            if game_board[i+y*8] == None:
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(PlayerTurn):
                captures.append(i+y*8)
                break
            else:
                break
        for i in range(y+1,8,1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(PlayerTurn):
                captures.append(x+i*8)
                break
            else:
                break

        for i in range(y-1,-1,-1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(PlayerTurn):
                captures.append(x+i*8)
                break
            else:
                break

    # Bishop and Queen for both
    if game_board[selected][0] in 'BQ':
        i = selected+7
        while (i-7)%8 != 0 and (i-7)//8 != 7:   # Check if valid move
            if game_board[i] == None:   # Check if no blocking piece
                moves.append(i)
            elif game_board[i][1] != str(PlayerTurn): # Check if is attacking
                captures.append(i)
                break
            else:
                break
            i += 7
        i = selected+9
        while (i-9)%8 != 7 and (i-9)//8 != 7:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i += 9
        i = selected-7
        while (i+7)%8 != 7 and (i+7)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i -= 7
        i = selected-9
        while (i+9)%8 != 0 and (i+9)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(PlayerTurn):
                captures.append(i)
                break
            else:
                break
            i -= 9
    # Knight for both players
    if game_board[selected][0] == 'N':
        x,y = selected%8,selected//8
        if x >= 2 and y <= 6:   # Check if valid move
            if game_board[(x-2)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-2)+(y+1)*8)
            elif game_board[(x-2)+(y+1)*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append((x-2)+(y+1)*8)
        if x >= 1 and y <= 5:
            if game_board[(x-1)+(y+2)*8] == None:
                moves.append((x-1)+(y+2)*8)
            elif game_board[(x-1)+(y+2)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y+2)*8)
        if x <= 6 and y <= 5:
            if game_board[(x+1)+(y+2)*8] == None:
                moves.append((x+1)+(y+2)*8)
            elif game_board[(x+1)+(y+2)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y+2)*8)
        if x <= 5 and y <= 6:
            if game_board[(x+2)+(y+1)*8] == None:
                moves.append((x+2)+(y+1)*8)
            elif game_board[(x+2)+(y+1)*8][1] != str(PlayerTurn):
                captures.append((x+2)+(y+1)*8)
        if x <= 5 and y >= 1:
            if game_board[(x+2)+(y-1)*8] == None:
                moves.append((x+2)+(y-1)*8)
            elif game_board[(x+2)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x+2)+(y-1)*8)
        if x <= 6 and y >= 2:
            if game_board[(x+1)+(y-2)*8] == None:
                moves.append((x+1)+(y-2)*8)
            elif game_board[(x+1)+(y-2)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y-2)*8)
        if x >= 1 and y >= 2:
            if game_board[(x-1)+(y-2)*8] == None:
                moves.append((x-1)+(y-2)*8)
            elif game_board[(x-1)+(y-2)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y-2)*8)
        if x >= 2 and y >= 1:
            if game_board[(x-2)+(y-1)*8] == None:
                moves.append((x-2)+(y-1)*8)
            elif game_board[(x-2)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x-2)+(y-1)*8)

    # King for both players, bit more complicated because of checkmate
    if game_board[selected][0] == 'K':
        x,y = selected%8,selected//8
        attacked = attacked_spaces(1+PlayerTurn%2,game_board)
        if x >= 1 and y <= 6: # Check if valid move
            if game_board[(x-1)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-1)+(y+1)*8)
            elif game_board[(x-1)+(y+1)*8][1] != str(PlayerTurn): # Check if is attacking
                captures.append((x-1)+(y+1)*8)
        if y <= 6:
            if game_board[x+(y+1)*8] == None:
                moves.append(x+(y+1)*8)
            elif game_board[x+(y+1)*8][1] != str(PlayerTurn):
                captures.append(x+(y+1)*8)
        if x <= 6 and y <= 6:
            if game_board[(x+1)+(y+1)*8] == None:
                moves.append((x+1)+(y+1)*8)
            elif game_board[(x+1)+(y+1)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y+1)*8)
        if x <= 6:
            if game_board[(x+1)+y*8] == None:
                moves.append((x+1)+y*8)
            elif game_board[(x+1)+y*8][1] != str(PlayerTurn):
                captures.append((x+1)+y*8)
        if x <= 6 and y >= 1:
            if game_board[(x+1)+(y-1)*8] == None:
                moves.append((x+1)+(y-1)*8)
            elif game_board[(x+1)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x+1)+(y-1)*8)
        if y >= 1:
            if game_board[x+(y-1)*8] == None:
                moves.append(x+(y-1)*8)
            elif game_board[x+(y-1)*8][1] != str(PlayerTurn):
                captures.append(x+(y-1)*8)
        if x >= 1 and y >= 1:
            if game_board[(x-1)+(y-1)*8] == None:
                moves.append((x-1)+(y-1)*8)
            elif game_board[(x-1)+(y-1)*8][1] != str(PlayerTurn):
                captures.append((x-1)+(y-1)*8)
        if x >= 1:
            if game_board[(x-1)+y*8] == None:
                moves.append((x-1)+y*8)
            elif game_board[(x-1)+y*8][1] != str(PlayerTurn):
                captures.append((x-1)+y*8)

    # Find the player's king
    for i in range(64):
        if game_board[i] != None and game_board[i][0] == 'K' and game_board[i][1] == str(PlayerTurn):
            break

    # Check if a move will result in check
    t_moves = list(moves)
    for j in t_moves:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+PlayerTurn%2,t_game):
            moves.remove(j)

    # See if a capture will result in a check
    t_captures = list(captures)
    for j in t_captures:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+PlayerTurn%2,t_game):
            captures.remove(j)

    board_buttons[selected].event_on(5)
    for i in moves:
        board_buttons[i].event_on(6)
    for i in captures:
        board_buttons[i].event_on(7)
"""Deselects pieces"""
def deselect_piece():

    global captures,moves,selected
    if selected != None:
        board_buttons[selected].event_off(5)
        for i in moves:
            board_buttons[i].event_off(6)
        for i in captures:
            board_buttons[i].event_off(7)
        captures = []
        moves = []
        selected = None
"""Moves pieces"""
def move_piece(destination):#Moves piece

    global game_board, en_passent
    if game_board[selected][0] == 'P':
        # En-passent rule activation
        if abs(destination-selected) in (7,9) and en_passent != None and abs(en_passent-destination) == 8:
            game_board[en_passent] = None

        # En-passent rule initiation
        en_passent = None
        if abs(destination-selected) == 16:
            en_passent = destination

        # Open the menu to select promotion
        if destination < 8 and PlayerTurn == 2:
            open_menu(bpromote_menu)
        if destination > 55 and PlayerTurn == 1:
            open_menu(wpromote_menu)

    game_board[destination] = game_board[selected]
    game_board[selected] = None
"""Function to figure out attackable spaces"""
def attacked_spaces(player,board):
    attacked = []
    for i in range(64):
        if board[i] == None:
            continue

        # Pawn for player 1
        if board[i] == 'P1' and player == 1:
            if i%8 != 0:
                attacked.append(i+7)
            if i%8 != 7:
                attacked.append(i+9)

        # Pawn for player 2
        if board[i] == 'P2' and player == 2:
            if i%8 != 7:
                attacked.append(i-7)
            if i%8 != 0:
                attacked.append(i-9)

        # Rook and half of Queen for both players
        if board[i][0] in 'RQ' and board[i][1] == str(player):
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
        if board[i][0] in 'BQ' and board[i][1] == str(player):

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
        if board[i][0] == 'N' and board[i][1] == str(player):
            x,y = i%8,i//8

            if x >= 2 and y <= 6:
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

        if board[i][0] == 'K' and board[i][1] == str(player):
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
def is_checkmated():#Checkmate function
    for i in range(64):
        select_piece(i)
        if moves+captures != []:
            deselect_piece()
            return 0
        deselect_piece()
    return 1

""" Variables """

PlayerTurn = 1
selected = None
moves = []
captures = []
game_board = [None for i in range(64)]
en_passent = None

"""Game Board Creation"""
font = pygame.font.Font(None, 36)

win_bg = Surface((250,90))
win_bg.fill((220,20,60))
draw.rect(win_bg,(255,0,0),(5,5,240,80))

layer_black = Surface((50,50))
layer_black.fill((90,74,32))
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
game_menu = make_menu((0,0,800,800),'game',0)
open_menu(game_menu)

board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

for i in range(64):
    if (i+i//8)%2 == 0:
        board_buttons[i].add_layer(layer_black,(0,0),(0,))

add_layer_multi(layer_is_move,(0,0),(-5,6,-7),board_buttons)

add_objects(game_menu,board_buttons)

"""Promotion Menus"""
wqueen_btn = Button((10,10,50,50),'Q',(0,))
wknight_btn = Button((60,10,50,50),'N',(0,))
wrook_btn = Button((10,60,50,50),'R',(0,))
wbishop_btn = Button((60,60,50,50),'B',(0,))
bqueen_btn = Button((10,10,50,50),'Q',(0,))
bknight_btn = Button((60,10,50,50),'N',(0,))
brook_btn = Button((10,60,50,50),'R',(0,))
bbishop_btn = Button((60,60,50,50),'B',(0,))

wqueen_btn.add_layer(whiteQueen,(0,0),(0,))
wrook_btn.add_layer(whiteRook,(0,0),(0,))
wknight_btn.add_layer(whiteKnight,(0,0),(0,))
wbishop_btn.add_layer(whiteBishop,(0,0),(0,))
bqueen_btn.add_layer(blackQueen,(0,0),(0,))
brook_btn.add_layer(blackRook,(0,0),(0,))
bknight_btn.add_layer(blackKnight,(0,0),(0,))
bbishop_btn.add_layer(blackBishop,(0,0),(0,))

wpromote_menu = make_menu((240,240,120,120),'wpromote',1)
wpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(wpromote_menu,(wqueen_btn,wknight_btn,wrook_btn,wbishop_btn))

bpromote_menu = make_menu((240,240,120,120),'bpromote',1)
bpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(bpromote_menu,(bqueen_btn,bknight_btn,brook_btn,bbishop_btn))

"""Music!!!!!!!!!!!!"""
pygame.mixer.music.load('Music/Theme.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(0)
pygame.mixer.music.queue('Music/Theme2.mp3')

"""START THE GAME!"""
GameStart()

""" Main Loop """
running = 1
while running:
    """ STEP 1: Get inputs """
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

    """ STEP 2: Handle inputs / update menus """

    update_menus(mx,my,lc,chars)

    if is_menu_open(wpromote_menu) or is_menu_open(bpromote_menu):  # Promotion menus
        for i in wpromote_menu.get_pressed():   # Check selection
            close_menu(wpromote_menu)
            game_board[c] = i+'1'
            deselect_piece()
            PlayerTurn = 2
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(4)

        for i in bpromote_menu.get_pressed():   # Check selection
            close_menu(bpromote_menu)
            game_board[c] = i+'2'
            deselect_piece()
            PlayerTurn = 1
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(5)

    elif is_menu_open(game_menu):
        # Handle the game board and game menu
        for c in game_menu.get_pressed():
            if c == 'new':      # Reset game button
                GameStart()
            elif c == 'quit':   # Exit game button
                running = 0
            else:
                if selected == None:    # Select piece that was clicked on
                    select_piece(c)
                else:
                    if selected == c:   # Deselect currently selected piece
                        deselect_piece()
                    else:
                        if c in moves or c in captures: # If the chosen square is an option
                            move_piece(c)

                            if not is_menu_open(wpromote_menu) and not is_menu_open(bpromote_menu):
                                deselect_piece()
                                PlayerTurn = 1+PlayerTurn%2
                                if is_checkmated():
                                    open_menu(win_menu)
                                    win_menu.event_on(5+PlayerTurn%2)
                            else:
                                break

                        else:
                            deselect_piece()
                            select_piece(c)

    """ STEP 3: Draw menus """

    update_menu_images()

    if is_menu_open(game_menu):
        # Draw the pieces on the game board
        for i in range(64):
            if game_board[i] == 'P1':
                game_menu.blit(whitePawn,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'P2':
                game_menu.blit(blackPawn,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'K1':
                game_menu.blit(whiteKing,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'K2':
                game_menu.blit(blackKing,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'Q1':
                game_menu.blit(whiteQueen,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'Q2':
                game_menu.blit(blackQueen,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'R1':
                game_menu.blit(whiteRook,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'R2':
                game_menu.blit(blackRook,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'B1':
                game_menu.blit(whiteBishop,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'B2':
                game_menu.blit(blackBishop,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'N1':
                game_menu.blit(whiteKnight,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'N2':
                game_menu.blit(blackKnight,(100+(i%8)*50,450-(i//8)*50))
    font = pygame.font.Font(None, 36)
    GridSystem()
    screen.fill((0,0,255))
    draw.rect(screen,(255,0,0),(100,100,400,400))
    draw_menus(screen)

    display.flip()
    time.wait(10)

quit()
