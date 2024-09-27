#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { namespace ZHfunctions {


// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {

    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            rp reso;
            reso.charge = 0;
            TLorentzVector reso_lv; 
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { // MC kinematics
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }
                    else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while(std::next_permutation(v.begin(), v.end()));
    }
    else {
        std::cout << "ERROR: resonanceBuilder_mass_recoil, at least two leptons required." << std::endl;
        exit(1);
    }
  
    if(result.size() > 1) {
  
        Vec_rp bestReso;
        
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {
            
            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        
            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }

     
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
        }
        else {
            std::cout << "ERROR: resonanceBuilder_mass_recoil, no mininum found." << std::endl;
            exit(1);
        }
        return bestReso;
    }
    else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}    




struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}
 
 
 
// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
}

// calculate the cosine(theta) of the missing energy vector
float get_cosTheta_miss(Vec_rp met){
    
    float costheta = 0.;
    if(met.size() > 0) {
        
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));
    }
    return costheta;
}

std::vector<std::vector<int>> sel_dijet_score(ROOT::VecOps::RVec<float> score1, ROOT::VecOps::RVec<float> score2, std::vector<int> exclude_jets, bool exclude_pair_flip) {
    std::vector<std::vector<int>> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < score1.size(); ++i) { //assuming here that u_score and d_score for the same jet are complementary so a jet wouldn't pass the check with itself
        if (std::find(exclude_jets.begin(), exclude_jets.end(), i) != exclude_jets.end()) continue;
        for (size_t j = 0; j < score2.size(); ++j){ //making sure not to check the same pair twice in this way
            if (std::find(exclude_jets.begin(), exclude_jets.end(), j) != exclude_jets.end()) continue;

            if (exclude_pair_flip == true && j<=i) continue; //excludes checking for the same pair and saving the dijet twice, useful is scores are the same variable being checked twice
            
            if ((score1[i]>0.5 && score2[j]>0.5)){
                result.emplace_back(); //creates new row

                result.back().emplace_back(i); //fill the row with the pair of jets indices, they correspond to the same class used for the jets variables and the scores
                result.back().emplace_back(j);
            }
        }
    }

    return result; //result.size() will give the number of pairs/rows passing the selection
  }

std::vector<float> get_dijet_mass(std::vector<std::vector<int>> dijets_idx,  ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.M()); //invariant mass of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_dijet_px(std::vector<std::vector<int>> dijets_idx,  ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Px()); //px of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_dijet_py(std::vector<std::vector<int>> dijets_idx,  ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Py()); //py of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_dijet_pz(std::vector<std::vector<int>> dijets_idx,  ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Pz()); //pz of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_dijet_energy(std::vector<std::vector<int>> dijets_idx,  ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.E()); //energy of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<std::tuple<int, int, int, int, bool>> get_trijet_idx(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, bool lead_jet_flavor) { 
    std::vector<std::tuple<int, int, int, int, bool>> result; 

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows
        std::tuple<int, int, int, int, bool> trijet(
            lead_jet_idx,           // Leading jet index
            dijets_idx[i][0],       // First dijet index
            dijets_idx[i][1],       // Second dijet index
            static_cast<int>(i),    // Index of the dijet pair
            lead_jet_flavor         // Leading jet flavor
        );
        
        result.push_back(trijet);
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_trijet_mass(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[lead_jet_idx] + jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.M()); //invariant mass of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_trijet_px(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[lead_jet_idx] + jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Px()); //px of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_trijet_py(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[lead_jet_idx] + jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Py()); //py of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_trijet_pz(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[lead_jet_idx] + jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.Pz()); //pz of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

std::vector<float> get_trijet_energy(std::vector<std::vector<int>> dijets_idx, int lead_jet_idx, ROOT::VecOps::RVec<TLorentzVector> jets_p4) { 
    std::vector<float> result; //returns vectors of indices of pairs of jets passing the selection

    for (size_t i = 0; i < dijets_idx.size(); ++i) { //this is meant to work after sel_dijet_score so it's already organised in pairs of jets with one index sampling the rows

        TLorentzVector p4 = jets_p4[lead_jet_idx] + jets_p4[dijets_idx[i][0]] + jets_p4[dijets_idx[i][1]];
        result.emplace_back(p4.E()); //energy of the dijet
        }
  
    return result; //result.size() will give the number of pairs/rows passing the selection
}

  // --- functions Helper
