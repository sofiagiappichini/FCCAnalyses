import ROOT

# global parameters
intLumi        = 150.0e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = 'e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu'
#ana_tex        = ''
delphesVersion = '3.5.1pre05'
#delphesVersion = ''
energy         = 91
collider       = 'FCC-ee'
inputDir       = '/eos/user/s/sgiappic/test_bkg3/final/'
#inputDir       = 'output_finalSel_Ztautau/'
#formats        = ['png','pdf']
formats        = ['pdf']
#yaxis          = ['lin','log']
yaxis          = ['log']
#stacksig       = ['nostack']
stacksig       = ['stack']
outdir         = '/eos/user/s/sgiappic/test_bkg3/plots/'
#outdir         = 'plots_Ztautau_spring2021_vs_prewinter2023/'
splitLeg       = True ### to split legend for backgrounds and signals ###

variables = [

    #gen variables
    "n_FSGenElectron",
    "n_FSGenMuon",
    "n_FSGenNeutrino",
    #"n_FSGenPhoton",

    "FSGenElectron_e",
    "FSGenElectron_p",
    "FSGenElectron_pt",
    "FSGenElectron_pz",
    "FSGenElectron_eta",
    "FSGenElectron_theta",
    "FSGenElectron_phi",
    "FSGenElectron_vertex_x",
    "FSGenElectron_vertex_y",
    "FSGenElectron_vertex_z",
    "FSGenElectron_vertex_x_prompt",
    "FSGenElectron_vertex_y_prompt",
    "FSGenElectron_vertex_z_prompt",

    "FSGen_Lxy",
    "FSGen_Lxyz",
    "FSGen_Lxyz_prompt",

    "FSGenMuon_e",
    "FSGenMuon_p",
    "FSGenMuon_pt",
    "FSGenMuon_pz",
    "FSGenMuon_eta",
    "FSGenMuon_theta",
    "FSGenMuon_phi",
    "FSGenMuon_vertex_x",
    "FSGenMuon_vertex_y",
    "FSGenMuon_vertex_z",
    "FSGenMuon_vertex_x_prompt",
    "FSGenMuon_vertex_y_prompt",
    "FSGenMuon_vertex_z_prompt",

    "FSGenNeutrino_e",
    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_theta",
    "FSGenNeutrino_phi",

    #"FSGenPhoton_e",
    #"FSGenPhoton_p",
    #"FSGenPhoton_pt",
    #"FSGenPhoton_pz",
    #"FSGenPhoton_eta",
    #"FSGenPhoton_theta",
    #"FSGenPhoton_phi",

    #"FSGen_ee_invMass",
    #"FSGen_mumu_invMass",
    #"FSGen_emu_invMass",
    "FSGen_invMass",
    #"FSGen_eenu_invMass",

    #reco variables
    "n_RecoTracks",
    "n_RecoJets",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",

    #"jets_e",
    #"RecoJet_e",
    #"RecoJet_p",
    #"RecoJet_pt",
    #"RecoJet_pz",
    #"RecoJet_eta",
    #"RecoJet_theta",
    #"RecoJet_phi",
    #"RecoJet_charge",

    #"RecoJetTrack_absD0",
    #"RecoJetTrack_absD0_prompt",
    #"RecoJetTrack_absZ0",
    #"RecoJetTrack_absZ0_prompt",
    #"RecoJetTrack_absD0sig",
    #"RecoJetTrack_absD0sig_prompt",
    #"RecoJetTrack_absZ0sig",
    #"RecoJetTrack_absZ0sig_prompt",
    #"RecoJetTrack_D0cov",
    #"RecoJetTrack_Z0cov",

    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
    "RecoElectron_charge",

    "RecoElectronTrack_absD0",
    "RecoElectronTrack_absD0_prompt",
    "RecoElectronTrack_absZ0",
    "RecoElectronTrack_absZ0_prompt",
    "RecoElectronTrack_absD0sig",
    "RecoElectronTrack_absD0sig_med",
    "RecoElectronTrack_absD0sig_prompt",
    "RecoElectronTrack_absZ0sig",
    "RecoElectronTrack_absZ0sig_prompt",
    "RecoElectronTrack_D0cov",
    "RecoElectronTrack_Z0cov",

    #"RecoPhoton_e",
    #"RecoPhoton_p",
    #"RecoPhoton_pt",
    #"RecoPhoton_pz",
    #"RecoPhoton_eta",
    #"RecoPhoton_theta",
    #"RecoPhoton_phi",
    #"RecoPhoton_charge",

    "RecoMuon_e",
    "RecoMuon_p",
    "RecoMuon_pt",
    "RecoMuon_pz",
    "RecoMuon_eta",
    "RecoMuon_theta",
    "RecoMuon_phi",
    "RecoMuon_charge",

    "RecoMuonTrack_absD0",
    "RecoMuonTrack_absD0_prompt",
    "RecoMuonTrack_absZ0",
    "RecoMuonTrack_absZ0_prompt",
    "RecoMuonTrack_absD0sig",
    "RecoMuonTrack_absD0sig_prompt",
    "RecoMuonTrack_absZ0sig",
    "RecoMuonTrack_absZ0sig_prompt",
    "RecoMuonTrack_D0cov",
    "RecoMuonTrack_Z0cov",

    "Reco_DecayVertexElectron_x",       
    "Reco_DecayVertexElectron_y",          
    "Reco_DecayVertexElectron_z",          
    "Reco_DecayVertexElectron_x_prompt",   
    "Reco_DecayVertexElectron_y_prompt",    
    "Reco_DecayVertexElectron_z_prompt",    
    "Reco_DecayVertexElectron_chi2",    
    "Reco_DecayVertexElectron_probability", 

    "Reco_DecayVertexMuon_x",        
    "Reco_DecayVertexMuon_y",           
    "Reco_DecayVertexMuon_z",          
    "Reco_DecayVertexMuon_x_prompt",    
    "Reco_DecayVertexMuon_y_prompt",    
    "Reco_DecayVertexMuon_z_prompt",    
    "Reco_DecayVertexMuon_chi2",       
    "Reco_DecayVertexMuon_probability", 

    "Reco_Lxy",
    "Reco_Lxyz",
    "Reco_Lxyz_prompt",

    "RecoMissingEnergy_e",
    "RecoMissingEnergy_p",
    "RecoMissingEnergy_pt",
    "RecoMissingEnergy_px",
    "RecoMissingEnergy_py",
    "RecoMissingEnergy_pz",
    "RecoMissingEnergy_eta",
    "RecoMissingEnergy_theta",
    "RecoMissingEnergy_phi",

    #"Reco_ee_invMass",
    #"Reco_mumu_invMass",
    #"Reco_emu_invMass",
    "Reco_invMass",

    #"Reco_ee_cos",
    #"Reco_mumu_cos",
    #"Reco_emu_cos",
    "Reco_cos",

    #"Reco_ee_DR",
    #"Reco_mumu_DR",
    #"Reco_emu_DR",
    "Reco_DR",
    
]

    
#Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']  = [
    "selNone",
    # "sel1FSGenEle",
    # "sel1FSGenEle_eeInvMassGt80",
    # "sel1FSGenNu",
    #"sel2RecoEle",
    #"sel2RecoEle_vetoes",
    # "sel2RecoEle_absD0Gt0p1",
    #"sel2RecoEle_vetoes_MissingEnergyGt10",
    # "sel2RecoEle_vetoes_absD0Gt0p5",
    #"sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5",

    "sel2RecoSF",
    "sel2RecoDF",
    "sel2RecoSF_vetoes",
    "sel2RecoDF_vetoes",
    "sel2RecoSF_vetoes_M",
    "sel2RecoDF_vetoes_M",
]

