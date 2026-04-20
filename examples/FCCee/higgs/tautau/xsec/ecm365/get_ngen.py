import json

# === Load the JSON-like file ===
def load_event_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# === Extract numberOfEvents for a given list of process names ===
def get_number_of_events(data, process_names):
    result = {}
    for name in process_names:
        if name in data:
            result[name] = data[name].get("numberOfEvents", None)
        else:
            result[name] = None  # Not found
    return result

# === Example usage ===
if __name__ == "__main__":
    # Your JSON filename
    filename = "/afs/cern.ch/work/f/fccsw/public/FCCDicts/FCCee_procDict_winter2023_IDEA.json"

    # List of processes you're interested in
    processList = {

    'p8_ee_WW_ecm365':{},
    'p8_ee_WW_tautau_ecm365':{},
    'p8_ee_Zqq_ecm365':{},
    'p8_ee_ZZ_ecm365':{},
    'p8_ee_Zbb_ecm365':{},
    'p8_ee_Zcc_ecm365':{},
    'p8_ee_Zss_ecm365':{},
    'p8_ee_tt_ecm365':{},
    
    'wzp6_ee_tautau_ecm365':{},
    'wzp6_ee_mumu_ecm365':{},
    'wzp6_ee_ee_Mee_30_150_ecm365':{},

    'wzp6_ee_tautauH_Htautau_ecm365': {},
    'wzp6_ee_tautauH_Hbb_ecm365': {},
    'wzp6_ee_tautauH_Hcc_ecm365': {},
    'wzp6_ee_tautauH_Hss_ecm365': {},
    'wzp6_ee_tautauH_Hgg_ecm365': {},
    'wzp6_ee_tautauH_HWW_ecm365': {},
    'wzp6_ee_tautauH_HZZ_ecm365': {},

    'wzp6_egamma_eZ_Zmumu_ecm365': {},
    'wzp6_egamma_eZ_Zee_ecm365': {},
    'wzp6_gammae_eZ_Zmumu_ecm365': {},
    'wzp6_gammae_eZ_Zee_ecm365': {},

    'wzp6_gaga_tautau_60_ecm365': {},
    'wzp6_gaga_mumu_60_ecm365': {},
    'wzp6_gaga_ee_60_ecm365': {},

    'wzp6_ee_nuenueZ_ecm365': {},
    'wzp6_ee_nunuH_Htautau_ecm365': {},
    'wzp6_ee_nunuH_Hbb_ecm365': {},
    'wzp6_ee_nunuH_Hcc_ecm365': {},
    'wzp6_ee_nunuH_Hss_ecm365': {},
    'wzp6_ee_nunuH_Hgg_ecm365': {},
    'wzp6_ee_nunuH_HWW_ecm365': {},
    'wzp6_ee_nunuH_HZZ_ecm365': {},

    'wzp6_ee_eeH_Htautau_ecm365': {},
    'wzp6_ee_eeH_Hbb_ecm365': {},
    'wzp6_ee_eeH_Hcc_ecm365': {},
    'wzp6_ee_eeH_Hss_ecm365': {},
    'wzp6_ee_eeH_Hgg_ecm365': {},
    'wzp6_ee_eeH_HWW_ecm365': {},
    'wzp6_ee_eeH_HZZ_ecm365': {},

    'wzp6_ee_mumuH_Htautau_ecm365': {},
    'wzp6_ee_mumuH_Hbb_ecm365': {},
    'wzp6_ee_mumuH_Hcc_ecm365': {},
    'wzp6_ee_mumuH_Hss_ecm365': {},
    'wzp6_ee_mumuH_Hgg_ecm365': {},
    'wzp6_ee_mumuH_HWW_ecm365': {},
    'wzp6_ee_mumuH_HZZ_ecm365': {},

    'wzp6_ee_bbH_Htautau_ecm365': {},
    'wzp6_ee_bbH_Hbb_ecm365': {},
    'wzp6_ee_bbH_Hcc_ecm365': {},
    'wzp6_ee_bbH_Hss_ecm365': {},
    'wzp6_ee_bbH_Hgg_ecm365': {},
    'wzp6_ee_bbH_HWW_ecm365': {},
    'wzp6_ee_bbH_HZZ_ecm365': {},

    'wzp6_ee_ccH_Htautau_ecm365': {},
    'wzp6_ee_ccH_Hbb_ecm365': {},
    'wzp6_ee_ccH_Hcc_ecm365': {},
    'wzp6_ee_ccH_Hss_ecm365': {},
    'wzp6_ee_ccH_Hgg_ecm365': {},
    'wzp6_ee_ccH_HWW_ecm365': {},
    'wzp6_ee_ccH_HZZ_ecm365': {},

    'wzp6_ee_ssH_Htautau_ecm365': {},
    'wzp6_ee_ssH_Hbb_ecm365': {},
    'wzp6_ee_ssH_Hcc_ecm365': {},
    'wzp6_ee_ssH_Hss_ecm365': {},
    'wzp6_ee_ssH_Hgg_ecm365': {},
    'wzp6_ee_ssH_HWW_ecm365': {},
    'wzp6_ee_ssH_HZZ_ecm365': {},

    'wzp6_ee_qqH_Htautau_ecm365': {},
    'wzp6_ee_qqH_Hbb_ecm365': {},
    'wzp6_ee_qqH_Hcc_ecm365': {},
    'wzp6_ee_qqH_Hss_ecm365': {},
    'wzp6_ee_qqH_Hgg_ecm365': {},
    'wzp6_ee_qqH_HWW_ecm365': {},
    'wzp6_ee_qqH_HZZ_ecm365': {},

    'wzp6_ee_nuenueH_Htautau_ecm365': {},
    'wzp6_ee_nuenueH_Hbb_ecm365': {},
    'wzp6_ee_nuenueH_Hcc_ecm365': {},
    'wzp6_ee_nuenueH_Hss_ecm365': {},
    'wzp6_ee_nuenueH_Hgg_ecm365': {},
    'wzp6_ee_nuenueH_HWW_ecm365': {},
    'wzp6_ee_nuenueH_HZZ_ecm365': {},  

    'wzp6_ee_numunumuH_Htautau_ecm365': {},
    'wzp6_ee_numunumuH_Hbb_ecm365': {},
    'wzp6_ee_numunumuH_Hcc_ecm365': {},
    'wzp6_ee_numunumuH_Hss_ecm365': {},
    'wzp6_ee_numunumuH_Hgg_ecm365': {},
    'wzp6_ee_numunumuH_HWW_ecm365': {},
    'wzp6_ee_numunumuH_HZZ_ecm365': {},

    'wzp6_ee_VBF_nunuH_Htautau_ecm365': {},
    'wzp6_ee_VBF_nunuH_Hbb_ecm365': {},
    'wzp6_ee_VBF_nunuH_Hcc_ecm365': {},
    'wzp6_ee_VBF_nunuH_Hss_ecm365': {},
    'wzp6_ee_VBF_nunuH_Hgg_ecm365': {},
    'wzp6_ee_VBF_nunuH_HWW_ecm365': {},
    'wzp6_ee_VBF_nunuH_HZZ_ecm365': {},
    }

    # Load data and extract
    event_data = load_event_file(filename)
    selected = get_number_of_events(event_data, processList)

    # Print results
    for name, num_events in selected.items():
        print(f"'{name}': {num_events},")
