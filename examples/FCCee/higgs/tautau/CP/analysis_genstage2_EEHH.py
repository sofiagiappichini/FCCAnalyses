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

inputr_xsec = "/ceph/awiedl/FCCee/HiggsCP/stage1/"

outputr_xsec   = "/ceph/awiedl/FCCee/HiggsCP/stage2/"

inputr_EFT = "/ceph/sgiappic/HiggsCP/CP/stage1"

outputr_EFT = "/ceph/sgiappic/HiggsCP/CP/stage2_Gen"

#Optional: ncpus, default is 4
nCPUS = 10

if EFT :
    processList = processList_EFT
    inputDir = inputr_EFT
    outputDir = outputr_EFT
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

                .Define("FSGenZDaughter_p4",     "FCCAnalyses::ZHfunctions::build_p4(FSGenElectron_px[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_py[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_pz[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_e[abs(FSGenElectron_parentPDG)!=15])")
                .Define("FSGenZDaughter_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(FSGenZDaughter_p4)")
                .Define("FSGenZDaughter_charge",    "FSGenElectron_charge[abs(FSGenElectron_parentPDG)!=15]")
                .Define("FSGenZDaughter_mass",    "FSGenElectron_mass[abs(FSGenElectron_parentPDG)!=15]")
                .Define("FSGenZDaughter_vertex_x",   "FSGenElectron_vertex_x[abs(FSGenElectron_parentPDG)!=15]")
                .Define("FSGenZDaughter_vertex_y",   "FSGenElectron_vertex_y[abs(FSGenElectron_parentPDG)!=15]")
                .Define("FSGenZDaughter_vertex_z",   "FSGenElectron_vertex_z[abs(FSGenElectron_parentPDG)!=15]")
                .Define("n_FSGenZDaughter",     "FSGenZDaughter_mass.size()")

                .Define("FSGenMuon_size",   "FSGenMuon_vertex_z[abs(FSGenMuon_parentPDG)!=15]")
                .Define("n_FSGenMuon_sel",     "FSGenMuon_size.size()")
                

                ######################
                ##### FILTERING ######
                ######################
                .Define("OnePairGen",     "(n_FSGenZDaughter==2 and n_FSGenMuon_sel==0)*1.0")

                .Filter("OnePairGen==1 && n_FSRGenTau==2")

                .Filter("(FSGenZDaughter_charge.at(0) + FSGenZDaughter_charge.at(1))==0")

                .Filter("(FSRGenTau_charge.at(0) + FSRGenTau_charge.at(1))==0")

                #################
                # Gen particles #
                #################
                
                .Define("FSRGenTau_Lxyz", "return sqrt(FSRGenTau_vertex_x*FSRGenTau_vertex_x + FSRGenTau_vertex_y*FSRGenTau_vertex_y + FSRGenTau_vertex_z*FSRGenTau_vertex_z);") #in mm
        
                # tautau invariant mass
                .Define("GenTau_e", "if (n_FSRGenTau>1) return (FSRGenTau_e.at(0) + FSRGenTau_e.at(1)); else return float(-1000.);")
                .Define("GenTau_px", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0) + FSRGenTau_px.at(1)); else return float(-1000.);")
                .Define("GenTau_py", "if (n_FSRGenTau>1) return (FSRGenTau_py.at(0) + FSRGenTau_py.at(1)); else return float(-1000.);")
                .Define("GenTau_pz", "if (n_FSRGenTau>1) return (FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("FSRGenTau_invMass", "if (n_FSRGenTau>1) return sqrt(GenTau_e*GenTau_e - GenTau_px*GenTau_px - GenTau_py*GenTau_py - GenTau_pz*GenTau_pz ); else return float(-1000.);")
                
                # cosine between two leptons, in lab frame
                .Define("GenTau_p", "if (n_FSRGenTau>1) return sqrt(GenTau_px*GenTau_px + GenTau_py*GenTau_py + GenTau_pz*GenTau_pz); else return float(-1.);")
                .Define("GenTau_scalar", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0)*FSRGenTau_px.at(1) + FSRGenTau_py.at(0)*FSRGenTau_py.at(1) + FSRGenTau_pz.at(0)*FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("FSRGenTau_cos", "if (n_FSRGenTau>1) return (GenTau_scalar/(FSRGenTau_p.at(0)*FSRGenTau_p.at(1))); else return float(-2.);")

                # angular distance between two leptons, in lab frame
                # deltaEta and deltaPhi return the absolute values of the difference, may be intersting to keep the sign and order the taus by rapidity (y) (DOI: 10.1103/PhysRevD.99.095007) or soemthing else (pt...)
                .Define("FSRGenTau_DEta","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_eta.at(0) - FSRGenTau_eta.at(1); \
                                        else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_eta.at(1) - FSRGenTau_eta.at(0); else return float(-10.);")
                .Define("FSRGenTau_Acoplanarity","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_phi.at(0) - FSRGenTau_phi.at(1); \
                                        else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_phi.at(1) - FSRGenTau_phi.at(0); else return float(-10.); ")
                .Define("FSRGenTau_DR","if (n_FSRGenTau>1) return myUtils::deltaR(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1), FSRGenTau_eta.at(0), FSRGenTau_eta.at(1)); else return float(-1.);")

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

                .Define("HRF_GenTau_DEta",    "if (HRF_GenTau_y.at(0)>HRF_GenTau_y.at(1)) return (HRF_GenTau_eta.at(0) - HRF_GenTau_eta.at(1)); \
                                        else if (HRF_GenTau_y.at(0)<HRF_GenTau_y.at(1)) return (HRF_GenTau_eta.at(1) - HRF_GenTau_eta.at(0)); else return float(-10.);")
                .Define("HRF_GenTau_Acoplanarity",    "if (HRF_GenTau_y.at(0)>HRF_GenTau_y.at(1)) return (HRF_GenTau_phi.at(0) - HRF_GenTau_phi.at(1)); \
                                        else if (HRF_GenTau_y.at(0)<HRF_GenTau_y.at(1)) return (HRF_GenTau_phi.at(1) - HRF_GenTau_phi.at(0)); else return float(-10.);")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 

                .Define("GenZ_p4",     "FCCAnalyses::ZHfunctions::build_p4_single((FSGenZDaughter_px.at(0)+FSGenZDaughter_px.at(1)), (FSGenZDaughter_py.at(0)+FSGenZDaughter_py.at(1)), (FSGenZDaughter_pz.at(0)+FSGenZDaughter_pz.at(1)), (FSGenZDaughter_e.at(0)+FSGenZDaughter_e.at(1)))")
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

                .Define("FSGenZDaughter_DEta",    "if (FSGenZDaughter_y.at(0)>FSGenZDaughter_y.at(1)) return (FSGenZDaughter_eta.at(0) - FSGenZDaughter_eta.at(1)); \
                                        else if (FSGenZDaughter_y.at(0)<FSGenZDaughter_y.at(1)) return (FSGenZDaughter_eta.at(1) - FSGenZDaughter_eta.at(0)); else return float(-10.);")
                .Define("FSGenZDaughter_Acoplanarity",    "if (FSGenZDaughter_y.at(0)>FSGenZDaughter_y.at(1)) return (FSGenZDaughter_phi.at(0) - FSGenZDaughter_phi.at(1)); \
                                        else if (FSGenZDaughter_y.at(0)<FSGenZDaughter_y.at(1)) return (FSGenZDaughter_phi.at(1) - FSGenZDaughter_phi.at(0)); else return float(-10.);")
                
                .Define("ZRF_GenZDaughter_p4",    "return myUtils::boosted_p4(- GenZ_p4, FSGenZDaughter_p4);")
                .Define("ZRF_GenZDaughter_px",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_py",    "FCCAnalyses::ZHfunctions::get_py_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_pz",    "FCCAnalyses::ZHfunctions::get_px_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_p",    "FCCAnalyses::ZHfunctions::get_p_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_pt",    "FCCAnalyses::ZHfunctions::get_pt_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_e",    "FCCAnalyses::ZHfunctions::get_e_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_eta",    "FCCAnalyses::ZHfunctions::get_eta_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_phi",    "FCCAnalyses::ZHfunctions::get_phi_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_theta",    "FCCAnalyses::ZHfunctions::get_theta_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_y",    "FCCAnalyses::ZHfunctions::get_y_tlv(ZRF_GenZDaughter_p4)")
                .Define("ZRF_GenZDaughter_charge",    "FSGenZDaughter_charge")

                .Define("ZRF_GenZDaughter_DEta",    "if (ZRF_GenZDaughter_y.at(0)>ZRF_GenZDaughter_y.at(1)) return (ZRF_GenZDaughter_eta.at(0) - ZRF_GenZDaughter_eta.at(1)); \
                                        else if (ZRF_GenZDaughter_y.at(0)<ZRF_GenZDaughter_y.at(1)) return (ZRF_GenZDaughter_eta.at(1) - ZRF_GenZDaughter_eta.at(0)); else return float(-10.);")
                .Define("ZRF_GenZDaughter_Acoplanarity",    "if (ZRF_GenZDaughter_y.at(0)>ZRF_GenZDaughter_y.at(1)) return (ZRF_GenZDaughter_phi.at(0) - ZRF_GenZDaughter_phi.at(1)); \
                                        else if (ZRF_GenZDaughter_y.at(0)<ZRF_GenZDaughter_y.at(1)) return (ZRF_GenZDaughter_phi.at(1) - ZRF_GenZDaughter_phi.at(0)); else return float(-10.);")

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715, changed some of the names around
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                .Define("HRF_GenTauM_p4",       "HRF_GenTau_p4[HRF_GenTau_charge==-1]")
                .Define("HRF_GenTauM_p",       "HRF_GenTau_p[HRF_GenTau_charge==-1]")
                .Define("ZRF_GenZDaughterM_p4",       "ZRF_GenZDaughter_p4[ZRF_GenZDaughter_charge==-1]")
                .Define("ZRF_GenZDaughterM_p",       "ZRF_GenZDaughter_p[ZRF_GenZDaughter_charge==-1]")
                #angle between H vector in lab frame and tau in H rest frame
                .Define("GenTheta2",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenHiggs_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{HRF_GenTauM_p4.at(0)})/(GenHiggs_p.at(0)*HRF_GenTauM_p.at(0)))")
                #angle between Z vector in lab frame and Muon in Z rest frame
                .Define("GenTheta1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenZ_p4}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenZDaughterM_p4.at(0)})/(GenZ_p*ZRF_GenZDaughterM_p.at(0)))")
                #angle between decay planes of H and Z
                .Define("GenPhi",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{HRF_GenTauM_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenZDaughterM_p4.at(0)})/(HRF_GenTauM_p.at(0)*ZRF_GenZDaughterM_p.at(0)))")
                #angle between beam line and Z decay plane
                .Define("Beam_vec",     "FCCAnalyses::ZHfunctions::build_p4_single(0, 0, 1, 0)") #unitary vector of beam axis along z
                .Define("Beam_p",       "float(1.)") #magnitude

                .Define("GenPhi1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenZDaughterM_p4.at(0)})/(Beam_p*ZRF_GenZDaughterM_p.at(0)))")
                .Define("GenThetastar",      "acos(FCCAnalyses::ZHfunctions::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{GenZ_p4})/(Beam_p*GenZ_p))")

                .Define("GenThetastar_cos",        "(cos(GenThetastar))")
                .Define("GenTheta1_cos",        "(cos(GenTheta1))")
                .Define("GenTheta2_cos",        "(cos(GenTheta2))")
                .Define("GenPhi_cos",        "(cos(GenPhi))")
                .Define("GenPhi1_cos",        "(cos(GenPhi1))")

                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                .Define("GenRecoil",       "(Total_p4-GenZ_p4).M()")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
            ######## Monte-Carlo particles #######
            "n_FSGenZDaughter",
            "FSGenZDaughter_e",
            "FSGenZDaughter_p",
            "FSGenZDaughter_pt",
            "FSGenZDaughter_px",
            "FSGenZDaughter_py",
            "FSGenZDaughter_pz",
            "FSGenZDaughter_y",
            "FSGenZDaughter_eta",
            "FSGenZDaughter_theta",
            "FSGenZDaughter_phi",
            "FSGenZDaughter_charge",
            "FSGenZDaughter_mass",
            "FSGenZDaughter_vertex_x",
            "FSGenZDaughter_vertex_y",
            "FSGenZDaughter_vertex_z",

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
            "FSRGenTau_vertex_x",
            "FSRGenTau_vertex_y",
            "FSRGenTau_vertex_z",

            #"n_TauNeg_MuNuNu",       
            #"n_TauNeg_MuNuNu_Phot",  
            #"n_TauNeg_ENuNu",        
            #"n_TauNeg_ENuNu_Phot",   
            #"n_TauNeg_PiNu",         
            #"n_TauNeg_PiNu_Phot",    
            #"n_TauNeg_KNu",          
            #"n_TauNeg_KNu_Phot",     
            #"n_TauNeg_PiK0Nu",       
            #"n_TauNeg_PiK0Nu_Phot",  
            #"n_TauNeg_KK0Nu",        
            #"n_TauNeg_KK0Nu_Phot",   
            #"n_TauNeg_3PiNu",        
            #"n_TauNeg_3PiNu_Phot",   
            #"n_TauNeg_PiKKNu",       
            #"n_TauNeg_PiKKNu_Phot",  

            #"n_TauPos_MuNuNu",       
            #"n_TauPos_MuNuNu_Phot",  
            #"n_TauPos_ENuNu",        
            #"n_TauPos_ENuNu_Phot",   
            #"n_TauPos_PiNu",         
            #"n_TauPos_PiNu_Phot",    
            #"n_TauPos_KNu",          
            #"n_TauPos_KNu_Phot",     
            #"n_TauPos_PiK0Nu",       
            #"n_TauPos_PiK0Nu_Phot",  
            #"n_TauPos_KK0Nu",        
            #"n_TauPos_KK0Nu_Phot",   
            #"n_TauPos_3PiNu",        
            #"n_TauPos_3PiNu_Phot",   
            #"n_TauPos_PiKKNu",       
            #"n_TauPos_PiKKNu_Phot", 

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

            "FSGenZDaughter_DEta", 
            "FSGenZDaughter_Acoplanarity", 

            "ZRF_GenZDaughter_px",  
            "ZRF_GenZDaughter_py",  
            "ZRF_GenZDaughter_pz", 
            "ZRF_GenZDaughter_p", 
            "ZRF_GenZDaughter_pt",  
            "ZRF_GenZDaughter_e",   
            "ZRF_GenZDaughter_eta", 
            "ZRF_GenZDaughter_phi",  
            "ZRF_GenZDaughter_theta",    
            "ZRF_GenZDaughter_y", 

            "ZRF_GenZDaughter_DEta", 
            "ZRF_GenZDaughter_Acoplanarity", 
            
            "FSRGenTau_DEta",
            "FSRGenTau_Acoplanarity",
            "FSRGenTau_cos",
            "FSRGenTau_DR",

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

            "HRF_GenTau_DEta", 
            "HRF_GenTau_Acoplanarity",

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

            "GenRecoil",

        ]

        return branchList