extralabel = {}
extralabel['selNone'] = "Before selection"
# extralabel['sel1FSGenEle'] = "At least 1 final state gen electron"
# extralabel['sel1FSGenEle_eeInvMassGt80'] = "At least 1 final state gen electron, gen ee inv mass > 80 GeV"
# extralabel['sel1FSGenNu'] = "At least 1 final state gen neutrino"
#extralabel['sel2RecoEle'] = "2 electrons"
#extralabel['sel2RecoEle_vetoes'] = "2 electrons; No muons, jets, or photons"
# extralabel['sel2RecoEle_absD0Gt0p1'] = "2 electrons with |d_0|>0.1 mm"
#extralabel['sel2RecoEle_vetoes_MissingEnergyGt10'] = "2 electrons; No muons, jets, or photons; Missing momentum > 10 GeV"
# extralabel['sel2RecoEle_vetoes_absD0Gt0p5'] = "2 electrons with |d_0|>0.1 mm; No muons, jets, or photons"
#extralabel['sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5'] = "2 electrons with |d_0|>0.5 mm; No muons, jets, or photons; Missing momentum > 10 GeV"

extralabel['sel2RecoSF']="Two same flavor leptons"
extralabel['sel2RecoDF']="Two different flavor leptons"
extralabel['sel2RecoSF_vetoes']="Two same flavor leptons, no photons"
extralabel['sel2RecoDF_vetoes']="Two different flavor leptons, no photons"
extralabel['sel2RecoSF_vetoes_M']="Two same flavor leptons, no photons, 15<M(l,l)<70 GeV"
extralabel['sel2RecoDF_vetoes_M']="Two different flavor leptons, no photons, 15<M(l,l)<70 GeV"

