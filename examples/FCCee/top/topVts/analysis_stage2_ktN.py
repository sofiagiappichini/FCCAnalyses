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
outputDir   = "/eos/user/s/sgiappic/topVts/stage2_ktN"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July10/winter2023/stage2_ktN"

#Optional
nCPUS       = 8
runBatch    = True
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

                .Define("jet_ktN_dR_b",        "if (dilep_cat==1) return jet_kt6_dR_b; if (semilep_cat==1) return jet_kt4_dR_b; if (dihad_cat==1) return jet_kt2_dR_b; else return ROOT::VecOps::RVec<double>{}")
                .Define("jet_ktN_dR_s",        "if (dilep_cat==1) return jet_kt6_dR_s; if (semilep_cat==1) return jet_kt4_dR_s; if (dihad_cat==1) return jet_kt2_dR_s; else return ROOT::VecOps::RVec<double>{}")
                .Define("jet_ktN_isSig",       "if (dilep_cat==1) return jet_kt6_isSig; if (semilep_cat==1) return jet_kt4_isSig; if (dihad_cat==1) return jet_kt2_isSig; else return ROOT::VecOps::RVec<double>{}")
                .Define("jet_ktN_Max_mass",     "Max(jet_ktN_mass)")
                .Define("jet_ktN_Min_energy",   "Min(jet_ktN_energy)")

                .Define("jet_ktN_flavor",      "if (dilep_cat==1) return jet_kt6_flavor; if (semilep_cat==1) return jet_kt4_flavor; if (dihad_cat==1) return jet_kt2_flavor; else return ROOT::VecOps::RVec<int>{}")
                .Define("jet_ktN_isG",    "if (dilep_cat==1) return recojet_isG_kt6; if (semilep_cat==1) return recojet_isG_kt4; if (dihad_cat==1) return recojet_isG_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isQ",    "if (dilep_cat==1) return recojet_isQ_kt6; if (semilep_cat==1) return recojet_isQ_kt4; if (dihad_cat==1) return recojet_isQ_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isS",    "if (dilep_cat==1) return recojet_isS_kt6; if (semilep_cat==1) return recojet_isS_kt4; if (dihad_cat==1) return recojet_isS_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isC",    "if (dilep_cat==1) return recojet_isC_kt6; if (semilep_cat==1) return recojet_isC_kt4; if (dihad_cat==1) return recojet_isC_kt2; else return ROOT::VecOps::RVec<float>{};")
                .Define("jet_ktN_isB",    "if (dilep_cat==1) return recojet_isB_kt6; if (semilep_cat==1) return recojet_isB_kt4; if (dihad_cat==1) return recojet_isB_kt2; else return ROOT::VecOps::RVec<float>{};")

                .Define("n_jets_ktN",      "if (dilep_cat==1) return n_jets_kt6; if (semilep_cat==1) return n_jets_kt4; if (dihad_cat==1) return n_jets_kt2; else return int(-1)")
                .Define("n_jets_ktN_btag",      "if (dilep_cat==1) return n_btags_kt6; if (semilep_cat==1) return n_btags_kt4; if (dihad_cat==1) return n_btags_kt2; else return int(-1)")
                .Define("n_jets_ktN_ctag",      "if (dilep_cat==1) return n_ctags_kt6; if (semilep_cat==1) return n_ctags_kt4; if (dihad_cat==1) return n_ctags_kt2; else return int(-1)")
                .Define("n_jets_ktN_stag",      "if (dilep_cat==1) return n_stags_kt6; if (semilep_cat==1) return n_stags_kt4; if (dihad_cat==1) return n_stags_kt2; else return int(-1)")

                .Define("jet_ktN_leadS_idx",    "if (dilep_cat==1) return jet_kt6_leadS_idx; if (semilep_cat==1) return jet_kt4_leadS_idx; if (dihad_cat==1) return jet_kt2_leadS_idx; else return int(-1)")
                .Define("jet_ktN_leadS_px",     "if (dilep_cat==1) return jet_kt6_leadS_px; if (semilep_cat==1) return jet_kt4_leadS_px; if (dihad_cat==1) return jet_kt2_leadS_px; else return float(-99.)")
                .Define("jet_ktN_leadS_py",     "if (dilep_cat==1) return jet_kt6_leadS_py; if (semilep_cat==1) return jet_kt4_leadS_py; if (dihad_cat==1) return jet_kt2_leadS_py; else return float(-99.)")
                .Define("jet_ktN_leadS_pz",     "if (dilep_cat==1) return jet_kt6_leadS_pz; if (semilep_cat==1) return jet_kt4_leadS_pz; if (dihad_cat==1) return jet_kt2_leadS_pz; else return float(-99.)")
                .Define("jet_ktN_leadS_phi",    "if (dilep_cat==1) return jet_kt6_leadS_phi; if (semilep_cat==1) return jet_kt4_leadS_phi; if (dihad_cat==1) return jet_kt2_leadS_phi; else return float(-99.)")
                .Define("jet_ktN_leadS_eta",    "if (dilep_cat==1) return jet_kt6_leadS_eta; if (semilep_cat==1) return jet_kt4_leadS_eta; if (dihad_cat==1) return jet_kt2_leadS_eta; else return float(-99.)")
                .Define("jet_ktN_leadS_energy", "if (dilep_cat==1) return jet_kt6_leadS_energy; if (semilep_cat==1) return jet_kt4_leadS_energy; if (dihad_cat==1) return jet_kt2_leadS_energy; else return float(-99.)")
                .Define("jet_ktN_leadS_mass",   "if (dilep_cat==1) return jet_kt6_leadS_mass; if (semilep_cat==1) return jet_kt4_leadS_mass; if (dihad_cat==1) return jet_kt2_leadS_mass; else return float(-99.)")
                .Define("jet_ktN_leadS_dR_b",   "if (dilep_cat==1) return jet_kt6_leadS_dR_b; if (semilep_cat==1) return jet_kt4_leadS_dR_b; if (dihad_cat==1) return jet_kt2_leadS_dR_b; else return float(-99.)")
                .Define("jet_ktN_leadS_dR_s",   "if (dilep_cat==1) return jet_kt6_leadS_dR_s; if (semilep_cat==1) return jet_kt4_leadS_dR_s; if (dihad_cat==1) return jet_kt2_leadS_dR_s; else return float(-99.)")
                .Define("jet_ktN_leadS_isSig",  "if (dilep_cat==1) return jet_kt6_leadS_isSig; if (semilep_cat==1) return jet_kt4_leadS_isSig; if (dihad_cat==1) return jet_kt2_leadS_isSig; else return float(-99.)")
                .Define("jet_ktN_leadS_flavor", "if (dilep_cat==1) return jet_kt6_leadS_flavor; if (semilep_cat==1) return jet_kt4_leadS_flavor; if (dihad_cat==1) return jet_kt2_leadS_flavor; else return float(-99.)")
                .Define("jet_ktN_leadS_isG",    "if (dilep_cat==1) return jet_kt6_leadS_isG; if (semilep_cat==1) return jet_kt4_leadS_isG; if (dihad_cat==1) return jet_kt2_leadS_isG; else return float(-99.)")
                .Define("jet_ktN_leadS_isQ",    "if (dilep_cat==1) return jet_kt6_leadS_isQ; if (semilep_cat==1) return jet_kt4_leadS_isQ; if (dihad_cat==1) return jet_kt2_leadS_isQ; else return float(-99.)")
                .Define("jet_ktN_leadS_isS",    "if (dilep_cat==1) return jet_kt6_leadS_isS; if (semilep_cat==1) return jet_kt4_leadS_isS; if (dihad_cat==1) return jet_kt2_leadS_isS; else return float(-99.)")
                .Define("jet_ktN_leadS_isC",    "if (dilep_cat==1) return jet_kt6_leadS_isC; if (semilep_cat==1) return jet_kt4_leadS_isC; if (dihad_cat==1) return jet_kt2_leadS_isC; else return float(-99.)")
                .Define("jet_ktN_leadS_isB",    "if (dilep_cat==1) return jet_kt6_leadS_isB; if (semilep_cat==1) return jet_kt4_leadS_isB; if (dihad_cat==1) return jet_kt2_leadS_isB; else return float(-99.)")

                .Define("jet_ktN_subS_idx",    "if (dilep_cat==1) return jet_kt6_subS_idx; if (semilep_cat==1) return jet_kt4_subS_idx; if (dihad_cat==1) return jet_kt2_subS_idx; else return int(-1)")
                .Define("jet_ktN_subS_px",     "if (dilep_cat==1) return jet_kt6_subS_px; if (semilep_cat==1) return jet_kt4_subS_px; if (dihad_cat==1) return jet_kt2_subS_px; else return float(-99.)")
                .Define("jet_ktN_subS_py",     "if (dilep_cat==1) return jet_kt6_subS_py; if (semilep_cat==1) return jet_kt4_subS_py; if (dihad_cat==1) return jet_kt2_subS_py; else return float(-99.)")
                .Define("jet_ktN_subS_pz",     "if (dilep_cat==1) return jet_kt6_subS_pz; if (semilep_cat==1) return jet_kt4_subS_pz; if (dihad_cat==1) return jet_kt2_subS_pz; else return float(-99.)")
                .Define("jet_ktN_subS_phi",    "if (dilep_cat==1) return jet_kt6_subS_phi; if (semilep_cat==1) return jet_kt4_subS_phi; if (dihad_cat==1) return jet_kt2_subS_phi; else return float(-99.)")
                .Define("jet_ktN_subS_eta",    "if (dilep_cat==1) return jet_kt6_subS_eta; if (semilep_cat==1) return jet_kt4_subS_eta; if (dihad_cat==1) return jet_kt2_subS_eta; else return float(-99.)")
                .Define("jet_ktN_subS_energy", "if (dilep_cat==1) return jet_kt6_subS_energy; if (semilep_cat==1) return jet_kt4_subS_energy; if (dihad_cat==1) return jet_kt2_subS_energy; else return float(-99.)")
                .Define("jet_ktN_subS_mass",   "if (dilep_cat==1) return jet_kt6_subS_mass; if (semilep_cat==1) return jet_kt4_subS_mass; if (dihad_cat==1) return jet_kt2_subS_mass; else return float(-99.)")
                .Define("jet_ktN_subS_dR_b",   "if (dilep_cat==1) return jet_kt6_subS_dR_b; if (semilep_cat==1) return jet_kt4_subS_dR_b; if (dihad_cat==1) return jet_kt2_subS_dR_b; else return float(-99.)")
                .Define("jet_ktN_subS_dR_s",   "if (dilep_cat==1) return jet_kt6_subS_dR_s; if (semilep_cat==1) return jet_kt4_subS_dR_s; if (dihad_cat==1) return jet_kt2_subS_dR_s; else return float(-99.)")
                .Define("jet_ktN_subS_isSig",  "if (dilep_cat==1) return jet_kt6_subS_isSig; if (semilep_cat==1) return jet_kt4_subS_isSig; if (dihad_cat==1) return jet_kt2_subS_isSig; else return float(-99.)")
                .Define("jet_ktN_subS_flavor", "if (dilep_cat==1) return jet_kt6_subS_flavor; if (semilep_cat==1) return jet_kt4_subS_flavor; if (dihad_cat==1) return jet_kt2_subS_flavor; else return float(-99.)")
                .Define("jet_ktN_subS_isG",    "if (dilep_cat==1) return jet_kt6_subS_isG; if (semilep_cat==1) return jet_kt4_subS_isG; if (dihad_cat==1) return jet_kt2_subS_isG; else return float(-99.)")
                .Define("jet_ktN_subS_isQ",    "if (dilep_cat==1) return jet_kt6_subS_isQ; if (semilep_cat==1) return jet_kt4_subS_isQ; if (dihad_cat==1) return jet_kt2_subS_isQ; else return float(-99.)")
                .Define("jet_ktN_subS_isS",    "if (dilep_cat==1) return jet_kt6_subS_isS; if (semilep_cat==1) return jet_kt4_subS_isS; if (dihad_cat==1) return jet_kt2_subS_isS; else return float(-99.)")
                .Define("jet_ktN_subS_isC",    "if (dilep_cat==1) return jet_kt6_subS_isC; if (semilep_cat==1) return jet_kt4_subS_isC; if (dihad_cat==1) return jet_kt2_subS_isC; else return float(-99.)")
                .Define("jet_ktN_subS_isB",    "if (dilep_cat==1) return jet_kt6_subS_isB; if (semilep_cat==1) return jet_kt4_subS_isB; if (dihad_cat==1) return jet_kt2_subS_isB; else return float(-99.)")

                .Define("jet_ktN_leadC_idx",    "if (dilep_cat==1) return jet_kt6_leadC_idx; if (semilep_cat==1) return jet_kt4_leadC_idx; if (dihad_cat==1) return jet_kt2_leadC_idx; else return int(-1)")
                .Define("jet_ktN_leadC_px",     "if (dilep_cat==1) return jet_kt6_leadC_px; if (semilep_cat==1) return jet_kt4_leadC_px; if (dihad_cat==1) return jet_kt2_leadC_px; else return float(-99.)")
                .Define("jet_ktN_leadC_py",     "if (dilep_cat==1) return jet_kt6_leadC_py; if (semilep_cat==1) return jet_kt4_leadC_py; if (dihad_cat==1) return jet_kt2_leadC_py; else return float(-99.)")
                .Define("jet_ktN_leadC_pz",     "if (dilep_cat==1) return jet_kt6_leadC_pz; if (semilep_cat==1) return jet_kt4_leadC_pz; if (dihad_cat==1) return jet_kt2_leadC_pz; else return float(-99.)")
                .Define("jet_ktN_leadC_phi",    "if (dilep_cat==1) return jet_kt6_leadC_phi; if (semilep_cat==1) return jet_kt4_leadC_phi; if (dihad_cat==1) return jet_kt2_leadC_phi; else return float(-99.)")
                .Define("jet_ktN_leadC_eta",    "if (dilep_cat==1) return jet_kt6_leadC_eta; if (semilep_cat==1) return jet_kt4_leadC_eta; if (dihad_cat==1) return jet_kt2_leadC_eta; else return float(-99.)")
                .Define("jet_ktN_leadC_energy", "if (dilep_cat==1) return jet_kt6_leadC_energy; if (semilep_cat==1) return jet_kt4_leadC_energy; if (dihad_cat==1) return jet_kt2_leadC_energy; else return float(-99.)")
                .Define("jet_ktN_leadC_mass",   "if (dilep_cat==1) return jet_kt6_leadC_mass; if (semilep_cat==1) return jet_kt4_leadC_mass; if (dihad_cat==1) return jet_kt2_leadC_mass; else return float(-99.)")
                .Define("jet_ktN_leadC_dR_b",   "if (dilep_cat==1) return jet_kt6_leadC_dR_b; if (semilep_cat==1) return jet_kt4_leadC_dR_b; if (dihad_cat==1) return jet_kt2_leadC_dR_b; else return float(-99.)")
                .Define("jet_ktN_leadC_dR_s",   "if (dilep_cat==1) return jet_kt6_leadC_dR_s; if (semilep_cat==1) return jet_kt4_leadC_dR_s; if (dihad_cat==1) return jet_kt2_leadC_dR_s; else return float(-99.)")
                .Define("jet_ktN_leadC_isSig",  "if (dilep_cat==1) return jet_kt6_leadC_isSig; if (semilep_cat==1) return jet_kt4_leadC_isSig; if (dihad_cat==1) return jet_kt2_leadC_isSig; else return float(-99.)")
                .Define("jet_ktN_leadC_flavor", "if (dilep_cat==1) return jet_kt6_leadC_flavor; if (semilep_cat==1) return jet_kt4_leadC_flavor; if (dihad_cat==1) return jet_kt2_leadC_flavor; else return float(-99.)")
                .Define("jet_ktN_leadC_isG",    "if (dilep_cat==1) return jet_kt6_leadC_isG; if (semilep_cat==1) return jet_kt4_leadC_isG; if (dihad_cat==1) return jet_kt2_leadC_isG; else return float(-99.)")
                .Define("jet_ktN_leadC_isQ",    "if (dilep_cat==1) return jet_kt6_leadC_isQ; if (semilep_cat==1) return jet_kt4_leadC_isQ; if (dihad_cat==1) return jet_kt2_leadC_isQ; else return float(-99.)")
                .Define("jet_ktN_leadC_isS",    "if (dilep_cat==1) return jet_kt6_leadC_isS; if (semilep_cat==1) return jet_kt4_leadC_isS; if (dihad_cat==1) return jet_kt2_leadC_isS; else return float(-99.)")
                .Define("jet_ktN_leadC_isC",    "if (dilep_cat==1) return jet_kt6_leadC_isC; if (semilep_cat==1) return jet_kt4_leadC_isC; if (dihad_cat==1) return jet_kt2_leadC_isC; else return float(-99.)")
                .Define("jet_ktN_leadC_isB",    "if (dilep_cat==1) return jet_kt6_leadC_isB; if (semilep_cat==1) return jet_kt4_leadC_isB; if (dihad_cat==1) return jet_kt2_leadC_isB; else return float(-99.)")

                .Define("jet_ktN_subC_idx",    "if (dilep_cat==1) return jet_kt6_subC_idx; if (semilep_cat==1) return jet_kt4_subC_idx; if (dihad_cat==1) return jet_kt2_subC_idx; else return int(-1)")
                .Define("jet_ktN_subC_px",     "if (dilep_cat==1) return jet_kt6_subC_px; if (semilep_cat==1) return jet_kt4_subC_px; if (dihad_cat==1) return jet_kt2_subC_px; else return float(-99.)")
                .Define("jet_ktN_subC_py",     "if (dilep_cat==1) return jet_kt6_subC_py; if (semilep_cat==1) return jet_kt4_subC_py; if (dihad_cat==1) return jet_kt2_subC_py; else return float(-99.)")
                .Define("jet_ktN_subC_pz",     "if (dilep_cat==1) return jet_kt6_subC_pz; if (semilep_cat==1) return jet_kt4_subC_pz; if (dihad_cat==1) return jet_kt2_subC_pz; else return float(-99.)")
                .Define("jet_ktN_subC_phi",    "if (dilep_cat==1) return jet_kt6_subC_phi; if (semilep_cat==1) return jet_kt4_subC_phi; if (dihad_cat==1) return jet_kt2_subC_phi; else return float(-99.)")
                .Define("jet_ktN_subC_eta",    "if (dilep_cat==1) return jet_kt6_subC_eta; if (semilep_cat==1) return jet_kt4_subC_eta; if (dihad_cat==1) return jet_kt2_subC_eta; else return float(-99.)")
                .Define("jet_ktN_subC_energy", "if (dilep_cat==1) return jet_kt6_subC_energy; if (semilep_cat==1) return jet_kt4_subC_energy; if (dihad_cat==1) return jet_kt2_subC_energy; else return float(-99.)")
                .Define("jet_ktN_subC_mass",   "if (dilep_cat==1) return jet_kt6_subC_mass; if (semilep_cat==1) return jet_kt4_subC_mass; if (dihad_cat==1) return jet_kt2_subC_mass; else return float(-99.)")
                .Define("jet_ktN_subC_dR_b",   "if (dilep_cat==1) return jet_kt6_subC_dR_b; if (semilep_cat==1) return jet_kt4_subC_dR_b; if (dihad_cat==1) return jet_kt2_subC_dR_b; else return float(-99.)")
                .Define("jet_ktN_subC_dR_s",   "if (dilep_cat==1) return jet_kt6_subC_dR_s; if (semilep_cat==1) return jet_kt4_subC_dR_s; if (dihad_cat==1) return jet_kt2_subC_dR_s; else return float(-99.)")
                .Define("jet_ktN_subC_isSig",  "if (dilep_cat==1) return jet_kt6_subC_isSig; if (semilep_cat==1) return jet_kt4_subC_isSig; if (dihad_cat==1) return jet_kt2_subC_isSig; else return float(-99.)")
                .Define("jet_ktN_subC_flavor", "if (dilep_cat==1) return jet_kt6_subC_flavor; if (semilep_cat==1) return jet_kt4_subC_flavor; if (dihad_cat==1) return jet_kt2_subC_flavor; else return float(-99.)")
                .Define("jet_ktN_subC_isG",    "if (dilep_cat==1) return jet_kt6_subC_isG; if (semilep_cat==1) return jet_kt4_subC_isG; if (dihad_cat==1) return jet_kt2_subC_isG; else return float(-99.)")
                .Define("jet_ktN_subC_isQ",    "if (dilep_cat==1) return jet_kt6_subC_isQ; if (semilep_cat==1) return jet_kt4_subC_isQ; if (dihad_cat==1) return jet_kt2_subC_isQ; else return float(-99.)")
                .Define("jet_ktN_subC_isS",    "if (dilep_cat==1) return jet_kt6_subC_isS; if (semilep_cat==1) return jet_kt4_subC_isS; if (dihad_cat==1) return jet_kt2_subC_isS; else return float(-99.)")
                .Define("jet_ktN_subC_isC",    "if (dilep_cat==1) return jet_kt6_subC_isC; if (semilep_cat==1) return jet_kt4_subC_isC; if (dihad_cat==1) return jet_kt2_subC_isC; else return float(-99.)")
                .Define("jet_ktN_subC_isB",    "if (dilep_cat==1) return jet_kt6_subC_isB; if (semilep_cat==1) return jet_kt4_subC_isB; if (dihad_cat==1) return jet_kt2_subC_isB; else return float(-99.)")

                .Define("jet_ktN_leadB_idx",    "if (dilep_cat==1) return jet_kt6_leadB_idx; if (semilep_cat==1) return jet_kt4_leadB_idx; if (dihad_cat==1) return jet_kt2_leadB_idx; else return int(-1)")
                .Define("jet_ktN_leadB_px",     "if (dilep_cat==1) return jet_kt6_leadB_px; if (semilep_cat==1) return jet_kt4_leadB_px; if (dihad_cat==1) return jet_kt2_leadB_px; else return float(-99.)")
                .Define("jet_ktN_leadB_py",     "if (dilep_cat==1) return jet_kt6_leadB_py; if (semilep_cat==1) return jet_kt4_leadB_py; if (dihad_cat==1) return jet_kt2_leadB_py; else return float(-99.)")
                .Define("jet_ktN_leadB_pz",     "if (dilep_cat==1) return jet_kt6_leadB_pz; if (semilep_cat==1) return jet_kt4_leadB_pz; if (dihad_cat==1) return jet_kt2_leadB_pz; else return float(-99.)")
                .Define("jet_ktN_leadB_phi",    "if (dilep_cat==1) return jet_kt6_leadB_phi; if (semilep_cat==1) return jet_kt4_leadB_phi; if (dihad_cat==1) return jet_kt2_leadB_phi; else return float(-99.)")
                .Define("jet_ktN_leadB_eta",    "if (dilep_cat==1) return jet_kt6_leadB_eta; if (semilep_cat==1) return jet_kt4_leadB_eta; if (dihad_cat==1) return jet_kt2_leadB_eta; else return float(-99.)")
                .Define("jet_ktN_leadB_energy", "if (dilep_cat==1) return jet_kt6_leadB_energy; if (semilep_cat==1) return jet_kt4_leadB_energy; if (dihad_cat==1) return jet_kt2_leadB_energy; else return float(-99.)")
                .Define("jet_ktN_leadB_mass",   "if (dilep_cat==1) return jet_kt6_leadB_mass; if (semilep_cat==1) return jet_kt4_leadB_mass; if (dihad_cat==1) return jet_kt2_leadB_mass; else return float(-99.)")
                .Define("jet_ktN_leadB_dR_b",   "if (dilep_cat==1) return jet_kt6_leadB_dR_b; if (semilep_cat==1) return jet_kt4_leadB_dR_b; if (dihad_cat==1) return jet_kt2_leadB_dR_b; else return float(-99.)")
                .Define("jet_ktN_leadB_dR_s",   "if (dilep_cat==1) return jet_kt6_leadB_dR_s; if (semilep_cat==1) return jet_kt4_leadB_dR_s; if (dihad_cat==1) return jet_kt2_leadB_dR_s; else return float(-99.)")
                .Define("jet_ktN_leadB_isSig",  "if (dilep_cat==1) return jet_kt6_leadB_isSig; if (semilep_cat==1) return jet_kt4_leadB_isSig; if (dihad_cat==1) return jet_kt2_leadB_isSig; else return float(-99.)")
                .Define("jet_ktN_leadB_flavor", "if (dilep_cat==1) return jet_kt6_leadB_flavor; if (semilep_cat==1) return jet_kt4_leadB_flavor; if (dihad_cat==1) return jet_kt2_leadB_flavor; else return float(-99.)")
                .Define("jet_ktN_leadB_isG",    "if (dilep_cat==1) return jet_kt6_leadB_isG; if (semilep_cat==1) return jet_kt4_leadB_isG; if (dihad_cat==1) return jet_kt2_leadB_isG; else return float(-99.)")
                .Define("jet_ktN_leadB_isQ",    "if (dilep_cat==1) return jet_kt6_leadB_isQ; if (semilep_cat==1) return jet_kt4_leadB_isQ; if (dihad_cat==1) return jet_kt2_leadB_isQ; else return float(-99.)")
                .Define("jet_ktN_leadB_isS",    "if (dilep_cat==1) return jet_kt6_leadB_isS; if (semilep_cat==1) return jet_kt4_leadB_isS; if (dihad_cat==1) return jet_kt2_leadB_isS; else return float(-99.)")
                .Define("jet_ktN_leadB_isC",    "if (dilep_cat==1) return jet_kt6_leadB_isC; if (semilep_cat==1) return jet_kt4_leadB_isC; if (dihad_cat==1) return jet_kt2_leadB_isC; else return float(-99.)")
                .Define("jet_ktN_leadB_isB",    "if (dilep_cat==1) return jet_kt6_leadB_isB; if (semilep_cat==1) return jet_kt4_leadB_isB; if (dihad_cat==1) return jet_kt2_leadB_isB; else return float(-99.)")

                .Define("jet_ktN_subB_idx",    "if (dilep_cat==1) return jet_kt6_subB_idx; if (semilep_cat==1) return jet_kt4_subB_idx; if (dihad_cat==1) return jet_kt2_subB_idx; else return int(-1)")
                .Define("jet_ktN_subB_px",     "if (dilep_cat==1) return jet_kt6_subB_px; if (semilep_cat==1) return jet_kt4_subB_px; if (dihad_cat==1) return jet_kt2_subB_px; else return float(-99.)")
                .Define("jet_ktN_subB_py",     "if (dilep_cat==1) return jet_kt6_subB_py; if (semilep_cat==1) return jet_kt4_subB_py; if (dihad_cat==1) return jet_kt2_subB_py; else return float(-99.)")
                .Define("jet_ktN_subB_pz",     "if (dilep_cat==1) return jet_kt6_subB_pz; if (semilep_cat==1) return jet_kt4_subB_pz; if (dihad_cat==1) return jet_kt2_subB_pz; else return float(-99.)")
                .Define("jet_ktN_subB_phi",    "if (dilep_cat==1) return jet_kt6_subB_phi; if (semilep_cat==1) return jet_kt4_subB_phi; if (dihad_cat==1) return jet_kt2_subB_phi; else return float(-99.)")
                .Define("jet_ktN_subB_eta",    "if (dilep_cat==1) return jet_kt6_subB_eta; if (semilep_cat==1) return jet_kt4_subB_eta; if (dihad_cat==1) return jet_kt2_subB_eta; else return float(-99.)")
                .Define("jet_ktN_subB_energy", "if (dilep_cat==1) return jet_kt6_subB_energy; if (semilep_cat==1) return jet_kt4_subB_energy; if (dihad_cat==1) return jet_kt2_subB_energy; else return float(-99.)")
                .Define("jet_ktN_subB_mass",   "if (dilep_cat==1) return jet_kt6_subB_mass; if (semilep_cat==1) return jet_kt4_subB_mass; if (dihad_cat==1) return jet_kt2_subB_mass; else return float(-99.)")
                .Define("jet_ktN_subB_dR_b",   "if (dilep_cat==1) return jet_kt6_subB_dR_b; if (semilep_cat==1) return jet_kt4_subB_dR_b; if (dihad_cat==1) return jet_kt2_subB_dR_b; else return float(-99.)")
                .Define("jet_ktN_subB_dR_s",   "if (dilep_cat==1) return jet_kt6_subB_dR_s; if (semilep_cat==1) return jet_kt4_subB_dR_s; if (dihad_cat==1) return jet_kt2_subB_dR_s; else return float(-99.)")
                .Define("jet_ktN_subB_isSig",  "if (dilep_cat==1) return jet_kt6_subB_isSig; if (semilep_cat==1) return jet_kt4_subB_isSig; if (dihad_cat==1) return jet_kt2_subB_isSig; else return float(-99.)")
                .Define("jet_ktN_subB_flavor", "if (dilep_cat==1) return jet_kt6_subB_flavor; if (semilep_cat==1) return jet_kt4_subB_flavor; if (dihad_cat==1) return jet_kt2_subB_flavor; else return float(-99.)")
                .Define("jet_ktN_subB_isG",    "if (dilep_cat==1) return jet_kt6_subB_isG; if (semilep_cat==1) return jet_kt4_subB_isG; if (dihad_cat==1) return jet_kt2_subB_isG; else return float(-99.)")
                .Define("jet_ktN_subB_isQ",    "if (dilep_cat==1) return jet_kt6_subB_isQ; if (semilep_cat==1) return jet_kt4_subB_isQ; if (dihad_cat==1) return jet_kt2_subB_isQ; else return float(-99.)")
                .Define("jet_ktN_subB_isS",    "if (dilep_cat==1) return jet_kt6_subB_isS; if (semilep_cat==1) return jet_kt4_subB_isS; if (dihad_cat==1) return jet_kt2_subB_isS; else return float(-99.)")
                .Define("jet_ktN_subB_isC",    "if (dilep_cat==1) return jet_kt6_subB_isC; if (semilep_cat==1) return jet_kt4_subB_isC; if (dihad_cat==1) return jet_kt2_subB_isC; else return float(-99.)")
                .Define("jet_ktN_subB_isB",    "if (dilep_cat==1) return jet_kt6_subB_isB; if (semilep_cat==1) return jet_kt4_subB_isB; if (dihad_cat==1) return jet_kt2_subB_isB; else return float(-99.)")

                ## cs dijets and trijets

                .Define("dijet_cs_ktN_idx",     "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_ktN_isC, jet_ktN_isS, {jet_ktN_leadS_idx, jet_ktN_leadB_idx}, false)")
                .Define("dijet_cs_ktN_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_cs_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_cs_ktN_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_cs_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_cs_ktN_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_cs_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_cs_ktN_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_cs_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_cs_ktN_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_cs_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_dijet_cs_ktN",   "int(dijet_cs_ktN_mass.size())")

                .Define("trijet_Scs_ktN_idx",     "FCCAnalyses::ZHfunctions::get_trijet_idx(dijet_cs_ktN_idx, jet_ktN_leadS_idx, true)")
                .Define("trijet_Scs_ktN_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Scs_ktN_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Scs_ktN_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Scs_ktN_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Scs_ktN_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_trijet_Scs_ktN",   "int(trijet_Scs_ktN_mass.size())")

                .Define("trijet_Bcs_ktN_idx",     "FCCAnalyses::ZHfunctions::get_trijet_idx(dijet_cs_ktN_idx, jet_ktN_leadB_idx, false)")
                .Define("trijet_Bcs_ktN_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Bcs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bcs_ktN_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(trijet_Bcs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bcs_ktN_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Bcs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bcs_ktN_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(trijet_Bcs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bcs_ktN_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(trijet_Bcs_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_trijet_Bcs_ktN",   "int(trijet_Bcs_ktN_mass.size())")

                ## ud dijets and trijets

                .Define("dijet_ud_ktN_idx",     "FCCAnalyses::ZHfunctions::sel_dijet_score(jet_ktN_isQ, jet_ktN_isQ, {jet_ktN_leadS_idx, jet_ktN_leadB_idx}, true)")
                .Define("dijet_ud_ktN_px",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ud_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_ud_ktN_py",     "FCCAnalyses::ZHfunctions::get_dijet_py(dijet_ud_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_ud_ktN_pz",     "FCCAnalyses::ZHfunctions::get_dijet_px(dijet_ud_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_ud_ktN_energy", "FCCAnalyses::ZHfunctions::get_dijet_energy(dijet_ud_ktN_idx, jet_ktN_cat_p4)")
                .Define("dijet_ud_ktN_mass",   "FCCAnalyses::ZHfunctions::get_dijet_mass(dijet_ud_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_dijet_ud_ktN",   "int(dijet_ud_ktN_mass.size())")

                .Define("trijet_Sud_ktN_idx",     "FCCAnalyses::ZHfunctions::get_trijet_idx(dijet_ud_ktN_idx, jet_leadS_idx, true)")
                .Define("trijet_Sud_ktN_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Sud_ktN_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Sud_ktN_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Sud_ktN_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Sud_ktN_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(trijet_Scs_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_trijet_Sud_ktN",   "int(trijet_Sud_ktN_mass.size())")

                .Define("trijet_Bud_ktN_idx",     "FCCAnalyses::ZHfunctions::get_trijet_idx(dijet_ud_ktN_idx, jet_leadB_idx, false)")
                .Define("trijet_Bud_ktN_px",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Bud_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bud_ktN_py",     "FCCAnalyses::ZHfunctions::get_trijet_py(trijet_Bud_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bud_ktN_pz",     "FCCAnalyses::ZHfunctions::get_trijet_px(trijet_Bud_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bud_ktN_energy", "FCCAnalyses::ZHfunctions::get_trijet_energy(trijet_Bud_ktN_idx, jet_ktN_cat_p4)")
                .Define("trijet_Bud_ktN_mass",   "FCCAnalyses::ZHfunctions::get_trijet_mass(trijet_Bud_ktN_idx, jet_ktN_cat_p4)")
                .Define("n_trijet_Bud_ktN",   "int(trijet_Bud_ktN_mass.size())") 

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
                        "jet_ktN_isG", "jet_ktN_isQ", "jet_ktN_isS", "jet_ktN_isC", "jet_ktN_isB", "jet_ktN_dR_b", "jet_ktN_dR_s", "jet_ktN_isSig",
                        "dijet_ktN_px", "dijet_ktN_py", "dijet_ktN_pz", "dijet_ktN_energy", "dijet_ktN_mass"]
        branchList += ["jet_ktN_leadS_idx", "jet_ktN_leadS_px",   "jet_ktN_leadS_py",     "jet_ktN_leadS_pz",   "jet_ktN_leadS_phi",  "jet_ktN_leadS_eta", "jet_ktN_leadS_energy",
                       "jet_ktN_leadS_mass", "jet_ktN_leadS_flavor", "jet_ktN_leadS_dR_b", "jet_ktN_leadS_dR_s", "jet_ktN_leadS_isSig",
                       "jet_ktN_leadS_isG",  "jet_ktN_leadS_isQ",    "jet_ktN_leadS_isS",  "jet_ktN_leadS_isC",  "jet_ktN_leadS_isB"]
        branchList += ["jet_ktN_subS_idx", "jet_ktN_subS_px",    "jet_ktN_subS_py",      "jet_ktN_subS_pz",    "jet_ktN_subS_phi",   "jet_ktN_subS_eta", "jet_ktN_subS_energy",
                       "jet_ktN_subS_mass",  "jet_ktN_subS_flavor",  "jet_ktN_subS_dR_b",  "jet_ktN_subS_dR_s",  "jet_ktN_subS_isSig",
                       "jet_ktN_subS_isG",   "jet_ktN_subS_isQ",     "jet_ktN_subS_isS",   "jet_ktN_subS_isC",   "jet_kt2_subS_isB"]
        branchList += ["jet_ktN_leadC_idx", "jet_ktN_leadC_px",   "jet_ktN_leadC_py",     "jet_ktN_leadC_pz",   "jet_ktN_leadC_phi",  "jet_ktN_leadC_eta", "jet_ktN_leadC_energy",
                       "jet_ktN_leadC_mass", "jet_ktN_leadC_flavor", "jet_ktN_leadC_dR_b", "jet_ktN_leadC_dR_s", "jet_ktN_leadC_isSig",
                       "jet_ktN_leadC_isG",  "jet_ktN_leadC_isQ",    "jet_ktN_leadC_isS",  "jet_ktN_leadC_isC",  "jet_ktN_leadC_isB"]
        branchList += ["jet_ktN_subC_idx", "jet_ktN_subC_px",    "jet_ktN_subC_py",      "jet_ktN_subC_pz",    "jet_ktN_subC_phi",   "jet_ktN_subC_eta", "jet_ktN_subC_energy",
                       "jet_ktN_subC_mass",  "jet_ktN_subC_flavor",  "jet_ktN_subC_dR_b",  "jet_ktN_subC_dR_s",  "jet_ktN_subC_isSig",
                       "jet_ktN_subC_isG",   "jet_ktN_subC_isQ",     "jet_ktN_subC_isS",   "jet_ktN_subC_isC",   "jet_kt2_subC_isB"]
        branchList += ["jet_ktN_leadB_idx", "jet_ktN_leadB_px",   "jet_ktN_leadB_py",     "jet_ktN_leadB_pz",   "jet_ktN_leadB_phi",  "jet_ktN_leadB_eta", "jet_ktN_leadB_energy",
                       "jet_ktN_leadB_mass", "jet_ktN_leadB_flavor", "jet_ktN_leadB_dR_b", "jet_ktN_leadB_dR_s", "jet_ktN_leadB_isSig",
                       "jet_ktN_leadB_isG",  "jet_ktN_leadB_isQ",    "jet_ktN_leadB_isS",  "jet_ktN_leadB_isC",  "jet_ktN_leadB_isB"]
        branchList += ["jet_ktN_subB_idx", "jet_ktN_subB_px",    "jet_ktN_subB_py",      "jet_ktN_subB_pz",    "jet_ktN_subB_phi",   "jet_ktN_subB_eta", "jet_ktN_subB_energy",
                       "jet_ktN_subB_mass",  "jet_ktN_subB_flavor",  "jet_ktN_subB_dR_b",  "jet_ktN_subB_dR_s",  "jet_ktN_subB_isSig",
                       "jet_ktN_subB_isG",   "jet_ktN_subB_isQ",     "jet_ktN_subB_isS",   "jet_ktN_subB_isC",   "jet_kt2_subB_isB"]
        branchList += ["dijet_cs_ktN_idx", "dijet_cs_ktN_px", "dijet_cs_ktN_py", "dijet_cs_ktN_pz", "dijet_cs_ktN_energy", "dijet_cs_ktN_mass", "n_cs_dijet_ktN",
                        "trijet_Scs_ktN_idx", "trijet_Scs_ktN_px", "trijet_Scs_ktN_py", "trijet_Scs_ktN_pz", "trijet_Scs_ktN_energy", "trijet_Scs_ktN_mass", "n_Scs_trijet_ktN",
                        "trijet_Bcs_ktN_idx", "trijet_Bcs_ktN_px", "trijet_Bcs_ktN_py", "trijet_Bcs_ktN_pz", "trijet_Bcs_ktN_energy", "trijet_Bcs_ktN_mass", "n_Bcs_trijet_ktN"]
        branchList += ["dijet_ud_ktN_idx", "dijet_ud_ktN_px", "dijet_ud_ktN_py", "dijet_ud_ktN_pz", "dijet_ud_ktN_energy", "dijet_ud_ktN_mass", "n_ud_dijet_ktN",
                        "trijet_Sud_ktN_idx", "trijet_Sud_ktN_px", "trijet_Sud_ktN_py", "trijet_Sud_ktN_pz", "trijet_Sud_ktN_energy", "trijet_Sud_ktN_mass", "n_Sud_trijet_ktN",
                        "trijet_Bud_ktN_idx", "trijet_Bud_ktN_px", "trijet_Bud_ktN_py", "trijet_Bud_ktN_pz", "trijet_Bud_ktN_energy", "trijet_Bud_ktN_mass", "n_Bud_trijet_ktN"]
        

        return branchList