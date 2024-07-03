import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10}, #check that it's fine to keep them in chunks, otherwise just remove the option and leave {},
    #'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_HWW_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hmumu_ecm240': {'chunks':10},
}

inputDir = "/eos/user/s/sgiappic/HiggsCP/stage1_24_06_27/"

#Optional: output directory, default is local running directory
outputDir   = "/eos/user/s/sgiappic/HiggsCP/stage2/" #your output directory

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

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

            ### to find already made functions, this is where they are or where they can be added instead of writing them here
            ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

            #################
            # Gen particles #
            #################

            # filter events based on gen or reco variables
            .Filter("n_FSRGenTau==2 && n_GenHiggs>0")
            
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

            #just to check that the reconstruction of the higgs works comparing to the gen class of the higgs itself
            .Define("GenHiggs_Reco_p4",      "myUtils::build_p4(ROOT::VecOps::RVec<float>{GenDiTau_px}, ROOT::VecOps::RVec<float>{GenDiTau_py}, ROOT::VecOps::RVec<float>{GenDiTau_pz}, ROOT::VecOps::RVec<float>{GenDiTau_e})")
            .Define("GenHiggs_Reco_px",    "myUtils::get_pxtvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_py",    "myUtils::get_pytvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_pz",    "myUtils::get_pxtvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_p",    "myUtils::get_ptvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_pt",    "myUtils::get_pttvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_e",    "myUtils::get_etvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_eta",    "myUtils::get_etatvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_phi",    "myUtils::get_phitvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_theta",    "myUtils::get_thetatvl(GenHiggs_Reco_p4)")
            .Define("GenHiggs_Reco_y",    "myUtils::get_ytvl(GenHiggs_Reco_p4)")

            .Define("GenHiggs_p4",      "myUtils::build_p4(GenHiggs_px, GenHiggs_py, GenHiggs_pz, GenHiggs_e)")
            #not needed for the boosting but nice to get a sense of the values
            .Define("GenHiggs_beta",        "return (GenHiggs_p.at(0)/GenHiggs_e.at(0))")
            .Define("GenHiggs_gamma",  "myUtils::get_gamma(GenHiggs_p.at(0), GenHiggs_e.at(0))") # only works with one particle, not the whole class #myUtils::get_gamma(GenHiggs_p.at(0), GenHiggs_e.at(0))

            #boosted_p4 function will boost a vector of 4-vectors(tvl, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
            .Define("FSRGenTau_p4",     "myUtils::build_p4(FSRGenTau_px, FSRGenTau_py, FSRGenTau_pz, FSRGenTau_e)")
            .Define("HiggsRF_GenTau_p4",    "myUtils::boosted_p4_root(- GenHiggs_p4.at(0), FSRGenTau_p4)")
            .Define("HiggsRF_GenTau_px",    "myUtils::get_pxtvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_py",    "myUtils::get_pytvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_pz",    "myUtils::get_pxtvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_p",    "myUtils::get_ptvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_pt",    "myUtils::get_pttvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_e",    "myUtils::get_etvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_eta",    "myUtils::get_etatvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_phi",    "myUtils::get_phitvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_theta",    "myUtils::get_thetatvl(HiggsRF_GenTau_p4)")
            .Define("HiggsRF_GenTau_y",    "myUtils::get_ytvl(HiggsRF_GenTau_p4)")

            .Define("HiggsRF_GenDiTau_DEta",    "if (HiggsRF_GenTau_y.at(0)>HiggsRF_GenTau_y.at(1)) return (HiggsRF_GenTau_eta.at(0) - HiggsRF_GenTau_eta.at(1)); \
                                    else if (HiggsRF_GenTau_y.at(0)<HiggsRF_GenTau_y.at(1)) return (HiggsRF_GenTau_eta.at(1) - HiggsRF_GenTau_eta.at(0)); else return float(-10.);")
            .Define("HiggsRF_GenDiTau_DPhi",    "if (HiggsRF_GenTau_y.at(0)>HiggsRF_GenTau_y.at(1)) return (HiggsRF_GenTau_phi.at(0) - HiggsRF_GenTau_phi.at(1)); \
                                    else if (HiggsRF_GenTau_y.at(0)<HiggsRF_GenTau_y.at(1)) return (HiggsRF_GenTau_phi.at(1) - HiggsRF_GenTau_phi.at(0)); else return float(-10.);")

            #angle between higgs vector in lab frame and tau in higgs rest frame
            .Define("HiggsRF_GenTau_thetastar",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenHiggs_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{HiggsRF_GenTau_p4.at(0)})/(GenHiggs_p.at(0)*HiggsRF_GenTau_p.at(0)))")

            #reconstructing the Z assuming that the decay is visible (here for mumu)
            .Define("GenDiMuon_e", "if (n_FSGenMuon>1) return (FSGenMuon_e.at(0) + FSGenMuon_e.at(1)); else return float(-1000.);")
            .Define("GenDiMuon_px", "if (n_FSGenMuon>1) return (FSGenMuon_px.at(0) + FSGenMuon_px.at(1)); else return float(-1000.);")
            .Define("GenDiMuon_py", "if (n_FSGenMuon>1) return (FSGenMuon_py.at(0) + FSGenMuon_py.at(1)); else return float(-1000.);")
            .Define("GenDiMuon_pz", "if (n_FSGenMuon>1) return (FSGenMuon_pz.at(0) + FSGenMuon_pz.at(1)); else return float(-1000.);")

            .Define("GenZ_Reco_p4",      "if (n_FSGenMuon>1) return myUtils::build_p4(ROOT::VecOps::RVec<float>{GenDiMuon_px}, ROOT::VecOps::RVec<float>{GenDiMuon_py}, ROOT::VecOps::RVec<float>{GenDiMuon_pz}, ROOT::VecOps::RVec<float>{GenDiMuon_e}); else return ROOT::VecOps::RVec<TLorentzVector>{}")
            .Define("GenZ_Reco_px",    "myUtils::get_pxtvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_py",    "myUtils::get_pytvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_pz",    "myUtils::get_pxtvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_p",    "myUtils::get_ptvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_pt",    "myUtils::get_pttvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_e",    "myUtils::get_etvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_eta",    "myUtils::get_etatvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_phi",    "myUtils::get_phitvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_theta",    "myUtils::get_thetatvl(GenZ_Reco_p4)")
            .Define("GenZ_Reco_y",    "myUtils::get_ytvl(GenZ_Reco_p4)")

            .Define("GenZ_gamma",  "myUtils::get_gamma(GenZ_p.at(0), GenZ_e.at(0))") # only works with one particle, not the whole class #myUtils::get_gamma(GenZ_p.at(0), GenZ_e.at(0))

            #boosted_p4 function will boost a vector of 4-vectors(tvl, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
            .Define("FSGenMuon_p4",     "myUtils::build_p4(FSGenMuon_px, FSGenMuon_py, FSGenMuon_pz, FSGenMuon_e)")
            .Define("ZRF_GenMuon_p4",    "myUtils::boosted_p4_root(- GenZ_p4.at(0), FSGenMuon_p4)")
            .Define("ZRF_GenMuon_px",    "myUtils::get_pxtvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_py",    "myUtils::get_pytvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_pz",    "myUtils::get_pxtvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_p",    "myUtils::get_ptvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_pt",    "myUtils::get_pttvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_e",    "myUtils::get_etvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_eta",    "myUtils::get_etatvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_phi",    "myUtils::get_phitvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_theta",    "myUtils::get_thetatvl(ZRF_GenMuon_p4)")
            .Define("ZRF_GenMuon_y",    "myUtils::get_ytvl(ZRF_GenMuon_p4)")

            .Define("ZRF_GenDiMuon_DEta",    "if (ZRF_GenMuon_y.at(0)>ZRF_GenMuon_y.at(1)) return (ZRF_GenMuon_eta.at(0) - ZRF_GenMuon_eta.at(1)); \
                                    else if (ZRF_GenMuon_y.at(0)<ZRF_GenMuon_y.at(1)) return (ZRF_GenMuon_eta.at(1) - ZRF_GenMuon_eta.at(0)); else return float(-10.);")
            .Define("ZRF_GenDiMuon_DPhi",    "if (ZRF_GenMuon_y.at(0)>ZRF_GenMuon_y.at(1)) return (ZRF_GenMuon_phi.at(0) - ZRF_GenMuon_phi.at(1)); \
                                    else if (ZRF_GenMuon_y.at(0)<ZRF_GenMuon_y.at(1)) return (ZRF_GenMuon_phi.at(1) - ZRF_GenMuon_phi.at(0)); else return float(-10.);")

            #angle between Z vector in lab frame and Muon in Z rest frame
            .Define("ZRF_GenMuon_theta2",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenZ_Reco_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenMuon_p4.at(0)})/(GenZ_Reco_p.at(0)*ZRF_GenMuon_p.at(0)))")
            #angle between decay planes of H and Z
            .Define("GenHiggs_GenZ_phi1",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{HiggsRF_GenTau_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenMuon_p4.at(0)})/(HiggsRF_GenTau_p.at(0)*ZRF_GenMuon.at(0)))")
            #angle between Z vector in lab frame and Muon in Z rest frame
            .Define("Beam_vec",     "myUtils::build_p4(0, 0, 1, 0)") #unitary vector of beam axis along z
            .Define("Beam_p",       "float(1.)") #magnitude
            .Define("GenZ_phi",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{ZRF_GenMuon_p4.at(0)})/(Beam_p*ZRF_GenMuon.at(0)))")
            .Define("GenZ_theta1",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{Beam_vec}, ROOT::VecOps::RVec<TLorentzVector>{GenZ_Reco_p4.at(0)})/(Beam_p*GenZ_Reco_p4.at(0)))")

            .Define("FSGenMuon_plus_e",       "if (FSGenMuon_charge == 1 && n_FSGenMuon == 2) return FSGenMuon_e; else return float(-1.);")

            ##################
            # Reco particles #
            ##################

            


            #############################################
            ##        Build Tau -> 3Pi candidates      ##
            #############################################

            .Define("Tau23PiCandidates",         "myUtils::build_tau23pi(VertexObject,RecoPartPIDAtVertex)")
            .Define("n_Tau23PiCandidates",        "float(myUtils::getFCCAnalysesComposite_N(Tau23PiCandidates))")

            .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
            .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
            .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
            .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
            .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
            .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
            .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
            .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
            .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
            .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

            .Define("Tau23PiCandidates_pion1px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
            .Define("Tau23PiCandidates_pion1py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
            .Define("Tau23PiCandidates_pion1pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
            .Define("Tau23PiCandidates_pion1p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
            .Define("Tau23PiCandidates_pion1q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
            .Define("Tau23PiCandidates_pion1d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 0)")
            .Define("Tau23PiCandidates_pion1z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 0)")

            .Define("Tau23PiCandidates_pion2px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
            .Define("Tau23PiCandidates_pion2py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
            .Define("Tau23PiCandidates_pion2pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
            .Define("Tau23PiCandidates_pion2p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
            .Define("Tau23PiCandidates_pion2q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
            .Define("Tau23PiCandidates_pion2d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 1)")
            .Define("Tau23PiCandidates_pion2z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 1)")

            .Define("Tau23PiCandidates_pion3px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 0)")
            .Define("Tau23PiCandidates_pion3py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 1)")
            .Define("Tau23PiCandidates_pion3pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 2)")
            .Define("Tau23PiCandidates_pion3p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, -1)")
            .Define("Tau23PiCandidates_pion3q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2)")
            .Define("Tau23PiCandidates_pion3d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 2)")
            .Define("Tau23PiCandidates_pion3z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 2)")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
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

                "n_AllGenTau",
                "AllGenTau_e",
                "AllGenTau_p",
                "AllGenTau_pt",
                "AllGenTau_px",
                "AllGenTau_py",
                "AllGenTau_pz",
                "AllGenTau_y",
                "AllGenTau_eta",
                "AllGenTau_theta",
                "AllGenTau_phi",
                "AllGenTau_charge",
                "AllGenTau_mass",
                "AllGenTau_parentPDG",
                "AllGenTau_vertex_x",
                "AllGenTau_vertex_y",
                "AllGenTau_vertex_z",

                "noFSRGenTau_parentPDG",

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

                "n_GenZ",
                "n_GenH",

                ######## Reconstructed particles #######
                "RecoMC_PID",

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
                "RecoElectronTrack_absD0",
                "RecoElectronTrack_absZ0",
                "RecoElectronTrack_absD0sig",
                "RecoElectronTrack_absZ0sig",
                "RecoElectronTrack_D0cov",
                "RecoElectronTrack_Z0cov",

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
                "RecoMuonTrack_absD0",
                "RecoMuonTrack_absZ0",
                "RecoMuonTrack_absD0sig",
                "RecoMuonTrack_absZ0sig",
                "RecoMuonTrack_D0cov",
                "RecoMuonTrack_Z0cov",

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

                "RecoMissingEnergy_e",
                "RecoMissingEnergy_p",
                "RecoMissingEnergy_pt",
                "RecoMissingEnergy_px",
                "RecoMissingEnergy_py",
                "RecoMissingEnergy_pz",
                "RecoMissingEnergy_eta",
                "RecoMissingEnergy_theta",
                "RecoMissingEnergy_phi",

                "n_RecoTracks",
                #"n_RecoVertex",
                "RecoVertexObject",
                "RecoVertex",
                "n_PrimaryTracks",
                "PrimaryVertexObject",
                "PrimaryVertex", 
                "PrimaryVertex_xyz",
                "PrimaryVertes_xy",
                "n_SecondaryTracks",
                "SecondaryVertexObject",
                "SecondaryVertex",
                "SecondaryVertex_xyz",
                "SecondaryVertes_xy",
                "VertexObject", 
                "RecoPartPID" ,
                "RecoPartPIDAtVertex",
        ]
        #complex variables added here at stage2
        branchList += [
                ######## Monte-Carlo particles #######
                "FSRGenTau_Lxyz",
                "GenDiTau_e",
                "GenDiTau_px",
                "GenDiTau_py",
                "GenDiTau_pz",
                "GenDiTau_p",
                "GenDiTau_DEta",
                "GenDiTau_DPhi",
                "GenDiTau_absDEta",
                "GenDiTau_absDPhi",
                "GenDiTau_invMass",
                "GenDiTau_cos",
                "GenDiTau_DR",

                "GenHiggs_Reco_e",
                "GenHiggs_Reco_p", 
                "GenHiggs_Reco_pt", 
                "GenHiggs_Reco_px", 
                "GenHiggs_Reco_py", 
                "GenHiggs_Reco_pz", 
                "GenHiggs_Reco_y", 
                "GenHiggs_Reco_eta", 
                "GenHiggs_Reco_theta", 
                "GenHiggs_Reco_phi", 

                "GenHiggs_beta",
                "GenHiggs_gamma",

                "HiggsRF_GenTau_px",  
                "HiggsRF_GenTau_py",  
                "HiggsRF_GenTau_pz", 
                "HiggsRF_GenTau_p", 
                "HiggsRF_GenTau_pt",  
                "HiggsRF_GenTau_e",   
                "HiggsRF_GenTau_eta", 
                "HiggsRF_GenTau_phi",  
                "HiggsRF_GenTau_theta",    
                "HiggsRF_GenTau_y", 

                "HiggsRF_GenDiTau_DEta", 
                "HiggsRF_GenDiTau_DPhi", 
                "HiggsRF_GenTau_thetastar",

                "GenZ_Reco_e",
                "GenZ_Reco_p", 
                "GenZ_Reco_pt", 
                "GenZ_Reco_px", 
                "GenZ_Reco_py", 
                "GenZ_Reco_pz", 
                "GenZ_Reco_y", 
                "GenZ_Reco_eta", 
                "GenZ_Reco_theta", 
                "GenZ_Reco_phi", 

                "GenZ_gamma",

                "ZRF_GenMuon_px",  
                "ZRF_GenMuon_py",  
                "ZRF_GenMuon_pz", 
                "ZRF_GenMuon_p", 
                "ZRF_GenMuon_pt",  
                "ZRF_GenMuon_e",   
                "ZRF_GenMuon_eta", 
                "ZRF_GenMuon_phi",  
                "ZRF_GenMuon_theta",    
                "ZRF_GenMuon_y", 

                "ZRF_GenDiMuon_DEta", 
                "ZRF_GenDiMuon_DPhi", 
                "ZRF_GenMuon_thetaH",

                "HiggsRF_GenTau_thetastar",
                "ZRF_GenMuon_theta2",
                "GenHiggs_GenZ_phi1", 
                "GenZ_phi", 
                "GenZ_theta2",  
                
                "FSGenMuon_plus_e",

        ]

        branchList += [
                "n_Tau23PiCandidates", "Tau23PiCandidates_mass", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",
                "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0",

                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz",
                "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz",
                "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz",
                "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",   
        ]

        return branchList