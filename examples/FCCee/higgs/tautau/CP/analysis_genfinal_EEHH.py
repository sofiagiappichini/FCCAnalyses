#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/sgiappic/HiggsCP/CP/stage2_Gen"

#Optional: output directory, default is local running directory
outputDir = "/ceph/sgiappic/HiggsCP/CP/final_Gen"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 4

#produces ROOT TTrees, default is False
doTree = False

#Mandatory: List of processes
processList = {
    'noISR_e+e-_noCuts_EWonly':{},
    'noISR_e+e-_noCuts_cehim_m1':{},
    'noISR_e+e-_noCuts_cehim_p1':{},
    'noISR_e+e-_noCuts_cehre_m1':{},
    'noISR_e+e-_noCuts_cehre_p1':{},
}
###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    'noISR_e+e-_noCuts_EWonly':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051559935862, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehim_m1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051749741618, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehim_p1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051749741618, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehre_m1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00058001482393, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehre_p1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00045498699833000005, "kfactor": 1.0, "matchingEfficiency": 1.0},

}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selGen": "true",
    #"selReco_Maria": " (Recoil>120 && Recoil<140) && (TauFromJet_type[0]>=0 && TauFromJet_type[1]>=0)",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "n_FSGenElectron":                  {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenElectron_e":                  {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_p":                  {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_pt":                 {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_px":                 {"name":"FSGenElectron_px",                 "title":"Final state gen electrons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_py":                 {"name":"FSGenElectron_py",                 "title":"Final state gen electrons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_pz":                 {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_y":                  {"name":"FSGenElectron_y",                  "title":"Final state gen electrons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenElectron_eta":                {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenElectron_theta":              {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":                {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenElectron_charge":             {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenElectron_mass":               {"name":"FSGenElectron_mass",               "title":"Final state gen electrons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSGenElectron_vertex_x":           {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_y":           {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_z":           {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
   
    "n_FSRGenTau":                      {"name":"n_FSRGenTau",                  "title":"Number of final state gen taus",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSRGenTau_e":                      {"name":"FSRGenTau_e",                  "title":"Final state gen taus energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_p":                      {"name":"FSRGenTau_p",                  "title":"Final state gen taus p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_pt":                     {"name":"FSRGenTau_pt",                 "title":"Final state gen taus p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_px":                     {"name":"FSRGenTau_px",                 "title":"Final state gen taus p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_py":                     {"name":"FSRGenTau_py",                 "title":"Final state gen taus p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_pz":                     {"name":"FSRGenTau_pz",                 "title":"Final state gen taus p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_y":                      {"name":"FSRGenTau_y",                  "title":"Final state gen taus rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSRGenTau_eta":                    {"name":"FSRGenTau_eta",                "title":"Final state gen taus #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTau_theta":                  {"name":"FSRGenTau_theta",              "title":"Final state gen taus #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTau_phi":                    {"name":"FSRGenTau_phi",                "title":"Final state gen taus #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTau_charge":                 {"name":"FSRGenTau_charge",             "title":"Final state gen taus charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSRGenTau_mass":                   {"name":"FSRGenTau_mass",               "title":"Final state gen taus mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSRGenTau_vertex_x":               {"name":"FSRGenTau_vertex_x", "title":"Final state gen #tau^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSRGenTau_vertex_y":               {"name":"FSRGenTau_vertex_y", "title":"Final state gen #tau^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSRGenTau_vertex_z":               {"name":"FSRGenTau_vertex_z", "title":"Final state gen #tau^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},

    #"n_TauNeg_MuNuNu":                  {"name":"n_TauNeg_MuNuNu",          "title":"Number of #tau^{-} decays into #mu #nu #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_MuNuNu_Phot":             {"name":"n_TauNeg_MuNuNu_Phot",     "title":"Number of #tau^{-} decays into #mu #nu #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_ENuNu":                   {"name":"n_TauNeg_ENuNu",           "title":"Number of #tau^{-} decays into e #nu #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_ENuNu_Phot":              {"name":"n_TauNeg_ENuNu_Phot",      "title":"Number of #tau^{-} decays into e #nu #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiNu":                    {"name":"n_TauNeg_PiNu",            "title":"Number of #tau^{-} decays into #pi #nu per events",                "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiNu_Phot":               {"name":"n_TauNeg_PiNu_Phot",       "title":"Number of #tau^{-} decays into #pi #nu #gamma per events",         "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KNu":                     {"name":"n_TauNeg_KNu",             "title":"Number of #tau^{-} decays into K #nu per events",                  "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KNu_Phot":                {"name":"n_TauNeg_KNu_Phot",        "title":"Number of #tau^{-} decays into K #nu #gamma per events",           "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiK0Nu":                  {"name":"n_TauNeg_PiK0Nu",          "title":"Number of #tau^{-} decays into #pi K^{0} #nu per events",          "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiK0Nu_Phot":             {"name":"n_TauNeg_PiK0Nu_Phot",     "title":"Number of #tau^{-} decays into #pi K^{0} #nu #gamma per events",   "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KK0Nu":                   {"name":"n_TauNeg_KK0Nu",           "title":"Number of #tau^{-} decays into K K^{0} #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KK0Nu_Phot":              {"name":"n_TauNeg_KK0Nu_Phot",      "title":"Number of #tau^{-} decays into K K^{0} #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_3PiNu":                   {"name":"n_TauNeg_3PiNu",           "title":"Number of #tau^{-} decays into 3 #pi #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_3PiNu_Phot":              {"name":"n_TauNeg_3PiNu_Phot",      "title":"Number of #tau^{-} decays into 3 #pi #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiKKNu":                  {"name":"n_TauNeg_PiKKNu",          "title":"Number of #tau^{-} decays into #pi K K #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiKKNu_Phot":             {"name":"n_TauNeg_PiKKNu_Phot",     "title":"Number of #tau^{-} decays into #pi K K #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},

    #"n_TauPos_MuNuNu":                  {"name":"n_TauPos_MuNuNu",          "title":"Number of #tau^{+} decays into #mu #nu #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauPos_MuNuNu_Phot":             {"name":"n_TauPos_MuNuNu_Phot",     "title":"Number of #tau^{+} decays into #mu #nu #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_ENuNu":                   {"name":"n_TauPos_ENuNu",           "title":"Number of #tau^{+} decays into e #nu #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_ENuNu_Phot":              {"name":"n_TauPos_ENuNu_Phot",      "title":"Number of #tau^{+} decays into e #nu #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiNu":                    {"name":"n_TauPos_PiNu",            "title":"Number of #tau^{+} decays into #pi #nu per events",                "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiNu_Phot":               {"name":"n_TauPos_PiNu_Phot",       "title":"Number of #tau^{+} decays into #pi #nu #gamma per events",         "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KNu":                     {"name":"n_TauPos_KNu",             "title":"Number of #tau^{+} decays into K #nu per events",                  "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KNu_Phot":                {"name":"n_TauPos_KNu_Phot",        "title":"Number of #tau^{+} decays into K #nu #gamma per events",           "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiK0Nu":                  {"name":"n_TauPos_PiK0Nu",          "title":"Number of #tau^{+} decays into #pi K^{0} #nu per events",          "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiK0Nu_Phot":             {"name":"n_TauPos_PiK0Nu_Phot",     "title":"Number of #tau^{+} decays into #pi K^{0} #nu #gamma per events",   "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KK0Nu":                   {"name":"n_TauPos_KK0Nu",           "title":"Number of #tau^{+} decays into K K^{0} #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KK0Nu_Phot":              {"name":"n_TauPos_KK0Nu_Phot",      "title":"Number of #tau^{+} decays into K K^{0} #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_3PiNu":                   {"name":"n_TauPos_3PiNu",           "title":"Number of #tau^{+} decays into 3 #pi #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_3PiNu_Phot":              {"name":"n_TauPos_3PiNu_Phot",      "title":"Number of #tau^{+} decays into 3 #pi #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiKKNu":                  {"name":"n_TauPos_PiKKNu",          "title":"Number of #tau^{+} decays into #pi K K #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiKKNu_Phot":             {"name":"n_TauPos_PiKKNu_Phot",     "title":"Number of #tau^{+} decays into #pi K K #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},

    "n_FSGenNeutrino":                  {"name":"n_FSGenNeutrino",                  "title":"Number of final state gen neutrinos",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenNeutrino_e":                  {"name":"FSGenNeutrino_e",                  "title":"Final state gen neutrinos energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_p":                  {"name":"FSGenNeutrino_p",                  "title":"Final state gen neutrinos p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_pt":                 {"name":"FSGenNeutrino_pt",                 "title":"Final state gen neutrinos p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_px":                 {"name":"FSGenNeutrino_px",                 "title":"Final state gen neutrinos p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_py":                 {"name":"FSGenNeutrino_py",                 "title":"Final state gen neutrinos p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_pz":                 {"name":"FSGenNeutrino_pz",                 "title":"Final state gen neutrinos p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_y":                  {"name":"FSGenNeutrino_y",                  "title":"Final state gen neutrinos rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenNeutrino_eta":                {"name":"FSGenNeutrino_eta",                "title":"Final state gen neutrinos #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenNeutrino_theta":              {"name":"FSGenNeutrino_theta",              "title":"Final state gen neutrinos #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":                {"name":"FSGenNeutrino_phi",                "title":"Final state gen neutrinos #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenNeutrino_charge":             {"name":"FSGenNeutrino_charge",             "title":"Final state gen neutrinos charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
                                        
    "n_FSGenPhoton":                    {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenPhoton_e":                    {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_p":                    {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_pt":                   {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_px":                   {"name":"FSGenPhoton_px",                 "title":"Final state gen photons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_py":                   {"name":"FSGenPhoton_py",                 "title":"Final state gen photons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_pz":                   {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_y":                    {"name":"FSGenPhoton_y",                  "title":"Final state gen photons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenPhoton_eta":                  {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenPhoton_theta":                {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                  {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenPhoton_charge":               {"name":"FSGenPhoton_charge",             "title":"Final state gen photons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},

    "n_GenHiggs":                       {"name":"n_GenHiggs",                  "title":"Number of gen Higgs",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "GenHiggs_e":                       {"name":"GenHiggs_e",                  "title":"Gen Higgs energy [GeV]",           "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_p":                       {"name":"GenHiggs_p",                  "title":"Gen Higgs p [GeV]",                "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_pt":                      {"name":"GenHiggs_pt",                 "title":"Gen Higgs p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_px":                      {"name":"GenHiggs_px",                 "title":"Gen Higgs p_{x} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_py":                      {"name":"GenHiggs_py",                 "title":"Gen Higgs p_{y} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_pz":                      {"name":"GenHiggs_pz",                 "title":"Gen Higgs p_{z} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_y":                       {"name":"GenHiggs_y",                  "title":"Gen Higgs rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "GenHiggs_mass":                    {"name":"GenHiggs_y",                  "title":"Gen Higgs M [GeV]",                "bin":50, "xmin":90, "xmax":140},
    "GenHiggs_eta":                     {"name":"GenHiggs_eta",                "title":"Gen Higgs #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "GenHiggs_theta":                   {"name":"GenHiggs_theta",              "title":"Gen Higgs #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "GenHiggs_phi":                     {"name":"GenHiggs_phi",                "title":"Gen Higgs #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "GenHiggs_charge":                  {"name":"GenHiggs_charge",             "title":"Gen Higgs charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},

    "GenZ_e":                       {"name":"GenZ_e",                  "title":"Gen Z energy [GeV]",           "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_p":                       {"name":"GenZ_p",                  "title":"Gen Z p [GeV]",                "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_pt":                      {"name":"GenZ_pt",                 "title":"Gen Z p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_px":                      {"name":"GenZ_px",                 "title":"Gen Z p_{x} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_py":                      {"name":"GenZ_py",                 "title":"Gen Z p_{y} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_pz":                      {"name":"GenZ_pz",                 "title":"Gen Z p_{z} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_y":                       {"name":"GenZ_y",                  "title":"Gen Z rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "GenZ_mass":                    {"name":"GenZ_y",                  "title":"Gen Z M [GeV]",                "bin":50, "xmin":90, "xmax":140},
    "GenZ_eta":                     {"name":"GenZ_eta",                "title":"Gen Z #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "GenZ_theta":                   {"name":"GenZ_theta",              "title":"Gen Z #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "GenZ_phi":                     {"name":"GenZ_phi",                "title":"Gen Z #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},

    "FSGenZLead_px":               {"name":"FSGenZLead_px",                 "title":"Gen leading Z daughter p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZLead_py":               {"name":"FSGenZLead_py",                 "title":"Gen leading Z daughter p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZLead_pz":               {"name":"FSGenZLead_pz",                 "title":"Gen leading Z daughter p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZLead_p":                {"name":"FSGenZLead_p",                  "title":"Gen leading Z daughter p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZLead_pt":               {"name":"FSGenZLead_pt",                 "title":"Gen leading Z daughter p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZLead_e":                {"name":"FSGenZLead_e",                  "title":"Gen leading Z daughter energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenZLead_eta":              {"name":"FSGenZLead_eta",                "title":"Gen leading Z daughter #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZLead_phi":              {"name":"FSGenZLead_phi",                "title":"Gen leading Z daughter #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZLead_theta":            {"name":"FSGenZLead_theta",              "title":"Gen leading Z daughter #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenZLead_y":                {"name":"FSGenZLead_y",                  "title":"Gen leading Z daughter rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSGenZLead_mass":             {"name":"FSGenZLead_mass",               "title":"Gen leading Z daughter mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSGenZSub_px":                {"name":"FSGenZSub_px",                 "title":"Gen subleading Z daughter p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZSub_py":                {"name":"FSGenZSub_py",                 "title":"Gen subleading Z daughter p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZSub_pz":                {"name":"FSGenZSub_pz",                 "title":"Gen subleading Z daughter p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZSub_p":                 {"name":"FSGenZSub_p",                  "title":"Gen subleading Z daughter p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZSub_pt":                {"name":"FSGenZSub_pt",                 "title":"Gen subleading Z daughter p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZSub_e":                 {"name":"FSGenZSub_e",                  "title":"Gen subleading Z daughter energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenZSub_eta":               {"name":"FSGenZSub_eta",                "title":"Gen subleading Z daughter #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZSub_phi":               {"name":"FSGenZSub_phi",                "title":"Gen subleading Z daughter #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZSub_theta":             {"name":"FSGenZSub_theta",              "title":"Gen subleading Z daughter #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenZSub_y":                 {"name":"FSGenZSub_y",                  "title":"Gen subleading Z daughter rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSGenZSub_mass":              {"name":"FSGenZSub_mass",               "title":"Gen subleading Z daughter mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSGenZP_px":               {"name":"FSGenZP_px",                 "title":"Gen positive Z daughter p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZP_py":               {"name":"FSGenZP_py",                 "title":"Gen positive Z daughter p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZP_pz":               {"name":"FSGenZP_pz",                 "title":"Gen positive Z daughter p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSGenZP_p":                {"name":"FSGenZP_p",                  "title":"Gen positive Z daughter p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZP_pt":               {"name":"FSGenZP_pt",                 "title":"Gen positive Z daughter p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZP_e":                {"name":"FSGenZP_e",                  "title":"Gen positive Z daughter energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenZP_eta":              {"name":"FSGenZP_eta",                "title":"Gen positive Z daughter #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZP_phi":              {"name":"FSGenZP_phi",                "title":"Gen positive Z daughter #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZP_theta":            {"name":"FSGenZP_theta",              "title":"Gen positive Z daughter #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenZP_y":                {"name":"FSGenZP_y",                  "title":"Gen positive Z daughter rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSGenZP_mass":             {"name":"FSGenZP_mass",               "title":"Gen positive Z daughter mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSGenZM_px":                {"name":"FSGenZM_px",                 "title":"Gen negative Z daughter p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZM_py":                {"name":"FSGenZM_py",                 "title":"Gen negative Z daughter p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZM_pz":                {"name":"FSGenZM_pz",                 "title":"Gen negative Z daughter p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSGenZM_p":                 {"name":"FSGenZM_p",                  "title":"Gen negative Z daughter p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZM_pt":                {"name":"FSGenZM_pt",                 "title":"Gen negative Z daughter p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSGenZM_e":                 {"name":"FSGenZM_e",                  "title":"Gen negative Z daughter energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenZM_eta":               {"name":"FSGenZM_eta",                "title":"Gen negative Z daughter #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZM_phi":               {"name":"FSGenZM_phi",                "title":"Gen negative Z daughter #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZM_theta":             {"name":"FSGenZM_theta",              "title":"Gen negative Z daughter #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenZM_y":                 {"name":"FSGenZM_y",                  "title":"Gen negative Z daughter rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSGenZM_mass":              {"name":"FSGenZM_mass",               "title":"Gen negative Z daughter mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSRGenTauLead_px":               {"name":"FSRGenTauLead_px",                 "title":"#tau_{leading} p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauLead_py":               {"name":"FSRGenTauLead_py",                 "title":"#tau_{leading} p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauLead_pz":               {"name":"FSRGenTauLead_pz",                 "title":"#tau_{leading} p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauLead_p":                {"name":"FSRGenTauLead_p",                  "title":"#tau_{leading} p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauLead_pt":               {"name":"FSRGenTauLead_pt",                 "title":"#tau_{leading} p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauLead_e":                {"name":"FSRGenTauLead_e",                  "title":"#tau_{leading} energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTauLead_eta":              {"name":"FSRGenTauLead_eta",                "title":"#tau_{leading} #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauLead_phi":              {"name":"FSRGenTauLead_phi",                "title":"#tau_{leading} #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauLead_theta":            {"name":"FSRGenTauLead_theta",              "title":"#tau_{leading} #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTauLead_y":                {"name":"FSRGenTauLead_y",                  "title":"#tau_{leading} rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSRGenTauLead_mass":             {"name":"FSRGenTauLead_mass",               "title":"#tau_{leading} mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSRGenTauSub_px":                {"name":"FSRGenTauSub_px",                 "title":"#tau_{subleading} p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauSub_py":                {"name":"FSRGenTauSub_py",                 "title":"#tau_{subleading} p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauSub_pz":                {"name":"FSRGenTauSub_pz",                 "title":"#tau_{subleading} p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauSub_p":                 {"name":"FSRGenTauSub_p",                  "title":"#tau_{subleading} p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauSub_pt":                {"name":"FSRGenTauSub_pt",                 "title":"#tau_{subleading} p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauSub_e":                 {"name":"FSRGenTauSub_e",                  "title":"#tau_{subleading} energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTauSub_eta":               {"name":"FSRGenTauSub_eta",                "title":"#tau_{subleading} #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauSub_phi":               {"name":"FSRGenTauSub_phi",                "title":"#tau_{subleading} #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauSub_theta":             {"name":"FSRGenTauSub_theta",              "title":"#tau_{subleading} #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTauSub_y":                 {"name":"FSRGenTauSub_y",                  "title":"#tau_{subleading} rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSRGenTauSub_mass":              {"name":"FSRGenTauSub_mass",               "title":"#tau_{subleading} mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSRGenTauP_px":               {"name":"FSRGenTauP_px",                 "title":"#tau^{+} p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauP_py":               {"name":"FSRGenTauP_py",                 "title":"#tau^{+} p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauP_pz":               {"name":"FSRGenTauP_pz",                 "title":"#tau^{+} p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},   
    "FSRGenTauP_p":                {"name":"FSRGenTauP_p",                  "title":"#tau^{+} p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauP_pt":               {"name":"FSRGenTauP_pt",                 "title":"#tau^{+} p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauP_e":                {"name":"FSRGenTauP_e",                  "title":"#tau^{+} energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTauP_eta":              {"name":"FSRGenTauP_eta",                "title":"#tau^{+} #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauP_phi":              {"name":"FSRGenTauP_phi",                "title":"#tau^{+} #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauP_theta":            {"name":"FSRGenTauP_theta",              "title":"#tau^{+} #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTauP_y":                {"name":"FSRGenTauP_y",                  "title":"#tau^{+} rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSRGenTauP_mass":             {"name":"FSRGenTauP_mass",               "title":"#tau^{+} mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSRGenTauM_px":                {"name":"FSRGenTauM_px",                 "title":"#tau^{-} p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauM_py":                {"name":"FSRGenTauM_py",                 "title":"#tau^{-} p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauM_pz":                {"name":"FSRGenTauM_pz",                 "title":"#tau^{-} p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100}, 
    "FSRGenTauM_p":                 {"name":"FSRGenTauM_p",                  "title":"#tau^{-} p [GeV]",                "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauM_pt":                {"name":"FSRGenTauM_pt",                 "title":"#tau^{-} p_{T} [GeV]",            "bin":50,"xmin":0 ,"xmax":100},
    "FSRGenTauM_e":                 {"name":"FSRGenTauM_e",                  "title":"#tau^{-} energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTauM_eta":               {"name":"FSRGenTauM_eta",                "title":"#tau^{-} #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauM_phi":               {"name":"FSRGenTauM_phi",                "title":"#tau^{-} #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTauM_theta":             {"name":"FSRGenTauM_theta",              "title":"#tau^{-} #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTauM_y":                 {"name":"FSRGenTauM_y",                  "title":"#tau^{-} rapidity",               "bin":80, "xmin":-4., "xmax":4.},
    "FSRGenTauM_mass":              {"name":"FSRGenTauM_mass",               "title":"#tau^{-} mass",                   "bin":30, "xmin":0., "xmax":3.},

    "FSRGenTau_DPhi":         {"name":"FSRGenTau_DPhi",           "title":"#Delta#phi(#tau#tau)",                                "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTau_DR":                   {"name":"FSRGenTau_DR",                     "title":"#Delta R(#tau#tau)",                  "bin":70, "xmin":0,"xmax":7},
    "FSRGenTau_cos":                  {"name":"FSRGenTau_cos",                    "title":"cos#theta(#tau#tau)",                 "bin":100, "xmin":-1.,"xmax":1.},
    "FSRGenTau_DEta":                             {"name":"FSRGenTau_DEta",           "title":"Gen di-#tau #Delta#eta",                                  "bin":128, "xmin":-6.4,"xmax":6.4},

    "FSGenZDaughter_DPhi":         {"name":"FSGenZDaughter_DPhi",           "title":"#Delta#phi(ll)",                                "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZDaughter_DR":                   {"name":"FSGenZDaughter_DR",                     "title":"#Delta R(ll)",                  "bin":70, "xmin":0,"xmax":7},
    "FSGenZDaughter_cos":                  {"name":"FSGenZDaughter_cos",                    "title":"cos#theta(ll)",                 "bin":100, "xmin":-1.,"xmax":1.},
    "FSGenZDaughter_DEta":                   {"name":"FSGenZDaughter_DEta",           "title":"Gen Z daughters #Delta#eta",                                  "bin":128, "xmin":-6.4,"xmax":6.4},

    #### CP variables

    "FSRGenTau_DEta_y":                             {"name":"FSRGenTau_DEta_y",           "title":"Gen di-#tau #Delta#eta",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSRGenTau_DPhi_y":                           {"name":"FSRGenTau_DPhi_y",           "title":"#Delta#phi(#tau#tau)",                                "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZDaughter_DEta_y":                 {"name":"FSGenZDaughter_DEta_y",           "title":"Gen Z daughters #Delta#eta",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenZDaughter_DPhi_y":                 {"name":"FSGenZDaughter_DPhi_y",           "title":"Gen Z daughters #Delta#phi",                                  "bin":128, "xmin":-6.4,"xmax":6.4},

    "HRF_GenTauLead_px":                 {"name":"HRF_GenTauLead_px",                 "title":"Gen #tau_{fing} p_{x} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauLead_py":                 {"name":"HRF_GenTauLead_py",                 "title":"Gen #tau_{leading} p_{y} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauLead_pz":                 {"name":"HRF_GenTauLead_pz",                 "title":"Gen #tau_{leading} p_{z} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauLead_p":                  {"name":"HRF_GenTauLead_p",                  "title":"Gen #tau_{leading} p [GeV] in H rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauLead_pt":                 {"name":"HRF_GenTauLead_pt",                 "title":"Gen #tau_{leading} p_{T} [GeV] in H rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauLead_e":                  {"name":"HRF_GenTauLead_e",                  "title":"Gen #tau_{leading} energy [GeV] in H rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauLead_eta":                {"name":"HRF_GenTauLead_eta",                "title":"Gen #tau_{leading} #eta in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauLead_phi":                {"name":"HRF_GenTauLead_phi",                "title":"Gen #tau_{leading} #phi in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauLead_theta":              {"name":"HRF_GenTauLead_theta",              "title":"Gen #tau_{leading} #theta in H rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "HRF_GenTauLead_y":                  {"name":"HRF_GenTauLead_y",                  "title":"Gen #tau_{leading} rapidity in H rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "HRF_GenTauSub_px":                 {"name":"HRF_GenTauSub_px",                 "title":"Gen #tau_{subleading} p_{x} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauSub_py":                 {"name":"HRF_GenTauSub_py",                 "title":"Gen #tau_{subleading} p_{y} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauSub_pz":                 {"name":"HRF_GenTauSub_pz",                 "title":"Gen #tau_{subleading} p_{z} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauSub_p":                  {"name":"HRF_GenTauSub_p",                  "title":"Gen #tau_{subleading} p [GeV] in H rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauSub_pt":                 {"name":"HRF_GenTauSub_pt",                 "title":"Gen #tau_{subleading} p_{T} [GeV] in H rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauSub_e":                  {"name":"HRF_GenTauSub_e",                  "title":"Gen #tau_{subleading} energy [GeV] in H rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauSub_eta":                {"name":"HRF_GenTauSub_eta",                "title":"Gen #tau_{subleading} #eta in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauSub_phi":                {"name":"HRF_GenTauSub_phi",                "title":"Gen #tau_{subleading} #phi in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauSub_theta":              {"name":"HRF_GenTauSub_theta",              "title":"Gen #tau_{subleading} #theta in H rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "HRF_GenTauSub_y":                  {"name":"HRF_GenTauSub_y",                  "title":"Gen #tau_{subleading} rapidity in H rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "HRF_GenTauP_px":                 {"name":"HRF_GenTauP_px",                 "title":"Gen #tau^{+} p_{x} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauP_py":                 {"name":"HRF_GenTauP_py",                 "title":"Gen #tau^{+} p_{y} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauP_pz":                 {"name":"HRF_GenTauP_pz",                 "title":"Gen #tau^{+} p_{z} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauP_p":                  {"name":"HRF_GenTauP_p",                  "title":"Gen #tau^{+} p [GeV] in H rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauP_pt":                 {"name":"HRF_GenTauP_pt",                 "title":"Gen #tau^{+} p_{T} [GeV] in H rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauP_e":                  {"name":"HRF_GenTauP_e",                  "title":"Gen #tau^{+} energy [GeV] in H rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauP_eta":                {"name":"HRF_GenTauP_eta",                "title":"Gen #tau^{+} #eta in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauP_phi":                {"name":"HRF_GenTauP_phi",                "title":"Gen #tau^{+} #phi in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauP_theta":              {"name":"HRF_GenTauP_theta",              "title":"Gen #tau^{+} #theta in H rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "HRF_GenTauP_y":                  {"name":"HRF_GenTauP_y",                  "title":"Gen #tau^{+} rapidity in H rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "HRF_GenTauM_px":                 {"name":"HRF_GenTauM_px",                 "title":"Gen #tau^{-} p_{x} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauM_py":                 {"name":"HRF_GenTauM_py",                 "title":"Gen #tau^{-} p_{y} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauM_pz":                 {"name":"HRF_GenTauM_pz",                 "title":"Gen #tau^{-} p_{z} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTauM_p":                  {"name":"HRF_GenTauM_p",                  "title":"Gen #tau^{-} p [GeV] in H rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauM_pt":                 {"name":"HRF_GenTauM_pt",                 "title":"Gen #tau^{-} p_{T} [GeV] in H rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauM_e":                  {"name":"HRF_GenTauM_e",                  "title":"Gen #tau^{-} energy [GeV] in H rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTauM_eta":                {"name":"HRF_GenTauM_eta",                "title":"Gen #tau^{-} #eta in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauM_phi":                {"name":"HRF_GenTauM_phi",                "title":"Gen #tau^{-} #phi in H rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTauM_theta":              {"name":"HRF_GenTauM_theta",              "title":"Gen #tau^{-} #theta in H rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "HRF_GenTauM_y":                  {"name":"HRF_GenTauM_y",                  "title":"Gen #tau^{-} rapidity in H rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "HRF_GenTau_DEta":                   {"name":"HRF_GenTau_DEta",           "title":"Gen di-#tau #Delta#eta in H rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTau_DPhi":           {"name":"HRF_GenTau_DPhi",           "title":"Gen di-#tau #Delta#phi in H rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTau_DEta_y":                   {"name":"HRF_GenTau_DEta_y",           "title":"Gen di-#tau #Delta#eta in H rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "HRF_GenTau_DPhi_y":           {"name":"HRF_GenTau_DPhi_y",           "title":"Gen di-#tau #Delta#phi in H rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},

    "ZRF_GenZLead_px":                 {"name":"ZRF_GenZLead_px",                 "title":"Gen leading Z daughter p_{x} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZLead_py":                 {"name":"ZRF_GenZLead_py",                 "title":"Gen leading Z daughter p_{y} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZLead_pz":                 {"name":"ZRF_GenZLead_pz",                 "title":"Gen leading Z daughter p_{z} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZLead_p":                  {"name":"ZRF_GenZLead_p",                  "title":"Gen leading Z daughter p [GeV] in Z rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZLead_pt":                 {"name":"ZRF_GenZLead_pt",                 "title":"Gen leading Z daughter p_{T} [GeV] in Z rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZLead_e":                  {"name":"ZRF_GenZLead_e",                  "title":"Gen leading Z daughter energy [GeV] in Z rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZLead_eta":                {"name":"ZRF_GenZLead_eta",                "title":"Gen leading Z daughter #eta in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZLead_phi":                {"name":"ZRF_GenZLead_phi",                "title":"Gen leading Z daughter #phi in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZLead_theta":              {"name":"ZRF_GenZLead_theta",              "title":"Gen leading Z daughter #theta in Z rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "ZRF_GenZLead_y":                  {"name":"ZRF_GenZLead_y",                  "title":"Gen leading Z daughter rapidity in Z rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "ZRF_GenZSub_px":                 {"name":"ZRF_GenZSub_px",                 "title":"Gen subleading Z daughter p_{x} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZSub_py":                 {"name":"ZRF_GenZSub_py",                 "title":"Gen subleading Z daughter p_{y} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZSub_pz":                 {"name":"ZRF_GenZSub_pz",                 "title":"Gen subleading Z daughter p_{z} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZSub_p":                  {"name":"ZRF_GenZSub_p",                  "title":"Gen subleading Z daughter p [GeV] in Z rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZSub_pt":                 {"name":"ZRF_GenZSub_pt",                 "title":"Gen subleading Z daughter p_{T} [GeV] in Z rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZSub_e":                  {"name":"ZRF_GenZSub_e",                  "title":"Gen subleading Z daughter energy [GeV] in Z rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZSub_eta":                {"name":"ZRF_GenZSub_eta",                "title":"Gen subleading Z daughter #eta in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZSub_phi":                {"name":"ZRF_GenZSub_phi",                "title":"Gen subleading Z daughter #phi in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZSub_theta":              {"name":"ZRF_GenZSub_theta",              "title":"Gen subleading Z daughter #theta in Z rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "ZRF_GenZSub_y":                  {"name":"ZRF_GenZSub_y",                  "title":"Gen subleading Z daughter rapidity in Z rest frame",               "bin":40, "xmin":-4., "xmax":4.},
    
    "ZRF_GenZP_px":                 {"name":"ZRF_GenZP_px",                 "title":"Gen positive Z daughter p_{x} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZP_py":                 {"name":"ZRF_GenZP_py",                 "title":"Gen positive Z daughter p_{y} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZP_pz":                 {"name":"ZRF_GenZP_pz",                 "title":"Gen positive Z daughter p_{z} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZP_p":                  {"name":"ZRF_GenZP_p",                  "title":"Gen positive Z daughter p [GeV] in Z rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZP_pt":                 {"name":"ZRF_GenZP_pt",                 "title":"Gen positive Z daughter p_{T} [GeV] in Z rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZP_e":                  {"name":"ZRF_GenZP_e",                  "title":"Gen positive Z daughter energy [GeV] in Z rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZP_eta":                {"name":"ZRF_GenZP_eta",                "title":"Gen positive Z daughter #eta in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZP_phi":                {"name":"ZRF_GenZP_phi",                "title":"Gen positive Z daughter #phi in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZP_theta":              {"name":"ZRF_GenZP_theta",              "title":"Gen positive Z daughter #theta in Z rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "ZRF_GenZP_y":                  {"name":"ZRF_GenZP_y",                  "title":"Gen positive Z daughter rapidity in Z rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "ZRF_GenZM_px":                 {"name":"ZRF_GenZM_px",                 "title":"Gen negative Z daughter p_{x} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZM_py":                 {"name":"ZRF_GenZM_py",                 "title":"Gen negative Z daughter p_{y} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZM_pz":                 {"name":"ZRF_GenZM_pz",                 "title":"Gen negative Z daughter p_{z} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZM_p":                  {"name":"ZRF_GenZM_p",                  "title":"Gen negative Z daughter p [GeV] in Z rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZM_pt":                 {"name":"ZRF_GenZM_pt",                 "title":"Gen negative Z daughter p_{T} [GeV] in Z rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZM_e":                  {"name":"ZRF_GenZM_e",                  "title":"Gen negative Z daughter energy [GeV] in Z rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZM_eta":                {"name":"ZRF_GenZM_eta",                "title":"Gen negative Z daughter #eta in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZM_phi":                {"name":"ZRF_GenZM_phi",                "title":"Gen negative Z daughter #phi in Z rest frame",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZM_theta":              {"name":"ZRF_GenZM_theta",              "title":"Gen negative Z daughter #theta in Z rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "ZRF_GenZM_y":                  {"name":"ZRF_GenZM_y",                  "title":"Gen negative Z daughter rapidity in Z rest frame",               "bin":40, "xmin":-4., "xmax":4.},

    "ZRF_GenZDaughter_DEta":                   {"name":"ZRF_GenZDaughter_DEta",           "title":"Gen Z daughters #Delta#eta in Z rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZDaughter_DPhi":           {"name":"ZRF_GenZDaughter_DPhi",           "title":"Gen Z daughters #Delta#phi in Z rest frame",                          "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZDaughter_DEta_y":                   {"name":"ZRF_GenZDaughter_DEta_y",           "title":"Gen Z daughters #Delta#eta in Z rest frame",                                  "bin":128, "xmin":-6.4,"xmax":6.4},
    "ZRF_GenZDaughter_DPhi_y":           {"name":"ZRF_GenZDaughter_DPhi_y",           "title":"Gen Z daughters #Delta#phi in Z rest frame",                          "bin":128, "xmin":-6.4,"xmax":6.4},

    "GenThetastar":           {"name":"GenThetastar",         "title":"Gen #theta^{*}",                  "bin":32, "xmin":0,"xmax":3.2},
    "GenTheta2":              {"name":"GenTheta2",            "title":"Gen #theta_{2}",                  "bin":32, "xmin":0,"xmax":3.2},
    "GenPhi1":                {"name":"GenPhi1",              "title":"Gen #phi_{1}",                    "bin":32, "xmin":0,"xmax":3.2},
    "GenPhi":                 {"name":"GenPhi",               "title":"Gen #phi",                        "bin":32, "xmin":0,"xmax":3.2},
    "GenTheta1":              {"name":"GenTheta1",            "title":"Gen #theta_{1}",                  "bin":32, "xmin":0,"xmax":3.2},

    "GenThetastar_cos":           {"name":"GenThetastar_cos",         "title":"Gen cos#theta^{*}",                  "bin":50, "xmin":-1.,"xmax":1.},
    "GenTheta2_cos":              {"name":"GenTheta2_cos",            "title":"Gen cos#theta_{2}",                  "bin":50, "xmin":-1.,"xmax":1.},
    "GenPhi1_cos":                {"name":"GenPhi1_cos",              "title":"Gen cos#phi_{1}",                    "bin":50, "xmin":-1.,"xmax":1.},
    "GenPhi_cos":                 {"name":"GenPhi_cos",               "title":"Gen cos#phi",                        "bin":50, "xmin":-1.,"xmax":1.},
    "GenTheta1_cos":              {"name":"GenTheta1_cos",            "title":"Gen cos#theta_{1}",                  "bin":50, "xmin":-1.,"xmax":1.},

    "GenRecoil":                   {"name":"GenRecoil",                   "title":"Gen M_{recoil} [GeV]",                     "bin":80, "xmin":80., "xmax":160.},
    

}
