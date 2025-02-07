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

TLorentzVector build_p4_single(float px, float py, float pz, float e) {
    TLorentzVector tlv;
    tlv.SetPxPyPzE(px, py, pz, e);
    return tlv;
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

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> get_chargedleading_fromjet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // similar to the findTauInJet function but I only want the leading charged particle in the jet

    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);

        // Find Lead (This needs to change to first sort the jcs by p or pt, it is very messy right now)

        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        // First loop just to find the lead (not very efficient). 
        for (const auto& jc : jcs) {

            // Anything else lets: find the highest pt one, charged particle as lead only
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
            }
        }
        // save the leading particle, one per jet, if only neutral particles are present thenn it return a null particle
        partMod.momentum.x = lead.Px();
        partMod.momentum.y = lead.Py();
        partMod.momentum.z = lead.Pz();
        partMod.mass = lead.M();
        partMod.energy= lead.E();
        partMod.charge = chargeLead; 
        out.push_back(partMod);
        
    }
    return out;

}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> get_neutral_fromjet(const ROOT::VecOps::RVec<FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents>& jets) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;
    // Loop over jets
    for (const auto& jet : jets) {
        TLorentzVector totalNeutralMomentum; 
        edm4hep::ReconstructedParticleData combinedNeutral;

        // Loop over jet constituents to find neutral particles
        for (const auto& jc : jet) {
            if (jc.charge == 0) { 
                TLorentzVector neutralMomentum;
                neutralMomentum.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                totalNeutralMomentum += neutralMomentum;
            }
        }

        combinedNeutral.momentum.x = totalNeutralMomentum.Px();
        combinedNeutral.momentum.y = totalNeutralMomentum.Py();
        combinedNeutral.momentum.z = totalNeutralMomentum.Pz();
        combinedNeutral.mass = totalNeutralMomentum.M();
        combinedNeutral.energy = totalNeutralMomentum.E();
        combinedNeutral.charge = 0.; 
        out.push_back(combinedNeutral);
    }

    return out;
}

//begin of minimalizer function 1
// returns taus in lab frame

const double m_tau = 1.777;  // GeV/c^2

// Chi-squared function to be minimized
class Chi2Function : public ROOT::Minuit2::FCNBase {
public:
    Chi2Function(const TLorentzVector& Pi_plus, const TLorentzVector& Pi_minus, 
                 const TLorentzVector& Recoil, const TLorentzVector& EMiss)
        : Pi_plus_(Pi_plus), Pi_minus_(Pi_minus), Recoil_(Recoil), EMiss_(EMiss) {}

