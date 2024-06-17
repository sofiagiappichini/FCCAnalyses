import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Huu_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hdd_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hmumu_ecm240': {'chunks':10},
}

inputDir = "//"

#Optional: output directory, default is local running directory
outputDir   = "/eos/user/sgiappic/HiggsCP/stage1/"

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional: ncpus, default is 4
nCPUS = 10

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
                .Filter("n_GenTaus==0")
                #.Filter("n_GenPions>0 || n_GenKLs>0 || n_GenKpluss>0")
                
                .Define("GenN_Lxyz", "return sqrt(GenN_vertex_x*GenN_vertex_x + GenN_vertex_y*GenN_vertex_y + GenN_vertex_z*GenN_vertex_z)") #in mm
                
                # use the time of creation fo the leptons to get the lifetime of the HNL 
                .Define("GenN_tau", "return (FSGenLepton_time * GenN_e.at(0) / GenN_mass.at(0)) ") #tau of HNLs in s
        
                # ee invariant mass
                .Define("FSGen_TwoLeptons_energy", "if (n_FSGenLepton>1) return (FSGenLepton_e.at(0) + FSGenLepton_e.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_px", "if (n_FSGenLepton>1) return (FSGenLepton_px.at(0) + FSGenLepton_px.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_py", "if (n_FSGenLepton>1) return (FSGenLepton_py.at(0) + FSGenLepton_py.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_pz", "if (n_FSGenLepton>1) return (FSGenLepton_pz.at(0) + FSGenLepton_pz.at(1)); else return float(-1.);")
                .Define("FSGen_invMass", "if (n_FSGenLepton>1) return sqrt(FSGen_TwoLeptons_energy*FSGen_TwoLeptons_energy - FSGen_TwoLeptons_px*FSGen_TwoLeptons_px - FSGen_TwoLeptons_py*FSGen_TwoLeptons_py - FSGen_TwoLeptons_pz*FSGen_TwoLeptons_pz ); else return float(-1.);")

                ##################
                # Reco particles #
                ##################
                
                # dilepton invariant mass 
                .Define("Reco_TwoLeptons_energy", "if (n_RecoLeptons>1) return (Reco_e.at(0) + Reco_e.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_px", "if (n_RecoLeptons>1) return (Reco_px.at(0) + Reco_px.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_py", "if (n_RecoLeptons>1) return (Reco_py.at(0) + Reco_py.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_pz", "if (n_RecoLeptons>1) return (Reco_pz.at(0) + Reco_pz.at(1)); else return float(-1.);")
                .Define("Reco_invMass", "if (n_RecoLeptons>1) return sqrt(Reco_TwoLeptons_energy*Reco_TwoLeptons_energy - Reco_TwoLeptons_px*Reco_TwoLeptons_px - Reco_TwoLeptons_py*Reco_TwoLeptons_py - Reco_TwoLeptons_pz*Reco_TwoLeptons_pz ); else return float(-1.);")

                # cosine between two leptons
                .Define("Reco_TwoLeptons_p", "if (n_RecoLeptons>1) return (Reco_px.at(0)*Reco_px.at(1) + Reco_py.at(0)*Reco_py.at(1) + Reco_pz.at(0)*Reco_pz.at(1)); else return float(-2.);")
                .Define("Reco_cos", "if (n_RecoLeptons>1) return (Reco_TwoLeptons_p/(Reco_p.at(0)*Reco_p.at(1))); else return float(-2.);")

                # angular distance between two leptons 
                .Define("Reco_DR","if (n_RecoLeptons>1) return myUtils::deltaR(Reco_phi.at(0), Reco_phi.at(1), Reco_eta.at(0), Reco_eta.at(1)); else return float(-1.);")

               )
                return df2

#__________________________________________________________
#Mandatory: output function, please make sure you return the branchlist as a python list
def output():
    branchList = [
            ######## Monte-Carlo particles #######
            "FSGen_invMass",

            ######## Reconstructed particles #######
            "Reco_invMass",
            "Reco_cos",
            "Reco_DR",
                ]
    return branchList