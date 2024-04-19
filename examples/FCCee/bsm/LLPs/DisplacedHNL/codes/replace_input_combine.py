import shutil
import os

# Define the original sample name and the replacement sample name
nomeFile = "HNL_2.86e-7_80gev"  # original file name
replacement_words= [
    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev"
]  # Add more replacement words as needed

# Create a backup directory if it doesn't exist
backup_dir = "combine_backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Loop through each replacement word
for replacement_word in replacement_words:

    # Backup the original file
    shutil.copy("/eos/user/s/sgiappic/combine/datacard_asym_tracks_DF.txt", os.path.join(backup_dir, "datacard_backup.txt"))

    # Perform substitution using sed within the loop
    with open(os.path.join(backup_dir, "datacard_backup.txt"), "r") as file:
        file_data = file.read()
    file_data = file_data.replace(nomeFile, replacement_word)
    with open(os.path.join(backup_dir, "datacard_backup.txt"), "w") as file:
        file.write(file_data)

    os.system("combine -M Significance {} -t -1 --expectSignal=1 >significance.txt".format(os.path.join(backup_dir, "datacard_backup.txt")))

    # Define the file names
    input_file = "significance.txt"
    output_file = "/eos/user/s/sgiappic/combine/output_tracks_asymDR_DF.csv"

    with open(input_file, "r") as file:
            read = False
            for line in file:
                if "Significance:" in line:
                    content_of_row=float(line[14:])
                    read=True
            if read == False:
                content_of_row='error'

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write("{}, {}\n".format(replacement_word, content_of_row))

    os.remove(os.path.join(backup_dir, "datacard_backup.txt"))

    print("Content from {} has been written to {}".format(input_file, output_file))