    double operator()(const std::vector<double>& params) const {
        // Extract parameters (neutrino momenta for each tau)
        double px_plus = params[0], py_plus = params[1], pz_plus = params[2];
        double px_minus = params[3], py_minus = params[4], pz_minus = params[5];

        // Calculate the 4-vectors for the neutrinos
        TLorentzVector Nu_plus(px_plus, py_plus, pz_plus, std::sqrt(px_plus*px_plus + py_plus*py_plus + pz_plus*pz_plus));
        TLorentzVector Nu_minus(px_minus, py_minus, pz_minus, std::sqrt(px_minus*px_minus + py_minus*py_minus + pz_minus*pz_minus));

        // Reconstruct the taus
        TLorentzVector Tau_plus = Nu_plus + Pi_plus_;
        TLorentzVector Tau_minus = Nu_minus + Pi_minus_;

        // Tau mass constraints
        double massP = Tau_plus.M();
        double massM = Tau_minus.M();

        // Chi-squared term for tau masses
        double chi2_mass = ((massP - m_tau) * (massP - m_tau) / 0.01) + ((massM - m_tau) * (massM - m_tau) / 0.01);  // 10 MeV resolution for tau mass

        // Compute the missing transverse energy (EMiss) terms
        double emiss_x_calc = (Nu_plus + Nu_minus).Px();
        double emiss_y_calc = (Nu_plus + Nu_minus).Py();
        double emiss_z_calc = (Nu_plus + Nu_minus).Pz();
        double emiss_e_calc = (Nu_plus + Nu_minus).E();

        double chi2_met = ((emiss_x_calc - EMiss_.Px()) * (emiss_x_calc - EMiss_.Px()) / 0.01) + 
                          ((emiss_y_calc - EMiss_.Py()) * (emiss_y_calc - EMiss_.Py()) / 0.01) + 
                          ((emiss_z_calc - EMiss_.Pz()) * (emiss_z_calc - EMiss_.Pz()) / 0.01) +
                          ((emiss_e_calc - EMiss_.E()) * (emiss_e_calc - EMiss_.E()) / 0.01);  // 10 MeV resolution for missing energy

        // now for the recoil, might be too constrained at this point??
        double recoil_x_calc = (Tau_plus + Tau_minus).Px();
        double recoil_y_calc = (Tau_plus + Tau_minus).Py();
        double recoil_z_calc = (Tau_plus + Tau_minus).Pz();
        double recoil_e_calc = (Tau_plus + Tau_minus).E();

        double chi2_recoil = ((recoil_x_calc - Recoil_.Px()) * (recoil_x_calc - Recoil_.Px()) / 0.01) + 
                          ((recoil_y_calc - Recoil_.Py()) * (recoil_y_calc - Recoil_.Py()) / 0.01) + 
                          ((recoil_z_calc - Recoil_.Pz()) * (recoil_z_calc - Recoil_.Pz()) / 0.01) +
                          ((recoil_e_calc - Recoil_.E()) * (recoil_e_calc - Recoil_.E()) / 0.01);

        // Total chi-squared
        return chi2_mass + chi2_met;
    }

    // Minuit2 interface to call the chi2 function
    virtual double Up() const { return 0.0; }  // Returns the unweighted function
    virtual double operator()(const double *xx) const { return operator()(std::vector<double>(xx, xx + 6)); }

private:
    TLorentzVector Pi_plus_;
    TLorentzVector Pi_minus_;
    TLorentzVector Recoil_;
    TLorentzVector EMiss_;
};

// Wrapper for Minuit2
static Chi2Function* chi2FunctionInstance = nullptr;

void Chi2Wrapper(Int_t& npar, Double_t* grad, Double_t& fval, Double_t* par, Int_t flag) {
    if (chi2FunctionInstance) {
        std::vector<double> params(par, par + 6);
        fval = chi2FunctionInstance->operator()(params);
    }
}

