import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    #'noISR_e+e-_noCuts_EWonly':{},
    #'noISR_e+e-_noCuts_cehim_m1':{},
    #'noISR_e+e-_noCuts_cehim_p1':{},
    #'noISR_e+e-_noCuts_cehre_m1':{},
    #'noISR_e+e-_noCuts_cehre_p1':{},
    
    'EWonly_taudecay_2Pi2Nu':{},
    #'cehim_m1_taudecay_2Pi2Nu':{},
    #'cehim_p1_taudecay_2Pi2Nu':{},
    #'cehre_m1_taudecay_2Pi2Nu':{},
    #'cehre_p1_taudecay_2Pi2Nu':{},

    #'EWonly_taudecay_PiPi0Nu':{},
    #'cehim_m1_taudecay_PiPi0Nu':{},
    #'cehim_p1_taudecay_PiPi0Nu':{},
    #'cehre_m1_taudecay_PiPi0Nu':{},
    #'cehre_p1_taudecay_PiPi0Nu':{},

    #'cehim_m5_taudecay_2Pi2Nu':{},
    #'cehim_p5_taudecay_2Pi2Nu':{},
    #'cehre_m5_taudecay_2Pi2Nu':{},
    #'cehre_p5_taudecay_2Pi2Nu':{},

    #'cehim_m2_taudecay_2Pi2Nu':{},
    #'cehim_p2_taudecay_2Pi2Nu':{},
    #'cehre_m2_taudecay_2Pi2Nu':{},
    #'cehre_p2_taudecay_2Pi2Nu':{},

    #'cehim_p0p1_taudecay_2Pi2Nu':{},
    #'cehim_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_p0p1_taudecay_2Pi2Nu':{},

    #'cehim_p10_taudecay_2Pi2Nu':{},
    #'cehim_m10_taudecay_2Pi2Nu':{},

    #'wzp6_ee_eeH_Htautau_ecm240': {},
    #'p8_ee_ZZ_ecm240':{'chunks':100},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir = "/ceph/mpresill/FCCee/ZH_SMEFT_LO_noISR_noCuts_prod/ele"
#inputDir = '/ceph/sgiappic/HiggsCP'
#inputDir = "/ceph/sgiappic/HiggsCP/winter23"

