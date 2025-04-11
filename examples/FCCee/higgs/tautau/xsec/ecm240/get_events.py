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
        #try:
        #    events_processed = infile.Get('eventsProcessed').GetVal()
        #except AttributeError:
        #    LOGGER.warning('Input file is missing information about '
        #                   'original number of events!')

        #try:
        #    events_in_ttree = infile.Get("events").GetEntries()
        #except AttributeError:
        #    LOGGER.error('Input file is missing "events" TTree!\nAborting...')
        #    sys.exit(3)
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

all = [
    'wzp6_ee_QQH_Htautau_ecm240',
    #'wzp6_ee_eeH_Htautau_ecm240',
    #'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_LLH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',

    "wzp6_ee_tautauH_Htautau_ecm240",
    "wzp6_ee_tautauH_HQQ_ecm240",
    "wzp6_ee_tautauH_Hgg_ecm240",
    "wzp6_ee_tautauH_HVV_ecm240",

    #"wzp6_ee_nunuH_Htautau_ecm240",
    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    #"wzp6_ee_LLH_Htautau_ecm240",
    "wzp6_ee_LLH_HQQ_ecm240",
    "wzp6_ee_LLH_Hgg_ecm240",
    "wzp6_ee_LLH_HVV_ecm240",

    #"wzp6_ee_QQH_Htautau_ecm240",
    "wzp6_ee_QQH_HQQ_ecm240",
    "wzp6_ee_QQH_Hgg_ecm240",
    "wzp6_ee_QQH_HVV_ecm240",

    "p8_ee_Zqq_ecm240",
    "wzp6_ee_LL_ecm240",
    "wzp6_ee_tautau_ecm240",

    "p8_ee_WW_ecm240",
    "p8_ee_Zqq_ecm240",
    "p8_ee_ZZ_ecm240",

    "wzp6_ee_LL_ecm240",
    "wzp6_ee_tautau_ecm240",

    "wzp6_ee_nuenueZ_ecm240",

    "wzp6_ee_egamma_eZ_ZLL_ecm240",
    
    "wzp6_ee_gaga_LL_60_ecm240",
    "wzp6_ee_gaga_tautau_60_ecm240",

]

DY = [
    "p8_ee_Zqq_ecm240",
    "wzp6_ee_LL_ecm240",
    "wzp6_ee_tautau_ecm240",

]

ZH = [

    "wzp6_ee_tautauH_Htautau_ecm240",
    "wzp6_ee_tautauH_HQQ_ecm240",
    "wzp6_ee_tautauH_Hgg_ecm240",
    "wzp6_ee_tautauH_HVV_ecm240",

    #"wzp6_ee_nunuH_Htautau_ecm240",
    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    #"wzp6_ee_LLH_Htautau_ecm240",
    "wzp6_ee_LLH_HQQ_ecm240",
    "wzp6_ee_LLH_Hgg_ecm240",
    "wzp6_ee_LLH_HVV_ecm240",

    #"wzp6_ee_QQH_Htautau_ecm240",
    "wzp6_ee_QQH_HQQ_ecm240",
    "wzp6_ee_QQH_Hgg_ecm240",
    "wzp6_ee_QQH_HVV_ecm240",
]

signal = [
    'wzp6_ee_QQH_Htautau_ecm240',
    #'wzp6_ee_eeH_Htautau_ecm240',
    #'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_LLH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
]

DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/ecm240/"

TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
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

# Define the tree name
tree_name = "events"
leaf_name = "Tau_cos"