ROOT::VecOps::RVec<TLorentzVector> build_nu_kin(const TLorentzVector& Recoil, const TLorentzVector& EMiss,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Tau_vis,
                                                 const ROOT::VecOps::RVec<float>& charge) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector Pi_plus, Pi_minus;
    
    // Order the taus by charge: first the positive then negative to keep consistent later on
    if (charge[0] == 1) {
        Pi_plus = Tau_vis[0];
        Pi_minus = Tau_vis[1];
    } else {
        Pi_plus = Tau_vis[1];
        Pi_minus = Tau_vis[0];
    }

    // Initialize Minuit2
    ROOT::Minuit2::Minuit2Minimizer minimizer;
    
    // Define the chi2 function for minimization
    Chi2Function chi2Function(Pi_plus, Pi_minus, Recoil, EMiss);
    chi2FunctionInstance = &chi2Function;
    ROOT::Math::Functor fcn(chi2Function, 6);
    minimizer.SetFunction(fcn);

    // Set initial parameter values and step sizes for the neutrino momenta
    minimizer.SetVariable(0, "px_plus", 0.0, 0.01);  
    minimizer.SetVariable(1, "py_plus", 0.0, 0.01);  
    minimizer.SetVariable(2, "pz_plus", 0.0, 0.01);  
    minimizer.SetVariable(3, "px_minus", 0.0, 0.01); 
    minimizer.SetVariable(4, "py_minus", 0.0, 0.01); 
    minimizer.SetVariable(5, "pz_minus", 0.0, 0.01); 

    // Perform the minimization
    minimizer.Minimize();

    // Extract uncertainties (sigma) from the first fit
    const double* sigma = minimizer.Errors();

    // Re-run the minimization with adaptive step sizes
    for (int i = 0; i < 6; ++i) {
        minimizer.SetVariableStepSize(i, sigma[i]);  
    }

    // Second minimization pass
    minimizer.Minimize();  

    // Retrieve the fitted parameters
    const double* params = minimizer.X();

    // Reconstruct the neutrino and tau 4-vectors from the fitted parameters
    TLorentzVector Nu_plus_fit(params[0], params[1], params[2], 
                                std::sqrt(params[0]*params[0] + params[1]*params[1] + params[2]*params[2]));
    TLorentzVector Nu_minus_fit(params[3], params[4], params[5], 
                                 std::sqrt(params[3]*params[3] + params[4]*params[4] + params[5]*params[5]));
    
    TLorentzVector Tau_plus_fit = Nu_plus_fit + Pi_plus;
    TLorentzVector Tau_minus_fit = Nu_minus_fit + Pi_minus;

    result.push_back(Tau_plus_fit);
    result.push_back(Tau_minus_fit);
    
    return result;
}

//end

//---------------------------------------------------------------------

//begin of minmalizer function 2
//returns neutrinos in lab frame
//following ILC paper https://arxiv.org/pdf/1804.01241 and reference from d. Jeans https://arxiv.org/pdf/1507.01700

class NuKinFunctor : public ROOT::Minuit2::FCNBase {
public:
    NuKinFunctor(const TLorentzVector& Recoil,
                 const TLorentzVector& TauP_p_p4,
                 const TLorentzVector& TauM_p_p4,
                 const TLorentzVector& TauP_k_p4,
                 const TLorentzVector& TauM_k_p4,
                 const TLorentzVector& TauP_d_p4,
                 const TLorentzVector& TauM_d_p4)
        : Recoil_(Recoil), TauP_p_p4_(TauP_p_p4), TauM_p_p4_(TauM_p_p4),
          TauP_k_p4_(TauP_k_p4), TauM_k_p4_(TauM_k_p4),
          TauP_d_p4_(TauP_d_p4), TauM_d_p4_(TauM_d_p4) {}

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

        TVector3 TauP_h_par = ((TauP_h_p4.Vect().Dot(TauP_p_p4_.Vect())) / ((TauP_p_p4_.Vect()).Mag2())) * TauP_p_p4_.Vect();
        TVector3 TauM_h_par = ((TauM_h_p4.Vect().Dot(TauM_p_p4_.Vect())) / ((TauM_p_p4_.Vect()).Mag2())) * TauM_p_p4_.Vect();

        TVector3 TauP_fcap = (TauP_h_par.Cross((TauP_d_p4_.Vect()).Cross(TauP_h_par))).Unit();
        TVector3 TauM_fcap = (TauM_h_par.Cross((TauM_d_p4_.Vect()).Cross(TauM_h_par))).Unit();

        TVector3 TauP_k_par = ((TauP_k_p4_.Vect().Dot(TauP_p_p4_.Vect())) / ((TauP_p_p4_.Vect()).Mag2())) * TauP_p_p4_.Vect();
        TVector3 TauM_k_par = ((TauM_k_p4_.Vect().Dot(TauM_p_p4_.Vect())) / ((TauM_p_p4_.Vect()).Mag2())) * TauM_p_p4_.Vect();

        TVector3 TauP_k_perp = (TauP_k_p4_.Vect() - TauP_k_par);
        TVector3 TauM_k_perp = (TauM_k_p4_.Vect() - TauM_k_par);

