from game import game_runner
from game import basic_players
import numpy as np

# What am I going to train on?
# Run basic players against each other and create finalized board vectors.
# With probability 1/2 roll back a move, otherwise take the final board
# target is the winner (if there is one)


# For now don't roll back, just take final board
NUM_EXAMPLES = 1000
games = []
winners = []


for i in range(NUM_EXAMPLES):
    my_game_runner = game_runner.GameRunner(
        basic_players.TakeWinningMoveRandomPlayer(),
        basic_players.TakeWinningMoveRandomPlayer())
    my_game = my_game_runner.run_game()
    # if np.random.rand() < .5:
    # roll back
    winner = my_game.winner()
    games.append(my_game.board)
    winners.append(winner)
