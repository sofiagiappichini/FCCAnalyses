import os, copy # tagging
import ROOT
import urllib.request
from copy import deepcopy

processList = {
    'IDEA_events_000731799': {},
    #'CMS_Phase2_events_000731799': {},
    #'CMS_Phase1_events_000731799': {},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/ecm240/EDM4HEP/wzp6_ee_nunuH_Htautau_ecm240/"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1_res/tautau/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

### necessary to run on HTCondor ###
#eosType = "eosuser"

#Optional running on HTCondor, default is False
#runBatch = True

#nCPUS = 6

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#ompGroup = "group_u_FCC.local_gen"

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
#model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
#url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
#url_preproc = "{}/{}.json".format(url_model_dir, model_name)
#url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
#model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
#model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

#local_preproc = "{}/{}.json".format(model_dir, model_name)
#local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
#def get_file_path(url, filename):
#    if os.path.exists(filename):
#        return os.path.abspath(filename)
    #else:
    #    urllib.request.urlretrieve(url, os.path.basename(url))
    #    return os.path.basename(url)
    ## this is the old version of the tagger and we don't care about it


#weaver_preproc = get_file_path(url_preproc, local_preproc)
#weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
#    InclusiveJetClusteringHelper,
)

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
                .Define("reco_mc_index","ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)")

                #.Redefine("ReconstructedParticles",ROOT.SmearObjects.SmearedReconstructedParticle(18.3, 0, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"]) 
                #.Redefine("ReconstructedParticles",ROOT.SmearObjects.SmearedReconstructedParticle(18.3, 130, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"]) 
                #.Redefine("ReconstructedParticles",ROOT.SmearObjects.SmearedReconstructedParticle(21.7, 11, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                #.Redefine("ReconstructedParticles",ROOT.SmearObjects.SmearedReconstructedParticle(3.5631, 13, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                #.Redefine("ReconstructedParticles",ROOT.SmearObjects.SmearedReconstructedParticle(1.2671, 22, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])

                #.Define("Electron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(smeared_electron, smeared_electron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))
                
                #ELECTRONS 
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
                .Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
                .Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
                .Define("RecoElectrons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")

                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                .Define("RecoMuons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons)")
                .Define("RecoMuons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard, ReconstructedParticles)")
                .Define("RecoMuons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard, RecoMuons_iso)")
                
                .Define("RecoLeptons", "ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
                .Define("n_RecoLeptons",  "ReconstructedParticle::get_n(RecoLeptons)") 

                .Define("RecoLeptons_sel", "ReconstructedParticle::merge(RecoElectrons_sel, RecoMuons_sel)")

                .Filter("n_RecoLeptons==0")

                .Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,RecoLeptons)")  
        )


        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticlesJET",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        #EXCLUSIVE 2 JETS=
        jetClusteringHelper_kt2  = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 2, "kt2"
        )
        df2 = jetClusteringHelper_kt2.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_kt2.define(df2)

        df2 = (df2
                .Define("TagJet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("TagJet_kt2_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets))
                .Define("n_TagJet_kt2_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2",           "return int(TagJet_kt2_flavor.size())")
                .Define("TagJet_kt2_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt2.constituents))

                #.Define("TauFromJet_kt2", "FCCAnalyses::ZHfunctions::findTauInJet({})".format(jetClusteringHelper_kt2.constituents)) 
                .Define("TauFromJet_kt2", "FCCAnalyses::ZHfunctions::findTauInJet_smearing({},Particle,21.7,3.5631, 1.2671, 18.3)".format(jetClusteringHelper_kt2.constituents)) 

                .Define("TauFromJet_kt2_type_sel","ReconstructedParticle::get_type(TauFromJet_kt2)")
                .Define("TauFromJet_kt2_tau", "TauFromJet_kt2[TauFromJet_kt2_type_sel>=0]") 
                .Define("TauFromJet_kt2_p","ReconstructedParticle::get_p(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_pt","ReconstructedParticle::get_pt(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_px","ReconstructedParticle::get_px(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_py","ReconstructedParticle::get_py(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_pz","ReconstructedParticle::get_pz(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_theta","ReconstructedParticle::get_theta(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_phi","ReconstructedParticle::get_phi(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_eta","ReconstructedParticle::get_eta(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_y","ReconstructedParticle::get_y(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_e","ReconstructedParticle::get_e(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_charge","ReconstructedParticle::get_charge(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_type","ReconstructedParticle::get_type(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_mass","ReconstructedParticle::get_mass(TauFromJet_kt2_tau)")
                .Define("n_TauFromJet_kt2","TauFromJet_kt2_pt.size()")

                .Define("TagJet_kt2_sel_e",      "TagJet_kt2_e[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_p",      "TagJet_kt2_p[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_pt",      "TagJet_kt2_pt[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_px",      "TagJet_kt2_px[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_py",      "TagJet_kt2_py[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_pz",      "TagJet_kt2_pz[TauFromJet_kt2_type_sel<0]")
		        .Define("TagJet_kt2_sel_eta",     "TagJet_kt2_eta[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_theta",   "TagJet_kt2_theta[TauFromJet_kt2_type_sel<0]")
		        .Define("TagJet_kt2_sel_phi",     "TagJet_kt2_phi[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_mass",      "TagJet_kt2_mass[TauFromJet_kt2_type_sel<0]")
                .Define("n_TagJet_kt2_sel", "TagJet_kt2_sel_e.size()")

        )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
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
        ]

        return branchList