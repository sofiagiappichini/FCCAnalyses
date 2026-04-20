import os

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")
     
def create_condor_config_lxplus(nCPUs: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''

    cfg = 'executable       = $(filename)\n'

    cfg += 'Log              = '+output_dir+'/log/condor_job.$(ClusterId).$(ProcId).log\n'

    cfg += 'Output           = '+output_dir+'/out/condor_job.$(ClusterId).$(ProcId).out\n'

    cfg += 'Error            = '+output_dir+'/err/condor_job.$(ClusterId).$(ProcId).err\n'

    cfg += 'getenv           = False\n'

    cfg += 'environment      = "LS_SUBCWD={log_dir}"\n'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "longlunch"\n'

    cfg += '+AccountingGroup = "group_u_FCC.local_gen"\n'

    cfg += 'RequestCpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = ( (OpSysAndVer =?= "AlmaLinux9") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n'

    cfg += 'on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n'

    cfg += 'queue filename matching files'
 
    #for process in processList:
    with open(output_dir + '/job_submit.cfg', 'w') as sub:
        sub.write(cfg)
        for file in os.listdir(output_dir ):
            filename = os.fsdecode(file)
            if filename.endswith('.sh'):
                sub.write(f' ' + output_dir + '/' + filename)

def create_condor_config_KIT(nCPUs: int,
                         memory: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''
    cfg = 'Universe          = docker\n'

    cfg += 'docker_image     = cverstege/alma9-gridjob\n'

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
 
    with open(output_dir + '/job_submit.cfg', 'w') as sub:
        sub.write(cfg)
        for file in os.listdir(output_dir):
            filename = os.fsdecode(file)
            if filename.endswith('.sh'):
                sub.write(f' ' + output_dir + filename)

# _____________________________________________________________________________
def create_subjob_script(
                         input_dir: str,
                         output_dir: str,):
    '''
    Creates sub-job script to be run.
    '''

    make_dir_if_not_exists(output_dir+"/err")
    make_dir_if_not_exists(output_dir+"/log")
    make_dir_if_not_exists(output_dir+"/out")

    for tag in TAG:
        for cat in CAT:
            for sub in SUB:

                #for process in processList:
                scr  = '#!/bin/bash\n\n'
                scr += "source /afs/cern.ch/user/s/sgiappic/FCCAnalyses/setup.sh\n\n"
                scr += f"fccanalysis final /afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/BDT/final-new/{tag}/analysis_final_{cat}{sub}.py"
                scr += '\n\n'     
                with open(output_dir + tag + cat + sub + '.sh', 'w') as sh:
                    sh.write(scr)
                print(f"SUBMISSION FIlE CREATED: {tag}")

def submit_jobs(output_dir: str):
    #for process in processList:
        dir = output_dir #+ process 
        num_files = len(os.listdir(dir))-1
        os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
        #print(f"GOOD SUBMISSION: {process}")

TAG = [
    "ktN-tag",
    "ktN-explicit",
]             

CAT = [
    #"QQ",
    #"NuNu",
    "LL",
]

SUB = [
    "LL",
    "LH",
    "HH",
]

inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"
output = '/afs/cern.ch/user/s/sgiappic/HTCondor/final_240_bdt_ll/' ##output directory of submission files, needs to be different to have unique submission files

nCPUS = 4
memory = 10000

create_subjob_script(inputDir, output)

create_condor_config_lxplus(nCPUS, output)

submit_jobs(output)