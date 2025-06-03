#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <random>
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
    return eta1 - eta2;
  }

float deltaPhi(float phi1, float phi2){
    float PHI = 3.14159265;
    return PHI - std::abs(std::abs(phi1-phi2) - PHI);
  }

float deltaR(float phi1, float phi2, float eta1, float eta2) {
    return sqrt(deltaEta(eta1,eta2)*deltaEta(eta1,eta2) + deltaPhi(phi1,phi2)*deltaPhi(phi1,phi2));
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

ROOT::VecOps::RVec<float> build_float(float v1, float v2) {
    ROOT::VecOps::RVec<float> result;
    result.push_back(v1);
    result.push_back(v2);
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

ROOT::VecOps::RVec<TLorentzVector> build_p4_class(TLorentzVector v1, TLorentzVector v2) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    result.push_back(v1);
    result.push_back(v2);
    return result;
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

TLorentzVector boosted_p4_single(TLorentzVector boost, TLorentzVector vec) {
    vec.Boost( - boost.BoostVector());
    return vec;
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

ROOT::VecOps::RVec<int> deltaR_sel_idx_v2(ROOT::VecOps::RVec<float> phi1, ROOT::VecOps::RVec<float> phi2, ROOT::VecOps::RVec<float> eta1, ROOT::VecOps::RVec<float> eta2, float min_delta) {
    ROOT::VecOps::RVec<int> result;
    std::vector<bool> matches(phi2.size(), false);

    for (size_t i = 0; i < phi1.size(); ++i) { //run over first vector of particles
        size_t check = -1;
        float DR_min = min_delta; //value to start with comparing the matches with the second particles, reset for next first particle

        for (size_t j = 0; j < phi2.size(); ++j) {  //run over second vector of particles
            if (matches[j]) continue; //skip if the second particle has already a match

            float DR = sqrt(deltaEta(eta1[i],eta2[j])*deltaEta(eta1[i],eta2[j]) + deltaPhi(phi1[i],phi2[j])*deltaPhi(phi1[i],phi2[j]));
            
            if (DR<DR_min) { //fisr iteration is min_delta, then new minumum to match
                DR_min = DR; 
                check = j;
            }   
        }

        if (check!=-1) { //make sure two first particles are not matched to the same second particle
            result.push_back(i);
            matches[check] = true; //second particle matched now
        }
    }
    return result;
  }

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_Charged (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        TLorentzVector neutral;
        TLorentzVector charged;
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauCharged;
        edm4hep::ReconstructedParticleData TauNeutral;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int track;
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
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
                track = jc.tracks_begin;
            }
        }

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            out.push_back(TauCharged); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            out.push_back(TauCharged); //make sure to keep this iteration saved as non tau jets
            continue;
        }//jets with electrons or muon, cannot be tau jets

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;
        charged+=lead;

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
            if (jc.charge>0) {
                count_piP++; 
                charged+=tlv;
                }  

            else if (jc.charge<0) {
                count_piM++;  
                charged+=tlv;
                }

            else  {
                count_pho++;
                neutral+=tlv;
                }

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

            Tau.momentum.x=sum_tau.Px();
            Tau.momentum.y=sum_tau.Py();
            Tau.momentum.z=sum_tau.Pz();
            Tau.mass= sum_tau.M();
            Tau.energy= sum_tau.E();
            Tau.charge= (count_piP-count_piM);
            Tau.type = tauID;
            Tau.tracks_begin = 0;

            TauCharged.momentum.x=charged.Px();
            TauCharged.momentum.y=charged.Py();
            TauCharged.momentum.z=charged.Pz();
            TauCharged.mass= charged.M();
            TauCharged.energy= charged.E();
            TauCharged.charge= chargeLead;
            TauCharged.type = tauID;
            TauCharged.tracks_begin = track;

            TauNeutral.momentum.x=neutral.Px();
            TauNeutral.momentum.y=neutral.Py();
            TauNeutral.momentum.z=neutral.Pz();
            TauNeutral.mass= neutral.M();
            TauNeutral.energy= neutral.E();
            TauNeutral.charge= chargeLead;
            TauNeutral.type = tauID;
            TauNeutral.tracks_begin = track;

            if (tauID!=-1 && Tau.mass<3)  {
                out.push_back(TauCharged);
            }
            else {
                Tau.momentum.x = 0;
                Tau.momentum.y = 0;
                Tau.momentum.z = 0;
                Tau.mass = 0;
                Tau.energy= 0;
                Tau.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                tauID = -2;
                Tau.type = tauID;

                TauCharged.momentum.x = 0;
                TauCharged.momentum.y = 0;
                TauCharged.momentum.z = 0;
                TauCharged.mass = 0;
                TauCharged.energy= 0;
                TauCharged.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                TauCharged.type = tauID;

                TauNeutral.momentum.x = 0;
                TauNeutral.momentum.y = 0;
                TauNeutral.momentum.z = 0;
                TauNeutral.mass = 0;
                TauNeutral.energy= 0;
                TauNeutral.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                TauNeutral.type = tauID;

                out.push_back(TauCharged);
            }
        }

        else {
            tauID=-3;
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            
            out.push_back(TauCharged);
        }
    }
    return out;

}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_Neutral (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        TLorentzVector neutral;
        TLorentzVector charged;
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauCharged;
        edm4hep::ReconstructedParticleData TauNeutral;
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
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
            }
        }

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            out.push_back(TauNeutral); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            out.push_back(TauNeutral); //make sure to keep this iteration saved as non tau jets
            continue;
        }//jets with electrons or muon, cannot be tau jets

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;
        charged+=lead;

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
            if (jc.charge>0) {
                count_piP++; 
                charged+=tlv;
                }  

            else if (jc.charge<0) {
                count_piM++;  
                charged+=tlv;
                }

            else  {
                count_pho++;
                neutral+=tlv;
                }

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

            Tau.momentum.x=sum_tau.Px();
            Tau.momentum.y=sum_tau.Py();
            Tau.momentum.z=sum_tau.Pz();
            Tau.mass= sum_tau.M();
            Tau.energy= sum_tau.E();
            Tau.charge= (count_piP-count_piM);
            Tau.type = tauID;

            TauCharged.momentum.x=charged.Px();
            TauCharged.momentum.y=charged.Py();
            TauCharged.momentum.z=charged.Pz();
            TauCharged.mass= charged.M();
            TauCharged.energy= charged.E();
            TauCharged.charge= chargeLead;
            TauCharged.type = tauID;

            TauNeutral.momentum.x=neutral.Px();
            TauNeutral.momentum.y=neutral.Py();
            TauNeutral.momentum.z=neutral.Pz();
            TauNeutral.mass= neutral.M();
            TauNeutral.energy= neutral.E();
            TauNeutral.charge= chargeLead;
            // charge of the mother tau
            TauNeutral.type = tauID;

            if (tauID!=-1 && Tau.mass<3)  {
                out.push_back(TauNeutral);
            }
            else {
                Tau.momentum.x = 0;
                Tau.momentum.y = 0;
                Tau.momentum.z = 0;
                Tau.mass = 0;
                Tau.energy= 0;
                Tau.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                tauID = -2;
                Tau.type = tauID;

                TauCharged.momentum.x = 0;
                TauCharged.momentum.y = 0;
                TauCharged.momentum.z = 0;
                TauCharged.mass = 0;
                TauCharged.energy= 0;
                TauCharged.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                TauCharged.type = tauID;

                TauNeutral.momentum.x = 0;
                TauNeutral.momentum.y = 0;
                TauNeutral.momentum.z = 0;
                TauNeutral.mass = 0;
                TauNeutral.energy= 0;
                TauNeutral.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                TauNeutral.type = tauID;

                out.push_back(TauNeutral);
            }
        }

        else {
            tauID=-3;
            Tau.type = tauID;
            TauCharged.type = tauID;
            TauNeutral.type = tauID;
            
            out.push_back(TauNeutral);
        }
    }
    return out;

}

