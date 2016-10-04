from game import basic_players
from game import game_runner

my_game_runner = game_runner.GameRunner(
    basic_players.HumanPlayer(), basic_players.TakeWinningMoveRandomPlayer())
my_game = my_game_runner.run_game()
winner = my_game.winner()
print "FINAL BOARD"
print my_game_runner.game.board
if winner == 0:
    print "YOU WIN!"
else:
    print "YOU LOSE!"
