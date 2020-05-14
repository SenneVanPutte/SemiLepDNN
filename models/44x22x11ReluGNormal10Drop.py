from keras.models import Sequential
from keras.layers.core import Dense, Dropout

numVariables = 22
model = Sequential()
model.add(Dense(44, input_dim=numVariables, init='glorot_normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(22, init='glorot_normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(11, init='glorot_normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(2, init='glorot_uniform', activation='softmax'))
