import os

def Make_workspace(jobdir):

    if not os.path.exists(jobdir):
            os.system(f"mkdir -p {jobdir}")
     
def create_condor_config(local_dir: str,
                         nCPUs: int,
                         memory: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''
    cfg = 'Universe          = docker\n'

    cfg += 'docker_image     = cverstege/alma9-base\n'

    cfg += 'accounting_group = cms.higgs \n'

    cfg += 'output_dir       = '+output_dir+'\n'

    cfg += 'executable       = $(filename)\n'

    cfg += 'log              = $(output_dir)log/condor_$(ClusterId).$(ProcId).log\n'

    cfg += 'output           = $(output_dir)out/condor_$(ClusterId).$(ProcId).out\n'

    cfg += 'error            = $(output_dir)err/condor_$(ClusterId).$(ProcId).err\n'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "espresso"\n'

    cfg += 'request_memory   = '+str(memory)+' MB\n'

    cfg += 'request_cpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'

    cfg += 'should_transfer_files   = IF_NEEDED\n'

    cfg += 'when_to_transfer_output  = ON_EXIT\n'

    cfg += 'queue filename matching files'
 
    with open('submit.sub', 'w') as sub:
        sub.write(cfg)
        for file in os.listdir('/work/awiedl/'):
            filename = os.fsdecode(file)
            if filename.endswith('.sh'):
                sub.write(f' ' + '/work/awiedl/' + filename)

# _____________________________________________________________________________
def create_subjob_script(local_dir: str,
                         source_dir: str,
                         input_dir: str,
                         output_dir: str,
                         processList: dict,
                         ananame: str):
    '''
    Creates sub-job script to be run.
    '''
    submit_list = []
    for process in processList:
        if not os.path.exists(output_dir+process):
            os.system(f"mkdir -p {output_dir+process}")            
        if not os.path.exists(output_dir+'err'):
            os.system(f"mkdir -p {output_dir+'err'}")            
        if not os.path.exists(output_dir+'log'):
            os.system(f"mkdir -p {output_dir+'log'}")            
        if not os.path.exists(output_dir+'out'):
            os.system(f"mkdir -p {output_dir+'out'}")            
        i = 0
        j = 0
        num_files = len(os.listdir(input_dir+process))
        g = '' 
        for file in os.listdir(input_dir+process):            
            g += input_dir + process + '/' + file + ' '
            i+=1
            if(i%10==0 or i==num_files):
                scr  = '#!/bin/bash\n\n'
                scr += 'source ' + source_dir + 'setup.sh\n\n'
                scr += 'cd ' + local_dir + '\n\n'
                scr += 'fccanalysis run ' + ananame + ' --batch '
                scr += f' --output  ' + output_dir + process + '/chunk_'+str(j)+'.root --files-list  ' + g
                scr += '\n\n'     
                with open('submit_'+process+'_chunk'+str(j)+'.sh', 'w') as sh:
                    sh.write(scr)
                g = ''
                j+=1
             

processList = {
#    'ZH_EW_LO__prod':{}, #testing sample, 50.000 Events
    
    'p8_ee_ZZ_ecm240':{'chunks':565},
    'p8_ee_Zqq_ecm240':{'chunks':1007},
    'p8_ee_WW_ecm240':{'chunks':3740},
    'wzp6_ee_tautau_ecm240':{'chunks':524},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':100},
    'wzp6_ee_mumu_ecm240':{'chunks':100},
    'wzp6_ee_nuenueZ_ecm240':{'chunks':20},
    'wzp6_egamma_eZ_Zee_ecm240':{'chunks':60},
    'wzp6_egamma_eZ_Zmumu_ecm240':{'chunks':60},
    'wzp6_gaga_ee_60_ecm240':{'chunks':225},
    'wzp6_gaga_mumu_60_ecm240':{'chunks':339},
    'wzp6_gaga_tautau_60_ecm240':{'chunks':337},
    'wzp6_gammae_eZ_Zee_ecm240':{'chunks':60},
    'wzp6_gammae_eZ_Zmumu_ecm240':{'chunks':56},

    'wzp6_ee_mumuH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_eeH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_Htautau_ecm240':{'chunks':12},
    'wzp6_ee_bbH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_ccH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_ssH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_qqH_Htautau_ecm240':{'chunks':2},

    'wzp6_ee_mumuH_Hbb_ecm240':{'chunks':3},
    'wzp6_ee_eeH_Hbb_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_Hbb_ecm240':{'chunks':12},
    'wzp6_ee_bbH_Hbb_ecm240':{'chunks':1},
    'wzp6_ee_ccH_Hbb_ecm240':{'chunks':2},
    'wzp6_ee_ssH_Hbb_ecm240':{'chunks':2},
    'wzp6_ee_qqH_Hbb_ecm240':{'chunks':5},

    'wzp6_ee_mumuH_Hcc_ecm240':{'chunks':4},
    'wzp6_ee_eeH_Hcc_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_Hcc_ecm240':{'chunks':11},
    'wzp6_ee_bbH_Hcc_ecm240':{'chunks':4},
    'wzp6_ee_ccH_Hcc_ecm240':{'chunks':4},
    'wzp6_ee_ssH_Hcc_ecm240':{'chunks':3},
    'wzp6_ee_qqH_Hcc_ecm240':{'chunks':2},

    'wzp6_ee_mumuH_HWW_ecm240':{'chunks':4},
    'wzp6_ee_eeH_HWW_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_HWW_ecm240':{'chunks':12},
    'wzp6_ee_bbH_HWW_ecm240':{'chunks':10},
    'wzp6_ee_ccH_HWW_ecm240':{'chunks':12},
    'wzp6_ee_ssH_HWW_ecm240':{'chunks':12},
    'wzp6_ee_qqH_HWW_ecm240':{'chunks':11},

    'wzp6_ee_mumuH_HZZ_ecm240':{'chunks':4},
    'wzp6_ee_eeH_HZZ_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_HZZ_ecm240':{'chunks':12},
    'wzp6_ee_bbH_HZZ_ecm240':{'chunks':10},
    'wzp6_ee_ccH_HZZ_ecm240':{'chunks':12},
    'wzp6_ee_ssH_HZZ_ecm240':{'chunks':6},
    'wzp6_ee_qqH_HZZ_ecm240':{'chunks':12},

    'wzp6_ee_mumuH_Hgg_ecm240':{'chunks':4},
    'wzp6_ee_eeH_Hgg_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_Hgg_ecm240':{'chunks':12},
    'wzp6_ee_bbH_Hgg_ecm240':{'chunks':2},
    'wzp6_ee_ccH_Hgg_ecm240':{'chunks':4},
    'wzp6_ee_ssH_Hgg_ecm240':{'chunks':4},
    'wzp6_ee_qqH_Hgg_ecm240':{'chunks':4},
    
    'wzp6_ee_mumuH_Hss_ecm240':{'chunks':4},
    'wzp6_ee_eeH_Hss_ecm240':{'chunks':4},
    'wzp6_ee_nunuH_Hss_ecm240':{'chunks':11},
    'wzp6_ee_bbH_Hss_ecm240':{'chunks':4},
    'wzp6_ee_ccH_Hss_ecm240':{'chunks':3},
    'wzp6_ee_ssH_Hss_ecm240':{'chunks':3},
    'wzp6_ee_qqH_Hss_ecm240':{'chunks':4},

    'wzp6_ee_tautauH_HWW_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_HZZ_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_Hbb_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_Hcc_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_Hss_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_Htautau_ecm240':{'chunks':4},
    'wzp6_ee_tautauH_Hgg_ecm240':{'chunks':4},
}

#inputDir = '/ceph/sgiappic/HiggsCP/winter23/'
inputDir = '/ceph/awiedl/FCCee/HiggsCP/stage1/'
outputDir = '/ceph/awiedl/FCCee/HiggsCP/stage2/NuNu/HH/'
localDir = '/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/NuNu/'
sourceDir = '/work/awiedl/FCCAnalyses/'
Filename = 'analysis_stage2_NuNuHH.py'
nCPUS = 4
Memory = 10000

create_subjob_script(localDir, sourceDir, inputDir, outputDir, processList, Filename)
create_condor_config(localDir, nCPUS, Memory, outputDir)
