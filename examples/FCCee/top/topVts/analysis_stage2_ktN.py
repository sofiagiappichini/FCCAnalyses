import os, copy # tagging

#Mandatory: List of processes
processList = {
            'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365': {'chunks':1, 'fraction':0.0001},
            'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365':   {'chunks':6},
            'wzp6_ee_SM_tt_tWbTWs_tallTlight_ecm365': {'chunks':6},
            'wzp6_ee_SM_tt_tWbTWs_tallTheavy_ecm365': {'chunks':6},
            'wzp6_ee_SM_tt_tWsTWb_tlepTall_ecm365':   {'chunks':6},
            'wzp6_ee_SM_tt_tWsTWb_tlightTall_ecm365': {'chunks':6},
            'wzp6_ee_SM_tt_tWsTWb_theavyTall_ecm365': {'chunks':6},

            'wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
            'wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
            'wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
            'wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13},

            'p8_ee_WW_ecm365': {'chunks':50},
            'p8_ee_ZZ_ecm365': {'chunks':50},

            # ZH samples, no inclusive ones
            'wzp6_ee_bbH_ecm365': {'chunks':5},
            'wzp6_ee_ccH_ecm365': {'chunks':5},
            'wzp6_ee_ssH_ecm365': {'chunks':5},
            'wzp6_ee_qqH_ecm365': {'chunks':5},
            'wzp6_ee_tautauH_ecm365': {'chunks':5},
            'wzp6_ee_mumuH_ecm365': {'chunks':5},
            'wzp6_ee_eeH_ecm365': {'chunks':5},
            'wzp6_ee_nunuH_ecm365': {'chunks':5},

            }

#Optional: output directory, default is local running directory
inputDir = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July24/winter2023"
outputDir   = "outputs/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July10/winter2023/stage2_ktN"

