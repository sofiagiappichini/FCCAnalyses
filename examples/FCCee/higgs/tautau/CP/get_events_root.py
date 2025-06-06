import uproot
import os
import shutil
import numpy as np
import csv
import ROOT
import glob

def file_exists(file_path):
    return os.path.isfile(file_path)

def get_entries(infilepath: str) -> tuple[int, int]:
    '''
    Get number of original entries and number of actual entries in the file
    '''
    events_processed = 0
    events_in_ttree = 0

    with ROOT.TFile(infilepath, 'READ') as infile:
        try:
            events_processed_obj = infile.Get('eventsProcessed')
            if events_processed_obj:
                events_processed = events_processed_obj.GetVal()
            events_ttree = infile.Get("events")
            if events_ttree:
                events_in_ttree = events_ttree.GetEntries()
            else:
                #print(f"Faulty {infilepath}")
                return None, None

        except AttributeError:
            return None, None


    return events_processed, events_in_ttree

dir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/"

for process in os.listdir(dir):
    i=0
    if "mg_ee_jjtata_smeft_cehim_m1_ecm240" not in process:
        continue
    #os.system(f"mkdir /eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/{process}")
    for file in os.listdir(dir+process):
        path = f"{dir}{process}/{file}"
        chunk_process_events, chunk_events_ttree = get_entries(path)
        #print(f"{process}: {file} with {chunk_events_ttree}")
        #if (chunk_events_ttree==1000000):
            #os.system(f"cp {path} /eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/{process}/chunk_{i}.root")
        i+=1
        print(f"{i}, {process}, {file}, {chunk_events_ttree}")
            #if "eetata" in process or "mumutata" in process:
            #    break
            #elif i>=10:
            #    break
