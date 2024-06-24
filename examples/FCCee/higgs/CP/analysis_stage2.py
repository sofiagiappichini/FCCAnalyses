import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10}, #check that it's fine to keep them in chunks, otherwise just remove the option and leave {},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Huu_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hdd_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hmumu_ecm240': {'chunks':10},
}

inputDir = "/ceph/sgiappic/HiggsCP/stage1"

#Optional: output directory, default is local running directory
outputDir   = "//" #your output directory

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
            .Filter("n_GenTau==2")
            
            .Define("GenTau_Lxyz", "return sqrt(GenTau_vertex_x.at(0)*GenTau_vertex_x.at(0) + GenTau_vertex_y.at(0)*GenTau_vertex_y.at(0) + GenTau_vertex_z.at(0)*GenTau_vertex_z.at(0))") #in mm
    
            # tautau invariant mass
            .Define("GenDiTau_energy", "if (n_GenTau>1) return (GenTau_e.at(0) + GenTau_e.at(1)); else return float(-1.);")
            .Define("GenDiTau_px", "if (n_GenTau>1) return (GenTau_px.at(0) + GenTau_px.at(1)); else return float(-1.);")
            .Define("GenDiTau_py", "if (n_GenTau>1) return (GenTau_py.at(0) + GenTau_py.at(1)); else return float(-1.);")
            .Define("GenDiTau_pz", "if (n_GenTau>1) return (GenTau_pz.at(0) + GenTau_pz.at(1)); else return float(-1.);")
            .Define("GenDiTau_invMass", "if (n_GenTai>1) return sqrt(GenDiTau_energy*GenDiTau_energy - GenDiTau_px*GenDiTau_px - GenDiTau_py*GenDiTau_py - GenDiTau_pz*GenDiTau_pz ); else return float(-1.);")
            
            # cosine between two leptons, in lab frame
            .Define("GenDiTau_p", "if (n_GenTau>1) return sqrt(GenDiTau_px*GenDiTau_px + GenDiTau_py*GenDiTau_py + GenDiTau_pz*GenDiTau_pz); else return float(-1.);")
            .Define("GenDiTau_scalar", "if (n_GenTau>1) return (GenTau_px.at(0)*GenTau_px.at(1) + GenTau_py.at(0)*GenTau_py.at(1) + GenTau_pz.at(0)*GenTau_pz.at(1)); else return float(-1.);")
            .Define("GenDiTau_cos", "if (n_GenTau>1) return (GenDiTau_scalar/(GenTau_p.at(0)*GenTau_p.at(1))); else return float(-2.);")

            # angular distance between two leptons, in lab frame
            .Define("GenDiTau_eta","if (n_GenTau>1>1) return myUtils::deltaEta(GenTau_eta.at(0), GenTau_eta.at(1)); else return float(-10.);")
            .Define("GenDiTau_phi","if (n_GenTau>1>1) return myUtils::deltaPhi(GenTau_phi.at(0), GenTau_phi.at(1)); else return float(-10.);")
            .Define("GenDiTau_DR","if (n_GenTau>1>1) return myUtils::deltaR(GenTau_phi.at(0), GenTau_phi.at(1), GenTau_eta.at(0), GenTau_eta.at(1)); else return float(-1.);")

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
                "GenTau_Lxyz",
                "GenDiTau_invMass",
                "GenDiTau_cos",
                "GenDiTau_DR",

                ######## Reconstructed particles #######
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