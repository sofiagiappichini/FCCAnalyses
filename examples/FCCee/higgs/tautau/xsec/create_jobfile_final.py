import os

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

    cfg += '+JobFlavour      = "espresso"\n'

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
                         cat_name: str,
                         sub_name:str,
                         output_dir: str,
                         output_ana: str,
                         ananame: str):
    '''
    Creates sub-job script to be run.
    '''
    submit_list = []
    if not os.path.exists(output_dir):
        os.system(f"mkdir -p {output_dir}")            
    if not os.path.exists(output_dir+'err'):
        os.system(f"mkdir -p {output_dir+'err'}")            
    if not os.path.exists(output_dir+'log'):
        os.system(f"mkdir -p {output_dir+'log'}")            
    if not os.path.exists(output_dir+'out'):
        os.system(f"mkdir -p {output_dir+'out'}")     
    scr  = '#!/bin/bash\n\n'
    scr += 'source ' + source_dir + 'setup.sh\n\n'
    scr += 'cd ' + local_dir + '\n\n'
    scr += 'fccanalysis final ' + ananame 
    with open(output_dir+'submit_'+cat_name+sub_name+'.sh', 'w') as sh:
        sh.write(scr)
    print("done")
             

#inputDir = '/ceph/sgiappic/HiggsCP/winter23/'
inputDir = '/ceph/awiedl/FCCee/HiggsCP/stage2_241025/'
output = '/work/sgiappic/HTCondor/final_241025/' ##output directory of submission files
outputDir_path = '/ceph/awiedl/FCCee/HiggsCP/final_241025_v2/' ##output directory of stage2 samples
localDir_path = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/'
sourceDir = '/ceph/sgiappic/FCCAnalyses/'
Filename_path = 'analysis_final_'
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
CAT = [
    "QQ",
    "LL",
    "NuNu",
]
nCPUS = 4
Memory = 10000
for cat in CAT:
    for sub in SUBDIR:
        localDir = localDir_path + cat + "/"
        outputDir = outputDir_path + cat + "/" + sub + "/"
        Filename = Filename_path + cat + sub + ".py"
        create_subjob_script(localDir, sourceDir, inputDir, cat, sub, output, outputDir, Filename)

create_condor_config(nCPUS, Memory, output)