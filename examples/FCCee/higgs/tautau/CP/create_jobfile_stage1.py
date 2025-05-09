import os
from math import ceil

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
    base_cfg = 'Universe          = docker\n'
    base_cfg += 'docker_image     = cverstege/alma9-gridjob\n'
    base_cfg += 'accounting_group = cms.higgs\n'
    base_cfg += 'output_dir       = ' + output_dir + '\n'
    base_cfg += 'executable       = $(filename)\n'
    base_cfg += 'log              = $(output_dir)log/condor_$(ClusterId).$(ProcId).log\n'
    base_cfg += 'output           = $(output_dir)out/condor_$(ClusterId).$(ProcId).out\n'
    base_cfg += 'error            = $(output_dir)err/condor_$(ClusterId).$(ProcId).err\n'
    base_cfg += 'max_retries      = 3\n'
    base_cfg += '+JobFlavor       = "espresso"\n'
    base_cfg += 'request_memory   = ' + str(memory) + ' MB\n'
    base_cfg += 'request_cpus     = ' + str(nCPUs) + '\n'
    base_cfg += 'requirements     = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'
    base_cfg += 'should_transfer_files   = IF_NEEDED\n'
    base_cfg += 'when_to_transfer_output = ON_EXIT\n\n'

    if chunks:
        for process in processList:
            job_cfg = base_cfg
            job_dir = output_dir + process + '/'
            sh_files = [f for f in os.listdir(job_dir) if f.endswith('.sh')]
            job_cfg += 'queue filename from (\n'
            job_cfg += '\n'.join(['  ' + job_dir + f for f in sh_files])
            job_cfg += '\n)\n'

            with open(job_dir + 'job_submit.cfg', 'w') as sub:
                sub.write(job_cfg)
    else:
        job_cfg = base_cfg
        sh_files = [f for f in os.listdir(output_dir) if f.endswith('.sh')]
        job_cfg += 'queue filename from (\n'
        job_cfg += '\n'.join(['  ' + output_dir + f for f in sh_files])
        job_cfg += '\n)\n'

        with open(output_dir + 'job_submit.cfg', 'w') as sub:
            sub.write(job_cfg)

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

    if chunks:

        for process in processList:
            j = 0
            files = os.listdir(input_dir + process)
            num_files = len(files)
            num_chunks = ceil(num_files / 20)  # Calculate the number of chunks (20 files per chunk)

            for chunk_idx in range(num_chunks):
                make_dir_if_not_exists(output_dir + process)
                # Collect up to 20 files for this chunk
                chunk_files = files[chunk_idx * 20:(chunk_idx + 1) * 20]
                files_list = ' '.join([input_dir + process + '/' + file for file in chunk_files])

                # Generate the submission script
                scr  = '#!/bin/bash\n\n'
                scr += 'source ' + source_dir + 'setup.sh\n\n'
                scr += 'cd ' + local_dir + '\n\n'
                scr += 'fccanalysis run ' + ananame + ' --batch '
                scr += f' --output ' + output_ana + process + '/' + 'chunk_' + str(chunk_idx) + '.root --files-list ' + files_list
                scr += '\n\n'

                # Write the script to a file
                script_path = output_dir + process + '/submit_chunk_' + str(chunk_idx) + '.sh'
                with open(script_path, 'w') as sh:
                    sh.write(scr)
                print(f"SUBMISSION FILE CREATED: {process}, chunk {chunk_idx}")
    
    else:

        for process in processList:
            scr  = '#!/bin/bash\n\n'
            scr += 'source ' + source_dir + 'setup.sh\n\n'
            scr += 'cd ' + local_dir + '\n\n'
            scr += 'fccanalysis run ' + ananame + ' --batch '
            scr += f' --output  ' + output_ana + process + '.root --files-list  ' + input_dir + process + '.root'
            scr += '\n\n'     
            with open(output_dir+'submit_'+process+'.sh', 'w') as sh:
                sh.write(scr)
        print("done")

def submit_jobs(output_dir: str):
    for process in processList:
        dir = output_dir + process 
        num_files = len(os.listdir(dir))-1
        os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
        #print(f"GOOD SUBMISSION: {process} with {num_files} chunks")
             

processList_ = {
    #'noISR_e+e-_noCuts_EWonly':{},
    #'noISR_e+e-_noCuts_cehim_m1':{},
    #'noISR_e+e-_noCuts_cehim_p1':{},
    #'noISR_e+e-_noCuts_cehre_m1':{},
    #'noISR_e+e-_noCuts_cehre_p1':{},
    
    'EWonly_taudecay_2Pi2Nu':{},
    'cehim_m1_taudecay_2Pi2Nu':{},
    'cehim_p1_taudecay_2Pi2Nu':{},
    'cehre_m1_taudecay_2Pi2Nu':{},
    'cehre_p1_taudecay_2Pi2Nu':{},

    #'cehim_m5_taudecay_2Pi2Nu':{},
    #'cehim_p5_taudecay_2Pi2Nu':{},
    #'cehre_m5_taudecay_2Pi2Nu':{},
    #'cehre_p5_taudecay_2Pi2Nu':{},

    'EWonly_taudecay_PiPi0Nu':{},
    'cehim_m1_taudecay_PiPi0Nu':{},
    'cehim_p1_taudecay_PiPi0Nu':{},
    'cehre_m1_taudecay_PiPi0Nu':{},
    'cehre_p1_taudecay_PiPi0Nu':{},

    #"e+e-_qqH_Htautau":{},
    "e+e-_qqH_H2Pi2Nu":{},

    #'cehim_m2_taudecay_2Pi2Nu':{},
    #'cehim_p2_taudecay_2Pi2Nu':{},
    #'cehre_m2_taudecay_2Pi2Nu':{},
    #'cehre_p2_taudecay_2Pi2Nu':{},

    #'cehim_p0p1_taudecay_2Pi2Nu':{},
    #'cehim_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_p0p1_taudecay_2Pi2Nu':{},

    #'cehim_p10_taudecay_2Pi2Nu':{},
    #'cehim_m10_taudecay_2Pi2Nu':{},

    #'wzp6_ee_eeH_Htautau_ecm240': {},
    #'p8_ee_ZZ_ecm240':{'chunks':100},
}

processList = {
    #'e+e-_eeH_H3PiNu':{},
    #'wzp6_ee_bbH_Htautau_ecm240':{},
    #'EWonly_taudecay_CPodd_2Pi2Nu':{},
    'p8_ee_ZZ_ecm240'
    #"p8_ee_llH_Hpinu_even":{},
    #"p8_ee_llH_Hpinu_odd":{},
}

chunks = True

#inputDir = "/ceph/mpresill/FCCee/ZH_SMEFT_LO_noISR_noCuts_prod/ele/"
#inputDir = "/ceph/sgiappic/HiggsCP/"
inputDir = "/ceph/sgiappic/HiggsCP/winter23/"
output = '/work/sgiappic/HTCondor/stage1_CPnew_ZZ/' ##output directory of submission files, needs to be different to have unique submission files
outputDir = "/ceph/sgiappic/HiggsCP/tutorial/stage1/" ##output directory of stage2 samples
localDir = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/CP/'
sourceDir = '/ceph/sgiappic/FCCAnalyses/'
Filename = 'analysis_stage1.py'

nCPUS = 1
Memory = 10000

create_subjob_script(localDir, sourceDir, inputDir, output, outputDir, Filename)

create_condor_config(nCPUS, Memory, output)

submit_jobs(output)