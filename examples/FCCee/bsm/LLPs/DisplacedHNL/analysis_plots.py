import ROOT

# global parameters
intLumi        = 90.0e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = '/eos/user/s/sgiappic//2HNL_test_tracks/final/'
outdir         = '/eos/user/s/sgiappic//2HNL_test_tracks/plots/'
formats        = ['png', 'pdf']
#formats        = ['pdf']
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
    #"n_FSGenNeutrino",
    "n_FSGenPhoton",

    #"FSGenElectron_e",
    #"FSGenElectron_p",
    #"FSGenElectron_pt",
    #"FSGenElectron_pz",
    #"FSGenElectron_eta",
    #"FSGenElectron_theta",
    #"FSGenElectron_phi",
    #"FSGenElectron_vertex_x",
    #"FSGenElectron_vertex_y",
    #"FSGenElectron_vertex_z",
    #"FSGenElectron_vertex_x_prompt",
    #"FSGenElectron_vertex_y_prompt",
    #"FSGenElectron_vertex_z_prompt",

    #"FSGen_Lxy",
    #"FSGen_Lxyz",
    #"FSGen_Lxyz_prompt",

    #"FSGenMuon_e",
    #"FSGenMuon_p",
    #"FSGenMuon_pt",
    #"FSGenMuon_pz",
    #"FSGenMuon_eta",
    #"FSGenMuon_theta",
    #"FSGenMuon_phi",
    #"FSGenMuon_vertex_x",
    #"FSGenMuon_vertex_y",
    #"FSGenMuon_vertex_z",
    #"FSGenMuon_vertex_x_prompt",
    #"FSGenMuon_vertex_y_prompt",
    #"FSGenMuon_vertex_z_prompt",

    #"FSGenNeutrino_e",
    #"FSGenNeutrino_p",
    #"FSGenNeutrino_pt",
    #"FSGenNeutrino_pz",
    #"FSGenNeutrino_eta",
    #"FSGenNeutrino_theta",
    #"FSGenNeutrino_phi",

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
    #"FSGen_invMass",

    #reco variables
    "n_RecoTracks",
    "n_RecoJets",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",
    "n_PrimaryTracks",
    "n_SecondaryTracks",

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
    "RecoElectron_px",
    "RecoElectron_py",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",

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
    "RecoMuon_px",
    "RecoMuon_py",
    "RecoMuon_pz",
    "RecoMuon_eta",
    "RecoMuon_theta",
    "RecoMuon_phi",

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
    "Reco_px",
    "Reco_py",
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

    "Reco_invMass",
    "Reco_cos",
    "Reco_DR",
    
]

    
#Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']  = [
    #"selNone",
    #"sel2Reco_vetoes",

    "sel2RecoSF_vetoes",
    #"sel2RecoSF_vetoes_15-80M",
    #"sel2RecoSF_vetoes_15-80M_40p",
    #"sel2RecoSF_vetoes_15-80M_40p_5ME",
    #"sel2RecoSF_vetoes_10-80M_39p_5ME_cos",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt",

    "sel2RecoDF_vetoes",
    #"sel2RecoDF_vetoes_15-80M",
    #"sel2RecoDF_vetoes_15-80M_40p",
    #"sel2RecoDF_vetoes_15-80M_40p_5ME",
    #"sel2RecoDF_vetoes_10-80M_39p_5ME_cos",
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43_cos",
]

extralabel = {}
extralabel['selNone'] = "Before selection"
extralabel['sel2Reco_vetoes']="Two leptons, no photons and jets"

extralabel['sel2RecoSF_vetoes']="Two same flavor leptons, no photons and jets"
extralabel['sel2RecoSF_vetoes_15-80M']="Two same flavor leptons, no photons, 15<M(l,l)<70 GeV"
extralabel['sel2RecoSF_vetoes_15-80M_40p']="Two same flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV"
extralabel['sel2RecoSF_vetoes_15-80M_40p_5ME']="Two same flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV, ME>5 Gev"
extralabel['sel2RecoSF_vetoes_10-80M_39p_5ME_cos']="Two same flavor leptons, no photons, 10<M(l,l)<80 GeV, p<39 GeV, ME>5 Gev, cos#theta>-0.8"
extralabel['sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt']="Two same flavor leptons, no photons and jets, 15<M(l,l')<80 GeV, p<42 GeV, E_{miss}>10 Gev, cos#theta>-0.8, 0.2<#theta_{miss}<3"

extralabel['sel2RecoDF_vetoes']="Two different flavor leptons, no photons and jets"
extralabel['sel2RecoDF_vetoes_15-80M']="Two different flavor leptons, no photons, 15<M(l,l)<70 GeV"
extralabel['sel2RecoDF_vetoes_15-80M_40p']="Two different flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV"
extralabel['sel2RecoDF_vetoes_15-80M_40p_5ME']="Two different flavor leptons, no photons, 15<M(l,l)<80 GeV, p<40 GeV, ME>5 Gev"
extralabel['sel2RecoDF_vetoes_10-80M_39p_5ME_cos']="Two different flavor leptons, no photons, 10<M(l,l)<80 GeV, p<39 GeV, ME>5 GeV, cos#theta>-0.8"
extralabel['sel2RecoDF_vetoes_15-80M_39p_10ME43_cos']="Two different flavor leptons, no photons and jets, 15<M(l,l')<80 GeV, p<39 GeV, 10<E_{miss}<43 GeV, cos#theta>-0.8"

