import ROOT

#Mandatory: List of processes
processList = {

        #centrally-produced backgrounds
        #'p8_ee_Zee_ecm91':{'chunks':100},
        #'p8_ee_Zmumu_ecm91':{'chunks':100},
        #'p8_ee_Ztautau_ecm91':{'chunks':100},
        'p8_ee_Zbb_ecm91':{'chunks':100},
        'p8_ee_Zcc_ecm91':{'chunks':100},
        #'p8_ee_Zud_ecm91':{'chunks':100},
        #'p8_ee_Zss_ecm91':{'chunks':100},

        #'emununu':{},
        #'tatanunu':{},

        #privately-produced signals
        #'HNL_4e-8_10gev':{},
        #'HNL_1.33e-9_20gev':{},
        #'HNL_2.86e-12_30gev':{},
        #'HNL_2.86e-7_30gev':{},
        #'HNL_5e-12_40gev':{},
        #'HNL_4e-12_50gev':{},
        #'HNL_6.67e-8_60gev':{},
        #'HNL_4e-8_60gev':{},
        #'HNL_2.86e-9_70gev':{},
        #'HNL_2.86e-8_80gev':{},

        #'HNL_4e-10_10gev':{},
        #'HNL_4e-10_20gev':{},
        #'HNL_4e-10_30gev':{},
        #'HNL_4e-10_40gev':{},
        #'HNL_4e-10_50gev':{},
        #'HNL_4e-10_60gev':{},
        #'HNL_4e-10_70gev':{},
        #'HNL_4e-10_80gev':{},

        #'HNL_1.33e-7_10gev':{},
        #'HNL_1.33e-7_20gev':{},
        #'HNL_1.33e-7_30gev':{},
        #'HNL_1.33e-7_40gev':{},
        #'HNL_1.33e-7_50gev':{},
        #'HNL_1.33e-7_60gev':{},
        #'HNL_1.33e-7_70gev':{},
        #'HNL_1.33e-7_80gev':{},

        #'HNL_2.86e-12_10gev':{},
        #'HNL_2.86e-12_20gev':{},
        #'HNL_2.86e-12_30gev':{},
        #'HNL_2.86e-12_40gev':{},
        #'HNL_2.86e-12_50gev':{},
        #'HNL_2.86e-12_60gev':{},
        #'HNL_2.86e-12_70gev':{},
        #'HNL_2.86e-12_80gev':{},

        #'HNL_5e-12_10gev':{},
        #'HNL_5e-12_20gev':{},
        #'HNL_5e-12_30gev':{},
        #'HNL_5e-12_40gev':{},
        #'HNL_5e-12_50gev':{},
        #'HNL_5e-12_60gev':{},
        #'HNL_5e-12_70gev':{},
        #'HNL_5e-12_80gev':{},

        #'HNL_6.67e-10_10gev':{},
        #'HNL_6.67e-10_20gev':{},
        #'HNL_6.67e-10_30gev':{},
        #'HNL_6.67e-10_40gev':{},
        #'HNL_6.67e-10_50gev':{},
        #'HNL_6.67e-10_60gev':{},
        #'HNL_6.67e-10_70gev':{},
        #'HNL_6.67e-10_80gev':{},

        #'HNL_2.86e-7_10gev':{},
        #'HNL_2.86e-7_20gev':{},
        #'HNL_2.86e-7_30gev':{},
        #'HNL_2.86e-7_40gev':{},
        #'HNL_2.86e-7_50gev':{},
        #'HNL_2.86e-7_60gev':{},
        #'HNL_2.86e-7_70gev':{},
        #'HNL_2.86e-7_80gev':{},
}

#Production tag. This points to the yaml files for getting sample statistics
#Mandatory when running over EDM4Hep centrally produced events
#Comment out when running over privately produced events
prodTag     = "FCCee/winter2023/IDEA/"

#Input directory
#Comment out when running over centrally produced events
#Mandatory when running over privately produced events
#inputDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
#inputDir = "/eos/user/s/sgiappic/2HNL_samples/root/"


#Optional: output directory, default is local dir
#outputDir = "output_stage1/"
outputDir = "/eos/user/s/sgiappic/2HNL_ana/stage1/"

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional: ncpus, default is 4
nCPUS = 10