//to use for tagged jets instead of explicit tau reconstruction but the idea of what I want is the same
ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> Jet_LeadingCharged(const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){
    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> result;
    for (int i = 0; i < jets.size(); ++i){

        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        TLorentzVector lead;
        int chargeLead=0;
        int track=0;
        
        for (const auto &jc : jcs){
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
            lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
            chargeLead=jc.charge;
            track = jc.tracks_begin;
        }
        }

        partMod.momentum.x=lead.Px();
        partMod.momentum.y=lead.Py();
        partMod.momentum.z=lead.Pz();
        partMod.mass= lead.M();
        partMod.energy= lead.E();
        partMod.charge= chargeLead;
        partMod.tracks_begin = track;
        
        result.push_back(partMod);
    }
    return result;
}

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> Jet_Charged(const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){
    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> result;
    for (int i = 0; i < jets.size(); ++i){

        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int chargeLead=0;
        int track=0;
        TLorentzVector sum;
        TLorentzVector lead;
        
        for (const auto &jc : jcs){
            if (jc.charge!=0) {
                TLorentzVector temp;
                temp.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead+=jc.charge;
                sum+=temp;
            
                if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt()){
                    track = jc.tracks_begin;
                    lead=temp;
            }
        }
        }

        partMod.momentum.x=sum.Px();
        partMod.momentum.y=sum.Py();
        partMod.momentum.z=sum.Pz();
        partMod.mass= sum.M();
        partMod.energy= sum.E();
        partMod.charge= chargeLead;
        partMod.tracks_begin = track;
        
        result.push_back(partMod);
    }
    return result;
}

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> Jet_Neutral(const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){
    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> result;
    for (int i = 0; i < jets.size(); ++i){

        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        TLorentzVector sum;
        int chargeLead=0;
        
        for (const auto &jc : jcs){
            if (jc.charge==0){
                TLorentzVector lead;
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                sum+=lead;
            }
        }

        partMod.momentum.x=sum.Px();
        partMod.momentum.y=sum.Py();
        partMod.momentum.z=sum.Pz();
        partMod.mass= sum.M();
        partMod.energy= sum.E();
        partMod.charge= chargeLead;
        
        result.push_back(partMod);
    }
    return result;
}

const double m_tau = 1.777;  // GeV/c^2

ROOT::VecOps::RVec<float> get_phi_track(ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<float> result;
    for (size_t i = 0; i < vec.size(); ++i) {  // Iterate over the indices
        double norm = std::sqrt(vec[i].X()*vec[i].X() + vec[i].Y()*vec[i].Y());
        result.push_back(atan2( - vec[i].X()/norm, vec[i].Y()/norm));
    }
    return result;
}

// Function to get the impact parameter vector from the track, defined in the origin frame pointing to the point on the track that is closest to the IP
ROOT::VecOps::RVec<TLorentzVector> ImpactVector(ROOT::VecOps::RVec<TLorentzVector> Track, ROOT::VecOps::RVec<float> D0, ROOT::VecOps::RVec<float> Z0) {

    ROOT::VecOps::RVec<TLorentzVector> impact;  

    for (size_t i = 0; i < Track.size(); ++i) {
        // Using the dot product condition to ensure perpendicularity
        double x2, y2;
        double z2 = Z0[i];
        double norm = std::sqrt(Track[i].X()*Track[i].X() + Track[i].Y()*Track[i].Y());

        double x1 = Track[i].X()/norm;
        double y1 = Track[i].Y()/norm;
        /*if (D0[i]>=0) { 
            x2 = - D0[i] * y1;
            y2 = D0[i] * x1;
        }
        else { 
            x2 = D0[i] * y1;
            y2 = - D0[i] * x1;
        }*/

        double phi = Track[i].Phi() + 3.141592653589793/2;
        x2 = D0[i] * std::cos(phi);
        y2 = D0[i] * std::sin(phi);

        TLorentzVector perp_vector(x2, y2, Z0[i], 0.);
        impact.push_back(perp_vector);
    }

    return impact;
}

