from game import connect4
import abc


class Connect4Player:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def choose_move(self, game):
        return
