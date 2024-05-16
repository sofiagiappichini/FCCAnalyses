import os
import shutil

# Define the original sample name and the replacement sample names

replacement_words = [
    "run_01",
    "run_02",
    "run_03",
    "run_04",
    "run_05",
    "run_06",
    #"run_07",
    #"run_08"
]

# Loop through each replacement word
for replacement_word in replacement_words:

    input_file = "/eos/user/s/sgiappic/2HNL_prod/HNL_6.67e-10_10mass_split/Events/{}/{}_tag_1_banner.txt".format(replacement_word, replacement_word)
    output_file = "/eos/user/s/sgiappic/2HNL_prod/HNL_6.67e-10_10mass_split/weights.txt"

    with open(input_file, "r") as file:
            read = False
            for line in file:
                if "#  Integrated weight (pb)  :" in line:      
                    content_of_row=float(line[35:])
                    read=True
            if read == False:
                content_of_row='error'
    
    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write("{}; {}\n".format(replacement_word, content_of_row))

    print("Content from {} has been written to {}".format(input_file, output_file))

