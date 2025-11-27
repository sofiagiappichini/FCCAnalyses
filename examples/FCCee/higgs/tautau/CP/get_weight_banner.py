import os
import shutil
import glob
import gzip

# Define the original sample name and the replacement sample names

replacement_words = [
    #'noISR_e+e-_noCuts_EWonly',
    #'noISR_e+e-_noCuts_cehim_m1',
    #'noISR_e+e-_noCuts_cehim_p1',
    #'noISR_e+e-_noCuts_cehre_m1',
    #'noISR_e+e-_noCuts_cehre_p1',

    #'noISR_e+e-_noCuts_EWonly_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_m1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_p1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_m1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_p1_taudecay_2Pi2Nu',

    #'noISR_e+e-_noCuts_cehim_m5_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_p5_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_m5_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_p5_taudecay_2Pi2Nu',

    #'noISR_e+e-_noCuts_cehim_m2_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_p2_taudecay_2Pi2Nu',
    #noISR_e+e-_noCuts_cehre_m2_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_p2_taudecay_2Pi2Nu',

    #'noISR_e+e-_noCuts_cehim_p0p1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_m0p1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_m0p1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehre_p0p1_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_p10_taudecay_2Pi2Nu',
    #'noISR_e+e-_noCuts_cehim_m10_taudecay_2Pi2Nu',

    #'noISR_e+e-_noCuts_EWonly_taudecay_PiPi0Nu',
    #'noISR_e+e-_noCuts_cehim_m1_taudecay_PiPi0Nu',
    #'noISR_e+e-_noCuts_cehim_p1_taudecay_PiPi0Nu',
    #'noISR_e+e-_noCuts_cehre_m1_taudecay_PiPi0Nu',
    #'noISR_e+e-_noCuts_cehre_p1_taudecay_PiPi0Nu',

    #"mg_ee_eetata_ecm240",
    #"mg_ee_eetata_smeft_cehim_m1_ecm240",
    #"mg_ee_eetata_smeft_cehim_p1_ecm240",
    #"mg_ee_eetata_smeft_cehre_m1_ecm240",
    #"mg_ee_eetata_smeft_cehre_p1_ecm240",
    #"mg_ee_jjtata_ecm240",
    #"mg_ee_jjtata_smeft_cehim_m1_ecm240",
    #"mg_ee_jjtata_smeft_cehim_p1_ecm240",
    #"mg_ee_jjtata_smeft_cehre_m1_ecm240",
    #"mg_ee_jjtata_smeft_cehre_p1_ecm240",
    #"mg_ee_mumutata_ecm240",
    #"mg_ee_mumutata_smeft_cehim_m1_ecm240",
    #"mg_ee_mumutata_smeft_cehim_p1_ecm240",
    #"mg_ee_mumutata_smeft_cehre_m1_ecm240",
    #"mg_ee_mumutata_smeft_cehre_p1_ecm240",
    #"mg_ee_eetata_pinu_c_mass_smeft_cehim_m1_ecm240",
    #"mg_ee_eetata_pinu_smeft_cehim_m1_ecm240",
    "llh-m1-2body",
    "llh-m1-3body",
    "llh-m1-4body",
    "llh-mixed-cehim-m1_2-3",
    "llh-mixed-cehim-m1_2-4",
    "llh-mixed-cehim-m1_3-2",
    "llh-mixed-cehim-m1_3-4",
    "llh-mixed-cehim-m1_4-2",
    "llh-mixed-cehim-m1_4-3",
    "llh-mixed-cehim-p1_2-3",
    "llh-mixed-cehim-p1_2-4",
    "llh-mixed-cehim-p1_3-2",
    "llh-mixed-cehim-p1_3-4",
    "llh-mixed-cehim-p1_4-2",
    "llh-mixed-cehim-p1_4-3",
    "llh-mixed-sm_2-3",
    "llh-mixed-sm_2-4",
    "llh-mixed-sm_3-2",
    "llh-mixed-sm_3-4",
    "llh-mixed-sm_4-2",
    "llh-mixed-sm_4-3",
    "llh-p1-2body",
    "llh-p1-3body",
    "llh-p1-4body",
    "llh-sm-2body",
    "llh-sm-3body",
    "llh-sm-4body",

]

# Loop through each replacement word
for replacement_word in replacement_words:

    #input_file = "/work/mpresill//MG5_aMC_v3_5_4/ZH_SMEFT_prod/{}/Events/run_01/run_01_tag_1_banner.txt".format(replacement_word)
    #output_file = "/ceph/sgiappic/HiggsCP/CPReco/weights.txt"

    pattern = f"/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/lhe/wMadspin/{replacement_word}.lhe.gz"
    lhe_gz_files = glob.glob(pattern)

    if not lhe_gz_files:
        print(f"No files found for {replacement_word}")
        continue

    first_file = lhe_gz_files[0]  # Take only the first match
    extracted_number = None
    second_row_found = False
    nevents = 0

    with gzip.open(first_file, 'rt') as f:
        in_init_block = False
        for line in f:
            if "#  Number of Events        : " in line:
                nevents+=int(line[35:])

            if "<init>" in line:
                in_init_block = True
                continue
            if "</init>" in line:
                in_init_block = False
                break

            if in_init_block:
                if second_row_found:
                    # Extract the first number from the second row inside <init>
                    numbers = line.split()
                    if len(numbers) > 0:
                        extracted_number = float(numbers[0])
                        break
                second_row_found = True

    if extracted_number is None:
        print(f"Could not extract number for {replacement_word}")
        continue

    output_file = "/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/CP/weight.txt"

    # Write the content of the selected row to the output CSV file
    #with open(output_file, "a") as csv_file:
    print("'{}':{{\"numberOfEvents\": {}, \"sumOfWeights\": {}, \"crossSection\": {}, \"kfactor\": 1.0, \"matchingEfficiency\": 1.0}},\n".format(replacement_word, nevents, nevents, extracted_number))

    #print(f"{nevents}")
    #print("Content from {} has been written to {}".format(first_file, output_file))