outputDir = "/ceph/sgiappic/HiggsCP/CPtest/stage1"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"

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
    def analysers(df2):
        df2 = (df2

                #################
                # Gen particles #
                #################

                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

                #all final state gen electrons and positrons
                .Define("GenElectron_PID", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenElectron", "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
                .Define("FSGenElectron_e", "FCCAnalyses::MCParticle::get_e(FSGenElectron)")
                .Define("FSGenElectron_p", "FCCAnalyses::MCParticle::get_p(FSGenElectron)")
                .Define("FSGenElectron_pt", "FCCAnalyses::MCParticle::get_pt(FSGenElectron)")
                .Define("FSGenElectron_px", "FCCAnalyses::MCParticle::get_px(FSGenElectron)")
                .Define("FSGenElectron_py", "FCCAnalyses::MCParticle::get_py(FSGenElectron)")
                .Define("FSGenElectron_pz", "FCCAnalyses::MCParticle::get_pz(FSGenElectron)")
                .Define("FSGenElectron_y", "FCCAnalyses::MCParticle::get_y(FSGenElectron)") #rapidity
                .Define("FSGenElectron_eta", "FCCAnalyses::MCParticle::get_eta(FSGenElectron)")
                .Define("FSGenElectron_theta", "FCCAnalyses::MCParticle::get_theta(FSGenElectron)")
                .Define("FSGenElectron_phi", "FCCAnalyses::MCParticle::get_phi(FSGenElectron)")
                .Define("FSGenElectron_charge", "FCCAnalyses::MCParticle::get_charge(FSGenElectron)")
                .Define("FSGenElectron_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenElectron)")
                .Define("FSGenElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenElectron,Particle,Particle0)")
                .Define("FSGenElectron_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron )")
                
                #all final state gen muons 
                .Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
                .Define("FSGenMuon", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
                .Define("FSGenMuon_e", "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
                .Define("FSGenMuon_p", "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
                .Define("FSGenMuon_pt", "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
                .Define("FSGenMuon_px", "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
                .Define("FSGenMuon_py", "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
                .Define("FSGenMuon_pz", "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
                .Define("FSGenMuon_y", "FCCAnalyses::MCParticle::get_y(FSGenMuon)")
                .Define("FSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
                .Define("FSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
                .Define("FSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
                .Define("FSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
                .Define("FSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
                .Define("FSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenMuon,Particle,Particle0)")
                .Define("FSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon )")
                .Define("FSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon )")
                .Define("FSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon )")
                
                #need to define a class only for muons coming from the Z
                #info on gen Z are not kept at all, muons seem to come directly from initial state electron
                .Define("ZFSGenMuon",   "FCCAnalyses::MCParticle::sel_parentID(15, false, true)(FSGenMuon,Particle,Particle0)")
                .Define("n_ZFSGenMuon", "FCCAnalyses::MCParticle::get_n(ZFSGenMuon)")
                .Define("ZFSGenMuon_e", "FCCAnalyses::MCParticle::get_e(ZFSGenMuon)")
                .Define("ZFSGenMuon_p", "FCCAnalyses::MCParticle::get_p(ZFSGenMuon)")
                .Define("ZFSGenMuon_pt", "FCCAnalyses::MCParticle::get_pt(ZFSGenMuon)")
                .Define("ZFSGenMuon_px", "FCCAnalyses::MCParticle::get_px(ZFSGenMuon)")
                .Define("ZFSGenMuon_py", "FCCAnalyses::MCParticle::get_py(ZFSGenMuon)")
                .Define("ZFSGenMuon_pz", "FCCAnalyses::MCParticle::get_pz(ZFSGenMuon)")
                .Define("ZFSGenMuon_y", "FCCAnalyses::MCParticle::get_y(ZFSGenMuon)")
                .Define("ZFSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(ZFSGenMuon)")
                .Define("ZFSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(ZFSGenMuon)")
                .Define("ZFSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(ZFSGenMuon)")
                .Define("ZFSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(ZFSGenMuon)")
                .Define("ZFSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(ZFSGenMuon)")
                .Define("ZFSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(ZFSGenMuon,Particle,Particle0)")
                .Define("ZFSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( ZFSGenMuon )")
                .Define("ZFSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( ZFSGenMuon )")
                .Define("ZFSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( ZFSGenMuon )")

                #distinguish between pre fsr and after iterative fsr taus and keep them in separate classes to be analysed
                .Define("AllGenTauPlus",    "FCCAnalyses::MCParticle::sel_pdgID(-15, false)(Particle)")
                .Define("AllGenTauMin",    "FCCAnalyses::MCParticle::sel_pdgID(15, false)(Particle)")
                .Define("AllGenTau",           "FCCAnalyses::MCParticle::mergeParticles(AllGenTauPlus, AllGenTauMin)")

                #all taus in the events
                .Define("n_AllGenTau",      "FCCAnalyses::MCParticle::get_n(AllGenTau)")
                .Define("AllGenTau_e",     "FCCAnalyses::MCParticle::get_e(AllGenTau)")
                .Define("AllGenTau_p",     "FCCAnalyses::MCParticle::get_p(AllGenTau)")
                .Define("AllGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(AllGenTau)")
                .Define("AllGenTau_px",     "FCCAnalyses::MCParticle::get_px(AllGenTau)")
                .Define("AllGenTau_py",     "FCCAnalyses::MCParticle::get_py(AllGenTau)")
                .Define("AllGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(AllGenTau)")
                .Define("AllGenTau_y",    "FCCAnalyses::MCParticle::get_y(AllGenTau)")
                .Define("AllGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(AllGenTau)")
                .Define("AllGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(AllGenTau)")
                .Define("AllGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(AllGenTau)")
                .Define("AllGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(AllGenTau,Particle,Particle0)")
                .Define("AllGenTau_charge", "FCCAnalyses::MCParticle::get_charge(AllGenTau)")
                .Define("AllGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(AllGenTau)")
                .Define("AllGenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( AllGenTau )")
                .Define("AllGenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( AllGenTau )")
                .Define("AllGenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( AllGenTau )")
                
                #post-fsr taus from higgs
                .Define("HiggsGenTau",           "FCCAnalyses::MCParticle::sel_HTauTau()(AllGenTau, Particle, Particle0, Particle1)")
                .Define("n_HiggsGenTau",      "FCCAnalyses::MCParticle::get_n(HiggsGenTau)")
                .Define("HiggsGenTau_e",     "FCCAnalyses::MCParticle::get_e(HiggsGenTau)")
                .Define("HiggsGenTau_p",     "FCCAnalyses::MCParticle::get_p(HiggsGenTau)")
                .Define("HiggsGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(HiggsGenTau)")
                .Define("HiggsGenTau_px",     "FCCAnalyses::MCParticle::get_px(HiggsGenTau)")
                .Define("HiggsGenTau_py",     "FCCAnalyses::MCParticle::get_py(HiggsGenTau)")
                .Define("HiggsGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(HiggsGenTau)")
                .Define("HiggsGenTau_y",    "FCCAnalyses::MCParticle::get_y(HiggsGenTau)")
                .Define("HiggsGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(HiggsGenTau)")
                .Define("HiggsGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(HiggsGenTau)")
                .Define("HiggsGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(HiggsGenTau)")
                .Define("HiggsGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(HiggsGenTau,Particle,Particle0)")
                .Define("HiggsGenTau_charge", "FCCAnalyses::MCParticle::get_charge(HiggsGenTau)")
                .Define("HiggsGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(HiggsGenTau)")
                .Define("HiggsGenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( HiggsGenTau )")
                .Define("HiggsGenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( HiggsGenTau )")
                .Define("HiggsGenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( HiggsGenTau )")

                #generic taus after fsr to work with the backgrounds
                .Define("GenTau",       "FCCAnalyses::MCParticle::sel_daughterID(15, false, true)(AllGenTau, Particle, Particle0)")
                .Define("n_GenTau",      "FCCAnalyses::MCParticle::get_n(GenTau)")
                .Define("GenTau_e",     "FCCAnalyses::MCParticle::get_e(GenTau)")
                .Define("GenTau_p",     "FCCAnalyses::MCParticle::get_p(GenTau)")
                .Define("GenTau_pt",     "FCCAnalyses::MCParticle::get_pt(GenTau)")
                .Define("GenTau_px",     "FCCAnalyses::MCParticle::get_px(GenTau)")
                .Define("GenTau_py",     "FCCAnalyses::MCParticle::get_py(GenTau)")
                .Define("GenTau_pz",     "FCCAnalyses::MCParticle::get_pz(GenTau)")
                .Define("GenTau_y",    "FCCAnalyses::MCParticle::get_y(GenTau)")
                .Define("GenTau_eta",    "FCCAnalyses::MCParticle::get_eta(GenTau)")
                .Define("GenTau_theta",     "FCCAnalyses::MCParticle::get_theta(GenTau)")
                .Define("GenTau_phi",    "FCCAnalyses::MCParticle::get_phi(GenTau)")
                .Define("GenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(GenTau,Particle,Particle0)")
                .Define("GenTau_charge", "FCCAnalyses::MCParticle::get_charge(GenTau)")
                .Define("GenTau_mass",   "FCCAnalyses::MCParticle::get_mass(GenTau)")
                .Define("GenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( GenTau )")
                .Define("GenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( GenTau )")
                .Define("GenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( GenTau )")

                #( int pdg_mother, std::vector<int> pdg_daughters, bool stableDaughters, bool chargeConjugateMother, bool chargeConjugateDaughters, bool inclusiveDecay)
                #rho nu decay (pi pi0 nu)
                .Define("TauPtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #pi nu decay
                .Define("TauPtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #ele nu decay
                .Define("TauPtoENuNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {-11, 12, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMtoENuNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {11, -12, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #mu nu decay
                .Define("TauPtoMuNuNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {-13, 14, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMtoMuNuNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {13, -14, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay (pi pi0 pi0 nu)
                .Define("TauPto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay - three prongs (pi pi pi nu)
                .Define("TauPto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 211, -211, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, -211, 211, 16},  true, false, false, false)  ( Particle, Particle1)" )

                #select the right decay for both taus

                ###############################

                .Filter("n_HiggsGenTau==2 && (HiggsGenTau_charge.at(0) + HiggsGenTau_charge.at(1))==0")
                .Filter("(TauPtoPiNu_idx.size()>0 || TauPtoRhoNu_idx.size()>0 || TauPtoENuNu_idx.size()>0 || TauPtoMuNuNu_idx.size()>0 || TauPto2Pi0Nu_idx.size()>0 || TauPto3PiNu_idx.size()>0)")
                .Filter("(TauMtoPiNu_idx.size()>0 || TauMtoRhoNu_idx.size()>0 || TauMtoENuNu_idx.size()>0 || TauMtoMuNuNu_idx.size()>0 || TauMto2Pi0Nu_idx.size()>0 || TauMto3PiNu_idx.size()>0)")
                #.Filter("(TauPtoPiNu_idx.size()>0 || TauPtoRhoNu_idx.size()>0 || TauPto2Pi0Nu_idx.size()>0 || TauPto3PiNu_idx.size()>0)")
                #.Filter("(TauMtoPiNu_idx.size()>0 || TauMtoRhoNu_idx.size()>0 || TauMto2Pi0Nu_idx.size()>0 || TauMto3PiNu_idx.size()>0)")
                
                ###############################

                .Define("GenPiP1_e",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_px",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_py",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_pz",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_p",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_pt",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_eta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_phi",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_theta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_charge",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_mass",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_vertex_x",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_vertex_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_vertex_z",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP1_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiP1_px, GenPiP1_py, GenPiP1_pz, GenPiP1_e)")

                .Define("GenPiP2_e",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_px",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_py",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_pz",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_p",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_pt",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_eta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_phi",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_theta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_charge",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_mass",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_vertex_x",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_vertex_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_vertex_z",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP2_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiP2_px, GenPiP2_py, GenPiP2_pz, GenPiP2_e)")

                .Define("GenPiP3_e",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_px",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_py",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_pz",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_p",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_pt",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_eta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_phi",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_theta",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_charge",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_mass",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_vertex_x",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_vertex_y",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_vertex_z",     "if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP3_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiP3_px, GenPiP3_py, GenPiP3_pz, GenPiP3_e)")

                .Define("GenPiP_e",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_px",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_py",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_pz",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_p",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_pt",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_y",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_eta",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_phi",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_theta",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_charge",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_mass",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_vertex_x",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_vertex_y",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_vertex_z",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[1])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[1])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiP_p4",        " if (TauPto3PiNu_idx.size()>0) return (GenPiP1_p4 + GenPiP2_p4 + GenPiP3_p4); else return FCCAnalyses::ZHfunctions::build_p4(GenPiP_px, GenPiP_py, GenPiP_pz, GenPiP_e);")

                
                .Define("GenNuP_e",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_px",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_py",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_pz",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_p",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_pt",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_y",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_eta",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_phi",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_theta",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_charge",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_mass",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenNuP_px, GenNuP_py, GenNuP_pz, GenNuP_e)")
                .Define("GenNuP_vertex_x",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_vertex_y",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_vertex_z",     "if (TauPtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoPiNu_idx[2])}); \
                                            else if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[4])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[6])}); \
                                            else if (TauPto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuP_Impact_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenNuP_vertex_x, GenNuP_vertex_y, GenNuP_vertex_z, ROOT::VecOps::RVec<float>{})")
                

                .Define("GammaP1_e",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[2])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[2])});\
                                              else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP2_e",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[3])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[3])});\
                                              else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP3_e",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[4])});\
                                         else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP4_e",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[5])});\
                                         else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaP1_px",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[2])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[2])});\
                                              else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP2_px",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[3])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[3])});\
                                              else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP3_px",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[4])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP4_px",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[5])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaP1_py",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[2])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[2])});\
                                              else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP2_py",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[3])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[3])});\
                                              else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP3_py",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[4])});\
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP4_py",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[5])});\
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaP1_pz",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[2])});\
                                             else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[2])});\
                                              else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP2_pz",     "if (TauPtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoRhoNu_idx[3])}); \
                                            else if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[3])});\
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP3_pz",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[4])});\
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaP4_pz",     "if (TauPto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPto2Pi0Nu_idx[5])});\
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaP1_p4",       "if (TauPto2Pi0Nu_idx.size()>0 || TauPtoRhoNu_idx.size()>0) return TLorentzVector(GammaP1_px.at(0), GammaP1_py.at(0), GammaP1_pz.at(0), GammaP1_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaP2_p4",       "if (TauPto2Pi0Nu_idx.size()>0 || TauPtoRhoNu_idx.size()>0) return TLorentzVector(GammaP2_px.at(0), GammaP2_py.at(0), GammaP2_pz.at(0), GammaP2_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaP3_p4",       "if (TauPto2Pi0Nu_idx.size()>0) return TLorentzVector(GammaP3_px.at(0), GammaP3_py.at(0), GammaP3_pz.at(0), GammaP3_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaP4_p4",       "if (TauPto2Pi0Nu_idx.size()>0) return TLorentzVector(GammaP4_px.at(0), GammaP4_py.at(0), GammaP4_pz.at(0), GammaP4_e.at(0)); else return TLorentzVector(0,0,0,0);")
                
                .Define("GenPi0P1_p4",       "if ((GammaP1_p4+GammaP2_p4).M()>0.13 && (GammaP1_p4+GammaP2_p4).M()<0.14) return (GammaP1_p4+GammaP2_p4); else return TLorentzVector(0,0,0,0);")
                .Define("GenPi0P1_px",    "GenPi0P1_p4.Px()")
                .Define("GenPi0P1_py",    "GenPi0P1_p4.Py()")
                .Define("GenPi0P1_pz",    "GenPi0P1_p4.Pz()")
                .Define("GenPi0P1_p",    "GenPi0P1_p4.P()")
                .Define("GenPi0P1_pt",    "GenPi0P1_p4.Pt()")
                .Define("GenPi0P1_e",     "GenPi0P1_p4.E()")
                .Define("GenPi0P1_eta",    "GenPi0P1_p4.Eta()")
                .Define("GenPi0P1_phi",    "GenPi0P1_p4.Phi()")
                .Define("GenPi0P1_theta",    "GenPi0P1_p4.Theta()")
                .Define("GenPi0P1_y",     "GenPi0P1_p4.Rapidity()")
                .Define("GenPi0P1_mass",    "GenPi0P1_p4.M()")

                .Define("GenPi0P2_p4",       "if ((GammaP3_p4+GammaP4_p4).M()>0.13 && (GammaP3_p4+GammaP4_p4).M()<0.14) return (GammaP3_p4+GammaP4_p4); else return TLorentzVector(0,0,0,0);")
                .Define("GenPi0P2_px",    "GenPi0P2_p4.Px()")
                .Define("GenPi0P2_py",    "GenPi0P2_p4.Py()")
                .Define("GenPi0P2_pz",    "GenPi0P2_p4.Pz()")
                .Define("GenPi0P2_p",    "GenPi0P2_p4.P()")
                .Define("GenPi0P2_pt",    "GenPi0P2_p4.Pt()")
                .Define("GenPi0P2_e",     "GenPi0P2_p4.E()")
                .Define("GenPi0P2_eta",    "GenPi0P2_p4.Eta()")
                .Define("GenPi0P2_phi",    "GenPi0P2_p4.Phi()")
                .Define("GenPi0P2_theta",    "GenPi0P2_p4.Theta()")
                .Define("GenPi0P2_y",     "GenPi0P2_p4.Rapidity()")
                .Define("GenPi0P2_mass",    "GenPi0P2_p4.M()")

                .Define("GenPiM1_e",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_px",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_py",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_pz",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_p",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_pt",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_eta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_phi",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_theta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_charge",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_mass",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_vertex_x",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_vertex_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_vertex_z",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM1_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiM1_px, GenPiM1_py, GenPiM1_pz, GenPiM1_e)")

                .Define("GenPiM2_e",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_px",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_py",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_pz",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_p",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_pt",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_eta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_phi",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_theta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_charge",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_mass",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_vertex_x",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_vertex_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_vertex_z",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[2])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM2_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiM2_px, GenPiM2_py, GenPiM2_pz, GenPiM2_e)")

                .Define("GenPiM3_e",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_px",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_py",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_pz",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_p",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_pt",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_eta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_phi",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_theta",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_charge",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_mass",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_vertex_x",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_vertex_y",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                            else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_vertex_z",     "if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[3])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM3_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenPiM3_px, GenPiM3_py, GenPiM3_pz, GenPiM3_e)")

                .Define("GenPiM_e",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                             else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_px",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_py",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                             else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_pz",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_p",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_pt",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_y",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_eta",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_phi",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_theta",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_charge",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_mass",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_vertex_x",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_vertex_y",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_vertex_z",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[1])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[1])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[1])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenPiM_p4",        " if (TauMto3PiNu_idx.size()>0) return (GenPiM1_p4 + GenPiM2_p4 + GenPiM3_p4); else return FCCAnalyses::ZHfunctions::build_p4(GenPiM_px, GenPiM_py, GenPiM_pz, GenPiM_e);")

                
                .Define("GenNuM_e",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_px",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_py",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_pz",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_p",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_pt",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_y",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_eta",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_phi",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_theta",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_charge",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_mass",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenNuM_px, GenNuM_py, GenNuM_pz, GenNuM_e)")
                .Define("GenNuM_vertex_x",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_vertex_y",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_vertex_z",     "if (TauMtoPiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoPiNu_idx[2])}); \
                                            else if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[4])}); \
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[6])}); \
                                            else if (TauMto3PiNu_idx.size()>0) return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto3PiNu_idx[4])}); \
                                             else return FCCAnalyses::MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GenNuM_Impact_p4",        "FCCAnalyses::ZHfunctions::build_p4(GenNuM_vertex_x, GenNuM_vertex_y, GenNuM_vertex_z, ROOT::VecOps::RVec<float>{})")

                .Define("GammaM1_e",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[2])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[2])});\
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM2_e",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[3])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[3])});\
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM3_e",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[4])});\
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM4_e",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[5])});\
                                            else return FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaM1_px",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[2])});\
                                             else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[2])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM2_px",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[3])});\
                                             else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[3])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM3_px",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[4])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM4_px",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[5])});\
                                             else return FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaM1_py",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[2])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[2])});\
                                            else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM2_py",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[3])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[3])});\
                                            else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM3_py",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[4])});\
                                            else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM4_py",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[5])});\
                                            else return FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaM1_pz",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[2])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[2])});\
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM2_pz",     "if (TauMtoRhoNu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoRhoNu_idx[3])});\
                                            else if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[3])});\
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM3_pz",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[4])});\
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                .Define("GammaM4_pz",     "if (TauMto2Pi0Nu_idx.size()>0) return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMto2Pi0Nu_idx[5])});\
                                            else return FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{});")
                
                .Define("GammaM1_p4",       "if (TauMto2Pi0Nu_idx.size()>0 || TauMtoRhoNu_idx.size()>0) return TLorentzVector(GammaM1_px.at(0), GammaM1_py.at(0), GammaM1_pz.at(0), GammaM1_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaM2_p4",       "if (TauMto2Pi0Nu_idx.size()>0 || TauMtoRhoNu_idx.size()>0) return TLorentzVector(GammaM2_px.at(0), GammaM2_py.at(0), GammaM2_pz.at(0), GammaM2_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaM3_p4",       "if (TauMto2Pi0Nu_idx.size()>0) return TLorentzVector(GammaM3_px.at(0), GammaM3_py.at(0), GammaM3_pz.at(0), GammaM3_e.at(0)); else return TLorentzVector(0,0,0,0);")
                .Define("GammaM4_p4",       "if (TauMto2Pi0Nu_idx.size()>0) return TLorentzVector(GammaM4_px.at(0), GammaM4_py.at(0), GammaM4_pz.at(0), GammaM4_e.at(0)); else return TLorentzVector(0,0,0,0);")
                
                .Define("GenPi0M1_p4",       "if ((GammaM1_p4+GammaM2_p4).M()>0.13 && (GammaM1_p4+GammaM2_p4).M()<0.14) return (GammaM1_p4+GammaM2_p4); else return TLorentzVector(0,0,0,0);")
                .Define("GenPi0M1_px",    "GenPi0M1_p4.Px()")
                .Define("GenPi0M1_py",    "GenPi0M1_p4.Py()")
                .Define("GenPi0M1_pz",    "GenPi0M1_p4.Pz()")
                .Define("GenPi0M1_p",    "GenPi0M1_p4.P()")
                .Define("GenPi0M1_pt",    "GenPi0M1_p4.Pt()")
                .Define("GenPi0M1_e",     "GenPi0M1_p4.E()")
                .Define("GenPi0M1_eta",    "GenPi0M1_p4.Eta()")
                .Define("GenPi0M1_phi",    "GenPi0M1_p4.Phi()")
                .Define("GenPi0M1_theta",    "GenPi0M1_p4.Theta()")
                .Define("GenPi0M1_y",     "GenPi0M1_p4.Rapidity()")
                .Define("GenPi0M1_mass",    "GenPi0M1_p4.M()")

                .Define("GenPi0M2_p4",       "if ((GammaM3_p4+GammaM4_p4).M()>0.13 && (GammaM3_p4+GammaM4_p4).M()<0.14) return (GammaM3_p4+GammaM4_p4); else return TLorentzVector(0,0,0,0);")
                .Define("GenPi0M2_px",    "GenPi0M2_p4.Px()")
                .Define("GenPi0M2_py",    "GenPi0M2_p4.Py()")
                .Define("GenPi0M2_pz",    "GenPi0M2_p4.Pz()")
                .Define("GenPi0M2_p",    "GenPi0M2_p4.P()")
                .Define("GenPi0M2_pt",    "GenPi0M2_p4.Pt()")
                .Define("GenPi0M2_e",     "GenPi0M2_p4.E()")
                .Define("GenPi0M2_eta",    "GenPi0M2_p4.Eta()")
                .Define("GenPi0M2_phi",    "GenPi0M2_p4.Phi()")
                .Define("GenPi0M2_theta",    "GenPi0M2_p4.Theta()")
                .Define("GenPi0M2_y",     "GenPi0M2_p4.Rapidity()")
                .Define("GenPi0M2_mass",    "GenPi0M2_p4.M()")

                .Define("GenRhoP_p4",       "GenPi0P1_p4+GenPiP_p4.at(0)")
                .Define("GenRhoP_px",    "GenRhoP_p4.Px()")
                .Define("GenRhoP_py",    "GenRhoP_p4.Py()")
                .Define("GenRhoP_pz",    "GenRhoP_p4.Pz()")
                .Define("GenRhoP_p",    "GenRhoP_p4.P()")
                .Define("GenRhoP_pt",    "GenRhoP_p4.Pt()")
                .Define("GenRhoP_e",     "GenRhoP_p4.E()")
                .Define("GenRhoP_eta",    "GenRhoP_p4.Eta()")
                .Define("GenRhoP_phi",    "GenRhoP_p4.Phi()")
                .Define("GenRhoP_theta",    "GenRhoP_p4.Theta()")
                .Define("GenRhoP_y",     "GenRhoP_p4.Rapidity()")
                .Define("GenRhoP_mass",    "GenRhoP_p4.M()")

                .Define("GenRhoM_p4",       "GenPi0M1_p4+GenPiM_p4.at(0)")
                .Define("GenRhoM_px",    "GenRhoM_p4.Px()")
                .Define("GenRhoM_py",    "GenRhoM_p4.Py()")
                .Define("GenRhoM_pz",    "GenRhoM_p4.Pz()")
                .Define("GenRhoM_p",    "GenRhoM_p4.P()")
                .Define("GenRhoM_pt",    "GenRhoM_p4.Pt()")
                .Define("GenRhoM_e",     "GenRhoM_p4.E()")
                .Define("GenRhoM_eta",    "GenRhoM_p4.Eta()")
                .Define("GenRhoM_phi",    "GenRhoM_p4.Phi()")
                .Define("GenRhoM_theta",    "GenRhoM_p4.Theta()")
                .Define("GenRhoM_y",     "GenRhoM_p4.Rapidity()")
                .Define("GenRhoM_mass",    "GenRhoM_p4.M()")

                #all final state gen neutrinos and anti-neutrinos
                .Define("GenElectronNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(12, true)(Particle)")
                .Define("GenMuonNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(14, true)(Particle)")
                .Define("GenTauNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(16, true)(Particle)")
                .Define("GenNeutrino1_PID", "FCCAnalyses::MCParticle::mergeParticles(GenElectronNeutrino_PID, GenMuonNeutrino_PID)") #merge all the neutrino flavors into one class, takes two arguments
                .Define("GenNeutrino_PID", "FCCAnalyses::MCParticle::mergeParticles(GenNeutrino1_PID, GenTauNeutrino_PID)") 
                .Define("FSGenNeutrino", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutrino_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenNeutrino", "FCCAnalyses::MCParticle::get_n(FSGenNeutrino)")
                .Define("FSGenNeutrino_e", "FCCAnalyses::MCParticle::get_e(FSGenNeutrino)")
                .Define("FSGenNeutrino_p", "FCCAnalyses::MCParticle::get_p(FSGenNeutrino)")
                .Define("FSGenNeutrino_pt", "FCCAnalyses::MCParticle::get_pt(FSGenNeutrino)")
                .Define("FSGenNeutrino_px", "FCCAnalyses::MCParticle::get_px(FSGenNeutrino)")
                .Define("FSGenNeutrino_py", "FCCAnalyses::MCParticle::get_py(FSGenNeutrino)")
                .Define("FSGenNeutrino_pz", "FCCAnalyses::MCParticle::get_pz(FSGenNeutrino)")
                .Define("FSGenNeutrino_y", "FCCAnalyses::MCParticle::get_y(FSGenNeutrino)")
                .Define("FSGenNeutrino_eta", "FCCAnalyses::MCParticle::get_eta(FSGenNeutrino)")
                .Define("FSGenNeutrino_theta", "FCCAnalyses::MCParticle::get_theta(FSGenNeutrino)")
                .Define("FSGenNeutrino_phi", "FCCAnalyses::MCParticle::get_phi(FSGenNeutrino)")
                .Define("FSGenNeutrino_charge", "FCCAnalyses::MCParticle::get_charge(FSGenNeutrino)")
                #.Define("FSGenNeutrino_parentPDG", "FCCAnalyses::MCParticle::get_parentid(FSGenNeutrino,Particle,Particle0)")
                
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
                .Define("FSGenPhoton_y", "FCCAnalyses::MCParticle::get_y(FSGenPhoton)")
                .Define("FSGenPhoton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenPhoton)")
                .Define("FSGenPhoton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenPhoton)")
                .Define("FSGenPhoton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenPhoton)")
                .Define("FSGenPhoton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenPhoton)")
                #.Define("FSGenPhoton_parentPDG", "FCCAnalyses::MCParticle::get_parentid(FSGenPhoton,Particle,Particle0)")

                .Define("GenHiggs",   "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")
                .Define("n_GenHiggs",   "FCCAnalyses::MCParticle::get_n(GenHiggs)")
                .Define("GenHiggs_e", "FCCAnalyses::MCParticle::get_e(GenHiggs)")
                .Define("GenHiggs_p", "FCCAnalyses::MCParticle::get_p(GenHiggs)")
                .Define("GenHiggs_pt", "FCCAnalyses::MCParticle::get_pt(GenHiggs)")
                .Define("GenHiggs_px", "FCCAnalyses::MCParticle::get_px(GenHiggs)")
                .Define("GenHiggs_py", "FCCAnalyses::MCParticle::get_py(GenHiggs)")
                .Define("GenHiggs_pz", "FCCAnalyses::MCParticle::get_pz(GenHiggs)")
                .Define("GenHiggs_y", "FCCAnalyses::MCParticle::get_y(GenHiggs)")
                .Define("GenHiggs_mass",  "FCCAnalyses::MCParticle::get_mass(GenHiggs)")
                .Define("GenHiggs_eta", "FCCAnalyses::MCParticle::get_eta(GenHiggs)")
                .Define("GenHiggs_theta", "FCCAnalyses::MCParticle::get_theta(GenHiggs)")
                .Define("GenHiggs_phi", "FCCAnalyses::MCParticle::get_phi(GenHiggs)")
                .Define("GenHiggs_charge", "FCCAnalyses::MCParticle::get_charge(GenHiggs)")
                
                ##################
                # Reco particles #
                ##################

                #simple mc to reco association to get pid, only work on the whole classes, not subsets
                .Define("RecoMC_PID", "ReconstructedParticle2MC::getRP2MC_pdg(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                
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
                .Define("RecoElectron_y",     "ReconstructedParticle::get_y(RecoElectrons)")
                .Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
                .Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectron_mass",     "ReconstructedParticle::get_mass(RecoElectrons)")
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                .Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
                .Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
                .Define("RecoElectrons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")

                .Define("n_RecoElectrons_sel",  "ReconstructedParticle::get_n(RecoElectrons_sel)") 
                .Define("RecoElectron_sel_e",      "ReconstructedParticle::get_e(RecoElectrons_sel)")
                .Define("RecoElectron_sel_p",      "ReconstructedParticle::get_p(RecoElectrons_sel)")
                .Define("RecoElectron_sel_pt",      "ReconstructedParticle::get_pt(RecoElectrons_sel)")
                .Define("RecoElectron_sel_px",      "ReconstructedParticle::get_px(RecoElectrons_sel)")
                .Define("RecoElectron_sel_py",      "ReconstructedParticle::get_py(RecoElectrons_sel)")
                .Define("RecoElectron_sel_pz",      "ReconstructedParticle::get_pz(RecoElectrons_sel)")
                .Define("RecoElectron_sel_y",      "ReconstructedParticle::get_y(RecoElectrons_sel)")
                .Define("RecoElectron_sel_eta",     "ReconstructedParticle::get_eta(RecoElectrons_sel)") #pseudorapidity eta
                .Define("RecoElectron_sel_theta",   "ReconstructedParticle::get_theta(RecoElectrons_sel)")
                .Define("RecoElectron_sel_phi",     "ReconstructedParticle::get_phi(RecoElectrons_sel)") #polar angle in the transverse plane phi
                .Define("RecoElectron_sel_charge",  "ReconstructedParticle::get_charge(RecoElectrons_sel)")
                .Define("RecoElectron_sel_mass",     "ReconstructedParticle::get_mass(RecoElectrons_sel)")
                .Define("RecoElectronTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons_sel,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons_sel,EFlowTrack_1)")

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
                .Define("RecoMuon_y",     "ReconstructedParticle::get_y(RecoMuons)")
                .Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
                .Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuon_mass",     "ReconstructedParticle::get_mass(RecoMuons)")
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")

                .Define("RecoMuons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons)")
                .Define("RecoMuons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard, ReconstructedParticles)")
                .Define("RecoMuons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard, RecoMuons_iso)")
                
                .Define("n_RecoMuons_sel",  "ReconstructedParticle::get_n(RecoMuons_sel)") 
                .Define("RecoMuon_sel_e",      "ReconstructedParticle::get_e(RecoMuons_sel)")
                .Define("RecoMuon_sel_p",      "ReconstructedParticle::get_p(RecoMuons_sel)")
                .Define("RecoMuon_sel_pt",      "ReconstructedParticle::get_pt(RecoMuons_sel)")
                .Define("RecoMuon_sel_px",      "ReconstructedParticle::get_px(RecoMuons_sel)")
                .Define("RecoMuon_sel_py",      "ReconstructedParticle::get_py(RecoMuons_sel)")
                .Define("RecoMuon_sel_pz",      "ReconstructedParticle::get_pz(RecoMuons_sel)")
                .Define("RecoMuon_sel_y",      "ReconstructedParticle::get_y(RecoMuons_sel)")
                .Define("RecoMuon_sel_eta",     "ReconstructedParticle::get_eta(RecoMuons_sel)") #pseudorapidity eta
                .Define("RecoMuon_sel_theta",   "ReconstructedParticle::get_theta(RecoMuons_sel)")
                .Define("RecoMuon_sel_phi",     "ReconstructedParticle::get_phi(RecoMuons_sel)") #polar angle in the transverse plane phi
                .Define("RecoMuon_sel_charge",  "ReconstructedParticle::get_charge(RecoMuons_sel)")
                .Define("RecoMuon_sel_mass",     "ReconstructedParticle::get_mass(RecoMuons_sel)")
                .Define("RecoMuonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons_sel,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons_sel,EFlowTrack_1)")

                # LEPTONS
                .Define("RecoLeptons", "ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
                .Define("n_RecoLeptons",  "ReconstructedParticle::get_n(RecoLeptons)") 
                .Define("RecoLepton_e",      "ReconstructedParticle::get_e(RecoLeptons)")
                .Define("RecoLepton_p",      "ReconstructedParticle::get_p(RecoLeptons)")
                .Define("RecoLepton_pt",      "ReconstructedParticle::get_pt(RecoLeptons)")
                .Define("RecoLepton_px",      "ReconstructedParticle::get_px(RecoLeptons)")
                .Define("RecoLepton_py",      "ReconstructedParticle::get_py(RecoLeptons)")
                .Define("RecoLepton_pz",      "ReconstructedParticle::get_pz(RecoLeptons)")
                .Define("RecoLepton_y",      "ReconstructedParticle::get_y(RecoLeptons)")
                .Define("RecoLepton_eta",     "ReconstructedParticle::get_eta(RecoLeptons)") #pseudorapidity eta
                .Define("RecoLepton_theta",   "ReconstructedParticle::get_theta(RecoLeptons)")
                .Define("RecoLepton_phi",     "ReconstructedParticle::get_phi(RecoLeptons)") #polar angle in the transverse plane phi
                .Define("RecoLepton_charge",  "ReconstructedParticle::get_charge(RecoLeptons)")
                .Define("RecoLepton_mass",     "ReconstructedParticle::get_mass(RecoLeptons)")
                .Define("RecoLeptonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons,EFlowTrack_1))") #significance
                .Define("RecoLeptonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoLeptonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons,EFlowTrack_1)")

                .Define("RecoLeptons_sel", "ReconstructedParticle::merge(RecoElectrons_sel, RecoMuons_sel)")
                .Define("n_RecoLeptons_sel",  "ReconstructedParticle::get_n(RecoLeptons_sel)") 
                .Define("RecoLepton_sel_e",      "ReconstructedParticle::get_e(RecoLeptons_sel)")
                .Define("RecoLepton_sel_p",      "ReconstructedParticle::get_p(RecoLeptons_sel)")
                .Define("RecoLepton_sel_pt",      "ReconstructedParticle::get_pt(RecoLeptons_sel)")
                .Define("RecoLepton_sel_px",      "ReconstructedParticle::get_px(RecoLeptons_sel)")
                .Define("RecoLepton_sel_py",      "ReconstructedParticle::get_py(RecoLeptons_sel)")
                .Define("RecoLepton_sel_pz",      "ReconstructedParticle::get_pz(RecoLeptons_sel)")
                .Define("RecoLepton_sel_y",      "ReconstructedParticle::get_y(RecoLeptons_sel)")
                .Define("RecoLepton_sel_eta",     "ReconstructedParticle::get_eta(RecoLeptons_sel)") #pseudorapidity eta
                .Define("RecoLepton_sel_theta",   "ReconstructedParticle::get_theta(RecoLeptons_sel)")
                .Define("RecoLepton_sel_phi",     "ReconstructedParticle::get_phi(RecoLeptons_sel)") #polar angle in the transverse plane phi
                .Define("RecoLepton_sel_charge",  "ReconstructedParticle::get_charge(RecoLeptons_sel)")
                .Define("RecoLepton_sel_mass",     "ReconstructedParticle::get_mass(RecoLeptons_sel)")
                .Define("RecoLeptonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons_sel,EFlowTrack_1))") #significance
                .Define("RecoLeptonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoLeptonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons_sel,EFlowTrack_1)")
                .Define("RecoLepton_sel_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_sel_px, RecoLepton_sel_py, RecoLepton_sel_pz, RecoLepton_sel_e)")

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
		        .Define("RecoPhoton_y",     "ReconstructedParticle::get_y(RecoPhotons)") 
		        .Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
                .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		        .Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
                .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")
                .Define("RecoPhoton_mass",  "ReconstructedParticle::get_mass(RecoPhotons)")

                # different definition of missing energy from fccanalysis classes instead of edm4hep
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(240, ReconstructedParticles)") #ecm 
                .Define("RecoEmiss_px",  "RecoEmiss[0].momentum.x")
                .Define("RecoEmiss_py",  "RecoEmiss[0].momentum.y")
                .Define("RecoEmiss_pz",  "RecoEmiss[0].momentum.z")
                .Define("RecoEmiss_pt",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
                .Define("RecoEmiss_p",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
                .Define("RecoEmiss_e",   "RecoEmiss[0].energy")
                .Define("RecoEmiss_p4",  "TLorentzVector(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
                .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
                .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
                .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
                .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
                .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

                # JETS, reclustered from the reconstructed particles, never use the class in the samples
                ### https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h ###

                .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,RecoMuons_sel)")
                .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,RecoElectrons_sel)")

                .Define("Photons_excl",   "ReconstructedParticles[ReconstructedParticles.type == 22 && ReconstructedParticles.energy < 2]") #this considers all photons with type 22 

                .Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoLeps,Photons_excl)")
            
                .Define("RP_px_sel",          "ReconstructedParticle::get_px(ReconstructedParticlesJET)")
                .Define("RP_py_sel",          "ReconstructedParticle::get_py(ReconstructedParticlesJET)")
                .Define("RP_pz_sel",          "ReconstructedParticle::get_pz(ReconstructedParticlesJET)")
                .Define("RP_e_sel",           "ReconstructedParticle::get_e(ReconstructedParticlesJET)")
                .Define("RP_m_sel",           "ReconstructedParticle::get_mass(ReconstructedParticlesJET)")
                .Define("RP_q_sel",           "ReconstructedParticle::get_charge(ReconstructedParticlesJET)")
                #.Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets_sel",  "JetClusteringUtils::set_pseudoJets(RP_px_sel, RP_py_sel, RP_pz_sel, RP_e_sel)" )

                .Define("NoMuons", "ReconstructedParticle::remove(ReconstructedParticles, RecoMuons)")
                .Define("NoLeptons", "ReconstructedParticle::remove(NoMuons, RecoElectrons)")

                .Define("ChargedHadron", "ReconstructedParticle::sel_charge(1, true) (NoLeptons)")
                .Define("n_ChargedHadron",      "ReconstructedParticle::get_n(ChargedHadron)") 
                .Define("ChargedHadron_e",      "ReconstructedParticle::get_e(ChargedHadron)")
                .Define("ChargedHadron_p",      "ReconstructedParticle::get_p(ChargedHadron)")
                .Define("ChargedHadron_pt",      "ReconstructedParticle::get_pt(ChargedHadron)")
                .Define("ChargedHadron_px",      "ReconstructedParticle::get_px(ChargedHadron)")
                .Define("ChargedHadron_py",      "ReconstructedParticle::get_py(ChargedHadron)")
                .Define("ChargedHadron_pz",      "ReconstructedParticle::get_pz(ChargedHadron)")
		        .Define("ChargedHadron_eta",     "ReconstructedParticle::get_eta(ChargedHadron)") #pseudorapidity eta
                .Define("ChargedHadron_theta",   "ReconstructedParticle::get_theta(ChargedHadron)")
		        .Define("ChargedHadron_phi",     "ReconstructedParticle::get_phi(ChargedHadron)") #polar angle in the transverse plane phi
                .Define("ChargedHadron_charge",  "ReconstructedParticle::get_charge(ChargedHadron)")
                .Define("ChargedHadron_mass",  "ReconstructedParticle::get_mass(ChargedHadron)")
                .Define("ChargedHadron_p4",  "FCCAnalyses::ZHfunctions::build_p4(ChargedHadron_px, ChargedHadron_py, ChargedHadron_pz, ChargedHadron_e)")

                .Define("NeutralHadron_cand",   "ReconstructedParticles[ReconstructedParticles.type != 22]") #this instead excludes all photons with type 22, type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                .Define("NeutralHadron",       "ReconstructedParticle::sel_charge(0, true) (NeutralHadron_cand)")
                .Define("n_NeutralHadron",  "ReconstructedParticle::get_n(NeutralHadron)") #count how many photons are in the event in total
                .Define("NeutralHadron_e",      "ReconstructedParticle::get_e(NeutralHadron)")
                .Define("NeutralHadron_p",      "ReconstructedParticle::get_p(NeutralHadron)")
                .Define("NeutralHadron_pt",      "ReconstructedParticle::get_pt(NeutralHadron)")
                .Define("NeutralHadron_px",      "ReconstructedParticle::get_px(NeutralHadron)")
                .Define("NeutralHadron_py",      "ReconstructedParticle::get_py(NeutralHadron)")
                .Define("NeutralHadron_pz",      "ReconstructedParticle::get_pz(NeutralHadron)")
		        .Define("NeutralHadron_eta",     "ReconstructedParticle::get_eta(NeutralHadron)") #pseudorapidity eta
                .Define("NeutralHadron_theta",   "ReconstructedParticle::get_theta(NeutralHadron)")
		        .Define("NeutralHadron_phi",     "ReconstructedParticle::get_phi(NeutralHadron)") #polar angle in the transverse plane phi
                .Define("NeutralHadron_charge",  "ReconstructedParticle::get_charge(NeutralHadron)")
                .Define("NeutralHadron_mass",  "ReconstructedParticle::get_mass(NeutralHadron)")
                .Define("NeutralHadron_p4",  "FCCAnalyses::ZHfunctions::build_p4(NeutralHadron_px, NeutralHadron_py, NeutralHadron_pz, NeutralHadron_e)")

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
        collections_noleps["PFParticles"] = "ReconstructedParticlesJET"

        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 0.5, 2, "R5"
        )
        df2 = jetClusteringHelper_R5.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_R5.define(df2)

        ## tagger inference
        df2 = jetFlavourHelper_R5.inference(weaver_preproc, weaver_model, df2)

        df2 = (df2
                .Define("TagJet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("TagJet_R5_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets))
                .Define("n_TagJet_R5_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5",           "return TagJet_R5_e.size()")
                .Define("TagJet_R5_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_R5.constituents))

                .Define("TagJet_R5_isG",    "recojet_isG_R5")
                .Define("TagJet_R5_isU",    "recojet_isU_R5")
                .Define("TagJet_R5_isD",    "recojet_isD_R5")
                .Define("TagJet_R5_isS",    "recojet_isS_R5")
                .Define("TagJet_R5_isC",    "recojet_isC_R5")
                .Define("TagJet_R5_isB",    "recojet_isB_R5")
                .Define("TagJet_R5_isTAU",    "recojet_isTAU_R5")

                .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 0)".format(jetClusteringHelper_R5.constituents)) 
                .Define("TauFromJet_R5_type_sel","ReconstructedParticle::get_type(TauFromJet_R5)")
                .Define("TauFromJet_R5_tau", "TauFromJet_R5[TauFromJet_R5_type_sel>=0]") 
                .Define("TauFromJet_R5_p","ReconstructedParticle::get_p(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pt","ReconstructedParticle::get_pt(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_px","ReconstructedParticle::get_px(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_py","ReconstructedParticle::get_py(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pz","ReconstructedParticle::get_pz(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_theta","ReconstructedParticle::get_theta(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_phi","ReconstructedParticle::get_phi(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_eta","ReconstructedParticle::get_eta(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_y","ReconstructedParticle::get_y(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_e","ReconstructedParticle::get_e(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_charge","ReconstructedParticle::get_charge(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_type","ReconstructedParticle::get_type(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_mass","ReconstructedParticle::get_mass(TauFromJet_R5_tau)")
                .Define("n_TauFromJet_R5","TauFromJet_R5_pt.size()")

                .Define("TagJet_R5_sel_e",      "TagJet_R5_e[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_p",      "TagJet_R5_p[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_pt",      "TagJet_R5_pt[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_px",      "TagJet_R5_px[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_py",      "TagJet_R5_py[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_pz",      "TagJet_R5_pz[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
		        .Define("TagJet_R5_sel_eta",     "TagJet_R5_eta[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_theta",   "TagJet_R5_theta[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
		        .Define("TagJet_R5_sel_phi",     "TagJet_R5_phi[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("TagJet_R5_sel_mass",      "TagJet_R5_mass[TauFromJet_R5_type_sel<0 && TagJet_R5_cleanup==1]")
                .Define("n_TagJet_R5_sel", "TagJet_R5_sel_e.size()")

                #get the leading charged particle in the tau jet, if only neutral particles are present then the particle is null
                .Define("ChargedTau_all",      "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 1)".format(jetClusteringHelper_R5.constituents))
                .Define("ChargedTau_type",      "ReconstructedParticle::get_type(ChargedTau_all)") 
                .Define("ChargedTau",      "ChargedTau_all[ChargedTau_type>=0]") 
                .Define("n_ChargedTau",      "ReconstructedParticle::get_n(ChargedTau)") 
                .Define("ChargedTau_e",      "ReconstructedParticle::get_e(ChargedTau)")
                .Define("ChargedTau_p",      "ReconstructedParticle::get_p(ChargedTau)")
                .Define("ChargedTau_pt",      "ReconstructedParticle::get_pt(ChargedTau)")
                .Define("ChargedTau_px",      "ReconstructedParticle::get_px(ChargedTau)")
                .Define("ChargedTau_py",      "ReconstructedParticle::get_py(ChargedTau)")
                .Define("ChargedTau_pz",      "ReconstructedParticle::get_pz(ChargedTau)")
		        .Define("ChargedTau_eta",     "ReconstructedParticle::get_eta(ChargedTau)") #pseudorapidity eta
                .Define("ChargedTau_theta",   "ReconstructedParticle::get_theta(ChargedTau)")
		        .Define("ChargedTau_phi",     "ReconstructedParticle::get_phi(ChargedTau)") #polar angle in the transverse plane phi
                .Define("ChargedTau_charge",  "ReconstructedParticle::get_charge(ChargedTau)")
                .Define("ChargedTau_mass",  "ReconstructedParticle::get_mass(ChargedTau)")
                .Define("ChargedTau_p4",  "FCCAnalyses::ZHfunctions::build_p4(ChargedTau_px, ChargedTau_py, ChargedTau_pz, ChargedTau_e)")

                #get the neutral hadronic system for the tau jet, all in one "particle" variable, photons are kept separetely but would be related in pairs to pi0
                .Define("NeutralTau_all",      "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 2)".format(jetClusteringHelper_R5.constituents))
                .Define("NeutralTau_type",      "ReconstructedParticle::get_type(NeutralTau_all)") 
                .Define("NeutralTau",      "NeutralTau_all[NeutralTau_type>=0]") 
                .Define("n_NeutralTau",      "ReconstructedParticle::get_n(NeutralTau)") 
                .Define("NeutralTau_e",      "ReconstructedParticle::get_e(NeutralTau)")
                .Define("NeutralTau_p",      "ReconstructedParticle::get_p(NeutralTau)")
                .Define("NeutralTau_pt",      "ReconstructedParticle::get_pt(NeutralTau)")
                .Define("NeutralTau_px",      "ReconstructedParticle::get_px(NeutralTau)")
                .Define("NeutralTau_py",      "ReconstructedParticle::get_py(NeutralTau)")
                .Define("NeutralTau_pz",      "ReconstructedParticle::get_pz(NeutralTau)")
		        .Define("NeutralTau_eta",     "ReconstructedParticle::get_eta(NeutralTau)") #pseudorapidity eta
                .Define("NeutralTau_theta",   "ReconstructedParticle::get_theta(NeutralTau)")
		        .Define("NeutralTau_phi",     "ReconstructedParticle::get_phi(NeutralTau)") #polar angle in the transverse plane phi
                .Define("NeutralTau_charge",  "ReconstructedParticle::get_charge(NeutralTau)")
                .Define("NeutralTau_mass",  "ReconstructedParticle::get_mass(NeutralTau)")
                .Define("NeutralTau_p4",  "FCCAnalyses::ZHfunctions::build_p4(NeutralTau_px, NeutralTau_py, NeutralTau_pz, NeutralTau_e)") 

                #get the leading charged particle in the jet, if only neutral particles are present then the particle is null
                .Define("ChargedJet_temp",      "FCCAnalyses::ZHfunctions::Jet_Charged({})".format(jetClusteringHelper_R5.constituents))
                .Define("ChargedJet",           "ChargedJet_temp[TagJet_R5_cleanup==1 && TagJet_R5_isTAU>0.5]")
                .Define("n_ChargedJet",      "ReconstructedParticle::get_n(ChargedJet)") 
                .Define("ChargedJet_e",      "ReconstructedParticle::get_e(ChargedJet)")
                .Define("ChargedJet_p",      "ReconstructedParticle::get_p(ChargedJet)")
                .Define("ChargedJet_pt",      "ReconstructedParticle::get_pt(ChargedJet)")
                .Define("ChargedJet_px",      "ReconstructedParticle::get_px(ChargedJet)")
                .Define("ChargedJet_py",      "ReconstructedParticle::get_py(ChargedJet)")
                .Define("ChargedJet_pz",      "ReconstructedParticle::get_pz(ChargedJet)")
		        .Define("ChargedJet_eta",     "ReconstructedParticle::get_eta(ChargedJet)") #pseudorapidity eta
                .Define("ChargedJet_theta",   "ReconstructedParticle::get_theta(ChargedJet)")
		        .Define("ChargedJet_phi",     "ReconstructedParticle::get_phi(ChargedJet)") #polar angle in the transverse plane phi
                .Define("ChargedJet_charge",  "ReconstructedParticle::get_charge(ChargedJet)")
                .Define("ChargedJet_mass",  "ReconstructedParticle::get_mass(ChargedJet)")
                .Define("ChargedJet_p4",  "FCCAnalyses::ZHfunctions::build_p4(ChargedJet_px, ChargedJet_py, ChargedJet_pz, ChargedJet_e)")

                #get the neutral hadronic system for the jet, all in one "particle" variable, photons are kept separetely but would be related in pairs to pi0
                .Define("NeutralJet_temp",      "FCCAnalyses::ZHfunctions::Jet_Neutral({})".format(jetClusteringHelper_R5.constituents))
                .Define("NeutralJet",           "NeutralJet_temp[TagJet_R5_cleanup==1 && TagJet_R5_isTAU>0.5]")
                .Define("n_NeutralJet",      "ReconstructedParticle::get_n(NeutralJet)") 
                .Define("NeutralJet_e",      "ReconstructedParticle::get_e(NeutralJet)")
                .Define("NeutralJet_p",      "ReconstructedParticle::get_p(NeutralJet)")
                .Define("NeutralJet_pt",      "ReconstructedParticle::get_pt(NeutralJet)")
                .Define("NeutralJet_px",      "ReconstructedParticle::get_px(NeutralJet)")
                .Define("NeutralJet_py",      "ReconstructedParticle::get_py(NeutralJet)")
                .Define("NeutralJet_pz",      "ReconstructedParticle::get_pz(NeutralJet)")
		        .Define("NeutralJet_eta",     "ReconstructedParticle::get_eta(NeutralJet)") #pseudorapidity eta
                .Define("NeutralJet_theta",   "ReconstructedParticle::get_theta(NeutralJet)")
		        .Define("NeutralJet_phi",     "ReconstructedParticle::get_phi(NeutralJet)") #polar angle in the transverse plane phi
                .Define("NeutralJet_charge",  "ReconstructedParticle::get_charge(NeutralJet)")
                .Define("NeutralJet_mass",  "ReconstructedParticle::get_mass(NeutralJet)")
                .Define("NeutralJet_p4",  "FCCAnalyses::ZHfunctions::build_p4(NeutralJet_px, NeutralJet_py, NeutralJet_pz, NeutralJet_e)") 

                ### now i want to study the thadronic tau reconstruction with the function and the jet tagger by comparing it to the gen info for taus decaying not to electrons or muons

                .Define("GenTau_el",       "FCCAnalyses::MCParticle::sel_daughterID(-11, false, true)(HiggsGenTau,Particle,Particle1)")
                .Define("HadGenTau",       "FCCAnalyses::MCParticle::sel_daughterID(-13, false, true)(GenTau_el,Particle,Particle1)")
                .Define("HadGenTau_e",     "FCCAnalyses::MCParticle::get_e(HadGenTau)")
                .Define("HadGenTau_p",     "FCCAnalyses::MCParticle::get_p(HadGenTau)")
                .Define("HadGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(HadGenTau)")
                .Define("HadGenTau_px",     "FCCAnalyses::MCParticle::get_px(HadGenTau)")
                .Define("HadGenTau_py",     "FCCAnalyses::MCParticle::get_py(HadGenTau)")
                .Define("HadGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(HadGenTau)")
                .Define("HadGenTau_y",    "FCCAnalyses::MCParticle::get_y(HadGenTau)")
                .Define("HadGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(HadGenTau)")
                .Define("HadGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(HadGenTau)")
                .Define("HadGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(HadGenTau)")
                .Define("HadGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(HadGenTau,Particle,Particle0)")
                .Define("HadGenTau_charge", "FCCAnalyses::MCParticle::get_charge(HadGenTau)")
                .Define("HadGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(HadGenTau)")
                .Define("n_GenTau_had",     "HadGenTau_eta.size()")

                .Define("TauTag_eta_sel",      "TagJet_R5_eta[TagJet_R5_isTAU>0.9 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_phi_sel",      "TagJet_R5_phi[TagJet_R5_isTAU>0.9 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_sel_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_sel, HadGenTau_phi, TauTag_eta_sel, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_R5_match",          "if (n_GenTau_had>0) return TauTag_sel_idx.size(); else return TauTag_eta_sel.size();")

                .Define("TauTag_eta_selmass",      "TagJet_R5_eta[TagJet_R5_isTAU>0.9 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3 && TagJet_R5_mass<3]")
                .Define("TauTag_phi_selmass",      "TagJet_R5_phi[TagJet_R5_isTAU>0.9 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3 && TagJet_R5_mass<3]")
                .Define("TauTag_selmass_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_selmass, HadGenTau_phi, TauTag_eta_selmass, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_R5_mass_match",          "if (n_GenTau_had>0) return TauTag_selmass_idx.size(); else return TauTag_eta_selmass.size();")

                .Define("TauTag_eta_sel5",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1]")
                .Define("TauTag_phi_sel5",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1]")
                .Define("TauTag_sel5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_sel5, HadGenTau_phi, TauTag_eta_sel5, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_R5_match5",          "if (n_GenTau_had>0) return TauTag_sel5_idx.size(); else return TauTag_eta_sel5.size();")

                .Define("TauTag_eta_selmass5",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_phi_selmass5",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_selmass5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_selmass5, HadGenTau_phi, TauTag_eta_selmass5, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_R5_mass_match5",          "if (n_GenTau_had>0) return TauTag_selmass5_idx.size(); else return TauTag_eta_selmass5.size();")

                .Define("TauFromJet_R5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauFromJet_R5_phi, HadGenTau_phi, TauFromJet_R5_eta, HadGenTau_eta, 0.2)")
                .Define("n_TauFromJet_R5_match",          "if (n_GenTau_had>0) return TauFromJet_R5_idx.size(); else return n_TauFromJet_R5;")

                .Define("n_events_tag",       "if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_tag_mass",       "if (n_GenTau_had==n_TauTag_R5_mass_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_mass_match && n_GenTau_had==2) return 2;  else if (n_GenTau_had==n_TauTag_R5_mass_match && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_tag5",       "if (n_GenTau_had==n_TauTag_R5_match5 && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_match5 && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_R5_match5 && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_tag5_mass",       "if (n_GenTau_had==n_TauTag_R5_mass_match5 && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_mass_match5 && n_GenTau_had==2) return 2;  else if (n_GenTau_had==n_TauTag_R5_mass_match5 && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_func",       "if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==0) return 0; else return -1;")

                # varibales for the CP to save here in stage1

                #first of all get the IP from the Z daughters

                #.Define("RecoElectronSelTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoElectrons_sel, EFlowTrack_1)") ### EFlowTrack_1 contains all tracks, selecting a subset associated with certain particles ###
                #.Define("RecoMuonSelTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoMuons_sel, EFlowTrack_1)")
                #.Define("RecoLeptonSelTracks",   "ReconstructedTrack::Merge( RecoElectronSelTracks, RecoMuonSelTracks)")

                #.Define("RecoDecayVertexObjectZ",   "VertexFitterSimple::VertexFitter_Tk( 0, RecoElectronTracks)" ) ### reconstructing a vertex withour any request n=0 ###
                #.Define("RecoDecayVertexZ",  "VertexingUtils::get_VertexData( RecoDecayVertexObjectZ )")
                #.Define("RecoIP_p4",     "TLorentzVector(RecoDecayVertexZ.position.x, RecoDecayVertexZ.position.y, RecoDecayVertexZ.position.z, 0.)")

                #hen get the impact vector from the new IP to the charged hadron track
                #for now we use the collision point and the phi and vector of the particle at the origin as proxi for the IP, phi at d0 and vector at d0
                
                .Define("RecoChargedHadronTrack",   "ReconstructedParticle2Track::getRP2TRK( ChargedHadron, EFlowTrack_1)")
                .Define("RecoChargedHadronTrack_D0", "ReconstructedParticle2Track::getRP2TRK_D0(ChargedHadron,EFlowTrack_1)")
                .Define("RecoChargedHadronTrack_Z0", "ReconstructedParticle2Track::getRP2TRK_Z0(ChargedHadron,EFlowTrack_1)")
                .Define("RecoChargedHadronTrack_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(ChargedHadron,EFlowTrack_1)") #significance
                .Define("RecoChargedHadronTrack_Z0sig", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(ChargedHadron,EFlowTrack_1)")
                .Define("RecoChargedHadronTrack_charge", "ReconstructedParticle2Track::getRP2TRK_charge(ChargedHadron,EFlowTrack_1)")
                .Define("RecoChargedHadronTrack_omega", "ReconstructedParticle2Track::getRP2TRK_omega(ChargedHadron,EFlowTrack_1)")

                .Define("ChargedHadronImpact_p4",     "FCCAnalyses::ZHfunctions::ImpactVector(ChargedHadron_p4, RecoChargedHadronTrack_D0, RecoChargedHadronTrack_Z0)")

                .Define("RecoChargedTauTrack",   "ReconstructedParticle2Track::getRP2TRK( ChargedTau, EFlowTrack_1)")
                .Define("RecoChargedTauTrack_D0", "ReconstructedParticle2Track::getRP2TRK_D0(ChargedTau,EFlowTrack_1)")
                .Define("RecoChargedTauTrack_Z0", "ReconstructedParticle2Track::getRP2TRK_Z0(ChargedTau,EFlowTrack_1)")
                .Define("RecoChargedTauTrack_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(ChargedTau,EFlowTrack_1)") #significance
                .Define("RecoChargedTauTrack_Z0sig", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(ChargedTau,EFlowTrack_1)")
                .Define("RecoChargedTauTrack_charge", "ReconstructedParticle2Track::getRP2TRK_charge(ChargedTau,EFlowTrack_1)")
                .Define("RecoChargedTauTrack_omega", "ReconstructedParticle2Track::getRP2TRK_omega(ChargedTau,EFlowTrack_1)")

                .Define("ChargedTauImpact_p4",     "FCCAnalyses::ZHfunctions::ImpactVector(ChargedTau_p4, RecoChargedTauTrack_D0, RecoChargedTauTrack_Z0)")
                
                .Define("RecoChargedJetTrack",   "ReconstructedParticle2Track::getRP2TRK( ChargedJet, EFlowTrack_1)")
                .Define("RecoChargedJetTrack_D0", "ReconstructedParticle2Track::getRP2TRK_D0(ChargedJet,EFlowTrack_1)")
                .Define("RecoChargedJetTrack_Z0", "ReconstructedParticle2Track::getRP2TRK_Z0(ChargedJet,EFlowTrack_1)")
                .Define("RecoChargedJetTrack_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(ChargedJet,EFlowTrack_1)") #significance
                .Define("RecoChargedJetTrack_Z0sig", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(ChargedJet,EFlowTrack_1)")
                .Define("RecoChargedJetTrack_charge", "ReconstructedParticle2Track::getRP2TRK_charge(ChargedJet,EFlowTrack_1)")
                .Define("RecoChargedJetTrack_omega", "ReconstructedParticle2Track::getRP2TRK_omega(ChargedJet,EFlowTrack_1)")

                .Define("ChargedJetImpact_p4",     "FCCAnalyses::ZHfunctions::ImpactVector(ChargedJet_p4, RecoChargedJetTrack_D0, RecoChargedJetTrack_Z0)")

                .Define("RecoLeptonTrack",   "ReconstructedParticle2Track::getRP2TRK( RecoLeptons_sel, EFlowTrack_1)")
                .Define("RecoLeptonTrack_D0", "ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons_sel,EFlowTrack_1)")
                .Define("RecoLeptonTrack_Z0", "ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons_sel,EFlowTrack_1)")
                .Define("RecoLeptonTrack_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons_sel,EFlowTrack_1)") #significance
                .Define("RecoLeptonTrack_Z0sig", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons_sel,EFlowTrack_1)")
                .Define("RecoLeptonTrack_charge", "ReconstructedParticle2Track::getRP2TRK_charge(RecoLeptons_sel,EFlowTrack_1)")
                .Define("RecoLeptonTrack_omega", "ReconstructedParticle2Track::getRP2TRK_omega(RecoLeptons_sel,EFlowTrack_1)")

                .Define("LeptonImpact_p4",     "FCCAnalyses::ZHfunctions::ImpactVector(RecoLepton_sel_p4, RecoLeptonTrack_D0, RecoLeptonTrack_Z0)")

                # reconstructed tracks
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")
                .Define("RecoVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 0, EFlowTrack_1)" ) ### reconstructing a vertex withour any request n=0 ###
                .Define("RecoVertex",  "VertexingUtils::get_VertexData( RecoVertexObject )")

                .Define("PrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)") 
                .Define("n_PrimaryTracks",  "ReconstructedParticle2Track::getTK_n( PrimaryTracks )")
                .Define("PrimaryVertexObject", "VertexFitterSimple::VertexFitter_Tk(1, PrimaryTracks, true, 4.5, 20e-3, 300)")
                .Define("PrimaryVertex",  "VertexingUtils::get_VertexData( PrimaryVertexObject )")
                .Define("RecoIP_p4",        "TLorentzVector(PrimaryVertex.position.x, PrimaryVertex.position.y, PrimaryVertex.position.z, 0.)")
                
                .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1, PrimaryTracks )")
                .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )
                .Define("SecondaryVertexObject", "VertexFitterSimple::VertexFitter_Tk(2, SecondaryTracks)")
                .Define("SecondaryVertex",  "VertexingUtils::get_VertexData( SecondaryVertexObject )")
                
                # MC vertex association
                #.Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(3)( Particle )" )
                .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
                .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject, ReconstructedParticles, EFlowTrack_1, MCRecoAssociations0, MCRecoAssociations1)")
                .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0, MCRecoAssociations1, Particle)")
                .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

                ### LCFIPlus algorithm for secondary vertices ###
                #find the DVs
                #ROOT::VecOps::RVec<edm4hep::TrackState> np_tracks, ROOT::VecOps::RVec<edm4hep::TrackState> thetracks, VertexingUtils::FCCAnalysesVertex PV, bool V0_rej, double chi2_cut, double invM_cut, double chi2Tr_cut)
                .Define("RecoDVs", "VertexFinderLCFIPlus::get_SV_event(SecondaryTracks, EFlowTrack_1, PrimaryVertexObject, true, 10., 5., 5.)")
                #find number of DVs
                .Define("n_RecoDVs", "VertexingUtils::get_n_SV(RecoDVs)")
                # DV position in 3d (TVector3) from the origin
                .Define("DV_p3", "VertexingUtils::get_position_SV(RecoDVs)")
                
                
        )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
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

            "n_HiggsGenTau",
            "HiggsGenTau_e",
            "HiggsGenTau_p",
            "HiggsGenTau_pt",
            "HiggsGenTau_px",
            "HiggsGenTau_py",
            "HiggsGenTau_pz",
            "HiggsGenTau_y",
            "HiggsGenTau_eta",
            "HiggsGenTau_theta",
            "HiggsGenTau_phi",
            "HiggsGenTau_charge",
            "HiggsGenTau_mass",
            "HiggsGenTau_parentPDG",
            "HiggsGenTau_vertex_x",
            "HiggsGenTau_vertex_y",
            "HiggsGenTau_vertex_z",

            "n_GenTau",
            "GenTau_e",
            "GenTau_p",
            "GenTau_pt",
            "GenTau_px",
            "GenTau_py",
            "GenTau_pz",
            "GenTau_y",
            "GenTau_eta",
            "GenTau_theta",
            "GenTau_phi",
            "GenTau_charge",
            "GenTau_mass",
            "GenTau_parentPDG",
            "GenTau_vertex_x",
            "GenTau_vertex_y",
            "GenTau_vertex_z",

            "GenNuP_e",
            "GenNuP_p",
            "GenNuP_pt",
            "GenNuP_px",
            "GenNuP_py",
            "GenNuP_pz",
            "GenNuP_y",
            "GenNuP_eta",
            "GenNuP_theta",
            "GenNuP_phi",
            "GenNuP_charge",
            "GenNuP_mass",
            "GenNuP_p4",
            "GenNuP_Impact_p4",

            "GenNuM_e",
            "GenNuM_p",
            "GenNuM_pt",
            "GenNuM_px",
            "GenNuM_py",
            "GenNuM_pz",
            "GenNuM_y",
            "GenNuM_eta",
            "GenNuM_theta",
            "GenNuM_phi",
            "GenNuM_charge",
            "GenNuM_mass",
            "GenNuM_p4",
            "GenNuM_Impact_p4",

            "GenPiP_e",
            "GenPiP_p",
            "GenPiP_pt",
            "GenPiP_px",
            "GenPiP_py",
            "GenPiP_pz",
            "GenPiP_y",
            "GenPiP_eta",
            "GenPiP_theta",
            "GenPiP_phi",
            "GenPiP_charge",
            "GenPiP_mass",
            "GenPiP_p4",
            #"GenPiP_Impact_p4",

            "GenPiM_e",
            "GenPiM_p",
            "GenPiM_pt",
            "GenPiM_px",
            "GenPiM_py",
            "GenPiM_pz",
            "GenPiM_y",
            "GenPiM_eta",
            "GenPiM_theta",
            "GenPiM_phi",
            "GenPiM_charge",
            "GenPiM_mass",
            "GenPiM_p4",
            #"GenPiM_Impact_p4",

            "GenPiP1_e",
            "GenPiP1_p",
            "GenPiP1_pt",
            "GenPiP1_px",
            "GenPiP1_py",
            "GenPiP1_pz",
            "GenPiP1_y",
            "GenPiP1_eta",
            "GenPiP1_theta",
            "GenPiP1_phi",
            "GenPiP1_charge",
            "GenPiP1_mass",
            "GenPiP1_p4",
            #"GenPiP1_Impact_p4",

            "GenPiM1_e",
            "GenPiM1_p",
            "GenPiM1_pt",
            "GenPiM1_px",
            "GenPiM1_py",
            "GenPiM1_pz",
            "GenPiM1_y",
            "GenPiM1_eta",
            "GenPiM1_theta",
            "GenPiM1_phi",
            "GenPiM1_charge",
            "GenPiM1_mass",
            "GenPiM1_p4",

            "GenPiP2_e",
            "GenPiP2_p",
            "GenPiP2_pt",
            "GenPiP2_px",
            "GenPiP2_py",
            "GenPiP2_pz",
            "GenPiP2_y",
            "GenPiP2_eta",
            "GenPiP2_theta",
            "GenPiP2_phi",
            "GenPiP2_charge",
            "GenPiP2_mass",
            "GenPiP2_p4",
            #"GenPiP2_Impact_p4",

            "GenPiM2_e",
            "GenPiM2_p",
            "GenPiM2_pt",
            "GenPiM2_px",
            "GenPiM2_py",
            "GenPiM2_pz",
            "GenPiM2_y",
            "GenPiM2_eta",
            "GenPiM2_theta",
            "GenPiM2_phi",
            "GenPiM2_charge",
            "GenPiM2_mass",
            "GenPiM2_p4",
            #"GenPiM2_Impact_p4",

            "GenPiP3_e",
            "GenPiP3_p",
            "GenPiP3_pt",
            "GenPiP3_px",
            "GenPiP3_py",
            "GenPiP3_pz",
            "GenPiP3_y",
            "GenPiP3_eta",
            "GenPiP3_theta",
            "GenPiP3_phi",
            "GenPiP3_charge",
            "GenPiP3_mass",
            "GenPiP3_p4",
            #"GenPiP3_Impact_p4",

            "GenPiM3_e",
            "GenPiM3_p",
            "GenPiM3_pt",
            "GenPiM3_px",
            "GenPiM3_py",
            "GenPiM3_pz",
            "GenPiM3_y",
            "GenPiM3_eta",
            "GenPiM3_theta",
            "GenPiM3_phi",
            "GenPiM3_charge",
            "GenPiM3_mass",
            "GenPiM3_p4",
            #"GenPiM3_Impact_p4",

            "GenPi0P1_e",
            "GenPi0P1_p",
            "GenPi0P1_pt",
            "GenPi0P1_px",
            "GenPi0P1_py",
            "GenPi0P1_pz",
            "GenPi0P1_y",
            "GenPi0P1_eta",
            "GenPi0P1_theta",
            "GenPi0P1_phi",
            "GenPi0P1_mass",
            "GenPi0P1_p4",

            "GenPi0P2_e",
            "GenPi0P2_p",
            "GenPi0P2_pt",
            "GenPi0P2_px",
            "GenPi0P2_py",
            "GenPi0P2_pz",
            "GenPi0P2_y",
            "GenPi0P2_eta",
            "GenPi0P2_theta",
            "GenPi0P2_phi",
            "GenPi0P2_mass",
            "GenPi0P2_p4",

            "GenRhoP_e",
            "GenRhoP_p",
            "GenRhoP_pt",
            "GenRhoP_px",
            "GenRhoP_py",
            "GenRhoP_pz",
            "GenRhoP_y",
            "GenRhoP_eta",
            "GenRhoP_theta",
            "GenRhoP_phi",
            "GenRhoP_mass",
            "GenRhoP_p4",

            "GenPi0M1_e",
            "GenPi0M1_p",
            "GenPi0M1_pt",
            "GenPi0M1_px",
            "GenPi0M1_py",
            "GenPi0M1_pz",
            "GenPi0M1_y",
            "GenPi0M1_eta",
            "GenPi0M1_theta",
            "GenPi0M1_phi",
            "GenPi0M1_mass",
            "GenPi0M1_p4",

            "GenPi0M2_e",
            "GenPi0M2_p",
            "GenPi0M2_pt",
            "GenPi0M2_px",
            "GenPi0M2_py",
            "GenPi0M2_pz",
            "GenPi0M2_y",
            "GenPi0M2_eta",
            "GenPi0M2_theta",
            "GenPi0M2_phi",
            "GenPi0M2_mass",
            "GenPi0M2_p4",

            "GenRhoM_e",
            "GenRhoM_p",
            "GenRhoM_pt",
            "GenRhoM_px",
            "GenRhoM_py",
            "GenRhoM_pz",
            "GenRhoM_y",
            "GenRhoM_eta",
            "GenRhoM_theta",
            "GenRhoM_phi",
            "GenRhoM_mass",
            "GenRhoM_p4",

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

            "n_GenTau_had",
            "HadGenTau_e",
            "HadGenTau_p",
            "HadGenTau_pt",
            "HadGenTau_px",
            "HadGenTau_py",
            "HadGenTau_pz",
            "HadGenTau_y",
            "HadGenTau_eta",
            "HadGenTau_theta",
            "HadGenTau_phi",
            "HadGenTau_charge",
            "HadGenTau_mass",

        ]
        branchList +=[

        ######## Reconstructed particles #######
            #"RecoMC_PID",

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
            "RecoElectronTrack_absD0",
            "RecoElectronTrack_absZ0",
            "RecoElectronTrack_absD0sig",
            "RecoElectronTrack_absZ0sig",
            "RecoElectronTrack_D0cov",
            "RecoElectronTrack_Z0cov",

            "n_RecoElectrons_sel",
            "RecoElectron_sel_e",
            "RecoElectron_sel_p",
            "RecoElectron_sel_pt",
            "RecoElectron_sel_px",
            "RecoElectron_sel_py",
            "RecoElectron_sel_pz",
            "RecoElectron_sel_y",
            "RecoElectron_sel_eta",
            "RecoElectron_sel_theta",
            "RecoElectron_sel_phi",
            "RecoElectron_sel_charge",
            "RecoElectron_sel_mass",
            "RecoElectronTrack_sel_absD0",
            "RecoElectronTrack_sel_absZ0",
            "RecoElectronTrack_sel_absD0sig",
            "RecoElectronTrack_sel_absZ0sig",
            "RecoElectronTrack_sel_D0cov",
            "RecoElectronTrack_sel_Z0cov",

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
            "RecoMuon_mass",
            "RecoMuonTrack_absD0",
            "RecoMuonTrack_absZ0",
            "RecoMuonTrack_absD0sig",
            "RecoMuonTrack_absZ0sig",
            "RecoMuonTrack_D0cov",
            "RecoMuonTrack_Z0cov",

            "n_RecoMuons_sel",
            "RecoMuon_sel_e",
            "RecoMuon_sel_p",
            "RecoMuon_sel_pt",
            "RecoMuon_sel_px",
            "RecoMuon_sel_py",
            "RecoMuon_sel_pz",
            "RecoMuon_sel_y",
            "RecoMuon_sel_eta",
            "RecoMuon_sel_theta",
            "RecoMuon_sel_phi",
            "RecoMuon_sel_charge",
            "RecoMuon_sel_mass",
            "RecoMuonTrack_sel_absD0",
            "RecoMuonTrack_sel_absZ0",
            "RecoMuonTrack_sel_absD0sig",
            "RecoMuonTrack_sel_absZ0sig",
            "RecoMuonTrack_sel_D0cov",
            "RecoMuonTrack_sel_Z0cov",

            "n_RecoLeptons",
            "RecoLepton_e",
            "RecoLepton_p",
            "RecoLepton_pt",
            "RecoLepton_px",
            "RecoLepton_py",
            "RecoLepton_pz",
            "RecoLepton_y",
            "RecoLepton_eta",
            "RecoLepton_theta",
            "RecoLepton_phi",
            "RecoLepton_charge",
            "RecoLepton_mass",
            "RecoLeptonTrack_absD0",
            "RecoLeptonTrack_absZ0",
            "RecoLeptonTrack_absD0sig",
            "RecoLeptonTrack_absZ0sig",
            "RecoLeptonTrack_D0cov",
            "RecoLeptonTrack_Z0cov",

            "n_RecoLeptons_sel",
            "RecoLepton_sel_e",
            "RecoLepton_sel_p",
            "RecoLepton_sel_pt",
            "RecoLepton_sel_px",
            "RecoLepton_sel_py",
            "RecoLepton_sel_pz",
            "RecoLepton_sel_y",
            "RecoLepton_sel_eta",
            "RecoLepton_sel_theta",
            "RecoLepton_sel_phi",
            "RecoLepton_sel_charge",
            "RecoLepton_sel_mass",
            "RecoLeptonTrack_sel_absD0",
            "RecoLeptonTrack_sel_absZ0",
            "RecoLeptonTrack_sel_absD0sig",
            "RecoLeptonTrack_sel_absZ0sig",
            "RecoLeptonTrack_sel_D0cov",
            "RecoLeptonTrack_sel_Z0cov",

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
            "RecoPhoton_mass",

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",

            #"n_RecoTracks",
            #"RecoVertexObject",
            #"RecoVertex",
            #"n_PrimaryTracks",
            #"PrimaryVertexObject",
            #"PrimaryVertex", 
            #"PrimaryVertex_xyz",
            #"PrimaryVertes_xy",
            #"n_SecondaryTracks",
            #"SecondaryVertexObject",
            #"SecondaryVertex",
            #"SecondaryVertex_xyz",
            #"SecondaryVertes_xy",
            #"VertexObject", 
            #"RecoPartPID" ,
            #"RecoPartPIDAtVertex",
        ]

        branchList += [
            "TagJet_R5_px", 
            "TagJet_R5_py",    
            "TagJet_R5_pz",      
            "TagJet_R5_p",  
            "TagJet_R5_pt",    
            "TagJet_R5_phi", 
            "TagJet_R5_eta",     
            "TagJet_R5_theta",          
            "TagJet_R5_e",     
            "TagJet_R5_mass",        
            "TagJet_R5_charge",       
            "TagJet_R5_flavor", 
            "n_TagJet_R5_constituents",   
            "n_TagJet_R5_charged_constituents",   
            "n_TagJet_R5_neutral_constituents",   
            "n_TagJet_R5",    
            "TagJet_R5_cleanup",        

            "TagJet_R5_isG",  
            "TagJet_R5_isU",
            "TagJet_R5_isD",   
            "TagJet_R5_isS",  
            "TagJet_R5_isC",
            "TagJet_R5_isB",  
            "TagJet_R5_isTAU",

            "TauFromJet_R5_p",
            "TauFromJet_R5_pt",
            "TauFromJet_R5_px",
            "TauFromJet_R5_py",
            "TauFromJet_R5_pz",
            "TauFromJet_R5_theta",
            "TauFromJet_R5_phi",
            "TauFromJet_R5_e",
            "TauFromJet_R5_eta",
            "TauFromJet_R5_y",
            "TauFromJet_R5_charge",
            "TauFromJet_R5_type",
            "TauFromJet_R5_mass",
            "n_TauFromJet_R5",

            "TagJet_R5_sel_e",     
            "TagJet_R5_sel_p",     
            "TagJet_R5_sel_pt",     
            "TagJet_R5_sel_px",   
            "TagJet_R5_sel_py",   
            "TagJet_R5_sel_pz",     
            "TagJet_R5_sel_eta",    
            "TagJet_R5_sel_theta",   
            "TagJet_R5_sel_phi",     
            "TagJet_R5_sel_mass",      
            "n_TagJet_R5_sel", 

        ]

        branchList +=[

            "n_ChargedHadron",
            "ChargedHadron_e",
            "ChargedHadron_p",
            "ChargedHadron_pt",
            "ChargedHadron_px",
            "ChargedHadron_py",
            "ChargedHadron_pz",
            "ChargedHadron_eta",
            "ChargedHadron_theta",
            "ChargedHadron_phi",
            "ChargedHadron_charge",
            "ChargedHadron_mass",
            "ChargedHadron_p4",

            "n_NeutralHadron",
            "NeutralHadron_e",
            "NeutralHadron_p",
            "NeutralHadron_pt",
            "NeutralHadron_px",
            "NeutralHadron_py",
            "NeutralHadron_pz",
            "NeutralHadron_eta",
            "NeutralHadron_theta",
            "NeutralHadron_phi",
            "NeutralHadron_charge",
            "NeutralHadron_mass",
            "NeutralHadron_p4",

            "n_ChargedTau",
            "ChargedTau_e",
            "ChargedTau_p",
            "ChargedTau_pt",
            "ChargedTau_px",
            "ChargedTau_py",
            "ChargedTau_pz",
            "ChargedTau_eta",
            "ChargedTau_theta",
            "ChargedTau_phi",
            "ChargedTau_charge",
            "ChargedTau_mass",
            "ChargedTau_p4",

            "n_NeutralTau",
            "NeutralTau_e",
            "NeutralTau_p",
            "NeutralTau_pt",
            "NeutralTau_px",
            "NeutralTau_py",
            "NeutralTau_pz",
            "NeutralTau_eta",
            "NeutralTau_theta",
            "NeutralTau_phi",
            "NeutralTau_charge",
            "NeutralTau_mass",
            "NeutralTau_p4",

            "n_ChargedJet",
            "ChargedJet_e",
            "ChargedJet_p",
            "ChargedJet_pt",
            "ChargedJet_px",
            "ChargedJet_py",
            "ChargedJet_pz",
            "ChargedJet_eta",
            "ChargedJet_theta",
            "ChargedJet_phi",
            "ChargedJet_charge",
            "ChargedJet_mass",
            "ChargedJet_p4",

            "n_NeutralJet",
            "NeutralJet_e",
            "NeutralJet_p",
            "NeutralJet_pt",
            "NeutralJet_px",
            "NeutralJet_py",
            "NeutralJet_pz",
            "NeutralJet_eta",
            "NeutralJet_theta",
            "NeutralJet_phi",
            "NeutralJet_charge",
            "NeutralJet_mass",
            "NeutralJet_p4",

            "ChargedHadronImpact_p4", 
            "ChargedTauImpact_p4", 
            "ChargedJetImpact_p4",
            "LeptonImpact_p4", 
            "RecoIP_p4",

            "RecoChargedHadronTrack",
            "RecoChargedHadronTrack_D0",
            "RecoChargedHadronTrack_Z0",
            "RecoChargedHadronTrack_D0sig",
            "RecoChargedHadronTrack_Z0sig",
            "RecoChargedHadronTrack_charge",
            "RecoChargedHadronTrack_omega",

            "RecoChargedTauTrack",
            "RecoChargedTauTrack_D0",
            "RecoChargedTauTrack_Z0",
            "RecoChargedTauTrack_D0sig",
            "RecoChargedTauTrack_Z0sig",
            "RecoChargedTauTrack_charge",
            "RecoChargedTauTrack_omega",

            "RecoChargedJetTrack",
            "RecoChargedJetTrack_D0",
            "RecoChargedJetTrack_Z0",
            "RecoChargedJetTrack_D0sig",
            "RecoChargedJetTrack_Z0sig",
            "RecoChargedJetTrack_charge",
            "RecoChargedJetTrack_omega",

            "RecoLeptonTrack",
            "RecoLeptonTrack_D0",
            "RecoLeptonTrack_Z0",
            "RecoLeptonTrack_D0sig",
            "RecoLeptonTrack_Z0sig",
            "RecoLeptonTrack_charge",
            "RecoLeptonTrack_omega",

            "n_RecoDVs", 
            "DV_p3",

        ]

        return branchList