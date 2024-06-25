"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Declare a total count that will represent turn. 0 = X, 1 = O
    totalCount = 0

    # Iterate a board, add one to total count for every X, subtract for every Y
    for row in board:
        for column in row:
            if column == 'X':
                totalCount += 1
            if column == 'O':
                totalCount -= 1
    
    # Return X if totalCount = 0, O if otherwise
    return 'X' if totalCount == 0 else 'O'


def actions(board):
    # Check if the board state we are in is terminal

    # Declare a set of possible actions
    possibleActions = set()
    if terminal(board):
        return None
    
    if board is None:
        return None
    
    # Iterate each row and column, and add all empty indices to the set
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column is EMPTY:
                possibleActions.add((i, j))
    
    # Return the set of all possible actions
    return possibleActions
    raise NotImplementedError


def result(board, action):
    
    # Create a deepcopy of the board (copy.deepcopy(board))
    result = copy.deepcopy(board)
    
    # Check if action being done can be done, raise exception if it can't
    possibleActions = actions(board)
    if action not in possibleActions:
        raise ValueError
    
    # Update the deepcopy with the action of the player and return
    result[action[0]][action[1]] = player(board)
    return result
    raise NotImplementedError


def winner(board):
    
    # check if board is None
    if board is None:
        return None
    
    # Check all rows
    for row in board:
        # Create a set of the row, if it equals 1, then we only have one element and that is a winner
        if len(set(row)) == 1 and row[0] is not EMPTY:
            return row[0]
    
    # Check if middle square is not empty
    if board[1][1] is not EMPTY:
        # Create a list representing both diagonals
        diag1 = (board[0][0], board[1][1], board[2][2])
        diag2 = (board[2][0], board[1][1], board[0][2])
        # Transform it into a set
        check1 = set(diag1)
        check2 = set(diag2)
        
        # Check the length of each set to equal 1 and return the contents of the middle square
        if len(check1) == 1:
            return board[1][1]
        
        if len(check2) == 1:
            return board[1][1]
   
    # Create an iterable to traverse the first row only
    for count, element in enumerate(board[0]):

        # Check if the contents in the same position of the second and third row equal the one in the first
        if element is not None and (board[1][count] == element and board[2][count] == element):
            print("winning board column: ", board)
            return element
        
    # Return none if no winner or tied
    return None
    raise NotImplementedError


def terminal(board):
    # Check for a winner
    if board is None:
        return None
    
    if (winner(board)) is not None:
        return True
    
    # Check if board is full
    for row in board:
        for column in row:
            if column is None:
                return False
            
    return True
    raise NotImplementedError


def utility(board):
    # Check wether the winner is X or )
    util = winner(board)

    # Return 1 if X, -1 if O, 0 if None
    if util == 'X':
        return 1
    elif util == 'O':
        return -1
    return 0

    raise NotImplementedError


def minimax(board):
    # Check if state is terminal state
    if terminal(board):
        return None
    
    # Check whose turn is it
    turn = player(board)

    # Run the function corresponding to the turn
    if turn == 'X':
        value, move = maxV(board)
        return move
    elif turn == 'O':
        value, move = minV(board)
        return move
    
    return None
    raise NotImplementedError


def minV(board):
    # Check if board is a final board and return it's utility (and no move)
    if terminal(board):
        return utility(board), None
    
    # Declare a v Value as float('inf')
    v = float('inf')
    # Declare a value to store the move to return
    move = None
    possibleMoves = actions(board)
    # Iterate over all possible moves to do
    for action in possibleMoves:
        # Run maxV function of the result(board, action), x is the utility we are looking for
        calc, currMove = maxV(result(board, action))
        # If x smaller than v, make v = x
        if calc < v:
            v = calc
            # Change move to the current move
            move = action
        # If v == -1, return move
            if v == -1:
                return v, move
    # Return v, move
    return v, move
    raise NotImplementedError

# Function that will return the max optimization for the player


def maxV(board):
    # Check if board is a final board and return it's utility (and no move)
    if terminal(board):
        return utility(board), None
    # Declare a v Value as float('-inf')
    v = float('-inf')
    # Declare a value to store the move to return
    move = None
    possibleMoves = actions(board)

    # Iterate over all possible moves to do
    for action in possibleMoves:
        # Run minV function of the result(board, action), x is the utility we are looking for
        calc, currMove = minV(result(board, action))
        # If x > v, update v = x and move = new move
        if calc > v:
            v = calc
            move = action

         # If v == 1, return the move corresponding
            if v == 1:
                return v, move
    # return v, move
    return v, move
    raise NotImplementedError