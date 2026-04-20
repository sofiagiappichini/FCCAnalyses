import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {

    'p8_ee_WW_ecm240':{'chunks':300},
    'p8_ee_Zqq_ecm240':{'chunks':100},
    'p8_ee_ZZ_ecm240':{'chunks':50},
    
    'wzp6_ee_tautau_ecm240':{'chunks':50},
    'wzp6_ee_mumu_ecm240':{'chunks':50},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':80},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':1},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':6},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':6},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':6},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':6},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':30},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':30},
    'wzp6_gaga_ee_60_ecm240': {'chunks':20},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':2},
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':1},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':1},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':1},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':1},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':1},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"

outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ktN-tag/stage2_241202/LL/LH"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = True

nCPUS = 6

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "microcentury"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

            ### to find already made functions, this is where they are or where they can be added instead of writing them here
            ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

            ### defining filters for 3 lepton final state based on flavor combination: 3 same flavor, 1 pair, all plus one hadronic taus

                .Define("TauTag_px",      "TagJet_kt1_px[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_py",      "TagJet_kt1_py[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_pz",      "TagJet_kt1_pz[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_pt",      "TagJet_kt1_pt[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_p",      "TagJet_kt1_p[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_e",      "TagJet_kt1_e[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_phi",      "TagJet_kt1_phi[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_eta",      "TagJet_kt1_eta[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_theta",      "TagJet_kt1_theta[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_charge",      "TagJet_kt1_charge[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_mass",      "TagJet_kt1_mass[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isG",      "TagJet_kt1_isG[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isU",      "TagJet_kt1_isU[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isD",      "TagJet_kt1_isD[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isS",      "TagJet_kt1_isS[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isC",      "TagJet_kt1_isC[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isB",      "TagJet_kt1_isB[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_isTAU",      "TagJet_kt1_isTAU[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("TauTag_flavor",      "TagJet_kt1_flavor[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_TauTag_constituents",        "n_TagJet_kt1_constituents[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_TauTag_charged_constituents",        "n_TagJet_kt1_charged_constituents[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_TauTag_neutral_constituents",        "n_TagJet_kt1_neutral_constituents[TagJet_kt1_isTAU>0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_TauTag",          "TauTag_px.size()")

                .Define("QuarkTag_px",      "TagJet_kt1_px[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_py",      "TagJet_kt1_py[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_pz",      "TagJet_kt1_pz[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_pt",      "TagJet_kt1_pt[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_p",      "TagJet_kt1_p[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_e",      "TagJet_kt1_e[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_phi",      "TagJet_kt1_phi[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_eta",      "TagJet_kt1_eta[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_theta",      "TagJet_kt1_theta[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_charge",      "TagJet_kt1_charge[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_mass",      "TagJet_kt1_mass[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isG",      "TagJet_kt1_isG[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isU",      "TagJet_kt1_isU[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isD",      "TagJet_kt1_isD[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isS",      "TagJet_kt1_isS[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isC",      "TagJet_kt1_isC[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isB",      "TagJet_kt1_isB[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_isTAU",      "TagJet_kt1_isTAU[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("QuarkTag_flavor",      "TagJet_kt1_flavor[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_QuarkTag_constituents",        "n_TagJet_kt1_constituents[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_QuarkTag_charged_constituents",        "n_TagJet_kt1_charged_constituents[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_kt1_neutral_constituents[TagJet_kt1_isTAU<=0.5 && TagJet_kt1_cleanup==1]")
                .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ####################################

                .Define("ThreeLeptons",    "(((n_RecoElectrons_sel==3 and n_RecoMuons_sel==0) or (n_RecoElectrons_sel==0 and n_RecoMuons_sel==3)) and abs(RecoLepton_sel_charge.at(0) + RecoLepton_sel_charge.at(1) + RecoLepton_sel_charge.at(2))==1)*1.0")
                .Define("OnePair",     "((n_RecoElectrons_sel==2 and n_RecoMuons_sel==1 and (RecoElectron_sel_charge.at(0) + RecoElectron_sel_charge.at(1))==0) or (n_RecoElectrons_sel==1 and n_RecoMuons_sel==2 and (RecoMuon_sel_charge.at(0) + RecoMuon_sel_charge.at(1))==0))*1.0")

                .Filter("n_TauTag==1 && n_QuarkTag==0")
                .Filter("(ThreeLeptons==1 || OnePair==1)") 

                ####################################

                ##################
                # Reco particles #
                ##################

                .Define("RecoEmiss_p4",  "FCCAnalyses::ZHfunctions::build_p4_single(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
                .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
                .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
                .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
                .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
                .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_sel_px, RecoLepton_sel_py, RecoLepton_sel_pz, RecoLepton_sel_e)")

                .Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_3(RecoLepton_p4, RecoLepton_sel_charge, RecoLepton_sel_mass, 91.188)")

                .Filter("RecoZH_idx[0]>=0 && RecoZH_idx[1]>=0 && RecoZH_idx[2]>=0")

                .Define("RecoZ1_p4",      "RecoLepton_p4.at(RecoZH_idx[0])")
                .Define("RecoZ2_p4",        "RecoLepton_p4.at(RecoZH_idx[1])")
                
                .Define("RecoZLead_p4",      "if (RecoZ1_p4.Pt()>RecoZ2_p4.Pt()) return RecoZ1_p4; else return RecoZ2_p4;")
                .Define("RecoZLead_px",    "RecoZLead_p4.Px()")
                .Define("RecoZLead_py",    "RecoZLead_p4.Py()")
                .Define("RecoZLead_pz",    "RecoZLead_p4.Pz()")
                .Define("RecoZLead_p",    "RecoZLead_p4.P()")
                .Define("RecoZLead_pt",    "RecoZLead_p4.Pt()")
                .Define("RecoZLead_e",     "RecoZLead_p4.E()")
                .Define("RecoZLead_eta",    "RecoZLead_p4.Eta()")
                .Define("RecoZLead_phi",    "RecoZLead_p4.Phi()")
                .Define("RecoZLead_theta",    "RecoZLead_p4.Theta()")
                .Define("RecoZLead_y",     "RecoZLead_p4.Rapidity()")
                .Define("RecoZLead_mass",    "RecoZLead_p4.M()")

                .Define("RecoZSub_p4",      "if (RecoZ1_p4.Pt()>RecoZ2_p4.Pt()) return RecoZ2_p4; else return RecoZ1_p4;")
                .Define("RecoZSub_px",    "RecoZSub_p4.Px()")
                .Define("RecoZSub_py",    "RecoZSub_p4.Py()")
                .Define("RecoZSub_pz",    "RecoZSub_p4.Pz()")
                .Define("RecoZSub_p",    "RecoZSub_p4.P()")
                .Define("RecoZSub_pt",    "RecoZSub_p4.Pt()")
                .Define("RecoZSub_e",     "RecoZSub_p4.E()")
                .Define("RecoZSub_eta",    "RecoZSub_p4.Eta()")
                .Define("RecoZSub_phi",    "RecoZSub_p4.Phi()")
                .Define("RecoZSub_theta",    "RecoZSub_p4.Theta()")
                .Define("RecoZSub_y",     "RecoZSub_p4.Rapidity()")
                .Define("RecoZSub_mass",    "RecoZSub_p4.M()")

                .Define("RecoZP_p4",      "if (RecoLepton_sel_charge.at(RecoZH_idx[0])==1) return RecoZ1_p4; else return RecoZ2_p4;")
                .Define("RecoZP_px",    "RecoZP_p4.Px()")
                .Define("RecoZP_py",    "RecoZP_p4.Py()")
                .Define("RecoZP_pz",    "RecoZP_p4.Pz()")
                .Define("RecoZP_p",    "RecoZP_p4.P()")
                .Define("RecoZP_pt",    "RecoZP_p4.Pt()")
                .Define("RecoZP_e",     "RecoZP_p4.E()")
                .Define("RecoZP_eta",    "RecoZP_p4.Eta()")
                .Define("RecoZP_phi",    "RecoZP_p4.Phi()")
                .Define("RecoZP_theta",    "RecoZP_p4.Theta()")
                .Define("RecoZP_y",     "RecoZP_p4.Rapidity()")
                .Define("RecoZP_mass",    "RecoZP_p4.M()")

                .Define("RecoZM_p4",      "if (RecoLepton_sel_charge.at(RecoZH_idx[0])==1) return RecoZ2_p4; else return RecoZ1_p4;")
                .Define("RecoZM_px",    "RecoZM_p4.Px()")
                .Define("RecoZM_py",    "RecoZM_p4.Py()")
                .Define("RecoZM_pz",    "RecoZM_p4.Pz()")
                .Define("RecoZM_p",    "RecoZM_p4.P()")
                .Define("RecoZM_pt",    "RecoZM_p4.Pt()")
                .Define("RecoZM_e",     "RecoZM_p4.E()")
                .Define("RecoZM_eta",    "RecoZM_p4.Eta()")
                .Define("RecoZM_phi",    "RecoZM_p4.Phi()")
                .Define("RecoZM_theta",    "RecoZM_p4.Theta()")
                .Define("RecoZM_y",     "RecoZM_p4.Rapidity()")
                .Define("RecoZM_mass",    "RecoZM_p4.M()")

                .Define("RecoZ_p4",          "RecoZ1_p4+RecoZ2_p4")
                .Define("RecoZ_px",    "RecoZ_p4.Px()")
                .Define("RecoZ_py",    "RecoZ_p4.Py()")
                .Define("RecoZ_pz",    "RecoZ_p4.Pz()")
                .Define("RecoZ_p",    "RecoZ_p4.P()")
                .Define("RecoZ_pt",    "RecoZ_p4.Pt()")
                .Define("RecoZ_e",     "RecoZ_p4.E()")
                .Define("RecoZ_eta",    "RecoZ_p4.Eta()")
                .Define("RecoZ_phi",    "RecoZ_p4.Phi()")
                .Define("RecoZ_theta",    "RecoZ_p4.Theta()")
                .Define("RecoZ_y",     "RecoZ_p4.Rapidity()")
                .Define("RecoZ_mass",    "RecoZ_p4.M()")

                .Define("RecoTau1_p4",      "RecoLepton_p4.at(RecoZH_idx[2])")
                .Define("RecoTau2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(TauTag_px.at(0), TauTag_py.at(0), TauTag_pz.at(0), TauTag_e.at(0))")
                .Define("RecoTau1_type",        "if (RecoLepton_sel_mass.at(RecoZH_idx[2])<0.05) return float(-0.11); else return float(-0.13);")
                .Define("RecoTau2_type",        "TauTag_isTAU.at(0)")
                .Define("n_RecoTau1_constituents",        "return float(1);")
                .Define("n_RecoTau2_constituents",        "n_TauTag_constituents.at(0)")
                .Define("n_RecoTau1_charged_constituents",        "return float(1);")
                .Define("n_RecoTau2_charged_constituents",        "n_TauTag_charged_constituents.at(0)")
                .Define("n_RecoTau1_neutral_constituents",        "return float(0);")
                .Define("n_RecoTau2_neutral_constituents",        "n_TauTag_neutral_constituents.at(0)")

                .Define("TauLepton_type",        "if (RecoLepton_sel_mass.at(0)<0.05) return float(-0.11); else return float(-0.13);")
                .Define("TauHadron_type",        "TauTag_isTAU.at(0)")
                .Define("n_TauLepton_constituents",        "return float(1);")
                .Define("n_TauHadron_constituents",        "n_TauTag_constituents.at(0)")
                .Define("n_TauLepton_charged_constituents",        "return float(1);")
                .Define("n_TauHadron_charged_constituents",        "n_TauTag_charged_constituents.at(0)")
                .Define("n_TauLepton_neutral_constituents",        "return float(0);")
                .Define("n_TauHadron_neutral_constituents",        "n_TauTag_neutral_constituents.at(0)")

                .Define("RecoH_p4",         "RecoTau1_p4+RecoTau2_p4")
                .Define("RecoH_px",    "RecoH_p4.Px()")
                .Define("RecoH_py",    "RecoH_p4.Py()")
                .Define("RecoH_pz",    "RecoH_p4.Pz()")
                .Define("RecoH_p",    "RecoH_p4.P()")
                .Define("RecoH_pt",    "RecoH_p4.Pt()")
                .Define("RecoH_e",     "RecoH_p4.E()")
                .Define("RecoH_eta",    "RecoH_p4.Eta()")
                .Define("RecoH_phi",    "RecoH_p4.Phi()")
                .Define("RecoH_theta",    "RecoH_p4.Theta()")
                .Define("RecoH_y",     "RecoH_p4.Rapidity()")
                .Define("RecoH_mass",    "RecoH_p4.M()")

                .Define("TauLead_p4",       "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau1_p4; else return RecoTau2_p4;")
                .Define("TauLead_px",    "TauLead_p4.Px()")
                .Define("TauLead_py",    "TauLead_p4.Py()")
                .Define("TauLead_pz",    "TauLead_p4.Pz()")
                .Define("TauLead_p",    "TauLead_p4.P()")
                .Define("TauLead_pt",    "TauLead_p4.Pt()")
                .Define("TauLead_e",     "TauLead_p4.E()")
                .Define("TauLead_eta",    "TauLead_p4.Eta()")
                .Define("TauLead_phi",    "TauLead_p4.Phi()")
                .Define("TauLead_theta",    "TauLead_p4.Theta()")
                .Define("TauLead_y",     "TauLead_p4.Rapidity()")
                .Define("TauLead_mass",    "TauLead_p4.M()")
                .Define("TauLead_type",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau1_type; else return RecoTau2_type;")
                .Define("n_TauLead_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_constituents; else return n_RecoTau2_constituents;")
                .Define("n_TauLead_charged_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_charged_constituents; else return n_RecoTau2_charged_constituents;")
                .Define("n_TauLead_neutral_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_neutral_constituents; else return n_RecoTau2_neutral_constituents;")

                .Define("TauSub_p4",       "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau2_p4; else return RecoTau1_p4;")
                .Define("TauSub_px",    "TauSub_p4.Px()")
                .Define("TauSub_py",    "TauSub_p4.Py()")
                .Define("TauSub_pz",    "TauSub_p4.Pz()")
                .Define("TauSub_p",    "TauSub_p4.P()")
                .Define("TauSub_pt",    "TauSub_p4.Pt()")
                .Define("TauSub_e",     "TauSub_p4.E()")
                .Define("TauSub_eta",    "TauSub_p4.Eta()")
                .Define("TauSub_phi",    "TauSub_p4.Phi()")
                .Define("TauSub_theta",    "TauSub_p4.Theta()")
                .Define("TauSub_y",     "TauSub_p4.Rapidity()")
                .Define("TauSub_mass",    "TauSub_p4.M()")
                .Define("TauSub_type",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau2_type; else return RecoTau1_type;")
                .Define("n_TauSub_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_constituents; else return n_RecoTau1_constituents;")
                .Define("n_TauSub_charged_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_charged_constituents; else return n_RecoTau1_charged_constituents;")
                .Define("n_TauSub_neutral_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_neutral_constituents; else return n_RecoTau1_neutral_constituents;")

                .Define("Tau_DR",       "FCCAnalyses::ZHfunctions::deltaR(TauLead_phi, TauSub_phi, TauLead_eta, TauSub_eta)")
                .Define("Tau_scalar",      "(TauLead_px*TauSub_px + TauLead_py*TauSub_py + TauLead_pz*TauSub_pz)")
                .Define("Tau_cos",      "Tau_scalar/(TauLead_p*TauSub_p)")
                .Define("Tau_DEta",    "(TauLead_eta - TauSub_eta)")
                .Define("Tau_DPhi",     "FCCAnalyses::ZHfunctions::deltaPhi(TauLead_phi, TauSub_phi)")

                .Define("RecoZDaughter_DR",       "FCCAnalyses::ZHfunctions::deltaR(RecoZLead_phi, RecoZSub_phi, RecoZLead_eta, RecoZSub_eta)")
                .Define("RecoZDaughter_scalar",      "(RecoZLead_px*RecoZSub_px + RecoZLead_py*RecoZSub_py + RecoZLead_pz*RecoZSub_pz)")
                .Define("RecoZDaughter_cos",      "RecoZDaughter_scalar/(RecoZLead_p*RecoZSub_p)")
                .Define("RecoZDaughter_DEta",    "(RecoZLead_eta - RecoZSub_eta)")
                .Define("RecoZDaughter_DPhi",    "FCCAnalyses::ZHfunctions::deltaPhi(RecoZLead_phi, RecoZSub_phi)")

                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,1.,240.)")
                .Define("Recoil",       "(Total_p4-RecoZ_p4).M()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
            ######## Monte-Carlo particles #######
            "n_FSGenElectron",
            "FSGenElectron_e",
            "FSGenElectron_p",
            "FSGenElectron_pt",
            "FSGenElectron_px",
            "FSGenElectron_py",
            "FSGenElectron_pz",
            "FSGenElectron_y",
            "FSGenElectron_eta",
            "FSGenElectron_theta",
            "FSGenElectron_phi",
            "FSGenElectron_charge",
            "FSGenElectron_mass",
            "FSGenElectron_parentPDG",
            "FSGenElectron_vertex_x",
            "FSGenElectron_vertex_y",
            "FSGenElectron_vertex_z",

            "n_FSGenMuon",
            "FSGenMuon_e",
            "FSGenMuon_p",
            "FSGenMuon_pt",
            "FSGenMuon_px",
            "FSGenMuon_py",
            "FSGenMuon_pz",
            "FSGenMuon_y",
            "FSGenMuon_eta",
            "FSGenMuon_theta",
            "FSGenMuon_phi",
            "FSGenMuon_charge",
            "FSGenMuon_mass",
            "FSGenMuon_parentPDG",
            "FSGenMuon_vertex_x",
            "FSGenMuon_vertex_y",
            "FSGenMuon_vertex_z",

            #"n_AllGenTau",
            #"AllGenTau_e",
            #"AllGenTau_p",
            #"AllGenTau_pt",
            #"AllGenTau_px",
            #"AllGenTau_py",
            #"AllGenTau_pz",
            #"AllGenTau_y",
            #"AllGenTau_eta",
            #"AllGenTau_theta",
            #"AllGenTau_phi",
            #"AllGenTau_charge",
            #"AllGenTau_mass",
            #"AllGenTau_parentPDG",
            #"AllGenTau_vertex_x",
            #"AllGenTau_vertex_y",
            #"AllGenTau_vertex_z",

            "n_HiggsGenTau",
            "HiggsGenTau_e",
            "HiggsGenTau_p",
            "HiggsGenTau_pt",
            "HiggsGenTau_px",
            "HiggsGenTau_py",
            "HiggsGenTau_pz",
            "HiggsGenTau_y",
            "HiggsGenTau_eta",
            "HiggsGenTau_theta",
            "HiggsGenTau_phi",
            "HiggsGenTau_charge",
            "HiggsGenTau_mass",
            "HiggsGenTau_parentPDG",
            "HiggsGenTau_vertex_x",
            "HiggsGenTau_vertex_y",
            "HiggsGenTau_vertex_z",

            "n_TauNeg_MuNuNu",       
            "n_TauNeg_MuNuNu_Phot",  
            "n_TauNeg_ENuNu",        
            "n_TauNeg_ENuNu_Phot",   
            "n_TauNeg_PiNu",         
            "n_TauNeg_PiNu_Phot",    
            "n_TauNeg_KNu",          
            "n_TauNeg_KNu_Phot",     
            "n_TauNeg_PiK0Nu",       
            "n_TauNeg_PiK0Nu_Phot",  
            "n_TauNeg_KK0Nu",        
            "n_TauNeg_KK0Nu_Phot",   
            "n_TauNeg_3PiNu",        
            "n_TauNeg_3PiNu_Phot",   
            "n_TauNeg_PiKKNu",       
            "n_TauNeg_PiKKNu_Phot",  

            "n_TauPos_MuNuNu",       
            "n_TauPos_MuNuNu_Phot",  
            "n_TauPos_ENuNu",        
            "n_TauPos_ENuNu_Phot",   
            "n_TauPos_PiNu",         
            "n_TauPos_PiNu_Phot",    
            "n_TauPos_KNu",          
            "n_TauPos_KNu_Phot",     
            "n_TauPos_PiK0Nu",       
            "n_TauPos_PiK0Nu_Phot",  
            "n_TauPos_KK0Nu",        
            "n_TauPos_KK0Nu_Phot",   
            "n_TauPos_3PiNu",        
            "n_TauPos_3PiNu_Phot",   
            "n_TauPos_PiKKNu",       
            "n_TauPos_PiKKNu_Phot", 

            "n_FSGenNeutrino",
            "FSGenNeutrino_e",
            "FSGenNeutrino_p",
            "FSGenNeutrino_pt",
            "FSGenNeutrino_px",
            "FSGenNeutrino_py",
            "FSGenNeutrino_pz",
            "FSGenNeutrino_y",
            "FSGenNeutrino_eta",
            "FSGenNeutrino_theta",
            "FSGenNeutrino_phi",
            "FSGenNeutrino_charge",
            #"FSGenNeutrino_parentPDG",

            "n_FSGenPhoton",
            "FSGenPhoton_e",
            "FSGenPhoton_p",
            "FSGenPhoton_pt",
            "FSGenPhoton_px",
            "FSGenPhoton_py",
            "FSGenPhoton_pz",
            "FSGenPhoton_y",
            "FSGenPhoton_eta",
            "FSGenPhoton_theta",
            "FSGenPhoton_phi",
            "FSGenPhoton_charge",
            #"FSGenPhoton_parentPDG",

            "n_GenHiggs",
            "GenHiggs_e",
            "GenHiggs_p", 
            "GenHiggs_pt", 
            "GenHiggs_px", 
            "GenHiggs_py", 
            "GenHiggs_pz", 
            "GenHiggs_y", 
            "GenHiggs_mass",
            "GenHiggs_eta", 
            "GenHiggs_theta", 
            "GenHiggs_phi", 
            "GenHiggs_charge", 

            ######## Reconstructed particles #######
            #"RecoMC_PID",

            "n_RecoElectrons",
            "RecoElectron_e",
            "RecoElectron_p",
            "RecoElectron_pt",
            "RecoElectron_px",
            "RecoElectron_py",
            "RecoElectron_pz",
            "RecoElectron_y",
            "RecoElectron_eta",
            "RecoElectron_theta",
            "RecoElectron_phi",
            "RecoElectron_charge",
            "RecoElectron_mass",
            "RecoElectronTrack_absD0",
            "RecoElectronTrack_absZ0",
            "RecoElectronTrack_absD0sig",
            "RecoElectronTrack_absZ0sig",
            "RecoElectronTrack_D0cov",
            "RecoElectronTrack_Z0cov",

            "n_RecoElectrons_sel",
            "RecoElectron_sel_e",
            "RecoElectron_sel_p",
            "RecoElectron_sel_pt",
            "RecoElectron_sel_px",
            "RecoElectron_sel_py",
            "RecoElectron_sel_pz",
            "RecoElectron_sel_y",
            "RecoElectron_sel_eta",
            "RecoElectron_sel_theta",
            "RecoElectron_sel_phi",
            "RecoElectron_sel_charge",
            "RecoElectron_sel_mass",
            "RecoElectronTrack_sel_absD0",
            "RecoElectronTrack_sel_absZ0",
            "RecoElectronTrack_sel_absD0sig",
            "RecoElectronTrack_sel_absZ0sig",
            "RecoElectronTrack_sel_D0cov",
            "RecoElectronTrack_sel_Z0cov",

            "n_RecoMuons",
            "RecoMuon_e",
            "RecoMuon_p",
            "RecoMuon_pt",
            "RecoMuon_px",
            "RecoMuon_py",
            "RecoMuon_pz",
            "RecoMuon_y",
            "RecoMuon_eta",
            "RecoMuon_theta",
            "RecoMuon_phi",
            "RecoMuon_charge",
            "RecoMuon_mass",
            "RecoMuonTrack_absD0",
            "RecoMuonTrack_absZ0",
            "RecoMuonTrack_absD0sig",
            "RecoMuonTrack_absZ0sig",
            "RecoMuonTrack_D0cov",
            "RecoMuonTrack_Z0cov",

            "n_RecoMuons_sel",
            "RecoMuon_sel_e",
            "RecoMuon_sel_p",
            "RecoMuon_sel_pt",
            "RecoMuon_sel_px",
            "RecoMuon_sel_py",
            "RecoMuon_sel_pz",
            "RecoMuon_sel_y",
            "RecoMuon_sel_eta",
            "RecoMuon_sel_theta",
            "RecoMuon_sel_phi",
            "RecoMuon_sel_charge",
            "RecoMuon_sel_mass",
            "RecoMuonTrack_sel_absD0",
            "RecoMuonTrack_sel_absZ0",
            "RecoMuonTrack_sel_absD0sig",
            "RecoMuonTrack_sel_absZ0sig",
            "RecoMuonTrack_sel_D0cov",
            "RecoMuonTrack_sel_Z0cov",

            "n_RecoLeptons",
            "RecoLepton_e",
            "RecoLepton_p",
            "RecoLepton_pt",
            "RecoLepton_px",
            "RecoLepton_py",
            "RecoLepton_pz",
            "RecoLepton_y",
            "RecoLepton_eta",
            "RecoLepton_theta",
            "RecoLepton_phi",
            "RecoLepton_charge",
            "RecoLepton_mass",
            "RecoLeptonTrack_absD0",
            "RecoLeptonTrack_absZ0",
            "RecoLeptonTrack_absD0sig",
            "RecoLeptonTrack_absZ0sig",
            "RecoLeptonTrack_D0cov",
            "RecoLeptonTrack_Z0cov",

            "n_RecoLeptons_sel",
            "RecoLepton_sel_e",
            "RecoLepton_sel_p",
            "RecoLepton_sel_pt",
            "RecoLepton_sel_px",
            "RecoLepton_sel_py",
            "RecoLepton_sel_pz",
            "RecoLepton_sel_y",
            "RecoLepton_sel_eta",
            "RecoLepton_sel_theta",
            "RecoLepton_sel_phi",
            "RecoLepton_sel_charge",
            "RecoLepton_sel_mass",
            "RecoLeptonTrack_sel_absD0",
            "RecoLeptonTrack_sel_absZ0",
            "RecoLeptonTrack_sel_absD0sig",
            "RecoLeptonTrack_sel_absZ0sig",
            "RecoLeptonTrack_sel_D0cov",
            "RecoLeptonTrack_sel_Z0cov",

            "n_RecoPhotons",
            "RecoPhoton_e",
            "RecoPhoton_p",
            "RecoPhoton_pt",
            "RecoPhoton_px",
            "RecoPhoton_py",
            "RecoPhoton_pz",
            "RecoPhoton_y",
            "RecoPhoton_eta",
            "RecoPhoton_theta",
            "RecoPhoton_phi",
            "RecoPhoton_charge",
            "RecoPhoton_mass",

            "n_NeutralHadrons",
            "NeutralHadrons_e",
            "NeutralHadrons_p",
            "NeutralHadrons_pt",
            "NeutralHadrons_px",
            "NeutralHadrons_py",
            "NeutralHadrons_pz",
            "NeutralHadrons_eta",
            "NeutralHadrons_theta",
            "NeutralHadrons_phi",
            "NeutralHadrons_charge",
            "NeutralHadrons_mass",

            #"n_NoEfficiency",
            #"NoEfficiency_e",
            #"NoEfficiency_p",
            #"NoEfficiency_pt",
            #"NoEfficiency_px",
            #"NoEfficiency_py",
            #"NoEfficiency_pz",
            #"NoEfficiency_eta",
            #"NoEfficiency_theta",
            #"NoEfficiency_phi",
            #"NoEfficiency_charge",
            #"NoEfficiency_type",
            #"NoEfficiency_mass",

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",

            #"n_RecoTracks",
            #"RecoVertexObject",
            #"RecoVertex",
            #"n_PrimaryTracks",
            #"PrimaryVertexObject",
            #"PrimaryVertex", 
            #"PrimaryVertex_xyz",
            #"PrimaryVertes_xy",
            #"n_SecondaryTracks",
            #"SecondaryVertexObject",
            #"SecondaryVertex",
            #"SecondaryVertex_xyz",
            #"SecondaryVertes_xy",
            #"VertexObject", 
            #"RecoPartPID" ,
            #"RecoPartPIDAtVertex",

            #"Jets_R5_e",     
            #"Jets_R5_p",     
            #"Jets_R5_pt",     
            #"Jets_R5_px",   
            #"Jets_R5_py",   
            #"Jets_R5_pz",     
            #"Jets_R5_eta",    
            #"Jets_R5_theta",   
            #"Jets_R5_phi",     
            #"Jets_R5_mass",        
            #"n_Jets_R5", 

            #"Jets_excl4_e",     
            #"Jets_excl4_p",     
            #"Jets_excl4_pt",     
            #"Jets_excl4_px",   
            #"Jets_excl4_py",   
            #"Jets_excl4_pz",     
            #"Jets_excl4_eta",    
            #"Jets_excl4_theta",   
            #"Jets_excl4_phi",     
            #"Jets_excl4_mass",        
            #"n_Jets_excl4", 
 
            #"TauFromJet_R5_p",
            #"TauFromJet_R5_pt",
            #"TauFromJet_R5_px",
            #"TauFromJet_R5_py",
            #"TauFromJet_R5_pz",
            #"TauFromJet_R5_theta",
            #"TauFromJet_R5_phi",
            #"TauFromJet_R5_e",
            #"TauFromJet_R5_eta",
            #"TauFromJet_R5_y",
            #"TauFromJet_R5_charge",
            #"TauFromJet_R5_type",
            #"TauFromJet_R5_mass",
            #"n_TauFromJet_R5",

            #"TauFromJet_p",
            #"TauFromJet_pt",
            #"TauFromJet_px",
            #"TauFromJet_py",
            #"TauFromJet_pz",
            #"TauFromJet_theta",
            #"TauFromJet_phi",
            #"TauFromJet_eta",
            #"TauFromJet_y",
            #"TauFromJet_e",
            #"TauFromJet_charge",
            #"TauFromJet_type",
            #"TauFromJet_mass",
            #"n_TauFromJet",

            #"Jets_R5_sel_e",     
            #"Jets_R5_sel_p",     
            #"Jets_R5_sel_pt",     
            #"Jets_R5_sel_px",   
            #"Jets_R5_sel_py",   
            #"Jets_R5_sel_pz",     
            #"Jets_R5_sel_eta",    
            #"Jets_R5_sel_theta",   
            #"Jets_R5_sel_phi",     
            #"Jets_R5_sel_mass",      
            #"n_Jets_R5_sel", 

            "TagJet_R5_px", 
            "TagJet_R5_py",    
            "TagJet_R5_pz",      
            "TagJet_R5_p",  
            "TagJet_R5_pt",    
            "TagJet_R5_phi", 
            "TagJet_R5_eta",     
            "TagJet_R5_theta",          
            "TagJet_R5_e",     
            "TagJet_R5_mass",        
            "TagJet_R5_charge",       
            "TagJet_R5_flavor", 
            "n_TagJet_R5_constituents",   
            "n_TagJet_R5_charged_constituents",   
            "n_TagJet_R5_neutral_constituents",   
            "n_TagJet_R5",    
            "TagJet_R5_cleanup",        

            "TagJet_R5_isG",  
            "TagJet_R5_isU",
            "TagJet_R5_isD",   
            "TagJet_R5_isS",  
            "TagJet_R5_isC",
            "TagJet_R5_isB",  
            "TagJet_R5_isTAU",

            "TauFromJet_R5_p",
            "TauFromJet_R5_pt",
            "TauFromJet_R5_px",
            "TauFromJet_R5_py",
            "TauFromJet_R5_pz",
            "TauFromJet_R5_theta",
            "TauFromJet_R5_phi",
            "TauFromJet_R5_e",
            "TauFromJet_R5_eta",
            "TauFromJet_R5_y",
            "TauFromJet_R5_charge",
            "TauFromJet_R5_type",
            "TauFromJet_R5_mass",
            "n_TauFromJet_R5",

            "TagJet_R5_sel_e",     
            "TagJet_R5_sel_p",     
            "TagJet_R5_sel_pt",     
            "TagJet_R5_sel_px",   
            "TagJet_R5_sel_py",   
            "TagJet_R5_sel_pz",     
            "TagJet_R5_sel_eta",    
            "TagJet_R5_sel_theta",   
            "TagJet_R5_sel_phi",     
            "TagJet_R5_sel_mass",      
            "n_TagJet_R5_sel", 
            
            "TagJet_kt4_px", 
            "TagJet_kt4_py",    
            "TagJet_kt4_pz",      
            "TagJet_kt4_p",  
            "TagJet_kt4_pt",    
            "TagJet_kt4_phi", 
            "TagJet_kt4_eta",     
            "TagJet_kt4_theta",          
            "TagJet_kt4_e",     
            "TagJet_kt4_mass",        
            "TagJet_kt4_charge",       
            "TagJet_kt4_flavor", 
            "n_TagJet_kt4_constituents",   
            "n_TagJet_kt4_charged_constituents",   
            "n_TagJet_kt4_neutral_constituents",   
            "n_TagJet_kt4",          

            "TagJet_kt4_isG",  
            "TagJet_kt4_isU",
            "TagJet_kt4_isD",   
            "TagJet_kt4_isS",  
            "TagJet_kt4_isC",
            "TagJet_kt4_isB",  
            "TagJet_kt4_isTAU",

            "TauFromJet_kt4_p",
            "TauFromJet_kt4_pt",
            "TauFromJet_kt4_px",
            "TauFromJet_kt4_py",
            "TauFromJet_kt4_pz",
            "TauFromJet_kt4_theta",
            "TauFromJet_kt4_phi",
            "TauFromJet_kt4_e",
            "TauFromJet_kt4_eta",
            "TauFromJet_kt4_y",
            "TauFromJet_kt4_charge",
            "TauFromJet_kt4_type",
            "TauFromJet_kt4_mass",
            "n_TauFromJet_kt4",

            "TagJet_kt4_sel_e",     
            "TagJet_kt4_sel_p",     
            "TagJet_kt4_sel_pt",     
            "TagJet_kt4_sel_px",   
            "TagJet_kt4_sel_py",   
            "TagJet_kt4_sel_pz",     
            "TagJet_kt4_sel_eta",    
            "TagJet_kt4_sel_theta",   
            "TagJet_kt4_sel_phi",     
            "TagJet_kt4_sel_mass",      
            "n_TagJet_kt4_sel",

            "TagJet_kt3_px", 
            "TagJet_kt3_py",    
            "TagJet_kt3_pz",      
            "TagJet_kt3_p",  
            "TagJet_kt3_pt",    
            "TagJet_kt3_phi", 
            "TagJet_kt3_eta",     
            "TagJet_kt3_theta",          
            "TagJet_kt3_e",     
            "TagJet_kt3_mass",        
            "TagJet_kt3_charge",       
            "TagJet_kt3_flavor", 
            "n_TagJet_kt3_constituents",   
            "n_TagJet_kt3_charged_constituents",   
            "n_TagJet_kt3_neutral_constituents",   
            "n_TagJet_kt3",          

            "TagJet_kt3_isG",  
            "TagJet_kt3_isU",
            "TagJet_kt3_isD",   
            "TagJet_kt3_isS",  
            "TagJet_kt3_isC",
            "TagJet_kt3_isB",  
            "TagJet_kt3_isTAU",

            "TauFromJet_kt3_p",
            "TauFromJet_kt3_pt",
            "TauFromJet_kt3_px",
            "TauFromJet_kt3_py",
            "TauFromJet_kt3_pz",
            "TauFromJet_kt3_theta",
            "TauFromJet_kt3_phi",
            "TauFromJet_kt3_e",
            "TauFromJet_kt3_eta",
            "TauFromJet_kt3_y",
            "TauFromJet_kt3_charge",
            "TauFromJet_kt3_type",
            "TauFromJet_kt3_mass",
            "n_TauFromJet_kt3",

            "TagJet_kt3_sel_e",     
            "TagJet_kt3_sel_p",     
            "TagJet_kt3_sel_pt",     
            "TagJet_kt3_sel_px",   
            "TagJet_kt3_sel_py",   
            "TagJet_kt3_sel_pz",     
            "TagJet_kt3_sel_eta",    
            "TagJet_kt3_sel_theta",   
            "TagJet_kt3_sel_phi",     
            "TagJet_kt3_sel_mass",      
            "n_TagJet_kt3_sel",

            "TagJet_kt2_px", 
            "TagJet_kt2_py",    
            "TagJet_kt2_pz",      
            "TagJet_kt2_p",  
            "TagJet_kt2_pt",    
            "TagJet_kt2_phi", 
            "TagJet_kt2_eta",     
            "TagJet_kt2_theta",          
            "TagJet_kt2_e",     
            "TagJet_kt2_mass",        
            "TagJet_kt2_charge",       
            "TagJet_kt2_flavor", 
            "n_TagJet_kt2_constituents",   
            "n_TagJet_kt2_charged_constituents",   
            "n_TagJet_kt2_neutral_constituents",   
            "n_TagJet_kt2",          

            "TagJet_kt2_isG",  
            "TagJet_kt2_isU",
            "TagJet_kt2_isD",   
            "TagJet_kt2_isS",  
            "TagJet_kt2_isC",
            "TagJet_kt2_isB",  
            "TagJet_kt2_isTAU",

            "TauFromJet_kt2_p",
            "TauFromJet_kt2_pt",
            "TauFromJet_kt2_px",
            "TauFromJet_kt2_py",
            "TauFromJet_kt2_pz",
            "TauFromJet_kt2_theta",
            "TauFromJet_kt2_phi",
            "TauFromJet_kt2_e",
            "TauFromJet_kt2_eta",
            "TauFromJet_kt2_y",
            "TauFromJet_kt2_charge",
            "TauFromJet_kt2_type",
            "TauFromJet_kt2_mass",
            "n_TauFromJet_kt2",

            "TagJet_kt2_sel_e",     
            "TagJet_kt2_sel_p",     
            "TagJet_kt2_sel_pt",     
            "TagJet_kt2_sel_px",   
            "TagJet_kt2_sel_py",   
            "TagJet_kt2_sel_pz",     
            "TagJet_kt2_sel_eta",    
            "TagJet_kt2_sel_theta",   
            "TagJet_kt2_sel_phi",     
            "TagJet_kt2_sel_mass",      
            "n_TagJet_kt2_sel",

            "TagJet_kt1_px", 
            "TagJet_kt1_py",    
            "TagJet_kt1_pz",      
            "TagJet_kt1_p",  
            "TagJet_kt1_pt",    
            "TagJet_kt1_phi", 
            "TagJet_kt1_eta",     
            "TagJet_kt1_theta",          
            "TagJet_kt1_e",     
            "TagJet_kt1_mass",        
            "TagJet_kt1_charge",       
            "TagJet_kt1_flavor", 
            "n_TagJet_kt1_constituents",   
            "n_TagJet_kt1_charged_constituents",   
            "n_TagJet_kt1_neutral_constituents",   
            "n_TagJet_kt1",          

            "TagJet_kt1_isG",  
            "TagJet_kt1_isU",
            "TagJet_kt1_isD",   
            "TagJet_kt1_isS",  
            "TagJet_kt1_isC",
            "TagJet_kt1_isB",  
            "TagJet_kt1_isTAU",

            "TauFromJet_kt1_p",
            "TauFromJet_kt1_pt",
            "TauFromJet_kt1_px",
            "TauFromJet_kt1_py",
            "TauFromJet_kt1_pz",
            "TauFromJet_kt1_theta",
            "TauFromJet_kt1_phi",
            "TauFromJet_kt1_e",
            "TauFromJet_kt1_eta",
            "TauFromJet_kt1_y",
            "TauFromJet_kt1_charge",
            "TauFromJet_kt1_type",
            "TauFromJet_kt1_mass",
            "n_TauFromJet_kt1",

            "TagJet_kt1_sel_e",     
            "TagJet_kt1_sel_p",     
            "TagJet_kt1_sel_pt",     
            "TagJet_kt1_sel_px",   
            "TagJet_kt1_sel_py",   
            "TagJet_kt1_sel_pz",     
            "TagJet_kt1_sel_eta",    
            "TagJet_kt1_sel_theta",   
            "TagJet_kt1_sel_phi",     
            "TagJet_kt1_sel_mass",      
            "n_TagJet_kt1_sel",

            "n_GenTau_had", 
            "n_TauTag_R5_match",  
            "n_TauTag_R5mass_match",
            "n_events_R5tag",  
            "n_events_R5masstag",
            "n_events_R5excl",

            "n_TauTag_kt4_match",  
            "n_TauTag_kt4mass_match",
            "n_events_kt4tag",  
            "n_events_kt4masstag",
            "n_events_kt4excl",

            "n_TauTag_kt3_match",  
            "n_TauTag_kt3mass_match",
            "n_events_kt3tag",  
            "n_events_kt3masstag",
            "n_events_kt3excl",

            "n_TauTag_kt2_match",  
            "n_TauTag_kt2mass_match",
            "n_events_kt2tag",  
            "n_events_kt2masstag",
            "n_events_kt2excl",

            "n_TauTag_kt1_match",  
            "n_TauTag_kt1mass_match",
            "n_events_kt1tag",  
            "n_events_kt1masstag",
            "n_events_kt1excl",  

        ]
        #complex variables added here at stage2
        branchList += [
            "TauTag_px", 
            "TauTag_py",    
            "TauTag_pz",      
            "TauTag_p",  
            "TauTag_pt",    
            "TauTag_phi", 
            "TauTag_eta",     
            "TauTag_theta",          
            "TauTag_e",     
            "TauTag_mass",        
            "TauTag_charge",       
            "TauTag_flavor",       
            "n_TauTag",          
            "TauTag_isG",  
            "TauTag_isU",
            "TauTag_isD",   
            "TauTag_isS",  
            "TauTag_isC",
            "TauTag_isB",  
            "TauTag_isTAU",

            "QuarkTag_px", 
            "QuarkTag_py",    
            "QuarkTag_pz",      
            "QuarkTag_p",  
            "QuarkTag_pt",    
            "QuarkTag_phi", 
            "QuarkTag_eta",     
            "QuarkTag_theta",          
            "QuarkTag_e",     
            "QuarkTag_mass",        
            "QuarkTag_charge",       
            "QuarkTag_flavor",       
            "n_QuarkTag",          
            "QuarkTag_isG",  
            "QuarkTag_isU",
            "QuarkTag_isD",   
            "QuarkTag_isS",  
            "QuarkTag_isC",
            "QuarkTag_isB",  
            "QuarkTag_isTAU",

            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",

            "RecoZ_px",
            "RecoZ_py",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_phi",
            "RecoZ_theta",
            "RecoZ_y",
            "RecoZ_mass",

            "RecoZLead_px", 
            "RecoZLead_py",   
            "RecoZLead_pz",   
            "RecoZLead_p",    
            "RecoZLead_pt",   
            "RecoZLead_e",    
            "RecoZLead_eta",    
            "RecoZLead_phi",    
            "RecoZLead_theta",   
            "RecoZLead_y",     
            "RecoZLead_mass",   

            "RecoZSub_px",    
            "RecoZSub_py",   
            "RecoZSub_pz",   
            "RecoZSub_p",   
            "RecoZSub_pt",  
            "RecoZSub_e",     
            "RecoZSub_eta",   
            "RecoZSub_phi",   
            "RecoZSub_theta",    
            "RecoZSub_y",    
            "RecoZSub_mass",   

            "RecoZP_px", 
            "RecoZP_py",   
            "RecoZP_pz",   
            "RecoZP_p",    
            "RecoZP_pt",   
            "RecoZP_e",    
            "RecoZP_eta",    
            "RecoZP_phi",    
            "RecoZP_theta",   
            "RecoZP_y",     
            "RecoZP_mass",   

            "RecoZM_px",    
            "RecoZM_py",   
            "RecoZM_pz",   
            "RecoZM_p",   
            "RecoZM_pt",  
            "RecoZM_e",     
            "RecoZM_eta",   
            "RecoZM_phi",   
            "RecoZM_theta",    
            "RecoZM_y",    
            "RecoZM_mass", 

            "RecoH_px",
            "RecoH_py",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_phi",
            "RecoH_theta",
            "RecoH_y",
            "RecoH_mass",

            "TauLead_px",    
            "TauLead_py",   
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_phi",    
            "TauLead_theta",    
            "TauLead_y",    
            "TauLead_mass",
            "TauLead_type",
            "n_TauLead_constituents",
            "n_TauLead_charged_constituents",
            "n_TauLead_neutral_constituents",

            "TauSub_px",    
            "TauSub_py",   
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta",    
            "TauSub_phi",    
            "TauSub_theta",    
            "TauSub_y",    
            "TauSub_mass",
            "TauSub_type",
            "n_TauSub_constituents",
            "n_TauSub_charged_constituents",
            "n_TauSub_neutral_constituents",

            "Recoil",
            "Collinear_mass", 
        
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta", 
            "Tau_DPhi",
            
            "RecoZDaughter_DR", 
            "RecoZDaughter_cos", 
            "RecoZDaughter_DEta", 
            "RecoZDaughter_DPhi", 

            "TauLepton_type", 
            "TauHadron_type",      
            "n_TauLepton_constituents",       
            "n_TauHadron_constituents",  
            "n_TauLepton_charged_constituents", 
            "n_TauHadron_charged_constituents",      
            "n_TauLepton_neutral_constituents",  
            "n_TauHadron_neutral_constituents",

        ]

        return branchList
