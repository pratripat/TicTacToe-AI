import pygame, sys

pygame.init()

#CONSTS
EMPTY = 0
HUMAN = 'X'
AI = 'O'

#Players and the turn
players = [HUMAN, AI]
turn = 0

#Screen and resolution
res = 200
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('TicTacToe AI')
font = pygame.font.SysFont('comicsans', 60)

#Generates a 3*3 board
def generate_board(value):
    return [[value for j in range(3)] for i in range(3)]

#Renders the board
def render_board(screen, font, board):
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (64,38,92), (j*res+2, i*res+2, res-4, res-4))

            if board[i][j] != EMPTY:
                label = font.render(str(board[i][j]), 1, (189,75,100))
                screen.blit(label, ((j+0.5)*res-label.get_width()/2, (i+0.5)*res-label.get_height()/2))

#Adds move to board
def append_board(board, i, j, player):
    if [i,j] in get_posible_moves(board):
        board[i][j] = player
        return True

    return False

#Gives all possible moves from a given board
def get_posible_moves(board):
    return [[i,j] for j in range(3) for i in range(3) if board[i][j] == EMPTY]

#Alogrithm that find sthe best move from board state
def minimax(board, depth, maximising=True):
    winner = check_for_win(board)
    tie = check_for_tie(board)

    if winner:
        if winner == AI:
            return float('inf'), None
        return -float('inf'), None

    if tie:
        return 0, None

    if maximising:
        score = -float('inf')
        best_position = None

        for [i, j] in get_posible_moves(board):
            board[i][j] = AI
            new_score = minimax(board, depth-1, False)[0]

            if new_score > score:
                score = new_score
                best_position = [i, j]

            board[i][j] = EMPTY

        return score, best_position

    else:
        score = float('inf')
        best_position = None

        for [i, j] in get_posible_moves(board):
            board[i][j] = HUMAN
            new_score = minimax(board, depth-1, True)[0]

            if new_score < score:
                score = new_score
                best_position = [i, j]

            board[i][j] = EMPTY

        return score, best_position

#Returns who won the game
def check_for_win(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                continue

            current_player = board[i][j]
            for dir in [(1,0), (1,1), (0,1), (1,-1)]:
                for k in range(1,3):
                    i2 = i+(dir[1]*k)
                    j2 = j+(dir[0]*k)

                    if (i2 < 0 or i2 > 2) or (j2 < 0 or j2 > 2):
                        break

                    if board[i2][j2] != current_player:
                        break

                    if k == 2:
                        return current_player

    return None

#Returns if the game has been tied
def check_for_tie(board):
    for i in range(3):
        if EMPTY in board[i]:
            return False

    return True

#Generated board
board = generate_board(EMPTY)

#Game loop
while True:
    player = players[turn]

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Human's turn
            if player == AI:
                continue

            if append_board(board, event.pos[1]//res, event.pos[0]//res, player):
                turn += 1
                turn %= 2

    #Ai's turn
    if player == AI:
        score, (i,j) = minimax(board, 3)
        append_board(board, i, j, AI)
        turn += 1
        turn %= 2

    #Rendering and updating the screen
    screen.fill((27,30,35))
    render_board(screen, font, board)
    pygame.display.update()

    #Checking for win or tie
    winner = check_for_win(board)

    #The game has been won
    if winner:
        i = 0
        while i < 3000:
            label = font.render(f'{winner} won the game.', 1, (80,169,207))
            screen.blit(label, (screen.get_width()/2-label.get_width()/2, screen.get_height()/2-label.get_height()/2))
            pygame.display.update()
            i += 1

        board = generate_board(EMPTY)
        turn = 0

    #The game has been tied
    if check_for_tie(board):
        i = 0
        while i < 3000:
            label = font.render('The game has been tied.', 1, (80,169,207))
            screen.blit(label, (screen.get_width()/2-label.get_width()/2, screen.get_height()/2-label.get_height()/2))
            pygame.display.update()
            i += 1

        board = generate_board(EMPTY)
        turn = 0
