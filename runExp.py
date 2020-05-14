import os


def write_python(source_dir, var):
    py_file = open('job.py', 'w')
    # imports
    py_file.write('#!/usr/bin/env python\n')
    py_file.write('import os\n')
    #py_file.write('import ROOT\n')
    py_file.write('from analyze import analyze_ks\n')
    py_file.write('from runDNN import run\n')
    py_file.write('\n')
  
    # train
    py_file.write('run()\n')
    py_file.write('\n')
    
    # validate
    py_file.write('r_files = os.listdir(\'.\')\n')
    #py_file.write('os.system(\'pwd\')\n')
    #py_file.write('os.system(\'ls -l\')\n')
    py_file.write('print(r_files)\n')
    py_file.write('for r_file in r_files:\n')
    py_file.write('    if \'.root\' in r_file and \'_DNN\' in r_file: break\n')
    py_file.write('print(r_file)\n')
    #py_file.write('pm, sig, roc, sigy = analyze(r_file)\n')
    #py_file.write('pm, sig, roc, sigy = analyze(\'DNN.root\')\n')
    #py_file.write('ps, pb, pm, sig, roc, sigy = analyze_ks(\'DNN.root\', \'PyKeras\')\n')
    py_file.write('ps, pb, pm, sig, roc, sigy = analyze_ks(r_file, \'PyKeras\')\n')
    py_file.write('\n')

    # wite results
    #py_file.write('res_str = \'{:30}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\'.format(\''+var+'\', pm, sig, roc, sigy)\n')
    py_file.write('res_str = \'{:30}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\'.format(\''+var+'\', ps, pb, pm, sig, roc, sigy)\n')
    py_file.write('res_file = open(\'result.txt\', \'w\')\n')
    py_file.write('res_file.write(res_str)\n')
    py_file.write('res_file.close()\n')
    py_file.close()
    
def write_bash(source_dir, var): 
    sh_file = open('job.sh', 'w')
    # initial stuff    
    sh_file.write('#!/bin/bash\n')
    sh_file.write('export X509_USER_PROXY=/user/svanputt/.proxy\n')
    sh_file.write('voms-proxy-info\n')
    scram_arch = os.popen('echo $SCRAM_ARCH').read().replace('\n', '')
    sh_file.write('export SCRAM_ARCH='+scram_arch+'\n')
    sh_file.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
    sh_file.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
    sh_file.write('cd '+source_dir+'/../../\n')
    sh_file.write('eval `scramv1 ru -sh`\n')
    sh_file.write('ulimit -c 0\n')
    sh_file.write('cd $TMPDIR \n')
    sh_file.write('\n')

    # get python and run
    sh_file.write('cp -r '+os.getcwd()+' .\n')
    sh_file.write('ls -l\n')
    sh_file.write('cd '+var+'\n')
    sh_file.write('ls -l\n')
    #sh_file.write('rm -rf *_DNN_*\n')
    sh_file.write('cp '+source_dir+'/analyze.py .\n')
    sh_file.write('cp '+source_dir+'/runDNN.py .\n')
    sh_file.write('python job.py\n') 
    sh_file.write('ls -l\n')
    sh_file.write('\n')

    # move output back
    sh_file.write('cd ../\n')
    sh_file.write('cp -r '+var+' '+os.getcwd()+'/../\n')
    #sh_file.write('cp result.txt '+os.getcwd()+'/.\n')
    #sh_file.write('cp rootfiles/* '+os.getcwd()+'/rootfiles/.\n')
    sh_file.close()
    os.system('chmod +x job.sh')

def write_cfg(source_dir, template_file, var_str):
    template = open(source_dir+'/'+template_file, 'r')
    template_lines = template.readlines()
    template.close()
    
    cfg_file = open('cfg.py', 'w')
    #check_str = '#BATCH_SIZE'
    check_str = '#MODEL_FILE'
    for line in template_lines:
        if check_str in line:
            cfg_file.write(line.replace(check_str, var_str))
        else: cfg_file.write(line)
    cfg_file.close()