        // Perpendicular components are straightforward
        TVector3 TauP_q_perp = -TauP_k_perp;
        TVector3 TauM_q_perp = -TauM_k_perp;

        // Use the parameters to assign the neutrino parallel component
        TVector3 TauP_q_par_cap = (cos(param1) * TauP_h_par.Unit() + sin(param1) * TauP_fcap);
        TVector3 TauM_q_par_cap = (cos(param2) * TauM_h_par.Unit() + sin(param2) * TauM_fcap);

        // Solve tau mass balance to find the magnitude of the neutrinos
        double AP = m_tau * m_tau - TauP_h_p4.M() * TauP_h_p4.M() - 2 * ((TauP_h_p4.Vect()).Dot(TauP_k_perp));
        double BP = 2 * (TauP_q_par_cap.Dot(TauP_h_p4.Vect() - TauP_k_perp));
        double CP = 2 * TauP_h_p4.E();

        double aP = BP * BP - CP * CP;
        double bP = 2 * AP * BP;
        double cP = AP * AP - CP * CP * (TauP_k_perp.Mag2());

        double dP = bP * bP - 4 * aP * cP;

        double AM = m_tau * m_tau - TauM_h_p4.M() * TauM_h_p4.M() - 2 * ((TauM_h_p4.Vect()).Dot(TauM_k_perp));
        double BM = 2 * (TauM_q_par_cap.Dot(TauM_h_p4.Vect() - TauM_k_perp));
        double CM = 2 * TauM_h_p4.E();

        double aM = BM * BM - CM * CM;
        double bM = 2 * AM * BM;
        double cM = AM * AM - CM * CM * (TauM_k_perp.Mag2());

        double dM = bM * bM - 4 * aM * cM;

        if (dP < 0 || dM < 0) {
            // Large penalty to avoid this region
            return 1e6;
        }

        // Calculate neutrino momenta for both solutions
        double QP1 = (-bP + sqrt(dP)) / (2 * aP);
        double QP2 = (-bP - sqrt(dP)) / (2 * aP);
        double QM1 = (-bM + sqrt(dM)) / (2 * aM);
        double QM2 = (-bM - sqrt(dM)) / (2 * aM);

        TLorentzVector TauP_nu1_p4, TauP_nu2_p4, TauM_nu1_p4, TauM_nu2_p4;
        TauP_nu1_p4.SetPxPyPzE(QP1 * TauP_q_par_cap.Px(), QP1 * TauP_q_par_cap.Py(), QP1 * TauP_q_par_cap.Pz(), sqrt(pow(QP1 * TauP_q_par_cap.Px(), 2) + pow(QP1 * TauP_q_par_cap.Py(), 2) + pow(QP1 * TauP_q_par_cap.Pz(), 2)));
        TauP_nu2_p4.SetPxPyPzE(QP2 * TauP_q_par_cap.Px(), QP2 * TauP_q_par_cap.Py(), QP2 * TauP_q_par_cap.Pz(), sqrt(pow(QP2 * TauP_q_par_cap.Px(), 2) + pow(QP2 * TauP_q_par_cap.Py(), 2) + pow(QP2 * TauP_q_par_cap.Pz(), 2)));
        TauM_nu1_p4.SetPxPyPzE(QM1 * TauM_q_par_cap.Px(), QM1 * TauM_q_par_cap.Py(), QM1 * TauM_q_par_cap.Pz(), sqrt(pow(QM1 * TauM_q_par_cap.Px(), 2) + pow(QM1 * TauM_q_par_cap.Py(), 2) + pow(QM1 * TauM_q_par_cap.Pz(), 2)));
        TauM_nu2_p4.SetPxPyPzE(QM2 * TauM_q_par_cap.Px(), QM2 * TauM_q_par_cap.Py(), QM2 * TauM_q_par_cap.Pz(), sqrt(pow(QM2 * TauM_q_par_cap.Px(), 2) + pow(QM2 * TauM_q_par_cap.Py(), 2) + pow(QM2 * TauM_q_par_cap.Pz(), 2)));

