from keras import regularizers
from keras.models import Sequential
from keras.layers.core import Dense, Dropout

numVariables = 22
model = Sequential()
model.add(Dense(484, input_dim=numVariables, activation='relu', kernel_regularizer=regularizers.l2(0.1)))
model.add(Dense(2, activation='softmax'))
