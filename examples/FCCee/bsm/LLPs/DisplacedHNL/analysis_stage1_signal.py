#Mandatory: List of processes
processList = {
        #privately-produced signals
        'HNL_4e-8_10gev':{},
        #'eenu_30GeV_1p41e-6Ve':{},
        #'eenu_50GeV_1p41e-6Ve':{},
        #'eenu_70GeV_1p41e-6Ve':{},
        #'eenu_90GeV_1p41e-6Ve':{},

        #test
        #'p8_ee_Zee_ecm91':{'fraction':0.000001},
        #'p8_ee_Zuds_ecm91':{'chunks':10,'fraction':0.000001},
}

#Production tag. This points to the yaml files for getting sample statistics
#Mandatory when running over EDM4Hep centrally produced events
#Comment out when running over privately produced events
#prodTag     = "FCCee/winter2023/IDEA/"

#Input directory
#Comment out when running over centrally produced events
#Mandatory when running over privately produced events
#inputDir = "/eos/experiment/fcc/ee/analyses/case-studies/bsm/LLPs/HNL_Majorana_eenu/spring2021/output_MadgraphPythiaDelphes"
#inputDir = "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v2"
inputDir = "/afs/cern.ch/user/s/sgiappic/"


#Optional: output directory, default is local dir
#outputDir = "/eos/experiment/fcc/ee/analyses/case-studies/bsm/LLPs/HNL_Majorana_eenu/spring2021/output_stage1/"
#outputDir = "/eos/experiment/fcc/ee/analyses/case-studies/bsm/LLPs/HNL_Majorana_eenu/pre_winter2023_tests_v2/output_stage1/"
#outputDir = "/eos/user/j/jalimena/FCCeeLLP/"
#outputDir = "output_stage1/"
outputDir = "/eos/user/s/sgiappic/test_sig/stage1/"

#outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/bsm/LLPs/HNL_Majorana_eenu/spring2021/output_stage1/"
#outputDirEos = "/eos/user/j/jalimena/FCCeeLLP/"
#eosType = "eosuser"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
        def analysers(df):

                df2 = (df

                #Access the various objects and their properties with the following syntax: .Define("<your_variable>", "<accessor_fct (name_object)>")
		#This will create a column in the RDataFrame named <your_variable> and filled with the return value of the <accessor_fct> for the given collection/object 
		#Accessor functions are the functions found in the C++ analyzers code that return a certain variable, e.g. <namespace>::get_n(object) returns the number 
		#of these objects in the event and <namespace>::get_pt(object) returns the pt of the object. Here you can pick between two namespaces to access either
		#reconstructed (namespace = ReconstructedParticle) or MC-level objects (namespace = MCParticle). 
		#For the name of the object, in principle the names of the EDM4HEP collections are used - photons, muons and electrons are an exception, see below

		#OVERVIEW: Accessing different objects and counting them
               

                # Following code is written specifically for the HNL study
                ####################################################################################################
                #.Alias("Particle1", "Particle#1.index")
                #.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                #.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 
                #all final state gen electrons and positrons
                .Define("GenElectron_PID", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenElectron", "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
                #put in dummy values below if there aren't any FSGenElectrons, to avoid seg fault
                .Define("FSGenElectron_e", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_e(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_p", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_p(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_pt", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pt(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_px", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_px(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_py", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_py(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_pz", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pz(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_eta", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_eta(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_theta", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_theta(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_phi", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_phi(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_charge", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_charge(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")

                .Define("FSGenElectron_vertex_x", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_vertex_y", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                .Define("FSGenElectron_vertex_z", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
                
                #all final state gen Muons
                .Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
                .Define("FSGenMuon", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
                #put in dummy values below if there aren't any FSGenMuons, to avoid seg fault
                .Define("FSGenMuon_e", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_e(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_p", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_p(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_pt", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pt(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_px", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_px(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_py", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_py(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_pz", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pz(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_eta", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_eta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_theta", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_theta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_phi", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_phi(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_charge", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_charge(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")

                .Define("FSGenMuon_vertex_x", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_vertex_y", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
                .Define("FSGenMuon_vertex_z", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")

                # Finding the Lxy of the HNL
                ### both leptons have the same vertex decaying from Z or W so when there are no electrons use one of the muons, when there are at least one electron use that ###
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                #.Define("FSGen_Lxy", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y)")
                .Define("FSGen_Lxy", "if (n_FSGenElectron==0) return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y); \
                                        else return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y); ")
                # Finding the Lxyz of the HNL
                #.Define("FSGen_Lxyz", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y + FSGenElectron_vertex_z*FSGenElectron_vertex_z)")
                .Define("FSGen_Lxyz", "if (n_FSGenElectron==0) return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y + FSGenMuon_vertex_z*FSGenMuon_vertex_z); \
                                        else return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y + FSGenElectron_vertex_z*FSGenElectron_vertex_z); ")

                #all final state gen neutrinos and anti-neutrinos
                .Define("GenNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(12, true)(Particle)")
                .Define("FSGenNeutrino", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutrino_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenNeutrino", "FCCAnalyses::MCParticle::get_n(FSGenNeutrino)")
                .Define("FSGenNeutrino_e", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_e(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_p", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_p(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_pt", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_pt(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_px", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_px(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_py", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_py(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_pz", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_pz(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_eta", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_eta(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_theta", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_theta(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_phi", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_phi(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")
                .Define("FSGenNeutrino_charge", "if (n_FSGenNeutrino>0) return FCCAnalyses::MCParticle::get_charge(FSGenNeutrino); else return FCCAnalyses::MCParticle::get_genStatus(GenNeutrino_PID);")

                #all final state gen photons
                .Define("GenPhoton_PID", "FCCAnalyses::MCParticle::sel_pdgID(22, false)(Particle)")
                .Define("FSGenPhoton", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenPhoton_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenPhoton", "FCCAnalyses::MCParticle::get_n(FSGenPhoton)")
                .Define("FSGenPhoton_e", "FCCAnalyses::MCParticle::get_e(FSGenPhoton)")
                .Define("FSGenPhoton_p", "FCCAnalyses::MCParticle::get_p(FSGenPhoton)")
                .Define("FSGenPhoton_pt", "FCCAnalyses::MCParticle::get_pt(FSGenPhoton)")
                .Define("FSGenPhoton_px", "FCCAnalyses::MCParticle::get_px(FSGenPhoton)")
                .Define("FSGenPhoton_py", "FCCAnalyses::MCParticle::get_py(FSGenPhoton)")
                .Define("FSGenPhoton_pz", "FCCAnalyses::MCParticle::get_pz(FSGenPhoton)")
                .Define("FSGenPhoton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenPhoton)")
                .Define("FSGenPhoton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenPhoton)")
                .Define("FSGenPhoton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenPhoton)")
                .Define("FSGenPhoton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenPhoton)")

                # ee invariant mass
                .Define("FSGen_ee_energy", "if (n_FSGenElectron>1) return (FSGenElectron_e.at(0) + FSGenElectron_e.at(1)); else return float(-1.);")
                .Define("FSGen_ee_px", "if (n_FSGenElectron>1) return (FSGenElectron_px.at(0) + FSGenElectron_px.at(1)); else return float(-1.);")
                .Define("FSGen_ee_py", "if (n_FSGenElectron>1) return (FSGenElectron_py.at(0) + FSGenElectron_py.at(1)); else return float(-1.);")
                .Define("FSGen_ee_pz", "if (n_FSGenElectron>1) return (FSGenElectron_pz.at(0) + FSGenElectron_pz.at(1)); else return float(-1.);")
                #.Define("FSGen_ee_invMass", "if (n_FSGenElectron>1) return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz ); else return float(-1.);")

                ### mumu invariant mass ###
                .Define("FSGen_mumu_energy", "if (n_FSGenMuon>1) return (FSGenMuon_e.at(0) + FSGenMuon_e.at(1)); else return float(-1.);")
                .Define("FSGen_mumu_px", "if (n_FSGenMuon>1) return (FSGenMuon_px.at(0) + FSGenMuon_px.at(1)); else return float(-1.);")
                .Define("FSGen_mumu_py", "if (n_FSGenMuon>1) return (FSGenMuon_py.at(0) + FSGenMuon_py.at(1)); else return float(-1.);")
                .Define("FSGen_mumu_pz", "if (n_FSGenMuon>1) return (FSGenMuon_pz.at(0) + FSGenMuon_pz.at(1)); else return float(-1.);")
                #.Define("FSGen_mumu_invMass", "if (n_FSGenMuon>1) return sqrt(FSGen_mumu_energy*FSGen_mumu_energy - FSGen_mumu_px*FSGen_mumu_px - FSGen_mumu_py*FSGen_mumu_py - FSGen_mumu_pz*FSGen_mumu_pz ); else return float(-1.);")

                ### emu invariant mass -> for final states with (at least) one electron and one muon ###
                .Define("FSGen_emu_energy", "if (n_FSGenElectron>0 && n_FSGenMuon>0) return (FSGenElectron_e.at(0) + FSGenMuon_e.at(0)); else return float(-1.);")
                .Define("FSGen_emu_px", "if (n_FSGenElectron>0 && n_FSGenMuon>0) return (FSGenElectron_px.at(0) + FSGenMuon_px.at(0)); else return float(-1.);")
                .Define("FSGen_emu_py", "if (n_FSGenElectron>0 && n_FSGenMuon>0) return (FSGenElectron_py.at(0) + FSGenMuon_py.at(0)); else return float(-1.);")
                .Define("FSGen_emu_pz", "if (n_FSGenElectron>0 && n_FSGenMuon>0) return (FSGenElectron_pz.at(0) + FSGenMuon_pz.at(0)); else return float(-1.);")
                #.Define("FSGen_emu_invMass", "if (n_FSGenElectron>0 && n_FSGenMuon>0) return sqrt(FSGen_emu_energy*FSGen_emu_energy - FSGen_emu_px*FSGen_emu_px - FSGen_emu_py*FSGen_emu_py - FSGen_emu_pz*FSGen_emu_pz ); else return float(-1.);")

                ### there may be events with two electrons and two muons, then both instances are true and it probably saves the second but then it's not an event we want so it doesn't matter in the end ###
                
                .Define("FSGen_invMass", "if (n_FSGenMuon>1) return sqrt(FSGen_mumu_energy*FSGen_mumu_energy - FSGen_mumu_px*FSGen_mumu_px - FSGen_mumu_py*FSGen_mumu_py - FSGen_mumu_pz*FSGen_mumu_pz ); \
                                        else if (n_FSGenElectron>1) return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz ); \
                                        else if (n_FSGenElectron>0 && n_FSGenMuon>0) return sqrt(FSGen_emu_energy*FSGen_emu_energy - FSGen_emu_px*FSGen_emu_px - FSGen_emu_py*FSGen_emu_py - FSGen_emu_pz*FSGen_emu_pz ); \
                                        else return float(-1.);")

                ### not useful for backgrounds without neutrinos in the final state as it's not a selection step anyway ###
                # eenu invariant mass
                .Define("FSGen_eenu_energy", "if (n_FSGenElectron>1 && n_FSGenNeutrino>0) return (FSGenElectron_e.at(0) + FSGenElectron_e.at(1) + FSGenNeutrino_e.at(0)); else return float(-1.);")
                .Define("FSGen_eenu_px", "if (n_FSGenElectron>1 && n_FSGenNeutrino>0) return (FSGenElectron_px.at(0) + FSGenElectron_px.at(1) + FSGenNeutrino_px.at(0)); else return float(-1.);")
                .Define("FSGen_eenu_py", "if (n_FSGenElectron>1 && n_FSGenNeutrino>0) return (FSGenElectron_py.at(0) + FSGenElectron_py.at(1) + FSGenNeutrino_py.at(0)); else return float(-1.);")
                .Define("FSGen_eenu_pz", "if (n_FSGenElectron>1 && n_FSGenNeutrino>0) return (FSGenElectron_pz.at(0) + FSGenElectron_pz.at(1) + FSGenNeutrino_pz.at(0)); else return float(-1.);")
                .Define("FSGen_eenu_invMass", "if (n_FSGenElectron>1 && n_FSGenNeutrino>0) return sqrt(FSGen_eenu_energy*FSGen_eenu_energy - FSGen_eenu_px*FSGen_eenu_px - FSGen_eenu_py*FSGen_eenu_py - FSGen_eenu_pz*FSGen_eenu_pz ); else return float(-1.);")
                
                # MC event primary vertex
                .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )



                ################### Reconstructed particles #####################
                #.Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack)")

                #JETS
                ### count how many jets are in the event in total to check, it doesn't work with this method on reclustered jets, only on the edm4hep collections Jet ###
		.Define("n_RecoJets", "ReconstructedParticle::get_n(Jet)") 

                ### Jet clustering with different algorithm ###
                .Define("RP_px", "ReconstructedParticle::get_px(ReconstructedParticles) ")
                .Define("RP_py", "ReconstructedParticle::get_py(ReconstructedParticles) ")
                .Define("RP_pz", "ReconstructedParticle::get_pz(ReconstructedParticles) ")
                .Define("RP_e", "ReconstructedParticle::get_e(ReconstructedParticles) ")

                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets",  "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)" )

                # run jet clustering with all reconstructed particles. 
                ### Durham algo, exclusive clustering (first number 2) N_jets=0 (second number), E-scheme=0 (third and forth numbers) ###
                .Define( "FCCAnalysesJets_ee_genkt",  "JetClustering::clustering_ee_kt(2, 0, 1, 0)(pseudo_jets)" )
                .Define("jets_ee_genkt",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_ee_genkt )")

                ### in our case with 0 jets all jet variables are useless, try one just to check ###
                # access the jets kinematics :
                .Define("jets_e",  "JetClusteringUtils::get_e(jets_ee_genkt)")
                        
                # access the jet constituents:
                #.Define("jetconstituents_ee_genkt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt) ")
                                
                # access the "dmerge" distances:
                #.Define("dmerge_23", "JetClusteringUtils::get_exclusive_dmerge( FCCAnalysesJets, 2)" )

		#PHOTONS
	        .Alias("Photon", "Photon_objIdx.index") 
		.Define("RecoPhotons",  "ReconstructedParticle::get(Photon, ReconstructedParticles)")
		.Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total

		#ELECTRONS AND MUONS
		.Alias("Electron", "Electron_objIdx.index")
		.Define("RecoElectrons",  "ReconstructedParticle::get(Electron, ReconstructedParticles)")
		.Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total

		.Alias("Muon", "Muon_objIdx.index")
		.Define("RecoMuons",  "ReconstructedParticle::get(Muon, ReconstructedParticles)")
		.Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total

                #SIMPLE VARIABLES: Access the basic kinematic variables of the (selected) jets, works analogously for electrons, muons
		#.Define("RecoJet_e",      "ReconstructedParticle::get_e(Jet)")
                #.Define("RecoJet_p",      "ReconstructedParticle::get_p(Jet)") #momentum p
                #.Define("RecoJet_pt",      "ReconstructedParticle::get_pt(Jet)") #transverse momentum pt
                #.Define("RecoJet_px",      "ReconstructedParticle::get_px(Jet)")
                #.Define("RecoJet_py",      "ReconstructedParticle::get_py(Jet)")
                #.Define("RecoJet_pz",      "ReconstructedParticle::get_pz(Jet)")
		#.Define("RecoJet_eta",     "ReconstructedParticle::get_eta(Jet)") #pseudorapidity eta
                #.Define("RecoJet_theta",   "ReconstructedParticle::get_theta(Jet)")
		#.Define("RecoJet_phi",     "ReconstructedParticle::get_phi(Jet)") #polar angle in the transverse plane phi
                #.Define("RecoJet_charge",  "ReconstructedParticle::get_charge(Jet)")
                #.Define("RecoJetTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(Jet,EFlowTrack))")
                #.Define("RecoJetTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(Jet,EFlowTrack))")
                #.Define("RecoJetTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(Jet,EFlowTrack))") #significance
                #.Define("RecoJetTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(Jet,EFlowTrack))")
                #.Define("RecoJetTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(Jet,EFlowTrack)") #variance (not sigma)
                #.Define("RecoJetTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(Jet,EFlowTrack)")

                .Define("RecoElectron_e",      "ReconstructedParticle::get_e(RecoElectrons)")
                .Define("RecoElectron_p",      "ReconstructedParticle::get_p(RecoElectrons)")
                .Define("RecoElectron_pt",      "ReconstructedParticle::get_pt(RecoElectrons)")
                .Define("RecoElectron_px",      "ReconstructedParticle::get_px(RecoElectrons)")
                .Define("RecoElectron_py",      "ReconstructedParticle::get_py(RecoElectrons)")
                .Define("RecoElectron_pz",      "ReconstructedParticle::get_pz(RecoElectrons)")
		.Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
		.Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                #.Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack))")
                #.Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack))")
                #.Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack))") #significance
                #.Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack))")
                #.Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack)") #variance (not sigma)
                #.Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack)")

                .Define("RecoPhoton_e",      "ReconstructedParticle::get_e(RecoPhotons)")
                .Define("RecoPhoton_p",      "ReconstructedParticle::get_p(RecoPhotons)")
                .Define("RecoPhoton_pt",      "ReconstructedParticle::get_pt(RecoPhotons)")
                .Define("RecoPhoton_px",      "ReconstructedParticle::get_px(RecoPhotons)")
                .Define("RecoPhoton_py",      "ReconstructedParticle::get_py(RecoPhotons)")
                .Define("RecoPhoton_pz",      "ReconstructedParticle::get_pz(RecoPhotons)")
		.Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
                .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		.Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
                .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")

                .Define("RecoMuon_e",      "ReconstructedParticle::get_e(RecoMuons)")
                .Define("RecoMuon_p",      "ReconstructedParticle::get_p(RecoMuons)")
                .Define("RecoMuon_pt",      "ReconstructedParticle::get_pt(RecoMuons)")
                .Define("RecoMuon_px",      "ReconstructedParticle::get_px(RecoMuons)")
                .Define("RecoMuon_py",      "ReconstructedParticle::get_py(RecoMuons)")
                .Define("RecoMuon_pz",      "ReconstructedParticle::get_pz(RecoMuons)")
		.Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
		.Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                #.Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack))")
                #.Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack))")
                #.Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack))") #significance
                #.Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack))")
                #.Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack)") #variance (not sigma)
                #.Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack)")
                
                ### cosine between two leptons ###
                .Define("Reco_ee_p", "if (n_RecoElectrons>1) return (RecoElectron_px.at(0)*RecoElectron_px.at(1) + RecoElectron_py.at(0)*RecoElectron_py.at(1) + RecoElectron_pz.at(0)*RecoElectron_pz.at(1)); else return float(-2.);")
                .Define("Reco_mumu_p", "if (n_RecoMuons>1) return (RecoMuon_px.at(0)*RecoMuon_px.at(1) + RecoMuon_py.at(0)*RecoMuon_py.at(1) + RecoMuon_pz.at(0)*RecoMuon_pz.at(1)); else return float(-2.);")
                .Define("Reco_emu_p", "if (n_RecoMuons>0 && n_RecoElectrons>0) return (RecoElectron_px.at(0)*RecoMuon_px.at(0) + RecoElectron_py.at(0)*RecoMuon_py.at(0) + RecoElectron_pz.at(0)*RecoMuon_pz.at(0)); else return float(-2.);")
           
                #.Define("Reco_ee_cos", "if (n_RecoElectrons>1) return (Reco_ee_p/(RecoElectron_p.at(0)*RecoElectron_p.at(1))); else return float(-2.);")
                #.Define("Reco_mumu_cos", "if (n_RecoMuons>1) return (Reco_mumu_p/(RecoMuon_p.at(0)*RecoMuon_p.at(1))); else return float(-2.);")
                #.Define("Reco_emu_cos", "if (n_RecoMuons>0 && n_RecoElectrons>0) return (Reco_emu_p/(RecoMuon_p.at(0)*RecoElectron_p.at(0))); else return float(-2.);")
                .Define("Reco_cos", "if (n_RecoMuons>1) return (Reco_mumu_p/(RecoMuon_p.at(0)*RecoMuon_p.at(1))); \
                                        else if (n_RecoElectrons>1) return (Reco_ee_p/(RecoElectron_p.at(0)*RecoElectron_p.at(1))); \
                                        else if (n_RecoMuons>0 && n_RecoElectrons>0) return (Reco_emu_p/(RecoMuon_p.at(0)*RecoElectron_p.at(0))); \
                                        else return float(-2.);")

                ### angular distance between two leptons ###
                #.Define("Reco_ee_DR", "if (n_RecoElectrons>1) return sqrt((RecoElectron_phi.at(0) - RecoElectron_phi.at(1))*(RecoElectron_phi.at(0) - RecoElectron_phi.at(1)) + (RecoElectron_eta.at(0) - RecoElectron_eta.at(1))*(RecoElectron_eta.at(0) - RecoElectron_eta.at(1))); else return float(-1.);")
                #.Define("Reco_mumu_DR", "if (n_RecoMuons>1) return sqrt((RecoMuon_phi.at(0) - RecoMuon_phi.at(1))*(RecoMuon_phi.at(0) - RecoMuon_phi.at(1)) + (RecoMuon_eta.at(0) - RecoMuon_eta.at(1))*(RecoMuon_eta.at(0) - RecoMuon_eta.at(1))); else return float(-1.);")
                #.Define("Reco_emu_DR", "if (n_RecoMuons>0 && n_RecoElectrons>0) return sqrt((RecoElectron_phi.at(0) - RecoMuon_phi.at(0))*(RecoElectron_phi.at(0) - RecoMuon_phi.at(0)) + (RecoElectron_eta.at(0) - RecoMuon_eta.at(0))*(RecoElectron_eta.at(0) - RecoMuon_eta.at(0))); else return float(-1.);")
                .Define("Reco_DR","if (n_RecoMuons>1) return sqrt((RecoMuon_phi.at(0) - RecoMuon_phi.at(1))*(RecoMuon_phi.at(0) - RecoMuon_phi.at(1)) + (RecoMuon_eta.at(0) - RecoMuon_eta.at(1))*(RecoMuon_eta.at(0) - RecoMuon_eta.at(1))); \
                                        else if (n_RecoElectrons>1) return sqrt((RecoElectron_phi.at(0) - RecoElectron_phi.at(1))*(RecoElectron_phi.at(0) - RecoElectron_phi.at(1)) + (RecoElectron_eta.at(0) - RecoElectron_eta.at(1))*(RecoElectron_eta.at(0) - RecoElectron_eta.at(1))); \
                                        else if (n_RecoMuons>0 && n_RecoElectrons>0) return sqrt((RecoElectron_phi.at(0) - RecoMuon_phi.at(0))*(RecoElectron_phi.at(0) - RecoMuon_phi.at(0)) + (RecoElectron_eta.at(0) - RecoMuon_eta.at(0))*(RecoElectron_eta.at(0) - RecoMuon_eta.at(0))); \
                                        else return float(-1.);")

                # Now we reconstruct the reco decay vertex using the reco'ed tracks from electrons and muons
                #.Define("RecoElectronTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoElectrons, EFlowTrack)") ### EFlowTrack contains all tracks ###
                #.Define("RecoMuonTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoMuons, EFlowTrack)")

                # First the full object, of type Vertexing::FCCAnalysesVertex
                #.Define("RecoDecayVertexObjectElectron",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoElectronTracks)" ) ### 1 = primary vertex, 2 = secondary vertex ###
                #.Define("RecoDecayVertexObjectMuon",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoMuonTracks)" ) ### necessary when there are no electrons present, otherwise one electron track is sufficient ###

                # from which we extract the edm4hep::VertexData object, which contains the vertex position in mm
                #.Define("RecoDecayVertexElectron",  "VertexingUtils::get_VertexData( RecoDecayVertexObjectElectron )")
                #.Define("RecoDecayVertexMuon",  "VertexingUtils::get_VertexData( RecoDecayVertexObjectMuon )")

                ### same definition that gen distance but with reco objects ###
                #.Define("Reco_Lxy", "if (n_RecoMuons>1) return sqrt(RecoDecayVertexMuon.position.x*RecoDecayVertexMuon.position.x + RecoDecayVertexMuon.position.y*RecoDecayVertexMuon.position.y); \
                                        #else if (n_RecoElectrons>1) return sqrt(RecoDecayVertexElectron.position.x*RecoDecayVertexElectron.position.x + RecoDecayVertexElectron.position.y*RecoDecayVertexElectron.position.y); \
                                        #else if (n_RecoElectrons>0 && n_RecoMuons>0) return sqrt(RecoDecayVertexElectron.position.x*RecoDecayVertexElectron.position.x + RecoDecayVertexElectron.position.y*RecoDecayVertexElectron.position.y); \
                                        #else return float(-1.);")
                #.Define("Reco_Lxyz","if (n_RecoMuons>1) return sqrt(RecoDecayVertexMuon.position.x*RecoDecayVertexMuon.position.x + RecoDecayVertexMuon.position.y*RecoDecayVertexMuon.position.y + RecoDecayVertexMuon.position.z*RecoDecayVertexMuon.position.z); \
                                        #else if (n_RecoElectrons>1) return sqrt(RecoDecayVertexElectron.position.x*RecoDecayVertexElectron.position.x + RecoDecayVertexElectron.position.y*RecoDecayVertexElectron.position.y + RecoDecayVertexElectron.position.z*RecoDecayVertexElectron.position.z); \
                                        #else if (n_RecoElectrons>0 && n_RecoMuons>0) return sqrt(RecoDecayVertexMuon.position.x*RecoDecayVertexMuon.position.x + RecoDecayVertexMuon.position.y*RecoDecayVertexMuon.position.y + RecoDecayVertexMuon.position.z*RecoDecayVertexMuon.position.z); \
                                        #else return float(-1.);")

                #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
		#.Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
		# .Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
		#.Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
		#.Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
		#.Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
		#.Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
		#.Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
		#.Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
		#.Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy

                # ee invariant mass
                .Define("Reco_ee_energy", "if (n_RecoElectrons>1) return (RecoElectron_e.at(0) + RecoElectron_e.at(1)); else return float(-1.);")
                .Define("Reco_ee_px", "if (n_RecoElectrons>1) return (RecoElectron_px.at(0) + RecoElectron_px.at(1)); else return float(-1.);")
                .Define("Reco_ee_py", "if (n_RecoElectrons>1) return (RecoElectron_py.at(0) + RecoElectron_py.at(1)); else return float(-1.);")
                .Define("Reco_ee_pz", "if (n_RecoElectrons>1) return (RecoElectron_pz.at(0) + RecoElectron_pz.at(1)); else return float(-1.);")
                #.Define("Reco_ee_invMass", "if (n_RecoElectrons>1) return sqrt(Reco_ee_energy*Reco_ee_energy - Reco_ee_px*Reco_ee_px - Reco_ee_py*Reco_ee_py - Reco_ee_pz*Reco_ee_pz ); else return float(-1.);")

                ### mumu invariant mass ###
                .Define("Reco_mumu_energy", "if (n_RecoMuons>1) return (RecoMuon_e.at(0) + RecoMuon_e.at(1)); else return float(-1.);")
                .Define("Reco_mumu_px", "if (n_RecoMuons>1) return (RecoMuon_px.at(0) + RecoMuon_px.at(1)); else return float(-1.);")
                .Define("Reco_mumu_py", "if (n_RecoMuons>1) return (RecoMuon_py.at(0) + RecoMuon_py.at(1)); else return float(-1.);")
                .Define("Reco_mumu_pz", "if (n_RecoMuons>1) return (RecoMuon_pz.at(0) + RecoMuon_pz.at(1)); else return float(-1.);")
                #.Define("Reco_mumu_invMass", "if (n_RecoMuons>1) return sqrt(Reco_mumu_energy*Reco_mumu_energy - Reco_mumu_px*Reco_mumu_px - Reco_mumu_py*Reco_mumu_py - Reco_mumu_pz*Reco_mumu_pz ); else return float(-1.);")

                ### emu invariant mass ###
                .Define("Reco_emu_energy", "if (n_RecoElectrons>0 && n_RecoMuons>0) return (RecoElectron_e.at(0) + RecoMuon_e.at(0)); else return float(-1.);")
                .Define("Reco_emu_px", "if (n_RecoElectrons>0 && n_RecoMuons>0) return (RecoElectron_px.at(0) + RecoMuon_px.at(0)); else return float(-1.);")
                .Define("Reco_emu_py", "if (n_RecoElectrons>0 && n_RecoMuons>0) return (RecoElectron_py.at(0) + RecoMuon_py.at(0)); else return float(-1.);")
                .Define("Reco_emu_pz", "if (n_RecoElectrons>0 && n_RecoMuons>0) return (RecoElectron_pz.at(0) + RecoMuon_pz.at(0)); else return float(-1.);")
                #.Define("Reco_emu_invMass", "if (n_RecoElectrons>0 && n_RecoMuons>0) return sqrt(Reco_emu_energy*Reco_emu_energy - Reco_emu_px*Reco_emu_px - Reco_emu_py*Reco_emu_py - Reco_emu_pz*Reco_emu_pz ); else return float(-1.);")

                .Define("Reco_invMass", "if (n_RecoMuons>1) return sqrt(Reco_mumu_energy*Reco_mumu_energy - Reco_mumu_px*Reco_mumu_px - Reco_mumu_py*Reco_mumu_py - Reco_mumu_pz*Reco_mumu_pz ); \
                                        else if (n_RecoElectrons>1) return sqrt(Reco_ee_energy*Reco_ee_energy - Reco_ee_px*Reco_ee_px - Reco_ee_py*Reco_ee_py - Reco_ee_pz*Reco_ee_pz ); \
                                        else if (n_RecoElectrons>0 && n_RecoMuons>0) return sqrt(Reco_emu_energy*Reco_emu_energy - Reco_emu_px*Reco_emu_px - Reco_emu_py*Reco_emu_py - Reco_emu_pz*Reco_emu_pz ); \
                                        else return float(-1.);")

               )
                return df2

        def output():
                branchList = [
                        ######## Monte-Carlo particles #######
                        "n_FSGenElectron",
                        "FSGenElectron_e",
                        "FSGenElectron_p",
                        "FSGenElectron_pt",
                        "FSGenElectron_px",
                        "FSGenElectron_py",
                        "FSGenElectron_pz",
                        "FSGenElectron_eta",
                        "FSGenElectron_theta",
                        "FSGenElectron_phi",
                        "FSGenElectron_charge",
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
                        "FSGenMuon_eta",
                        "FSGenMuon_theta",
                        "FSGenMuon_phi",
                        "FSGenMuon_charge",
                        "FSGenMuon_vertex_x",
                        "FSGenMuon_vertex_y",
                        "FSGenMuon_vertex_z",

                        "FSGen_Lxy",
                        "FSGen_Lxyz",
                        #"FSGen_ee_invMass",
                        #"FSGen_eenu_invMass",
                        #"FSGen_mumu_invMass",
                        #"FSGen_emu_invMass",
                        "FSGen_invMass",

                        "n_FSGenNeutrino",
                        "FSGenNeutrino_e",
                        "FSGenNeutrino_p",
                        "FSGenNeutrino_pt",
                        "FSGenNeutrino_px",
                        "FSGenNeutrino_py",
                        "FSGenNeutrino_pz",
                        "FSGenNeutrino_eta",
                        "FSGenNeutrino_theta",
                        "FSGenNeutrino_phi",
                        "FSGenNeutrino_charge",

                        #"n_FSGenPhoton",
                        #"FSGenPhoton_e",
                        #"FSGenPhoton_p",
                        #"FSGenPhoton_pt",
                        #"FSGenPhoton_px",
                        #"FSGenPhoton_py",
                        #"FSGenPhoton_pz",
                        #"FSGenPhoton_eta",
                        #"FSGenPhoton_theta",
                        #"FSGenPhoton_phi",
                        #"FSGenPhoton_charge",

                        ######## Reconstructed particles #######
                        #"n_RecoTracks",
                        "n_RecoJets",
                        "n_RecoPhotons",
                        "n_RecoElectrons",
                        "n_RecoMuons",

                        #"jets_e",
                        #"RecoJet_e",
                        #"RecoJet_p",
                        #"RecoJet_pt",
                        #"RecoJet_px",
                        #"RecoJet_py",
                        #"RecoJet_pz",
                        #"RecoJet_eta",
                        #"RecoJet_theta",
                        #"RecoJet_phi",
                        #"RecoJet_charge",
                        #"RecoJetTrack_absD0",
                        #"RecoJetTrack_absZ0",
                        #"RecoJetTrack_absD0sig",
                        #"RecoJetTrack_absZ0sig",
                        #"RecoJetTrack_D0cov",
                        #"RecoJetTrack_Z0cov",

                        #"RecoPhoton_e",
                        #"RecoPhoton_p",
                        #"RecoPhoton_pt",
                        #"RecoPhoton_px",
                        #"RecoPhoton_py",
                        #"RecoPhoton_pz",
                        #"RecoPhoton_eta",
                        #"RecoPhoton_theta",
                        #"RecoPhoton_phi",
                        #"RecoPhoton_charge",

                        "RecoElectron_e",
                        "RecoElectron_p",
                        "RecoElectron_pt",
                        "RecoElectron_px",
                        "RecoElectron_py",
                        "RecoElectron_pz",
                        "RecoElectron_eta",
                        "RecoElectron_theta",
                        "RecoElectron_phi",
                        "RecoElectron_charge",
                        #"RecoElectronTrack_absD0",
                        #"RecoElectronTrack_absZ0",
                        #"RecoElectronTrack_absD0sig",
                        #"RecoElectronTrack_absZ0sig",
                        #"RecoElectronTrack_D0cov",
                        #"RecoElectronTrack_Z0cov",
                        #"RecoDecayVertexObjectElectron",
                        #"RecoDecayVertexObjectMuon",
                        #"RecoDecayVertexElectron",
                        #"RecoDecayVertexMuon",

                        #"Reco_Lxy",
                        #"Reco_Lxyz",

                        "RecoMuon_e",
                        "RecoMuon_p",
                        "RecoMuon_pt",
                        "RecoMuon_px",
                        "RecoMuon_py",
                        "RecoMuon_pz",
                        "RecoMuon_eta",
                        "RecoMuon_theta",
                        "RecoMuon_phi",
                        "RecoMuon_charge",
                        #"RecoMuonTrack_absD0",
                        #"RecoMuonTrack_absZ0",
                        #"RecoMuonTrack_absD0sig",
                        #"RecoMuonTrack_absZ0sig",
                        #"RecoMuonTrack_D0cov",
                        #"RecoMuonTrack_Z0cov", 

                        #"RecoMissingEnergy_e",
                        #"RecoMissingEnergy_p",
                        #"RecoMissingEnergy_pt",
                        #"RecoMissingEnergy_px",
                        #"RecoMissingEnergy_py",
                        #"RecoMissingEnergy_pz",
                        #"RecoMissingEnergy_eta",
                        #"RecoMissingEnergy_theta",
                        #"RecoMissingEnergy_phi",

                        # enunu branches
                        #"Reco_ee_invMass",
                        #"Reco_mumu_invMass",
                        #"Reco_emu_invMass",
                        "Reco_invMass",

                        #"Reco_ee_cos",
                        #"Reco_mumu_cos",
                        #"Reco_emu_cos",
                        "Reco_cos",

                        #"Reco_ee_DR",
                        #"Reco_mumu_DR",
                        #"Reco_emu_DR",
                        "Reco_DR",

		]

                return branchList
