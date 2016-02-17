from game import connect4


class GameRunner:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game = connect4.Connect4Game()

    def run_game(self):
        winner = -1
        while winner == -1:
            next_player = self.game.current_turn()
            game_copy = self.game.make_copy()
            move = None
            if next_player == 0:
                move = self.player1.choose_move(game_copy)
            elif next_player == 1:
                move = self.player2.choose_move(game_copy)
            self.game.make_move(move)
            winner = self.game.winner()
        return self.game
