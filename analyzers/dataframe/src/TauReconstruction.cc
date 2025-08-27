#include "FCCAnalyses/TauReconstruction.h"

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "Minuit2/FCNBase.h"
#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/Track.h"
#include "edm4hep/TrackerHitData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/Cluster.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/CalorimeterHitData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "FCCAnalyses/JetClusteringUtils.h"
#include "edm4hep/ParticleIDData.h"
#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"


namespace FCCAnalyses { namespace TauReconstruction {

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request){

    // Identify taus. This algorithm requires to first build a jet (for example clustering_ee_kt(2, 4, 1, 0)).
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it with specific decay modes.
    // The taus will have charge +-1, mass below 3 GeV, no leptons.
    
    // "request" parameter, should be >0 only if needing specific consituents of the tau: 
        // 0 for full visible tau, 
        // 1 for charged pion (the one with same charge as the tau if from the rho resonance (3 prong)), 
        // 2 for opposite charged pion in rho resonance (3 prong) or sum of neutral particles (1 prong), 
        // 3 for sum of charged pions, 
        // 4 or else for neutral system only (only different from 1 and 2 in case of 3 prong).

    // The outpiut is a ReconstructedParticle type, all the variables are then accessible through the usual methods.
    // Every jet will return one entry so the vector can then be filtered by the tau ID for specific tau modes or quark jets.

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    for (int i = 0; i < jets.size(); ++i) {

        // Full visible tau (0 in request)
        TLorentzVector sum_tau; 
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauVis;
        // Neutral consituents (2 or 4 in request)
        TLorentzVector neutral;
        // Charged constituents (1 or 3 in request)
        TLorentzVector charged;
        // Individual ones
        ROOT::VecOps::RVec<TLorentzVector> charged_vec;
        // Their charge
        ROOT::VecOps::RVec<int> charges_vec;
        // Their track index to access later for track related variables 
        ROOT::VecOps::RVec<int> track_vec;
        
        float tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0;

        // Leading particle
        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;
        int track=0;

        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);

        // First loop through the consituents to find the leading pion. 
        for (const auto& jc : jcs) {

            // No electrons or muons in hadronic tau decays
            if (fabs(jc.mass -  0.105658) < 1.e-03) {
                tauID=-13;
                continue; 
                }
            if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                tauID=-11;
                continue;
            }

            // Now find the leading charged particle
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
                track = jc.tracks_begin; // This saves the index in the track collection related to the leading pion. It is useful in some analysis.
            }
        }

        charges_vec.push_back(chargeLead);
        charged_vec.push_back(lead);
        track_vec.push_back(track);

        if (lead.Pt()<2) {
            tauID=-1;
            Tau.type = tauID;
            out.push_back(Tau); 
            continue;
        } // Too low pt, the particle will be empty but still will show up as an entry 

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            out.push_back(Tau); 
            continue;
        }// Leptons in jet, the particle will be empty but still will show up as an entry 

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;
        charged+=lead;

        // Now loop to build the tau adding candidates to the lead only if they satisfy some conditions: distance, charge, etc 
        for (const auto& jc : jcs) {

            TLorentzVector tlv;  
            tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

            if (tlv==lead) continue;

            // Distance (in terms of Theta)
            double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

            if (tlv.Pt()<1 || dTheta>0.20) continue;

            if (jc.charge>0) {
                count_piP++; 
                charged+=tlv;
                charges_vec.push_back(jc.charge);
                charged_vec.push_back(tlv);
                track_vec.push_back(jc.tracks_begin);
                }  

            else if (jc.charge<0) {
                count_piM++;  
                charged+=tlv;
                charges_vec.push_back(jc.charge);
                charged_vec.push_back(tlv);
                track_vec.push_back(jc.tracks_begin);
                }

            else  {
                count_pho++;
                neutral+=tlv;
                }

            sum_tau += tlv; 

        }

        // Lets build the ID : count the charged pions and the neutrals. 
        // Considering the decays of the tau, we want candidates with one or three charged candidates (one or three prongs).
        // The ID is then increased depending on the number of photons/neutral hadrons found.

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

            if (request==0) {
                Tau.momentum.x=sum_tau.Px();
                Tau.momentum.y=sum_tau.Py();
                Tau.momentum.z=sum_tau.Pz();
                Tau.mass= sum_tau.M();
                Tau.energy= sum_tau.E();
                Tau.charge= (count_piP-count_piM);
                Tau.type = tauID;
                Tau.tracks_begin = track;
            }
            else if (request==1 || request==2) {
                // Get the pion from the rho resonance for the request==2
                if ((count_piP+count_piM)==3) {
                    TLorentzVector second;
                    int second_track;
                    TLorentzVector third;
                    double minMassDifference = -1e6;
                    for (size_t i = 0; i < charges_vec.size(); ++i) {
                        for (size_t j = i + 1; j < charges_vec.size(); ++j) {
                            if (charges_vec[i] + charges_vec[j] == 0) {  // opposite charges
                                double invMass = (charged_vec[i] + charged_vec[j]).M();
                                double massDifference = std::abs(invMass - 0.775); //rho 0 in gev
                                
                                if (minMassDifference == -1e6) {
                                    minMassDifference = massDifference;
                                    // Save the pion with same charge as the tau as the charged one and the other as the neutral
                                    if (charges_vec[i]==1){
                                        second = charged_vec[i];
                                        third = charged_vec[j];
                                        second_track = track_vec[i];   
                                    }
                                    else {
                                        second = charged_vec[j];
                                        third = charged_vec[i];
                                        second_track = track_vec[j];
                                    }
                                } 
                                else if (massDifference < minMassDifference) {
                                    // Update if we find a smaller mass difference
                                    minMassDifference = massDifference;
                                    if (charges_vec[i]==1){
                                        second = charged_vec[i];
                                        third = charged_vec[j];
                                        second_track = track_vec[i];   
                                    }
                                    else {
                                        second = charged_vec[j];
                                        third = charged_vec[i];
                                        second_track = track_vec[j];
                                    }
                                }
                            }
                        }
                    }

                    if (request==1) {
                        Tau.momentum.x=second.Px();
                        Tau.momentum.y=second.Py();
                        Tau.momentum.z=second.Pz();
                        Tau.mass= second.M();
                        Tau.energy= second.E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = second_track;
                    }
                    else {
                        Tau.momentum.x=third.Px();
                        Tau.momentum.y=third.Py();
                        Tau.momentum.z=third.Pz();
                        Tau.mass= third.M();
                        Tau.energy= third.E();
                        Tau.charge= (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
                        Tau.type = tauID;
                        Tau.tracks_begin = second_track; // and same track index as the charged
                    }
                }
                else {
                    if (request==1) {
                        Tau.momentum.x=lead.Px();
                        Tau.momentum.y=lead.Py();
                        Tau.momentum.z=lead.Pz();
                        Tau.mass= lead.M();
                        Tau.energy= lead.E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = track;
                    }
                    else {
                        Tau.momentum.x=(sum_tau-lead).Px();
                        Tau.momentum.y=(sum_tau-lead).Py();
                        Tau.momentum.z=(sum_tau-lead).Pz();
                        Tau.mass= (sum_tau-lead).M();
                        Tau.energy= (sum_tau-lead).E();
                        Tau.charge= (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
                        Tau.type = tauID;
                        Tau.tracks_begin = track; // and same track index as the charged
                    }
                }
            }
            else if (request==3) {
                Tau.momentum.x=charged.Px();
                Tau.momentum.y=charged.Py();
                Tau.momentum.z=charged.Pz();
                Tau.mass= charged.M();
                Tau.energy= charged.E();
                Tau.charge= (count_piP-count_piM);
                Tau.type = tauID;
                Tau.tracks_begin = track;
            }
            else {
                Tau.momentum.x=neutral.Px();
                Tau.momentum.y=neutral.Py();
                Tau.momentum.z=neutral.Pz();
                Tau.mass= neutral.M();
                Tau.energy= neutral.E();
                Tau.charge= (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
                Tau.type = tauID;
                Tau.tracks_begin = track; // and same track index as the charged
            }

            // Save taus (or its components) with mass below 3 GeV
            if (sum_tau.M()<3)  {
                    out.push_back(Tau);
            }
            else {
                // Reset the particle if it's not a tau but keep a different ID to identify the cause
                Tau.momentum.x = 0;
                Tau.momentum.y = 0;
                Tau.momentum.z = 0;
                Tau.mass = 0;
                Tau.energy= 0;
                Tau.charge = 0; 
                Tau.type = -2;
                out.push_back(Tau);
            }
        }
        else {
            Tau.type = -3;            
            out.push_back(Tau);
        }
    }
    return out;

}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_pi0 (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request){

    // Identify taus. This algorithm requires to first build a jet (for example clustering_ee_kt(2, 4, 1, 0)).
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it with specific decay modes.
    // The taus will have charge +-1, mass below 3 GeV, no leptons.
    
    // "request" parameter, should be >0 only if needing specific consituents of the tau: 
        // 0 for full visible tau, 
        // 1 for charged pion (the one with same charge as the tau if from the rho resonance (3 prong)), 
        // 2 for opposite charged pion in rho resonance (3 prong) or sum of neutral particles (1 prong), 
        // 3 for sum of charged pions, 
        // 4 or else for neutral system only (only different from 1 and 2 in case of 3 prong).

    // The outpiut is a ReconstructedParticle type, all the variables are then accessible through the usual methods.
    // Every jet will return one entry so the vector can then be filtered by the tau ID for specific tau modes or quark jets.

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; 
        TLorentzVector neutral;
        TLorentzVector charged;
        ROOT::VecOps::RVec<TLorentzVector> charged_vec;
        ROOT::VecOps::RVec<int> charges_vec;
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauVis;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        ROOT::VecOps::RVec<int> track_vec;
        ROOT::VecOps::RVec<TLorentzVector> photons_vec;
        float tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0, count_pi0=0;
        int track=0;

        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        for (const auto& jc : jcs) {

            if (fabs(jc.mass -  0.105658) < 1.e-03) {
                tauID=-13;
                continue; 
                }
            if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                tauID=-11;
                continue; 
            }

            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
                track = jc.tracks_begin;
            }
        }

        charges_vec.push_back(chargeLead);
        charged_vec.push_back(lead);
        track_vec.push_back(track);

        if (lead.Pt()<2) {
            tauID=-1;
            Tau.type = tauID;
            out.push_back(Tau);
            continue;
        }

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            out.push_back(Tau); 
            continue;
        }

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} 

        sum_tau+=lead;
        charged+=lead;

        for (const auto& jc : jcs) {

            TLorentzVector tlv;  
            tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

            if (tlv==lead) continue;

            double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

            if (tlv.Pt()<1 || dTheta>0.20) continue;

            if (jc.charge>0) {
                count_piP++; 
                charged+=tlv;
                charges_vec.push_back(1);
                charged_vec.push_back(tlv);
                track_vec.push_back(jc.tracks_begin);
                }  

            else if (jc.charge<0) {
                count_piM++;  
                charged+=tlv;
                charges_vec.push_back(-1);
                charged_vec.push_back(tlv);
                track_vec.push_back(jc.tracks_begin);
                }

            else  {
                count_pho++;
                neutral+=tlv;
                }

            sum_tau += tlv;  

        }

        // pi0 reconstruction from pairs of photons, one photon can only be associated with one pi0
        std::vector<bool> used(photons_vec.size(), false);
        for (size_t i = 0; i < photons_vec.size(); ++i) {
            if (used[i]) continue;
            for (size_t j = i + 1; j < photons_vec.size(); ++j) {
                if (used[j]) continue;
                TLorentzVector pair = photons_vec[i] + photons_vec[j];
                double mass = pair.M();
                // 50 MeV mass tollerance
                if (std::abs(mass - 0.135) < 0.05) {
                    count_pi0++;
                    used[i] = true;
                    used[j] = true;
                    break; 
                }
            }
        }

        // Lets build the ID : count the charged pions and the neutrals. 
        // Considering the decays of the tau, we want candidates with one or three charged candidates (one or three prongs).
        // The ID is then increased depending on the number of photons/neutral hadrons found.
        // New values consider if a pi0 was found.

        if (tauID!=-13 && tauID!=-11 && abs(count_piP-count_piM)==1 && ( (count_piP+count_piM)==1 || (count_piP+count_piM)==3) ){    

            if( (count_piP+count_piM)==1 && count_pho==0) tauID=0;
            if( (count_piP+count_piM)==1 && count_pho==1) tauID=1;

            if( (count_piP+count_piM)==1 && count_pho==2 && count_pi0==0) tauID=2;
            if( (count_piP+count_piM)==1 && count_pho==2 && count_pi0==1) tauID=3;

            if( (count_piP+count_piM)==1 && count_pho==3 && count_pi0==0) tauID=4;
            if( (count_piP+count_piM)==1 && count_pho==3 && count_pi0==1) tauID=5;

            if( (count_piP+count_piM)==1 && count_pho==4 && count_pi0==0) tauID=6;
            if( (count_piP+count_piM)==1 && count_pho==4 && count_pi0==1) tauID=7;
            if( (count_piP+count_piM)==1 && count_pho==4 && count_pi0==2) tauID=8;

            if( (count_piP+count_piM)==1 && count_pho==5 && count_pi0==0) tauID=9;
            if( (count_piP+count_piM)==1 && count_pho==5 && count_pi0==1) tauID=10;
            if( (count_piP+count_piM)==1 && count_pho==5 && count_pi0==2) tauID=11;

            if( (count_piP+count_piM)==1 && count_pho>5 && count_pi0==0) tauID=12;
            if( (count_piP+count_piM)==1 && count_pho>5 && count_pi0==1) tauID=13;
            if( (count_piP+count_piM)==1 && count_pho>5 && count_pi0==2) tauID=14;
            if( (count_piP+count_piM)==1 && count_pho>5 && count_pi0>2) tauID=15;

            if( (count_piP+count_piM)==3 && count_pho==0) tauID=20;
            if( (count_piP+count_piM)==3 && count_pho==1) tauID=21;

            if( (count_piP+count_piM)==3 && count_pho==2 && count_pi0==0) tauID=22;
            if( (count_piP+count_piM)==3 && count_pho==2 && count_pi0==1) tauID=23;

            if( (count_piP+count_piM)==3 && count_pho==3 && count_pi0==0) tauID=24;
            if( (count_piP+count_piM)==3 && count_pho==3 && count_pi0==1) tauID=25;

            if( (count_piP+count_piM)==3 && count_pho==4 && count_pi0==0) tauID=26;
            if( (count_piP+count_piM)==3 && count_pho==4 && count_pi0==1) tauID=27;
            if( (count_piP+count_piM)==3 && count_pho==4 && count_pi0==2) tauID=28;

            if( (count_piP+count_piM)==3 && count_pho==5 && count_pi0==0) tauID=29;
            if( (count_piP+count_piM)==3 && count_pho==5 && count_pi0==1) tauID=30;
            if( (count_piP+count_piM)==3 && count_pho==5 && count_pi0==2) tauID=31;

            if( (count_piP+count_piM)==3 && count_pho>5 && count_pi0==0) tauID=32;
            if( (count_piP+count_piM)==3 && count_pho>5 && count_pi0==1) tauID=33;
            if( (count_piP+count_piM)==3 && count_pho>5 && count_pi0==2) tauID=34;
            if( (count_piP+count_piM)==3 && count_pho>5 && count_pi0>2) tauID=35;

            TauVis.momentum.x=sum_tau.Px();
            TauVis.momentum.y=sum_tau.Py();
            TauVis.momentum.z=sum_tau.Pz();
            TauVis.mass= sum_tau.M();
            TauVis.energy= sum_tau.E();
            TauVis.charge= (count_piP-count_piM);
            TauVis.type = tauID;
            TauVis.tracks_begin = 0;

            if (request==0) {
                Tau.momentum.x=sum_tau.Px();
                Tau.momentum.y=sum_tau.Py();
                Tau.momentum.z=sum_tau.Pz();
                Tau.mass= sum_tau.M();
                Tau.energy= sum_tau.E();
                Tau.charge= (count_piP-count_piM);
                Tau.type = tauID;
                Tau.tracks_begin = track;
            }
            else if (request==1 || request==2) {
                if ((count_piP+count_piM)==3) {
                    TLorentzVector second;
                    int second_track;
                    TLorentzVector third;
                    double minMassDifference = -1e6;
                    for (size_t i = 0; i < charges_vec.size(); ++i) {
                        for (size_t j = i + 1; j < charges_vec.size(); ++j) {
                            if (charges_vec[i] + charges_vec[j] == 0) {  
                                double invMass = (charged_vec[i] + charged_vec[j]).M();
                                double massDifference = std::abs(invMass - 0.775);
                                
                                if (minMassDifference == -1e6) {
                                    minMassDifference = massDifference;

                                    if (charges_vec[i]==1){
                                        second = charged_vec[i];
                                        third = charged_vec[j];
                                        second_track = track_vec[i];   
                                    }
                                    else {
                                        second = charged_vec[j];
                                        third = charged_vec[i];
                                        second_track = track_vec[j];
                                    }
                                } 
                                else if (massDifference < minMassDifference) {

                                    minMassDifference = massDifference;
                                    if (charges_vec[i]==1){
                                        second = charged_vec[i];
                                        third = charged_vec[j];
                                        second_track = track_vec[i];   
                                    }
                                    else {
                                        second = charged_vec[j];
                                        third = charged_vec[i];
                                        second_track = track_vec[j];
                                    }
                                }
                            }
                        }
                    }

                    if (request==1) {
                        Tau.momentum.x=second.Px();
                        Tau.momentum.y=second.Py();
                        Tau.momentum.z=second.Pz();
                        Tau.mass= second.M();
                        Tau.energy= second.E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = second_track;
                    }
                    else {
                        Tau.momentum.x=third.Px();
                        Tau.momentum.y=third.Py();
                        Tau.momentum.z=third.Pz();
                        Tau.mass= third.M();
                        Tau.energy= third.E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = second_track;
                    }
                }
                else {
                    if (request==1) {
                        Tau.momentum.x=lead.Px();
                        Tau.momentum.y=lead.Py();
                        Tau.momentum.z=lead.Pz();
                        Tau.mass= lead.M();
                        Tau.energy= lead.E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = track;
                    }
                    else {
                        Tau.momentum.x=(sum_tau-lead).Px();
                        Tau.momentum.y=(sum_tau-lead).Py();
                        Tau.momentum.z=(sum_tau-lead).Pz();
                        Tau.mass= (sum_tau-lead).M();
                        Tau.energy= (sum_tau-lead).E();
                        Tau.charge= (count_piP-count_piM);
                        Tau.type = tauID;
                        Tau.tracks_begin = track;
                    }
                }
            }
            else if (request==3) {
                Tau.momentum.x=charged.Px();
                Tau.momentum.y=charged.Py();
                Tau.momentum.z=charged.Pz();
                Tau.mass= charged.M();
                Tau.energy= charged.E();
                Tau.charge= (count_piP-count_piM);
                Tau.type = tauID;
                Tau.tracks_begin = track;
            }
            else {
                Tau.momentum.x=neutral.Px();
                Tau.momentum.y=neutral.Py();
                Tau.momentum.z=neutral.Pz();
                Tau.mass= neutral.M();
                Tau.energy= neutral.E();
                Tau.charge= (count_piP-count_piM);
                Tau.type = tauID;
                Tau.tracks_begin = track;
            }

            if (tauID!=-1 && TauVis.mass<3)  {
                    out.push_back(Tau);
            }
            else {
                Tau.momentum.x = 0;
                Tau.momentum.y = 0;
                Tau.momentum.z = 0;
                Tau.mass = 0;
                Tau.energy= 0;
                Tau.charge = 0; 
                tauID = -2;
                Tau.type = tauID;
                out.push_back(Tau);
            }
        }
        else {
            tauID=-3;
            Tau.type = tauID;            
            out.push_back(Tau);
        }
    }
    return out;

}

