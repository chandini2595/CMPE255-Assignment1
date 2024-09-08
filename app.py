from flask import Flask, jsonify, request, send_from_directory
import random

app = Flask(__name__)

# Initialize game state
game_state = {
    'board': [],
    'flipped_cards': [],
    'matches': 0
}

def initialize_game():
    global game_state
    cards = list(range(1, 9)) * 2  # 8 pairs of cards
    random.shuffle(cards)
    game_state = {
        'board': [{'value': card, 'flipped': False} for card in cards],
        'flipped_cards': [],
        'matches': 0
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/init', methods=['POST'])
def init_game():
    initialize_game()
    return jsonify(game_state)

@app.route('/flip', methods=['POST'])
def flip_card():
    global game_state
    data = request.get_json()
    index = data.get('index')
    
    if len(game_state['flipped_cards']) < 2 and not game_state['board'][index]['flipped']:
        game_state['board'][index]['flipped'] = True
        game_state['flipped_cards'].append(index)
        
        if len(game_state['flipped_cards']) == 2:
            first, second = game_state['flipped_cards']
            if game_state['board'][first]['value'] == game_state['board'][second]['value']:
                game_state['matches'] += 1
            else:
                game_state['board'][first]['flipped'] = False
                game_state['board'][second]['flipped'] = False
            game_state['flipped_cards'] = []
    
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset_game():
    initialize_game()
    return jsonify(game_state)

if __name__ == '__main__':
    initialize_game()
    app.run(host='0.0.0.0', port=5003)
