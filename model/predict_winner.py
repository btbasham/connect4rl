from game import game_runner
from game import basic_players
from game import connect4
import numpy as np

# What am I going to train on?
# Run basic players against each other and create finalized board vectors.
# With probability 1/2 roll back a move, otherwise take the final board
# target is the winner (if there is one)


# For now don't roll back, just take final board
NUM_EXAMPLES = 100000
NUM_TRAIN_EXAMPLES = 80000
NUM_TEST_EXAMPLES = NUM_EXAMPLES - NUM_TRAIN_EXAMPLES
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
    #num_steps_back = np.random.randint(7)
    # for i in range(num_steps_back):
    #    my_game.unmake_move()
    if winner != 2:
        games.append(my_game.board)
        winners.append(winner)

    # TODO: represent games as 3 channels instead of 1

print "calculated winners"
games = np.array(games)
winners = np.array(winners)

batch_size = 200
num_rows = connect4.NUM_ROWS
num_columns = connect4.NUM_COLUMNS


def transform_two_channels(game_board):
    assert len(game_board.shape) == 2
    return np.stack((game_board == 0, game_board == 1))

print games.shape
games = np.array([transform_two_channels(game) for game in games])
print games.shape

X_train = games[:NUM_TRAIN_EXAMPLES]
Y_train = winners[:NUM_TRAIN_EXAMPLES]

X_test = games[NUM_TRAIN_EXAMPLES:]
Y_test = winners[NUM_TRAIN_EXAMPLES:]

X_train = X_train.reshape(-1, 2, num_rows, num_columns)
X_test = X_test.reshape(-1, 2, num_rows, num_columns)
X_train.astype('float32')
X_test.astype('float32')
Y_train = Y_train.reshape(-1, 1).astype('float32')
Y_test = Y_test.reshape(-1, 1).astype('float32')

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D

print "made X,Y"
model = Sequential()

model.add(Convolution2D(50, 2, 2,
                        border_mode='valid',
                        input_shape=(2, num_rows, num_columns)))
model.add(Activation('relu'))
model.add(Convolution2D(50, 2, 2, border_mode='valid',))
model.add(Activation('relu'))
model.add(Convolution2D(50, 2, 2, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(50, 2, 2, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(50, 2, 2, border_mode='valid'))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(20))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(
    loss='binary_crossentropy', optimizer='adadelta', class_mode='binary')

print "compiled model"
model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=50,
          show_accuracy=True, verbose=1, validation_data=(X_test, Y_test))
print "fit"
score = model.evaluate(X_test, Y_test, show_accuracy=True, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
