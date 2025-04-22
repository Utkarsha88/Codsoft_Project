from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

BOARD_SIZE = 4
HUMAN = 'X'
AI = 'O'
EMPTY = ""

def is_winner(board, player):
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)):
            return True
        if all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player for i in range(BOARD_SIZE)):
         return True
    if all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True
    return False

def is_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True




def evaluate(board):
    if is_winner(board, AI):
        return 100
    elif is_winner(board, HUMAN):
        return -100
    return 0 

def minimax(board, depth, alpha, beta, is_max):
    score = evaluate(board)
    if score != 0 or is_full(board) or depth == 0:
        
        return score

    if is_max:
        best = -math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    val = minimax(board, depth - 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    val = minimax(board, depth - 1 , alpha, beta, True)
                    board[i][j] = EMPTY
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def best_move(board):
    best_score = -math.inf
    move = (-1, -1)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 4, -math.inf, math.inf, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    
    
    if is_winner(board, HUMAN):
        return jsonify({
            'aiMove': [-1, -1],
            'winner': 'Human'
        })

    
    ai_row, ai_col = best_move(board)
    if ai_row != -1 and ai_col != -1:
        board[ai_row][ai_col] = AI

    
    winner = None
    if is_winner(board, AI):
        winner = 'AI'
    elif is_full(board):
        winner = 'Draw'

    return jsonify({
        'aiMove': [ai_row, ai_col],
        'winner': winner
    })

if __name__ == '__main__':
    app.run(debug=True)
