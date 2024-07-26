import os, copy # tagging

#Mandatory: List of processes
processList = {
#             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365': {'chunks':1, 'fraction':0.0001}
             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365':   {'chunks':6},
             #'wzp6_ee_SM_tt_tWbTWs_tallTlight_ecm365': {'chunks':6},
             #'wzp6_ee_SM_tt_tWbTWs_tallTheavy_ecm365': {'chunks':6},
             #'wzp6_ee_SM_tt_tWsTWb_tlepTall_ecm365':   {'chunks':6},
             #'wzp6_ee_SM_tt_tWsTWb_tlightTall_ecm365': {'chunks':6},
             #'wzp6_ee_SM_tt_tWsTWb_theavyTall_ecm365': {'chunks':6},

             #'wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             #'wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             #'wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             #'wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13}

#             'p8_ee_ZZ_ecm365': {'chunks':1, 'fraction':0.0001}
#             'p8_ee_WW_ecm365': {'chunks':50},
#             'p8_ee_ZZ_ecm365': {'chunks':50},

             # ZH samples, no inclusive ones
#             'wzp6_ee_bbH_ecm365': {'chunks':5},
#             'wzp6_ee_ccH_ecm365': {'chunks':5},
#             'wzp6_ee_ssH_ecm365': {'chunks':5},
#             'wzp6_ee_qqH_ecm365': {'chunks':5},
#             'wzp6_ee_tautauH_ecm365': {'chunks':5},
#             'wzp6_ee_mumuH_ecm365': {'chunks':5},
#             'wzp6_ee_eeH_ecm365': {'chunks':5},
#             'wzp6_ee_nunuH_ecm365': {'chunks':5}

            }

#Optional: output directory, default is local running directory
inputDir = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July10/winter2023"
outputDir   = "outputs/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July10/winter2023"

