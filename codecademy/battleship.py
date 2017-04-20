from random import randint

board = []
board_size = 10

for x in range(10):
    board.append(["."] * board_size)


def print_board(board):
    for row in board:
        print " ".join(row)


print "Let's play Battleship!"
print_board(board)


def random_row(board):
    return randint(0, len(board) - 1)


def random_col(board):
    return randint(0, len(board[0]) - 1)


ship_row = random_row(board)
ship_col = random_col(board)

def build_ship(ship_row,ship_col):
    if ship_row < board_size-3:
        ship_row_position = [ship_row, ship_row + 1, ship_row + 2]
    else:
        ship_row_position = [ship_row, ship_row - 1, ship_row - 2]
    return [ship_row_position,ship_col]

ship = build_ship(ship_row,ship_col)
print ship

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(4):
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))

    if guess_row in ship[0] and guess_col == ship[1]:
        #Mark section that was hit with "H" & print new board
        guess_idx = ship[0].index(guess_row)
        ship[0][guess_idx] = "X"
        board[guess_row][guess_col] = "X"
        print_board(board)

        #Check if entire ship was sunk
        if ship[0] == ['X','X','X']:
            print "Congratulations! You sunk my battleship!"
            break
        else:
            print "Congratulations! You hit my battleship, but didn't sink it yet!"
            #print ship_row_position
    else:
        if (guess_row < 0 or guess_row > board_size-1) or (guess_col < 0 or guess_col > board_size-1):
            print "Oops, that's not even in the ocean."
        elif (board[guess_row][guess_col] == "O"):
            print "You guessed that one already."
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "O"
        print "Turn", turn + 1
        print_board(board)
        if turn == 9:
            print "Game Over"