float deltaEta(float eta1, float eta2) {
    return std::abs(eta1 - eta2);
  }

float deltaPhi(float phi1, float phi2){
    float PHI = std::abs(phi1-phi2);
    if (PHI<=3.14159265)
      return PHI;
    else
      return 2*3.14159265-PHI;
  }

float deltaR(float phi1, float phi2, float eta1, float eta2) {
    return sqrt(deltaEta(eta1,eta2)*deltaEta(eta1,eta2) + deltaPhi(phi1,phi2)*deltaPhi(phi1,phi2));
  }

ROOT::VecOps::RVec<int> deltaR_sel_idx(ROOT::VecOps::RVec<float> phi1, ROOT::VecOps::RVec<float> phi2, ROOT::VecOps::RVec<float> eta1, ROOT::VecOps::RVec<float> eta2, float min_delta) {
    ROOT::VecOps::RVec<int> result;
    for (size_t i = 0; i < phi1.size(); ++i) {  
        float DR1 = sqrt(deltaEta(eta1[i],eta2[1])*deltaEta(eta1[i],eta2[1]) + deltaPhi(phi1[i],phi2[1])*deltaPhi(phi1[i],phi2[1]));
        float DR2 = sqrt(deltaEta(eta1[i],eta2[2])*deltaEta(eta1[i],eta2[2]) + deltaPhi(phi1[i],phi2[2])*deltaPhi(phi1[i],phi2[2]));
        if (DR1>min_delta && DR2>min_delta) result.push_back(i);
    }
    return result;
  }


float get_gamma(float p, float e) {
    float c = 2.998e8;
    float beta = p/e;
    float gamma = 1./(sqrt(1 - beta*beta));
    return gamma;
  }

//supports vectors of _tlv of different sizes, if one of them is size one then it's used recursively otherwise the smaller size of the vectors is used to get the value
ROOT::VecOps::RVec<float> get_scalar( ROOT::VecOps::RVec<TLorentzVector> v1,  ROOT::VecOps::RVec<TLorentzVector> v2) {
    ROOT::VecOps::RVec<float> result;
    if (v2.size()==1 && v1.size()>1) {
    TLorentzVector v = v2[0];
        for (size_t i = 0; i < v1.size(); ++i) {  
        result.push_back(v1[i].Px()*v[0] + v1[i].Py()*v[1] + v1[i].Pz()*v[2]);
        }
    }
    else if (v1.size()==1 && v2.size()>1) {
        TLorentzVector v = v1[0];
        for (size_t i = 0; i < v2.size(); ++i) {  
        result.push_back(v2[i].Px()*v[0] + v2[i].Py()*v[1] + v2[i].Pz()*v[2]);
        }
    }
    else {
        float size = std::min(v1.size(), v2.size());
        for (size_t i = 0; i < size; ++i) {  
        result.push_back(v1[i].Px()*v2[i].Px() + v1[i].Py()*v2[i].Py() + v1[i].Pz()*v2[i].Pz());
        }
    }
    return result;
}

ROOT::VecOps::RVec<TLorentzVector> build_p4(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz, ROOT::VecOps::RVec<float> e) {
    ROOT::VecOps::RVec<TLorentzVector> p4;
    for (size_t i = 0; i < px.size(); ++i) {  
        TLorentzVector tlv;
        tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        p4.push_back(tlv);
    }
    return p4;
}

TLorentzVector build_p4_single(float px, float py, float pz, float e) {
    TLorentzVector tlv;
    tlv.SetPxPyPzE(px, py, pz, e);
    return tlv;
}

ROOT::VecOps::RVec<float> get_p_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  
        result.push_back(vec[i].P());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_mass_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  
        result.push_back(vec[i].M());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_e_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].E());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_px_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Px());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_py_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Py());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_pz_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Pz());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_pt_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Pt());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_eta_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Eta());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_phi_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Phi());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_theta_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Theta());
    }
    return result;
}

