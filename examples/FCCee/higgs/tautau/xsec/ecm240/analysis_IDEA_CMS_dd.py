import os, copy # tagging
import ROOT
import urllib.request
processList = {
    'IDEA_events_000421007': {},
    'CMS_Phase2_events_000421007': {},
    'CMS_Phase1_events_000421007': {},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/ecm240/EDM4HEP/wzp6_ee_nunuH_Hdd_ecm240/"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1/dd/"
#outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"

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
#compGroup = "group_u_FCC.local_gen"

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
#model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    #else:
    #    urllib.request.urlretrieve(url, os.path.basename(url))
    #    return os.path.basename(url)
    ## this is the old version of the tagger and we don't care about it


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

                #################
                # Gen particles #
                #################

                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

                .Define("GenDown_PID", "FCCAnalyses::MCParticle::sel_pdgID(1, true)(Particle)")
                .Define("n_GenDown", "FCCAnalyses::MCParticle::get_n(GenDown_PID)")
                .Define("GenDown_e", "FCCAnalyses::MCParticle::get_e(GenDown_PID)")
                .Define("GenDown_p", "FCCAnalyses::MCParticle::get_p(GenDown_PID)")
                .Define("GenDown_pt", "FCCAnalyses::MCParticle::get_pt(GenDown_PID)")
                .Define("GenDown_px", "FCCAnalyses::MCParticle::get_px(GenDown_PID)")
                .Define("GenDown_py", "FCCAnalyses::MCParticle::get_py(GenDown_PID)")
                .Define("GenDown_pz", "FCCAnalyses::MCParticle::get_pz(GenDown_PID)")
                .Define("GenDown_y", "FCCAnalyses::MCParticle::get_y(GenDown_PID)") #rapidity
                .Define("GenDown_eta", "FCCAnalyses::MCParticle::get_eta(GenDown_PID)")
                .Define("GenDown_theta", "FCCAnalyses::MCParticle::get_theta(GenDown_PID)")
                .Define("GenDown_phi", "FCCAnalyses::MCParticle::get_phi(GenDown_PID)")
                .Define("GenDown_charge", "FCCAnalyses::MCParticle::get_charge(GenDown_PID)")
                .Define("GenDown_mass",   "FCCAnalyses::MCParticle::get_mass(GenDown_PID)")
        )
        #### tagging
        
        global jetClusteringHelper_R5
        global jetFlavourHelper_R5
        ## define jet and run clustering parameters
        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
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
        collections_noleps = copy.deepcopy(collections)
        collections_noleps["PFParticles"] = "ReconstructedParticles"

        ## def __init__(self, coll, njets, tag="")
        
        #EXCLUSIVE 2 JETS
        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_kt2  = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 2, "kt2"
        )
        df2 = jetClusteringHelper_kt2.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_kt2.define(df2)

        ## tagger inference
        df2 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df2)

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

                .Define("TagJet_kt2_isG",    "recojet_isG_kt2")
                .Define("TagJet_kt2_isU",    "recojet_isU_kt2")
                .Define("TagJet_kt2_isD",    "recojet_isD_kt2")
                .Define("TagJet_kt2_isS",    "recojet_isS_kt2")
                .Define("TagJet_kt2_isC",    "recojet_isC_kt2")
                .Define("TagJet_kt2_isB",    "recojet_isB_kt2")
                .Define("TagJet_kt2_isTAU",    "recojet_isTAU_kt2")

                .Define("Down_p_res_0_20", "FCCAnalyses::ZHfunctions::reso_p_jets(GenDown_p, TagJet_kt2_p, GenDown_charge, TagJet_kt2_charge, 20., 0.)")
                .Define("Down_p_res_20_40", "FCCAnalyses::ZHfunctions::reso_p_jets(GenDown_p, TagJet_kt2_p, GenDown_charge, TagJet_kt2_charge, 40., 20.)")
                .Define("Down_p_res_40_60", "FCCAnalyses::ZHfunctions::reso_p_jets(GenDown_p, TagJet_kt2_p, GenDown_charge, TagJet_kt2_charge, 60., 40.)")
                .Define("Down_p_res_60_higher", "FCCAnalyses::ZHfunctions::reso_p_jets(GenDown_p, TagJet_kt2_p, GenDown_charge, TagJet_kt2_charge, 1000., 60.)")
                .Define("Down_p_res_total", "FCCAnalyses::ZHfunctions::reso_p_jets(GenDown_p, TagJet_kt2_p, GenDown_charge, TagJet_kt2_charge, 1000., 0.)")

        )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

            "GenDown_PID",
            "n_GenDown",
            "GenDown_e",
            "GenDown_p",
            "GenDown_pt",
            "GenDown_px",
            "GenDown_py",
            "GenDown_pz",
            "GenDown_y",
            "GenDown_eta",
            "GenDown_theta",
            "GenDown_phi",
            "GenDown_charge",
            "GenDown_mass",

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

            "TagJet_kt2_isG",  
            "TagJet_kt2_isU",
            "TagJet_kt2_isD",   
            "TagJet_kt2_isS",  
            "TagJet_kt2_isC",
            "TagJet_kt2_isB",  
            "TagJet_kt2_isTAU",

            "Down_p_res_0_20",
            "Down_p_res_20_40",
            "Down_p_res_40_60",
            "Down_p_res_60_higher",
            "Down_p_res_total",
        ]

        return branchList