// find the intersection between two tracks defined by one point and one vector (both TVector3)
TVector3 findIntersection(const TVector3& P1, const TVector3& d1, const TVector3& P2, const TVector3& d2) {
    TVector3 closestPoint;
    TVector3 crossDir = d1.Cross(d2);
    double denom = crossDir.Mag2();

    // Handle parallel lines
    if (denom == 0) {  
        TVector3 diff = P2 - P1;

        // Find the closest point on line 2 from P2
        double s = diff.Dot(d2) / d2.Mag2();
        TVector3 point2 = P2 + s * d2;
        
        closestPoint = point2;
    }
    else{
        // Calculate parameters t and s for line equations
        TVector3 diff = P2 - P1;
        double t = (diff.Cross(d2)).Dot(crossDir) / denom;
        double s = (diff.Cross(d1)).Dot(crossDir) / denom;

        // Calculate closest points on each line
        TVector3 point1 = P1 + t * d1;
        TVector3 point2 = P2 + s * d2;

        closestPoint = point2;
    }
    return closestPoint;
}

// Function to find the closest point on the line defined by d0 and pi to the point IP
TLorentzVector ImpactFromIP(const TLorentzVector& d0, const TLorentzVector& pi, const TLorentzVector& IP) {
    //pi is the direction of the track that corresponds to the d0
    double t = (IP.Vect() - d0.Vect()).Dot((pi.Vect()).Unit());

    // Compute the closest point
    TVector3 point = d0.Vect() + t * (pi.Vect()).Unit();

    TLorentzVector closestPoint;
    closestPoint.SetPxPyPzE(point.X(), point.Y(), point.Z(), 0.);
    TLorentzVector impactVector = closestPoint - IP;

    return impactVector;
}

//return parallel component of a vector v that lies in the plane defined by a and b
TVector3 ProjectOntoPlane(const TVector3& v, const TVector3& a, const TVector3& b) {
    // Compute normal to the plane
    TVector3 n = a.Cross(b);
    n = n.Unit(); 

    // Projection of v onto normal
    double v_dot_n = v.Dot(n);
    TVector3 v_perp = v_dot_n * n;
    TVector3 v_parallel = v - v_perp;

    return v_parallel;
}

Vec_i getIndex(Vec_rp in, Vec_rp reco, bool verbose=false) {
    Vec_i result;
    if(verbose) cout << "GET INDEX" << endl;
    for(auto & p: in) {
        if(verbose) cout << " TARGET " << p.energy << endl;
        for(int i = 0; i < reco.size(); ++i) {
            if(verbose) cout << "   PROBE " << reco[i].energy << endl;
            // match on energy, for charged particles can match on track index
            if(reco[i].energy == p.energy) {
                //cout << i << " " << reco[i].energy << " " <<  p.energy << " " << endl;
                result.push_back(i);
                if(verbose) cout << "   FOUND " << i << endl;
                break;
            }
        }
    }
    return result;
}

Vec_f particleResolution(Vec_rp in, Vec_i in_idx, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, int mode=0){
    Vec_f result;

    // avoid events that have the extra soft photon and screws up the MC/RECO collections
    if(reco.size() != recind.size()) return result;

    result.reserve(in.size());

    for(int i = 0; i < in.size(); ++i) {
        TLorentzVector reco_p4;
        reco_p4.SetXYZM(in[i].momentum.x, in[i].momentum.y, in[i].momentum.z, in[i].mass);
        int mc_index = mcind[recind[in_idx[i]]];
        if(mc_index >= 0 && mc_index < (int)mc.size()) {
            TLorentzVector mc_;
            mc_.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
            //cout << reco_p4.P() << " " << mc_.P()<< " "  << reco_p4.Theta() << " " << mc_.Theta() << " "  << reco_p4.Phi() << " " << mc_.Phi() << endl;
            if(mode == 0) result.emplace_back((reco_p4.P()-mc_.P())/mc_.P());
            else if(mode == 1) result.push_back(reco_p4.Theta()/mc_.Theta());
            else if(mode == 2) result.push_back(reco_p4.Phi()/mc_.Phi());
        }
    } 
    return result;
}

Vec_f dR_matching(Vec_rp in, Vec_i in_idx, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc){
    Vec_f result;

    // avoid events that have the extra soft photon and screws up the MC/RECO collections
    //if(reco.size() != recind.size()) return result;

    result.reserve(in.size());

    for(int i = 0; i < in.size(); ++i) {
        TLorentzVector reco_p4;
        reco_p4.SetXYZM(in[i].momentum.x, in[i].momentum.y, in[i].momentum.z, in[i].mass);
        int mc_index = mcind[recind[in_idx[i]]];
        if(mc_index >= 0 && mc_index < (int)mc.size() && mc.at(mc_index).PDG != 22){
            TLorentzVector mc_;
            mc_.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
            //cout << reco_p4.P() << " " << mc_.P()<< " "  << reco_p4.Theta() << " " << mc_.Theta() << " "  << reco_p4.Phi() << " " << mc_.Phi() << endl;
            result.emplace_back(reco_p4.DeltaR(mc_));
        }
        else{
            result.emplace_back(-1000.);
        }
    } 
    return result;
}

Vec_i Reco2MCpdg(Vec_rp in, Vec_i in_idx, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc){
    Vec_f result;

    result.reserve(in.size());
    for(int i = 0; i < in.size(); ++i) {
        int mc_index = mcind[recind[in_idx[i]]];
        if(mc_index >= 0 && mc_index < (int)mc.size()){
            result.emplace_back(mc.at(mc_index).PDG);
        }
        else{
            result.emplace_back(-1000.);
        }
    } 
    return result;
}

