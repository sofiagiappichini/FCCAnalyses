import os

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")

def Make_workspace(jobdir):

    if not os.path.exists(jobdir):
            os.system(f"mkdir -p {jobdir}")
     
def create_condor_config(nCPUs: int,
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

    cfg += '+JobFlavour      = "longlunch"\n'

    cfg += 'request_memory   = '+str(memory)+' MB\n'

    cfg += 'request_cpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'

    cfg += 'should_transfer_files   = IF_NEEDED\n'

    cfg += 'when_to_transfer_output  = ON_EXIT\n'

    cfg += 'queue filename matching files'
 
    with open(output_dir+'job_submit.cfg', 'w') as sub:
        sub.write(cfg)
        for file in os.listdir(output_dir):
            #if "NuNuLL" in file:
                filename = os.fsdecode(file)
                if filename.endswith('.sh'):
                    sub.write(f' ' + output_dir + filename)

# _____________________________________________________________________________
def create_subjob_script(local_dir: str,
                         source_dir: str,
                         input_dir: str,
                         output_dir: str,
                         output_ana: str,
                         ananame: str):
    '''
    Creates sub-job script to be run.
    '''

    make_dir_if_not_exists(output_dir)
    make_dir_if_not_exists(output_dir+"out")
    make_dir_if_not_exists(output_dir+"log")
    make_dir_if_not_exists(output_dir+"err")

    for process in processList:
        #print(process)
        i = 0
        j = 0
        num_files = len(os.listdir(input_dir+process))
        #processList['process']['chunks']
        g = '' 
        for file in os.listdir(input_dir+process):           
            #print(file) 
            g += input_dir + process + '/' + file + ' '
            i+=1
            if(i%10==0 or i==num_files):
                scr  = '#!/bin/bash\n\n'
                scr += 'source ' + source_dir + 'setup.sh\n\n'
                scr += 'cd ' + local_dir + '\n\n'
                scr += 'fccanalysis run ' + ananame + ' --batch '
                scr += f' --output  ' + output_ana + process + '/' + 'chunk_'+str(j)+'.root --files-list  ' + g
                scr += '\n\n'     
                with open(output_dir+'submit_'+process+'_chunk'+str(j)+'.sh', 'w') as sh:
                    sh.write(scr)
                g = ''
                j+=1
    print("done")
             

processList_ = {
    'p8_ee_WW_ecm240':{'chunks':100},
    'p8_ee_Zqq_ecm240':{'chunks':100},
    'p8_ee_ZZ_ecm240':{'chunks':100},
    
    'wzp6_ee_tautau_ecm240':{'chunks':100},
    'wzp6_ee_mumu_ecm240':{'chunks':100},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':100},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':1},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':100},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':100},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':100},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':100},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':100},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':100},
    'wzp6_gaga_ee_60_ecm240': {'chunks':100},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':100},

    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':1},
}
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':1},
}

inputDir = "/ceph/sgiappic/HiggsCP/winter23/"
output = '/work/sgiappic/HTCondor/stage1_eff/' ##output directory of submission files, needs to be different to have unique submission files
outputDir = '/ceph/awiedl/FCCee/HiggsCP/stage1_eff/' ##output directory of stage2 samples
localDir = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/'
sourceDir = '/ceph/sgiappic/FCCAnalyses/'
Filename = 'analysis_stage1_eff.py'

nCPUS = 4
Memory = 10000

create_subjob_script(localDir, sourceDir, inputDir, output, outputDir, Filename)

create_condor_config(nCPUS, Memory, output)