'''for replacement_word in replacement_words:

    root_file_path = DIRECTORY_EOS + replacement_word
    process_events = 0
    events_ttree = 0

    flist = glob.glob(root_file_path + '/*.root')
    print(f"{replacement_word} & {len(flist)}")

for replacement_word in replacement_words:

    root_file_path = DIRECTORY_EOS + replacement_word
    process_events = 0
    events_ttree = 0

    flist = glob.glob(root_file_path + '/chunk*.root')
    for filepath in flist:
        chunk_process_events, chunk_events_ttree = get_entries(filepath)
        if chunk_process_events is not None and chunk_events_ttree is not None:
            process_events += chunk_process_events #original number of events
            events_ttree += chunk_events_ttree
    print((f"{replacement_word} & {process_events} & "))
    row.append(f"{replacement_word} & {process_events} & ")
    raw[replacement_word] = process_events
tab.append(row)

'''
'''
for tag in TAG:
    tab = []
    for cat in CAT:
        for sub in SUBDIR:
            directory = DIRECTORY + tag + "/stage2_280125_cut/" + cat + "/" + sub + "/"
            print(directory)
            newrow = []
            newrow.append(f"{cat+sub} & ") #header

            for replacement_word in replacement_words:
            
                root_file_path = directory + replacement_word
                process_events = 0
                events_ttree = 0

                flist = glob.glob(root_file_path + '/*.root')
                for filepath in flist:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        process_events += chunk_process_events #original number of events
                        events_ttree += chunk_events_ttree #number of events after selection=

                newrow.append(f"{events_ttree} & ")

                #if process_events!=0 :
                #    newrow.append(f"{events_ttree/process_events:.2e} & ")
                #else:
                #    ratio = 1/raw[replacement_word]
                #    newrow.append(f"$\leq$ {ratio:.2e} & ") 

            tab.append(newrow)

    # Write the content of the selected row to the output CSV file
    transposed_tab = list(zip(*tab))

    output_file = DIRECTORY + tag + "/nevents_cut.txt"
    
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        # Write each row of the matrix
        writer.writerows(transposed_tab)
'''
for tag in TAG:
    table_data = {}
    table_data_temp = {}  
    hh_total_data = {}  
    dy_total_data = {}
    sig_total_data = {}

    for cat in CAT:
        for sub in SUBDIR:
            directory = DIRECTORY + tag + "/final_241202/" + cat + "/" + sub + "/"
            col_name = f"{cat}{sub}"

            for file in all:
                file_name = f"{file}_selReco_histo.root"
                histo_file_path = os.path.join(directory, file_name)

                if os.path.exists(histo_file_path):
                    histo_file = uproot.open(histo_file_path)
                    selected_leaf = histo_file[leaf_name]
                    total_entries = sum(selected_leaf.values())
                else:
                    total_entries = 0

                if file in signal:
                    if col_name not in sig_total_data:
                        sig_total_data[col_name] = 0
                    sig_total_data[col_name] += total_entries
                elif file in ZH:
                    if col_name not in hh_total_data:
                        hh_total_data[col_name] = 0
                    hh_total_data[col_name] += total_entries
                elif file in DY:
                    if col_name not in dy_total_data:
                        dy_total_data[col_name] = 0
                    dy_total_data[col_name] += total_entries
                else:
                    if file not in table_data_temp:
                        table_data_temp[file] = {}
                    table_data_temp[file][col_name] = f"{total_entries:.2e}" if total_entries !=0 else "0"
        
    if sig_total_data:
        table_data['wzp6_ee_ZH_Htautau_ecm240'] = {col: f"{value:.2e}" for col, value in sig_total_data.items()}

    if hh_total_data:
        table_data['ZH background'] = {col: f"{value:.2e}" for col, value in hh_total_data.items()}

    if dy_total_data:
        table_data['DY'] = {col: f"{value:.2e}" for col, value in dy_total_data.items()}

    if table_data_temp:
        table_data.update(table_data_temp)

    column_headers = sorted(set(f"{cat}{sub}" for cat in CAT for sub in SUBDIR))

    # LaTeX Table Header
    latex_table_content = """
    \\begin{table}[h]
    \\centering
    \\begin{tabular}{|c|""" + "c|" * len(column_headers) + """}
    \\hline
    File Name & """ + " & ".join(column_headers) + """ \\\\
    \\hline
    """

    # Prepare data for LaTeX & CSV output
    latex_rows = []

    for file_name, row_data in table_data.items():
        latex_row = [file_name]  

        for col in column_headers:
            value = row_data.get(col, 0)  # Default to 0 if missing
            latex_row.append(f"{value}")

        latex_rows.append(" & ".join(latex_row) + " \\\\ \\hline")

    # LaTeX Table Footer
    latex_table_content += "\n".join(latex_rows) + """
    \\end{tabular}
    \\caption{Fit Results}
    \\end{table}
    """

    # Save LaTeX Table
    latex_output_file = f"/ceph/sgiappic/HiggsCP/ecm240/{tag}_nevents.txt"
    with open(latex_output_file, "w") as f:
        f.write(latex_table_content)

    print(f"LaTeX table saved: {latex_output_file}")

