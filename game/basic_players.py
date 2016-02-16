from game import player
from game import connect4
import numpy as np
from player import Connect4Player


class RandomPlayer(Connect4Player):

    def choose_move(self, game):
        return np.random.choice(game.valid_moves())


class TakeWinningMoveRandomPlayer(Connect4Player):

    def choose_move(self, game):
        valid_moves = game.valid_moves()
        my_player = game.current_turn()
        for move in valid_moves:
            game.make_move(move)
            if (game.winner() == my_player):
                return move
            game.unmake_move()
        return np.random.choice(valid_moves)


class HumanPlayer(Connect4Player):

    def choose_move(self, game):
        print "Board::"
        print game.board
        valid_cols = game.valid_cols()
        my_move = None
        while my_move == None:
            print "Select a column to play in:"
            move = int(raw_input())
            if valid_cols[move]:
                my_move = move
        return my_move
