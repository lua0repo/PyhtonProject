import random

# Constants for the game
PLAYER = "X"
AI = "O"
EMPTY = " "
SIZE = 3

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(SIZE):
        if all([cell == player for cell in board[i]]):  # Check row
            return True
        if all([board[j][i] == player for j in range(SIZE)]):  # Check column
            return True
    
    # Check diagonals
    if all([board[i][i] == player for i in range(SIZE)]):  # Primary diagonal
        return True
    if all([board[i][SIZE-1-i] == player for i in range(SIZE)]):  # Secondary diagonal
        return True
    
    return False

def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    # If AI wins, return 1 (maximize for AI)
    if check_winner(board, AI):
        return 1
    # If player wins, return -1 (minimize for player)
    if check_winner(board, PLAYER):
        return -1
    # If board is full and no winner, it's a draw (return 0)
    if is_full(board):
        return 0
    
    if is_maximizing:
        best = -float('inf')
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = EMPTY
        return best
    else:
        best = float('inf')
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = EMPTY
        return best

def best_move(board):
    best_val = -float('inf')
    move = (-1, -1)
    
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    
    return move

def player_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            row, col = move // SIZE, move % SIZE
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER
                break
            else:
                print("Cell already taken! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Please enter a number between 1 and 9.")

def ai_move(board):
    print("AI is making its move...")
    row, col = best_move(board)
    board[row][col] = AI

def play_game():
    board = [[EMPTY] * SIZE for _ in range(SIZE)]
    print_board(board)
    
    while True:
        player_move(board)
        print_board(board)
        if check_winner(board, PLAYER):
            print("You win!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        
        ai_move(board)
        print_board(board)
        if check_winner(board, AI):
            print("AI wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe!")
    play_game()
