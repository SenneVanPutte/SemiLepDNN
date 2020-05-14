from keras.models import Sequential
from keras.layers.core import Dense, Dropout

numVariables = 22
model = Sequential()
model.add(Dense(22, input_dim=numVariables, init='glorot_normal', activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(11, init='glorot_normal', activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(5, init='glorot_normal', activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(2, init='glorot_uniform', activation='softmax'))
