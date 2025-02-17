import shutil
import os

# Define the original sample name and the replacement sample name
nomeFile = "HNL_2.86e-7_80gev"  # original file name

cut_SF = "selReco_gen_notracks_nojets_5M80_0.8cos_10MET_22ME70_leadE40"
cut_DF = "selReco_gen_notracks_nojets_5M80_0.8cos_10MET"

replacement_words = [ 
    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.78e-8_10gev",
    "HNL_2.78e-8_20gev",
    "HNL_2.78e-8_30gev",
    "HNL_2.78e-8_40gev",
    "HNL_2.78e-8_50gev",
    "HNL_2.78e-8_60gev",
    "HNL_2.78e-8_70gev",
    "HNL_2.78e-8_80gev",

    "HNL_6.05e-9_10gev",
    "HNL_6.05e-9_20gev",
    "HNL_6.05e-9_30gev",
    "HNL_6.05e-9_40gev",
    "HNL_6.05e-9_50gev",
    "HNL_6.05e-9_60gev",
    "HNL_6.05e-9_70gev",
    "HNL_6.05e-9_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_2.90e-10_10gev",
    "HNL_2.90e-10_20gev",
    "HNL_2.90e-10_30gev",
    "HNL_2.90e-10_40gev",
    "HNL_2.90e-10_50gev",
    "HNL_2.90e-10_60gev",
    "HNL_2.90e-10_70gev",
    "HNL_2.90e-10_80gev",

    "HNL_6.34e-11_10gev",
    "HNL_6.34e-11_20gev",
    "HNL_6.34e-11_30gev",
    "HNL_6.34e-11_40gev",
    "HNL_6.34e-11_50gev",
    "HNL_6.34e-11_60gev",
    "HNL_6.34e-11_70gev",
    "HNL_6.34e-11_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    

    "HNL_4e-8_10gev",
    "HNL_4e-8_20gev",
    "HNL_4e-8_30gev",
    "HNL_4e-8_40gev",
    "HNL_4e-8_50gev",
    "HNL_4e-8_60gev",
    "HNL_4e-8_70gev",
    "HNL_4e-8_80gev",

    "HNL_8.35e-9_10gev",
    "HNL_8.35e-9_20gev",
    "HNL_8.35e-9_30gev",
    "HNL_8.35e-9_40gev",
    "HNL_8.35e-9_50gev",
    "HNL_8.35e-9_60gev",
    "HNL_8.35e-9_70gev",
    "HNL_8.35e-9_80gev",

    "HNL_1.81e-9_10gev",
    "HNL_1.81e-9_20gev",
    "HNL_1.81e-9_30gev",
    "HNL_1.81e-9_40gev",
    "HNL_1.81e-9_50gev",
    "HNL_1.81e-9_60gev",
    "HNL_1.81e-9_70gev",
    "HNL_1.81e-9_80gev",

    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_8.69e-11_10gev",
    "HNL_8.69e-11_20gev",
    "HNL_8.69e-11_30gev",
    "HNL_8.69e-11_40gev",
    "HNL_8.69e-11_50gev",
    "HNL_8.69e-11_60gev",
    "HNL_8.69e-11_70gev",
    "HNL_8.69e-11_80gev",

    "HNL_1.90e-11_10gev",
    "HNL_1.90e-11_20gev",
    "HNL_1.90e-11_30gev",
    "HNL_1.90e-11_40gev",
    "HNL_1.90e-11_50gev",
    "HNL_1.90e-11_60gev",
    "HNL_1.90e-11_70gev",
    "HNL_1.90e-11_80gev",

    "HNL_4e-12_10gev",
    "HNL_4e-12_20gev",
    "HNL_4e-12_30gev",
    "HNL_4e-12_40gev",
    "HNL_4e-12_50gev",
    "HNL_4e-12_60gev",
    "HNL_4e-12_70gev",
    "HNL_4e-12_80gev",

    

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_5.97e-9_10gev",
    "HNL_5.97e-9_20gev",
    "HNL_5.97e-9_30gev",
    "HNL_5.97e-9_40gev",
    "HNL_5.97e-9_50gev",
    "HNL_5.97e-9_60gev",
    "HNL_5.97e-9_70gev",
    "HNL_5.97e-9_80gev",

    "HNL_1.30e-9_10gev",
    "HNL_1.30e-9_20gev",
    "HNL_1.30e-9_30gev",
    "HNL_1.30e-9_40gev",
    "HNL_1.30e-9_50gev",
    "HNL_1.30e-9_60gev",
    "HNL_1.30e-9_70gev",
    "HNL_1.30e-9_80gev",

    "HNL_2.86e-10_10gev",
    "HNL_2.86e-10_20gev",
    "HNL_2.86e-10_30gev",
    "HNL_2.86e-10_40gev",
    "HNL_2.86e-10_50gev",
    "HNL_2.86e-10_60gev",
    "HNL_2.86e-10_70gev",
    "HNL_2.86e-10_80gev",

    "HNL_6.20e-11_10gev",
    "HNL_6.20e-11_20gev",
    "HNL_6.20e-11_30gev",
    "HNL_6.20e-11_40gev",
    "HNL_6.20e-11_50gev",
    "HNL_6.20e-11_60gev",
    "HNL_6.20e-11_70gev",
    "HNL_6.20e-11_80gev",

    "HNL_1.36e-11_10gev",
    "HNL_1.36e-11_20gev",
    "HNL_1.36e-11_30gev",
    "HNL_1.36e-11_40gev",
    "HNL_1.36e-11_50gev",
    "HNL_1.36e-11_60gev",
    "HNL_1.36e-11_70gev",
    "HNL_1.36e-11_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    ##inverted

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_1.04e-8_10gev",
    "HNL_1.04e-8_20gev",
    "HNL_1.04e-8_30gev",
    "HNL_1.04e-8_40gev",
    "HNL_1.04e-8_50gev",
    "HNL_1.04e-8_60gev",
    "HNL_1.04e-8_70gev",
    "HNL_1.04e-8_80gev",

    "HNL_2.27e-9_10gev",
    "HNL_2.27e-9_20gev",
    "HNL_2.27e-9_30gev",
    "HNL_2.27e-9_40gev",
    "HNL_2.27e-9_50gev",
    "HNL_2.27e-9_60gev",
    "HNL_2.27e-9_70gev",
    "HNL_2.27e-9_80gev",

    "HNL_5e-10_10gev",
    "HNL_5e-10_20gev",
    "HNL_5e-10_30gev",
    "HNL_5e-10_40gev",
    "HNL_5e-10_50gev",
    "HNL_5e-10_60gev",
    "HNL_5e-10_70gev",
    "HNL_5e-10_80gev",

    "HNL_1.09e-10_10gev",
    "HNL_1.09e-10_20gev",
    "HNL_1.09e-10_30gev",
    "HNL_1.09e-10_40gev",
    "HNL_1.09e-10_50gev",
    "HNL_1.09e-10_60gev",
    "HNL_1.09e-10_70gev",
    "HNL_1.09e-10_80gev",

    "HNL_2.38e-11_10gev",
    "HNL_2.38e-11_20gev",
    "HNL_2.38e-11_30gev",
    "HNL_2.38e-11_40gev",
    "HNL_2.38e-11_50gev",
    "HNL_2.38e-11_60gev",
    "HNL_2.38e-11_70gev",
    "HNL_2.38e-11_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    

    "HNL_6.67e-8_10gev",
    "HNL_6.67e-8_20gev",
    "HNL_6.67e-8_30gev",
    "HNL_6.67e-8_40gev",
    "HNL_6.67e-8_50gev",
    "HNL_6.67e-8_60gev",
    "HNL_6.67e-8_70gev",
    "HNL_6.67e-8_80gev",

    "HNL_1.39e-8_10gev",
    "HNL_1.39e-8_20gev",
    "HNL_1.39e-8_30gev",
    "HNL_1.39e-8_40gev",
    "HNL_1.39e-8_50gev",
    "HNL_1.39e-8_60gev",
    "HNL_1.39e-8_70gev",
    "HNL_1.39e-8_80gev",

    "HNL_3.02e-9_10gev",
    "HNL_3.02e-9_20gev",
    "HNL_3.02e-9_30gev",
    "HNL_3.02e-9_40gev",
    "HNL_3.02e-9_50gev",
    "HNL_3.02e-9_60gev",
    "HNL_3.02e-9_70gev",
    "HNL_3.02e-9_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_1.45e-10_10gev",
    "HNL_1.45e-10_20gev",
    "HNL_1.45e-10_30gev",
    "HNL_1.45e-10_40gev",
    "HNL_1.45e-10_50gev",
    "HNL_1.45e-10_60gev",
    "HNL_1.45e-10_70gev",
    "HNL_1.45e-10_80gev",

    "HNL_3.17e-11_10gev",
    "HNL_3.17e-11_20gev",
    "HNL_3.17e-11_30gev",
    "HNL_3.17e-11_40gev",
    "HNL_3.17e-11_50gev",
    "HNL_3.17e-11_60gev",
    "HNL_3.17e-11_70gev",
    "HNL_3.17e-11_80gev",

    "HNL_6.67e-12_10gev",
    "HNL_6.67e-12_20gev",
    "HNL_6.67e-12_30gev",
    "HNL_6.67e-12_40gev",
    "HNL_6.67e-12_50gev",
    "HNL_6.67e-12_60gev",
    "HNL_6.67e-12_70gev",
    "HNL_6.67e-12_80gev",

    

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",

    "HNL_5.97e-8_10gev",
    "HNL_5.97e-8_20gev",
    "HNL_5.97e-8_30gev",
    "HNL_5.97e-8_40gev",
    "HNL_5.97e-8_50gev",
    "HNL_5.97e-8_60gev",
    "HNL_5.97e-8_70gev",
    "HNL_5.97e-8_80gev",

    "HNL_1.30e-8_10gev",
    "HNL_1.30e-8_20gev",
    "HNL_1.30e-8_30gev",
    "HNL_1.30e-8_40gev",
    "HNL_1.30e-8_50gev",
    "HNL_1.30e-8_60gev",
    "HNL_1.30e-8_70gev",
    "HNL_1.30e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    "HNL_6.20e-10_10gev",
    "HNL_6.20e-10_20gev",
    "HNL_6.20e-10_30gev",
    "HNL_6.20e-10_40gev",
    "HNL_6.20e-10_50gev",
    "HNL_6.20e-10_60gev",
    "HNL_6.20e-10_70gev",
    "HNL_6.20e-10_80gev",

    "HNL_1.36e-10_10gev",
    "HNL_1.36e-10_20gev",
    "HNL_1.36e-10_30gev",
    "HNL_1.36e-10_40gev",
    "HNL_1.36e-10_50gev",
    "HNL_1.36e-10_60gev",
    "HNL_1.36e-10_70gev",
    "HNL_1.36e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",
    
    
]  # Add more replacement words as needed

