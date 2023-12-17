import copy
import math

import pygame
import sys
import random

# GUI Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Gameplay Constants
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
EMPTY = 0

def create_board():
    return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def draw_board(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen,   (128, 0, 128), (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, (0, 0, 0), (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int((row + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), int(SQUARE_SIZE / 2 - 5))

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                    height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   int(SQUARE_SIZE / 2 - 5))
            elif board[row][col] == AI_PIECE:
                pygame.draw.circle(screen,  (0, 255, 0), (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                    height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   int(SQUARE_SIZE / 2 - 5))
    pygame.display.update()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True


    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


# Window(4 pieces) score evaluation
def evaluate_window(window,piece):
    score = 0

    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    # Opponent pieces score count
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 2

    # Your pieces score count
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    return score


# Finding the score of the current board
def score_position(board,piece):
    score = 0

    # Center Score:
    center_array = [int(i) for i in list(board[:][COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal Score:
    for r in range (ROW_COUNT):
        row_array = [int(i) for i in list(board[r][:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH] # Making a valid row of length 4 to check its pieces
            score += evaluate_window(window,piece)

    # Vertical Score:
    for c in range(COLUMN_COUNT-3):
        column_array = [int(i) for i in list(board[:][c])]
        for r in range(ROW_COUNT-3):
            window = column_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive Diagonal Score:
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)

    # Negative Diagonal Score:
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)

    return score


def is_terminal_node(board):
    return winning_move(board, AI_PIECE) or winning_move(board, PLAYER_PIECE) or len(get_valid_locations(board)) == 0


# Minimax Algorithm
def minimax(board, depth, maximizingPlayer):

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Finding the heuristic values of the board's last move
    if depth == 0 or is_terminal:

        # Winning move cases
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None,9999999999999) # --> (val, val) Same format because it is a recursive funciton that returns 2 values
            elif winning_move(board, PLAYER_PIECE):
                return (None, -9999999999999)
            else: # Game is over, no more valid moves
                return (None,0)
        # Depth is zero
        else:
            return (None,score_position(board, AI_PIECE))

    # If it is the AI move (maximizing player)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            row = get_next_open_row(board, c)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, c, AI_PIECE) # Child
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = c
        return column, value

    # If it is the Player move (minimizing player)
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            row = get_next_open_row(board, c)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, c,PLAYER_PIECE) # Child
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = c
        return column, value

# Getting the valid column locations that can be started with
def get_valid_locations(board):
    valid_locations = []
    for column in range(COLUMN_COUNT):
        if is_valid_location(board,column):
            valid_locations.append(column)
    return valid_locations


def main():
    pygame.init()

    global screen, width, height
    width = COLUMN_COUNT * SQUARE_SIZE
    height = (ROW_COUNT + 1) * SQUARE_SIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    my_font = pygame.font.SysFont("monospace", 75)

    board = create_board()
    draw_board(board)
    game_over = False
    turn = random.randint(PLAYER,AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER: # The Player Turn
                    col = event.pos[0] // SQUARE_SIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = my_font.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                        turn += 1
                        turn %= 2
                        draw_board(board)

        if turn == AI and not game_over: # The AI Turn
            col, minimax_score = minimax(board, 5, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = my_font.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn %= 2
                draw_board(board)

        if game_over:
            pygame.time.wait(3000)

if __name__ == "__main__":
    main()