#Optional running on HTCondor, default is False
runBatch = True

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "tomorrow"

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
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 
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

                ### merging electrons and muons ###
                .Define("FSGenLepton", "FCCAnalyses::MCParticle::mergeParticles(FSGenElectron, FSGenMuon)") 
                .Define("n_FSGenLepton", "FCCAnalyses::MCParticle::get_n(FSGenLepton)")
                #put in dummy values below if there aren't any FSGenMuons, to avoid seg fault
                .Define("FSGenLepton_e", "FCCAnalyses::MCParticle::get_e(FSGenLepton)")
                .Define("FSGenLepton_p", "FCCAnalyses::MCParticle::get_p(FSGenLepton)")
                .Define("FSGenLepton_pt", "FCCAnalyses::MCParticle::get_pt(FSGenLepton)")
                .Define("FSGenLepton_px", "FCCAnalyses::MCParticle::get_px(FSGenLepton)")
                .Define("FSGenLepton_py", "FCCAnalyses::MCParticle::get_py(FSGenLepton)")
                .Define("FSGenLepton_pz", "FCCAnalyses::MCParticle::get_pz(FSGenLepton)")
                .Define("FSGenLepton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenLepton)")
                .Define("FSGenLepton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenLepton)")
                .Define("FSGenLepton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenLepton)")
                .Define("FSGenLepton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenLepton)")
                .Define("FSGenLepton_time", "FCCAnalyses::MCParticle::get_time(FSGenLepton)") #creation time in s

                .Define("FSGenLepton_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x(FSGenLepton)")
                .Define("FSGenLepton_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y(FSGenLepton)")
                .Define("FSGenLepton_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z(FSGenLepton)")

                # Finding the Lxy of the HNL
                ### both leptons have the same vertex decaying from Z or W so when there are no electrons use one of the muons, when there are at least one electron use that ###
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                .Define("FSGen_Lxy", "return sqrt(FSGenLepton_vertex_x*FSGenLepton_vertex_x + FSGenLepton_vertex_y*FSGenLepton_vertex_y)")
                # Finding the Lxyz of the HNL
                .Define("FSGen_Lxyz", "return sqrt(FSGenLepton_vertex_x*FSGenLepton_vertex_x + FSGenLepton_vertex_y*FSGenLepton_vertex_y + FSGenLepton_vertex_z*FSGenLepton_vertex_z)")
                
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

                ### Gen HNLs, merged the two ###
                .Define("GenN1_PID", "FCCAnalyses::MCParticle::sel_pdgID(9900012, true)(Particle)") #true to include charge conjugate
                .Define("GenN2_PID", "FCCAnalyses::MCParticle::sel_pdgID(9900014, true)(Particle)") #true to include charge conjugate
                .Define("GenN", "FCCAnalyses::MCParticle::mergeParticles(GenN1_PID, GenN2_PID)") 
                .Define("GenN_status", "FCCAnalyses::MCParticle::get_genStatus(GenN)") 
                .Define("n_GenN", "FCCAnalyses::MCParticle::get_n(GenN)")
                .Define("GenN_e", "FCCAnalyses::MCParticle::get_e(GenN)")
                .Define("GenN_p", "FCCAnalyses::MCParticle::get_p(GenN)")
                .Define("GenN_mass", "FCCAnalyses::MCParticle::get_mass(GenN)")

                ### definetly overkill for this study, gets the associated daugthers and then their vertex ###
                .Define("GenN1_indices", "MCParticle::get_indices( 9900012, {}, false, true, true, true) ( Particle, Particle1)" )
                .Define("GenN2_indices", "MCParticle::get_indices( 9900014, {}, false, true, true, true) ( Particle, Particle1)" )
                .Define("GenN1_dec", "FCCAnalyses::MCParticle::get_list_of_stable_particles_from_decay(GenN1_indices[0], Particle, Particle1)")
                .Define("GenN2_dec", "FCCAnalyses::MCParticle::get_list_of_stable_particles_from_decay(GenN2_indices[0], Particle, Particle1)")
                .Define("GenN_d1", "if (GenN1_dec.size()>0) return MCParticle::sel_byIndex(GenN1_dec.at(0), Particle); else return MCParticle::sel_byIndex(GenN2_dec.at(0), Particle);")

                .Define("GenN_vertex_x",    "return MCParticle::get_vertex_x({GenN_d1})")
                .Define("GenN_vertex_y",    "return MCParticle::get_vertex_y({GenN_d1})")
                .Define("GenN_vertex_z",    "return MCParticle::get_vertex_z({GenN_d1})")
                .Define("GenN_Lxyz", "return sqrt(GenN_vertex_x*GenN_vertex_x + GenN_vertex_y*GenN_vertex_y + GenN_vertex_z*GenN_vertex_z)") #in mm
                
                ### use the time of creation fo the leptons to get the lifetime of the HNL ###
                .Define("GenN_tau", "return (FSGenLepton_time * GenN_e.at(0) / GenN_mass.at(0)) ") #tau of HNLs in s
        
                # ee invariant mass
                .Define("FSGen_TwoLeptons_energy", "if (n_FSGenLepton>1) return (FSGenLepton_e.at(0) + FSGenLepton_e.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_px", "if (n_FSGenLepton>1) return (FSGenLepton_px.at(0) + FSGenLepton_px.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_py", "if (n_FSGenLepton>1) return (FSGenLepton_py.at(0) + FSGenLepton_py.at(1)); else return float(-1.);")
                .Define("FSGen_TwoLeptons_pz", "if (n_FSGenLepton>1) return (FSGenLepton_pz.at(0) + FSGenLepton_pz.at(1)); else return float(-1.);")
                .Define("FSGen_invMass", "if (n_FSGenLepton>1) return sqrt(FSGen_TwoLeptons_energy*FSGen_TwoLeptons_energy - FSGen_TwoLeptons_px*FSGen_TwoLeptons_px - FSGen_TwoLeptons_py*FSGen_TwoLeptons_py - FSGen_TwoLeptons_pz*FSGen_TwoLeptons_pz ); else return float(-1.);")

                # MC event primary vertex
                .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

                ################### Reconstructed particles #####################
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

                #JETS
                ### count how many jets are in the event in total to check, it doesn't work with this method on reclustered jets, only on the edm4hep collections Jet ###
		.Define("n_RecoJets", "ReconstructedParticle::get_n(Jet)") 

                #SIMPLE VARIABLES: Access the basic kinematic variables of the (selected) jets, works analogously for electrons, muons
		.Define("RecoJet_e",      "ReconstructedParticle::get_e(Jet)")
                .Define("RecoJet_p",      "ReconstructedParticle::get_p(Jet)") #momentum p
                .Define("RecoJet_pt",      "ReconstructedParticle::get_pt(Jet)") #transverse momentum pt
                .Define("RecoJet_px",      "ReconstructedParticle::get_px(Jet)")
                .Define("RecoJet_py",      "ReconstructedParticle::get_py(Jet)")
                .Define("RecoJet_pz",      "ReconstructedParticle::get_pz(Jet)")
		.Define("RecoJet_eta",     "ReconstructedParticle::get_eta(Jet)") #pseudorapidity eta
                .Define("RecoJet_theta",   "ReconstructedParticle::get_theta(Jet)")
		.Define("RecoJet_phi",     "ReconstructedParticle::get_phi(Jet)") #polar angle in the transverse plane phi
                .Define("RecoJet_charge",  "ReconstructedParticle::get_charge(Jet)")
                .Define("RecoJetTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(Jet,EFlowTrack_1))") #significance
                .Define("RecoJetTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(Jet,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoJetTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(Jet,EFlowTrack_1)")

		#PHOTONS
		.Alias("Photon0", "Photon#0.index") 
		.Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
		.Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total
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

		#ELECTRONS 
		.Alias("Electron0", "Electron#0.index")
		.Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
		.Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total
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
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                # MUONS
		.Alias("Muon0", "Muon#0.index")
		.Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
		.Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total
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
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")

                ### building variables for the two leptons final state ###
                .Define("RecoLeptons", "ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
                .Define("n_RecoLeptons",  "ReconstructedParticle::get_n(RecoLeptons)") 
                .Define("Reco_e",      "ReconstructedParticle::get_e(RecoLeptons)")
                .Define("Reco_p",      "ReconstructedParticle::get_p(RecoLeptons)")
                .Define("Reco_pt",      "ReconstructedParticle::get_pt(RecoLeptons)")
                .Define("Reco_px",      "ReconstructedParticle::get_px(RecoLeptons)")
                .Define("Reco_py",      "ReconstructedParticle::get_py(RecoLeptons)")
                .Define("Reco_pz",      "ReconstructedParticle::get_pz(RecoLeptons)")
		.Define("Reco_eta",     "ReconstructedParticle::get_eta(RecoLeptons)") #pseudorapidity eta
                .Define("Reco_theta",   "ReconstructedParticle::get_theta(RecoLeptons)")
		.Define("Reco_phi",     "ReconstructedParticle::get_phi(RecoLeptons)") #polar angle in the transverse plane phi
                .Define("Reco_charge",  "ReconstructedParticle::get_charge(RecoLeptons)")
                .Define("RecoTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons,EFlowTrack_1))") #significance
                .Define("RecoTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons,EFlowTrack_1))")
                .Define("RecoTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons,EFlowTrack_1)")

                ### cosine between two leptons ###
                .Define("Reco_TwoLeptons_p", "if (n_RecoLeptons>1) return (Reco_px.at(0)*Reco_px.at(1) + Reco_py.at(0)*Reco_py.at(1) + Reco_pz.at(0)*Reco_pz.at(1)); else return float(-2.);")
                .Define("Reco_cos", "if (n_RecoLeptons>1) return (Reco_TwoLeptons_p/(Reco_p.at(0)*Reco_p.at(1))); else return float(-2.);")

                ### angular distance between two leptons ###
                .Define("Reco_DR","if (n_RecoLeptons>1) return myUtils::deltaR(Reco_phi.at(0), Reco_phi.at(1), Reco_eta.at(0), Reco_eta.at(1)); else return float(-1.);")

                ### Jet clustering with different algorithm, only on non leptons ###
                .Define("JetsParticles", "ReconstructedParticle::remove(ReconstructedParticles, RecoLeptons)")
                .Define("RP_px", "ReconstructedParticle::get_px(JetsParticles) ")
                .Define("RP_py", "ReconstructedParticle::get_py(JetsParticles) ")
                .Define("RP_pz", "ReconstructedParticle::get_pz(JetsParticles) ")
                .Define("RP_e", "ReconstructedParticle::get_e(JetsParticles) ")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets",  "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)" )
                ### Durham algo, exclusive clustering (first number 2) N_jets=0 (second number), E-scheme=0 (third and forth numbers) ###
                .Define( "FCCAnalysesJets_ee_kt",  "JetClustering::clustering_ee_kt(2, 0, 1, 0)(pseudo_jets)" )
                .Define("jets_ee_kt",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_ee_kt )")
                ### get the number of jets in a workaround way, anyway is exactly zero for exclusive clustering ###
                .Define("jets_e",  "JetClusteringUtils::get_e(jets_ee_kt)")
                .Define("n_jets", "jets_e.size()")

                ### not useful in this case as the primary track code runs by looking at the chi2 of vertex, taking out the tracks making it larger until there is only one track ###
                ### so there will always be one primary track even if they should both be secondary but the code doesn't handle that and we have both secondary in principle ###
                .Define("PrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)") 
                .Define("PrimaryVertexObject", "VertexFitterSimple::VertexFitter_Tk(1, PrimaryTracks, true, 4.5, 20e-3, 300)")
                .Define("n_PrimaryTracks",  "ReconstructedParticle2Track::getTK_n( PrimaryTracks )")
                .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1, PrimaryTracks )")
                .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )

                ### reconstruct the reco decay vertex using the reco'ed tracks from electrons and muons ###
                .Define("RecoElectronTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoElectrons, EFlowTrack_1)") ### EFlowTrack_1 contains all tracks, selecting a subset associated with certain particles ###
                .Define("RecoMuonTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoMuons, EFlowTrack_1)")
                .Define("RecoLeptonTracks",   "ReconstructedTrack::Merge( RecoElectronTracks, RecoMuonTracks)") ### merges two tracks collections ###
                
                .Define("RecoDecayVertexObjectLepton",   "VertexFitterSimple::VertexFitter_Tk( 0, RecoLeptonTracks)" ) ### reconstructing a vertex withour any request n=0 ###
                .Define("RecoDecayVertexLepton",  "VertexingUtils::get_VertexData( RecoDecayVertexObjectLepton )")

                .Define("Reco_Lxyz","return sqrt(RecoDecayVertexLepton.position.x*RecoDecayVertexLepton.position.x + RecoDecayVertexLepton.position.y*RecoDecayVertexLepton.position.y + RecoDecayVertexLepton.position.z*RecoDecayVertexLepton.position.z);")
                .Define("Reco_Lxy","return sqrt(RecoDecayVertexLepton.position.x*RecoDecayVertexLepton.position.x + RecoDecayVertexLepton.position.y*RecoDecayVertexLepton.position.y);")

                ### LCFIPlus algorithm for vertexing ###
                #find the DVs
                .Define("RecoDVs", "VertexFinderLCFIPlus::get_SV_event(RecoLeptonTracks, EFlowTrack_1, PrimaryVertexObject, true, 9., 40., 5.)")
                #find number of DVs
                .Define("n_RecoDVs", "VertexingUtils::get_n_SV(RecoDVs)")
                .Define("DV_Lxyz", "VertexingUtils::get_d3d_SV(RecoDVs, PrimaryVertexObject)")

                #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
		.Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
		.Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
		.Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
		.Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
		.Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
		.Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
		.Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
		.Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
		.Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy

                ### dilepton invariant mass ###
                .Define("Reco_TwoLeptons_energy", "if (n_RecoLeptons>1) return (Reco_e.at(0) + Reco_e.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_px", "if (n_RecoLeptons>1) return (Reco_px.at(0) + Reco_px.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_py", "if (n_RecoLeptons>1) return (Reco_py.at(0) + Reco_py.at(1)); else return float(-1.);")
                .Define("Reco_TwoLeptons_pz", "if (n_RecoLeptons>1) return (Reco_pz.at(0) + Reco_pz.at(1)); else return float(-1.);")
                .Define("Reco_invMass", "if (n_RecoLeptons>1) return sqrt(Reco_TwoLeptons_energy*Reco_TwoLeptons_energy - Reco_TwoLeptons_px*Reco_TwoLeptons_px - Reco_TwoLeptons_py*Reco_TwoLeptons_py - Reco_TwoLeptons_pz*Reco_TwoLeptons_pz ); else return float(-1.);")

               )
                return df2

        def output():
                branchList = [
                        ######## Monte-Carlo particles #######
                        "n_FSGenElectron",
                        "n_FSGenMuon",
                        "n_FSGenLepton",
                        "n_FSGenPhoton",
                        #"n_GenN",
                        #"n_FSGenNeutrino",

                        #"FSGenLepton_e",
                        #"FSGenLepton_p",
                        #"FSGenLepton_pt",
                        #"FSGenLepton_px",
                        #"FSGenLepton_py",
                        #"FSGenLepton_pz",
                        #"FSGenLepton_eta",
                        #"FSGenLepton_theta",
                        #"FSGenLepton_phi",
                        #"FSGenLepton_charge",
                        #"FSGenLepton_time",
                        #"FSGenLepton_vertex_x",
                        #"FSGenLepton_vertex_y",
                        #"FSGenLepton_vertex_z",

                        #"FSGen_Lxy",
                        #"FSGen_Lxyz",
                        #"FSGen_invMass",
                        #"GenN_Lxyz"
                        #"GenN_tau",
                        #"GenN_mass",
                        #"GenN_e",
                        #"GenN_p",

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
                        "n_RecoTracks",
                        "n_PrimaryTracks",
                        "n_SecondaryTracks",
                        "n_jets",
                        "n_RecoPhotons",
                        "n_RecoElectrons",
                        "n_RecoMuons",
                        "n_RecoLeptons",

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

                        #"RecoElectron_e",
                        #"RecoElectron_p",
                        #"RecoElectron_pt",
                        #"RecoElectron_px",
                        #"RecoElectron_py",
                        #"RecoElectron_pz",
                        #"RecoElectron_eta",
                        #"RecoElectron_theta",
                        #"RecoElectron_phi",
                        #"RecoElectron_charge",
                        #"RecoElectronTrack_absD0",
                        #"RecoElectronTrack_absZ0",
                        #"RecoElectronTrack_absD0sig",
                        #"RecoElectronTrack_absZ0sig",
                        #"RecoElectronTrack_D0cov",
                        #"RecoElectronTrack_Z0cov",

                        "RecoMissingEnergy_e",
                        "RecoMissingEnergy_p",
                        "RecoMissingEnergy_pt",
                        "RecoMissingEnergy_px",
                        "RecoMissingEnergy_py",
                        "RecoMissingEnergy_pz",
                        "RecoMissingEnergy_eta",
                        "RecoMissingEnergy_theta",
                        "RecoMissingEnergy_phi",

                        "Reco_e",
                        "Reco_p",
                        "Reco_pt",
                        "Reco_px",
                        "Reco_py",
                        "Reco_pz",
                        "Reco_eta",
                        "Reco_theta",
                        "Reco_phi",
                        "Reco_charge",
                        "RecoTrack_absD0",
                        "RecoTrack_absZ0",
                        "RecoTrack_absD0sig",
                        "RecoTrack_absZ0sig",
                        "RecoTrack_D0cov",
                        "RecoTrack_Z0cov",

                        "RecoDecayVertexLepton",
                        "Reco_Lxy",
                        "Reco_Lxyz",
                        "Reco_invMass",
                        "Reco_cos",
                        "Reco_DR",

                        #"n_RecoDVs",
                        #"DV_Lxyz", 
                        #"DV_Lxyz_sig",

		]

                return branchList