ROOT::VecOps::RVec<float> jet_reso(ROOT::VecOps::RVec<float> jet_px,ROOT::VecOps::RVec<float> jet_py,ROOT::VecOps::RVec<float> jet_pz,ROOT::VecOps::RVec<float> jet_mass,ROOT::VecOps::RVec<edm4hep::MCParticleData> mc){

    ROOT::VecOps::RVec<float> result;
    result.reserve(2);

    float total_DR; 
    float min_DR = 1000.;
    int mc2jet1_idx = -1;
    int mc2jet2_idx = -1;


    TLorentzVector jet1;
    TLorentzVector jet2;
    jet1.SetXYZM(jet_px[0], jet_py[0], jet_pz[0], jet_mass[0]);
    jet2.SetXYZM(jet_px[1], jet_py[1], jet_pz[1], jet_mass[1]);

    for(int i = 0; i < mc.size(); ++i){
        //std::cout << mc.at(i).parents_begin << std::endl; 
        for(int j = i+1; j < mc.size(); ++j){

            TLorentzVector mc_quark1;
            TLorentzVector mc_quark2;
            mc_quark1.SetXYZM(mc[i].momentum.x, mc[i].momentum.y, mc[i].momentum.z, mc[i].mass);
            mc_quark2.SetXYZM(mc[j].momentum.x, mc[j].momentum.y, mc[j].momentum.z, mc[j].mass);

            total_DR = jet1.DeltaR(mc_quark1) + jet2.DeltaR(mc_quark2);

            if(min_DR > total_DR){

                min_DR = total_DR;
                mc2jet1_idx = i;
                mc2jet2_idx = j;
            }

            total_DR = jet1.DeltaR(mc_quark2) + jet2.DeltaR(mc_quark1);

            if(min_DR > total_DR){

                min_DR = total_DR;
                mc2jet1_idx = j;
                mc2jet2_idx = i;
            }
        }
    }

    //std::cout << mc2jet1_idx << std::endl;
    //std::cout << mc2jet2_idx << std::endl;

    TLorentzVector quark2jet1;
    quark2jet1.SetXYZM(mc[mc2jet1_idx].momentum.x, mc[mc2jet1_idx].momentum.y, mc[mc2jet1_idx].momentum.z, mc[mc2jet1_idx].mass);
    float reso_1 = (jet1.P()-quark2jet1.P())/quark2jet1.P();
    //std::cout << reso_1 << std::endl;

    TLorentzVector quark2jet2;
    quark2jet1.SetXYZM(mc[mc2jet2_idx].momentum.x, mc[mc2jet2_idx].momentum.y, mc[mc2jet2_idx].momentum.z, mc[mc2jet2_idx].mass);
    float reso_2 = (jet2.P()-quark2jet2.P())/quark2jet2.P();
    //std::cout << reso_2 << std::endl;

    result.push_back(reso_1);
    result.push_back(reso_2);

    return result; 
}


ROOT::VecOps::RVec<float> reso_p_pdg(ROOT::VecOps::RVec<int> recind,
				    ROOT::VecOps::RVec<int> mcind,
				    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                    ROOT::VecOps::RVec<int> ind,
				    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    int pdg,
                    int parID,
                    float upper,
                    float lower) {

    ROOT::VecOps::RVec<float> result;
    result.reserve(reco.size());

    for (unsigned int i=0; i<reco.size();i++){
        int reco_idx = recind.at(i);
        int mc_idx = mcind.at(reco_idx);
        int mc_pdg = mc.at(mc_idx).PDG;

        if(std::fabs(mc_pdg) == pdg){
            
            int par_idx = mc.at(mc_idx).parents_begin;
            int index = ind.at(par_idx);
            int parPDG = mc.at(index).PDG;
            
            if(parPDG == parID){

                TLorentzVector mc_tlv;
                TLorentzVector reco_tlv;
                mc_tlv.SetXYZM(mc.at(mc_idx).momentum.x,mc.at(mc_idx).momentum.y,mc.at(mc_idx).momentum.z,mc.at(mc_idx).mass);
                float mc_p = mc_tlv.P();
                reco_tlv.SetXYZM(reco.at(i).momentum.x,reco.at(i).momentum.y,reco.at(i).momentum.z,reco.at(i).mass);
                float reco_p = reco_tlv.P();

                if(reco_p >= lower && reco_p < upper){
                    float reso = (reco_p - mc_p)/mc_p;
                    result.emplace_back(reso);
                }
            }
        }
    }
    return result;
}

ROOT::VecOps::RVec<TLorentzVector> smear_jet(ROOT::VecOps::RVec<TLorentzVector> jets, float FWHM_CMS, float FWHM_IDEA, float Dijet_M, float Dijet_p){
    ROOT::VecOps::RVec<TLorentzVector> p4;
    static std::random_device rd;
    static std::mt19937 gen(rd());

    for(unsigned int i = 0; i < jets.size(); i++){
        
        std::normal_distribution<> d(jets[i].P(), jets[i].P()*(sqrt(pow(FWHM_CMS/2.3548,2.)-pow(FWHM_IDEA/2.3548,2.)))/jets[i].M());
        float smeared_p = d(gen);

        float smeared_e = std::sqrt(smeared_p * smeared_p + jets[i].M() * jets[i].M());
        float smeared_x = smeared_p * std::sin(jets[i].Theta()) * std::cos(jets[i].Phi());
        float smeared_y = smeared_p * std::sin(jets[i].Theta()) * std::sin(jets[i].Phi());
        float smeared_z = smeared_p * std::cos(jets[i].Theta());

        
        TLorentzVector tlv;
        tlv.SetPxPyPzE(smeared_x, smeared_y, smeared_z, smeared_e);
        p4.push_back(tlv);
    }
    return p4;
}



