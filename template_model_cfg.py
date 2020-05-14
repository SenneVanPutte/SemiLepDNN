src_dir = '/pnfs/iihe/cms/store/user/svanputt/HWWNano/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__Semilep2017__MHSemiLepVars__MH2HDMaBDTsplit__MHskim4BDT__hadd/'

cfg_dict = {
    # Name tag
    'name' : '2HDMaVWjets',
 
    # Signal files list
    'sig_files' : [
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_1200_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_1200_MH4_150_pos.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_200_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_200_MH4_150_pos.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_300_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_300_MH4_150_pos.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_400_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_400_MH4_150_pos.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_500_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_500_MH4_150_pos.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_600_MH4_150_neg.root',
    src_dir+'nanoLatino_2HDMa_SemiLep_MH3_600_MH4_150_pos.root',
    ],

    # Background files list
    'bck_files' : [
    src_dir+'nanoLatino_WJetsToLNu-0J.root',
    src_dir+'nanoLatino_WJetsToLNu-1J.root',
    src_dir+'nanoLatino_WJetsToLNu-2J.root',
    ],

    # Name of trees in the root files
    'tree_name' : 'Events',

    # List with variables
    'variables' : [
        'mtw1', 
        'MHlnjj_deta_ljjVmet', 
        'MHlnjj_dphi_ljjVmet', 
        'MHlnjj_deta_jjVl', 
        'MHlnjj_dphi_jjVl', 
        'MHlnjj_dphi_lVmet', 
        'MHlnjj_deta_lVmet', 
        'PuppiMET_pt', 
        'MHlnjj_pt_ljj', 
        'MHlnjj_m_lmetjj', 
        'MHlnjj_PTljj_D_PTmet', 
        'MHlnjj_PTljj_D_Mlmetjj', 
        'MHlnjj_MINPTlj_D_PTmet', 
        'MHlnjj_MINPTlj_D_Mlmetjj', 
        'MHlnjj_dphi_jVj', 
        'MHlnjj_deta_jVj', 
        'MHlnjj_m_jj', 
        'MHlnjj_m_ljj', 
        'MHlnjj_MAXPTlj_D_PTmet', 
        'MHlnjj_MAXPTlj_D_Mlmetjj','MHlnjj_MTljj_D_PTmet', 
        'MHlnjj_MTljj_D_Mlmetjj'
    ],

    # Event weights
    'weight' : 'XSWeight*Lepton_tightElectron_mvaFall17V1Iso_WP90_IdIsoSF[0]*Lepton_tightMuon_cut_Tight_HWWW_IdIsoSF[0]*puWeight*TriggerEffWeight_1l*Lepton_RecoSF[0]*EMTFbug_veto*Alt$(Lepton_promptgenmatched[0],0)*METFilter_MC*PrefireWeight*MH2HDMaBDT_trainingWeight',

    # File path to python file containing the model
    'model' : #MODEL_FILE, 

    # Data transformations
    'var_trans' : ['G'],    
   
    # Epochs 
    'epochs' : 50,

    # Batch size
    'batch_size' : 50,

    # Stop after X epochs of no improvement
    'tries' : 10,
}
