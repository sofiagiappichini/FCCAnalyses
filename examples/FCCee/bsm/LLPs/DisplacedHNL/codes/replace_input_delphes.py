import os
import shutil

# Define the original sample name and the replacement sample names
original_name = "HNL_2.86e-9_70gev"
replacement_words_all = [
    #"HNL_1.33e-7_10gev",
    #"HNL_1.33e-7_20gev",
    #"HNL_1.33e-7_30gev",
    #"HNL_1.33e-7_40gev",
    #"HNL_1.33e-7_50gev",
    #"HNL_1.33e-7_60gev",
    #"HNL_1.33e-7_70gev",
    #"HNL_1.33e-7_80gev",

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    #"HNL_4e-10_10gev",
    #"HNL_4e-10_20gev",
    #"HNL_4e-10_30gev",
    #"HNL_4e-10_40gev",
    #"HNL_4e-10_50gev",
    #"HNL_4e-10_60gev",
    #"HNL_4e-10_70gev",
    #"HNL_4e-10_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    #"HNL_2.86e-12_10gev",
    #"HNL_2.86e-12_20gev",
    #"HNL_2.86e-12_30gev",
    #"HNL_2.86e-12_40gev",
    #"HNL_2.86e-12_50gev",
    #"HNL_2.86e-12_60gev",
    #"HNL_2.86e-12_70gev",
    #"HNL_2.86e-12_80gev",

    #inverted

    #"HNL_2.86e-7_10gev",
    #"HNL_2.86e-7_20gev",
    #"HNL_2.86e-7_30gev",
    #"HNL_2.86e-7_40gev",
    #"HNL_2.86e-7_50gev",
    #"HNL_2.86e-7_60gev",
    #"HNL_2.86e-7_70gev",
    #"HNL_2.86e-7_80gev",

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    #"HNL_6.67e-10_10gev",
    #"HNL_6.67e-10_20gev",
    #"HNL_6.67e-10_30gev",
    #"HNL_6.67e-10_40gev",
    #"HNL_6.67e-10_50gev",
    #"HNL_6.67e-10_60gev",
    #"HNL_6.67e-10_70gev",
    #"HNL_6.67e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",

    #"HNL_5e-12_10gev",
    #"HNL_5e-12_20gev",
    #"HNL_5e-12_30gev",
    #"HNL_5e-12_40gev",
    #"HNL_5e-12_50gev",
    #"HNL_5e-12_60gev",
    #"HNL_5e-12_70gev",
    #"HNL_5e-12_80gev",
    
]

replacement_words =[
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",
]

# Create a backup directory if it doesn't exist
backup_dir = "backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Backup the original file
shutil.copy("/afs/cern.ch/user/s/sgiappic/pythia_proc.cmd", os.path.join(backup_dir, "pythia_proc_backup_original.cmd"))

# Loop through each replacement word
for replacement_word in replacement_words:
    # Make a copy of the original backup file
    shutil.copy(os.path.join(backup_dir, "pythia_proc_backup_original.cmd"), os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)))
    
    # Perform substitution using sed within the loop
    with open(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)), "r") as file:
        file_data = file.read()
    file_data = file_data.replace(original_name, replacement_word)
    with open(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)), "w") as file:
        file.write(file_data)
    
    # Execute the DelphesPythia8_EDM4HEP command
    os.system("source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh && DelphesPythia8_EDM4HEP /afs/cern.ch/user/s/sgiappic/card_IDEA.tcl /afs/cern.ch/user/s/sgiappic/edm4hep_IDEA.tcl {} /eos/user/s/sgiappic/2HNL_samples/root/{}.root".format(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)), replacement_word))
    
    # Remove the temporary backup file
    os.remove(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)))

