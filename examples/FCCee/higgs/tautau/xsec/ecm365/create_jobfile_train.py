import os

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")
     
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
                         output_dir: str):
    '''
    Creates sub-job script to be run.
    '''

    make_dir_if_not_exists(output_dir+"/err")
    make_dir_if_not_exists(output_dir+"/log")
    make_dir_if_not_exists(output_dir+"/out")

    for tag in TAG:
        for cat in CAT:
            for sub in SUBDIR:

                scr  = '#!/bin/bash\n\n'
                scr += 'source /ceph/sgiappic/FCCAnalyses/setup.sh\n\n'
                scr += 'python ' + local_dir + tag + '/' + '/train_bdt_' + cat + sub + '.py' 
                with open(output_dir+'submit_'+tag+'_'+cat+sub+'.sh', 'w') as sh:
                    sh.write(scr)
                print(f"done {tag} {cat+sub}")

def submit_jobs(output_dir: str):
    #for process in processList:
        dir = output_dir #+ process 
        num_files = len(os.listdir(dir))-1
        os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
             
output = '/work/sgiappic/HTCondor/BDT_train_365/' ##output directory of submission files
localDir = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/training/'

SUBDIR = [
    'LL',
    'LH',
    'HH',
]

CAT = [
    "QQ",
    #"LL",
    "NuNu",
]

TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
]

nCPUS = 1
Memory = 10000

create_subjob_script(localDir, output)

create_condor_config(nCPUS, Memory, output)

submit_jobs(output)