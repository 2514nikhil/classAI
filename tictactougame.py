import os


def printboard(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")


def render_game(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Tic Tac Toe Game:")
    print("1  | 2 | 3")
    print("---|---|---")
    print("4  | 5 | 6")
    print("---|---|---")
    print("7  | 8 | 9")
    print("Select a number from 1 to 9 to place your mark (X or O) in the corresponding position.")
    print()
    printboard(board)

def checkwin(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != ' ':
            return True
    return False

def checkdraw(board):
    return ' ' not in board

def tic_tac_tou():
    board = [' '] * 9
    current_player = 'X'

    render_game(board)
    
    choice = 0
    moves = 0
    while moves < 9:
        try:
            if current_player == 'O':
                choice = int(input("Player O, enter your move (1-9): "))
            else:
                choice = int(input("Player X, enter your move (1-9): "))
            
            if choice < 1 or choice > 9:
                print("Invalid input! Please enter a number between 1 and 9.")
                continue
            
            if board[choice - 1] in ['X', 'O']:
                print("This position is already taken! Choose another one.")
                continue
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")
            continue

        board[choice - 1] = current_player
        moves += 1
        render_game(board)
        
        if checkwin(board):
            print(f"Player {current_player} wins!")
            break

        if checkdraw(board):
            print("It's a draw!")
            break
        
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    tic_tac_tou()