def write_collect(start_dir):
    pwd = os.getcwd()
    os.chdir(start_dir)
    co_file = open('collect.py', 'w')
    # imports
    co_file.write('import os\n') 
    co_file.write('from analyze import tree_sort\n')
    co_file.write('from operator import itemgetter\n') 
    co_file.write('\n')

    # results file   
    co_file.write('path = \''+os.getcwd()+'\'\n')
    co_file.write('result_file = open(path+\'/results.txt\', \'w\')\n')
    co_file.write('open_str = \'{:30}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\n\'.format(\'Variable\', \'KS signal\', \'KS backgr\', \'min KS\', \'Max Significance\', \'ROC Area\', \'Sig Area\')\n')
    co_file.write('result_file.write(open_str)\n')
    co_file.write('\n')

    # dirs  
    co_file.write('dirs = os.listdir(path)\n')
    co_file.write('dirs.sort()\n')
    co_file.write('tree_l = []\n')
    co_file.write('psl_l = []\n')
    co_file.write('pbl_l = []\n')
    co_file.write('pml_l = []\n')
    co_file.write('sig_l = []\n')
    co_file.write('roc_l = []\n')
    co_file.write('for dir in dirs:\n')
    co_file.write('\n')
    co_file.write('    if not os.path.isdir(path+\'/\'+dir): continue\n')
    co_file.write('    res_file = open(path+\'/\'+dir+\'/result.txt\', \'r\')\n')
    co_file.write('    lines = res_file.readlines()\n')
    co_file.write('    res_file.close()\n')
    co_file.write('\n')
    co_file.write('    for line in lines:\n')
    co_file.write('        line_sp = line.replace(\' \', \'\').split(\'\t\')\n')
    co_file.write('        if len(line_sp) == 7:\n')
    co_file.write('            var = line_sp[0]\n')
    co_file.write('            sig_ks  = float(line_sp[1])\n')
    co_file.write('            bck_ks  = float(line_sp[2])\n')
    co_file.write('            min_ks  = float(line_sp[3])\n')
    co_file.write('            max_sig = float(line_sp[4])\n')
    co_file.write('            roc_a   = float(line_sp[5])\n')
    co_file.write('            sig_a   = float(line_sp[6])\n')
    co_file.write('            break\n')
    co_file.write('    tree_l.append(var)\n')
    #co_file.write('    tree_l.append(int(var.replace(\'Trees\', \'\')))\n')
    co_file.write('    psl_l.append(sig_ks)\n')
    co_file.write('    pbl_l.append(bck_ks)\n')
    co_file.write('    pml_l.append(min_ks)\n')
    co_file.write('    sig_l.append(sig_a)\n')
    co_file.write('    roc_l.append(roc_a)\n')
    co_file.write('    var_str = \'{:30}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\t{:20}\\n\'.format(var, str(sig_ks), str(bck_ks), str(min_ks), str(max_sig), str(roc_a), str(sig_a))\n')
    co_file.write('    result_file.write(var_str)\n')
    co_file.write('\n')

    # plot str
    co_file.write('psl_l = tree_sort(tree_l, psl_l)\n')
    co_file.write('pbl_l = tree_sort(tree_l, pbl_l)\n')
    co_file.write('pml_l = tree_sort(tree_l, pml_l)\n')
    co_file.write('sig_l = tree_sort(tree_l, sig_l)\n')
    co_file.write('roc_l = tree_sort(tree_l, roc_l)\n')
    co_file.write('tree_l = tree_sort(tree_l, tree_l)\n')
    co_file.write('result_file.write(\'\\n\')\n')
    co_file.write('result_file.write(\'tree_l = [\'+\', \'.join([str(t) for t in tree_l])+\']\\n\')\n')
    co_file.write('result_file.write(\'psl_l = [\'+\', \'.join([str(t) for t in psl_l])+\']\\n\')\n')
    co_file.write('result_file.write(\'pbl_l = [\'+\', \'.join([str(t) for t in pbl_l])+\']\\n\')\n')
    co_file.write('result_file.write(\'pml_l = [\'+\', \'.join([str(t) for t in pml_l])+\']\\n\')\n')
    co_file.write('result_file.write(\'sig_l = [\'+\', \'.join([str(t) for t in sig_l])+\']\\n\')\n')
    co_file.write('result_file.write(\'roc_l = [\'+\', \'.join([str(t) for t in roc_l])+\']\\n\')\n')

    # get max KSmin idx
    co_file.write('result_file.write(\'\\n\')\n')
    co_file.write('maxKS_idx = max(enumerate(pml_l), key=itemgetter(1))[0]\n')
    co_file.write('result_file.write(\'maxKS : \'+str(pml_l[maxKS_idx])+\'\\n\')\n')
    co_file.write('result_file.write(\'sig   : \'+str(sig_l[maxKS_idx])+\'\\n\')\n')
    co_file.write('result_file.write(\'roc   : \'+str(roc_l[maxKS_idx])+\'\\n\')\n')
    co_file.write('result_file.write(\'batch : \'+str(tree_l[maxKS_idx])+\'\\n\')\n')
    co_file.write('result_file.close()\n')
    co_file.write('\n')
    os.chdir(pwd)

