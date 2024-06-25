from tictactoe import player, actions, result, winner, terminal
EMPTY = None
board = [['X', 'O', EMPTY],
        ['O', 'X', EMPTY],
        [EMPTY, EMPTY, 'X']]


print("winner: ", winner(board))
print(terminal(board))

board = [['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']]

print("winner: ", winner(board))
print(terminal(board))

