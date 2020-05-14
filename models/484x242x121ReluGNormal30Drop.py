from keras.models import Sequential
from keras.layers.core import Dense, Dropout

numVariables = 22
model = Sequential()
model.add(Dense(numVariables*numVariables, input_dim=numVariables, init='glorot_normal', activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(max(numVariables*numVariables/2, 20), init='glorot_normal', activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(max(numVariables*numVariables/4, 10), init='glorot_normal', activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(2, init='glorot_uniform', activation='softmax'))