#Optional
nCPUS       = 8
runBatch    = False
batchQueue = "nextweek"
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df


                #### INCLUSIVE JET ALGORITHM

                .Define("dilep_R5_cat",   "(n_muons_sel+n_electrons_sel==2 and n_jets_pass==2) * 1.0")
                .Define("semilep_R5_cat", "(n_muons_sel+n_electrons_sel==1 and n_jets_pass==4) * 1.0")
                .Define("dihad_R5_cat",   "(n_muons_sel+n_electrons_sel==0 and n_jets_pass==6) * 1.0")

                .Define("jet_R5_cat_p4",     "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return myUtils::build_p4(jet_pass_px, jet_pass_py, jet_pass_pz, jet_pass_energy); else return ROOT::VecOps::RVec<TLorentzVector>{};")
                .Define("jet_R5_cat_px",     "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_px; else return float(-99.);")
                .Define("jet_R5_cat_py",     "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_py; else return float(-99.);")
                .Define("jet_R5_cat_pz",     "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_pz; else return float(-99.);")
                .Define("jet_R5_cat_phi",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_phi; else return float(-99.);")
                .Define("jet_R5_cat_eta",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_eta; else return float(-99.);")
                .Define("jet_R5_cat_energy", "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_energy; else return float(-99.);")
                .Define("jet_R5_cat_mass",   "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_mass; else return float(-99.);")
                .Define("jet_R5_cat_dR_b",   "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_dR_b; else return float(-99.);")
                .Define("jet_R5_cat_dR_s",   "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_dR_s; else return float(-99.);")
                .Define("jet_R5_cat_isSig",  "(jet_R5_cat_dR_s<0.3) * 1.0")

                .Define("jet_R5_cat_flavor", "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_flavor; else return float(-99.);")
                .Define("jet_R5_cat_isG",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_isG; else return float(-99.);")
                .Define("jet_R5_cat_isQ",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_isQ; else return float(-99.);")
                .Define("jet_R5_cat_isS",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_isS; else return float(-99.);")
                .Define("jet_R5_cat_isC",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_isC; else return float(-99.);")
                .Define("jet_R5_cat_isB",    "if (dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1) return jet_pass_isB; else return float(-99.);")

                .Define("n_jets_R5_cat",     "return int(jet_R5_cat_flavor.size())")

                .Define("dijet_R5_cs_ind",         "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_R5_cat_isC, jet_R5_cat_isS)")
                .Define("dijet_R5_cat_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_R5_cs_ind, jet_R5_cat_p4)")
                .Define("dijet_R5_cat_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_R5_cs_ind, jet_R5_cat_p4)")
                .Define("dijet_R5_cat_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_R5_cs_ind, jet_R5_cat_p4)")
                .Define("dijet_R5_cat_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_R5_cs_ind, jet_R5_cat_p4)")
                .Define("dijet_R5_cat_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_R5_cs_ind, jet_R5_cat_p4)")


                #### EXCLUSIVE JET ALGORITHMS

                .Define("jet_ktN_cat_p4",               "if (dilep_cat==1) return myUtils::build_p4(jet_kt6_px, jet_kt6_py, jet_kt6_pz, jet_kt6_energy); if (semilep_cat==1) return myUtils::build_p4(jet_kt4_px, jet_kt4_py, jet_kt4_pz, jet_kt4_energy); \
                                                        if (dihad_cat==1) return myUtils::build_p4(jet_kt2_px, jet_kt2_py, jet_kt2_pz, jet_kt2_energy); else return ROOT::VecOps::RVec<TLorentzVector>{};")
                .Define("jet_ktN_cat_cat_px",           "if (dilep_cat==1) return jet_kt6_px; if (semilep_cat==1) return jet_kt4_px; if (dihad_cat==1) return jet_kt2_px; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_py",           "if (dilep_cat==1) return jet_kt6_py; if (semilep_cat==1) return jet_kt4_py; if (dihad_cat==1) return jet_kt2_py; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_pz",           "if (dilep_cat==1) return jet_kt6_pz; if (semilep_cat==1) return jet_kt4_pz; if (dihad_cat==1) return jet_kt2_pz; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_phi",           "if (dilep_cat==1) return jet_kt6_phi; if (semilep_cat==1) return jet_kt4_phi; if (dihad_cat==1) return jet_kt2_phi; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_eta",           "if (dilep_cat==1) return jet_kt6_eta; if (semilep_cat==1) return jet_kt4_eta; if (dihad_cat==1) return jet_kt2_eta; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_energy",           "if (dilep_cat==1) return jet_kt6_energy; if (semilep_cat==1) return jet_kt4_energy; if (dihad_cat==1) return jet_kt2_energy; else return float(-99.0)")
                .Define("jet_ktN_cat_cat_mass",           "if (dilep_cat==1) return jet_kt6_mass; if (semilep_cat==1) return jet_kt4_mass; if (dihad_cat==1) return jet_kt2_mass; else return float(-99.0)")

                .Define("jet_ktN_cat_cat_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_ktN_cat_cat_phi - genBottom_phi.at(0)))); else return (3.1416+jet_ktN_cat_cat_phi);")
                .Define("jet_ktN_cat_cat_dEta_b",       "if (n_genBottoms>0) return abs(jet_ktN_cat_eta - genBottom_eta.at(0)); else return (99+jet_ktN_cat_eta);")
                .Define("jet_ktN_cat_dR_b",         "sqrt(jet_ktN_cat_dPhi_b*jet_ktN_cat_dPhi_b + jet_ktN_cat_dEta_b*jet_ktN_cat_dEta_b)")
                .Define("jet_ktN_cat_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_ktN_cat_phi - genStrange_phi.at(0)))); else return (3.1416+jet_ktN_cat_phi);")
                .Define("jet_ktN_cat_dEta_s",       "if (n_genStranges>0) return abs(jet_ktN_cat_eta - genStrange_eta.at(0)); else return (99+jet_ktN_cat_eta);")
                .Define("jet_ktN_cat_dR_s",         "sqrt(jet_ktN_cat_dPhi_s*jet_ktN_cat_dPhi_s + jet_ktN_cat_dEta_s*jet_ktN_cat_dEta_s)")
                .Define("jet_ktN_cat_isSig",        "(jet_ktN_cat_dR_s<0.3) * 1.0")
                .Define("jet_ktN_cat_Max_mass",     "Max(jet_ktN_cat_mass)")
                .Define("jet_ktN_cat_Min_energy",   "Min(jet_ktN_cat_energy)")

                .Define("jet_ktN_cat_flavour",      "if (dilep_cat==1) return jet_kt6_flavour; if (semilep_cat==1) return jet_kt4_flavour; if (dihad_cat==1) return jet_kt2_flavour; else return float(-99.0)")
                .Define("jet_ktN_cat_isG",    "if (dilep_cat==1) return recojet_isG_kt6; if (semilep_cat==1) return recojet_isG_kt4; if (dihad_cat==1) return recojet_isG_kt2; else return float(-99.);")
                .Define("jet_ktN_cat_isQ",    "if (dilep_cat==1) return recojet_isQ_kt6; if (semilep_cat==1) return recojet_isQ_kt4; if (dihad_cat==1) return recojet_isQ_kt2; else return float(-99.);")
                .Define("jet_ktN_cat_isS",    "if (dilep_cat==1) return recojet_isS_kt6; if (semilep_cat==1) return recojet_isS_kt4; if (dihad_cat==1) return recojet_isS_kt2; else return float(-99.);")
                .Define("jet_ktN_cat_isC",    "if (dilep_cat==1) return recojet_isC_kt6; if (semilep_cat==1) return recojet_isC_kt4; if (dihad_cat==1) return recojet_isC_kt2; else return float(-99.);")
                .Define("jet_ktN_cat_isB",    "if (dilep_cat==1) return recojet_isB_kt6; if (semilep_cat==1) return recojet_isB_kt4; if (dihad_cat==1) return recojet_isB_kt2; else return float(-99.);")

                .Define("n_jets_ktN_cat",      "if (dilep_cat==1) return n_jets_kt6; if (semilep_cat==1) return n_jets_kt4; if (dihad_cat==1) return n_jets_kt2; else return float(-99.0)")

                .Define("dijet_ktN_cs_ind",         "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_ktN_cat_isC, jet_ktN_cat_isS)")
                .Define("dijet_ktN_cat_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ktN_cs_ind, jet_ktN_cat_p4)")
                .Define("dijet_ktN_cat_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_ktN_cs_ind, jet_ktN_cat_p4)")
                .Define("dijet_ktN_cat_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ktN_cs_ind, jet_ktN_cat_p4)")
                .Define("dijet_ktN_cat_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_ktN_cs_ind, jet_ktN_cat_p4)")
                .Define("dijet_ktN_cat_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_ktN_cs_ind, jet_ktN_cat_p4)")

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
        branchList += ["jet_pass_px", "jet_pass_py", "jet_pass_pz", "jet_pass_phi", "jet_pass_eta", "jet_pass_energy", "jet_pass_mass", "jet_pass_flavor",
                       "jet_pass_dR_b", "jet_pass_dR_s", "jet_pass_isSig",     
                       "jet_pass_isG", "jet_pass_isQ", "jet_pass_isS", "jet_pass_isC", "jet_pass_isB", "n_jets_pass"]
        branchList += ["jet_kt6_px", "jet_kt6_py", "jet_kt6_pz", "jet_kt6_phi", "jet_kt6_eta", "jet_kt6_energy", "jet_kt6_mass", "jet_kt6_flavor",
                       "jet_kt6_dR_b", "jet_kt6_dR_s", "jet_kt6_isSig",
                       "recojet_isG_kt6", "recojet_isQ_kt6", "recojet_isS_kt6", "recojet_isC_kt6", "recojet_isB_kt6"]
        branchList += ["n_jets_kt2", "n_jets_kt4", "n_jets_kt6"]
        branchList += ["n_btags", "n_btags_kt2", "n_btags_kt4", "n_btags_kt6"]
        branchList += ["n_ctags", "n_ctags_kt2", "n_ctags_kt4", "n_ctags_kt6"]
        branchList += ["n_stags", "n_stags_kt2", "n_stags_kt4", "n_stags_kt6"]
        branchList += ["jet_kt2_Max_mass", "jet_kt2_Min_energy", "jet_kt4_Max_mass", "jet_kt4_Min_energy", "jet_kt6_Max_mass", "jet_kt6_Min_energy"]
        branchList += ["dilep_cat", "semilep_cat", "dihad_cat"]
        branchList += ["jet_leadS_px",   "jet_leadS_py",     "jet_leadS_pz",   "jet_leadS_phi",  "jet_leadS_eta", "jet_leadS_energy", 
                       "jet_leadS_mass", "jet_leadS_flavor", "jet_leadS_dR_b", "jet_leadS_dR_s", "jet_leadS_isSig",
                       "jet_leadS_isG",  "jet_leadS_isQ",    "jet_leadS_isS",  "jet_leadS_isC",  "jet_leadS_isB"]
        branchList += ["jet_subS_px",   "jet_subS_py",     "jet_subS_pz",   "jet_subS_phi",  "jet_subS_eta", "jet_subS_energy",
                       "jet_subS_mass", "jet_subS_flavor", "jet_subS_dR_b", "jet_subS_dR_s", "jet_subS_isSig",
                       "jet_subS_isG",  "jet_subS_isQ",    "jet_subS_isS",  "jet_subS_isC",  "jet_subS_isB"]
        branchList += ["jet_leadC_px",   "jet_leadC_py",     "jet_leadC_pz",   "jet_leadC_phi",  "jet_leadC_eta", "jet_leadC_energy",
                       "jet_leadC_mass", "jet_leadC_flavor", "jet_leadC_dR_b", "jet_leadC_dR_s", "jet_leadC_isSig",
                       "jet_leadC_isG",  "jet_leadC_isQ",    "jet_leadC_isS",  "jet_leadC_isC",  "jet_leadC_isB"]
        branchList += ["jet_subC_px",   "jet_subC_py",     "jet_subC_pz",   "jet_subC_phi",  "jet_subC_eta", "jet_subC_energy",
                       "jet_subC_mass", "jet_subC_flavor", "jet_subC_dR_b", "jet_subC_dR_s", "jet_subC_isSig",
                       "jet_subC_isG",  "jet_subC_isQ",    "jet_subC_isS",  "jet_subC_isC",  "jet_subC_isB"]

        branchList += ["jet_kt2_leadS_px",   "jet_kt2_leadS_py",     "jet_kt2_leadS_pz",   "jet_kt2_leadS_phi",  "jet_kt2_leadS_eta", "jet_kt2_leadS_energy",
                       "jet_kt2_leadS_mass", "jet_kt2_leadS_flavor", "jet_kt2_leadS_dR_b", "jet_kt2_leadS_dR_s", "jet_kt2_leadS_isSig",
                       "jet_kt2_leadS_isG",  "jet_kt2_leadS_isQ",    "jet_kt2_leadS_isS",  "jet_kt2_leadS_isC",  "jet_kt2_leadS_isB"]
        branchList += ["jet_kt2_subS_px",    "jet_kt2_subS_py",      "jet_kt2_subS_pz",    "jet_kt2_subS_phi",   "jet_kt2_subS_eta", "jet_kt2_subS_energy",
                       "jet_kt2_subS_mass",  "jet_kt2_subS_flavor",  "jet_kt2_subS_dR_b",  "jet_kt2_subS_dR_s",  "jet_kt2_subS_isSig",
                       "jet_kt2_subS_isG",   "jet_kt2_subS_isQ",     "jet_kt2_subS_isS",   "jet_kt2_subS_isC",   "jet_kt2_subS_isB"]
        branchList += ["jet_kt2_leadC_px",   "jet_kt2_leadC_py",     "jet_kt2_leadC_pz",   "jet_kt2_leadC_phi",  "jet_kt2_leadC_eta", "jet_kt2_leadC_energy",
                       "jet_kt2_leadC_mass", "jet_kt2_leadC_flavor", "jet_kt2_leadC_dR_b", "jet_kt2_leadC_dR_s", "jet_kt2_leadC_isSig",
                       "jet_kt2_leadC_isG",  "jet_kt2_leadC_isQ",    "jet_kt2_leadC_isS",  "jet_kt2_leadC_isC",  "jet_kt2_leadC_isB"]
        branchList += ["jet_kt2_subC_px",    "jet_kt2_subC_py",      "jet_kt2_subC_pz",    "jet_kt2_subC_phi",   "jet_kt2_subC_eta", "jet_kt2_subC_energy",
                       "jet_kt2_subC_mass",  "jet_kt2_subC_flavor",  "jet_kt2_subC_dR_b",  "jet_kt2_subC_dR_s",  "jet_kt2_subC_isSig",
                       "jet_kt2_subC_isG",   "jet_kt2_subC_isQ",     "jet_kt2_subC_isS",   "jet_kt2_subC_isC",   "jet_kt2_subC_isB"]
        branchList += ["jet_kt4_leadS_px",   "jet_kt4_leadS_py",     "jet_kt4_leadS_pz",   "jet_kt4_leadS_phi",  "jet_kt4_leadS_eta", "jet_kt4_leadS_energy",
                       "jet_kt4_leadS_mass", "jet_kt4_leadS_flavor", "jet_kt4_leadS_dR_b", "jet_kt4_leadS_dR_s", "jet_kt4_leadS_isSig",
                       "jet_kt4_leadS_isG",  "jet_kt4_leadS_isQ",    "jet_kt4_leadS_isS",  "jet_kt4_leadS_isC",  "jet_kt4_leadS_isB"]
        branchList += ["jet_kt4_subS_px",    "jet_kt4_subS_py",      "jet_kt4_subS_pz",    "jet_kt4_subS_phi",   "jet_kt4_subS_eta", "jet_kt4_subS_energy",
                       "jet_kt4_subS_mass",  "jet_kt4_subS_flavor",  "jet_kt4_subS_dR_b",  "jet_kt4_subS_dR_s",  "jet_kt4_subS_isSig",
                       "jet_kt4_subS_isG",   "jet_kt4_subS_isQ",     "jet_kt4_subS_isS",   "jet_kt4_subS_isC",   "jet_kt4_subS_isB"]
        branchList += ["jet_kt4_leadC_px",   "jet_kt4_leadC_py",     "jet_kt4_leadC_pz",   "jet_kt4_leadC_phi",  "jet_kt4_leadC_eta", "jet_kt4_leadC_energy",
                       "jet_kt4_leadC_mass", "jet_kt4_leadC_flavor", "jet_kt4_leadC_dR_b", "jet_kt4_leadC_dR_s", "jet_kt4_leadC_isSig",
                       "jet_kt4_leadC_isG",  "jet_kt4_leadC_isQ",    "jet_kt4_leadC_isS",  "jet_kt4_leadC_isC",  "jet_kt4_leadC_isB"]
        branchList += ["jet_kt4_subC_px",    "jet_kt4_subC_py",      "jet_kt4_subC_pz",    "jet_kt4_subC_phi",   "jet_kt4_subC_eta", "jet_kt4_subC_energy",
                       "jet_kt4_subC_mass",  "jet_kt4_subC_flavor",  "jet_kt4_subC_dR_b",  "jet_kt4_subC_dR_s",  "jet_kt4_subC_isSig",
                       "jet_kt4_subC_isG",   "jet_kt4_subC_isQ",     "jet_kt4_subC_isS",   "jet_kt4_subC_isC",   "jet_kt4_subC_isB"]
        branchList += ["jet_kt6_leadS_px",   "jet_kt6_leadS_py",     "jet_kt6_leadS_pz",   "jet_kt6_leadS_phi",  "jet_kt6_leadS_eta", "jet_kt6_leadS_energy", 
                       "jet_kt6_leadS_mass", "jet_kt6_leadS_flavor", "jet_kt6_leadS_dR_b", "jet_kt6_leadS_dR_s", "jet_kt6_leadS_isSig",
                       "jet_kt6_leadS_isG",  "jet_kt6_leadS_isQ",    "jet_kt6_leadS_isS",  "jet_kt6_leadS_isC",  "jet_kt6_leadS_isB"]
        branchList += ["jet_kt6_subS_px",    "jet_kt6_subS_py",      "jet_kt6_subS_pz",    "jet_kt6_subS_phi",   "jet_kt6_subS_eta", "jet_kt6_subS_energy",
                       "jet_kt6_subS_mass",  "jet_kt6_subS_flavor",  "jet_kt6_subS_dR_b",  "jet_kt6_subS_dR_s",  "jet_kt6_subS_isSig",
                       "jet_kt6_subS_isG",   "jet_kt6_subS_isQ",     "jet_kt6_subS_isS",   "jet_kt6_subS_isC",   "jet_kt6_subS_isB"]
        branchList += ["jet_kt6_leadC_px",   "jet_kt6_leadC_py",     "jet_kt6_leadC_pz",   "jet_kt6_leadC_phi",  "jet_kt6_leadC_eta", "jet_kt6_leadC_energy",
                       "jet_kt6_leadC_mass", "jet_kt6_leadC_flavor", "jet_kt6_leadC_dR_b", "jet_kt6_leadC_dR_s", "jet_kt6_leadC_isSig",
                       "jet_kt6_leadC_isG",  "jet_kt6_leadC_isQ",    "jet_kt6_leadC_isS",  "jet_kt6_leadC_isC",  "jet_kt6_leadC_isB"]
        branchList += ["jet_kt6_subC_px",    "jet_kt6_subC_py",      "jet_kt6_subC_pz",    "jet_kt6_subC_phi",   "jet_kt6_subC_eta", "jet_kt6_subC_energy",
                       "jet_kt6_subC_mass",  "jet_kt6_subC_flavor",  "jet_kt6_subC_dR_b",  "jet_kt6_subC_dR_s",  "jet_kt6_subC_isSig",
                       "jet_kt6_subC_isG",   "jet_kt6_subC_isQ",     "jet_kt6_subC_isS",   "jet_kt6_subC_isC",   "jet_kt6_subC_isB"]

        #### stage2 variables ####
        branchList += ["dilep_R5_cat", "semilep_R5_cat", "dihad_R5_cat"]
        branchList += ["jet_R5_cat_px", "jet_R5_cat_py", "jet_R5_cat_pz", "jet_R5_cat_phi", "jet_R5_cat_eta", "jet_R5_cat_energy", "jet_R5_cat_mass", "jet_R5_cat_flavor",
                        "n_jets_R5_cat", "jet_R5_cat_isG", "jet_R5_cat_isQ", "jet_R5_cat_isS", "jet_R5_cat_isC", "jet_R5_cat_isB",
                        "dijet_R5_cat_px", "dijet_R5_cat_py", "dijet_R5_cat_pz", "dijet_R5_cat_energy", "dijet_R5_cat_mass"]
        branchList += ["jet_ktN_cat_px", "jet_ktN_cat_py", "jet_ktN_cat_pz", "jet_ktN_cat_phi", "jet_ktN_cat_eta", "jet_ktN_cat_energy", "jet_ktN_cat_mass", "jet_ktN_cat_flavor",
                        "n_jets_ktN_cat", "jet_ktN_cat_isG", "jet_ktN_cat_isQ", "jet_ktN_cat_isS", "jet_ktN_cat_isC", "jet_ktN_cat_isB",
                        "dijet_ktN_cat_px", "dijet_ktN_cat_py", "dijet_ktN_cat_pz", "dijet_ktN_cat_energy", "dijet_ktN_cat_mass"]

        return branchList