#Optional
nCPUS       = 8
runBatch    = False
batchQueue = "nextweek"
compGroup = "group_u_FCC.local_gen"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

                .Filter("dilep_cat==1 || semilep_cat==1 || dihad_cat==1")


                #### EXCLUSIVE JET ALGORITHMS

                .Define("jet_ktN_p4",               "if (dilep_cat==1) return myUtils::build_p4(jet_kt6_px, jet_kt6_py, jet_kt6_pz, jet_kt6_energy); if (semilep_cat==1) return myUtils::build_p4(jet_kt4_px, jet_kt4_py, jet_kt4_pz, jet_kt4_energy); \
                                                        if (dihad_cat==1) return myUtils::build_p4(jet_kt2_px, jet_kt2_py, jet_kt2_pz, jet_kt2_energy); else return ROOT::VecOps::RVec<TLorentzVector>{};")
                .Define("jet_ktN_px",           "if (dilep_cat==1) return jet_kt6_px; if (semilep_cat==1) return jet_kt4_px; if (dihad_cat==1) return jet_kt2_px; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_py",           "if (dilep_cat==1) return jet_kt6_py; if (semilep_cat==1) return jet_kt4_py; if (dihad_cat==1) return jet_kt2_py; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_pz",           "if (dilep_cat==1) return jet_kt6_pz; if (semilep_cat==1) return jet_kt4_pz; if (dihad_cat==1) return jet_kt2_pz; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_phi",           "if (dilep_cat==1) return jet_kt6_phi; if (semilep_cat==1) return jet_kt4_phi; if (dihad_cat==1) return jet_kt2_phi; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_eta",           "if (dilep_cat==1) return jet_kt6_eta; if (semilep_cat==1) return jet_kt4_eta; if (dihad_cat==1) return jet_kt2_eta; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_energy",           "if (dilep_cat==1) return jet_kt6_energy; if (semilep_cat==1) return jet_kt4_energy; if (dihad_cat==1) return jet_kt2_energy; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_mass",           "if (dilep_cat==1) return jet_kt6_mass; if (semilep_cat==1) return jet_kt4_mass; if (dihad_cat==1) return jet_kt2_mass; else return ROOT::VecOps::RVec<float>{}")

                #.Define("jet_ktN_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_ktN_phi - genBottom_phi.at(0)))); else return (3.1416+jet_ktN_phi);")
                #.Define("jet_ktN_dEta_b",       "if (n_genBottoms>0) return abs(jet_ktN_eta - genBottom_eta.at(0)); else return (99+jet_ktN_eta);")
                #.Define("jet_ktN_dR_b",         "sqrt(jet_ktN_dPhi_b*jet_ktN_dPhi_b + jet_ktN_dEta_b*jet_ktN_dEta_b)")
                #.Define("jet_ktN_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_ktN_phi - genStrange_phi.at(0)))); else return (3.1416+jet_ktN_phi);")
                #.Define("jet_ktN_dEta_s",       "if (n_genStranges>0) return abs(jet_ktN_eta - genStrange_eta.at(0)); else return (99+jet_ktN_eta);")
                #.Define("jet_ktN_dR_s",         "sqrt(jet_ktN_dPhi_s*jet_ktN_dPhi_s + jet_ktN_dEta_s*jet_ktN_dEta_s)")
                #.Define("jet_ktN_isSig",        "(jet_ktN_dR_s<0.3) * 1.0")
                .Define("jet_ktN_Max_mass",     "Max(jet_ktN_mass)")
                .Define("jet_ktN_Min_energy",   "Min(jet_ktN_energy)")

                .Define("jet_ktN_flavour",      "if (dilep_cat==1) return jet_kt6_flavour; if (semilep_cat==1) return jet_kt4_flavour; if (dihad_cat==1) return jet_kt2_flavour; else return ROOT::VecOps::RVec<float>{}")
                .Define("jet_ktN_isG",    "if (dilep_cat==1) return recojet_isG_kt6; if (semilep_cat==1) return recojet_isG_kt4; if (dihad_cat==1) return recojet_isG_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isQ",    "if (dilep_cat==1) return recojet_isQ_kt6; if (semilep_cat==1) return recojet_isQ_kt4; if (dihad_cat==1) return recojet_isQ_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isS",    "if (dilep_cat==1) return recojet_isS_kt6; if (semilep_cat==1) return recojet_isS_kt4; if (dihad_cat==1) return recojet_isS_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isC",    "if (dilep_cat==1) return recojet_isC_kt6; if (semilep_cat==1) return recojet_isC_kt4; if (dihad_cat==1) return recojet_isC_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isB",    "if (dilep_cat==1) return recojet_isB_kt6; if (semilep_cat==1) return recojet_isB_kt4; if (dihad_cat==1) return recojet_isB_kt2; else return ROOT::VecOps::RVec<float>{};")

                .Define("n_jets_ktN",      "if (dilep_cat==1) return n_jets_kt6; if (semilep_cat==1) return n_jets_kt4; if (dihad_cat==1) return n_jets_kt2; else return ROOT::VecOps::RVec<float>{}")
                .Define("n_jets_ktN_btag",      "if (dilep_cat==1) return n_btags_kt6; if (semilep_cat==1) return n_btags_kt4; if (dihad_cat==1) return n_btags_kt2; else return ROOT::VecOps::RVec<float>{}")
                .Define("n_jets_ktN_ctag",      "if (dilep_cat==1) return n_ctags_kt6; if (semilep_cat==1) return n_ctags_kt4; if (dihad_cat==1) return n_ctags_kt2; else return ROOT::VecOps::RVec<float>{}")
                .Define("n_jets_ktN_stag",      "if (dilep_cat==1) return n_stags_kt6; if (semilep_cat==1) return n_stags_kt4; if (dihad_cat==1) return n_stags_kt2; else return ROOT::VecOps::RVec<float>{}")

                .Define("dijet_ktN_cs_ind",         "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_ktN_isC, jet_ktN_isS)")
                .Define("dijet_ktN_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ktN_cs_ind, jet_ktN_p4)")
                .Define("dijet_ktN_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_ktN_cs_ind, jet_ktN_p4)")
                .Define("dijet_ktN_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ktN_cs_ind, jet_ktN_p4)")
                .Define("dijet_ktN_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_ktN_cs_ind, jet_ktN_p4)")
                .Define("dijet_ktN_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_ktN_cs_ind, jet_ktN_p4)")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genBottoms", "n_genStranges", "n_genMuons", "n_genElectrons", 
                 "Wp_elenu", "Wp_munu", "Wp_taunu", "Wp_d", "Wp_s", "Wp_b",
                 "Wm_elenu", "Wm_munu", "Wm_taunu", "Wm_d", "Wm_s", "Wm_b",
                 "genW_px", "genW_py", "genW_pz", "genW_phi", "genW_eta", "genW_energy", "genW_mass", "genW_charge",
                 "n_muons", "n_electrons", "n_photons",
                 "muon_px", "muon_py", "muon_pz", "muon_phi", "muon_eta", "muon_energy", "muon_mass", "muon_charge",
                 "electron_px", "electron_py", "electron_pz", "electron_phi", "electron_eta", "electron_energy", "electron_mass", "electron_charge",
                 "photon_px", "photon_py", "photon_pz", "photon_phi", "photon_eta", "photon_energy", "photon_mass",
                 #"Emiss_energy", "Emiss_p", "Emiss_px", "Emiss_py", "Emiss_pz", "Emiss_phi", "Emiss_eta",
                 "recoEmiss_px", "recoEmiss_py", "recoEmiss_pz", "recoEmiss_e"
                 ]

        branchList += ["n_muons_sel", "n_electrons_sel",
                       "muon_1_px", "muon_1_py", "muon_1_pz", "muon_1_phi", "muon_1_eta", "muon_1_energy", "muon_1_charge",
                       "muon_2_px", "muon_2_py", "muon_2_pz", "muon_2_phi", "muon_2_eta", "muon_2_energy", "muon_2_charge",
                       "electron_1_px", "electron_1_py", "electron_1_pz", "electron_1_phi", "electron_1_eta", "electron_1_energy", "electron_1_charge",
                       "electron_2_px", "electron_2_py", "electron_2_pz", "electron_2_phi", "electron_2_eta", "electron_2_energy", "electron_2_charge"
                       ]

        #branchList += jetFlavourHelper_R5. outputBranches()
        #branchList = [item for item in branchList if item not in ["jet_kt2","jet_R5"]] 
        #branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor"]
        branchList += ["dilep_cat", "semilep_cat", "dihad_cat"]

        #### stage2 variables ####
        branchList += ["jet_ktN_px", "jet_ktN_py", "jet_ktN_pz", "jet_ktN_phi", "jet_ktN_eta", "jet_ktN_energy", "jet_ktN_mass", "jet_ktN_flavor",
                        "n_jets_ktN", "n_jets_ktN_btag", "n_jets_ktN_ctag", "n_jets_ktN_stag",
                        "jet_ktN_isG", "jet_ktN_isQ", "jet_ktN_isS", "jet_ktN_isC", "jet_ktN_isB",
                        "dijet_ktN_px", "dijet_ktN_py", "dijet_ktN_pz", "dijet_ktN_energy", "dijet_ktN_mass"]

        return branchList