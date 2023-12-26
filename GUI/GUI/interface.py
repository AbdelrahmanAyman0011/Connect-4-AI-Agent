import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
column = 0

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def calculate_board(board):
    PLAYER_SCORE = 0
    AI_SCORE = 0
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == AI_PIECE and board[r][c + 1] == AI_PIECE and board[r][c + 2] == AI_PIECE and board[r][c + 3] == AI_PIECE:
                AI_SCORE+=1 

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == AI_PIECE and board[r + 1][c] == AI_PIECE and board[r + 2][c] == AI_PIECE and board[r + 3][c] == AI_PIECE:
                AI_SCORE+=1 


    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == AI_PIECE and board[r + 1][c + 1] == AI_PIECE and board[r + 2][c + 2] == AI_PIECE and board[r + 3][c + 3] == AI_PIECE:
                AI_SCORE+=1 

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == AI_PIECE and board[r - 1][c + 1] == AI_PIECE and board[r - 2][c + 2] == AI_PIECE and board[r - 3][c + 3] == AI_PIECE:
                AI_SCORE+=1 

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE and board[r][c + 1] == PLAYER_PIECE and board[r][c + 2] == PLAYER_PIECE and board[r][c + 3] == PLAYER_PIECE:
                PLAYER_SCORE+=1 

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == PLAYER_PIECE and board[r + 1][c] == PLAYER_PIECE and board[r + 2][c] == PLAYER_PIECE and board[r + 3][c] == PLAYER_PIECE:
                PLAYER_SCORE+=1 


    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == PLAYER_PIECE and board[r + 1][c + 1] == PLAYER_PIECE and board[r + 2][c + 2] == PLAYER_PIECE and board[r + 3][c + 3] == PLAYER_PIECE:
                PLAYER_SCORE+=1 

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == PLAYER_PIECE and board[r - 1][c + 1] == PLAYER_PIECE and board[r - 2][c + 2] == PLAYER_PIECE and board[r - 3][c + 3] == PLAYER_PIECE:
                PLAYER_SCORE+=1 


    return AI_SCORE,PLAYER_SCORE

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(opp_piece) == 4:
        score -= 99999999999999999
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 50000
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 500

    # Your pieces score count
    if window.count(piece) == 4:
        score += 99999999999999999
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50000
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 500

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 100

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def end_game(board):
    return len(get_valid_locations(board)) == 0

def minimax(board, depth,maximizingPlayer):
    if depth == 0:
        return (None,score_position(board, AI_PIECE))
    valid_locations = get_valid_locations(board)
    if maximizingPlayer:
        value = -math.inf
        column = 0
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = 0
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def minimaxPru(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    if depth == 0:
        return (None,score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = 0
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimaxPru(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = 0
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimaxPru(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Connect Four")

# Font settings
font = pygame.font.Font(None, 36)

# Texts and positions
minimax_text = font.render("Play with Minimax", True, (255, 255, 255))
minimax_rect = minimax_text.get_rect(center=(200, 80))

minimaxPru_text = font.render("Play with MinimaxPru", True, (255, 255, 255))
minimaxPru_rect = minimaxPru_text.get_rect(center=(200, 140))


def display_result(player_wins, ai_wins):
    result_font = pygame.font.Font(None, 36)
    result_text = result_font.render(f"Player Wins: {player_wins} | AI Wins: {ai_wins}", True, RED)  # Set color to black
    result_rect = result_text.get_rect(topleft=(10, 10))  # Adjust the position to the top left corner
    screen.blit(result_text, result_rect)


# Font settings
font = pygame.font.Font(None, 36)

# Texts and positions
minimax_text = font.render("Play with Minimax", True, (255, 255, 255))
minimax_rect = minimax_text.get_rect(center=(200, 80))

minimaxPru_text = font.render("Play with MinimaxPru", True, (255, 255, 255))
minimaxPru_rect = minimaxPru_text.get_rect(center=(200, 140))

running = True
chosen_algorithm = None

while running:
    screen.fill((0, 0, 0))
    screen.blit(minimax_text, minimax_rect)
    screen.blit(minimaxPru_text, minimaxPru_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if minimax_rect.collidepoint(event.pos):
                chosen_algorithm = 'minimax'
                running = False

            if minimaxPru_rect.collidepoint(event.pos):
                chosen_algorithm = 'minimaxPru'
                running = False

    pygame.display.flip()

# Now 'chosen_algorithm' holds the user's choice
print("You chose to play with", chosen_algorithm)
algorithm_func = 1 if chosen_algorithm == 'minimax' else 0

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    AI_SCORE,PLAYER_SCORE = calculate_board(board)
                    ai_score ="AI Score", AI_SCORE
                    player_score = "PLAYER Score", PLAYER_SCORE
                    print(ai_score," ",player_score)
                    if end_game(board):
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # # Ask for Player 2 Input
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        if(algorithm_func):
            col, minimax_score = minimax(board, 5,  True)
        else:
            col, minimax_score = minimaxPru(board, 5, -math.inf, math.inf,  True)


        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            AI_SCORE,PLAYER_SCORE = calculate_board(board)
            ai_score ="AI Score", AI_SCORE
            player_score = "PLAYER Score", PLAYER_SCORE
            print(ai_score," ",player_score)
            if end_game(board):
                game_over = True
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        display_result(PLAYER_SCORE, AI_SCORE)
        pygame.display.update()
        pygame.time.wait(3000)