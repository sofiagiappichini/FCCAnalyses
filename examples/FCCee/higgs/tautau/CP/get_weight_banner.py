import os
import shutil

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

    'noISR_e+e-_noCuts_cehim_m2_taudecay_2Pi2Nu',
    'noISR_e+e-_noCuts_cehim_p2_taudecay_2Pi2Nu',
    'noISR_e+e-_noCuts_cehre_m2_taudecay_2Pi2Nu',
    'noISR_e+e-_noCuts_cehre_p2_taudecay_2Pi2Nu',
]

# Loop through each replacement word
for replacement_word in replacement_words:

    input_file = "/work/mpresill//MG5_aMC_v3_5_4/ZH_SMEFT_prod/{}/Events/run_01/run_01_tag_1_banner.txt".format(replacement_word)
    output_file = "/ceph/sgiappic/HiggsCP/CP/weights.txt"

    with open(input_file, "r") as file:
            read = False
            for line in file:
                if "#  Integrated weight (pb)  :" in line:      
                    content_of_row=float(line[35:])
                    read=True
                if "#  Number of Events        : " in line:
                    nevents=int(line[35:])
                    read=True

            if read == False:
                content_of_row='error'
                nevents="error"
    
    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write("'{}':{{\"numberOfEvents\": {}, \"sumOfWeights\": {}, \"crossSection\": {}, \"kfactor\": 1.0, \"matchingEfficiency\": 1.0}},\n".format(replacement_word, nevents, nevents, content_of_row))

    print("Content from {} has been written to {}".format(input_file, output_file))