def mkDirs(nBS, template_file):
    source_dir = os.getcwd()
 
    #template_split = template_file.split('_')
    #nVars_dir = template_split[0] + '_' +template_split[1] +'_'+str(len(Vars))+'vars_trees'
    nVars_dir = '2HDMa_L2Reg_var'
    #nVars_dir = '2HDMa_Model_var'
    if not os.path.isdir(nVars_dir): os.system('mkdir '+nVars_dir)
    os.system('cp analyze.py '+nVars_dir+'/analyze.py')
    os.chdir(nVars_dir)

    for bs in nBS:
        #bs_str = str(bs)+'BS'
        bs_str = str(bs)

        model_path = '\''+source_dir+'/models/'+bs+'.py\''

        #if os.path.isdir(bs_str): os.system('rm -rf '+bs_str) 
        #os.system('mkdir '+bs_str)
        if not os.path.isdir(bs_str): os.system('mkdir '+bs_str)
        #os.system('mkdir '+bs_str+'/rootfiles')

        os.chdir(bs_str)
        #write_cfg(source_dir, template_file, str(bs))
        write_cfg(source_dir, template_file, model_path)
        write_bash(source_dir, str(bs))
        write_python(source_dir, str(bs))
        os.chdir('../')
    os.chdir('../')
    
    return nVars_dir    

def run(nBS, template):
    print('[run] making dirs and writing files')
    base_dir = mkDirs(nBS, template)
    print('[run] starting submissions')
    sub(base_dir, nBS)
    print('[run] write collection file')
    write_collect(base_dir)

def sub(start_dir, new_jobs):
    queue='localgrid@cream02'
    QSOPT='-l walltime=168:00:00'
    source_dir = os.getcwd()
    if os.path.isdir('job/'+start_dir): os.system('rm -rf job/'+start_dir)
    os.system('mkdir job/'+start_dir)
    hits = os.listdir(source_dir+'/'+start_dir)
    for hit in hits:
        path = source_dir+'/'+start_dir+'/'+hit
        if not os.path.isdir(path): continue
        submit = False
        for job in new_jobs:
            if str(job) in hit: 
                submit = True
                break
        if not submit: continue
        print('[sub] submitting '+hit)
        nTry=0
        jName = start_dir+'_'+hit
        outFile = 'job/'+start_dir+'/'+hit+'.out' 
        errFile = 'job/'+start_dir+'/'+hit+'.err'
        jobFile = path+'/job.sh'  

        while nTry < 3 : 
            nTry += 1
            jobid = os.system('qsub '+QSOPT+' -N '+jName+' -q '+queue+' -o '+outFile+' -e '+errFile+' '+jobFile)
            print('[sub] attempt: '+str(nTry)+'--> return : '+str(jobid))
            if jobid == 0 : nTry = 999

# Batch size
#nBS = [10, 20, 50, 100, 200, 400, 800]
#run(nBS, 'template_bsvar_cfg.py')

# models
#models = ['176x88x44ReluGNormal10Drop', '352x176x88ReluGNormal10Drop', '44x22x11ReluGNormal10Drop', '484x242x121ReluGNormal10Drop', '88x44x22ReluGNormal10Drop']
#models = ['176x88x44ReluGNormal20Drop', '352x176x88ReluGNormal20Drop', '44x22x11ReluGNormal20Drop', '484x242x121ReluGNormal20Drop', '88x44x22ReluGNormal20Drop', '176x88x44ReluGNormal30Drop', '352x176x88ReluGNormal30Drop', '44x22x11ReluGNormal30Drop', '484x242x121ReluGNormal30Drop', '88x44x22ReluGNormal30Drop']
#models = ['44x22x11ReluGNormal15Drop', '44x22x11ReluGNormal25Drop']
#models = ['22x11x5ReluGNormal10Drop', '22x11x5ReluGNormal20Drop', '22x11x5ReluGNormal20Drop']
#models = ['22x11x5ReluGNormal30Drop', '22x11x5ReluGNormal00Drop', '88x44x22ReluGNormal40Drop', '88x44x22ReluGNormal50Drop']
#models = ['176x88x44ReluGNormal20DropL1reg0p5', '352x176x88ReluGNormal20DropL1reg0p5', '44x22x11ReluGNormal20DropL1reg0p5', '484x242x121ReluGNormal20DropL1reg0p5', '88x44x22ReluGNormal20DropL1reg0p5']
#models = ['44x22x11ReluGNormal20DropL1reg0p01', '44x22x11ReluGNormal20DropL1reg0p05', '44x22x11ReluGNormal20DropL1reg0p1', '44x22x11ReluGNormal20DropL1reg0p5']
models = ['484ReluGNormal', '484ReluGNormalL2reg0p01', '484ReluGNormalL2reg0p05', '484ReluGNormalL2reg0p1', '484ReluGNormal20Drop', '484ReluGNormalWcon']
#models = ['484ReluGNormalWcon']
run(models, 'template_model_cfg.py')


