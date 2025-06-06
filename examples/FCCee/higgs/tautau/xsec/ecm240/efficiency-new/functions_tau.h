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


namespace FCCAnalyses { namespace Taufunctions {

// function to build four vectors (px, py, pz, e) from the vectors containing the variables, the index is preserved
ROOT::VecOps::RVec<TLorentzVector> build_p4(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz, ROOT::VecOps::RVec<float> e) {
    ROOT::VecOps::RVec<TLorentzVector> p4;
    for (size_t i = 0; i < px.size(); ++i) {  
        TLorentzVector tlv;
        tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        p4.push_back(tlv);
    }
    return p4;
}

// function to boost a vector of TLorentzVector in the rest frame of another TLorentzVector
ROOT::VecOps::RVec<TLorentzVector> boosted_p4(TLorentzVector boost, ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    for (size_t i = 0; i < vec.size(); ++i) {
        TLorentzVector boosted=vec[i];
        boosted.Boost( - boost.BoostVector());
        result.push_back(boosted);
    }
    return result;
}
// function to boost a TLorentzVector in the rest frame of another TLorentzVector
TLorentzVector boosted_p4_single(TLorentzVector boost, TLorentzVector vec) {
    vec.Boost( - boost.BoostVector());
    return vec;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_All (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request){

    // Identify taus by starting from a jet. This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0)).
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it with specific decay modes
    
    // request parameter, should be not 0 only if needing specific particles in the tau: 
        // 0 for full visible tau, 
        // 1 for charged pion (the one with same chanrge as the tau if from the rho resonance (3 prong)), 
        // 2 for opposite charged pion in rho resonance (3 prong) or sum of neutral particles (1 prong), 
        // 3 for sum of charged pions, 
        // 4 or else for neutral system only (only different from 1 and 2 in case of 3 prong).

    // The outpiut is a ReconstructedParticle type, all the variables are then accessible through the usual methods.

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    for (int i = 0; i < jets.size(); ++i) {

        // Full visible tau (0 in request)
        TLorentzVector sum_tau; 
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauVis;
        // Neutral consituents (2 or 4 in request)
        TLorentzVector neutral;
        // Charged constituents (1 or 3 in request)
        // Sum of them
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

        // There is no easy and direct way of accessing the PID right now so we compare the masses to find specific particles.

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
        } // Too low pt, the particle will be null but still will show up as an entry 

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            out.push_back(Tau); 
            continue;
        }// Leptons in jet, the particle will be null but still will show up as an entry 

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
        // The Id is then increased depending on the number of photons/neutral hadrons found.

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
                                    // i want to save the pion with same charge as the tau as the charged one and the other as the neutral
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

            // Save properly taus (or its components) with mass below 3 GeV
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

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_All_pi0 (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request){

    // request parameter: 0 for full visible tau, 1 for charged pion from the rho resonance (3 prong) or charged pion (1 prong), 2 for opposite charged pion in rho resonance (3 prong) or neutral system (1 prong), 
    // 3 for sum of charged pions, 4 or else for neutral system only (only different from 1 and 2 in case of 3 prong)

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        TLorentzVector neutral;
        TLorentzVector charged;
        ROOT::VecOps::RVec<TLorentzVector> charged_vec;
        ROOT::VecOps::RVec<int> charges_vec;
        edm4hep::ReconstructedParticleData Tau;
        edm4hep::ReconstructedParticleData TauVis;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        ROOT::VecOps::RVec<int> track_vec;
        int track=0;
        float tauID=-1;
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

        charges_vec.push_back(chargeLead);
        charged_vec.push_back(lead);
        track_vec.push_back(track);

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            Tau.type = tauID;
            out.push_back(Tau); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            Tau.type = tauID;
            out.push_back(Tau); //make sure to keep this iteration saved as non tau jets
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
                            if (charges_vec[i] + charges_vec[j] == 0) {  // opposite charges
                                double invMass = (charged_vec[i] + charged_vec[j]).M();
                                double massDifference = std::abs(invMass - 0.775); //rho 0 in gev
                                
                                if (minMassDifference == -1e6) {
                                    minMassDifference = massDifference;
                                    // i want to save the pion with same charge as the tau as the charged one and the other as the neutral
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
                Tau.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
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


//find the leading particle in a collection, returns the particle
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Find_Leading(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in){
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    TLorentzVector lead;
    edm4hep::ReconstructedParticleData part;

    for (auto & p: in) {
        if (std::sqrt(p.momentum.x*p.momentum.x+p.momentum.y*p.momentum.y)>lead.Pt()){
            part = p;
            lead.SetPxPyPzE(p.momentum.x, p.momentum.y, p.momentum.z, p.energy);
        }
    }
    result.push_back(part);

    return result;
}

//find the leading particle in a collection, returns the particle
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Find_LeadingPair(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;

    edm4hep::ReconstructedParticleData lead;
    edm4hep::ReconstructedParticleData sub;
    double maxPt = -1.0;
    double subMaxPt = -1.0;

    for (const auto& p : in) {
        double pt = std::sqrt(p.momentum.x*p.momentum.x+p.momentum.y*p.momentum.y);

        // If new max pt, move current lead to sub and update lead
        if (pt > maxPt) {
            if (p.charge != lead.charge) {
                sub = lead;
                subMaxPt = maxPt;
            }
            lead = p;
            maxPt = pt;
        }
        // Else if it's a good subleading candidate with opposite charge
        else if (pt > subMaxPt && p.charge != lead.charge) {
            sub = p;
            subMaxPt = pt;
        }
    }

    // Add only if both found and charges are opposite
    if (maxPt > 0 && subMaxPt > 0 && lead.charge * sub.charge < 0) {
        result.push_back(lead);
        result.push_back(sub);
    }

    return result;
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

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> findTauInJet_pi0 (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        edm4hep::ReconstructedParticleData partMod;
        ROOT::VecOps::RVec<TLorentzVector> photons_vec;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        float tauID=-1;
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

            else  {
                count_pho++;
                // save the photons in a vector of tlvs for pi0 reconstruction
                if (tlv.M()<0.2) photons_vec.push_back(tlv);
                }

            sum_tau += tlv;  // This is the 4 momenta of only the particles we have selected

        }

        // pi0 reconstruction
        for (size_t i = 0; i < photons_vec.size(); ++i) {
            for (size_t j = i + 1; j < photons_vec.size(); ++j) {
                TLorentzVector pair = photons_vec[i] + photons_vec[j];
                double mass = pair.M();
                //apply 50 MeV of tollerance for the pi0 reconstruction for fast sim
                if (std::abs(mass - 0.135) < 5e-2) {
                    count_pi0++;
                }
            }
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


}}

#endif