colors = {}

colors['HNL_4e-8_10gev'] = ROOT.kCyan-7
colors['HNL_1.33e-9_20gev'] = ROOT.kAzure+5
colors['HNL_2.86e-12_30gev'] = ROOT.kBlue-7
colors['HNL_2.86e-7_30gev'] = ROOT.kOrange-2
colors['HNL_5e-12_40gev'] = ROOT.kOrange+8
colors['HNL_4e-12_50gev'] = ROOT.kBlue-4
colors['HNL_6.67e-8_60gev'] = ROOT.kRed-4
colors['HNL_4e-8_60gev'] = ROOT.kBlue-4
colors['HNL_2.86e-9_70gev'] = ROOT.kRed+2
colors['HNL_2.86e-8_80gev'] = ROOT.kBlue+2

colors['HNL'] = ROOT.kWhite

#colors['HNL_2.86e-12_30gev'] = ROOT.kAzure+6
#colors['HNL_2.86e-7_30gev'] = ROOT.kOrange+1
#colors['HNL_4e-12_50gev'] = ROOT.kBlue-4
#colors['HNL_2.86e-9_70gev'] = ROOT.kRed-4
#colors['HNL_6.67e-8_60gev'] = ROOT.kRed-4


colors['Zbb'] = 48
colors['Zcc'] = 44
colors['Zud'] = 41
colors['Ztautau'] = 34
colors['Zee'] = 29
colors['Zmumu'] = 32
colors['Zss'] = 20
colors['emununu'] = 40
colors['tatanunu'] = 38

#colors['Zbb'] = ROOT.kRed-4
#colors['Zcc'] = ROOT.kOrange-3
#colors['Zud'] = ROOT.kYellow-4
#colors['Ztautau'] = ROOT.kGreen-3
#colors['Zee'] = ROOT.kCyan-3
#colors['Zmumu'] = ROOT.kBlue-7
#colors['Zss'] = ROOT.kViolet-4

plots = {}
plots['HNL'] = {'signal':{
                    'HNL_4e-8_10gev':['HNL_4e-8_10gev'],
                    'HNL_1.33e-9_20gev':['HNL_1.33e-9_20gev'],
                    'HNL_2.86e-12_30gev':['HNL_2.86e-12_30gev'],
                    'HNL_2.86e-7_30gev':['HNL_2.86e-7_30gev'],
                    'HNL_5e-12_40gev':['HNL_5e-12_40gev'],
                    'HNL_4e-12_50gev':['HNL_4e-12_50gev'],
                    'HNL_6.67e-8_60gev':['HNL_6.67e-8_60gev'],
                    'HNL_4e-8_60gev':['HNL_4e-8_60gev'],
                    'HNL_2.86e-9_70gev':['HNL_2.86e-9_70gev'],
                    'HNL_2.86e-8_80gev':['HNL_2.86e-8_80gev'],
                },
                'backgrounds':{
                    #'HNL':['HNL_2.86e-12_30gev'], ### impossible to plot without both signals and backgrounds, choose one signal and make it white ### 
                    'Zud': ['p8_ee_Zud_ecm91'],
                    'Zss':['p8_ee_Zss_ecm91'],
                    'Zcc': ['p8_ee_Zcc_ecm91'],
                    'Zbb':['p8_ee_Zbb_ecm91'],
                    'Zee':['p8_ee_Zee_ecm91'],
                    'Zmumu': ['p8_ee_Zmumu_ecm91'],
                    'Ztautau': ['p8_ee_Ztautau_ecm91'],
                    'tatanunu': ['tatanunu'],
                    'emununu': ['emununu'],
                },
                }

legend = {}

legend['HNL_4e-8_10gev'] = 'U^{2}=4e-8, M_{N}=10 GeV'
legend['HNL_1.33e-9_20gev'] = 'U^{2}=1.33e-9, M_{N}=20 GeV'
legend['HNL_2.86e-12_30gev'] = 'U^{2}=2.86e-12, M_{N}=30 GeV'
legend['HNL_2.86e-7_30gev'] = 'U^{2}=2.86e-7, M_{N}=30 GeV'
legend['HNL_5e-12_40gev'] = 'U^{2}=5e-12, M_{N}=40 GeV'
legend['HNL_4e-12_50gev'] = 'U^{2}=4e-12, M_{N}=50 GeV'
legend['HNL_6.67e-8_60gev'] = 'U^{2}=6.67e-8, M_{N}=60 GeV'
legend['HNL_4e-8_60gev'] = 'U^{2}=4e-8, M_{N}=60 GeV'
legend['HNL_2.86e-9_70gev'] = 'U^{2}=2.86e-9, M_{N}=70 GeV'
legend['HNL_2.86e-8_80gev'] = 'U^{2}=2.86e-8, M_{N}=80 GeV'

legend['HNL'] = ''

legend['Zud'] = 'Z #rightarrow ud'
legend['Zss'] = 'Z #rightarrow ss'
legend['Zbb'] = 'Z #rightarrow bb'
legend['Zcc'] = 'Z #rightarrow cc'
legend['Zee'] = 'Z #rightarrow ee'
legend['Zmumu'] = 'Z #rightarrow #mu#mu'
legend['Ztautau'] = 'Z #rightarrow #tau#tau'
legend['emununu'] = 'e#mu#nu#nu'
legend['tatanunu'] = '#tau#tau#nu#nu'