        // Minimize the missing energy and select the best neutrino pair
        std::vector<std::tuple<double, TLorentzVector, TLorentzVector>> neutrino_pairs = {
            { (Recoil_ - (TauP_h_p4 + TauM_h_p4 + TauP_nu1_p4 + TauM_nu1_p4)).E(), TauP_nu1_p4, TauM_nu1_p4 },
            { (Recoil_ - (TauP_h_p4 + TauM_h_p4 + TauP_nu2_p4 + TauM_nu2_p4)).E(), TauP_nu2_p4, TauM_nu2_p4 },
            { (Recoil_ - (TauP_h_p4 + TauM_h_p4 + TauP_nu1_p4 + TauM_nu2_p4)).E(), TauP_nu1_p4, TauM_nu2_p4 },
            { (Recoil_ - (TauP_h_p4 + TauM_h_p4 + TauP_nu2_p4 + TauM_nu1_p4)).E(), TauP_nu2_p4, TauM_nu1_p4 }
        };

        auto best_pair = *std::min_element(neutrino_pairs.begin(), neutrino_pairs.end(),
            [](const auto& a, const auto& b) { return std::get<0>(a) < std::get<0>(b); });

        // Use copy constructor instead of assignment
        best_NuP_nu_ = TLorentzVector(std::get<1>(best_pair));
        best_NuM_nu_ = TLorentzVector(std::get<2>(best_pair));

        return std::get<0>(best_pair);
    }

    double Up() const override {
        return 0.0;  // Standard choice for Minuit2 minimization uncertainty
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
    mutable TLorentzVector best_NuP_nu_, best_NuM_nu_;
};

ROOT::VecOps::RVec<TLorentzVector> build_nu_kin_ILC(const TLorentzVector& Recoil, const TLorentzVector& EMiss,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Charged_p4,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Neutral_p4,
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Impact_p4,
                                                 const ROOT::VecOps::RVec<float>& charge) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector TauP_p_p4, TauM_p_p4, TauP_k_p4, TauM_k_p4, TauP_d_p4, TauM_d_p4;
    // order the particles by charge: first the positive then negative to keep consistent later on
    // assumes they have opposite charges
    if (charge[0]==1) {
        TauP_p_p4 = Charged_p4[0];
        TauM_p_p4 = Charged_p4[1];
        TauP_k_p4 = Neutral_p4[0];
        TauM_k_p4 = Neutral_p4[1];
        TauP_d_p4 = Impact_p4[0];
        TauM_d_p4 = Impact_p4[1];
    }
    else {
        TauP_p_p4 = Charged_p4[1];
        TauM_p_p4 = Charged_p4[0];
        TauP_k_p4 = Neutral_p4[1];
        TauM_k_p4 = Neutral_p4[0];
        TauP_d_p4 = Impact_p4[1];
        TauM_d_p4 = Impact_p4[0];
    }

    ROOT::Minuit2::Minuit2Minimizer minimizer;
    NuKinFunctor functor(Recoil, TauP_p_p4, TauM_p_p4, TauP_p_p4, TauM_p_p4, TauP_p_p4, TauM_p_p4);
    ROOT::Math::Functor fcn(functor, 2);
    minimizer.SetFunction(fcn);
    
    // Define parameters (only phi angles)
    // Set initial parameter values and step sizes for the neutrino momenta
    minimizer.SetVariable(0, "phi_plus", 0.0, 0.0005);
    minimizer.SetVariable(1, "phi_minus", 0.0, 0.0005);
    minimizer.Minimize();
    
    const double* params = minimizer.X();

    // Retrieve the best neutrino momenta that resulted in minimal missing energy
    result.push_back(functor.getBestNuP_Nu());  
    result.push_back(functor.getBestNuM_Nu());

    return result;
}


//end

