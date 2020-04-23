import ROOT
from ROOT import *

# Select Theano as backend for Keras
from os import environ
environ['KERAS_BACKEND'] = 'theano'

# Set architecture of system (AVX instruction set is not supported on SWAN)
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'

from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.optimizers import Adam
from keras.constraints import maxnorm

# Open file
SignFile = ROOT.TFile.Open("/afs/cern.ch/user/d/ddicroce/work/DNN/latino_Higgs.root")
BackFile = ROOT.TFile.Open("/afs/cern.ch/user/d/ddicroce/work/DNN/latino_Background.root")

# Get signal and background trees from file
signal     = SignFile.Get("latino")
background = BackFile.Get("latino")

# Add variables to dataloader
dataloader = ROOT.TMVA.DataLoader('dataset_pymva')
numVariables = 8
dataloader.AddVariable("mjj")
dataloader.AddVariable("mll")
dataloader.AddVariable("drll")
dataloader.AddVariable("dphill")
dataloader.AddVariable("ptTOT_cut")
dataloader.AddVariable("mTOT_cut")
dataloader.AddVariable("OLV1_cut")
dataloader.AddVariable("OLV2_cut")
weight = "XSWeight*SFweight2l*GenLepMatch2l*LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*bPogSF_CMVAL"
dataloader.SetSignalWeightExpression(weight)
dataloader.SetBackgroundWeightExpression(weight)

#################
# Add trees to dataloader
dataloader.AddSignalTree(signal, 1)
dataloader.AddBackgroundTree(background, 1)
trainTestSplit = 0.5
dataloader.PrepareTrainingAndTestTree(ROOT.TCut(''),
        'TrainTestSplit_Signal={}:'.format(trainTestSplit)+\
        'TrainTestSplit_Background={}:'.format(trainTestSplit)+\
        'SplitMode=Random')

# Setup TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

outputFile = ROOT.TFile.Open('TMVAOutputPyMVA_VBF.root', 'RECREATE')
factory = ROOT.TMVA.Factory('TMVAClassification', outputFile,
        '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:'+\
        'AnalysisType=Classification')


# Define model
model = Sequential()
model.add(Dense(72, input_dim=numVariables, init='glorot_normal', activation='relu'))
model.add(Dense(48, init='normal', activation='relu', W_constraint=maxnorm(1)))
model.add(Dropout(0.1))
model.add(Dense(32, init='glorot_normal', activation='relu',
        input_dim=numVariables))
model.add(Dropout(0.1))
model.add(Dense(32, init='glorot_normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(24, init='normal', activation='relu', W_constraint=maxnorm(1)))
model.add(Dense(4, init='normal', activation='relu', W_constraint=maxnorm(1)))
model.add(Dense(2, init='glorot_uniform', activation='softmax'))
#model.add(Dense(1, init='glorot_uniform', activation='sigmoid'))


# Set loss and optimizer
model.compile(loss='categorical_crossentropy', optimizer=Adam(),
        metrics=['categorical_accuracy',])
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Store model to file
model.save('model.h5')

# Print summary of model
model.summary()

# Keras interface with previously defined model
factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras',
        'H:!V:VarTransform=G:FilenameModel=model.h5:'+\
        'NumEpochs=10:BatchSize=72:'+\
        'TriesEarlyStopping=3')

factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras_v2',
        'H:!V:VarTransform=G:FilenameModel=model.h5:'+\
        'NumEpochs=20:BatchSize=72:'+\
        'TriesEarlyStopping=3')

factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras_v3',
        'H:!V:VarTransform=D,G:FilenameModel=model.h5:'+\
        'NumEpochs=10:BatchSize=72:')

# Fisher Method
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
        '!H:!V:Fisher:VarTransform=D,G')

# Gradient tree boosting from scikit-learn package
factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyGTB, 'GTB',
        'H:!V:VarTransform=None:'+\
        'NEstimators=100:LearningRate=0.1:MaxDepth=3')

# BDT method
factory.BookMethod(dataloader,'BDT', 'BDT',
        'H:!V:VarTransform=None:'+\
        'NTrees=1000:BoostType=Grad:SeparationType=GiniIndex:nCuts=20:PruneMethod=CostComplexity:PruneStrength=12')

factory.TrainAllMethods()

factory.TestAllMethods()

factory.EvaluateAllMethods()


# Enable Javascript for ROOT so that we can draw the canvas
#%jsroot on
# Print ROC
#canvas = factory.GetROCCurve(dataloader)
#canvas.Draw()