ROOT::VecOps::RVec<float> get_y_tlv(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        result.push_back(vec[i].Rapidity());
    }
    return result;
}

ROOT::VecOps::RVec<TLorentzVector> boosted_p4(TLorentzVector boost, ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    for (size_t i = 0; i < vec.size(); ++i) {
        TLorentzVector boosted=vec[i];
        boosted.Boost( - boost.BoostVector());
        result.push_back(boosted);
    }
    return result;
}

std::vector<std::vector<int>> sel_dilep_mass_idx(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, float min_dimass, float max_dimass) {
    std::vector<std::vector<int>> result;
    result.reserve(in.size());

    for (size_t i = 0; i < in.size(); ++i) {
        auto & p1 = in[i];
        for (size_t j = i + 1; j < in.size(); ++j){
            auto & p2 = in[j];

            if (p1.charge == - p2.charge) {
                float px = p1.momentum.x + p2.momentum.x;
                float py = p1.momentum.y + p2.momentum.y;
                float pz = p1.momentum.z + p2.momentum.z;
                float e = p1.energy + p2.energy;
                float inv = std::sqrt( e*e - px*px - py*py - pz*pz);

                if (inv>min_dimass && inv<max_dimass) {
                    result.emplace_back(); //creates new row

                    result.back().emplace_back(i); //fill the row with the pair of indices, they correspond to the same class used 
                    result.back().emplace_back(j);
                }
            }
        }
  }
  return result;
}

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> findTauInJet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0;

        // Find Lead (This needs to change to first sort the jcs by p or pt, it is very messy right now)

        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        // Eventually the FCC sw should have better ID for the particles, based on the detector. 
        // For the moment I compare the reconstructed  masses and charges to known values
        // (since that is what the PID module as references does). This is something to be improved in the future! 
        // Too truth-based.


        // First loop just to find the lead (not very efficient). 
        for (const auto& jc : jcs) {

            // No electrons or muons
            if (fabs(jc.mass -  0.105658) < 1.e-03) {
                tauID=-13;
                continue; 
                }
            if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                tauID=-11;
                continue; //stops the loop on jet constituents as soon as it finds a lepton
            }

            // Anything else lets: find the highest pt one, charged particle as lead only
            if ((jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
            }
        }

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        }//jets with electrons or muon, cannot be tau jets

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;

        // Now I loop to build the tau adding candidates to the lead
        // Only if they satisfy some conditions: distance, charge, etc 
        for (const auto& jc : jcs) {

            TLorentzVector tlv;  
            tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

            if (tlv==lead) continue;

            // Distance (in terms of Theta)
            double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

            // The Pt cut and Distance are parameters to tune in the future
            if (tlv.Pt()<1 || dTheta>0.20) continue;

            // Now count! 
            if (jc.charge>0) count_piP++;   

            else if (jc.charge<0) count_piM++;  

            else  count_pho++;

            sum_tau += tlv;  // This is the 4 momenta of only the particles we have selected

        }

        // Now we have a tau candidate and its momentum (sum_tau).
        // Lets build the ID : count the charged pions and the neutrals. 
        // The charge of the tau must be +1 or -1. 
        // Considering the decays of the tau: we want candidates with one or three charged candidates (one or three prongs) 
        //std::cout<<" Count? "<<count_piP<<"   "<<count_piM<<"  "<<count_pho<<"   "<<count_pho<<std::endl;
        // The ID number assigned is a bit dummy, helps to keep track of the kind of candidate we have (and see if we can be more restrictive)

        if (tauID!=-13 && tauID!=-11 && abs(count_piP-count_piM)==1 && ( (count_piP+count_piM)==1 || (count_piP+count_piM)==3) ){    

            if( (count_piP+count_piM)==1 && count_pho==0) tauID=0;
            if( (count_piP+count_piM)==1 && count_pho==1) tauID=1;
            if( (count_piP+count_piM)==1 && count_pho==2) tauID=2;
            if( (count_piP+count_piM)==1 && count_pho==3) tauID=3;
            if( (count_piP+count_piM)==1 && count_pho==4) tauID=4;
            if( (count_piP+count_piM)==1 && count_pho==5) tauID=5;
            if( (count_piP+count_piM)==1 && count_pho>=6) tauID=6;

            if( (count_piP+count_piM)==3 && count_pho==0)  tauID=10;
            if( (count_piP+count_piM)==3 && count_pho==1)  tauID=11;
            if( (count_piP+count_piM)==3 && count_pho==2)  tauID=12;
            if( (count_piP+count_piM)==3 && count_pho==3)  tauID=13;
            if( (count_piP+count_piM)==3 && count_pho==4)  tauID=14;
            if( (count_piP+count_piM)==3 && count_pho==5)  tauID=15;
            if( (count_piP+count_piM)==3 && count_pho>=6)  tauID=16;

            partMod.momentum.x=sum_tau.Px();
            partMod.momentum.y=sum_tau.Py();
            partMod.momentum.z=sum_tau.Pz();
            partMod.mass= sum_tau.M();
            partMod.energy= sum_tau.E();
            partMod.charge= (count_piP-count_piM);
            partMod.type = tauID;

            if (tauID!=-1 && partMod.mass<3)  out.push_back(partMod);
            else {
                partMod.momentum.x = 0;
                partMod.momentum.y = 0;
                partMod.momentum.z = 0;
                partMod.mass = 0;
                partMod.energy= 0;
                partMod.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                tauID = -2;
                partMod.type = tauID;
                out.push_back(partMod);
            }
        }

        else {
            tauID=-3;
            partMod.type = tauID;
            out.push_back(partMod);
        }
    }
    return out;

}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_pi0(const ROOT::VecOps::RVec<FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents>& jets){
	// Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
	// This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
	// Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it
	ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0, count_pi0=0;

        // Find Lead (This needs to change to first sort the jcs by p or pt, it is very messy right now)

        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        // Eventually the FCC sw should have better ID for the particles, based on the detector. 
        // For the moment I compare the reconstructed  masses and charges to known values
        // (since that is what the PID module as references does). This is something to be improved in the future! 
        // Too truth-based.


        // First loop just to find the lead (not very efficient). 
        for (const auto& jc : jcs) {

            // No electrons or muons
            if (fabs(jc.mass -  0.105658) < 1.e-03) {
                tauID=-13;
                continue; 
                }
            if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                tauID=-11;
                continue; //stops the loop on jet constituents as soon as it finds a lepton
            }

            // Anything else lets: find the highest pt one, charged particle as lead only
            if ((jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
            }
        }

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        }//jets with electrons or muon, cannot be tau jets

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;

        // Now I loop to build the tau adding candidates to the lead
        // Only if they satisfy some conditions: distance, charge, etc 
        for (const auto& jc : jcs) {

            TLorentzVector tlv;  
            tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

            if (tlv==lead) continue;

            // Distance (in terms of Theta)
            double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

            // The Pt cut and Distance are parameters to tune in the future
            if (tlv.Pt()<1 || dTheta>0.20) continue;

            // Now count! 
            if (jc.charge>0) count_piP++;   

            else if (jc.charge<0) count_piM++;  

            else  count_pho++;

            sum_tau += tlv;  // This is the 4 momenta of only the particles we have selected

        }
        
		// Now we have a tau candidate and its momentum (sum_tau).
		// Lets build the ID : count the charged pions and the neutrals.
		// The charge of the tau must be +1 or -1. 
		// Considering the decays of the tau: we want candidates with one or three charged candidates (one or three prongs) 
		//std::cout<<" Count? "<<count_piP<<"   "<<count_piM<<"  "<<count_pho<<"   "<<count_pho<<std::endl;
		// The ID number assigned is a bit dummy, helps to keep track of the kind of candidate we have (and see if we can be more restrictive)
		
		//check if how many pi0 can be in photons(max is set to 3)
		if(count_pho>1){
			
			double mass_tolerance = 0.015732*6.5; //stolen from Lars from some Breit-Wigner-Fit
			int best_mass_idx[6] = {-1,-1,-1,-1,-1,-1};
			for(i=0; i<6;i=i+2){
				double min_mass_diff = 10000.;
				int current_best_idx[2] = {-1,-1};
				int gamma1_idx = 0;
				for(const auto& jc : jcs){
					if(jc.charge!=0) continue;
					if(std::any_of(std::begin(best_mass_idx), std::end(best_mass_idx), [&](int i) { return i == gamma1_idx;})){
						++gamma1_idx;
						continue;
					}
					TLorentzVector gamma1;
					gamma1.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
					int gamma2_idx = 0;
					for(const auto& jc1 : jcs){
						if(jc1.charge!=0) continue;
						if(std::any_of(std::begin(best_mass_idx), std::end(best_mass_idx), [&](int i) { return i == gamma2_idx;})){
							++gamma2_idx;
							continue;
						}
						TLorentzVector gamma2;
						gamma2.SetPxPyPzE(jc1.momentum.x, jc1.momentum.y, jc1.momentum.z, jc1.energy);
						if(gamma1==gamma2){
							++gamma2_idx;
							continue;
						}
						if(gamma2_idx<gamma1_idx){
							++gamma2_idx;
							continue;
						}
						TLorentzVector Digamma = gamma1 + gamma2;	
						if((Digamma.M()-0.1349768) < mass_tolerance && Digamma.M()-0.1349768 < min_mass_diff){
							min_mass_diff = Digamma.M()-0.1349768;
							current_best_idx[0] = gamma1_idx;
							current_best_idx[1] = gamma2_idx; 
						}
					}
					++gamma1_idx;
				}
				if(current_best_idx[i]>-1) count_pi0++;
				best_mass_idx[i] = current_best_idx[0];
				best_mass_idx[i+1] = current_best_idx[1];
			}
		}
	
		if(tauID!=-13 && tauID!=-11 && abs(count_piP-count_piM)==1 && ((count_piP+count_piM)==1 || (count_piP+count_piM)==3)){

			if((count_piP+count_piM)==1 && count_pi0==0) tauID=9;
			if((count_piP+count_piM)==1 && count_pi0==1) tauID=14;
			if((count_piP+count_piM)==1 && count_pi0==2) tauID=20;
			if((count_piP+count_piM)==1 && count_pi0==3) tauID=27;
		
			if((count_piP+count_piM)==3 && count_pi0==0) tauID=67;
			if((count_piP+count_piM)==3 && count_pi0==1) tauID=76;
			if((count_piP+count_piM)==3 && count_pi0==2) tauID=87;

			partMod.momentum.x=sum_tau.Px();
			partMod.momentum.y=sum_tau.Py();
			partMod.momentum.z=sum_tau.Pz();
			partMod.mass= sum_tau.M();
			partMod.charge= (count_piP-count_piM);
			partMod.type = tauID;
			if(tauID!=-1 && partMod.mass<3) out.push_back(partMod);
			else{
				partMod.momentum.x = 0;
				partMod.momentum.y = 0;
				partMod.momentum.z = 0;
				partMod.mass = 0;
				partMod.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
				tauID = -1;
				partMod.type = tauID;
				out.push_back(partMod);
			}
		}

		else{
			tauID=-1;
			partMod.type = tauID;
			out.push_back(partMod);
		}
	}
	return out;
}

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> findTauInJet_OG (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){ //original function from maria

       // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
       // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
       // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

       ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

       // Loop over jets:
       
       for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0;

        // Find Lead (This needs to change to first sort the jcs by p or pt, it is very messy right now)
         
        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        // Eventually the FCC sw should have better ID for the particles, based on the detector. 
        // For the moment I compare the reconstructed  masses and charges to known values
        // (since that is what the PID module as references does). This is something to be improved in the future! 
        // Too truth-based.


        // First loop just to find the lead (not very efficient). 
        for (const auto& jc : jcs) {

           // I want the lead particle to be charged
           if (jc.charge==0) continue;
          
           // No electrons or muons
            if(  fabs(jc.mass -  0.105658) < 1.e-03) {
                        tauID=-13;
                        continue;
             }
             if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                        tauID=-11; continue;
             }

           // Anything else lets: find the highest pt one 
           if ((jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt()){
                        lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                        chargeLead=jc.charge;
           }
         }

        //std::cout<<"Jet? "<<i<<std::endl;
        //std::cout<<"Lead? "<<lead.Pt()<<"   "<<lead.Phi()<<"  "<<lead.Theta()<<std::endl;
     
        // Clean and start counting
        if (lead.Pt()<2) continue; // Too low pt 
        if (chargeLead==1) count_piP++;
        else if (chargeLead==-1) count_piM++;
        else {continue;} // This cannot happen 
        sum_tau+=lead;


        // Now I loop to build the tau adding candidates to the lead
        // Only if they satisfy some conditions: distance, charge, etc 
        for (const auto& jc : jcs) {

          TLorentzVector tlv;  
          tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

          if (tlv==lead) {
                        //std::cout<<"  skip lead "<<tlv.Pt()<<std::endl; 
                        continue;}

          // Distance (in terms of Theta)
          double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

//          std::cout<<"    cand?   " <<jc.mass<<"   "<<jc.type<<"   "<<tlv.Pt()<<"   "<<tlv.Phi()<<"   "<<tlv.Theta()<<"    "<<jc.charge<<"   "<<dTheta<<std::endl;//"  ->  "<<jet.Phi()-tlv.Phi()<<"  "<<jet.Theta()-tlv.Theta()<<std::endl;

          // Skip Muons and Electrons. If there is a muon or electron, this is not an hadronic tau! Save for the ID
          if(  fabs(jc.mass -  0.105658) < 1.e-03) {
                        tauID=-13; 
                        continue;
          }  
          if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                        tauID=-11; continue;
          }

          // The Pt cut and Distance are parameters to tune in the future
          if (tlv.Pt()<1 || dTheta>0.20) {continue;} 

          //  if(  fabs(jc.mass - 0.13957)< 1.e-03 ) {  // I tested this and rejected it: I want the kaons, not only the pions
          
          // Now count! 
          if(jc.charge>0) count_piP++;    
          else if (jc.charge<0) count_piM++;   
          else  count_pho++;

//          else if (jc.type == 22 ) count_pho++;
//          else {count_nu++; continue;}  // I am not distinguishing photons and pi0s. Could be tried in the future. 

          sum_tau += tlv;  // This is the 4 momenta of only the particles we have selected

        }


         // Now we have a tau candidate and its momentum (sum_tau).
         // Lets build the ID : count the charged pions and the neutrals. 
         // The charge of the tau must be +1 or -1. 
         // Considering the decays of the tau: we want candidates with one or three charged candidates (one or three prongs) 
         //std::cout<<" Count? "<<count_piP<<"   "<<count_piM<<"  "<<count_pho<<"   "<<count_pho<<std::endl;
         // The ID number assigned is a bit dummy, helps to keep track of the kind of candidate we have (and see if we can be more restrictive)

         if (tauID!=-13 && tauID!=-11  && abs(count_piP-count_piM)==1 && ( (count_piP+count_piM)==1 || (count_piP+count_piM)==3) ){    

            if( (count_piP+count_piM)==1 && count_pho==0) tauID=0;
            if( (count_piP+count_piM)==1 && count_pho==1) tauID=1;
            if( (count_piP+count_piM)==1 && count_pho==2) tauID=2;
            if( (count_piP+count_piM)==1 && count_pho==3) tauID=3;
            if( (count_piP+count_piM)==1 && count_pho==4) tauID=4;
            if( (count_piP+count_piM)==1 && count_pho==5) tauID=5;
            if( (count_piP+count_piM)==1 && count_pho>=6) tauID=6;

            if( (count_piP+count_piM)==3 && count_pho==0)  tauID=10;
            if( (count_piP+count_piM)==3 && count_pho==1)  tauID=11;
            if( (count_piP+count_piM)==3 && count_pho==2)  tauID=12;
            if( (count_piP+count_piM)==3 && count_pho==3)  tauID=13;
            if( (count_piP+count_piM)==3 && count_pho==4)  tauID=14;
            if( (count_piP+count_piM)==3 && count_pho==5)  tauID=15;
            if( (count_piP+count_piM)==3 && count_pho>=6)  tauID=16;

          }

          //std::cout<<" -->  Tau? "<<tauID<<"    "<<count_piP-count_piM<<"   "<<sum_tau.Pt()<<"   "<<sum_tau.Phi()<<"    "<<sum_tau.Theta()<<"   "<<sum_tau.M()<<std::endl;

          // Only save the tau if the ID makes sense, and if it has a reasonable mass (another parameter to tune)
          if (tauID!=-1){
            edm4hep::ReconstructedParticleData partMod; // =recop.at(recind.at(i));
            partMod.momentum.x=sum_tau.Px();
            partMod.momentum.y=sum_tau.Py();
            partMod.momentum.z=sum_tau.Pz();
            partMod.mass= sum_tau.M();
            partMod.charge= (count_piP-count_piM);
            partMod.type = tauID;
            if (tauID!=-1 && partMod.mass<3)  out.push_back(partMod);
 
          }

        }
        return out;

}


