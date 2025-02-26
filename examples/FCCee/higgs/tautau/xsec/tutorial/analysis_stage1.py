import os, copy # tagging
import ROOT
import urllib.request

# list of processes that you want to analyse, the name is the same of your .root file (after detector simulation)
processList = {
    'ee_Htautau': {'chunks':1},
}
#directory where the files can be found
inputDir = "/work/"

#Optional: output directory, default is local running directory
outputDir = "/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

                ##################
                # Reco particles #
                ##################

                #you can find the functions to save the variable for each particle at https://github.com/HEP-FCC/FCCAnalyses/blob/master/analyzers/dataframe/src/ReconstructedParticle.cc
                # what you would likely need is:
                # ReconstructedParticle::get_n() gives the number of particles in each event
                # ReconstructedParticle::get_e() gives the energy of particles in each event
                # ReconstructedParticle::get_p() gives the momentum of particles in each event
                # ReconstructedParticle::get_px() gives the x component of the momentum of particles in each event (similar for py, pz)
                # ReconstructedParticle::get_pt() gives the transverse (xy plane) momentum of particles in each event
                # ReconstructedParticle::get_eta() gives the angle between the xy plane and the momentum of the particle in each event
                # ReconstructedParticle::get_theta() gives the angle between the z axis and the momentum of the particle in each event
                # ReconstructedParticle::get_phi() gives the eta angle of the pt in the xy plane of particles in each event
                # ReconstructedParticle::get_mass() gives the mass of particles in each event
                # ReconstructedParticle::get_charge() gives the charge of particles in each event
                # we want to separate some types of particle: electrons, muons, photons, neutral hadrons, missing energy, jets and finally taus

                #ELECTRONS 
                # electrons, muons and photons are already separated into different branches (or classes) in you .root file so we can use those specific names to get 
                # the information that we want directly, this is done with the next two lines which tell the code we want to rename a feew things and were it should look
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
                .Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total
                
                # MUONS
                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                .Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total
                
                #PHOTONS
                .Alias("Photon0", "Photon#0.index") 
                .Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
                .Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total
                
                #NEUTRAL HADRONS
                # we don't have a class for neutral hadrons only but we have one class with all particles (ReconstructedParticles) so we can select the particles we want ourselves
                # this excludes all photons (with type 22), type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                # the charge selection makes sure the particles are neutral
                .Define("NeutralHadrons_cand",   "ReconstructedParticles[ReconstructedParticles.type != 22]") 
                .Define("NeutralHadrons",       "ReconstructedParticle::sel_charge(0, true) (NeutralHadrons_cand)")
                .Define("n_NeutralHadrons",  "ReconstructedParticle::get_n(NeutralHadrons)") #count how many photons are in the event in total
                
                # MISSING ENERGY
                # this class is a bit different than the rest so the variables are already defined
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(240, ReconstructedParticles)") #ecm 
                .Define("RecoEmiss_px",  "RecoEmiss[0].momentum.x")
                .Define("RecoEmiss_py",  "RecoEmiss[0].momentum.y")
                .Define("RecoEmiss_pz",  "RecoEmiss[0].momentum.z")
                .Define("RecoEmiss_pt",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
                .Define("RecoEmiss_p",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
                .Define("RecoEmiss_e",   "RecoEmiss[0].energy")

                # JETS, reclustered from the reconstructed particles, never use the class in the samples
                ### https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h ###

                .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
                .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
                .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
                .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
                .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
                .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
                .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E

                #R5 inclusive jet algorithm
                .Define("FCCAnalysesJets_R5", "JetClustering::clustering_ee_genkt(0.5, 0, 2., 0, 1, -1)(pseudo_jets)")
                .Define("Jets_R5",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_R5 )") 
                .Define("Jet_GetConstituents_R5","JetClusteringUtils::get_constituents(FCCAnalysesJets_R5)")
                .Define("Jets_Constituents_R5", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, Jet_GetConstituents_R5)") #build jet constituents lists for tau reconstruction

                # the function names to get the variables are the same as for the usual particles but the definitions are specific to work with a collection of particle (jet) instead of a single particle
		        .Define("Jets_R5_e",      "JetClusteringUtils::get_e(Jets_R5)")
                .Define("Jets_R5_p",      "JetClusteringUtils::get_p(Jets_R5)") #momentum p
                .Define("Jets_R5_pt",      "JetClusteringUtils::get_pt(Jets_R5)") #transverse momentum pt
                .Define("Jets_R5_px",      "JetClusteringUtils::get_px(Jets_R5)")
                .Define("Jets_R5_py",      "JetClusteringUtils::get_py(Jets_R5)")
                .Define("Jets_R5_pz",      "JetClusteringUtils::get_pz(Jets_R5)")
		        .Define("Jets_R5_eta",     "JetClusteringUtils::get_eta(Jets_R5)") #pseudorapidity eta
                .Define("Jets_R5_theta",   "JetClusteringUtils::get_theta(Jets_R5)")
		        .Define("Jets_R5_phi",     "JetClusteringUtils::get_phi(Jets_R5)") #polar angle in the transverse plane phi
                .Define("Jets_R5_mass",      "JetClusteringUtils::get_m(Jets_R5)")
                .Define("n_Jets_R5", "Jets_R5_e.size()")

                # TAUS, reconstruction of hadronic taus from jets
                # we don't have taus in our .root file because they are not stable particles but we can reconstruct them by knowing how they decay
                # this is done in the functions.h file and we now have a particle called tau
                .Define("TauFromJet_R5",    "FCCAnalyses::ZHfunctions::findTauInJet(Jets_Constituents_R5)") 
                .Define("TauFromJet_R5_type_sel",   "ReconstructedParticle::get_type(TauFromJet_R5)")
                .Define("TauFromJet_R5_tau",    "TauFromJet_R5[TauFromJet_R5_type_sel>=0]") 
                .Define("TauFromJet_R5_p",      "ReconstructedParticle::get_p(TauFromJet_R5_tau)")
                .Define("n_TauFromJet_R5",      "TauFromJet_R5_p.size()")

                # we can redefine our jets based on wether they are not taus 
                .Define("Jets_R5_sel_e",      "Jets_R5_e[TauFromJet_R5_type_sel<0 ]")
                .Define("n_Jets_R5_sel", "Jets_R5_sel_e.size()")
               
        )
        
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

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
            
        ]

        return branchList