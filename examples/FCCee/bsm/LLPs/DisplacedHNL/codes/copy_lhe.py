import os
import shutil

replacement_samples = [
    #"HNL_2.78e-8",
    #"HNL_6.05e-9",
    "HNL_5.97e-9",
    "HNL_1.30e-9",
    #"HNL_8.35e-9",
    #"HNL_1.81e-9",
    #"HNL_1.04e-8",
    "HNL_2.27e-9",
    #"HNL_1.39e-8",
    #"HNL_3.02e-9",
    "HNL_5.97e-8",
    #"HNL_1.30e-8",


]

replacement_run =[
    "run_01",
    "run_02",
    "run_03",
    "run_04",
    "run_05",
    "run_06",
    "run_07",
    "run_08",
]

run_dict ={
    "run_01":"10gev",
    "run_02":"20gev",
    "run_03":"30gev",
    "run_04":"40gev",
    "run_05":"50gev",
    "run_06":"60gev",
    "run_07":"70gev",
    "run_08":"80gev",
}

# Loop through each replacement word
for replacement_word in replacement_samples:
    for run in replacement_run:
        file_name =  replacement_word+"_"+run_dict[run]
        #change lhe file name to match 
        os.system("mv /eos/user/s/sgiappic/2HNL_prod/{}/Events/{}/unweighted_events.lhe.gz /eos/user/s/sgiappic/2HNL_prod/{}/Events/{}/{}.lhe.gz".format(replacement_word, run, replacement_word, run, file_name))
        #move lhe to directory
        os.system("cp /eos/user/s/sgiappic/2HNL_prod/{}/Events/{}/{}.lhe.gz /eos/user/s/sgiappic/2HNL_samples/lhe/".format(replacement_word, run, file_name))
        #unzip it
        os.system("gzip -d /eos/user/s/sgiappic/2HNL_samples/lhe/*gz")
        
        print("{}/{} processed".format(replacement_word, run))