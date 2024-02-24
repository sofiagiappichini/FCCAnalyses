import ROOT

# global parameters
intLumi        = 150.0e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = '/eos/user/s/sgiappic/sig+bkg_1/final/'
outdir         = '/eos/user/s/sgiappic/sig+bkg_1/plots/'
#formats        = ['png','pdf']
formats        = ['pdf']
#yaxis          = ['lin','log']
yaxis          = ['log']
stacksig       = ['nostack']
stackbkg       = ['stack']
#legendCoord    = [0.68,0.76,0.96,0.88]
#plotStatUnc    = True ### to include statistical uncertainty ###
splitLeg       = True ### to split legend for backgrounds and signals ###

variables = [

    #gen variables
    "n_FSGenElectron",
    "n_FSGenMuon",
    "n_FSGenNeutrino",
    "n_FSGenPhoton",

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
    #"FSGen_eenu_invMass",
    "FSGen_invMass",

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
    #"RecoElectron_charge",

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
    #"RecoMuon_charge",

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

    "Reco_DecayVertexLepton_x",       
    "Reco_DecayVertexLepton_y",          
    "Reco_DecayVertexLepton_z",          
    "Reco_DecayVertexLepton_x_prompt",   
    "Reco_DecayVertexLepton_y_prompt",    
    "Reco_DecayVertexLepton_z_prompt",    
    "Reco_DecayVertexLepton_chi2",    
    "Reco_DecayVertexLepton_probability", 

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

    "Reco_e",
    "Reco_p",
    "Reco_pt",
    "Reco_pz",
    "Reco_eta",
    "Reco_theta",
    "Reco_phi",

    "Reco_absD0_prompt",
    "Reco_absZ0_prompt",
    "Reco_absD0_med",
    "Reco_absZ0_med",
    "Reco_absD0",
    "Reco_absZ0",
    "Reco_absD0sig",
    "Reco_absD0sig_med",
    "Reco_absD0sig_prompt",
    "Reco_absZ0sig",
    "Reco_absZ0sig_med",
    "Reco_absZ0sig_prompt",
    "Reco_D0cov",
    "Reco_Z0cov",

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

    #"sel2RecoSF",
    #"sel2RecoDF",
    #"sel2Reco_vetoes",
    "sel2RecoSF_vetoes",
    "sel2RecoDF_vetoes",
    "sel2RecoSF_vetoes_M",
    "sel2RecoDF_vetoes_M",
    "sel2RecoSF_vetoes_Mp",
    "sel2RecoDF_vetoes_Mp",
    "sel2RecoSF_vetoes_Mp_ME",
    "sel2RecoDF_vetoes_Mp_ME",
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
extralabel['sel2Reco_vetoes']="Two leptons, no photons and jets"
extralabel['sel2RecoSF_vetoes']="Two same flavor leptons, no photons and jets"
extralabel['sel2RecoDF_vetoes']="Two different flavor leptons, no photons and jets"
extralabel['sel2RecoSF_vetoes_M']="Two same flavor leptons, no photons, 15<M(l,l)<70 GeV"
extralabel['sel2RecoDF_vetoes_M']="Two different flavor leptons, no photons, 15<M(l,l)<70 GeV"
extralabel['sel2RecoSF_vetoes_Mp']="Two same flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV"
extralabel['sel2RecoDF_vetoes_Mp']="Two different flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV"
extralabel['sel2RecoSF_vetoes_Mp_ME']="Two same flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV, ME>5 Gev"
extralabel['sel2RecoDF_vetoes_Mp_ME']="Two different flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV, ME>5 Gev"

colors = {}

colors['HNL_2e-11_10gev'] = ROOT.kOrange-4
colors['HNL_4e-10_10gev'] = ROOT.kCyan-7
colors['HNL_1.33e-9_20gev'] = ROOT.kAzure+5
colors['HNL_2.86e-12_30gev'] = ROOT.kBlue-4
colors['HNL_2.15e-10_40gev'] = ROOT.kOrange+1
colors['HNL_5e-8_50gev'] = ROOT.kRed-4
colors['HNL_4e-12_50gev'] = ROOT.kBlue+1
colors['HNL_2e-7_60gev'] = ROOT.kRed+1
colors['HNL_4e-8_60gev'] = ROOT.kBlue+2
colors['HNL_5e-12_70gev'] = ROOT.kPink-6
colors['HNL_2.86e-8_80gev'] = ROOT.kBlue+3
colors['HNL_2e-7_80gev'] = ROOT.kPink-7

colors['Zbb'] = 48
colors['Zcc'] = 44
colors['Zud'] = 41
colors['Ztautau'] = 34
colors['Zee'] = 29
colors['Zmumu'] = 32
colors['Zss'] = 20

#colors['Zbb'] = ROOT.kRed-4
#colors['Zcc'] = ROOT.kOrange-3
#colors['Zud'] = ROOT.kYellow-4
#colors['Ztautau'] = ROOT.kGreen-3
#colors['Zee'] = ROOT.kCyan-3
#colors['Zmumu'] = ROOT.kBlue-7
#colors['Zss'] = ROOT.kViolet-4

plots = {}
plots['HNL'] = {'signal':{
                    'HNL_4e-10_10gev':['HNL_4e-10_10gev'],
                    'HNL_2e-11_10gev':['HNL_2e-11_10gev'],
                    'HNL_1.33e-9_20gev':['HNL_1.33e-9_20gev'],
                    'HNL_2.86e-12_30gev':['HNL_2.86e-12_30gev'],
                    'HNL_2.15e-10_40gev':['HNL_2.15e-10_40gev'],
                    'HNL_5e-8_50gev':['HNL_5e-8_50gev'],
                    'HNL_4e-12_50gev':['HNL_4e-12_50gev'],
                    'HNL_2e-7_60gev':['HNL_2e-7_60gev'],
                    'HNL_4e-8_60gev':['HNL_4e-8_60gev'],
                    'HNL_5e-12_70gev':['HNL_5e-12_70gev'],
                    'HNL_2.86e-8_80gev':['HNL_2.86e-8_80gev'],
                    'HNL_2e-7_80gev':['HNL_2e-7_80gev'],
                },
                'backgrounds':{
                    'Zud': ['p8_ee_Zud_ecm91'],
                    'Zss':['p8_ee_Zss_ecm91'],
                    'Zcc': ['p8_ee_Zcc_ecm91'],
                    'Zbb':['p8_ee_Zbb_ecm91'],
                    
                    'Zee':['p8_ee_Zee_ecm91'],
                    'Zmumu': ['p8_ee_Zmumu_ecm91'],
                    'Ztautau': ['p8_ee_Ztautau_ecm91'],
                },
                }

legend = {}

legend['HNL_2e-11_10gev'] = 'U^{2}=2e-11, M_{N}=10 GeV'
legend['HNL_4e-10_10gev'] = 'U^{2}=4e-10, M_{N}=10 GeV'
legend['HNL_1.33e-9_20gev'] = 'U^{2}=1.33e-9, M_{N}=20 GeV'
legend['HNL_2.86e-12_30gev'] = 'U^{2}=2.86e-12, M_{N}=30 GeV'
legend['HNL_2.15e-10_40gev'] = 'U^{2}=2.15e-10, M_{N}=40 GeV'
legend['HNL_5e-8_50gev'] = 'U^{2}=5e-8, M_{N}=50 GeV'
legend['HNL_4e-12_50gev'] = 'U^{2}=4e-12, M_{N}=50 GeV'
legend['HNL_2e-7_60gev'] = 'U^{2}=2e-7, M_{N}=60 GeV'
legend['HNL_4e-8_60gev'] = 'U^{2}=4e-8, M_{N}=60 GeV'
legend['HNL_5e-12_70gev'] = 'U^{2}=5e-12, M_{N}=70 GeV'
legend['HNL_2.86e-8_80gev'] = 'U^{2}=2.86e-8, M_{N}=80 GeV'
legend['HNL_2e-7_80gev'] = 'U^{2}=2e-7, M_{N}=80 GeV'

legend['Zud'] = 'Z #rightarrow ud'
legend['Zss'] = 'Z #rightarrow ss'
legend['Zbb'] = 'Z #rightarrow bb'
legend['Zcc'] = 'Z #rightarrow cc'
legend['Zee'] = 'Z #rightarrow ee'
legend['Zmumu'] = 'Z #rightarrow #mu#mu'
legend['Ztautau'] = 'Z #rightarrow #tau#tau'