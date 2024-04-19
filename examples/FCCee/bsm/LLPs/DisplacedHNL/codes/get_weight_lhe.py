import os
import shutil

# Define the original sample name and the replacement sample names

replacement_words = [
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev"
]

# Loop through each replacement word
for replacement_word in replacement_words:

    input_file = "/eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe".format(replacement_word)
    output_file = "/eos/user/s/sgiappic/2HNL_samples/cross_section.txt"

    with open(input_file, "r") as file:
            read = False
            for line in file:
                if "#  Integrated weight (pb)  :" in line:
                    content_of_row=float(line[28:])
                    read=True
            if read == False:
                content_of_row='error'
    
    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write("'{}':['numberOfEvents': 50000, 'sumOfWeights': 50000, 'crossSection': {}, 'kfactor'': 1.0, 'matchingEfficiency': 1.0],\n".format(replacement_word, content_of_row))

    print("Content from {} has been written to {}".format(input_file, output_file))