ROOT::VecOps::RVec<float> check_matching(ROOT::VecOps::RVec<int> recind,
				    ROOT::VecOps::RVec<int> mcind,
				    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                    ROOT::VecOps::RVec<int> ind,
				    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    int pdg,
                    int parID,
                    float upper,
                    float lower) {

    ROOT::VecOps::RVec<float> result;
    result.reserve(reco.size());

    for (unsigned int i=0; i<reco.size();i++){
        int reco_idx = recind.at(i);
        int mc_idx = mcind.at(i);
        int mc_pdg = mc.at(mc_idx).PDG;

        if(std::fabs(mc_pdg) == pdg){
            
            int par_idx = mc.at(mc_idx).parents_begin;
            int index = ind.at(par_idx);
            int parPDG = mc.at(index).PDG;
            
            if(parPDG == parID){

                TLorentzVector mc_tlv;
                TLorentzVector reco_tlv;
                mc_tlv.SetXYZM(mc.at(mc_idx).momentum.x,mc.at(mc_idx).momentum.y,mc.at(mc_idx).momentum.z,mc.at(mc_idx).mass);
                float mc_p = mc_tlv.P();
                reco_tlv.SetXYZM(reco.at(reco_idx).momentum.x,reco.at(reco_idx).momentum.y,reco.at(reco_idx).momentum.z,reco.at(reco_idx).mass);
                float reco_p = reco_tlv.P();

                if(reco_p >= lower && reco_p < upper){
                    float dR = mc_tlv.DeltaR(reco_tlv);
                    result.emplace_back(dR);
                }
            }
        }
    }
    return result;
}

ROOT::VecOps::RVec<float> check_parents(ROOT::VecOps::RVec<int> recind,
				    ROOT::VecOps::RVec<int> mcind,
				    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                    ROOT::VecOps::RVec<int> ind,
				    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    int pdg) {

    ROOT::VecOps::RVec<float> result;
    result.reserve(reco.size());

    for (unsigned int i=0; i<recind.size();i++){
        int reco_idx = recind.at(i);
        int mc_idx = mcind.at(i);
        int mc_pdg = mc.at(mc_idx).PDG;

        if(std::fabs(mc_pdg) == pdg){
            
            int par_idx = mc.at(mc_idx).parents_begin;
            int index = ind.at(par_idx);
            int parPDG = mc.at(index).PDG;
            result.emplace_back(parPDG);
        }
    }
    return result;
}

ROOT::VecOps::RVec<float> smeared_p(
				    ROOT::VecOps::RVec<int> mcind,
				    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                    ROOT::VecOps::RVec<int> ind,
				    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    int pdg,
                    int parID,
                    double sf
                ) {

    ROOT::VecOps::RVec<float> result;

    for (unsigned int i=0; i<mcind.size();i++) {
        int mc_idx = mcind.at(i);
        int mc_pdg = mc.at(mc_idx).PDG;

        if(std::fabs(mc_pdg) == pdg){
            
            int par_idx = mc.at(mc_idx).parents_begin;
            int index = ind.at(par_idx);
            int parPDG = mc.at(index).PDG;
            
            if(parPDG == parID){

                TLorentzVector mc_tlv;
                TLorentzVector reco_tlv;
                mc_tlv.SetXYZM(mc.at(mc_idx).momentum.x,mc.at(mc_idx).momentum.y,mc.at(mc_idx).momentum.z,mc.at(mc_idx).mass);
                float mc_p = mc_tlv.P();
                reco_tlv.SetXYZM(reco.at(i).momentum.x,reco.at(i).momentum.y,reco.at(i).momentum.z,reco.at(i).mass);
                float reco_p = reco_tlv.P();

                float smeared_p = mc_p + sf * (reco_p - mc_p);
                if(smeared_p >=0){
                    result.emplace_back(10);
                }
                else{
                    result.emplace_back(-10);
                }
            }
        }
    }
    return result;
}

ROOT::VecOps::RVec<int> missing_matches_pdg(
				    ROOT::VecOps::RVec<int> mcind,
				    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
				    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    int pdg
                ) {

    ROOT::VecOps::RVec<int> result;

    for (unsigned int i=0; i<reco.size();i++) {
        int mc_idx = mcind.at(i);
        int mc_pdg = mc.at(mc_idx).PDG;

        if(std::fabs(mc_pdg) == pdg){
            if(mc_idx >= 0 and mc_idx < mc.size()){
                result.emplace_back(1);
            }
            else{
                result.emplace_back(0);
            }
        }
    }
    return result;
}

ROOT::VecOps::RVec<float> reso_p_jets(
    ROOT::VecOps::RVec<float> gen_p, 
    ROOT::VecOps::RVec<float> reco_p,
    ROOT::VecOps::RVec<float> gen_charge, 
    ROOT::VecOps::RVec<float> reco_charge, 
    int upper, 
    int lower) {

    ROOT::VecOps::RVec<float> result; 

    for (size_t i = 0; i < reco_p.size(); ++i) {

        if(reco_p[i] >= lower && reco_p[i] < upper){

            for (size_t j = 0; j < gen_p.size(); ++j){

                if(reco_charge.at(i) == gen_charge.at(j)){
                    
                    float reso = (reco_p[i] - gen_p[j])/gen_p[j];
                    result.emplace_back(reso);
                }
            }
        }
    }
    return result; //result.size() will give the number of pairs/rows passing the selection
}


//begin of minimizer function following ILC paper https://arxiv.org/pdf/1804.01241 and reference from d. Jeans https://arxiv.org/pdf/1507.01700
//returns neutrinos in lab frame
class NuKinFunctor : public ROOT::Minuit2::FCNBase {
public:
    NuKinFunctor(const TLorentzVector& Recoil,
                 const TLorentzVector& TauP_p_p4,
                 const TLorentzVector& TauM_p_p4,
                 const TLorentzVector& TauP_k_p4,
                 const TLorentzVector& TauM_k_p4,
                 const TLorentzVector& TauP_d_p4,
                 const TLorentzVector& TauM_d_p4,
                 const TLorentzVector& IP)
        : Recoil_(Recoil), TauP_p_p4_(TauP_p_p4), TauM_p_p4_(TauM_p_p4),
          TauP_k_p4_(TauP_k_p4), TauM_k_p4_(TauM_k_p4),
          TauP_d_p4_(TauP_d_p4), TauM_d_p4_(TauM_d_p4), IP_(IP) {}

    // Override the virtual operator() method (const std::vector<double>&)
    double operator()(const std::vector<double>& params) const override {
        // Wrap the vector to a raw array (pointer) and call the original operator()
        return operator()(params.data());
    }