const double m_tau = 1.777;  // GeV/c^2

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

        double phi = Track[i].Phi() + 3.141592653589793/2;
        x2 = D0[i] * std::cos(phi);
        y2 = D0[i] * std::sin(phi);

        TLorentzVector perp_vector(x2, y2, Z0[i], 0.);
        impact.push_back(perp_vector);
    }

    return impact;
}

// Find the intersection between two tracks defined by one point and one vector (both TVector3)
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

// Function to find the closest point on the line defined by d0 and direction of the track (track momentum) to the point IP
TLorentzVector ImpactFromIP(const TLorentzVector& d0, const TLorentzVector& pi, const TLorentzVector& IP) {
    double t = (IP.Vect() - d0.Vect()).Dot((pi.Vect()).Unit());

    TVector3 point = d0.Vect() + t * (pi.Vect()).Unit();

    TLorentzVector closestPoint;
    closestPoint.SetPxPyPzE(point.X(), point.Y(), point.Z(), 0.);
    TLorentzVector impactVector = closestPoint - IP;

    return impactVector;
}

// Return parallel component of a vector v that lies in the plane defined by a and b
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

// Begin of minimizer function to reconstruct the full tau momenta in di-tau events following reference https://arxiv.org/pdf/1507.01700
// Returns tau neutrinos in lab frame, only for hadronic decays
// Needs the charged daughters of the tau to be separated from the neutral particles in two vectors
// Recoil vector can either be the recoiling system or the center of mass
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

    double operator()(const std::vector<double>& params) const override {
        return operator()(params.data());
    }

    double operator()(const double* params) const {
        double param1 = params[0];  // phi angle for TauP
        double param2 = params[1];  // phi angle for TauM

        TLorentzVector TauP_h_p4 = TauP_p_p4_ + TauP_k_p4_;
        TLorentzVector TauM_h_p4 = TauM_p_p4_ + TauM_k_p4_;

        TLorentzVector TauP_d_p4_IP, TauM_d_p4_IP;

        // The method considers the tracks coming from the IP, 
        // The d0/z0 from edm4hep is not perpendicular to the track from the origin or from the IP so we use it as a reference point for the track position
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

        // If the discriminant is negative we assume it's zero so the function is smooth and the minimization will tell if it's correct or not without missing the minimum if near by
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
    
        // Full neutrino vectors, two solutions per tau
        TauP_nu1_p4.SetPxPyPzE(TauP_nu1_p3.Px(), TauP_nu1_p3.Py(), TauP_nu1_p3.Pz(), sqrt(pow(TauP_nu1_p3.Px(), 2) + pow(TauP_nu1_p3.Py(), 2) + pow(TauP_nu1_p3.Pz(), 2)));
        TauP_nu2_p4.SetPxPyPzE(TauP_nu2_p3.Px(), TauP_nu2_p3.Py(), TauP_nu2_p3.Pz(), sqrt(pow(TauP_nu2_p3.Px(), 2) + pow(TauP_nu2_p3.Py(), 2) + pow(TauP_nu2_p3.Pz(), 2)));
        TauM_nu1_p4.SetPxPyPzE(TauM_nu1_p3.Px(), TauM_nu1_p3.Py(), TauM_nu1_p3.Pz(), sqrt(pow(TauM_nu1_p3.Px(), 2) + pow(TauM_nu1_p3.Py(), 2) + pow(TauM_nu1_p3.Pz(), 2)));
        TauM_nu2_p4.SetPxPyPzE(TauM_nu2_p3.Px(), TauM_nu2_p3.Py(), TauM_nu2_p3.Pz(), sqrt(pow(TauM_nu2_p3.Px(), 2) + pow(TauM_nu2_p3.Py(), 2) + pow(TauM_nu2_p3.Pz(), 2)));

        TLorentzVector TauP1_p4 = TauP_nu1_p4 + TauP_h_p4;
        TLorentzVector TauP2_p4 = TauP_nu2_p4 + TauP_h_p4;
        TLorentzVector TauM1_p4 = TauM_nu1_p4 + TauM_h_p4;
        TLorentzVector TauM2_p4 = TauM_nu2_p4 + TauM_h_p4;

        // Final vectors to store based on decay lenght to resolve the two-fold ambiguity
        TLorentzVector TauP_p4, TauM_p4, TauP_nu_p4, TauM_nu_p4;

        // Compute the decay lenght for each tau from the IP
        // First of all, build the pion tracks with the d0 end point and then from that use the pion momentum to get the direction (defined as a TVector3 in both cases)
        TVector3 TauP_p_dir = (TauP_p_p4_.Vect()).Unit();
        TVector3 TauP_p_pt = TauP_d_p4_.Vect();

        // Now the tau track in a similar way but knowing that the beginning point is the IP, repeat for all the combinations (2 per sign)
        TVector3 TauP1_dir = (TauP1_p4.Vect()).Unit();
        TVector3 TauP2_dir = (TauP2_p4.Vect()).Unit();
    
        // The intesection of the tau and pion tracks is with respect to the origin so to get the decay lenght it needs to be traslated to the IP
        TVector3 intP_1 = findIntersection(TauP_p_pt, TauP_p_dir, IP_.Vect(), TauP1_dir);
        TVector3 intP_2 = findIntersection(TauP_p_pt, TauP_p_dir, IP_.Vect(), TauP2_dir);

        TVector3 IP_intP_1 = intP_1 - IP_.Vect();
        TVector3 IP_intP_2 = intP_2 - IP_.Vect();

        double TauP1_L = IP_intP_1.Mag();
        double TauP2_L = IP_intP_2.Mag();
        
        // Then figure out if the intersection is on the same direction of the tau track or opposite i.e. the IP is between the track direction and the interaction point which makes them incompatible
        double dotP_1 = TauP1_dir.Dot((IP_intP_1).Unit());
        double dotP_2 = TauP2_dir.Dot((IP_intP_2).Unit());

        double LambdaP_1 = 0, LambdaP_2 = 0;

        // IF the lines are truly parallel, the decay lenght is technically positive in the direction where there is some separation,
        // So now lambda will be exactly zero only in the case of negative or zero decay lenght
        // The problem of null decay lenght is that the lambda goes to 1 which would be favoured over better values
        if (dotP_1>=0 && TauP1_L>0) LambdaP_1 = std::exp(- TauP1_L / ( TauP1_p4.Beta() * TauP1_p4.Gamma() * 87.0 * 1e-3)); //mum to mm for consistency with the d0
        if (dotP_2>=0 && TauP2_L>0) LambdaP_2 = std::exp(- TauP2_L / ( TauP2_p4.Beta() * TauP2_p4.Gamma() * 87.0 * 1e-3));

        // Repeat for the negative tau
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

        // Use the lambda on the decay lenght as a weight: if it's still zero then the solution is not kept at all, otherwise it's a mix and the kinematics are the same anyway by construction
        double weightP1=0, weightP2=0, weightM1=0, weightM2=0;
        if (LambdaP_1>0 || LambdaP_2>0) {
            weightP1 = LambdaP_1 / (LambdaP_1 + LambdaP_2);
            weightP2 = LambdaP_2 / (LambdaP_1 + LambdaP_2);
        }
        if (LambdaM_1>0 || LambdaM_2>0) {
            weightM1 = LambdaM_1 / (LambdaM_1 + LambdaM_2);
            weightM2 = LambdaM_2 / (LambdaM_1 + LambdaM_2);
        }
        // Apply the weight on the nu and not the tau directly so the taus are only the visible part in case of bad solutions for the nu
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

ROOT::VecOps::RVec<TLorentzVector> TauNuReco_Impact(const TLorentzVector& Recoil, // recoil system or centre of mass
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Charged_p4, // sum of charged daughters of the taus
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Neutral_p4, // sum of neutral daughters of taus (if non then empty)
                                                 const ROOT::VecOps::RVec<float>& D0_p4, // d0 of leading prong
                                                 const ROOT::VecOps::RVec<float>& Z0_p4, //z0 of leading prong
                                                 const TLorentzVector& IP, // interaction point (e=0)
                                                 ROOT::VecOps::RVec<float> charge) // charge of taus, same indices as Charged_p4, Neutral_p4, D0_p4 and Z0_p4
                                                {
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector TauP_p_p4, TauM_p_p4, TauP_k_p4, TauM_k_p4, TauP_d_p4, TauM_d_p4;

    // Build impact vector from track momentum, d0 and z0, assume they have the same index in the collections if the tracks are extracted from the particle
    ROOT::VecOps::RVec<TLorentzVector> Impact_p4 = ImpactVector(Charged_p4, D0_p4, Z0_p4);

    // Order vectors by tau charge: first the positive then negative to keep consistent later on
    // Assumes they have opposite charges
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
    
    //ROOT::Minuit2::Minuit2Minimizer minimizer(ROOT::Minuit2::kMigrad);
    std::unique_ptr<ROOT::Math::Minimizer> minimizer(ROOT::Math::Factory::CreateMinimizer("Minuit2", "Migrad"));
    NuKinFunctor functor(Recoil, TauP_p_p4, TauM_p_p4, TauP_k_p4, TauM_k_p4, TauP_d_p4, TauM_d_p4, IP);
    ROOT::Math::Functor fcn(functor, 2);
    minimizer->SetFunction(fcn);
    minimizer->SetPrintLevel(-1);
    
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
            minimizer->SetVariable(0, "phi_plus", (phi_plus_range.first + phi_plus_range.second) / 2, 0.0001);
            minimizer->SetVariableLimits(0, phi_plus_range.first, phi_plus_range.second);

            // Set phi_minus with the current range
            minimizer->SetVariable(1, "phi_minus", (phi_minus_range.first + phi_minus_range.second) / 2, 0.0001);
            minimizer->SetVariableLimits(1, phi_minus_range.first, phi_minus_range.second);

            bool success = minimizer->Minimize();

            if (success) {

                double current_result = minimizer->MinValue();
                const double* best_params = minimizer->X();
                functor.operator()(best_params); 

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
    // Save the chi2 of the minimization as the first component of a TVL to maintain consistency
    TLorentzVector chi;
    chi.SetPxPyPzE(best_result, 0, 0, 0);
    result.push_back(chi);

    return result;
}

// Following kinematic reconstrcution of di-tau system in its rest frame in https://arxiv.org/pdf/1310.8503
// Returns the taus in the lab frame, for hadronic decays only
// Recoil vector can be recoiling system or center of mass
ROOT::VecOps::RVec<TLorentzVector> TauReco_Kin (TLorentzVector Recoil, ROOT::VecOps::RVec<TLorentzVector> Tau_vis, ROOT::VecOps::RVec<float> charge){
    // First of all, build the visible taus with either jet tagger or the explciit reconstruction
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector temp1;
    TLorentzVector temp2;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H_temp;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H;


    double E_tau = Recoil.M()/2; // energy of the single taus in the rest frame

    for (size_t i = 0; i < Tau_vis.size(); ++i) {

        // Boost the visible taus
        TLorentzVector boostedTau = Tau_vis[i]; 
        boostedTau.Boost(-Recoil.BoostVector()); 
        Tau_vis_H_temp.push_back(boostedTau);
    }

    // Order the taus by charge: first the positive then negative to keep consistent later on
    // Assumes they have opposite charges
    if (charge[0]==1) {
        Tau_vis_H.push_back(Tau_vis_H_temp[0]);
        Tau_vis_H.push_back(Tau_vis_H_temp[1]);
    }
    else {
        Tau_vis_H.push_back(Tau_vis_H_temp[1]);
        Tau_vis_H.push_back(Tau_vis_H_temp[0]);
    }

    // Determine the angle between the visible and neutrino in the rest frame
    double cos0 = (2 * E_tau * Tau_vis_H[0].E() - m_tau * m_tau - Tau_vis_H[0].M() * Tau_vis_H[0].M()) / (2 * Tau_vis_H[0].P() * sqrt(E_tau * E_tau - m_tau * m_tau));
    double cos1 = (2 * E_tau * Tau_vis_H[1].E() - m_tau * m_tau - Tau_vis_H[1].M() * Tau_vis_H[1].M()) / (2 * Tau_vis_H[1].P() * sqrt(E_tau * E_tau - m_tau * m_tau));

    // Solve the system of equations 
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
        // Invalid equations
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
        // Invalid equations
        result.push_back(temp1);
        result.push_back(temp2);
        return result;
    }

    double z1 = (-B + sqrt(discriminant)) / (2*A);
    double z2 = (-B - sqrt(discriminant)) / (2*A);

    double y1 = (q1 - p2*z1) / p1;
    double y2 = (q1 - p2*z2) / p1;

    double x1 = (d - b*y1 - c*z1) / a;
    double x2 = (d - b*y2 - c*z2) / a;

    // Now build the TLV for the tau
    double P_tau = sqrt(E_tau * E_tau - m_tau * m_tau);
    TLorentzVector plus1;
    plus1.SetPxPyPzE(P_tau * x1, P_tau * y1, P_tau * z1, E_tau);
    TLorentzVector plus2;
    plus2.SetPxPyPzE(P_tau * x2, P_tau * y2, P_tau * z2, E_tau);
    TLorentzVector min1;
    min1.SetPxPyPzE(-P_tau * x1, -P_tau * y1, -P_tau * z1, E_tau);
    TLorentzVector min2;
    min2.SetPxPyPzE(-P_tau * x2, -P_tau * y2, -P_tau * z2, E_tau);

    // Save the mean solution as the kinematics are the same, not safe if one needs to know precisely spin variables
    TLorentzVector tauP = (plus1 + plus2) * 0.5; // division doesn't work for tvl but multiplication is component-wise 
    TLorentzVector tauM = (min1 + min2) * 0.5;

    // Boost tau vectors back in the lab frame
    tauP.Boost(Recoil.BoostVector());
    tauM.Boost(Recoil.BoostVector());

    result.push_back(tauP);
    result.push_back(tauM);
    
    return result;
}

}}
