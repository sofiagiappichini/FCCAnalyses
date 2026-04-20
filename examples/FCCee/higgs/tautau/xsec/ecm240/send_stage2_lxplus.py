import ROOT
import os

DIRECTORIES = [
    #"/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/R5-explicit/",
    #"/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/R5-tag/",
    #"/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/BDT/stage3-new/ktN-explicit/",
    "/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/BDT/stage3-new/ktN-tag/",
]
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    "NuNu",
]

for dir in DIRECTORIES:
    for cat in CAT:

        directory = dir
        print(f"Directory {directory}")

        for sub in SUBDIR:

            #os.system(f"fccanalysis run {directory}/analysis_stage2_{cat}{sub}.py")
            os.system(f"fccanalysis run {directory}/analysis_stage3_{cat}{sub}.py")
            print(f"Executed {cat}{sub}")        