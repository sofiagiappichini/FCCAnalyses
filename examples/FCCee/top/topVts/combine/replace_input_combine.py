import shutil
import os

# Define the original sample name and the replacement sample name

directory = [ 
    "R5_070_Wqq_pair_tightBjet",
    "R5_070_top_trio_tightBjet",
    "ktN_070_top_trio_tightBjet",
]  

category = [
    "dilep",
    "semilep_cs",
    "semilep_ud",
    "dihad",
]

os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
os.system("cd /work/nfaltermann/cmssw/CMSSW_10_6_0/src/")
os.system("cmsenv")
os.system("cd /ceph/sgiappic/topVts/")

input_file = "significance.txt"
output_file = "/ceph/sgiappic/topVts/output_significance.csv"

for dir in directory:

    with open(output_file, "a") as csv_file:
        csv_file.write("{}: \n".format(dir))

    for cat in category:

        os.system("combine -M Significance datacard_{}_{}.txt -t -1 --expectSignal=1 >significance.txt".format(dir, cat))

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
            csv_file.write("{}: {} \n".format(cat, content_of_row))

        print("Content from {} has been written to {}".format(cat, output_file))

    os.system("combine -M Significance datacard_{}.txt -t -1 --expectSignal=1 >significance.txt".format(dir))

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
        csv_file.write("combination: {} \n".format(content_of_row))

    print("Content from {} has been written to {}".format(dir, output_file))

    with open(output_file, "a") as csv_file:
        csv_file.write("\n")
