import numpy as np


NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_TO_WIN = 4  # Number in a row to win.


class Connect4Game:

    """
    board: numpy array of shape NUM_ROWS, NUM_COLUMNS, where the value of
    board[i, j] is: -1 if the hole in row i and column j is empty,
                   0 if it is filled by the first player,
                   1 if it is filled by the second player.

    board[:, 0] corresponds to the BOTTOM of the board.

    first_player_moves: list of columns in which the first player moved, in order.

    second_player_moves:  list of columns in which the second player moved,
    in order.

    lines_to_check: lines_to_check[i] is an array of shape (NUM_TO_WIN,2) where
    each value is an index into self.board, such that if all of those are the same value,
    that player has won the game.
    """

    def __init__(self, board=None, moves=None):

        if board:
            assert(board.shape == (NUM_ROWS, NUM_COLUMNS))
            self.board = board
        else:
            self.board = np.zeros((NUM_ROWS, NUM_COLUMNS)).astype(int)
            self.board.fill(-1)
        if moves:
            assert(len(moves) == 2)
            num_first_moves = len(moves[0])
            num_second_moves = len(moves[1])
            if (num_first_moves < num_second_moves) or (num_first_moves > num_second_moves + 2):
                assert(False)
            self.first_player_moves = moves[0]
            self.second_player_moves = moves[1]
        else:
            self.first_player_moves = []
            self.second_player_moves = []
        self.lines_to_check = self.generate_lines_to_check()

    def current_turn(self):
        """
        Returns 0 if it is the first players move, and 1 if it is the second players move.
        """
        if len(self.first_player_moves) == len(self.second_player_moves) + 1:
            return 1
        elif len(self.first_player_moves) == len(self.second_player_moves):
            return 0
        else:
            assert(False)

    def valid_moves(self):
        """ returns an array of length NUM_COLUMNS with 1s in the positions of
        columns in which a move can be made, and 0 otherwise
        """
        return (self.board[:, -1] == -1)

    def lowest_open_in_column(self, column):
        "For a given column, returns the lowest open row, or -1 if no row is open"
        for row in range(NUM_ROWS):
            if self.board[row, column] == -1:
                return row
        return -1

    def make_move(self, player, column):
        assert(player == self.current_turn())
        assert(self.valid_moves()[column] == 1)
        row = self.lowest_open_in_column(column)
        self.board[row, column] = player
        if player == 0:
            self.first_player_moves.append(column)
        elif player == 1:
            self.second_player_moves.append(column)

    def generate_lines_to_check(self):
        lines_to_check = []
        # Vertical:
        for col in range(NUM_COLUMNS):
            for row in range(NUM_ROWS - NUM_TO_WIN):
                line = []
                for offset in range(0, NUM_TO_WIN):
                    line.append((row + offset, col))
                lines_to_check.append(line)
        # horizontal
        for col in range(NUM_COLUMNS - NUM_TO_WIN):
            for row in range(NUM_ROWS):
                line = []
                for offset in range(0, NUM_TO_WIN):
                    line.append((row, col + offset))
                lines_to_check.append(line)
        # diag right
        for col in range(NUM_COLUMNS - NUM_TO_WIN):
            for row in range(NUM_ROWS - NUM_TO_WIN):
                line = []
                for offset in range(0, NUM_TO_WIN):
                    line.append((row + offset, col + offset))
                lines_to_check.append(line)
        # diag left
        for col in range(NUM_COLUMNS - NUM_TO_WIN):
            for row in range(NUM_TO_WIN, NUM_ROWS):
                line = []
                for offset in range(0, NUM_TO_WIN):
                    line.append((row - offset, col + offset))
                lines_to_check.append(line)
        return lines_to_check

    def winner(self):
        # TODO: Do this with numpy magic
        for line in self.lines_to_check:
            player = self.board[line[0]]
            if player == -1:
                continue
            winning_line = True
            for offset in range(1, NUM_TO_WIN):
                if self.board[line[offset]] != player:
                    winning_line = False
            if winning_line:
                return player
        return -1
