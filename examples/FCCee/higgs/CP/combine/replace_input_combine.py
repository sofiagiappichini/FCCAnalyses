import shutil
import os

category = [
    "eeH",
    "mumuH",
    "bbH",
    "ccH",
    "ssH",
    "qqH",
    "QQH",
]
## need to work in centos7 : portal1-centos7.etp.kit.edu
os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
os.system("cd /work/nfaltermann/cmssw/CMSSW_10_6_0/src/")
os.system("cmsenv")
os.system("cd FCCAnalyses/examples/FCCee/higgs/CP/combine/")

input_file = "significance.txt"
output_file = "FCCAnalyses/examples/FCCee/higgs/CP/output_xsec.csv"

for cat in category:

    os.system("text2workspace.py datacard_{}.txt -o ws_{}.root".format(cat, cat))
    os.system("combine -M FitDiagnostics -t -1 --expectSignal=1 ws_{}.root --rMin -2 >significance.txt".format(cat))

    with open(input_file, "r") as file:
            read = False
            for line in file:
                if "Best fit r:" in line:
                    content_of_row=line[11:]
                    read=True
            if read == False:
                content_of_row='error'

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write("{}: {} \n".format(cat, content_of_row))

    print("Content from {} has been written to {}".format(cat, output_file))

os.system("text2workspace.py datacard_combined.txt -o ws_combined.root")
os.system("combine -M FitDiagnostics -t -1 --expectSignal=1 ws_combined.root --rMin -2  >significance.txt")

with open(input_file, "r") as file:
        read = False
        for line in file:
            if "Best fit r:" in line:
                content_of_row=line[11:]
                read=True
        if read == False:
            content_of_row='error'

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as csv_file:
    csv_file.write("combination: {} \n".format(content_of_row))

print("Content from {} has been written to {}".format(dir, output_file))

with open(output_file, "a") as csv_file:
    csv_file.write("\n")

# combineCards.py ee=datacard_eeH.txt mumu=datacard_mumuH.txt QQ=datacard_QQH.txt > datacard_combined.txt
# combineCards.py bb=datacard_bbH.txt cc=datacard_ccH.txt ss=datacard_ssH.txt qq=datacard_qqH.txt > datacard_QQH.txt