std::vector<int> FindBest_3(ROOT::VecOps::RVec<TLorentzVector> P4vector, ROOT::VecOps::RVec<float> vec_charge, ROOT::VecOps::RVec<float> vec_mass, double mass){ 

    double minDistance=10000;
    int dau1=-1;
    int dau2=-1;

    for (int i=0; i<P4vector.size(); i++){
        for (int j=i+1; j<P4vector.size(); j++){
            if ((vec_charge[i]!=vec_charge[j]) && (abs(vec_mass[i]-vec_mass[j])<0.01)) {
                TLorentzVector DiObj=P4vector[i]+P4vector[j];
                if ( fabs(DiObj.M()-mass)<minDistance) {
                    minDistance=fabs(DiObj.M()-mass);
                    dau1=i;
                    dau2=j; 
                }
            }
        }
    }
    int third=-1; 
    double ptThird=0;

    for (int i=0; i<P4vector.size(); i++){
        if (i==dau1 || i==dau2) continue;
        if ((P4vector[i].Pt()>ptThird) && (abs(vec_mass[i]-vec_mass[dau1])<0.01)) { 
            ptThird=P4vector[i].Pt(); 
            third=i;
            }
        }

    std::vector<int> idx;
    idx.push_back(dau1);
    idx.push_back(dau2); 
    idx.push_back(third); 

    return idx;
} 