colors = {}
#colors['eenu_30GeV_1p41e-6Ve'] = ROOT.kOrange+1
#colors['eenu_50GeV_1p41e-6Ve'] = ROOT.kRed
#colors['eenu_70GeV_1p41e-6Ve'] = ROOT.kBlue
#colors['eenu_90GeV_1p41e-6Ve'] = ROOT.kGreen+1

colors['Zbb'] = ROOT.kRed-4
colors['Zcc'] = ROOT.kOrange-3
colors['Zud'] = ROOT.kYellow-4
colors['Ztautau'] = ROOT.kGreen-3
colors['Zee'] = ROOT.kCyan-3
colors['Zmumu'] = ROOT.kBlue-7
colors['Zss'] = ROOT.kViolet-4

#colors['Ztautau_spring2021'] = ROOT.kBlack
#colors['Ztautau_pre_winter2023_tests_v2'] = ROOT.kRed


plots = {}
plots['HNL'] = {'signal':{
                     'eenu_30GeV_1p41e-6Ve':['eenu_30GeV_1p41e-6Ve'],
                     #'eenu_50GeV_1p41e-6Ve':['eenu_50GeV_1p41e-6Ve'],
                     #'eenu_70GeV_1p41e-6Ve':['eenu_70GeV_1p41e-6Ve'],
                     #'eenu_90GeV_1p41e-6Ve':['eenu_90GeV_1p41e-6Ve'],
    },
                'backgrounds':{
                    'Zbb':['p8_ee_Zbb_ecm91'],
                    'Zcc': ['p8_ee_Zcc_ecm91'],
                    'Zud': ['p8_ee_Zud_ecm91'],
                    'Ztautau': ['p8_ee_Ztautau_ecm91'],
                    'Zee':['p8_ee_Zee_ecm91'],
                    'Zmumu': ['p8_ee_Zmumu_ecm91'],
                    'Zss':['p8_ee_Zss_ecm91'],
                    #'Ztautau_spring2021': ['p8_ee_Ztautau_ecm91_spring2021'],
                    #'Ztautau_pre_winter2023_tests_v2': ['p8_ee_Ztautau_ecm91_pre_winter2023_tests_v2'],
                }
                }


legend = {}
#legend['eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
#legend['eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
#legend['eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'
#legend['eenu_90GeV_1p41e-6Ve'] = 'm_{N} = 90 GeV, V_{e} = 1.41e-6'

legend['Zbb'] = 'e^{+}e^{-} #rightarrow Z #rightarrow bb'
legend['Zcc'] = 'e^{+}e^{-} #rightarrow Z #rightarrow cc'
legend['Zud'] = 'e^{+}e^{-} #rightarrow Z #rightarrow ud'
legend['Ztautau'] = 'e^{+}e^{-} #rightarrow Z #rightarrow #tau#tau'
legend['Zee'] = 'e^{+}e^{-} #rightarrow Z #rightarrow ee'
legend['Zmumu'] = 'e^{+}e^{-} #rightarrow Z #rightarrow #mu#mu'
legend['Zss'] = 'e^{+}e^{-} #rightarrow Z #rightarrow ss'
#legend['Ztautau_spring2021'] = 'Z #rightarrow #tau#tau Spring2021'
#legend['Ztautau_pre_winter2023_tests_v2'] = 'Z #rightarrow #tau#tau pre winter2023 tests v2'