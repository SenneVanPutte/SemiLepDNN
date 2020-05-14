import copy

import ROOT
#from ROOT import *

# Select Theano as backend for Keras
import os
from os import environ
environ['KERAS_BACKEND'] = 'theano'

# Set architecture of system (AVX instruction set is not supported on SWAN)
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'

#from keras.models import Sequential
#from keras.layers.core import Dense, Dropout
from keras.optimizers import Adam
from keras.constraints import maxnorm


def run(cfg_file='cfg.py'):
    var = {}
    execfile(cfg_file, var)
    cfg_dict = copy.deepcopy(var['cfg_dict'])

    model_name = cfg_dict['model'].split('/')[-1].replace('.py', '')
    dnn_name = '_'.join(
        [
            cfg_dict['name'], 
            'DNN', 
            model_name, 
            str(cfg_dict['epochs'])+'epochs', 
            str(cfg_dict['batch_size'])+'batch', 
            str(cfg_dict['tries'])+'tries',
            str(len(cfg_dict['variables']))+'vars',
        ]
    )

    # Open files
    print('[run] Loading data')
    Sig_files = []
    for fil in cfg_dict['sig_files']:
        Sig_files.append(ROOT.TFile.Open(fil))
    
    Bck_files = []
    for fil in cfg_dict['bck_files']:
        Bck_files.append(ROOT.TFile.Open(fil))
    
    # Get signal and background trees from file
    sig_trees = []
    for fil in Sig_files:
        sig_trees.append(fil.Get(cfg_dict['tree_name']))
    bck_trees = []
    for fil in Bck_files:
        bck_trees.append(fil.Get(cfg_dict['tree_name']))
    
    # Add variables to dataloader
    print('[run] Adding variables')
    variables = cfg_dict['variables'] 
    
    out_dir = dnn_name
    os.system('mkdir '+out_dir)
    dataloader = ROOT.TMVA.DataLoader(out_dir)
    numVariables = len(variables)
    for var in variables:
        dataloader.AddVariable(var)
    weight = cfg_dict['weight'] 
    dataloader.SetSignalWeightExpression(weight)
    dataloader.SetBackgroundWeightExpression(weight)
    
    # Add trees to dataloader
    for tree in sig_trees:
        dataloader.AddSignalTree(tree, 1)
    for tree in bck_trees:
        dataloader.AddBackgroundTree(tree, 1)
    trainTestSplit = 0.75
    dataloader.PrepareTrainingAndTestTree(ROOT.TCut(''),
            'TrainTestSplit_Signal={}:'.format(trainTestSplit)+\
            'TrainTestSplit_Background={}:'.format(trainTestSplit)+\
            'SplitMode=Random')
    
    # Setup TMVA
    print('[run] Preparing factory')
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    #outputFile = ROOT.TFile.Open(out_dir+'/DNN.root', 'RECREATE')
    outputFile = ROOT.TFile.Open(dnn_name+'.root', 'RECREATE')
    factory = ROOT.TMVA.Factory('TMVAClassification', outputFile,
        '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:'+\
        'AnalysisType=Classification')

    # Load model
    print('[run] Loading model')
    os.system('cp '+cfg_dict['model']+' .')
    model_file = cfg_dict['model'].split('/')[-1]
    var = {}
    execfile(model_file, var)
    model = copy.deepcopy(var['model'])
    
    # Set loss and optimizer
    model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['categorical_accuracy',])
    #model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['binary_accuracy',])
    
    # Store model to file
    model.save(out_dir+'/model.h5')
    
    # Print summary of model
    model.summary()

    # Book method
    tra_str = ':VarTransform='+';'.join(cfg_dict['var_trans'])
    mod_str = ':FilenameModel='+out_dir+'/model.h5'
    epo_str = ':NumEpochs='+str(cfg_dict['epochs'])
    bat_str = ':BatchSize='+str(cfg_dict['batch_size'])
    if cfg_dict['tries'] is not None: try_str = ':TriesEarlyStopping='+str(cfg_dict['tries'])
    else: try_str = ''
    print('[run] Booking method: '+'H:!V'+tra_str+mod_str+epo_str+bat_str+try_str)
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras', 'H:!V'+tra_str+mod_str+epo_str+bat_str+try_str)

     
    print('[run] Start training')
    factory.TrainAllMethods()
    
    print('[run] Test method')
    factory.TestAllMethods()
    
    print('[run] Evaluate method')
    factory.EvaluateAllMethods()

    outputFile.Close()

#run('dnn_cfg.py')
#run()
