from keras.models import Sequential
from keras.layers.core import Dense, Dropout

numVariables = 22
model = Sequential()
model.add(Dense(352, input_dim=numVariables, init='glorot_normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(176, init='glorot_normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(88, init='glorot_normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, init='glorot_uniform', activation='softmax'))
