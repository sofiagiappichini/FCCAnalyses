import os

dir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/lhe/mg_ee_eetata_smeft_cehim_p1_ecm240/"

pattern = f"{dir}/*.lhe.gz"
lhe_gz_files = glob.glob(pattern)

for file in lhe_gz_files:
    os.system(f"gzip -d {file}")

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

    os.system("gzip /eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe".format(replacement_word))