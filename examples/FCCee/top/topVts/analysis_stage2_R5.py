import os, copy # tagging

#Mandatory: List of processes
processList = {
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
outputDir   = "/eos/user/s/sgiappic/topVts/stage2_R5"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July24/winter2023/stage2_R5"

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


                #### INCLUSIVE JET ALGORITHM

                .Define("dilep_R5_cat",   "(n_muons_sel+n_electrons_sel==2 and n_jets_pass==2) * 1.0")
                .Define("semilep_R5_cat", "(n_muons_sel+n_electrons_sel==1 and n_jets_pass==4) * 1.0")
                .Define("dihad_R5_cat",   "(n_muons_sel+n_electrons_sel==0 and n_jets_pass==6) * 1.0")

                .Filter("dilep_R5_cat==1 || semilep_R5_cat==1 || dihad_R5_cat==1")

                .Define("jet_R5_p4",     "myUtils::build_p4(jet_pass_px, jet_pass_py, jet_pass_pz, jet_pass_energy)")

                ## cs dijets and trijets

                .Define("dijet_cs_R5_idx",     "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_pass_isC, jet_pass_isS, {jet_leadS_idx, jet_leadB_idx}, false)")
                .Define("dijet_cs_R5_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_cs_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_cs_R5_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_cs_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_cs_R5_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_cs_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_cs_R5_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_cs_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_cs_R5_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_cs_R5_idx, jet_R5_cat_p4)")
                .Define("n_dijet_cs_R5",   "int(dijet_cs_R5_mass.size())")

                .Define("trijet_Scs_R5_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_cs_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Scs_R5_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(dijet_cs_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Scs_R5_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_cs_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Scs_R5_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(dijet_cs_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Scs_R5_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(dijet_cs_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("n_trijet_Scs_R5",   "int(trijet_Scs_R5_mass.size())")

                .Define("trijet_Bcs_R5_idx",     "FCCAnalyses::ZHfunctions::get_trijet_idx(dijet_cs_R5_idx, jet_leadB_idx, jet_leadB_idx, false)")
                .Define("trijet_Bcs_R5_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_cs_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bcs_R5_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(dijet_cs_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bcs_R5_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_cs_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bcs_R5_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(dijet_cs_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bcs_R5_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(dijet_cs_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("n_trijet_Bcs_R5",   "int(trijet_Bcs_R5_mass.size())")

                ## ud dijets and trijets

                .Define("dijet_ud_R5_idx",     "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_pass_isQ, jet_pass_isQ, {jet_leadS_idx, jet_leadB_idx}, true)")
                .Define("dijet_ud_R5_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ud_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_ud_R5_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_ud_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_ud_R5_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ud_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_ud_R5_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_ud_R5_idx, jet_R5_cat_p4)")
                .Define("dijet_ud_R5_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_ud_R5_idx, jet_R5_cat_p4)")
                .Define("n_dijet_ud_R5",   "int(dijet_ud_R5_mass.size())")

                .Define("trijet_Sud_R5_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_ud_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Sud_R5_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(dijet_ud_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Sud_R5_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_ud_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Sud_R5_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(dijet_ud_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("trijet_Sud_R5_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(dijet_ud_R5_idx, jet_leadS_idx, jet_R5_cat_p4)")
                .Define("n_trijet_Sud_R5",   "int(trijet_Sud_R5_mass.size())")

                .Define("trijet_Bud_R5_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_ud_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bud_R5_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(dijet_ud_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bud_R5_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(dijet_ud_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bud_R5_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(dijet_ud_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("trijet_Bud_R5_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(dijet_ud_R5_idx, jet_leadB_idx, jet_R5_cat_p4)")
                .Define("n_trijet_Bud_R5",   "int(trijet_Bud_R5_mass.size())")                

                

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
                       "jet_pass_dR_b", "jet_pass_dR_s", "jet_pass_isSig", "jet_pass_isG", "jet_pass_isQ", "jet_pass_isS", "jet_pass_isC", "jet_pass_isB", "n_jets_pass"]
        branchList += ["jet_leadS_idx", "jet_leadS_px",   "jet_leadS_py",     "jet_leadS_pz",   "jet_leadS_phi",  "jet_leadS_eta", "jet_leadS_energy", 
                       "jet_leadS_mass", "jet_leadS_flavor", "jet_leadS_dR_b", "jet_leadS_dR_s", "jet_leadS_isSig",
                       "jet_leadS_isG",  "jet_leadS_isQ",    "jet_leadS_isS",  "jet_leadS_isC",  "jet_leadS_isB"]
        branchList += ["jet_subS_idx", "jet_subS_px",   "jet_subS_py",     "jet_subS_pz",   "jet_subS_phi",  "jet_subS_eta", "jet_subS_energy",
                       "jet_subS_mass", "jet_subS_flavor", "jet_subS_dR_b", "jet_subS_dR_s", "jet_subS_isSig",
                       "jet_subS_isG",  "jet_subS_isQ",    "jet_subS_isS",  "jet_subS_isC",  "jet_subS_isB"]
        branchList += ["jet_leadC_idx", "jet_leadC_px",   "jet_leadC_py",     "jet_leadC_pz",   "jet_leadC_phi",  "jet_leadC_eta", "jet_leadC_energy",
                       "jet_leadC_mass", "jet_leadC_flavor", "jet_leadC_dR_b", "jet_leadC_dR_s", "jet_leadC_isSig",
                       "jet_leadC_isG",  "jet_leadC_isQ",    "jet_leadC_isS",  "jet_leadC_isC",  "jet_leadC_isB"]
        branchList += ["jet_subC_idx", "jet_subC_px",   "jet_subC_py",     "jet_subC_pz",   "jet_subC_phi",  "jet_subC_eta", "jet_subC_energy",
                       "jet_subC_mass", "jet_subC_flavor", "jet_subC_dR_b", "jet_subC_dR_s", "jet_subC_isSig",
                       "jet_subC_isG",  "jet_subC_isQ",    "jet_subC_isS",  "jet_subC_isC",  "jet_subC_isB"]
        branchList += ["jet_leadB_idx", "jet_leadB_px",   "jet_leadB_py",     "jet_leadB_pz",   "jet_leadB_phi",  "jet_leadB_eta", "jet_leadB_energy", 
                       "jet_leadB_mass", "jet_leadB_flavor", "jet_leadB_dR_b", "jet_leadB_dR_s", "jet_leadB_isBig",
                       "jet_leadB_isG",  "jet_leadB_isQ",    "jet_leadB_isS",  "jet_leadB_isC",  "jet_leadB_isB"]
        branchList += ["jet_subB_idx", "jet_subB_px",   "jet_subB_py",     "jet_subB_pz",   "jet_subB_phi",  "jet_subB_eta", "jet_subB_energy",
                       "jet_subB_mass", "jet_subB_flavor", "jet_subB_dR_b", "jet_subB_dR_s", "jet_subB_isBig",
                       "jet_subB_isG",  "jet_subB_isQ",    "jet_subB_isS",  "jet_subB_isC",  "jet_subB_isB"]

        #### stage2 variables ####
        branchList += ["dilep_R5_cat", "semilep_R5_cat", "dihad_R5_cat"]
        branchList += ["dijet_cs_R5_idx", "dijet_cs_R5_px", "dijet_cs_R5_py", "dijet_cs_R5_pz", "dijet_cs_R5_energy", "dijet_cs_R5_mass", "n_cs_dijet_R5",
                        "trijet_Scs_R5_idx", "trijet_Scs_R5_px", "trijet_Scs_R5_py", "trijet_Scs_R5_pz", "trijet_Scs_R5_energy", "trijet_Scs_R5_mass", "n_Scs_trijet_R5",
                        "trijet_Bcs_R5_idx", "trijet_Bcs_R5_px", "trijet_Bcs_R5_py", "trijet_Bcs_R5_pz", "trijet_Bcs_R5_energy", "trijet_Bcs_R5_mass", "n_Bcs_trijet_R5"]
        branchList += ["dijet_ud_R5_idx", "dijet_ud_R5_px", "dijet_ud_R5_py", "dijet_ud_R5_pz", "dijet_ud_R5_energy", "dijet_ud_R5_mass", "n_ud_dijet_R5",
                        "trijet_Sud_R5_px", "trijet_Sud_R5_py", "trijet_Sud_R5_pz", "trijet_Sud_R5_energy", "trijet_Sud_R5_mass", "n_Sud_trijet_R5",
                        "trijet_Bud_R5_px", "trijet_Bud_R5_py", "trijet_Bud_R5_pz", "trijet_Bud_R5_energy", "trijet_Bud_R5_mass", "n_Bud_trijet_R5"]
        return branchList