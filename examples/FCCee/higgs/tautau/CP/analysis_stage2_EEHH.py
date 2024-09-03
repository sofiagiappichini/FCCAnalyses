import os, copy # tagging
import ROOT

EFT = True

#Mandatory: List of processes
processList_EFT = {
    'noISR_e+e-_noCuts_EWonly':{},
    'noISR_e+e-_noCuts_cehim_m1':{},
    'noISR_e+e-_noCuts_cehim_p1':{},
    'noISR_e+e-_noCuts_cehre_m1':{},
    'noISR_e+e-_noCuts_cehre_p1':{},
}

processList_xsec = {
    'p8_ee_WW_ecm240':{'chunks':100},
    'p8_ee_Zqq_ecm240':{'chunks':100},
    'p8_ee_ZZ_ecm240':{'chunks':100},
    
    'wzp6_ee_tautau_ecm240':{'chunks':100},
    'wzp6_ee_mumu_ecm240':{'chunks':100},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':100},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':10},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':10},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':10},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':10},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':10},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':100},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':100},
    'wzp6_gaga_ee_60_ecm240': {'chunks':100},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':10},

    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':10},

}

inputDir_xsec = "/ceph/awiedl/FCCee/HiggsCP/stage1/"

outputDir_xsec   = "/ceph/awiedl/FCCee/HiggsCP/stage2/"

inputDir_EFT = "/ceph/sgiappic/HiggsCP/CP/stage1"

outputDir_EFT = "/ceph/sgiappic/HiggsCP/CP/stage2_id2"

#Optional: ncpus, default is 4
nCPUS = 10

if EFT :
    processList = processList_EFT
    inputDir = inputDir_EFT
    outputDir = outputDir_EFT
else:
    processList = processList_xsec
    inputDir = inputDir_xsec
    outputDir = outputDir_xsec