    // Override the operator() method that accepts a const double* (already implemented)
    double operator()(const double* params) const {
        double param1 = params[0];  // phi angle for TauP
        double param2 = params[1];  // phi angle for TauM

        TLorentzVector TauP_h_p4 = TauP_p_p4_ + TauP_k_p4_;
        TLorentzVector TauM_h_p4 = TauM_p_p4_ + TauM_k_p4_;

        TLorentzVector TauP_d_p4_IP, TauM_d_p4_IP;

        //d0 in files from the origin but we have a different IP so we account for that
        //the method considers the tracks coming from the IP
        //the tau calculation is with respect to the IP so i need to find the d0 there, using the d0 from the origin to find the track and then the point closest to it passing for IP
        TauP_d_p4_IP = ImpactFromIP(TauP_d_p4_, TauP_p_p4_, IP_);
        TauM_d_p4_IP = ImpactFromIP(TauM_d_p4_, TauM_p_p4_, IP_);

        TVector3 TauP_h_par = ProjectOntoPlane(TauP_h_p4.Vect(), TauP_p_p4_.Vect(),  TauP_d_p4_IP.Vect());
        TVector3 TauM_h_par = ProjectOntoPlane(TauM_h_p4.Vect(), TauM_p_p4_.Vect(),  TauM_d_p4_IP.Vect());

        TVector3 TauP_fcap = (TauP_h_par.Cross((TauP_d_p4_IP.Vect()).Cross(TauP_h_par))).Unit();
        TVector3 TauM_fcap = (TauM_h_par.Cross((TauM_d_p4_IP.Vect()).Cross(TauM_h_par))).Unit();

        TVector3 TauP_k_par = ProjectOntoPlane(TauP_k_p4_.Vect(), TauP_p_p4_.Vect(),  TauP_d_p4_IP.Vect());
        TVector3 TauM_k_par = ProjectOntoPlane(TauM_k_p4_.Vect(), TauM_p_p4_.Vect(),  TauM_d_p4_IP.Vect());

        TVector3 TauP_k_perp = (TauP_k_p4_.Vect() - TauP_k_par);
        TVector3 TauM_k_perp = (TauM_k_p4_.Vect() - TauM_k_par);

        // Perpendicular components are straightforward
        TVector3 TauP_q_perp = - TauP_k_perp;
        TVector3 TauM_q_perp = - TauM_k_perp;

        // Use the parameters to assign the neutrino parallel component
        TVector3 TauP_q_par = (cos(param1) * TauP_h_par.Unit() + sin(param1) * TauP_fcap);
        TVector3 TauM_q_par = (cos(param2) * TauM_h_par.Unit() + sin(param2) * TauM_fcap);

        // Solve tau mass balance to find the magnitude of the neutrinos
        double AP = m_tau * m_tau - TauP_h_p4.M() * TauP_h_p4.M() - 2 * ((TauP_h_p4.Vect()).Dot(TauP_k_perp));
        double BP = 2 * ((TauP_q_par).Dot(TauP_h_p4.Vect() - TauP_k_perp));
        double CP = 2 * TauP_h_p4.E();

        double aP = BP * BP - CP * CP;
        double bP = 2 * AP * BP;
        double cP = AP * AP - CP * CP * (TauP_k_perp.Mag2());

        double dP = bP * bP - 4 * aP * cP;

        double AM = m_tau * m_tau - TauM_h_p4.M() * TauM_h_p4.M() - 2 * ((TauM_h_p4.Vect()).Dot(TauM_k_perp));
        double BM = 2 * ((TauM_q_par).Dot(TauM_h_p4.Vect() - TauM_k_perp));
        double CM = 2 * TauM_h_p4.E();

        double aM = BM * BM - CM * CM;
        double bM = 2 * AM * BM;
        double cM = AM * AM - CM * CM * (TauM_k_perp.Mag2());

        double dM = bM * bM - 4 * aM * cM;

        TVector3 TauP_nu1_par, TauP_nu2_par, TauM_nu1_par, TauM_nu2_par;
        double QP1=0, QP2=0, QM1=0, QM2=0;

        // the idea is that if the discriminant is negative we assume it's zero so the function is smooth and the minimization will tell if it's correct or not (hopefully not but the minimum will not be skipped if nearby)
        if (dP >= 0 && dM >= 0) { 
            QP1 = (-bP + sqrt(dP)) / (2 * aP);
            QP2 = (-bP - sqrt(dP)) / (2 * aP);
            QM1 = (-bM + sqrt(dM)) / (2 * aM);
            QM2 = (-bM - sqrt(dM)) / (2 * aM);

        }
        else if (dP >= 0 && dM < 0) { 
            QP1 = (-bP + sqrt(dP)) / (2 * aP);
            QP2 = (-bP - sqrt(dP)) / (2 * aP);
            QM1 = (-bM) / (2 * aM);
            QM2 = (-bM) / (2 * aM);
        }
        else if (dP < 0 && dM >= 0) { 
            QP1 = (-bP) / (2 * aP);
            QP2 = (-bP) / (2 * aP);
            QM1 = (-bM + sqrt(dM)) / (2 * aM);
            QM2 = (-bM - sqrt(dM)) / (2 * aM);
        }
        else { 
            QP1 = (-bP) / (2 * aP);
            QP2 = (-bP) / (2 * aP);
            QM1 = (-bM) / (2 * aM);
            QM2 = (-bM) / (2 * aM);
        }
        TauP_nu1_par = QP1 * TauP_q_par;
        TauP_nu2_par = QP2 * TauP_q_par;
        TauM_nu1_par = QM1 * TauM_q_par;
        TauM_nu2_par = QM2 * TauM_q_par;

        TVector3 TauP_nu1_p3 = TauP_nu1_par + TauP_q_perp;
        TVector3 TauP_nu2_p3 = TauP_nu2_par + TauP_q_perp;
        TVector3 TauM_nu1_p3 = TauM_nu1_par + TauM_q_perp;
        TVector3 TauM_nu2_p3 = TauM_nu2_par + TauM_q_perp;

        TLorentzVector TauP_nu1_p4, TauP_nu2_p4, TauM_nu1_p4, TauM_nu2_p4;
    
        TauP_nu1_p4.SetPxPyPzE(TauP_nu1_p3.Px(), TauP_nu1_p3.Py(), TauP_nu1_p3.Pz(), sqrt(pow(TauP_nu1_p3.Px(), 2) + pow(TauP_nu1_p3.Py(), 2) + pow(TauP_nu1_p3.Pz(), 2)));
        TauP_nu2_p4.SetPxPyPzE(TauP_nu2_p3.Px(), TauP_nu2_p3.Py(), TauP_nu2_p3.Pz(), sqrt(pow(TauP_nu2_p3.Px(), 2) + pow(TauP_nu2_p3.Py(), 2) + pow(TauP_nu2_p3.Pz(), 2)));
        TauM_nu1_p4.SetPxPyPzE(TauM_nu1_p3.Px(), TauM_nu1_p3.Py(), TauM_nu1_p3.Pz(), sqrt(pow(TauM_nu1_p3.Px(), 2) + pow(TauM_nu1_p3.Py(), 2) + pow(TauM_nu1_p3.Pz(), 2)));
        TauM_nu2_p4.SetPxPyPzE(TauM_nu2_p3.Px(), TauM_nu2_p3.Py(), TauM_nu2_p3.Pz(), sqrt(pow(TauM_nu2_p3.Px(), 2) + pow(TauM_nu2_p3.Py(), 2) + pow(TauM_nu2_p3.Pz(), 2)));

        TLorentzVector TauP1_p4 = TauP_nu1_p4 + TauP_h_p4;
        TLorentzVector TauP2_p4 = TauP_nu2_p4 + TauP_h_p4;
        TLorentzVector TauM1_p4 = TauM_nu1_p4 + TauM_h_p4;
        TLorentzVector TauM2_p4 = TauM_nu2_p4 + TauM_h_p4;

        // final vectors to store based on decay lenght arguments
        TLorentzVector TauP_p4, TauM_p4, TauP_nu_p4, TauM_nu_p4;

        // compute the decay lenght for each tau, also from the IP which is where the right decay lenght of the tau comes from
        // first of all, build the pion tracks with the d0 end point and then from that use the pion momentum to get the direction (defined as a TVector3 in both cases)
        TVector3 TauP_p_dir = (TauP_p_p4_.Vect()).Unit();
        TVector3 TauP_p_pt = TauP_d_p4_.Vect();

        // now the tau track in a similar way but knowing that the beginning point is the IP, repeat for all the combinations (2 per sign)
        TVector3 TauP1_dir = (TauP1_p4.Vect()).Unit();
        TVector3 TauP2_dir = (TauP2_p4.Vect()).Unit();
    
        // get the intesection of the tau and pion tracks as a TVector3 with respect to the origin so to ge the decay lenght it needs to be traslated to the IP
        TVector3 intP_1 = findIntersection(TauP_p_pt, TauP_p_dir, IP_.Vect(), TauP1_dir);
        TVector3 intP_2 = findIntersection(TauP_p_pt, TauP_p_dir, IP_.Vect(), TauP2_dir);

        TVector3 IP_intP_1 = intP_1 - IP_.Vect();
        TVector3 IP_intP_2 = intP_2 - IP_.Vect();

        double TauP1_L = IP_intP_1.Mag();
        double TauP2_L = IP_intP_2.Mag();
        
        // then figure out if the intersection is on the same direction of the tau track or opposite i.e. the IP is between the track direction and the interaction point which makes them incompatible
        double dotP_1 = TauP1_dir.Dot((IP_intP_1).Unit());
        double dotP_2 = TauP2_dir.Dot((IP_intP_2).Unit());

        double LambdaP_1 = 0, LambdaP_2 = 0;

        // cosine 0 means the lines are truly parallel but then the decay lenght is technically positive in the direction where there is some separation,
        // so now lambda will be exactly zero only in the case of negative or zero decay lenght
        // the problem of null decay lenght is that the lambda goes to 1 which would be favoured over better values
        if (dotP_1>=0 && TauP1_L>0) LambdaP_1 = std::exp(- TauP1_L / ( TauP1_p4.Beta() * TauP1_p4.Gamma() * 87.0 * 1e-3)); //mum to mm for consistency with the d0
        if (dotP_2>=0 && TauP2_L>0) LambdaP_2 = std::exp(- TauP2_L / ( TauP2_p4.Beta() * TauP2_p4.Gamma() * 87.0 * 1e-3));

        // repeat for the negative
        TVector3 TauM_p_dir = (TauM_p_p4_.Vect()).Unit();
        TVector3 TauM_p_pt = TauM_d_p4_.Vect();

        TVector3 TauM1_dir = (TauM1_p4.Vect()).Unit();
        TVector3 TauM2_dir = (TauM2_p4.Vect()).Unit();
    
        TVector3 intM_1 = findIntersection(TauM_p_pt, TauM_p_dir, IP_.Vect(), TauM1_dir);
        TVector3 intM_2 = findIntersection(TauM_p_pt, TauM_p_dir, IP_.Vect(), TauM2_dir);

        TVector3 IP_intM_1 = intM_1 - IP_.Vect();
        TVector3 IP_intM_2 = intM_2 - IP_.Vect();

        double TauM1_L = IP_intM_1.Mag();
        double TauM2_L = IP_intM_2.Mag();

        double dotM_1 = TauM1_dir.Dot((IP_intM_1).Unit());
        double dotM_2 = TauM2_dir.Dot((IP_intM_2).Unit());

        double LambdaM_1 = 0, LambdaM_2 = 0;

        if (dotM_1>=0 && TauM1_L>0) LambdaM_1 = std::exp(- TauM1_L / ( TauM1_p4.Beta() * TauM1_p4.Gamma() * 87.0 * 1e-3));
        if (dotM_2>=0 && TauM2_L>0) LambdaM_2 = std::exp(- TauM2_L / ( TauM2_p4.Beta() * TauM2_p4.Gamma() * 87.0 * 1e-3));

        // use the lambda on the decay lenght as a weight: if it's still zero then the solution is not kept at all, otherwise it's a blend and the kinematics are the same anyway by construction
        // so now there is no need to check the lambdas after the minimization as it's taken care of here and if the solution doesn't make sense it's on the minimization
        double weightP1=0, weightP2=0, weightM1=0, weightM2=0;
        // avoid division by zero in case both lambdas are zero 
        if (LambdaP_1>0 || LambdaP_2>0) {
            weightP1 = LambdaP_1 / (LambdaP_1 + LambdaP_2);
            weightP2 = LambdaP_2 / (LambdaP_1 + LambdaP_2);
        }
        if (LambdaM_1>0 || LambdaM_2>0) {
            weightM1 = LambdaM_1 / (LambdaM_1 + LambdaM_2);
            weightM2 = LambdaM_2 / (LambdaM_1 + LambdaM_2);
        }
        //apply the weight on the nu and not the tau directly so the taus are only the visible part in case of bad solutions for the nu
        TauP_nu_p4 = weightP1 * TauP_nu1_p4 + weightP2 * TauP_nu2_p4;
        TauM_nu_p4 = weightM1 * TauM_nu1_p4 + weightM2 * TauM_nu2_p4;

        TauP_p4 = TauP_nu_p4 + TauP_h_p4;
        TauM_p4 = TauM_nu_p4 + TauM_h_p4;

        // Minimize the missing momentum and return the best neutrino pair
        double Pt_miss = (Recoil_ + (TauP_p4 + TauM_p4)).Pt();

        // Use copy constructor instead of assignment
        best_NuP_nu_ = TLorentzVector(TauP_nu_p4);
        best_NuM_nu_ = TLorentzVector(TauM_nu_p4);

        return Pt_miss;

    }

