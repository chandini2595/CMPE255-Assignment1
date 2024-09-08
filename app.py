from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Initialize game state
game_state = {
    'board': [' '] * 9,
    'current_player': 'X',
    'winner': None
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(game_state)

@app.route('/move', methods=['POST'])
def make_move():
    global game_state
    data = request.get_json()
    index = data.get('index')
    
    if game_state['board'][index] == ' ' and game_state['winner'] is None:
        game_state['board'][index] = game_state['current_player']
        winner = check_winner(game_state['board'])
        if winner:
            game_state['winner'] = winner
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset_game():
    global game_state
    game_state = {
        'board': [' '] * 9,
        'current_player': 'X',
        'winner': None
    }
    return jsonify(game_state)

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return board[condition[0]]
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)