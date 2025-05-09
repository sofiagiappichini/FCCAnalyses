#Input directory where the files produced at the stage1 level are
#inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/" 
inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/efficiency/ktN"

#Optional: output directory, default is local running directory
#outputDir   = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/efficiency/jet/" 
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/efficiency/ktN"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = False

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 1

#produces ROOT TTrees, default is False
doTree = False

processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {},
    'wzp6_ee_eeH_Htautau_ecm240': {},
    'wzp6_ee_mumuH_Htautau_ecm240': {},
    'wzp6_ee_bbH_Htautau_ecm240': {},
    'wzp6_ee_ccH_Htautau_ecm240': {},
    'wzp6_ee_ssH_Htautau_ecm240': {},
    'wzp6_ee_qqH_Htautau_ecm240': {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selNone":"true",

    "selTag2-5":"n_events_ktNtag==2",

    "selTag2-5e":"n_events_ktNexcl==2",

    "selGen2":"n_GenTau_had==2",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    ######## Monte-Carlo particles #######
    "n_FSGenElectron":                  {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenElectron_e":                  {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_p":                  {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_pt":                 {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_px":                 {"name":"FSGenElectron_px",                 "title":"Final state gen electrons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_py":                 {"name":"FSGenElectron_py",                 "title":"Final state gen electrons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_pz":                 {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_y":                  {"name":"FSGenElectron_y",                  "title":"Final state gen electrons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenElectron_eta":                {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenElectron_theta":              {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":                {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenElectron_charge":             {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenElectron_mass":               {"name":"FSGenElectron_mass",               "title":"Final state gen electrons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSGenElectron_parentPDG":          {"name":"FSGenElectron_parentPDG",          "title":"Final state gen electrons parent PDG",             "bin":30, "xmin":0., "xmax":30.},
    "FSGenElectron_vertex_x":           {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_y":           {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_z":           {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},

    "n_FSGenMuon":                      {"name":"n_FSGenMuon",                  "title":"Number of final state gen muons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenMuon_e":                      {"name":"FSGenMuon_e",                  "title":"Final state gen muons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_p":                      {"name":"FSGenMuon_p",                  "title":"Final state gen muons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_pt":                     {"name":"FSGenMuon_pt",                 "title":"Final state gen muons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_px":                     {"name":"FSGenMuon_px",                 "title":"Final state gen muons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_py":                     {"name":"FSGenMuon_py",                 "title":"Final state gen muons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_pz":                     {"name":"FSGenMuon_pz",                 "title":"Final state gen muons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_y":                      {"name":"FSGenMuon_y",                  "title":"Final state gen muons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenMuon_eta":                    {"name":"FSGenMuon_eta",                "title":"Final state gen muons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenMuon_theta":                  {"name":"FSGenMuon_theta",              "title":"Final state gen muons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenMuon_phi":                    {"name":"FSGenMuon_phi",                "title":"Final state gen muons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenMuon_charge":                 {"name":"FSGenMuon_charge",             "title":"Final state gen muons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenMuon_mass":                   {"name":"FSGenMuon_mass",               "title":"Final state gen muons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSGenMuon_parentPDG":              {"name":"FSGenMuon_parentPDG",          "title":"Final state gen muons parent PDG",             "bin":30, "xmin":0., "xmax":30.},
    "FSGenMuon_vertex_x":               {"name":"FSGenMuon_vertex_x", "title":"Final state gen #mu^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenMuon_vertex_y":               {"name":"FSGenMuon_vertex_y", "title":"Final state gen #mu^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenMuon_vertex_z":               {"name":"FSGenMuon_vertex_z", "title":"Final state gen #mu^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},

    ######## Reconstructed particles #######

    "n_RecoElectrons":                  {"name":"n_RecoElectrons",                  "title":"Number of reco electrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoElectron_e":                   {"name":"RecoElectron_e",                   "title":"Reco electron energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_p":                   {"name":"RecoElectron_p",                   "title":"Reco electron p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_pt":                  {"name":"RecoElectron_pt",                  "title":"Reco electron p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_px":                  {"name":"RecoElectron_px",                  "title":"Reco electron p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_py":                  {"name":"RecoElectron_py",                  "title":"Reco electron p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_pz":                  {"name":"RecoElectron_pz",                  "title":"Reco electron p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_y":                   {"name":"RecoElectron_y",                   "title":"Reco electron rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoElectron_eta":                 {"name":"RecoElectron_eta",                 "title":"Reco electron #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_theta":               {"name":"RecoElectron_theta",               "title":"Reco electron #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":                 {"name":"RecoElectron_phi",                 "title":"Reco electron #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":              {"name":"RecoElectron_charge",              "title":"Reco electron charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoElectron_mass":                {"name":"RecoElectron_mass",                "title":"Reco electron mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoElectronTrack_absD0":          {"name":"RecoElectronTrack_absD0",          "title":"Reco electron tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absZ0":          {"name":"RecoElectronTrack_absZ0",          "title":"Reco electron tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absD0sig":       {"name":"RecoElectronTrack_absD0sig",       "title":"Reco electron tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absZ0sig":       {"name":"RecoElectronTrack_absZ0sig",       "title":"Reco electron tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_D0cov":          {"name":"RecoElectronTrack_D0cov",          "title":"Reco electron tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoElectronTrack_Z0cov":          {"name":"RecoElectronTrack_Z0cov",          "title":"Reco electron tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoElectrons_sel":                  {"name":"n_RecoElectrons_sel",                  "title":"Number of reco isolated electrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoElectron_sel_e":                   {"name":"RecoElectron_sel_e",                   "title":"Reco electron isolated energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_p":                   {"name":"RecoElectron_sel_p",                   "title":"Reco electron isolated p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_pt":                  {"name":"RecoElectron_sel_pt",                  "title":"Reco electron isolated p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_px":                  {"name":"RecoElectron_sel_px",                  "title":"Reco electron isolated p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_py":                  {"name":"RecoElectron_sel_py",                  "title":"Reco electron isolated p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_pz":                  {"name":"RecoElectron_sel_pz",                  "title":"Reco electron isolated p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_y":                   {"name":"RecoElectron_sel_y",                   "title":"Reco electron isolated rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoElectron_sel_eta":                 {"name":"RecoElectron_sel_eta",                 "title":"Reco electron isolated #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_sel_theta":               {"name":"RecoElectron_sel_theta",               "title":"Reco electron isolated #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoElectron_sel_phi":                 {"name":"RecoElectron_sel_phi",                 "title":"Reco electron isolated #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_sel_charge":              {"name":"RecoElectron_sel_charge",              "title":"Reco electron isolated charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoElectron_sel_mass":                {"name":"RecoElectron_sel_mass",                "title":"Reco electron isolated mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoElectronTrack_sel_absD0":          {"name":"RecoElectronTrack_sel_absD0",          "title":"Reco electron isolated tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_sel_absZ0":          {"name":"RecoElectronTrack_sel_absZ0",          "title":"Reco electron isolated tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_sel_absD0sig":       {"name":"RecoElectronTrack_sel_absD0sig",       "title":"Reco electron isolated tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_sel_absZ0sig":       {"name":"RecoElectronTrack_sel_absZ0sig",       "title":"Reco electron isolated tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_sel_D0cov":          {"name":"RecoElectronTrack_sel_D0cov",          "title":"Reco electron isolated tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoElectronTrack_sel_Z0cov":          {"name":"RecoElectronTrack_sel_Z0cov",          "title":"Reco electron isolated tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoMuons":                  {"name":"n_RecoMuons",                  "title":"Number of reco muons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoMuon_e":                   {"name":"RecoMuon_e",                   "title":"Reco muon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_p":                   {"name":"RecoMuon_p",                   "title":"Reco muon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_pt":                  {"name":"RecoMuon_pt",                  "title":"Reco muon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_px":                  {"name":"RecoMuon_px",                  "title":"Reco muon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_py":                  {"name":"RecoMuon_py",                  "title":"Reco muon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_pz":                  {"name":"RecoMuon_pz",                  "title":"Reco muon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_y":                   {"name":"RecoMuon_y",                   "title":"Reco muon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoMuon_eta":                 {"name":"RecoMuon_eta",                 "title":"Reco muon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_theta":               {"name":"RecoMuon_theta",               "title":"Reco muon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":                 {"name":"RecoMuon_phi",                 "title":"Reco muon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":              {"name":"RecoMuon_charge",              "title":"Reco muon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoMuon_mass":                {"name":"RecoMuon_mass",                "title":"Reco muon mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoMuonTrack_absD0":          {"name":"RecoMuonTrack_absD0",          "title":"Reco muon tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absZ0":          {"name":"RecoMuonTrack_absZ0",          "title":"Reco muon tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absD0sig":       {"name":"RecoMuonTrack_absD0sig",       "title":"Reco muon tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absZ0sig":       {"name":"RecoMuonTrack_absZ0sig",       "title":"Reco muon tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_D0cov":          {"name":"RecoMuonTrack_D0cov",          "title":"Reco muon tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoMuonTrack_Z0cov":          {"name":"RecoMuonTrack_Z0cov",          "title":"Reco muon tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoMuons_sel":                  {"name":"n_RecoMuons_sel",                  "title":"Number of reco isolated electrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoMuon_sel_e":                   {"name":"RecoMuon_sel_e",                   "title":"Reco muon isolated energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_p":                   {"name":"RecoMuon_sel_p",                   "title":"Reco muon isolated p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_pt":                  {"name":"RecoMuon_sel_pt",                  "title":"Reco muon isolated p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_px":                  {"name":"RecoMuon_sel_px",                  "title":"Reco muon isolated p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_py":                  {"name":"RecoMuon_sel_py",                  "title":"Reco muon isolated p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_pz":                  {"name":"RecoMuon_sel_pz",                  "title":"Reco muon isolated p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_y":                   {"name":"RecoMuon_sel_y",                   "title":"Reco muon isolated rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoMuon_sel_eta":                 {"name":"RecoMuon_sel_eta",                 "title":"Reco muon isolated #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_sel_theta":               {"name":"RecoMuon_sel_theta",               "title":"Reco muon isolated #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoMuon_sel_phi":                 {"name":"RecoMuon_sel_phi",                 "title":"Reco muon isolated #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_sel_charge":              {"name":"RecoMuon_sel_charge",              "title":"Reco muon isolated charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoMuon_sel_mass":                {"name":"RecoMuon_sel_mass",                "title":"Reco muon isolated mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoMuonTrack_sel_absD0":          {"name":"RecoMuonTrack_sel_absD0",          "title":"Reco muon isolated tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_sel_absZ0":          {"name":"RecoMuonTrack_sel_absZ0",          "title":"Reco muon isolated tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_sel_absD0sig":       {"name":"RecoMuonTrack_sel_absD0sig",       "title":"Reco muon isolated tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_sel_absZ0sig":       {"name":"RecoMuonTrack_sel_absZ0sig",       "title":"Reco muon isolated tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_sel_D0cov":          {"name":"RecoMuonTrack_sel_D0cov",          "title":"Reco muon isolated tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoMuonTrack_sel_Z0cov":          {"name":"RecoMuonTrack_sel_Z0cov",          "title":"Reco muon isolated tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoLeptons":                {"name":"n_RecoLeptons",                  "title":"Number of reco leptons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoLepton_e":                 {"name":"RecoLepton_e",                   "title":"Reco lepton energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_p":                 {"name":"RecoLepton_p",                   "title":"Reco lepton p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_pt":                {"name":"RecoLepton_pt",                  "title":"Reco lepton p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_px":                {"name":"RecoLepton_px",                  "title":"Reco lepton p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_py":                {"name":"RecoLepton_py",                  "title":"Reco lepton p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_pz":                {"name":"RecoLepton_pz",                  "title":"Reco lepton p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_y":                 {"name":"RecoLepton_y",                   "title":"Reco lepton rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoLepton_eta":               {"name":"RecoLepton_eta",                 "title":"Reco lepton #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoLepton_theta":             {"name":"RecoLepton_theta",               "title":"Reco lepton #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoLepton_phi":               {"name":"RecoLepton_phi",                 "title":"Reco lepton #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoLepton_charge":            {"name":"RecoLepton_charge",              "title":"Reco lepton charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoLepton_mass":              {"name":"RecoLepton_mass",                "title":"Reco lepton mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoLeptonTrack_absD0":        {"name":"RecoLeptonTrack_absD0",          "title":"Reco lepton tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoLeptonTrack_absZ0":        {"name":"RecoLeptonTrack_absZ0",          "title":"Reco lepton tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoLeptonTrack_absD0sig":     {"name":"RecoLeptonTrack_absD0sig",       "title":"Reco lepton tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoLeptonTrack_absZ0sig":     {"name":"RecoLeptonTrack_absZ0sig",       "title":"Reco lepton tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoLeptonTrack_D0cov":        {"name":"RecoLeptonTrack_D0cov",          "title":"Reco lepton tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoLeptonTrack_Z0cov":        {"name":"RecoLeptonTrack_Z0cov",          "title":"Reco lepton tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoLeptons_sel":                {"name":"n_RecoLeptons_sel",                  "title":"Number of reco isolated electrons",                     "bin":5, "xmin":-0.5, "xmax":4.},
    "RecoLepton_sel_e":                 {"name":"RecoLepton_sel_e",                   "title":"Reco lepton isolated energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_sel_p":                 {"name":"RecoLepton_sel_p",                   "title":"Reco lepton isolated p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_sel_pt":                {"name":"RecoLepton_sel_pt",                  "title":"Reco lepton isolated p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoLepton_sel_px":                {"name":"RecoLepton_sel_px",                  "title":"Reco lepton isolated p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_sel_py":                {"name":"RecoLepton_sel_py",                  "title":"Reco lepton isolated p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_sel_pz":                {"name":"RecoLepton_sel_pz",                  "title":"Reco lepton isolated p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoLepton_sel_y":                 {"name":"RecoLepton_sel_y",                   "title":"Reco lepton isolated rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoLepton_sel_eta":               {"name":"RecoLepton_sel_eta",                 "title":"Reco lepton isolated #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoLepton_sel_theta":             {"name":"RecoLepton_sel_theta",               "title":"Reco lepton isolated #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoLepton_sel_phi":               {"name":"RecoLepton_sel_phi",                 "title":"Reco lepton isolated #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoLepton_sel_charge":            {"name":"RecoLepton_sel_charge",              "title":"Reco lepton isolated charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoLepton_sel_mass":              {"name":"RecoLepton_sel_mass",                "title":"Reco lepton isolated mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
    "RecoLeptonTrack_sel_absD0":        {"name":"RecoLeptonTrack_sel_absD0",          "title":"Reco lepton isolated tracks |d_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoLeptonTrack_sel_absZ0":        {"name":"RecoLeptonTrack_sel_absZ0",          "title":"Reco lepton isolated tracks |z_{0}| [mm]",            "bin":100,"xmin":0, "xmax":2000},
    "RecoLeptonTrack_sel_absD0sig":     {"name":"RecoLeptonTrack_sel_absD0sig",       "title":"Reco lepton isolated tracks |d_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoLeptonTrack_sel_absZ0sig":     {"name":"RecoLeptonTrack_sel_absZ0sig",       "title":"Reco lepton isolated tracks |z_{0} significance|",    "bin":100,"xmin":0, "xmax":600000},
    "RecoLeptonTrack_sel_D0cov":        {"name":"RecoLeptonTrack_sel_D0cov",          "title":"Reco lepton isolated tracks d_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},
    "RecoLeptonTrack_sel_Z0cov":        {"name":"RecoLeptonTrack_sel_Z0cov",          "title":"Reco lepton isolated tracks z_{0} #sigma^{2}",        "bin":100,"xmin":0, "xmax":0.5},

    "n_RecoPhotons":            {"name":"n_RecoPhotons",                  "title":"Number of reco photons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoPhoton_e":             {"name":"RecoPhoton_e",                   "title":"Reco photon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_p":             {"name":"RecoPhoton_p",                   "title":"Reco photon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_pt":            {"name":"RecoPhoton_pt",                  "title":"Reco photon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_px":            {"name":"RecoPhoton_px",                  "title":"Reco photon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_py":            {"name":"RecoPhoton_py",                  "title":"Reco photon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_pz":            {"name":"RecoPhoton_pz",                  "title":"Reco photon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_y":             {"name":"RecoPhoton_y",                   "title":"Reco photon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoPhoton_eta":           {"name":"RecoPhoton_eta",                 "title":"Reco photon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_theta":         {"name":"RecoPhoton_theta",               "title":"Reco photon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":           {"name":"RecoPhoton_phi",                 "title":"Reco photon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":        {"name":"RecoPhoton_charge",              "title":"Reco photon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    #"RecoPhoton_mass":          {"name":"RecoPhoton_mass",                 "title":"Reco photon mass [GeV]",                         "bin":50, "xmin":-0.05,"xmax":0.05},

    "RecoEmiss_px":             {"name":"RecoEmiss_px",                  "title":"Reco missing energy p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoEmiss_py":             {"name":"RecoEmiss_py",                  "title":"Reco missing energy p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoEmiss_pz":             {"name":"RecoEmiss_pz",                  "title":"Reco missing energy p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoEmiss_pt":             {"name":"RecoEmiss_pt",                  "title":"Reco missing energy p_{T} [GeV]",                    "bin":60,"xmin":0 ,"xmax":120},
    "RecoEmiss_p":              {"name":"RecoEmiss_p",                   "title":"Reco missing energy p [GeV]",                        "bin":60,"xmin":0 ,"xmax":120},
    "RecoEmiss_e":              {"name":"RecoEmiss_e",                   "title":"Reco missing energy energy [GeV]",                   "bin":60,"xmin":0 ,"xmax":240},
    
}