ROOT::VecOps::RVec<TLorentzVector> build_tau_p4 (TLorentzVector Recoil, TLorentzVector EMiss, ROOT::VecOps::RVec<TLorentzVector> Tau_vis, ROOT::VecOps::RVec<float> charge){
    
    //following Belle reconstruction https://arxiv.org/pdf/1310.8503
    // first of all, build the visible taus from pi and pi0 with either jet tagger or the explciit reconstruction
    // both should be built from the same jets so keeping the order as it is reuslts in the two taus which will be identified later by the charge of the pi
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector temp1;
    TLorentzVector temp2;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H_temp;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H;

    double E_tau = Recoil.E()/2; //energy of the single taus in the higgs rest frame

    for (size_t i = 0; i < Tau_vis.size(); ++i) {

        // boost the visible taus to the recoil frame / "true" higgs rest frame
        TLorentzVector boostedTau = Tau_vis[i]; 
        boostedTau.Boost(-Recoil.BoostVector()); 
        Tau_vis_H_temp.push_back(boostedTau);
    }

    // order the taus by charge: first the positive then negative to keep consistent later on
    // assumes they have opposite charges
    if (charge[0]==1) {
        Tau_vis_H.push_back(Tau_vis_H_temp[0]);
        Tau_vis_H.push_back(Tau_vis_H_temp[1]);
    }
    else {
        Tau_vis_H.push_back(Tau_vis_H_temp[1]);
        Tau_vis_H.push_back(Tau_vis_H_temp[0]);
    }

    // determine the angle between the visible and neutrino in the higgs frame
    double cos0 = (2 * E_tau * Tau_vis_H[0].E() - m_tau * m_tau - Tau_vis_H[0].M() * Tau_vis_H[0].M()) / (2 * Tau_vis_H[0].P() * sqrt(E_tau * E_tau - m_tau * m_tau));
    double cos1 = (2 * E_tau * Tau_vis_H[1].E() - m_tau * m_tau - Tau_vis_H[1].M() * Tau_vis_H[1].M()) / (2 * Tau_vis_H[1].P() * sqrt(E_tau * E_tau - m_tau * m_tau));

    // solve the system of equations 
    double a = Tau_vis_H[0].Px();
    double b = Tau_vis_H[0].Py();
    double c = Tau_vis_H[0].Pz();
    double d = Tau_vis_H[0].P() * cos0;

    double e = Tau_vis_H[1].Px();
    double f = Tau_vis_H[1].Py();
    double g = Tau_vis_H[1].Pz();
    double h = - Tau_vis_H[1].P() * cos1;

    double p1 = e*b - a*f;
    double p2 = e*c - a*g;
    double q1 = e*d - a*h;

    if (p1 == 0) {
        std::cerr << "Error: Invalid values encountered while solving the quadratic equation." << std::endl;
        result.push_back(temp1);
        result.push_back(temp2);
        return result;
    }

    double r1 = (p1 * d - b * q1) / p1;
    double r2 = (b * p2 - p1 * c) / p1;

    double A = (r2*r2) / (a*a) + (p2*p2) / (p1*p1) +1;
    double B = 2*((r1 * r2) / (a*a) - (q1 * p2) / (p1*p1));
    double C = (r1*r1) / (a*a) + (q1*q1) / (p1*p1) -1;

    double discriminant = B * B - 4 * A * C;
    if (discriminant < 0) {
        result.push_back(temp1);
        result.push_back(temp2);
        return result;
    }
    //else if (discriminant >= -10 && discriminant<0){
    //    discriminant = 0;
    //}

    double z1 = (-B + sqrt(discriminant)) / (2*A);
    double z2 = (-B - sqrt(discriminant)) / (2*A);

    double y1 = (q1 - p2*z1) / p1;
    double y2 = (q1 - p2*z2) / p1;

    double x1 = (d - b*y1 - c*z1) / a;
    double x2 = (d - b*y2 - c*z2) / a;

    // now i need to build the TLV for the tau adding back the recoil mass and tau mass
    double P_tau = sqrt(E_tau * E_tau - m_tau * m_tau);
    TLorentzVector plus1;
    plus1.SetPxPyPzE(P_tau * x1, P_tau * y1, P_tau * z1, E_tau);
    TLorentzVector plus2;
    plus2.SetPxPyPzE(P_tau * x2, P_tau * y2, P_tau * z2, E_tau);
    TLorentzVector min1;
    min1.SetPxPyPzE(-P_tau * x1, -P_tau * y1, -P_tau * z1, E_tau);
    TLorentzVector min2;
    min2.SetPxPyPzE(-P_tau * x2, -P_tau * y2, -P_tau * z2, E_tau);

    if (discriminant > 0) {
        // boost back the solutions to figure out the best one against the recoil frame
        plus1.Boost( Recoil.BoostVector());
        plus2.Boost( Recoil.BoostVector());
        min1.Boost( Recoil.BoostVector());
        min2.Boost( Recoil.BoostVector());

        TLorentzVector sol1 = plus1 + min1; 
        TLorentzVector sol2 = plus2 + min2; 

        // Energy conservation check
        double energy_diff1 = (Recoil - sol1).E();
        double energy_diff2 = (Recoil - sol2).E();

        // Compute momentum balance for both solutions
        double momentum_diff1 = (Recoil - sol1).P(); 
        double momentum_diff2 = (Recoil - sol2).P();

        TLorentzVector nuplus1, nuplus2, numin1, numin2;

        if (charge[0]==1){
            nuplus1 = plus1 - Tau_vis[0];
            nuplus2 = plus2 - Tau_vis[0];
            numin1 = min1 - Tau_vis[1];
            numin2 = min2 - Tau_vis[1];
        }
        else {
            nuplus1 = plus1 - Tau_vis[1];
            nuplus2 = plus2 - Tau_vis[1];
            numin1 = min1 - Tau_vis[0];
            numin2 = min2 - Tau_vis[0];
        }

        // Calculate deltaR between the neutrinos and tau
        float D1 = deltaR(plus1.Phi(), nuplus1.Phi(), plus1.Eta(), nuplus1.Eta());
        float D2 = deltaR(plus2.Phi(), nuplus2.Phi(), plus2.Eta(), nuplus2.Eta());

        // Now apply the criteria to choose the best solution:
        // 1. First, choose the solution with the smallest energy difference
        // 2. If the energy differences are similar, choose the one with the smallest momentum discrepancy
        // 3. If both are similar, use the deltaR minimization as a tie-breaker.

        bool choose_solution1 = false;
        bool choose_solution2 = false;

        if (energy_diff1 < energy_diff2) {
            //std::cout<<"energy first "<<energy_diff1<<std::endl;
            choose_solution1 = true;
        } else if (energy_diff1 > energy_diff2) {
            //std::cout<<"energy second "<<energy_diff2<<std::endl;
            choose_solution2 = true;
        } else { 
            if (momentum_diff1 < momentum_diff2) {
                //std::cout<<"momentum first "<<momentum_diff1<<std::endl;
                choose_solution1 = true;
            } else if (momentum_diff1 > momentum_diff2) {
                //std::cout<<"momentum second "<<momentum_diff2<<std::endl;
                choose_solution2 = true;
            } else { 
                if (D1 < D2) {
                    //std::cout<<"DR first "<<D1<<std::endl;
                    choose_solution1 = true;
                } else {
                    //std::cout<<"DR second "<<D2<<std::endl;
                    choose_solution2 = true;
                }
            }
        }

        if (choose_solution1) {
            result.push_back(plus1);
            result.push_back(min1);
        } else if (choose_solution2) {
            result.push_back(plus2);
            result.push_back(min2);
        }
    }
    else {
        result.push_back(plus1);
        result.push_back(min1);
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