    double Up() const override {
        return 0.0;  
    }

    // Getter methods
    TLorentzVector getBestNuP_Nu() const { return best_NuP_nu_; }
    TLorentzVector getBestNuM_Nu() const { return best_NuM_nu_; }

private:
    TLorentzVector Recoil_;
    TLorentzVector TauP_p_p4_;
    TLorentzVector TauM_p_p4_;
    TLorentzVector TauP_k_p4_;
    TLorentzVector TauM_k_p4_;
    TLorentzVector TauP_d_p4_;
    TLorentzVector TauM_d_p4_;
    TLorentzVector IP_;
    mutable double DL_M, DL_P, LambdaM_1_, LambdaM_2_, LambdaP_1_, LambdaP_2_;
    mutable double cosP_1, cosP_2, cosM_1, cosM_2;
    mutable TLorentzVector best_NuP_nu_, best_NuM_nu_;
};

ROOT::VecOps::RVec<TLorentzVector> build_nu_kin_ILC(const TLorentzVector& Recoil,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Charged_p4,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Neutral_p4,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Impact_p4,
                                                 const TLorentzVector& IP) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector TauP_p_p4, TauM_p_p4, TauP_k_p4, TauM_k_p4, TauP_d_p4, TauM_d_p4;
    // order the particles by charge: first the positive then negative to keep consistent later on
    // assumes they have opposite charges
    TauP_p_p4 = Charged_p4[0];
    TauM_p_p4 = Charged_p4[1];
    TauP_k_p4 = Neutral_p4[0];
    TauM_k_p4 = Neutral_p4[1];
    TauP_d_p4 = Impact_p4[0];
    TauM_d_p4 = Impact_p4[1];
    
    ROOT::Minuit2::Minuit2Minimizer minimizer(ROOT::Minuit2::kMigrad);
    NuKinFunctor functor(Recoil, TauP_p_p4, TauM_p_p4, TauP_k_p4, TauM_k_p4, TauP_d_p4, TauM_d_p4, IP);
    ROOT::Math::Functor fcn(functor, 2);
    minimizer.SetFunction(fcn);
    //minimizer.SetStrategy(2);
    minimizer.SetPrintLevel(-1);
    
    // Define the two ranges for phi angles
    std::vector<std::pair<double, double>> phi_ranges = {
        {-3.141592653589793/2, 0}, {0, 3.141592653589793/2}
    };

    // Track the best result
    double best_result = std::numeric_limits<double>::max();
    TLorentzVector best_nuP, best_nuM;
    double best_cP_1, best_cP_2, best_cM_1, best_cM_2;
    double best_LambdaP, best_LambdaM;
    double bestLP, bestLM;

    // Loop over all 4 combinations of (phi_plus, phi_minus)
    for (const auto& phi_plus_range : phi_ranges) {
        for (const auto& phi_minus_range : phi_ranges) {
            
            // Set phi_plus with the current range
            minimizer.SetVariable(0, "phi_plus", (phi_plus_range.first + phi_plus_range.second) / 2, 0.0001);
            minimizer.SetVariableLimits(0, phi_plus_range.first, phi_plus_range.second);

            // Set phi_minus with the current range
            minimizer.SetVariable(1, "phi_minus", (phi_minus_range.first + phi_minus_range.second) / 2, 0.0001);
            minimizer.SetVariableLimits(1, phi_minus_range.first, phi_minus_range.second);

            // Run the minimizer
            bool success = minimizer.Minimize();

            if (success) {

                double current_result = minimizer.MinValue();
                const double* best_params = minimizer.X();
                functor.operator()(best_params); // This updates the vectors internally

                if (current_result < best_result) {
                    best_result = current_result;
                    best_nuP = functor.getBestNuP_Nu();
                    best_nuM = functor.getBestNuM_Nu(); 

                }
            }
        }
    }
    // Retrieve the best neutrino momenta that resulted in minimal missing energy
    result.push_back(best_nuP);  
    result.push_back(best_nuM);

    TLorentzVector chi;
    chi.SetPxPyPzE(best_result, 0, 0, 0);
    result.push_back(chi);

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
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
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
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
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
           if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt()){
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