#Optional: ncpus, default is 4
nCPUS = 10

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "microcentury"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                #################
                # Gen particles #
                #################
                
                .Define("FSRGenTau_Lxyz", "return sqrt(FSRGenTau_vertex_x*FSRGenTau_vertex_x + FSRGenTau_vertex_y*FSRGenTau_vertex_y + FSRGenTau_vertex_z*FSRGenTau_vertex_z);") #in mm
        
                # tautau invariant mass
                .Define("GenDiTau_e", "if (n_FSRGenTau>1) return (FSRGenTau_e.at(0) + FSRGenTau_e.at(1)); else return float(-1000.);")
                .Define("GenDiTau_px", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0) + FSRGenTau_px.at(1)); else return float(-1000.);")
                .Define("GenDiTau_py", "if (n_FSRGenTau>1) return (FSRGenTau_py.at(0) + FSRGenTau_py.at(1)); else return float(-1000.);")
                .Define("GenDiTau_pz", "if (n_FSRGenTau>1) return (FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("GenDiTau_invMass", "if (n_FSRGenTau>1) return sqrt(GenDiTau_e*GenDiTau_e - GenDiTau_px*GenDiTau_px - GenDiTau_py*GenDiTau_py - GenDiTau_pz*GenDiTau_pz ); else return float(-1000.);")
                
                # cosine between two leptons, in lab frame
                .Define("GenDiTau_p", "if (n_FSRGenTau>1) return sqrt(GenDiTau_px*GenDiTau_px + GenDiTau_py*GenDiTau_py + GenDiTau_pz*GenDiTau_pz); else return float(-1.);")
                .Define("GenDiTau_scalar", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0)*FSRGenTau_px.at(1) + FSRGenTau_py.at(0)*FSRGenTau_py.at(1) + FSRGenTau_pz.at(0)*FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("GenDiTau_cos", "if (n_FSRGenTau>1) return (GenDiTau_scalar/(FSRGenTau_p.at(0)*FSRGenTau_p.at(1))); else return float(-2.);")

                # angular distance between two leptons, in lab frame
                # deltaEta and deltaPhi return the absolute values of the difference, may be intersting to keep the sign and order the taus by rapidity (y) (DOI: 10.1103/PhysRevD.99.095007) or soemthing else (pt...)
                .Define("GenDiTau_absDEta","if (n_FSRGenTau>1) return myUtils::deltaEta(FSRGenTau_eta.at(0), FSRGenTau_eta.at(1)); else return float(-10.);")
                .Define("GenDiTau_absDPhi","if (n_FSRGenTau>1) return myUtils::deltaPhi(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1)); else return float(-10.);")
                .Define("GenDiTau_DEta","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_eta.at(0) - FSRGenTau_eta.at(1); \
                                        else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_eta.at(1) - FSRGenTau_eta.at(0); else return float(-10.);")
                .Define("GenDiTau_DPhi","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_phi.at(0) - FSRGenTau_phi.at(1); \
                                        else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_phi.at(1) - FSRGenTau_phi.at(0); else return float(-10.); ")
                .Define("GenDiTau_DR","if (n_FSRGenTau>1) return myUtils::deltaR(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1), FSRGenTau_eta.at(0), FSRGenTau_eta.at(1)); else return float(-1.);")

                .Define("GenHiggs_p4",      "FCCAnalyses::ZHfunctions::build_p4(GenHiggs_px, GenHiggs_py, GenHiggs_pz, GenHiggs_e)")
                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("FSRGenTau_p4",     "FCCAnalyses::ZHfunctions::build_p4(FSRGenTau_px, FSRGenTau_py, FSRGenTau_pz, FSRGenTau_e)")
                .Define("HRF_GenTau_p4",    "myUtils::boosted_p4(- GenHiggs_p4.at(0), FSRGenTau_p4)")
                .Define("HRF_GenTau_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(HRF_GenTau_p4)")
                .Define("HRF_GenTau_charge",    "FSRGenTau_charge")

                .Define("HRF_GenDiTau_DEta",    "if (HRF_GenTau_y.at(0)>HRF_GenTau_y.at(1)) return (HRF_GenTau_eta.at(0) - HRF_GenTau_eta.at(1)); \
                                        else if (HRF_GenTau_y.at(0)<HRF_GenTau_y.at(1)) return (HRF_GenTau_eta.at(1) - HRF_GenTau_eta.at(0)); else return float(-10.);")
                .Define("HRF_GenDiTau_DPhi",    "if (HRF_GenTau_y.at(0)>HRF_GenTau_y.at(1)) return (HRF_GenTau_phi.at(0) - HRF_GenTau_phi.at(1)); \
                                        else if (HRF_GenTau_y.at(0)<HRF_GenTau_y.at(1)) return (HRF_GenTau_phi.at(1) - HRF_GenTau_phi.at(0)); else return float(-10.);")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("GenZ_p4",     "FCCAnalyses::ZHfunctions::build_p4_single((FSGenElectron_px.at(0)+FSGenElectron_px.at(1)), (FSGenElectron_py.at(0)+FSGenElectron_py.at(1)), (FSGenElectron_pz.at(0)+FSGenElectron_pz.at(1)), (FSGenElectron_e.at(0)+FSGenElectron_e.at(1)))")
                .Define("GenZ_px",    "GenZ_p4.Px()")
                .Define("GenZ_py",    "GenZ_p4.Py()")
                .Define("GenZ_pz",    "GenZ_p4.Pz()")
                .Define("GenZ_p",    "GenZ_p4.P()")
                .Define("GenZ_pt",    "GenZ_p4.Pt()")
                .Define("GenZ_e",     "GenZ_p4.E()")
                .Define("GenZ_eta",    "GenZ_p4.Eta()")
                .Define("GenZ_phi",    "GenZ_p4.Phi()")
                .Define("GenZ_theta",    "GenZ_p4.Theta()")
                .Define("GenZ_y",     "GenZ_p4.Rapidity()")
                .Define("GenZ_mass",    "GenZ_p4.M()")
                
                .Define("FSGenElectron_p4",     "FCCAnalyses::ZHfunctions::build_p4(FSGenElectron_px, FSGenElectron_py, FSGenElectron_pz, FSGenElectron_e)")
                .Define("ZRF_GenElectron_p4",    "return myUtils::boosted_p4(- GenZ_p4, FSGenElectron_p4);")
                .Define("ZRF_GenElectron_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(ZRF_GenElectron_p4)")
                .Define("ZRF_GenElectron_charge",    "FSGenElectron_charge")

                .Define("ZRF_GenDiElectron_DEta",    "if (ZRF_GenElectron_y.at(0)>ZRF_GenElectron_y.at(1)) return (ZRF_GenElectron_eta.at(0) - ZRF_GenElectron_eta.at(1)); \
                                        else if (ZRF_GenElectron_y.at(0)<ZRF_GenElectron_y.at(1)) return (ZRF_GenElectron_eta.at(1) - ZRF_GenElectron_eta.at(0)); else return float(-10.);")
                .Define("ZRF_GenDiElectron_DPhi",    "if (ZRF_GenElectron_y.at(0)>ZRF_GenElectron_y.at(1)) return (ZRF_GenElectron_phi.at(0) - ZRF_GenElectron_phi.at(1)); \
                                        else if (ZRF_GenElectron_y.at(0)<ZRF_GenElectron_y.at(1)) return (ZRF_GenElectron_phi.at(1) - ZRF_GenElectron_phi.at(0)); else return float(-10.);")

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715, changed some of the names around
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                .Define("HRF_GenTauM_p4",       "HRF_GenTau_p4[HRF_GenTau_charge==-1]")
                .Define("HRF_GenTauM_p",       "HRF_GenTau_p[HRF_GenTau_charge==-1]")
                .Define("ZRF_GenElectronM_p4",       "ZRF_GenElectron_p4[ZRF_GenElectron_charge==-1]")
                .Define("ZRF_GenElectronM_p",       "ZRF_GenElectron_p[ZRF_GenElectron_charge==-1]")
                #angle between H vector in lab frame and tau in H rest frame
                .Define("GenTheta2",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenHiggs_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{HRF_GenTauM_p4.at(0)})/(GenHiggs_p.at(0)*HRF_GenTauM_p.at(0)))")
                #angle between Z vector in lab frame and Muon in Z rest frame
                .Define("GenTheta1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenZ_p4}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenElectronM_p4.at(0)})/(GenZ_p*ZRF_GenElectronM_p.at(0)))")
                #angle between decay planes of H and Z
                .Define("GenPhi",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{HRF_GenTauM_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenElectronM_p4.at(0)})/(HRF_GenTauM_p.at(0)*ZRF_GenElectronM_p.at(0)))")
                #angle between beam line and Z decay plane
                .Define("Beam_vec",     "FCCAnalyses::ZHfunctions::build_p4_single(0, 0, 1, 0)") #unitary vector of beam axis along z
                .Define("Beam_p",       "float(1.)") #magnitude
                .Define("GenPhi1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenElectronM_p4.at(0)})/(Beam_p*ZRF_GenElectronM_p.at(0)))")
                .Define("GenThetastar",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{GenZ_p4})/(Beam_p*GenZ_p))")

                .Define("GenThetastar_cos",        "(cos(GenThetastar))")
                .Define("GenTheta1_cos",        "(cos(GenTheta1))")
                .Define("GenTheta2_cos",        "(cos(GenTheta2))")
                .Define("GenPhi_cos",        "(cos(GenPhi))")
                .Define("GenPhi1_cos",        "(cos(GenPhi1))")

                ##################
                # Reco particles #
                ##################

                .Define("OnePair",     "(n_RecoElectrons==2 and n_RecoMuons==0)*1.0")

                .Filter("OnePair==1 && n_TauFromJet_R5==2 && n_Jets_R5_sel==0")

                .Filter("(RecoElectron_charge.at(0) + RecoElectron_charge.at(1))==0")

                #one prong decay of both taus

                .Filter("TauFromJet_R5_type.at(0)==2 and TauFromJet_R5_type.at(1)==2 and (TauFromJet_R5_charge.at(0) + TauFromJet_R5_charge.at(1))==0")

                .Define("RecoEmiss_p4",  "FCCAnalyses::ZHfunctions::build_p4_single(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
                .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
                .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
                .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
                .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
                .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_px, RecoLepton_py, RecoLepton_pz, RecoLepton_e)")

                .Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_3(RecoLepton_p4, RecoLepton_charge, RecoLepton_mass, 91.188)")

                .Define("RecoZ1_p4",      "RecoLepton_p4.at(0)")
                .Define("RecoZ2_p4",      "RecoLepton_p4.at(1)")
                
                .Define("RecoTau1_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(TauFromJet_R5_px.at(0), TauFromJet_R5_py.at(0), TauFromJet_R5_pz.at(0), TauFromJet_R5_e.at(0))")
                .Define("RecoTau2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(TauFromJet_R5_px.at(1), TauFromJet_R5_py.at(1), TauFromJet_R5_pz.at(1), TauFromJet_R5_e.at(1))")

                .Define("RecoZ_p4",          "RecoZ1_p4+RecoZ2_p4")
                .Define("RecoH_p4",         "RecoTau1_p4+RecoTau2_p4")

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
                
                .Define("TauLead_p4","if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau1_p4; else return RecoTau2_p4;")
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

                .Define("Tau_Acoplanarity",      "(TauLead_phi-TauSub_phi)")
                .Define("Tau_DR",       "FCCAnalyses::ZHfunctions::deltaR(TauLead_phi, TauSub_phi, TauLead_eta, TauSub_eta)")
                .Define("Tau_scalar",      "(TauLead_px*TauSub_px + TauLead_py*TauSub_py + TauLead_pz*TauSub_pz)")
                .Define("Tau_cos",      "RecoH_p/Tau_scalar")

                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                .Define("Recoil",       "(Total_p4-RecoZ_p4).M()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

                #### reco CP angular variables

                .Define("RecoDiTau_DEta",    "if (TauLead_y>TauSub_y) return (TauLead_eta - TauSub_eta); \
                                        else if (TauLead_y<TauSub_y) return (TauSub_eta - TauLead_eta); else return double(-10.);")
                .Define("RecoDiTau_DPhi",    "if (TauLead_y>TauSub_y) return (TauLead_phi - TauSub_phi); \
                                        else if (TauLead_y<TauSub_y) return (TauSub_phi - TauLead_phi); else return double(-10.);")

                .Define("RecoDiElectron_DEta",    "if (RecoElectron_y.at(0)>RecoElectron_y.at(1)) return (RecoElectron_eta.at(0) - RecoElectron_eta.at(1)); \
                                        else if (RecoElectron_y.at(0)<RecoElectron_y.at(1)) return (RecoElectron_eta.at(1) - RecoElectron_eta.at(0)); else return float(-10.);")
                .Define("RecoDiElectron_DPhi",    "if (RecoElectron_y.at(0)>RecoElectron_y.at(1)) return (RecoElectron_phi.at(0) - RecoElectron_phi.at(1)); \
                                        else if (RecoElectron_y.at(0)<RecoElectron_y.at(1)) return (RecoElectron_phi.at(1) - RecoElectron_phi.at(0)); else return float(-10.);")


                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("RecoTau_p4",       "FCCAnalyses::ZHfunctions::build_p4(TauFromJet_R5_px, TauFromJet_R5_py, TauFromJet_R5_pz, TauFromJet_R5_e)")
                .Define("HRF_RecoTau_p4",    "myUtils::boosted_p4(- RecoH_p4, RecoTau_p4)")
                .Define("HRF_RecoTau_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(HRF_RecoTau_p4)")
                .Define("HRF_RecoTau_charge",    "TauFromJet_R5_charge")

                .Define("HRF_RecoDiTau_DEta",    "if (HRF_RecoTau_y.at(0)>HRF_RecoTau_y.at(1)) return (HRF_RecoTau_eta.at(0) - HRF_RecoTau_eta.at(1)); \
                                        else if (HRF_RecoTau_y.at(0)<HRF_RecoTau_y.at(1)) return (HRF_RecoTau_eta.at(1) - HRF_RecoTau_eta.at(0)); else return float(-10.);")
                .Define("HRF_RecoDiTau_DPhi",    "if (HRF_RecoTau_y.at(0)>HRF_RecoTau_y.at(1)) return (HRF_RecoTau_phi.at(0) - HRF_RecoTau_phi.at(1)); \
                                        else if (HRF_RecoTau_y.at(0)<HRF_RecoTau_y.at(1)) return (HRF_RecoTau_phi.at(1) - HRF_RecoTau_phi.at(0)); else return float(-10.);")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("RecoElectron_p4",     "FCCAnalyses::ZHfunctions::build_p4(RecoElectron_px, RecoElectron_py, RecoElectron_pz, RecoElectron_e)")
                .Define("ZRF_RecoElectron_p4",    "return myUtils::boosted_p4(- RecoZ_p4, RecoElectron_p4);")
                .Define("ZRF_RecoElectron_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(ZRF_RecoElectron_p4)")
                .Define("ZRF_RecoElectron_charge",    "RecoElectron_charge")

                .Define("ZRF_RecoDiElectron_DEta",    "if (ZRF_RecoElectron_y.at(0)>ZRF_RecoElectron_y.at(1)) return (ZRF_RecoElectron_eta.at(0) - ZRF_RecoElectron_eta.at(1)); \
                                        else if (ZRF_RecoElectron_y.at(0)<ZRF_RecoElectron_y.at(1)) return (ZRF_RecoElectron_eta.at(1) - ZRF_RecoElectron_eta.at(0)); else return float(-10.);")
                .Define("ZRF_RecoDiElectron_DPhi",    "if (ZRF_RecoElectron_y.at(0)>ZRF_RecoElectron_y.at(1)) return (ZRF_RecoElectron_phi.at(0) - ZRF_RecoElectron_phi.at(1)); \
                                        else if (ZRF_RecoElectron_y.at(0)<ZRF_RecoElectron_y.at(1)) return (ZRF_RecoElectron_phi.at(1) - ZRF_RecoElectron_phi.at(0)); else return float(-10.);")

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                #angle between H vector in lab frame and tau in H rest frame
                .Define("RecoTheta2",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{RecoH_p4}, HRF_RecoTau_p4[HRF_RecoTau_charge==-1])/(RecoH_p*HRF_RecoTau_p[HRF_RecoTau_charge==-1]))")
                #angle between Z vector in lab frame and Muon in Z rest frame
                .Define("RecoTheta1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{RecoZ_p4}, ZRF_RecoElectron_p4[ZRF_RecoElectron_charge==-1])/(RecoZ_p*ZRF_RecoElectron_p[ZRF_RecoElectron_charge==-1]))")
                #angle between decay planes of H and Z
                .Define("RecoPhi",      "acos(FCCAnalyses::ZHfunctions::get_scalar(HRF_RecoTau_p4[HRF_RecoTau_charge==-1], ZRF_RecoElectron_p4[ZRF_RecoElectron_charge==-1])/(HRF_RecoTau_p[HRF_RecoTau_charge==-1]*ZRF_RecoElectron_p[ZRF_RecoElectron_charge==-1]))")
                #angle between beam line and Z decay plane
                .Define("RecoPhi1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ZRF_RecoElectron_p4[ZRF_RecoElectron_charge==-1])/(Beam_p*ZRF_RecoElectron_p[ZRF_RecoElectron_charge==-1]))")
                .Define("RecoThetastar",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{RecoZ_p4})/(Beam_p*RecoZ_p))")

                .Define("RecoThetastar_cos",        "(cos(RecoThetastar))")
                .Define("RecoTheta1_cos",        "(cos(RecoTheta1))")
                .Define("RecoTheta2_cos",        "(cos(RecoTheta2))")
                .Define("RecoPhi_cos",        "(cos(RecoPhi))")
                .Define("RecoPhi1_cos",        "(cos(RecoPhi1))")

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

            #"n_ZFSGenMuon",
            #"ZFSGenMuon_e",
            #"ZFSGenMuon_p",
            #"ZFSGenMuon_pt",
            #"ZFSGenMuon_px",
            #"ZFSGenMuon_py",
            #"ZFSGenMuon_pz",
            #"ZFSGenMuon_y",
            #"ZFSGenMuon_eta",
            #"ZFSGenMuon_theta",
            #"ZFSGenMuon_phi",
            #"ZFSGenMuon_charge",
            #"ZFSGenMuon_mass",
            #"ZFSGenMuon_parentPDG",
            #"ZFSGenMuon_vertex_x",
            #"ZFSGenMuon_vertex_y",
            #"ZFSGenMuon_vertex_z",

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

            #"noFSRGenTau_parentPDG",

            "n_FSRGenTau",
            "FSRGenTau_e",
            "FSRGenTau_p",
            "FSRGenTau_pt",
            "FSRGenTau_px",
            "FSRGenTau_py",
            "FSRGenTau_pz",
            "FSRGenTau_y",
            "FSRGenTau_eta",
            "FSRGenTau_theta",
            "FSRGenTau_phi",
            "FSRGenTau_charge",
            "FSRGenTau_mass",
            "FSRGenTau_parentPDG",
            "FSRGenTau_vertex_x",
            "FSRGenTau_vertex_y",
            "FSRGenTau_vertex_z",

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

            #"n_GenZ",
            #"n_GenW",
            
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

            "Jets_R5_e",     
            "Jets_R5_p",     
            "Jets_R5_pt",     
            "Jets_R5_px",   
            "Jets_R5_py",   
            "Jets_R5_pz",     
            "Jets_R5_eta",    
            "Jets_R5_theta",   
            "Jets_R5_phi",     
            "Jets_R5_mass",        
            "n_Jets_R5", 

            "Jets_excl4_e",     
            "Jets_excl4_p",     
            "Jets_excl4_pt",     
            "Jets_excl4_px",   
            "Jets_excl4_py",   
            "Jets_excl4_pz",     
            "Jets_excl4_eta",    
            "Jets_excl4_theta",   
            "Jets_excl4_phi",     
            "Jets_excl4_mass",        
            "n_Jets_excl4", 
 
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

            "TauFromJet_p",
            "TauFromJet_pt",
            "TauFromJet_px",
            "TauFromJet_py",
            "TauFromJet_pz",
            "TauFromJet_theta",
            "TauFromJet_phi",
            "TauFromJet_eta",
            "TauFromJet_y",
            "TauFromJet_e",
            "TauFromJet_charge",
            "TauFromJet_type",
            "TauFromJet_mass",
            "n_TauFromJet",

            "Jets_R5_sel_e",     
            "Jets_R5_sel_p",     
            "Jets_R5_sel_pt",     
            "Jets_R5_sel_px",   
            "Jets_R5_sel_py",   
            "Jets_R5_sel_pz",     
            "Jets_R5_sel_eta",    
            "Jets_R5_sel_theta",   
            "Jets_R5_sel_phi",     
            "Jets_R5_sel_mass",      
            "n_Jets_R5_sel", 
        ]
        #complex variables added here at stage2
        branchList += [
            ######## Monte-Carlo particles #######
            "GenZ_e",
            "GenZ_p", 
            "GenZ_pt", 
            "GenZ_px", 
            "GenZ_py", 
            "GenZ_pz", 
            "GenZ_y", 
            "GenZ_mass",
            "GenZ_eta", 
            "GenZ_theta", 
            "GenZ_phi", 
            
            "GenDiTau_DEta",
            "GenDiTau_DPhi",
            "GenDiTau_absDEta",
            "GenDiTau_absDPhi",
            "GenDiTau_cos",
            "GenDiTau_DR",

            "HRF_GenTau_px",  
            "HRF_GenTau_py",  
            "HRF_GenTau_pz", 
            "HRF_GenTau_p", 
            "HRF_GenTau_pt",  
            "HRF_GenTau_e",   
            "HRF_GenTau_eta", 
            "HRF_GenTau_phi",  
            "HRF_GenTau_theta",    
            "HRF_GenTau_y", 

            "HRF_GenDiTau_DEta", 
            "HRF_GenDiTau_DPhi",

            "GenThetastar",
            "GenTheta2",
            "GenPhi1", 
            "GenPhi", 
            "GenTheta1", 

            "GenThetastar_cos",
            "GenTheta2_cos",
            "GenPhi1_cos", 
            "GenPhi_cos", 
            "GenTheta1_cos", 

        ]

        branchList += [
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

                "Tau_Acoplanarity",
                "Tau_DR",
                "Tau_cos",

                "Recoil",
                "Collinear_mass", 
        ]

        branchList += [

            "RecoDiTau_DEta", 
            "RecoDiTau_DPhi", 
            "RecoDiElectron_DEta", 
            "RecoDiElectron_DPhi", 

            "HRF_RecoTau_px",  
            "HRF_RecoTau_py",  
            "HRF_RecoTau_pz", 
            "HRF_RecoTau_p", 
            "HRF_RecoTau_pt",  
            "HRF_RecoTau_e",   
            "HRF_RecoTau_eta", 
            "HRF_RecoTau_phi",  
            "HRF_RecoTau_theta",    
            "HRF_RecoTau_y", 

            "HRF_RecoDiTau_DEta", 
            "HRF_RecoDiTau_DPhi", 

            "ZRF_RecoElectron_px",  
            "ZRF_RecoElectron_py",  
            "ZRF_RecoElectron_pz", 
            "ZRF_RecoElectron_p", 
            "ZRF_RecoElectron_pt",  
            "ZRF_RecoElectron_e",   
            "ZRF_RecoElectron_eta", 
            "ZRF_RecoElectron_phi",  
            "ZRF_RecoElectron_theta",    
            "ZRF_RecoElectron_y", 

            "ZRF_RecoDiElectron_DEta", 
            "ZRF_RecoDiElectron_DPhi", 

            "RecoThetastar",
            "RecoTheta2",
            "RecoPhi1", 
            "RecoPhi", 
            "RecoTheta1", 

            "RecoThetastar_cos",
            "RecoTheta2_cos",
            "RecoPhi1_cos", 
            "RecoPhi_cos", 
            "RecoTheta1_cos", 

        ]

        return branchList