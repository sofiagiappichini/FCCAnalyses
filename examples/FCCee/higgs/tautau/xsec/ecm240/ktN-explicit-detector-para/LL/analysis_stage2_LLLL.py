import os, copy # tagging
import ROOT
import urllib.request
from copy import deepcopy
#Mandatory: List of processes
processList = {

    # 'p8_ee_WW_ecm240':{'chunks':3740},
    # 'p8_ee_Zqq_ecm240':{'chunks':1007},
    # 'p8_ee_ZZ_ecm240':{'chunks':1000},
    
    # 'wzp6_ee_tautau_ecm240':{'chunks':1000},
    # 'wzp6_ee_mumu_ecm240':{'chunks':1000},
    # 'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':1000},

    # 'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':1000},
    # 'wzp6_egamma_eZ_Zee_ecm240': {'chunks':1000},
    # 'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':1000},
    # 'wzp6_gammae_eZ_Zee_ecm240': {'chunks':1000},

    # 'wzp6_gaga_tautau_60_ecm240': {'chunks':1000},
    # 'wzp6_gaga_mumu_60_ecm240': {'chunks':1000},
    # 'wzp6_gaga_ee_60_ecm240': {'chunks':1000},

    # 'wzp6_ee_nuenueZ_ecm240': {'chunks':1000},
    # 'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':1},
    # 'wzp6_ee_eeH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_eeH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_eeH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_eeH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_eeH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_eeH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_ee_bbH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_bbH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_ee_ccH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_ccH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_ee_ssH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_ssH_HZZ_ecm240': {'chunks':100},

    # 'wzp6_ee_qqH_Htautau_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_Hbb_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_Hcc_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_Hss_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_Hgg_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_HWW_ecm240': {'chunks':100},
    # 'wzp6_ee_qqH_HZZ_ecm240': {'chunks':100},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/ecm240/ktN-explicit/stage2_CMS2/LL/LL/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)

sF_e = [1., 14.64, 30.]
sF_mu = [1., 3.78, 7.]
sF_chad = [1., 17.15, 34.]
sF_gamma = [1., 1.2625, 3.]
sF_nhad = [1., 2.89, 6.]


#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df = (df
                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("Photon0", "Photon#0.index") 
                .Alias("Electron0", "Electron#0.index")
                .Alias("Muon0", "Muon#0.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
                .Define("reco_mc_index","ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)")

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
              )
        
        for i in [0,1,2]:

            df = (df
                    .Redefine("ReconstructedParticles",    ROOT.SmearObjects.SmearedReconstructedParticle(sF_e[i], 11, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                    .Redefine("ReconstructedParticles",    ROOT.SmearObjects.SmearedReconstructedParticle(sF_mu[i], 13, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                    .Redefine("ReconstructedParticles",    ROOT.SmearObjects.SmearedReconstructedParticle(sF_gamma[i], 22, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                    #.Redefine("ReconstructedParticles",    ROOT.SmearObjects.SmearedReconstructedParticle(sF_chad[i], 0, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
                    #.Redefine("ReconstructedParticles",    ROOT.SmearObjects.SmearedReconstructedParticle(sF_nhad[i], 130, 1, False),["ReconstructedParticles", "reco_mc_index", "Particle"])
            )

            df = (df
                    #PHOTONS
                    .Define(f"RecoPhotons_{i}",        f"ReconstructedParticle::get(Photon0, ReconstructedParticles)")
                    .Define(f"n_RecoPhotons_{i}",      f"ReconstructedParticle::get_n(RecoPhotons_{i})") #count how many photons are in the event in total
                    .Define(f"RecoPhoton_{i}_e",       f"ReconstructedParticle::get_e(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_p",       f"ReconstructedParticle::get_p(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_pt",      f"ReconstructedParticle::get_pt(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_px",      f"ReconstructedParticle::get_px(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_py",      f"ReconstructedParticle::get_py(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_pz",      f"ReconstructedParticle::get_pz(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_y",       f"ReconstructedParticle::get_y(RecoPhotons_{i})") 
                    .Define(f"RecoPhoton_{i}_eta",     f"ReconstructedParticle::get_eta(RecoPhotons_{i})") #pseudorapidity eta
                    .Define(f"RecoPhoton_{i}_theta",   f"ReconstructedParticle::get_theta(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_phi",     f"ReconstructedParticle::get_phi(RecoPhotons_{i})") #polar angle in the transverse plane phi
                    .Define(f"RecoPhoton_{i}_charge",  f"ReconstructedParticle::get_charge(RecoPhotons_{i})")
                    .Define(f"RecoPhoton_{i}_mass",    f"ReconstructedParticle::get_mass(RecoPhotons_{i})")

                    #ELECTRONS 
                    .Define(f"RecoElectrons_{i}",       f"ReconstructedParticle::get(Electron0, ReconstructedParticles)")
                    .Define(f"n_RecoElectrons_{i}",     f"ReconstructedParticle::get_n(RecoElectrons_{i})") #count how many Electrons_{i} are in the event in total
                    .Define(f"RecoElectron_{i}_e",      f"ReconstructedParticle::get_e(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_p",      f"ReconstructedParticle::get_p(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_pt",     f"ReconstructedParticle::get_pt(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_px",      f"ReconstructedParticle::get_px(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_py",      f"ReconstructedParticle::get_py(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_pz",      f"ReconstructedParticle::get_pz(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_y",       f"ReconstructedParticle::get_y(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_eta",     f"ReconstructedParticle::get_eta(RecoElectrons_{i})") #pseudorapidity eta
                    .Define(f"RecoElectron_{i}_theta",   f"ReconstructedParticle::get_theta(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_phi",     f"ReconstructedParticle::get_phi(RecoElectrons_{i})") #polar angle in the transverse plane phi
                    .Define(f"RecoElectron_{i}_charge",  f"ReconstructedParticle::get_charge(RecoElectrons_{i})")
                    .Define(f"RecoElectron_{i}_mass",    f"ReconstructedParticle::get_mass(RecoElectrons_{i})")

                    .Define(f"RecoElectrons_{i}_hard", f"FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons_{i})")
                    .Define(f"RecoElectrons_{i}_iso",  f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_{i}_hard, ReconstructedParticles)")
                    .Define(f"RecoElectrons_{i}_sel",  f"FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_{i}_hard, RecoElectrons_{i}_iso)")

                    .Define(f"n_RecoElectrons_{i}_sel",      f"ReconstructedParticle::get_n(RecoElectrons_{i}_sel)") 
                    .Define(f"RecoElectron_{i}_sel_e",       f"ReconstructedParticle::get_e(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_p",       f"ReconstructedParticle::get_p(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_pt",      f"ReconstructedParticle::get_pt(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_px",      f"ReconstructedParticle::get_px(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_py",      f"ReconstructedParticle::get_py(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_pz",      f"ReconstructedParticle::get_pz(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_y",       f"ReconstructedParticle::get_y(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_eta",     f"ReconstructedParticle::get_eta(RecoElectrons_{i}_sel)") #pseudorapidity eta
                    .Define(f"RecoElectron_{i}_sel_theta",   f"ReconstructedParticle::get_theta(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_phi",     f"ReconstructedParticle::get_phi(RecoElectrons_{i}_sel)") #polar angle in the transverse plane phi
                    .Define(f"RecoElectron_{i}_sel_charge",  f"ReconstructedParticle::get_charge(RecoElectrons_{i}_sel)")
                    .Define(f"RecoElectron_{i}_sel_mass",    f"ReconstructedParticle::get_mass(RecoElectrons_{i}_sel)")
            )

            df=(df
                    # MUONS
                    .Define(f"RecoMuons_{i}",       f"ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                    .Define(f"n_RecoMuons_{i}",     f"ReconstructedParticle::get_n(RecoMuons_{i})") #count how many muons are in the event in total
                    .Define(f"RecoMuon_{i}_e",      f"ReconstructedParticle::get_e(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_p",      f"ReconstructedParticle::get_p(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_pt",     f"ReconstructedParticle::get_pt(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_px",     f"ReconstructedParticle::get_px(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_py",     f"ReconstructedParticle::get_py(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_pz",     f"ReconstructedParticle::get_pz(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_y",      f"ReconstructedParticle::get_y(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_eta",    f"ReconstructedParticle::get_eta(RecoMuons_{i})") #pseudorapidity eta
                    .Define(f"RecoMuon_{i}_theta",  f"ReconstructedParticle::get_theta(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_phi",    f"ReconstructedParticle::get_phi(RecoMuons_{i})") #polar angle in the transverse plane phi
                    .Define(f"RecoMuon_{i}_charge", f"ReconstructedParticle::get_charge(RecoMuons_{i})")
                    .Define(f"RecoMuon_{i}_mass",   f"ReconstructedParticle::get_mass(RecoMuons_{i})")

                    .Define(f"RecoMuons_{i}_hard",  f"FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons_{i})")
                    .Define(f"RecoMuons_{i}_iso",   f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_{i}_hard, ReconstructedParticles)")
                    .Define(f"RecoMuons_{i}_sel",   f"FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_{i}_hard, RecoMuons_{i}_iso)")
                    
                    .Define(f"n_RecoMuons_{i}_sel",     f"ReconstructedParticle::get_n(RecoMuons_{i}_sel)") 
                    .Define(f"RecoMuon_{i}_sel_e",      f"ReconstructedParticle::get_e(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_p",      f"ReconstructedParticle::get_p(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_pt",     f"ReconstructedParticle::get_pt(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_px",     f"ReconstructedParticle::get_px(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_py",     f"ReconstructedParticle::get_py(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_pz",     f"ReconstructedParticle::get_pz(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_y",      f"ReconstructedParticle::get_y(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_eta",    f"ReconstructedParticle::get_eta(RecoMuons_{i}_sel)") #pseudorapidity eta
                    .Define(f"RecoMuon_{i}_sel_theta",  f"ReconstructedParticle::get_theta(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_phi",    f"ReconstructedParticle::get_phi(RecoMuons_{i}_sel)") #polar angle in the transverse plane phi
                    .Define(f"RecoMuon_{i}_sel_charge", f"ReconstructedParticle::get_charge(RecoMuons_{i}_sel)")
                    .Define(f"RecoMuon_{i}_sel_mass",   f"ReconstructedParticle::get_mass(RecoMuons_{i}_sel)")

                    # LEPTONS
                    .Define(f"RecoLeptons_{i}",        f"ReconstructedParticle::merge(RecoElectrons_{i}, RecoMuons_{i})")
                    .Define(f"n_RecoLeptons_{i}",      f"ReconstructedParticle::get_n(RecoLeptons_{i})") 
                    .Define(f"RecoLepton_{i}_e",       f"ReconstructedParticle::get_e(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_p",       f"ReconstructedParticle::get_p(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_pt",      f"ReconstructedParticle::get_pt(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_px",      f"ReconstructedParticle::get_px(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_py",      f"ReconstructedParticle::get_py(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_pz",      f"ReconstructedParticle::get_pz(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_y",       f"ReconstructedParticle::get_y(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_eta",     f"ReconstructedParticle::get_eta(RecoLeptons_{i})") #pseudorapidity eta
                    .Define(f"RecoLepton_{i}_theta",   f"ReconstructedParticle::get_theta(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_phi",     f"ReconstructedParticle::get_phi(RecoLeptons_{i})") #polar angle in the transverse plane phi
                    .Define(f"RecoLepton_{i}_charge",  f"ReconstructedParticle::get_charge(RecoLeptons_{i})")
                    .Define(f"RecoLepton_{i}_mass",    f"ReconstructedParticle::get_mass(RecoLeptons_{i})")

                    .Define(f"RecoLeptons_{i}_sel",        f"ReconstructedParticle::merge(RecoElectrons_{i}_sel, RecoMuons_{i}_sel)")
                    .Define(f"n_RecoLeptons_{i}_sel",      f"ReconstructedParticle::get_n(RecoLeptons_{i}_sel)") 
                    .Define(f"RecoLepton_{i}_sel_e",       f"ReconstructedParticle::get_e(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_p",       f"ReconstructedParticle::get_p(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_pt",      f"ReconstructedParticle::get_pt(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_px",      f"ReconstructedParticle::get_px(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_py",      f"ReconstructedParticle::get_py(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_pz",      f"ReconstructedParticle::get_pz(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_y",       f"ReconstructedParticle::get_y(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_eta",     f"ReconstructedParticle::get_eta(RecoLeptons_{i}_sel)") #pseudorapidity eta
                    .Define(f"RecoLepton_{i}_sel_theta",   f"ReconstructedParticle::get_theta(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_phi",     f"ReconstructedParticle::get_phi(RecoLeptons_{i}_sel)") #polar angle in the transverse plane phi
                    .Define(f"RecoLepton_{i}_sel_charge",  f"ReconstructedParticle::get_charge(RecoLeptons_{i}_sel)")
                    .Define(f"RecoLepton_{i}_sel_mass",    f"ReconstructedParticle::get_mass(RecoLeptons_{i}_sel)")

                    ####################
                    ##### FILTER #######
                    ####################

                    # four leptons in the whole event that make the Z boson, find the pair later, even if using tagged jets taus should not have leptons in the jets!!! should help with background rejection
                    # anyway now i want zero jets so it doesn't even matter
                    .Define(f"AllLeptons_{i}",  f"(((n_RecoElectrons_{i}==4 and n_RecoMuons_{i}==0) or (n_RecoElectrons_{i}==0 and n_RecoMuons_{i}==4)) and (RecoLepton_{i}_charge.at(0) + RecoLepton_{i}_charge.at(1) + RecoLepton_{i}_charge.at(2) + RecoLepton_{i}_charge.at(3))==0)*1.0")
                    .Define(f"TwoPairs_{i}",    f"((n_RecoElectrons_{i}==2 and n_RecoMuons_{i}==2) and (RecoElectron_{i}_charge.at(0) + RecoElectron_{i}_charge.at(1))==0 and (RecoMuon_{i}_charge.at(0) + RecoMuon_{i}_charge.at(1))==0)*1.0")
                    .Define(f"OnePair_{i}",     f"(((n_RecoElectrons_{i}==3 and n_RecoMuons_{i}==1) or (n_RecoElectrons_{i}==1 and n_RecoMuons_{i}==3))  and (RecoLepton_{i}_charge.at(0) + RecoLepton_{i}_charge.at(1) + RecoLepton_{i}_charge.at(2) + RecoLepton_{i}_charge.at(3))==0)*1.0")

                    .Filter(f"(AllLeptons_{i}==1 || TwoPairs_{i}==1 || OnePair_{i}==1)")

                    .Define(f"NoPhotons_{i}",   "ReconstructedParticles[ReconstructedParticles.type != 22]")

                    .Filter(f"n_RecoLeptons_{i} == NoPhotons_{i}.size()")
            )

        
            df = (df

                    .Define(f"RecoLepton_{i}_p4",  f"FCCAnalyses::ZHfunctions::build_p4(RecoLepton_{i}_px, RecoLepton_{i}_py, RecoLepton_{i}_pz, RecoLepton_{i}_e)")

                    .Define(f"RecoZH_{i}_idx",     f"FCCAnalyses::ZHfunctions::FindBest_4(RecoLepton_{i}_p4, RecoLepton_{i}_charge, RecoLepton_{i}_mass, 91.188, 125.25)")

                    .Define(f"RecoZ1_{i}_p4",      f"RecoLepton_{i}_p4.at(RecoZH_{i}_idx[0])")
                    .Define(f"RecoZ2_{i}_p4",      f"RecoLepton_{i}_p4.at(RecoZH_{i}_idx[1])")
                    
                    .Define(f"RecoZLead_{i}_p4",        f"if (RecoZ1_{i}_p4.Pt()>RecoZ2_{i}_p4.Pt()) return RecoZ1_{i}_p4; else return RecoZ2_{i}_p4;")
                    .Define(f"RecoZLead_{i}_px",        f"RecoZLead_{i}_p4.Px()")
                    .Define(f"RecoZLead_{i}_py",        f"RecoZLead_{i}_p4.Py()")
                    .Define(f"RecoZLead_{i}_pz",        f"RecoZLead_{i}_p4.Pz()")
                    .Define(f"RecoZLead_{i}_p",         f"RecoZLead_{i}_p4.P()")
                    .Define(f"RecoZLead_{i}_pt",        f"RecoZLead_{i}_p4.Pt()")
                    .Define(f"RecoZLead_{i}_e",         f"RecoZLead_{i}_p4.E()")
                    .Define(f"RecoZLead_{i}_eta",       f"RecoZLead_{i}_p4.Eta()")
                    .Define(f"RecoZLead_{i}_phi",       f"RecoZLead_{i}_p4.Phi()")
                    .Define(f"RecoZLead_{i}_theta",     f"RecoZLead_{i}_p4.Theta()")
                    .Define(f"RecoZLead_{i}_y",         f"RecoZLead_{i}_p4.Rapidity()")
                    .Define(f"RecoZLead_{i}_mass",      f"RecoZLead_{i}_p4.M()")

                    .Define(f"RecoZSub_{i}_p4",         f"if (RecoZ1_{i}_p4.Pt()>RecoZ2_{i}_p4.Pt()) return RecoZ2_{i}_p4; else return RecoZ1_{i}_p4;")
                    .Define(f"RecoZSub_{i}_px",         f"RecoZSub_{i}_p4.Px()")
                    .Define(f"RecoZSub_{i}_py",         f"RecoZSub_{i}_p4.Py()")
                    .Define(f"RecoZSub_{i}_pz",         f"RecoZSub_{i}_p4.Pz()")
                    .Define(f"RecoZSub_{i}_p",          f"RecoZSub_{i}_p4.P()")
                    .Define(f"RecoZSub_{i}_pt",         f"RecoZSub_{i}_p4.Pt()")
                    .Define(f"RecoZSub_{i}_e",          f"RecoZSub_{i}_p4.E()")
                    .Define(f"RecoZSub_{i}_eta",        f"RecoZSub_{i}_p4.Eta()")
                    .Define(f"RecoZSub_{i}_phi",        f"RecoZSub_{i}_p4.Phi()")
                    .Define(f"RecoZSub_{i}_theta",      f"RecoZSub_{i}_p4.Theta()")
                    .Define(f"RecoZSub_{i}_y",          f"RecoZSub_{i}_p4.Rapidity()")
                    .Define(f"RecoZSub_{i}_mass",       f"RecoZSub_{i}_p4.M()")

                    .Define(f"RecoZP_{i}_p4",           f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[0])==1) return RecoZ1_{i}_p4; else return RecoZ2_{i}_p4;")
                    .Define(f"RecoZP_{i}_px",           f"RecoZP_{i}_p4.Px()")
                    .Define(f"RecoZP_{i}_py",           f"RecoZP_{i}_p4.Py()")
                    .Define(f"RecoZP_{i}_pz",           f"RecoZP_{i}_p4.Pz()")
                    .Define(f"RecoZP_{i}_p",            f"RecoZP_{i}_p4.P()")
                    .Define(f"RecoZP_{i}_pt",           f"RecoZP_{i}_p4.Pt()")
                    .Define(f"RecoZP_{i}_e",            f"RecoZP_{i}_p4.E()")
                    .Define(f"RecoZP_{i}_eta",          f"RecoZP_{i}_p4.Eta()")
                    .Define(f"RecoZP_{i}_phi",          f"RecoZP_{i}_p4.Phi()")
                    .Define(f"RecoZP_{i}_theta",        f"RecoZP_{i}_p4.Theta()")
                    .Define(f"RecoZP_{i}_y",            f"RecoZP_{i}_p4.Rapidity()")
                    .Define(f"RecoZP_{i}_mass",         f"RecoZP_{i}_p4.M()")

                    .Define(f"RecoZM_{i}_p4",           f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[0])==1) return RecoZ2_{i}_p4; else return RecoZ1_{i}_p4;")
                    .Define(f"RecoZM_{i}_px",           f"RecoZM_{i}_p4.Px()")
                    .Define(f"RecoZM_{i}_py",           f"RecoZM_{i}_p4.Py()")
                    .Define(f"RecoZM_{i}_pz",           f"RecoZM_{i}_p4.Pz()")
                    .Define(f"RecoZM_{i}_p",            f"RecoZM_{i}_p4.P()")
                    .Define(f"RecoZM_{i}_pt",           f"RecoZM_{i}_p4.Pt()")
                    .Define(f"RecoZM_{i}_e",            f"RecoZM_{i}_p4.E()")
                    .Define(f"RecoZM_{i}_eta",          f"RecoZM_{i}_p4.Eta()")
                    .Define(f"RecoZM_{i}_phi",          f"RecoZM_{i}_p4.Phi()")
                    .Define(f"RecoZM_{i}_theta",        f"RecoZM_{i}_p4.Theta()")
                    .Define(f"RecoZM_{i}_y",            f"RecoZM_{i}_p4.Rapidity()")
                    .Define(f"RecoZM_{i}_mass",         f"RecoZM_{i}_p4.M()")

                    .Define(f"RecoZ_{i}_p4",            f"RecoZ1_{i}_p4+RecoZ2_{i}_p4")
                    .Define(f"RecoZ_{i}_px",            f"RecoZ_{i}_p4.Px()")
                    .Define(f"RecoZ_{i}_py",            f"RecoZ_{i}_p4.Py()")
                    .Define(f"RecoZ_{i}_pz",            f"RecoZ_{i}_p4.Pz()")
                    .Define(f"RecoZ_{i}_p",             f"RecoZ_{i}_p4.P()")
                    .Define(f"RecoZ_{i}_pt",            f"RecoZ_{i}_p4.Pt()")
                    .Define(f"RecoZ_{i}_e",             f"RecoZ_{i}_p4.E()")
                    .Define(f"RecoZ_{i}_eta",           f"RecoZ_{i}_p4.Eta()")
                    .Define(f"RecoZ_{i}_phi",           f"RecoZ_{i}_p4.Phi()")
                    .Define(f"RecoZ_{i}_theta",         f"RecoZ_{i}_p4.Theta()")
                    .Define(f"RecoZ_{i}_y",             f"RecoZ_{i}_p4.Rapidity()")
                    .Define(f"RecoZ_{i}_mass",          f"RecoZ_{i}_p4.M()")

                    .Define(f"RecoTau1_{i}_p4",         f"RecoLepton_{i}_p4.at(RecoZH_{i}_idx[2])")
                    .Define(f"RecoTau2_{i}_p4",         f"RecoLepton_{i}_p4.at(RecoZH_{i}_idx[3])")
                    .Define(f"RecoTau1_{i}_type",       f"if (RecoLepton_{i}_mass.at(RecoZH_{i}_idx[2])<0.05) return float(-0.11); else return float(-0.13);")
                    .Define(f"RecoTau2_{i}_type",       f"if (RecoLepton_{i}_mass.at(RecoZH_{i}_idx[2])<0.05) return float(-0.13); else return float(-0.11);")

                    .Define(f"RecoH_{i}_p4",            f"RecoTau1_{i}_p4+RecoTau2_{i}_p4")
                    .Define(f"RecoH_{i}_px",            f"RecoH_{i}_p4.Px()")
                    .Define(f"RecoH_{i}_py",            f"RecoH_{i}_p4.Py()")
                    .Define(f"RecoH_{i}_pz",            f"RecoH_{i}_p4.Pz()")
                    .Define(f"RecoH_{i}_p",             f"RecoH_{i}_p4.P()")
                    .Define(f"RecoH_{i}_pt",            f"RecoH_{i}_p4.Pt()")
                    .Define(f"RecoH_{i}_e",             f"RecoH_{i}_p4.E()")
                    .Define(f"RecoH_{i}_eta",           f"RecoH_{i}_p4.Eta()")
                    .Define(f"RecoH_{i}_phi",           f"RecoH_{i}_p4.Phi()")
                    .Define(f"RecoH_{i}_theta",         f"RecoH_{i}_p4.Theta()")
                    .Define(f"RecoH_{i}_y",             f"RecoH_{i}_p4.Rapidity()")
                    .Define(f"RecoH_{i}_mass",          f"RecoH_{i}_p4.M()")
            )
            df = (df
                    .Define(f"TauLead_{i}_p4",          f"if (RecoTau1_{i}_p4.Pt()>RecoTau2_{i}_p4.Pt()) return RecoTau1_{i}_p4; else return RecoTau2_{i}_p4;")
                    .Define(f"TauLead_{i}_px",          f"TauLead_{i}_p4.Px()")
                    .Define(f"TauLead_{i}_py",          f"TauLead_{i}_p4.Py()")
                    .Define(f"TauLead_{i}_pz",          f"TauLead_{i}_p4.Pz()")
                    .Define(f"TauLead_{i}_p",           f"TauLead_{i}_p4.P()")
                    .Define(f"TauLead_{i}_pt",          f"TauLead_{i}_p4.Pt()")
                    .Define(f"TauLead_{i}_e",           f"TauLead_{i}_p4.E()")
                    .Define(f"TauLead_{i}_eta",         f"TauLead_{i}_p4.Eta()")
                    .Define(f"TauLead_{i}_phi",         f"TauLead_{i}_p4.Phi()")
                    .Define(f"TauLead_{i}_theta",       f"TauLead_{i}_p4.Theta()")
                    .Define(f"TauLead_{i}_y",           f"TauLead_{i}_p4.Rapidity()")
                    .Define(f"TauLead_{i}_mass",        f"TauLead_{i}_p4.M()")
                    .Define(f"TauLead_{i}_type",        f"if (RecoTau1_{i}_p4.Pt()>RecoTau2_{i}_p4.Pt()) return RecoTau1_{i}_type; else return RecoTau2_{i}_type;")
                    
                    .Define(f"TauSub_{i}_p4",           f"if (RecoTau1_{i}_p4.Pt()>RecoTau2_{i}_p4.Pt()) return RecoTau2_{i}_p4; else return RecoTau1_{i}_p4;")
                    .Define(f"TauSub_{i}_px",           f"TauSub_{i}_p4.Px()")
                    .Define(f"TauSub_{i}_py",           f"TauSub_{i}_p4.Py()")
                    .Define(f"TauSub_{i}_pz",           f"TauSub_{i}_p4.Pz()")
                    .Define(f"TauSub_{i}_p",            f"TauSub_{i}_p4.P()")
                    .Define(f"TauSub_{i}_pt",           f"TauSub_{i}_p4.Pt()")
                    .Define(f"TauSub_{i}_e",            f"TauSub_{i}_p4.E()")
                    .Define(f"TauSub_{i}_eta",          f"TauSub_{i}_p4.Eta()")
                    .Define(f"TauSub_{i}_phi",          f"TauSub_{i}_p4.Phi()")
                    .Define(f"TauSub_{i}_theta",        f"TauSub_{i}_p4.Theta()")
                    .Define(f"TauSub_{i}_y",            f"TauSub_{i}_p4.Rapidity()")
                    .Define(f"TauSub_{i}_mass",         f"TauSub_{i}_p4.M()")
                    .Define(f"TauSub_{i}_type",         f"if (RecoTau1_{i}_p4.Pt()>RecoTau2_{i}_p4.Pt()) return RecoTau2_{i}_type; else return RecoTau1_{i}_type;")

                    .Define(f"TauP_{i}_p4",             f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[2])==1) return RecoTau1_{i}_p4; else return RecoTau2_{i}_p4;")
                    .Define(f"TauP_{i}_px",             f"TauP_{i}_p4.Px()")
                    .Define(f"TauP_{i}_py",             f"TauP_{i}_p4.Py()")
                    .Define(f"TauP_{i}_pz",             f"TauP_{i}_p4.Pz()")
                    .Define(f"TauP_{i}_p",              f"TauP_{i}_p4.P()")
                    .Define(f"TauP_{i}_pt",             f"TauP_{i}_p4.Pt()")
                    .Define(f"TauP_{i}_e",              f"TauP_{i}_p4.E()")
                    .Define(f"TauP_{i}_eta",            f"TauP_{i}_p4.Eta()")
                    .Define(f"TauP_{i}_phi",            f"TauP_{i}_p4.Phi()")
                    .Define(f"TauP_{i}_theta",          f"TauP_{i}_p4.Theta()")
                    .Define(f"TauP_{i}_y",              f"TauP_{i}_p4.Rapidity()")
                    .Define(f"TauP_{i}_mass",           f"TauP_{i}_p4.M()")
                    .Define(f"TauP_{i}_type",           f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[2])==1) return RecoTau1_{i}_type; else return RecoTau2_{i}_type;")

                    .Define(f"TauM_{i}_p4",             f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[2])==1) return RecoTau2_{i}_p4; else return RecoTau1_{i}_p4;")
                    .Define(f"TauM_{i}_px",             f"TauM_{i}_p4.Px()")
                    .Define(f"TauM_{i}_py",             f"TauM_{i}_p4.Py()")
                    .Define(f"TauM_{i}_pz",             f"TauM_{i}_p4.Pz()")
                    .Define(f"TauM_{i}_p",              f"TauM_{i}_p4.P()")
                    .Define(f"TauM_{i}_pt",             f"TauM_{i}_p4.Pt()")
                    .Define(f"TauM_{i}_e",              f"TauM_{i}_p4.E()")
                    .Define(f"TauM_{i}_eta",            f"TauM_{i}_p4.Eta()")
                    .Define(f"TauM_{i}_phi",            f"TauM_{i}_p4.Phi()")
                    .Define(f"TauM_{i}_theta",          f"TauM_{i}_p4.Theta()")
                    .Define(f"TauM_{i}_y",              f"TauM_{i}_p4.Rapidity()")
                    .Define(f"TauM_{i}_mass",           f"TauM_{i}_p4.M()")
                    .Define(f"TauM_{i}_type",           f"if (RecoLepton_{i}_charge.at(RecoZH_{i}_idx[2])==1) return RecoTau2_{i}_type; else return RecoTau1_{i}_type;")
                    
                    .Define(f"Tau_{i}_DR",              f"FCCAnalyses::ZHfunctions::deltaR(TauLead_{i}_phi, TauSub_{i}_phi, TauLead_{i}_eta, TauSub_{i}_eta)")
                    .Define(f"Tau_{i}_scalar",          f"(TauLead_{i}_px*TauSub_{i}_px + TauLead_{i}_py*TauSub_{i}_py + TauLead_{i}_pz*TauSub_{i}_pz)")
                    .Define(f"Tau_{i}_cos",             f"Tau_{i}_scalar/(TauLead_{i}_p*TauSub_{i}_p)")
                    .Define(f"Tau_{i}_DEta",            f"(TauLead_{i}_eta - TauSub_{i}_eta)")
                    .Define(f"Tau_{i}_DPhi",            f"FCCAnalyses::ZHfunctions::deltaPhi(TauLead_{i}_phi, TauSub_{i}_phi)")

                    .Define(f"RecoZDaughter_{i}_DR",       f"FCCAnalyses::ZHfunctions::deltaR(RecoZLead_{i}_phi, RecoZSub_{i}_phi, RecoZLead_{i}_eta, RecoZSub_{i}_eta)")
                    .Define(f"RecoZDaughter_{i}_scalar",   f"(RecoZLead_{i}_px*RecoZSub_{i}_px + RecoZLead_{i}_py*RecoZSub_{i}_py + RecoZLead_{i}_pz*RecoZSub_{i}_pz)")
                    .Define(f"RecoZDaughter_{i}_cos",      f"RecoZDaughter_{i}_scalar/(RecoZLead_{i}_p*RecoZSub_{i}_p)")
                    .Define(f"RecoZDaughter_{i}_DEta",     f"(RecoZLead_{i}_eta - RecoZSub_{i}_eta)")
                    .Define(f"RecoZDaughter_{i}_DPhi",     f"FCCAnalyses::ZHfunctions::deltaPhi(RecoZLead_{i}_phi, RecoZSub_{i}_phi)")

                    .Define(f"Total_{i}_p4",                   f"TLorentzVector(0.,0.,1.,240.)")
                    .Define(f"Recoil_{i}",                 f"(Total_{i}_p4-RecoZ_{i}_p4).M()")

                    .Define(f"p12_{i}",                  f"(TauLead_{i}_py*TauSub_{i}_px-TauLead_{i}_px*TauSub_{i}_py)")
                    .Define(f"r0_{i}",                   f"abs((RecoEmiss_py*TauLead_{i}_px-RecoEmiss_px*TauLead_{i}_py)/p12_{i})")
                    .Define(f"f0_{i}",                   f"1./(1.+r0_{i})")
                    .Define(f"r1_{i}",                   f"abs((RecoEmiss_py*TauSub_{i}_px-RecoEmiss_px*TauSub_{i}_py)/p12_{i})")
                    .Define(f"f1_{i}",                   f"1./(1.+r1_{i})")
                    .Define(f"Collinear_mass_{i}",       f"RecoH_{i}_mass/sqrt(f0_{i}*f1_{i})")

            )
        return df

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
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
        ]

        for i in [0,1,2]:
            branchList += [
                f"RecoElectrons_{i}",
                f"n_RecoElectrons_{i}",
                f"RecoElectron_{i}_e",
                f"RecoElectron_{i}_p",
                f"RecoElectron_{i}_pt",
                f"RecoElectron_{i}_px",
                f"RecoElectron_{i}_py",
                f"RecoElectron_{i}_pz",
                f"RecoElectron_{i}_y",
                f"RecoElectron_{i}_eta",
                f"RecoElectron_{i}_theta",
                f"RecoElectron_{i}_phi",
                f"RecoElectron_{i}_charge",
                f"RecoElectron_{i}_mass",

                f"RecoElectrons_{i}_sel",
                f"n_RecoElectrons_{i}_sel",
                f"RecoElectron_{i}_sel_e",
                f"RecoElectron_{i}_sel_p",
                f"RecoElectron_{i}_sel_pt",
                f"RecoElectron_{i}_sel_px",
                f"RecoElectron_{i}_sel_py",
                f"RecoElectron_{i}_sel_pz",
                f"RecoElectron_{i}_sel_y",
                f"RecoElectron_{i}_sel_eta",
                f"RecoElectron_{i}_sel_theta",
                f"RecoElectron_{i}_sel_phi",
                f"RecoElectron_{i}_sel_charge",
                f"RecoElectron_{i}_sel_mass",

                f"RecoMuons_{i}",
                f"n_RecoMuons_{i}",
                f"RecoMuon_{i}_e",
                f"RecoMuon_{i}_p",
                f"RecoMuon_{i}_pt",
                f"RecoMuon_{i}_px",
                f"RecoMuon_{i}_py",
                f"RecoMuon_{i}_pz",
                f"RecoMuon_{i}_y",
                f"RecoMuon_{i}_eta",
                f"RecoMuon_{i}_theta",
                f"RecoMuon_{i}_phi",
                f"RecoMuon_{i}_charge",
                f"RecoMuon_{i}_mass",

                f"RecoMuons_{i}_sel",
                f"n_RecoMuons_{i}_sel",
                f"RecoMuon_{i}_sel_e",
                f"RecoMuon_{i}_sel_p",
                f"RecoMuon_{i}_sel_pt",
                f"RecoMuon_{i}_sel_px",
                f"RecoMuon_{i}_sel_py",
                f"RecoMuon_{i}_sel_pz",
                f"RecoMuon_{i}_sel_y",
                f"RecoMuon_{i}_sel_eta",
                f"RecoMuon_{i}_sel_theta",
                f"RecoMuon_{i}_sel_phi",
                f"RecoMuon_{i}_sel_charge",
                f"RecoMuon_{i}_sel_mass",

                f"RecoLeptons_{i}",
                f"n_RecoLeptons_{i}",
                f"RecoLepton_{i}_e",
                f"RecoLepton_{i}_p",
                f"RecoLepton_{i}_pt",
                f"RecoLepton_{i}_px",
                f"RecoLepton_{i}_py",
                f"RecoLepton_{i}_pz",
                f"RecoLepton_{i}_y",
                f"RecoLepton_{i}_eta",
                f"RecoLepton_{i}_theta",
                f"RecoLepton_{i}_phi",
                f"RecoLepton_{i}_charge",
                f"RecoLepton_{i}_mass",

                f"RecoLeptons_{i}_sel",
                f"n_RecoLeptons_{i}_sel",
                f"RecoLepton_{i}_sel_e",
                f"RecoLepton_{i}_sel_p",
                f"RecoLepton_{i}_sel_pt",
                f"RecoLepton_{i}_sel_px",
                f"RecoLepton_{i}_sel_py",
                f"RecoLepton_{i}_sel_pz",
                f"RecoLepton_{i}_sel_y",
                f"RecoLepton_{i}_sel_eta",
                f"RecoLepton_{i}_sel_theta",
                f"RecoLepton_{i}_sel_phi",
                f"RecoLepton_{i}_sel_charge",
                f"RecoLepton_{i}_sel_mass",

                f"RecoPhotons_{i}",
                f"n_RecoPhotons_{i}",
                f"RecoPhoton_{i}_e",
                f"RecoPhoton_{i}_p",
                f"RecoPhoton_{i}_pt",
                f"RecoPhoton_{i}_px",
                f"RecoPhoton_{i}_py",
                f"RecoPhoton_{i}_pz",
                f"RecoPhoton_{i}_y",
                f"RecoPhoton_{i}_eta",
                f"RecoPhoton_{i}_theta",
                f"RecoPhoton_{i}_phi",
                f"RecoPhoton_{i}_charge",
                f"RecoPhoton_{i}_mass",

            ]
            #complex variables added here at stage2
            branchList += [

                f"RecoZ_{i}_px",
                f"RecoZ_{i}_py",
                f"RecoZ_{i}_pz",
                f"RecoZ_{i}_p",
                f"RecoZ_{i}_pt",
                f"RecoZ_{i}_e",
                f"RecoZ_{i}_eta",
                f"RecoZ_{i}_phi",
                f"RecoZ_{i}_theta",
                f"RecoZ_{i}_y",
                f"RecoZ_{i}_mass",

                f"RecoZLead_{i}_px", 
                f"RecoZLead_{i}_py",   
                f"RecoZLead_{i}_pz",   
                f"RecoZLead_{i}_p",    
                f"RecoZLead_{i}_pt",   
                f"RecoZLead_{i}_e",    
                f"RecoZLead_{i}_eta",    
                f"RecoZLead_{i}_phi",    
                f"RecoZLead_{i}_theta",   
                f"RecoZLead_{i}_y",     
                f"RecoZLead_{i}_mass",   

                f"RecoZSub_{i}_px",    
                f"RecoZSub_{i}_py",   
                f"RecoZSub_{i}_pz",   
                f"RecoZSub_{i}_p",   
                f"RecoZSub_{i}_pt",  
                f"RecoZSub_{i}_e",     
                f"RecoZSub_{i}_eta",   
                f"RecoZSub_{i}_phi",   
                f"RecoZSub_{i}_theta",    
                f"RecoZSub_{i}_y",    
                f"RecoZSub_{i}_mass",   

                f"RecoZP_{i}_px", 
                f"RecoZP_{i}_py",   
                f"RecoZP_{i}_pz",   
                f"RecoZP_{i}_p",    
                f"RecoZP_{i}_pt",   
                f"RecoZP_{i}_e",    
                f"RecoZP_{i}_eta",    
                f"RecoZP_{i}_phi",    
                f"RecoZP_{i}_theta",   
                f"RecoZP_{i}_y",     
                f"RecoZP_{i}_mass",   

                f"RecoZM_{i}_px",    
                f"RecoZM_{i}_py",   
                f"RecoZM_{i}_pz",   
                f"RecoZM_{i}_p",   
                f"RecoZM_{i}_pt",  
                f"RecoZM_{i}_e",     
                f"RecoZM_{i}_eta",   
                f"RecoZM_{i}_phi",   
                f"RecoZM_{i}_theta",    
                f"RecoZM_{i}_y",    
                f"RecoZM_{i}_mass", 

                f"RecoH_{i}_px",
                f"RecoH_{i}_py",
                f"RecoH_{i}_pz",
                f"RecoH_{i}_p",
                f"RecoH_{i}_pt",
                f"RecoH_{i}_e",
                f"RecoH_{i}_eta",
                f"RecoH_{i}_phi",
                f"RecoH_{i}_theta",
                f"RecoH_{i}_y",
                f"RecoH_{i}_mass",

                f"TauLead_{i}_px",    
                f"TauLead_{i}_py",   
                f"TauLead_{i}_pz",   
                f"TauLead_{i}_p",   
                f"TauLead_{i}_pt",   
                f"TauLead_{i}_e",    
                f"TauLead_{i}_eta",    
                f"TauLead_{i}_phi",    
                f"TauLead_{i}_theta",    
                f"TauLead_{i}_y",    
                f"TauLead_{i}_mass",
                f"TauLead_{i}_type",

                f"TauSub_{i}_px",    
                f"TauSub_{i}_py",   
                f"TauSub_{i}_pz",   
                f"TauSub_{i}_p",   
                f"TauSub_{i}_pt",   
                f"TauSub_{i}_e",    
                f"TauSub_{i}_eta",    
                f"TauSub_{i}_phi",    
                f"TauSub_{i}_theta",    
                f"TauSub_{i}_y",    
                f"TauSub_{i}_mass",
                f"TauSub_{i}_type",

                f"TauP_{i}_px",    
                f"TauP_{i}_py",   
                f"TauP_{i}_pz",   
                f"TauP_{i}_p",   
                f"TauP_{i}_pt",   
                f"TauP_{i}_e",    
                f"TauP_{i}_eta",    
                f"TauP_{i}_phi",    
                f"TauP_{i}_theta",    
                f"TauP_{i}_y",    
                f"TauP_{i}_mass",
                f"TauP_{i}_type",

                f"TauM_{i}_px",    
                f"TauM_{i}_py",   
                f"TauM_{i}_pz",   
                f"TauM_{i}_p",   
                f"TauM_{i}_pt",   
                f"TauM_{i}_e",    
                f"TauM_{i}_eta",    
                f"TauM_{i}_phi",    
                f"TauM_{i}_theta",    
                f"TauM_{i}_y",    
                f"TauM_{i}_mass",
                f"TauM_{i}_type",

                f"Recoil_{i}",
                f"Collinear_mass_{i}", 
            
                f"Tau_{i}_DR",
                f"Tau_{i}_cos",
                f"Tau_{i}_DEta", 
                f"Tau_{i}_DPhi",
                
                f"RecoZDaughter_{i}_DR", 
                f"RecoZDaughter_{i}_cos", 
                f"RecoZDaughter_{i}_DEta", 
                f"RecoZDaughter_{i}_DPhi", 

            ]
        return branchList