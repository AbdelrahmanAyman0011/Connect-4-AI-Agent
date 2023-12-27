# Connect 4 Problem Report

## Table of Contents:

1. [Introduction](#introduction)
2. [Assumptions](#assumptions)
3. [Algorithms](#algorithms)
4. [Results & Output](#results--output)

---

### Introduction <a name="introduction"></a>

Connect 4 is a two-player connection game where players choose a color and drop colored discs into a grid. The objective is to connect four discs in a row, vertically, horizontally, or diagonally. The game continues until one player achieves this goal or the grid fills up.

### Assumptions <a name="assumptions"></a>

- The game continues until the entire board is filled.
- The winning player is determined by achieving a greater number of connected fours.

### Algorithms <a name="algorithms"></a>

#### Minimax Algorithm

The Minimax algorithm evaluates possible moves by exploring the game tree to determine the best move, maximizing the AI's chances of winning while minimizing potential losses.

```python
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


```

### Minimax with Alpha-Beta Pruning

Alpha-Beta Pruning serves as an enhancement to the Minimax algorithm, drastically reducing the number of nodes evaluated within the game tree. This optimization technique operates by strategically eliminating branches that cannot impact the final decision, thereby vastly improving the search algorithm's efficiency.

#### How Alpha-Beta Pruning Works:

1. **Node Evaluation:**

   - Nodes within the game tree represent different game states resulting from player moves.

2. **Branch Elimination:**
   - Initialization of 'alpha' and 'beta' values to track best possible outcomes for players.
   - The algorithm selectively disregards branches by evaluating whether they can affect the final decision.
3. **Optimization Strategy:**

   - Alpha represents the maximizing player's best achievable value; beta represents the minimizing player's best achievable value.
   - If the algorithm identifies a move leading to a worse outcome than a previously evaluated move:
     - For the maximizing player, if alpha becomes greater than or equal to beta, it prunes the branch.
     - For the minimizing player, if beta becomes less than or equal to alpha, it prunes the branch.

4. **Efficiency Gains:**

   - Eliminating irrelevant branches reduces node evaluations, significantly trimming the search space.
   - This optimization facilitates deeper exploration of the game tree within a constrained time frame.

5. **Impact on Minimax:**
   - Alpha-Beta Pruning synergizes with the Minimax algorithm, elevating its performance in managing larger search spaces common in games like Connect 4.

Alpha-Beta Pruning is pivotal for the Minimax algorithm, enhancing its efficiency by smartly pruning irrelevant branches in the game tree, enabling more profound exploration and better decision-making within limited computational constraints.

```python
def minimaxPru(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    if depth == 0:
        return (None, score_position(board, AI_PIECE))
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
```
