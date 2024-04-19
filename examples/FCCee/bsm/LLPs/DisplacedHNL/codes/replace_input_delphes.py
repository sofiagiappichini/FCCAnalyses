import os
import shutil

# Define the original sample name and the replacement sample names
original_name = "HNL_2.86e-9_70gev"
replacement_words = [
    'HNL_4e-10_10gev',
    #'HNL_1.33e-7_10gev',
    'HNL_2.86e-12_10gev',
    #'HNL_5e-12_10gev',
    #'HNL_6.67e-10_10gev',
    #'HNL_2.86e-7_10gev',
]

# Create a backup directory if it doesn't exist
backup_dir = "backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Backup the original file
shutil.copy("pythia_proc.cmd", os.path.join(backup_dir, "pythia_proc_backup_original.cmd"))

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
    os.system("source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh && DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl {} /eos/user/s/sgiappic/2HNL_samples/root/{}.root".format(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)), replacement_word))
    
    # Remove the temporary backup file
    os.remove(os.path.join(backup_dir, "pythia_proc_backup_{}.cmd".format(replacement_word)))