SUBCUTS = [
    "_10gev",
    "_20gev",
    "_30gev",
 ]

SUBSTRING = [
    "_40gev",
    "_50gev",
    "_60gev",
    "_70gev",
    "_80gev", 
 ]

# Create a backup directory if it doesn't exist
backup_dir = "combine_backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Loop through each replacement word
for replacement_word in replacement_words:

    # Backup the original file
    shutil.copy("/eos/user/s/sgiappic/combine/datacard_24july_combined.txt", os.path.join(backup_dir, "datacard_backup.txt"))

    if "_10gev" in replacement_word:

        if "HNL_6.67e-8_10gev" in replacement_word:
            with open("/eos/user/s/sgiappic/combine/datacard_24july_10gev_combined_rebinned.txt", "r") as file:
                file_data = file.read()
        else:
            with open("/eos/user/s/sgiappic/combine/datacard_24july_10gev_combined.txt", "r") as file:
                file_data = file.read()

    else:
        # Perform substitution using sed within the loop
        with open(os.path.join(backup_dir, "datacard_backup.txt"), "r") as file:
            file_data = file.read()

    file_data = file_data.replace(nomeFile, replacement_word)

    for mass in SUBSTRING:
        if mass in replacement_word:

            newcut_SF = "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_SF"
            newcut_DF = "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_DF"
            file_data = file_data.replace(cut_SF, newcut_SF)
            file_data = file_data.replace(cut_DF, newcut_DF)
            with open(os.path.join(backup_dir, "datacard_backup.txt"), "w") as file:
                file.write(file_data)

    for mass in SUBCUTS:
        if mass in replacement_word:
            
            newcut_SF = "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35" + mass + "_SF"
            newcut_DF = "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35" + mass + "_DF"
            file_data = file_data.replace(cut_SF, newcut_SF)
            file_data = file_data.replace(cut_DF, newcut_DF)
            with open(os.path.join(backup_dir, "datacard_backup.txt"), "w") as file:
                file.write(file_data)

    os.system("combine -M Significance {} -t -1 --expectSignal=1 >significance.txt".format(os.path.join(backup_dir, "datacard_backup.txt")))

    # Define the file names
    input_file = "significance.txt"
    output_file = "/eos/user/s/sgiappic/combine/output_250211_125ab.csv"

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

    #os.remove(os.path.join(backup_dir, "datacard_backup.txt"))

    print("Content from {} has been written to {}".format(replacement_word, output_file))
