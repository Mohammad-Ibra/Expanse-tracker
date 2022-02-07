import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid = False
        val = None
        while not valid:
            square = input(self.letter + "\'turn. Input moves (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid = True
            except ValueError:
                print("Invalid! Try again!")
        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        return random.choice(game.available_moves())

class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            # get the square based on the minimax algorithm 
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == "X" else "O"

        if state.current_winner == other_player:
            return {
                'position':None,
                'score': 1*(state.num_empty_spaces() + 1) if other_player == max_player else -1*(state.num_empty_spaces() + 1)
            }

        elif not state.empty_squares():
            return {
                'position':None,
                'score':0
            }

        if player == max_player:
            best = {
                'position':None,
                'score': -math.inf
            }
        else:
            best = {
                'position':None,
                'score': math.inf
            }
        
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

