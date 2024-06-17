#Input directory where the files produced at the stage1 level are
inputDir = "/eos/user/s/sgiappic/2HNL_ana/stage1/"

#Output directory where the files produced at the final-selection level are
outputDir = "/eos/user/s/sgiappic/2HNL_ana/eff/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 204e6 #pb^-1

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 6

#produces ROOT TTrees, default is False
doTree = False

processList = {
        'p8_ee_Zee_ecm91':{},
        'p8_ee_Zmumu_ecm91':{},
        'p8_ee_Ztautau_ecm91':{},
        'p8_ee_Zbb_ecm91':{},
        'p8_ee_Zcc_ecm91':{},
        'p8_ee_Zud_ecm91':{},
        'p8_ee_Zss_ecm91':{},
            
        ### privately produced backgrounds ###
        'emununu':{},
        'tatanunu':{},

        'HNL_2.86e-12_30gev':{},
        'HNL_6.67e-10_30gev':{},
        'HNL_5e-12_60gev':{},
        'HNL_1.33e-7_80gev':{},
}

###Dictionary for prettier names of processes (optional)
processLabels = {
    #backgrounds
    'p8_ee_Zee_ecm91':"Z $\rightarrow$ ee",
    'p8_ee_Zmumu_ecm91':"Z $\rightarrow \mu \mu$",
    'p8_ee_Ztautau_ecm91':"Z $\rightarrow \tau \tau$",
    'p8_ee_Zbb_ecm91':"Z $\rightarrow$ bb",
    'p8_ee_Zcc_ecm91':"Z $\rightarrow$ cc",
    'p8_ee_Zud_ecm91':"Z $\rightarrow$ ud",
    'p8_ee_Zss_ecm91':"Z $\rightarrow$ ss",
    
    'emununu':"e $\mu \nu \nu$",
    'tatanunu':"$\tau \tau \nu \nu$",
}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "tatanunu":{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 2.855e-4, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "emununu":{"numberOfEvents": 999997, "sumOfWeights": 999997, "crossSection": 7.619e-4, "kfactor": 1.0, "matchingEfficiency": 1.0},
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### basic selection is vetoes on leptons, charge, photons, jets ###

    "selNone": "n_RecoTracks>-1",
    #"sel2Reco_vetoes": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2Reco_vetoes_tracks": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_RecoTracks==2",
    #"sel2Reco_vetoes_notracks": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0",
    #"sel2Reco_vetoes_nojetsexcl": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_jets_excl==0",
    #"sel2Reco_vetoes_nojets": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_antikt_jets==0",
    #"sel2Reco_vetoes_notracks_nojetsexcl": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_jets_excl==0",
    #"sel2Reco_vetoes_notracks_nojets": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 ",
 
    ### to be used for signal plots with no distintion between flavors ###
    #"sel2Reco_vetoes": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2Gen_vetoes": "n_FSGenLepton==2 && n_FSGenPhoton==0",

    #"sel2RecoSF_vetoes": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2RecoSF_vetoes_notracks": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0",
    #"sel2RecoSF_vetoes_notracks_nojets": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0",
    #"sel2RecoSF_vetoes_notracks_nojets_M80": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 \
    #                                    && RecoMissingEnergy_pt.at(0)>5",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt_0.8cos": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_antikt_jets==0 && n_noLeptonTracks == 0 && Reco_invMass<80 \
    #                                    && RecoMissingEnergy_pt.at(0)>5 && Reco_cos>-0.8",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt_0.8cos_chi_0.55d0": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 \
                                        #&& RecoMissingEnergy_pt.at(0)>5 && Reco_cos>-0.8 && RecoDecayVertexLepton.chi2<10 && RecoTrack_absD0.at(0)>0.55 && RecoTrack_absD0.at(1)>0.55 && Reco_Lxy<2000 && abs(RecoDecayVertexLepton.position.z)<2000",
    
    
    #"sel2RecoDF_vetoes": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2RecoDF_vetoes_notracks": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 ",
    #"sel2RecoDF_vetoes_notracks_nojets": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0",
    #"sel2RecoDF_vetoes_notracks_nojets_M80": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80",
    #"sel2RecoDF_vetoes_notracks_nojets_M80_5MEpt": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>5",
    #"sel2RecoDF_vetoes_notracks_nojets_M80_5MEpt_0.8cos": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_antikt_jets==0 && n_noLeptonTracks == 0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>5 && Reco_cos>-0.8",
    #"sel2RecoDF_vetoes_notracks_nojets_M80_5MEpt_0.8cos_chi_0.55d0": "n_RecoElectrons==1 && n_RecoMuons==1 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>5 && Reco_cos>-0.8 \
                                                       #&& RecoDecayVertexLepton.chi2<10 && RecoTrack_absD0.at(0)>0.5 && RecoTrack_absD0.at(1)>0.55 && Reco_Lxy<2000 && abs(RecoDecayVertexLepton.position.z)<2000",

    #"sel2Reco_vetoes": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2Reco_vetoes_notracks": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 ",
    #"sel2Reco_vetoes_notracks_nojets": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0",
    #"sel2Reco_vetoes_notracks_nojets_M80": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>10",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_antikt_jets==0 && n_noLeptonTracks == 0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>10 && Reco_cos>-0.8",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos_chi10_0.57d0": "n_RecoLeptons==2 && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0 && n_antikt_jets==0 && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>10 && Reco_cos>-0.8 \
    #                                                   && RecoDecayVertexLepton.chi2<10 && RecoTrack_absD0.at(0)>0.57 && RecoTrack_absD0.at(1)>0.57 && Reco_Lxy<2000 && abs(RecoDecayVertexLepton.position.z)<2000",
    
    #"M80_10MEpt_0.8cos": "Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>10 && Reco_cos>-0.8",
    "chi10_0.57d0": "RecoDecayVertexLepton.chi2<10 && RecoTrack_absD0.at(0)>0.57 && RecoTrack_absD0.at(1)>0.57 && Reco_Lxy<2000 && abs(RecoDecayVertexLepton.position.z)<2000",
  
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {

    #"sel2RecoSF_vetoes":"Two same flavor leptons, no photons",
    #"sel2RecoSF_vetoes_notracks":"Two same flavor leptons, no photons, no other track",
    #"sel2RecoSF_vetoes_notracks_nojets":"Two same flavor leptons, no photons, no other track, no jets",
    #"sel2RecoSF_vetoes_notracks_nojets_M80":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt_0.8cos":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, cos\theta>-0.8",
    #"sel2RecoSF_vetoes_notracks_nojets_M80_5MEpt_0.8cos_chi_0.55d0":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, cos\theta>-0.8, \chi^2<10, |d_0|>0.55 mm",

    #"sel2RecoDF_vetoes":"Two different flavor leptons, no photons",
    #"sel2RecoDF_vetoes_notracks":"Two different flavor leptons, no photons, no other trac",
    #"sel2RecoDF_vetoes_notracks_nojets":"Two different flavor leptons, no photons, no other track, no jets",
    #"sel2RecoDF_vetoes_notracks_nojets_M80":"Two different flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV",
    #"sel2RecoDF_vetoes_motracks_nojets_M80_5MEpt":"Two different flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV",
    #"sel2RecoDF_vetoes_notracks_nojets_M80_5MEpt_0.8cos":"Two different flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, cos\theta>-0.8",
    #"sel2RecoDF_vetoes_notracks_nojets_M80_5MEpt_0.8cos_chi_0.5d0":"Two different flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, cos\theta>-0.8, \chi^2<10, |d_0|>0.55 mm",

    "sel2Reco_vetoes":"Two leptons, no photons",
    "sel2Reco_vetoes_notracks":"Two leptons, no photons, no other trac",
    "sel2Reco_vetoes_notracks_nojets":"Two leptons, no photons, no other track, no jets",
    "sel2Reco_vetoes_notracks_nojets_M80":"Two leptons, no photons, no other track, no jets, M(l,l)<80 GeV",
    "sel2Reco_vetoes_n otracks_nojets_M80_10MEpt":"Two leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos":"Two leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos\theta>-0.8",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos_chi10_0.57d0":"Two leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos\theta>-0.8, \chi^2<10, |d_{0}|>0.57 mm",
    
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    ######## GEN VARIABLES
    "n_FSGenElectron":                  {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",          "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenMuon":                      {"name":"n_FSGenMuon",                      "title":"Number of final state gen muons",              "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenLepton":                    {"name":"n_FSGenLepton",                    "title":"Number of final state gen leptons",            "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPhoton":                    {"name":"n_FSGenPhoton",                    "title":"Number of final state gen photons",            "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_GenTaus":                        {"name":"n_GenTaus",                      "title":"Number of final state gen tau",              "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_GenPions":                       {"name":"n_GenPions",                    "title":"Number of final state gen pion",            "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_GenKpluss":                      {"name":"n_GenKpluss",                    "title":"Number of final state gen K+",            "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_GenKLs":                         {"name":"n_GenKLs",                        "title":"Number of final state gen KL",            "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_GenN":                           {"name":"n_GenN",                           "title":"Number of final state gen HNLs",               "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_FSGenNeutrino":                   {"name":"n_FSGenNeutrino",                  "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    
    #"FSGenLepton_e":                   {"name":"FSGenLepton_e",                  "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenLepton_p":                   {"name":"FSGenLepton_p",                  "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenLepton_pt":                  {"name":"FSGenLepton_pt",                 "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenLepton_pz":                  {"name":"FSGenLepton_pz",                 "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenLepton_eta":                 {"name":"FSGenLepton_eta",                "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    #"FSGenLepton_theta":               {"name":"FSGenLepton_theta",              "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenLepton_phi":                 {"name":"FSGenLepton_phi",                "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenLepton_charge":              {"name":"FSGenLepton_charge",             "title":"Final state gen electrons charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"FSGenLepton_vertex_x": {"name":"FSGenLepton_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-2000 ,"xmax":2000},
    #"FSGenLepton_vertex_y": {"name":"FSGenLepton_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-2000 ,"xmax":2000},
    #"FSGenLepton_vertex_z": {"name":"FSGenLepton_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-2000 ,"xmax":2000},
    #"FSGenLepton_vertex_x_prompt": {"name":"FSGenLepton_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1 ,"xmax":1},
    #"FSGenLepton_vertex_y_prompt": {"name":"FSGenLepton_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1 ,"xmax":1},
    #"FSGenLepton_vertex_z_prompt": {"name":"FSGenLepton_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1 ,"xmax":1},
    #"FSGenLepton_time":             {"name":"FSGenLepton_time",              "title":"Gen lepton time [s]",         "bin":100,"xmin":0 ,"xmax":1e-8},
    
    #"FSGen_Lxy":            {"name":"FSGen_Lxy",      "title":"Gen L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":2000},
    #"FSGen_Lxyz":           {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":2000},
    #"FSGen_Lxyz_prompt":    {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},
    #"FSGen_Lxy_prompt":     {"name":"FSGen_Lxy",     "title":"Gen L_{xy} [mm]",    "bin":100,"xmin":0 ,"xmax":10},
    #"FSGen_invMass":        {"name":"FSGen_invMass",  "title":"Gen M(l,l') [GeV]",   "bin":100,"xmin":0, "xmax":100},

    #"FSGenNeutrino_e":                   {"name":"FSGenNeutrino_e",                  "title":"Final state gen neutrinos energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_p":                   {"name":"FSGenNeutrino_p",                  "title":"Final state gen neutrinos p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_pt":                  {"name":"FSGenNeutrino_pt",                 "title":"Final state gen neutrinos p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_pz":                  {"name":"FSGenNeutrino_pz",                 "title":"Final state gen neutrinos p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_eta":                 {"name":"FSGenNeutrino_eta",                "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    #"FSGenNeutrino_theta":               {"name":"FSGenNeutrino_theta",              "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenNeutrino_phi":                 {"name":"FSGenNeutrino_phi",                "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenNeutrino_charge":              {"name":"FSGenNeutrino_charge",             "title":"Final state gen neutrinos charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"GenN_mass":                   {"name":"GenN_mass",                     "title":"Gen N mass [GeV]",               "bin":100,"xmin":0 ,"xmax":90},
    #"GenN_e":                      {"name":"GenN_e",                        "title":"Gen N energy [GeV]",             "bin":100,"xmin":0 ,"xmax":50},
    #"GenN_p":                      {"name":"GenN_p",                        "title":"Gen N momentum [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    #"GenN_tau":                    {"name":"GenN_tau",                      "title":"Gen HNL #tau [s]",               "bin":100,"xmin":0 ,"xmax":1e-8},
    #"GenN_Lxyz":                   {"name":"GenN_Lxyz",                     "title":"Gen N L_{xyz} [mm]",             "bin":100,"xmin":0 ,"xmax":2000},
    #"GenN_Lxyz_prompt":            {"name":"GenN_Lxyz",                     "title":"Gen N L_{xyz} [mm]",             "bin":100,"xmin":0 ,"xmax":10},
   
    #"FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    #"FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenPhoton_charge":              {"name":"FSGenPhoton_charge",             "title":"Final state gen photons charge",             "bin":3, "xmin":-1.5,"xmax":1.5},

    ######### RECO VARIABLES
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",             "bin":10,"xmin":0 ,"xmax":10},
    "n_noLeptonTracks":                    {"name":"n_noLeptonTracks",           "title":"Total number of non lepton tracks",             "bin":10,"xmin":0 ,"xmax":10},
    #"n_PrimaryTracks":                 {"name":"n_PrimaryTracks",                "title":"Total number of primary tracks",          "bin":10,"xmin":-0.5 ,"xmax":9.5},
    #"n_SecondaryTracks":               {"name":"n_SecondaryTracks",              "title":"Total number of secondary tracks",        "bin":10,"xmin":-0.5 ,"xmax":9.5},
    #"n_RecoDVs":                       {"name":"n_RecoDVs",                      "title":"Total number of DVs",                     "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":                   {"name":"n_RecoPhotons",                  "title":"Total number of reco photons",            "bin":5,"xmin":0 ,"xmax":5},
    "n_RecoElectrons":                 {"name":"n_RecoElectrons",                "title":"Total number of reco electrons",          "bin":5,"xmin":0 ,"xmax":5},
    "n_RecoMuons":                     {"name":"n_RecoMuons",                    "title":"Total number of reco muons",              "bin":5,"xmin":0 ,"xmax":5},
    "n_RecoLeptons":                   {"name":"n_RecoLeptons",                  "title":"Total number of reco leptons",            "bin":5,"xmin":0 ,"xmax":5},
    #"n_jets":                           {"name":"n_jets",                         "title":"Total number of reco jets",               "bin":5,"xmin":0 ,"xmax":5},
    #"n_jets_excl":                           {"name":"n_jets_excl",                "title":"Total number of reco jets",               "bin":5,"xmin":0 ,"xmax":5},
    "n_antikt_jets":                           {"name":"n_antikt_jets",              "title":"Total number of reco jets",               "bin":10,"xmin":0 ,"xmax":10},
    #"n_antikt_jets10":                           {"name":"n_antikt_jets10",                         "title":"Total number of reco jets",               "bin":10,"xmin":0,"xmax":10},
    #"n_RecoJets":                           {"name":"n_RecoJets",                         "title":"Total number of reco jets",               "bin":5,"xmin":-0.5 ,"xmax":4.5},
    
    #"RecoMC_PID":                    {"name":"RecoMC_PID",                    "title":"Reco Particles PID",            "bin":800,"xmin":-400,"xmax":400},

    #"jets_e":        {"name":"jets_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_e":        {"name":"RecoJet_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_p":        {"name":"RecoJet_p",        "title":"Reco jet p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_pz":       {"name":"RecoJet_pz",       "title":"Reco jet p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    #"RecoJet_theta":    {"name":"RecoJet_theta",    "title":"Reco jet #theta",       "bin":64, "xmin":0,"xmax":3.2},
    #"RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    #"RecoJetTrack_absD0":             {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoJetTrack_absD0_prompt":      {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoJetTrack_absZ0":             {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoJetTrack_absZ0_prompt":      {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoJetTrack_absD0sig":          {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoJetTrack_absD0sig_prompt":   {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoJetTrack_absZ0sig":          {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoJetTrack_absZ0sig_prompt":   {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoJetTrack_D0cov":      {"name":"RecoJetTrack_D0cov",     "title":"Reco jet tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    #"RecoJetTrack_Z0cov":      {"name":"RecoJetTrack_Z0cov",     "title":"Reco jet tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    #"RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoElectron_px":       {"name":"RecoElectron_px",       "title":"Reco electron p_{x} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    #"RecoElectron_py":       {"name":"RecoElectron_py",       "title":"Reco electron p_{y} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    #"RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    #"RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    #"RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    #"RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    #"RecoElectronTrack_absD0":             {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoElectronTrack_absD0_med":         {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":10},
    #"RecoElectronTrack_absD0_prompt":      {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoElectronTrack_absZ0":             {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoElectronTrack_absZ0_prompt":      {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoElectronTrack_absD0sig":          {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoElectronTrack_absD0sig_med":      {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    #"RecoElectronTrack_absD0sig_prompt":   {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoElectronTrack_absZ0sig":          {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoElectronTrack_absZ0sig_prompt":   {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoElectronTrack_D0cov":      {"name":"RecoElectronTrack_D0cov",     "title":"Reco electron tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    #"RecoElectronTrack_Z0cov":      {"name":"RecoElectronTrack_Z0cov",     "title":"Reco electron tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    #"RecoPhoton_e":        {"name":"RecoPhoton_e",        "title":"Reco photon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_p":        {"name":"RecoPhoton_p",        "title":"Reco photon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_pz":       {"name":"RecoPhoton_pz",       "title":"Reco photon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    #"RecoPhoton_theta":    {"name":"RecoPhoton_theta",    "title":"Reco photon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    #"RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "Reco_e":                   {"name":"Reco_e",         "title":"Reco lepton energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "Reco_p":                   {"name":"Reco_p",         "title":"Reco lepton p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    "Reco_pt":                  {"name":"Reco_pt",        "title":"Reco lepton p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "Reco_px":                  {"name":"Reco_px",        "title":"Reco lepton p_{x} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_py":                  {"name":"Reco_py",        "title":"Reco lepton p_{y} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_pz":                  {"name":"Reco_pz",        "title":"Reco lepton p_{z} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_eta":                 {"name":"Reco_eta",       "title":"Reco lepton #eta",               "bin":60, "xmin":-3,"xmax":3},
    "Reco_theta":               {"name":"Reco_theta",     "title":"Reco lepton #theta",             "bin":64, "xmin":0,"xmax":3.2},
    "Reco_phi":                 {"name":"Reco_phi",       "title":"Reco lepton #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},
    #"Reco_charge":              {"name":"Reco_charge",    "title":"Reco electron charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoTrack_absD0_prompt":        {"name":"RecoTrack_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    "RecoTrack_absZ0_prompt":        {"name":"RecoTrack_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    "RecoTrack_absD0_med":           {"name":"RecoTrack_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    "RecoTrack_absZ0_med":           {"name":"RecoTrack_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    "RecoTrack_absD0":               {"name":"RecoTrack_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    "RecoTrack_absZ0":               {"name":"RecoTrack_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    "RecoTrack_absD0sig":            {"name":"RecoTrack_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":10000},
    "RecoTrack_absD0sig_med":        {"name":"RecoTrack_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "RecoTrack_absD0sig_prompt":     {"name":"RecoTrack_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoTrack_absZ0sig":            {"name":"RecoTrack_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":10000},
    "RecoTrack_absZ0sig_prompt":     {"name":"RecoTrack_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoTrack_absZ0sig_med":        {"name":"RecoTrack_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "RecoTrack_D0cov":               {"name":"RecoTrack_D0cov",     "title":"Reco lepton tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoTrack_Z0cov":               {"name":"RecoTrack_Z0cov",     "title":"Reco lepton tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    
    "Reco_DecayVertexLepton_x":           {"name":"RecoDecayVertexLepton.position.x",  "title":"Reco decay lepton vertex x [mm]",            "bin":100,"xmin":-2000 ,"xmax":2000},
    "Reco_DecayVertexLepton_y":           {"name":"RecoDecayVertexLepton.position.y",  "title":"Reco decay lepton vertex y [mm]",            "bin":100,"xmin":-2000 ,"xmax":2000},
    "Reco_DecayVertexLepton_z":           {"name":"RecoDecayVertexLepton.position.z",  "title":"Reco decay lepton vertex z [mm]",            "bin":100,"xmin":-2000 ,"xmax":2000},
    "Reco_DecayVertexLepton_x_prompt":    {"name":"RecoDecayVertexLepton.position.x",  "title":"Reco decay lepton vertex x [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_y_prompt":    {"name":"RecoDecayVertexLepton.position.y",  "title":"Reco decay lepton vertex y [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_z_prompt":    {"name":"RecoDecayVertexLepton.position.z",  "title":"Reco decay lepton vertex z [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_chi2":        {"name":"RecoDecayVertexLepton.chi2",        "title":"Reco decay lepton vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":20},
    "Reco_DecayVertexLepton_probability": {"name":"RecoDecayVertexLepton.probability", "title":"Reco decay lepton vertex probability",       "bin":100,"xmin":0 ,"xmax":1},

    "Reco_Lxy":                     {"name":"Reco_Lxy",                    "title":"Reco L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_Lxy_prompt":              {"name":"Reco_Lxy",                    "title":"Reco L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":10},
    "Reco_Lxyz":                    {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_Lxyz_prompt":             {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},

    #"Reco_Lxyz_LCFI":                    {"name":"DV_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    #"Reco_Lxyz_prompt_LCFI":             {"name":"DV_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},
    
    "Reco_invMass":     {"name":"Reco_invMass",     "title":"Reco M(l,l') [GeV]",            "bin":100,"xmin":0, "xmax":100},
    "Reco_cos":         {"name":"Reco_cos",         "title":"Reco cos#theta(l,l')",          "bin":100,"xmin":-1., "xmax":1.},
    "Reco_DR":          {"name":"Reco_DR",          "title":"Reco #Delta R(l,l')",           "bin":70,"xmin":0, "xmax":7},

    "2DHsito":     {"cols":["Reco_invMass","RecoMissingEnergy_e"],     "title":"Invariant mass - Missing Energy",            "bins":[(100,0,100),(100,0,50)]},

    "RecoMissingEnergy_e":       {"name":"RecoMissingEnergy_e",       "title":"Reco Total Missing Energy [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_p":       {"name":"RecoMissingEnergy_p",       "title":"Reco Total Missing p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pt":      {"name":"RecoMissingEnergy_pt",      "title":"Reco Missing p_{T} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_px":      {"name":"RecoMissingEnergy_px",      "title":"Reco Missing p_{x} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_py":      {"name":"RecoMissingEnergy_py",      "title":"Reco Missing p_{y} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pz":      {"name":"RecoMissingEnergy_pz",      "title":"Reco Missing p_{z} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_eta":     {"name":"RecoMissingEnergy_eta",     "title":"Reco Missing Energy #eta",           "bin":60,"xmin":-3 ,"xmax":3},
    "RecoMissingEnergy_theta":   {"name":"RecoMissingEnergy_theta",   "title":"Reco Missing Energy #theta",         "bin":64,"xmin":0 , "xmax":3.2},
    "RecoMissingEnergy_phi":     {"name":"RecoMissingEnergy_phi",     "title":"Reco Missing Energy #phi",           "bin":64,"xmin":-3.2 ,"xmax":3.2},

    #"noLep_e":                   {"name":"noLep_e",         "title":"Reco non lepton energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    #"noLep_p":                   {"name":"noLep_p",         "title":"Reco non lepton p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    #"noLep_pt":                  {"name":"noLep_pt",        "title":"Reco non lepton p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    #"noLep_px":                  {"name":"noLep_px",        "title":"Reco non lepton p_{x} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    #"noLep_py":                  {"name":"noLep_py",        "title":"Reco non lepton p_{y} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    #"noLep_pz":                  {"name":"noLep_pz",        "title":"Reco non lepton p_{z} [GeV]",        "bin":100,"xmin":-50 ,"xmax":50},
    #"noLep_eta":                 {"name":"noLep_eta",       "title":"Reco non lepton #eta",               "bin":60, "xmin":-3,"xmax":3},
    #"noLep_theta":               {"name":"noLep_theta",     "title":"Reco non lepton #theta",             "bin":64, "xmin":0,"xmax":3.2},
    #"noLep_phi":                 {"name":"noLep_phi",       "title":"Reco non lepton #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},
    #"noLep_charge":              {"name":"noLep_charge",    "title":"Reco electron charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"RecoTracknoLep_absD0_prompt":        {"name":"RecoTracknoLep_absD0",        "title":"Reco non lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    #"RecoTracknoLep_absZ0_prompt":        {"name":"RecoTracknoLep_absZ0",        "title":"Reco non lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    #"RecoTracknoLep_absD0_med":           {"name":"RecoTracknoLep_absD0",        "title":"Reco non lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    #"RecoTracknoLep_absZ0_med":           {"name":"RecoTracknoLep_absZ0",        "title":"Reco non lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    #"RecoTracknoLep_absD0":               {"name":"RecoTracknoLep_absD0",        "title":"Reco non lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    #"RecoTracknoLep_absZ0":               {"name":"RecoTracknoLep_absZ0",        "title":"Reco non lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    #"RecoTracknoLep_absD0sig":            {"name":"RecoTracknoLep_absD0sig",  "title":"Reco non lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":10000},
    #"RecoTracknoLep_absD0sig_med":        {"name":"RecoTracknoLep_absD0sig",  "title":"Reco non lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    #"RecoTracknoLep_absD0sig_prompt":     {"name":"RecoTracknoLep_absD0sig",  "title":"Reco non lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoTracknoLep_absZ0sig":            {"name":"RecoTracknoLep_absZ0sig",  "title":"Reco non lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":10000},
    #"RecoTracknoLep_absZ0sig_prompt":     {"name":"RecoTracknoLep_absZ0sig",  "title":"Reco non lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoTracknoLep_absZ0sig_med":        {"name":"RecoTracknoLep_absZ0sig",  "title":"Reco non lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    #"RecoTracknoLep_D0cov":               {"name":"RecoTracknoLep_D0cov",     "title":"Reco non lepton tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    #"RecoTracknoLep_Z0cov":               {"name":"RecoTracknoLep_Z0cov",     "title":"Reco non lepton tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    
}
