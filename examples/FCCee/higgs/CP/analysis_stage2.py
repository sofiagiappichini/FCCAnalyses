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
            .Define("HiggsRF_GenTau_thetaH",      "return acos(myUtils::get_scalar(ROOT::VecOps::RVec<TLorentzVector>{GenHiggs_p4.at(0)}, ROOT::VecOps::RVec<TLorentzVector>{HiggsRF_GenTau_p4.at(0)})/(GenHiggs_p.at(0)*HiggsRF_GenTau_p.at(0)))")

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
        branchList = [
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
                "HiggsRF_GenTau_thetaH",

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