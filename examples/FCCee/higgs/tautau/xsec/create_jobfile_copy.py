import os

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")
     
def create_condor_config(nCPUs: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''

    cfg = 'executable       = $(filename)\n'

    cfg += 'Log              = '+output_dir+process+'/condor_job.$(ClusterId).$(ProcId).log\n'

    cfg += 'Output           = '+output_dir+process+'/condor_job.$(ClusterId).$(ProcId).out\n'

    cfg += 'Error            = '+output_dir+process+'/condor_job.$(ClusterId).$(ProcId).err\n'

    cfg += 'getenv           = False\n'

    cfg += 'environment      = "LS_SUBCWD={log_dir}"'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "longlunch"\n'

    cfg += '+AccountingGroup = "group_u_FCC.local_gen"\n'

    cfg += 'RequestCpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = ( (OpSysAndVer =?= "AlmaLinux9") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n'

    cfg += 'on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n'

    cfg += 'queue filename matching files'
 
    for process in processList:
        with open(output_dir + process + '/job_submit.cfg', 'w') as sub:
            sub.write(cfg)
            for file in os.listdir(output_dir + process):
                filename = os.fsdecode(file)
                if filename.endswith('.sh'):
                    sub.write(f' ' + output_dir + process + '/' + filename)

# _____________________________________________________________________________
def create_subjob_script(
                         input_dir: str,
                         output_dir: str,):
    '''
    Creates sub-job script to be run.
    '''

    for process in processList:
        j = 0
        for file in os.listdir(input_dir+process):   
            scr  = '#!/bin/bash\n\n'
            scr += 'scp -r ' + input_dir + process + ' sgiappic@portal1.etp.kit.edu:/ceph/awiedl/FCCee/HiggsCP/stage1_241202/'
            scr += '\n\n'     
            with open(output_dir + process + '.sh', 'w') as sh:
                sh.write(scr)
            j+=1
            print(f"SUBMISSION FIlE CREATED: {process}")

def submit_jobs(output_dir: str):
    for process in processList:
        dir = output_dir + process 
        num_files = len(os.listdir(dir))-1
        #os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
        print(f"GOOD SUBMISSION: {process}")

             

processList = {
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',
    
    'wzp6_ee_tautau_ecm240',
    'wzp6_ee_mumu_ecm240',
    'wzp6_ee_ee_Mee_30_150_ecm240',

    'wzp6_ee_tautauH_Htautau_ecm240',
    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
    'wzp6_ee_tautauH_Hgg_ecm240',
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',

    'wzp6_egamma_eZ_Zmumu_ecm240',
    'wzp6_egamma_eZ_Zee_ecm240',
    'wzp6_gammae_eZ_Zmumu_ecm240',
    'wzp6_gammae_eZ_Zee_ecm240',

    'wzp6_gaga_tautau_60_ecm240',
    'wzp6_gaga_mumu_60_ecm240',
    'wzp6_gaga_ee_60_ecm240',

    'wzp6_ee_nuenueZ_ecm240',

    'wzp6_ee_nunuH_Htautau_ecm240',
    'wzp6_ee_nunuH_Hbb_ecm240',
    'wzp6_ee_nunuH_Hcc_ecm240',
    'wzp6_ee_nunuH_Hss_ecm240',
    'wzp6_ee_nunuH_Hgg_ecm240',
    'wzp6_ee_nunuH_HWW_ecm240',
    'wzp6_ee_nunuH_HZZ_ecm240',

    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
    'wzp6_ee_eeH_Hgg_ecm240',
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
    'wzp6_ee_mumuH_Hgg_ecm240',
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',

    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_Htautau_ecm240',
    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',

    'wzp6_ee_qqH_Htautau_ecm240',
    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
}

inputDir = "c"
output = '/afs/cern.ch/user/s/sgiappic/HTCondor/' ##output directory of submission files, needs to be different to have unique submission files

nCPUS = 2

create_subjob_script(inputDir, output)

create_condor_config(nCPUS, output)

submit_jobs(output)