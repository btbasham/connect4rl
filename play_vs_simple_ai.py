from game import basic_players
from game import game_runner

game_runner = game_runner.GameRunner(
    basic_players.HumanPlayer(), basic_players.TakeWinningMoveRandomPlayer())
game = game_runner.run_game()
winner = game.winner()
print "FINAL BOARD"
print game_runner.game.board
if winner == 0:
    print "YOU WIN!"
else:
    print "YOU LOSE!"