std::vector<int> FindBest_4(ROOT::VecOps::RVec<TLorentzVector> P4vector, ROOT::VecOps::RVec<float> vec_charge, ROOT::VecOps::RVec<float> vec_mass, double mass1, double mass2){ 

    double minDistance=10000;
    int dau1=-1;
    int dau2=-1;

    for (int i=0; i<P4vector.size(); i++){
        for (int j=i+1; j<P4vector.size(); j++){
            if ((vec_charge[i]!=vec_charge[j]) && (abs(vec_mass[i]-vec_mass[j])<0.01)) {
                TLorentzVector DiObj=P4vector[i]+P4vector[j];
                if ( fabs(DiObj.M()-mass1)<minDistance) {
                    minDistance=fabs(DiObj.M()-mass1);
                    dau1=i;
                    dau2=j; 
                }
            }
        }
    }
    minDistance=10000;
    int dau3=-1;
    int dau4=-1;

    for (int i=0; i<P4vector.size(); i++){
        if (i==dau1 || i==dau2) continue;
        for (int j=i+1; j<P4vector.size(); j++){
            if (j==dau1 || j==dau2) continue;
            if (vec_charge[i]!=vec_charge[j]){
                TLorentzVector DiObj=P4vector[i]+P4vector[j];
                if ( fabs(DiObj.M()-mass2)<minDistance) {
                    minDistance=fabs(DiObj.M()-mass2);
                    dau3=i;
                    dau4=j; 
                }
            }
        }
    }

    std::vector<int> idx;
    idx.push_back(dau1);
    idx.push_back(dau2); 
    idx.push_back(dau3); 
    idx.push_back(dau4); 

    return idx;
} 

ROOT::VecOps::RVec<int> get_PID(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
    ROOT::VecOps::RVec<int> result;
    for (auto & p: in) {
        result.push_back(p.goodnessOfPID);
    }
    return result;
}


}}

#endif
