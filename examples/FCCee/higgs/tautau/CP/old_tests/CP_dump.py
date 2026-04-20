########################################
# ALL THE THING THAT DID NOT WORK OUT #
########################################             
                
                #############################
                ####### STAGE 2 #############
                #############################

                #########################################

                # following Belle reconstruction https://arxiv.org/pdf/1310.8503 to get the tau 4 vector in the recoil frame, then get the neutrino momentum by subtraction
                # then following ILC polarimetric vectors for the cp angle
                # the reconstruction does not work, the taus have about 5 gev more energy than they should

                .Define("Recoil_True_Tau_p4",        "FCCAnalyses::ZHfunctions::build_tau_p4(GenHiggs_p4, GenEmiss_p4, GenPi_p4, GenPi_Impact_p4, GenIP)")
                #filtering events where the discriminant to solve is negative and so the reconstruction didn't work out
                .Filter("Recoil_True_Tau_p4.at(0).P()!=0 and Recoil_True_Tau_p4.at(1).P()!=0")

                .Define("True_TauP_p4",     "Recoil_True_Tau_p4.at(0)")
                .Define("True_TauM_p4",     "Recoil_True_Tau_p4.at(1)")

                .Define("True_NuP_p4",      "Recoil_True_Tau_p4.at(0) - GenPiP_p4.at(0)")
                .Define("True_NuM_p4",      "Recoil_True_Tau_p4.at(1) - GenPiM_p4.at(0)")

                .Define("TauPRF_RecoPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauP_p4, GenPiP_p4.at(0))")
                .Define("TauPRF_RecoNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauP_p4, True_NuP_p4)")

                .Define("TauMRF_RecoPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauM_p4,  GenPiM_p4.at(0))")
                .Define("TauMRF_RecoNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauM_p4, True_NuM_p4)")
                
                .Define("hP_p3",       "TauPRF_RecoPiP_p4.Vect()")
                .Define("hM_p3",       "TauMRF_RecoPiM_p4.Vect()")

                # get the direction on which to compute the angles from the tauM boosted into the higgs/recoil rest frame
                .Define("Recoil_TauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, True_TauM_p4)")

                .Define("hPnorm",       "(( Recoil_TauM_p4.Vect() ).Cross( hP_p3 )).Unit()")
                .Define("hMnorm",       "(( Recoil_TauM_p4.Vect() ).Cross( hM_p3 )).Unit()")

                .Define("hh_norm",       "hPnorm.Cross(hMnorm)")
                .Define("CosDeltaPhi",        "hPnorm.Dot(hMnorm)")
                .Define("SinDeltaPhi",       "hh_norm.Dot( (Recoil_TauM_p4.Vect()).Unit() )")
                .Define("DeltaPhi",     "atan2(SinDeltaPhi, CosDeltaPhi)")

                #following Belle reconstruction https://arxiv.org/pdf/1310.8503 to get the tau 4 vector in the recoil frame, then get the neutrino momentum by subtraction
                # 5 gev too much reconstructed energy for the solutions of the taus

                .Define("RecoEmiss_p4",  "FCCAnalyses::ZHfunctions::build_p4_single(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")

                .Define("True_Tau_p4",        "FCCAnalyses::ZHfunctions::build_tau_p4(Recoil_p4, RecoEmiss_p4, RecoTau_p4, TauFromJet_R5_charge)")
                .Define("True_TauP_p4",       "True_Tau_p4.at(0)")
                .Define("True_TauP_idx",       "if (TauFromJet_R5_charge.at(0)==1) return 0; else return 1;")
                .Define("True_NuP_p4",         "if (TauFromJet_R5_charge.at(0)==1) return True_TauP_p4 - RecoTau_p4.at(0); else return True_TauP_p4 - RecoTau_p4.at(1);")
                .Define("True_TauM_p4",       "True_Tau_p4.at(1)")
                .Define("True_TauM_idx",       "if (TauFromJet_R5_charge.at(0)==1) return 1; else return 0;")
                .Define("True_NuM_p4",         "if (TauFromJet_R5_charge.at(0)==1) return True_TauM_p4 - RecoTau_p4.at(1); else return True_TauM_p4 - RecoTau_p4.at(0);") 
                #filtering events where the discriminant to solve is negative and so the reconstruction didn't work out
                .Filter("True_Tau_p4.at(0).P()!=0 and True_Tau_p4.at(1).P()!=0")
            
                .Define("TauPRF_RecoPiP_p4",    "if (TauFromJet_R5_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauP_p4, RecoTau_p4.at(0)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauP_p4,  RecoTau_p4.at(1));")
                .Define("TauPRF_RecoNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauP_p4, True_NuP_p4)")

                .Define("TauMRF_RecoPiM_p4",    "if (TauFromJet_R5_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauM_p4,  RecoTau_p4.at(1)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauM_p4,  RecoTau_p4.at(0));")
                .Define("TauMRF_RecoNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- True_TauM_p4, True_NuM_p4)")
                
                .Define("hP_p3",       "TauPRF_RecoPiP_p4.Vect()")
                .Define("hM_p3",       "TauMRF_RecoPiM_p4.Vect()")

                # get the direction on which to compute the angles from the tauM boosted into the higgs/recoil rest frame
                .Define("Recoil_TauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- Recoil_p4, True_TauM_p4)")

                .Define("hPnorm",       "(( Recoil_TauM_p4.Vect() ).Cross( hP_p3 )).Unit()")
                .Define("hMnorm",       "(( Recoil_TauM_p4.Vect() ).Cross( hM_p3 )).Unit()")

                .Define("hh_norm",       "hPnorm.Cross(hMnorm)")
                .Define("CosDeltaPhi",        "hPnorm.Dot(hMnorm)")
                .Define("SinDeltaPhi",       "hh_norm.Dot( (Recoil_TauM_p4.Vect()).Unit() )")
                .Define("DeltaPhi",     "atan2(SinDeltaPhi, CosDeltaPhi)")

                ####################################################

                # kinematic fit with minuit2 with polarimeters
                # no way of distinguishing the two solutions for each tau because only the first minimum is kept
                
                .Define("Kin_Tau_p4",        "FCCAnalyses::ZHfunctions::build_nu_kin(RecoEmiss_p4, RecoTau_p4, TauFromJet_R5_charge)")
                #.Filter("Kin_Tau_p4.at(0).M()>1.77 and Kin_Tau_p4.at(1).M()>1.77 and Kin_Tau_p4.at(0).M()<1.78 and Kin_Tau_p4.at(1).M()<1.78")
                #.Filter("Kin_Tau_p4.at(0).M()>0 && Kin_Tau_p4.at(1).M()>0")

                .Define("Kin_TauP_p4",       "Kin_Tau_p4.at(0)")
                .Define("Kin_TauM_p4",       "Kin_Tau_p4.at(1)")
                .Define("Kin_chi2",         "Kin_Tau_p4.at(2).Px()")

                .Define("Kin_NuP_p4",      "Kin_TauP_p4 - TauP_p4")
                .Define("Kin_NuM_p4",      "Kin_TauM_p4 - TauM_p4")

                .Define("Kin_TauNuP_DR",        "FCCAnalyses::ZHfunctions::deltaR(Kin_TauP_p4.Phi(), Kin_NuP_p4.Phi(), Kin_TauP_p4.Eta(), Kin_NuP_p4.Eta())")
                .Define("Kin_TauNuM_DR",        "FCCAnalyses::ZHfunctions::deltaR(Kin_TauM_p4.Phi(), Kin_NuM_p4.Phi(), Kin_TauM_p4.Eta(), Kin_NuM_p4.Eta())")

                .Define("TauPRF_KinPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauP_p4, TauP_p4)")
                .Define("TauPRF_KinNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauP_p4, Kin_NuP_p4)")

                .Define("TauMRF_KinPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauM_p4,  TauM_p4)")
                .Define("TauMRF_KinNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauM_p4, Kin_NuM_p4)")
                
                .Define("hP_p3Kin",       "TauPRF_KinPiP_p4.Vect()")
                .Define("hM_p3Kin",       "TauMRF_KinPiM_p4.Vect()")
                .Define("RecoilKin_TauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- RecoH_p4, Kin_TauM_p4)")

                .Define("hPnormKin",       "(( RecoilKin_TauM_p4.Vect() ).Cross( hP_p3Kin )).Unit()")
                .Define("hMnormKin",       "(( RecoilKin_TauM_p4.Vect() ).Cross( hM_p3Kin )).Unit()")

                .Define("hh_normKin",       "hPnormKin.Cross(hMnormKin)")
                .Define("CosDeltaPhiKin",        "hPnormKin.Dot(hMnormKin)")
                .Define("SinDeltaPhiKin",       "hh_normKin.Dot( (RecoilKin_TauM_p4.Vect()).Unit() )")
                .Define("DeltaPhiKin",     "atan2(SinDeltaPhiKin, CosDeltaPhiKin)")

                ## gen
                # kinematic fit with minuit2 with polarimeters
                # works well in terms of individual components of the reconstructed tau but then there is a flip of hh_normKin with respect to the gen one that completely kills the cp
                # may be due to the small deviation in the tau reconstruction, no toher variable is correlated to this effect
                

                .Define("Kin_Tau_p4",        "FCCAnalyses::ZHfunctions::build_nu_kin(GenEmiss_p4, GenPi_p4, GenPi_charge)")
                #.Filter("Kin_Tau_p4.at(0).M()>1.77 and Kin_Tau_p4.at(1).M()>1.77 and Kin_Tau_p4.at(0).M()<1.78 and Kin_Tau_p4.at(1).M()<1.78")
                #.Filter("Kin_Tau_p4.at(0).M()>0 && Kin_Tau_p4.at(1).M()>0")

                .Define("Kin_TauP_p4",       "Kin_Tau_p4.at(0)")
                .Define("Kin_TauM_p4",       "Kin_Tau_p4.at(1)")
                .Define("Kin_chi2",         "Kin_Tau_p4.at(2).Px()")

                .Define("Kin_NuP_p4",      "Kin_TauP_p4 - GenPiP_p4")
                .Define("Kin_NuM_p4",      "Kin_TauM_p4 - GenPiM_p4")

                .Define("Kin_TauNuP_DR",        "FCCAnalyses::ZHfunctions::deltaR(Kin_TauP_p4.Phi(), Kin_NuP_p4.Phi(), Kin_TauP_p4.Eta(), Kin_NuP_p4.Eta())")
                .Define("Kin_TauNuM_DR",        "FCCAnalyses::ZHfunctions::deltaR(Kin_TauM_p4.Phi(), Kin_NuM_p4.Phi(), Kin_TauM_p4.Eta(), Kin_NuM_p4.Eta())")

                .Define("TauPRF_KinPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauP_p4, GenPiP_p4)")
                .Define("TauPRF_KinNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauP_p4, Kin_NuP_p4)")

                .Define("TauMRF_KinPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauM_p4,  GenPiM_p4)")
                .Define("TauMRF_KinNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- Kin_TauM_p4, Kin_NuM_p4)")
                
                .Define("hP_p3Kin",       "TauPRF_KinPiP_p4.Vect()")
                .Define("hM_p3Kin",       "TauMRF_KinPiM_p4.Vect()")
                .Define("RecoilKin_TauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, Kin_TauM_p4)")

                .Define("hPnormKin",       "(( RecoilKin_TauM_p4.Vect() ).Cross( hP_p3Kin )).Unit()")
                .Define("hMnormKin",       "(( RecoilKin_TauM_p4.Vect() ).Cross( hM_p3Kin )).Unit()")

                .Define("hh_normKin",       "hPnormKin.Cross(hMnormKin)")
                .Define("CosDeltaPhiKin",        "hPnormKin.Dot(hMnormKin)")
                .Define("SinDeltaPhiKin",       "hh_normKin.Dot( (RecoilKin_TauM_p4.Vect()).Unit() )")
                .Define("DeltaPhiKin",     "atan2(SinDeltaPhiKin, CosDeltaPhiKin)")

                #saving the varibales for comparison

                .Define("Kin_TauP_Px", "Kin_TauP_p4.Px()")
                .Define("Kin_TauP_Py", "Kin_TauP_p4.Py()")
                .Define("Kin_TauP_Pz", "Kin_TauP_p4.Pz()")
                .Define("Kin_TauP_E", "Kin_TauP_p4.E()")
                .Define("Kin_TauP_M", "Kin_TauP_p4.M()")
                .Define("Kin_TauP_Eta", "Kin_TauP_p4.Eta()")
                .Define("Kin_TauP_Phi", "Kin_TauP_p4.Phi()")
                .Define("Kin_TauP_P", "Kin_TauP_p4.P()")
                .Define("Kin_TauP_Pt", "Kin_TauP_p4.Pt()")
                .Define("Kin_TauP_Theta", "Kin_TauP_p4.Theta()")
                .Define("Kin_TauP_Rapidity", "Kin_TauP_p4.Rapidity()")

                .Define("Kin_TauM_Px", "Kin_TauM_p4.Px()")
                .Define("Kin_TauM_Py", "Kin_TauM_p4.Py()")
                .Define("Kin_TauM_Pz", "Kin_TauM_p4.Pz()")
                .Define("Kin_TauM_E", "Kin_TauM_p4.E()")
                .Define("Kin_TauM_M", "Kin_TauM_p4.M()")
                .Define("Kin_TauM_Eta", "Kin_TauM_p4.Eta()")
                .Define("Kin_TauM_Phi", "Kin_TauM_p4.Phi()")
                .Define("Kin_TauM_P", "Kin_TauM_p4.P()")
                .Define("Kin_TauM_Pt", "Kin_TauM_p4.Pt()")
                .Define("Kin_TauM_Theta", "Kin_TauM_p4.Theta()")
                .Define("Kin_TauM_Rapidity", "Kin_TauM_p4.Rapidity()")

                .Define("Kin_NuP_Px", "Kin_NuP_p4.Px()")
                .Define("Kin_NuP_Py", "Kin_NuP_p4.Py()")
                .Define("Kin_NuP_Pz", "Kin_NuP_p4.Pz()")
                .Define("Kin_NuP_E", "Kin_NuP_p4.E()")
                .Define("Kin_NuP_M", "Kin_NuP_p4.M()")
                .Define("Kin_NuP_Eta", "Kin_NuP_p4.Eta()")
                .Define("Kin_NuP_Phi", "Kin_NuP_p4.Phi()")
                .Define("Kin_NuP_P", "Kin_NuP_p4.P()")
                .Define("Kin_NuP_Pt", "Kin_NuP_p4.Pt()")
                .Define("Kin_NuP_Theta", "Kin_NuP_p4.Theta()")
                .Define("Kin_NuP_Rapidity", "Kin_NuP_p4.Rapidity()")

                .Define("Kin_NuM_Px", "Kin_NuM_p4.Px()")
                .Define("Kin_NuM_Py", "Kin_NuM_p4.Py()")
                .Define("Kin_NuM_Pz", "Kin_NuM_p4.Pz()")
                .Define("Kin_NuM_E", "Kin_NuM_p4.E()")
                .Define("Kin_NuM_M", "Kin_NuM_p4.M()")
                .Define("Kin_NuM_Eta", "Kin_NuM_p4.Eta()")
                .Define("Kin_NuM_Phi", "Kin_NuM_p4.Phi()")
                .Define("Kin_NuM_P", "Kin_NuM_p4.P()")
                .Define("Kin_NuM_Pt", "Kin_NuM_p4.Pt()")
                .Define("Kin_NuM_Theta", "Kin_NuM_p4.Theta()")
                .Define("Kin_NuM_Rapidity", "Kin_NuM_p4.Rapidity()")

                .Define("TauPRF_KinPiP_Px", "TauPRF_KinPiP_p4.Px()")
                .Define("TauPRF_KinPiP_Py", "TauPRF_KinPiP_p4.Py()")
                .Define("TauPRF_KinPiP_Pz", "TauPRF_KinPiP_p4.Pz()")
                .Define("TauPRF_KinPiP_E", "TauPRF_KinPiP_p4.E()")
                .Define("TauPRF_KinPiP_M", "TauPRF_KinPiP_p4.M()")
                .Define("TauPRF_KinPiP_Eta", "TauPRF_KinPiP_p4.Eta()")
                .Define("TauPRF_KinPiP_Phi", "TauPRF_KinPiP_p4.Phi()")
                .Define("TauPRF_KinPiP_P", "TauPRF_KinPiP_p4.P()")
                .Define("TauPRF_KinPiP_Pt", "TauPRF_KinPiP_p4.Pt()")
                .Define("TauPRF_KinPiP_Theta", "TauPRF_KinPiP_p4.Theta()")
                .Define("TauPRF_KinPiP_Rapidity", "TauPRF_KinPiP_p4.Rapidity()")

                .Define("TauMRF_KinPiM_Px", "TauMRF_KinPiM_p4.Px()")
                .Define("TauMRF_KinPiM_Py", "TauMRF_KinPiM_p4.Py()")
                .Define("TauMRF_KinPiM_Pz", "TauMRF_KinPiM_p4.Pz()")
                .Define("TauMRF_KinPiM_E", "TauMRF_KinPiM_p4.E()")
                .Define("TauMRF_KinPiM_M", "TauMRF_KinPiM_p4.M()")
                .Define("TauMRF_KinPiM_Eta", "TauMRF_KinPiM_p4.Eta()")
                .Define("TauMRF_KinPiM_Phi", "TauMRF_KinPiM_p4.Phi()")
                .Define("TauMRF_KinPiM_P", "TauMRF_KinPiM_p4.P()")
                .Define("TauMRF_KinPiM_Pt", "TauMRF_KinPiM_p4.Pt()")
                .Define("TauMRF_KinPiM_Theta", "TauMRF_KinPiM_p4.Theta()")
                .Define("TauMRF_KinPiM_Rapidity", "TauMRF_KinPiM_p4.Rapidity()")

                .Define("TauPRF_KinNuP_Px", "TauPRF_KinNuP_p4.Px()")
                .Define("TauPRF_KinNuP_Py", "TauPRF_KinNuP_p4.Py()")
                .Define("TauPRF_KinNuP_Pz", "TauPRF_KinNuP_p4.Pz()")
                .Define("TauPRF_KinNuP_E", "TauPRF_KinNuP_p4.E()")
                .Define("TauPRF_KinNuP_M", "TauPRF_KinNuP_p4.M()")
                .Define("TauPRF_KinNuP_Eta", "TauPRF_KinNuP_p4.Eta()")
                .Define("TauPRF_KinNuP_Phi", "TauPRF_KinNuP_p4.Phi()")
                .Define("TauPRF_KinNuP_P", "TauPRF_KinNuP_p4.P()")
                .Define("TauPRF_KinNuP_Pt", "TauPRF_KinNuP_p4.Pt()")
                .Define("TauPRF_KinNuP_Theta", "TauPRF_KinNuP_p4.Theta()")
                .Define("TauPRF_KinNuP_Rapidity", "TauPRF_KinNuP_p4.Rapidity()")

                .Define("TauMRF_KinNuM_Px", "TauMRF_KinNuM_p4.Px()")
                .Define("TauMRF_KinNuM_Py", "TauMRF_KinNuM_p4.Py()")
                .Define("TauMRF_KinNuM_Pz", "TauMRF_KinNuM_p4.Pz()")
                .Define("TauMRF_KinNuM_E", "TauMRF_KinNuM_p4.E()")
                .Define("TauMRF_KinNuM_M", "TauMRF_KinNuM_p4.M()")
                .Define("TauMRF_KinNuM_Eta", "TauMRF_KinNuM_p4.Eta()")
                .Define("TauMRF_KinNuM_Phi", "TauMRF_KinNuM_p4.Phi()")
                .Define("TauMRF_KinNuM_P", "TauMRF_KinNuM_p4.P()")
                .Define("TauMRF_KinNuM_Pt", "TauMRF_KinNuM_p4.Pt()")
                .Define("TauMRF_KinNuM_Theta", "TauMRF_KinNuM_p4.Theta()")
                .Define("TauMRF_KinNuM_Rapidity", "TauMRF_KinNuM_p4.Rapidity()")

                .Define("RecoilKin_TauM_Px", "RecoilKin_TauM_p4.Px()")
                .Define("RecoilKin_TauM_Py", "RecoilKin_TauM_p4.Py()")
                .Define("RecoilKin_TauM_Pz", "RecoilKin_TauM_p4.Pz()")
                .Define("RecoilKin_TauM_E", "RecoilKin_TauM_p4.E()")
                .Define("RecoilKin_TauM_M", "RecoilKin_TauM_p4.M()")
                .Define("RecoilKin_TauM_Eta", "RecoilKin_TauM_p4.Eta()")
                .Define("RecoilKin_TauM_Phi", "RecoilKin_TauM_p4.Phi()")
                .Define("RecoilKin_TauM_P", "RecoilKin_TauM_p4.P()")
                .Define("RecoilKin_TauM_Pt", "RecoilKin_TauM_p4.Pt()")
                .Define("RecoilKin_TauM_Theta", "RecoilKin_TauM_p4.Theta()")
                .Define("RecoilKin_TauM_Rapidity", "RecoilKin_TauM_p4.Rapidity()")

                .Define("hPnormKin_Px", "hPnormKin.X()")
                .Define("hPnormKin_Py", "hPnormKin.Y()")
                .Define("hPnormKin_Pz", "hPnormKin.Z()")
                .Define("hPnormKin_P", "hPnormKin.Mag()")
                .Define("hPnormKin_Pt", "hPnormKin.Pt()")
                .Define("hPnormKin_Eta", "hPnormKin.Eta()")
                .Define("hPnormKin_Theta", "hPnormKin.Theta()")
                .Define("hPnormKin_Phi", "hPnormKin.Phi()")

                .Define("hMnormKin_Px", "hMnormKin.X()")
                .Define("hMnormKin_Py", "hMnormKin.Y()")
                .Define("hMnormKin_Pz", "hMnormKin.Z()")
                .Define("hMnormKin_P", "hMnormKin.Mag()")
                .Define("hMnormKin_Pt", "hMnormKin.Pt()")
                .Define("hMnormKin_Phi", "hMnormKin.Phi()")
                .Define("hMnormKin_Eta", "hMnormKin.Eta()")
                .Define("hMnormKin_Theta", "hMnormKin.Theta()")

                .Define("hh_normKin_Px", "hh_normKin.X()")
                .Define("hh_normKin_Py", "hh_normKin.Y()")
                .Define("hh_normKin_Pz", "hh_normKin.Z()")
                .Define("hh_normKin_P", "hh_normKin.Mag()")
                .Define("hh_normKin_Pt", "hh_normKin.Pt()")
                .Define("hh_normKin_Phi", "hh_normKin.Phi()")
                .Define("hh_normKin_Eta", "hh_normKin.Eta()")
                .Define("hh_normKin_Theta", "hh_normKin.Theta()")

                #comparison between kinematic fit and gen

                .Define("KinGenTauP_p4",       "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return (Kin_TauP_p4-HadGenTau_p4.at(0)); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return (Kin_TauP_p4-HadGenTau_p4.at(1)); \
                                                else return TLorentzVector {};")
                .Define("KinGenTauP_Px",        "KinGenTauP_p4.Px()")
                .Define("KinGenTauP_Py",        "KinGenTauP_p4.Py()")
                .Define("KinGenTauP_Pz",        "KinGenTauP_p4.Pz()")
                .Define("KinGenTauP_P",        "KinGenTauP_p4.P()")
                .Define("KinGenTauP_Pt",        "KinGenTauP_p4.Pt()")
                .Define("KinGenTauP_E",        "KinGenTauP_p4.E()")
                .Define("KinGenTauP_M",        "KinGenTauP_p4.M()")
                .Define("KinGenTauP_DPhi",       "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::deltaPhi(Kin_TauP_p4.Phi(), HadGenTau_p4.at(0).Phi()); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return FCCAnalyses::ZHfunctions::deltaPhi(Kin_TauP_p4.Phi(), HadGenTau_p4.at(1).Phi()); \
                                                else return float(-99);")
                .Define("KinGenTauP_DEta",      "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return (Kin_TauP_p4.Eta()-(HadGenTau_p4.at(0)).Eta()); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return (Kin_TauP_p4.Eta()-(HadGenTau_p4.at(1)).Eta()); \
                                                else return double(-99);")
                .Define("KinGenTauP_DTheta",      "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return ((Kin_TauP_p4.Vect()).Angle(HadGenTau_p4.at(0).Vect())); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return ((Kin_TauP_p4.Vect()).Angle(HadGenTau_p4.at(1).Vect())); \
                                                else return double(-99.);")
                

                .Define("KinGenNuP_p4",       "(Kin_NuP_p4-GenNuP_p4)")
                .Define("KinGenNuP_Px",        "KinGenNuP_p4.Px()")
                .Define("KinGenNuP_Py",        "KinGenNuP_p4.Py()")
                .Define("KinGenNuP_Pz",        "KinGenNuP_p4.Pz()")
                .Define("KinGenNuP_P",        "KinGenNuP_p4.P()")
                .Define("KinGenNuP_Pt",        "KinGenNuP_p4.Pt()")
                .Define("KinGenNuP_M",        "KinGenNuP_p4.M()")
                .Define("KinGenNuP_E",        "KinGenNuP_p4.E()")
                .Define("KinGenNuP_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(Kin_NuP_p4.Phi(), GenNuP_p4.Phi())")
                .Define("KinGenNuP_DEta",      "(Kin_NuP_p4.Eta()-(GenNuP_p4).Eta())")
                .Define("KinGenNuP_DTheta",     "((Kin_NuP_p4.Vect()).Angle(GenNuP_p4.Vect()))")

                .Define("TauPRF_KinGenNuP_p4",       "(TauPRF_KinNuP_p4-TauPRF_GenNuP_p4)")
                .Define("TauPRF_KinGenNuP_Px",        "TauPRF_KinGenNuP_p4.Px()")
                .Define("TauPRF_KinGenNuP_Py",        "TauPRF_KinGenNuP_p4.Py()")
                .Define("TauPRF_KinGenNuP_Pz",        "TauPRF_KinGenNuP_p4.Pz()")
                .Define("TauPRF_KinGenNuP_P",        "TauPRF_KinGenNuP_p4.P()")
                .Define("TauPRF_KinGenNuP_Pt",        "TauPRF_KinGenNuP_p4.Pt()")
                .Define("TauPRF_KinGenNuP_M",        "TauPRF_KinGenNuP_p4.M()")
                .Define("TauPRF_KinGenNuP_E",        "TauPRF_KinGenNuP_p4.E()")
                .Define("TauPRF_KinGenNuP_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(TauPRF_KinNuP_p4.Phi(), TauPRF_GenNuP_p4.Phi())")
                .Define("TauPRF_KinGenNuP_DEta",      "(TauPRF_KinNuP_p4.Eta()-(TauPRF_GenNuP_p4).Eta())")
                .Define("TauPRF_KinGenNuP_DTheta",      "((TauPRF_KinNuP_p4.Vect()).Angle(TauPRF_GenNuP_p4.Vect()))")

                .Define("TauPRF_KinGenPiP_p4",       "(TauPRF_KinPiP_p4-TauPRF_GenPiP_p4)")
                .Define("TauPRF_KinGenPiP_Px",        "TauPRF_KinGenPiP_p4.Px()")
                .Define("TauPRF_KinGenPiP_Py",        "TauPRF_KinGenPiP_p4.Py()")
                .Define("TauPRF_KinGenPiP_Pz",        "TauPRF_KinGenPiP_p4.Pz()")
                .Define("TauPRF_KinGenPiP_P",        "TauPRF_KinGenPiP_p4.P()")
                .Define("TauPRF_KinGenPiP_Pt",        "TauPRF_KinGenPiP_p4.Pt()")
                .Define("TauPRF_KinGenPiP_M",        "TauPRF_KinGenPiP_p4.M()")
                .Define("TauPRF_KinGenPiP_E",        "TauPRF_KinGenPiP_p4.E()")
                .Define("TauPRF_KinGenPiP_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(TauPRF_KinPiP_p4.Phi(), TauPRF_GenPiP_p4.Phi())")
                .Define("TauPRF_KinGenPiP_DEta",      "(TauPRF_KinPiP_p4.Eta()-(TauPRF_GenPiP_p4).Eta())")
                .Define("TauPRF_KinGenPiP_DTheta",      "((TauPRF_KinPiP_p4.Vect()).Angle(TauPRF_GenPiP_p4.Vect()))")

                .Define("KinGen_hPnorm_p3",       "(hPnormKin-GenhPnorm)")
                .Define("KinGen_hPnorm_Px",        "KinGen_hPnorm_p3.Px()")
                .Define("KinGen_hPnorm_Py",        "KinGen_hPnorm_p3.Py()")
                .Define("KinGen_hPnorm_Pz",        "KinGen_hPnorm_p3.Pz()")
                .Define("KinGen_hPnorm_P",        "KinGen_hPnorm_p3.Mag()")
                .Define("KinGen_hPnorm_Pt",        "KinGen_hPnorm_p3.Pt()")
                .Define("KinGen_hPnorm_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(hPnormKin.Phi(), GenhPnorm.Phi())")
                .Define("KinGen_hPnorm_DEta",      "(hPnormKin.Eta()-(GenhPnorm).Eta())")
                .Define("KinGen_hPnorm_DTheta",     "(hPnormKin.Angle(GenhPnorm))")

                .Define("KinGenTauM_p4",       "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return (Kin_TauM_p4-HadGenTau_p4.at(1)); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return (Kin_TauM_p4-HadGenTau_p4.at(0)); \
                                                else return TLorentzVector {};")
                .Define("KinGenTauM_Px",        "KinGenTauM_p4.Px()")
                .Define("KinGenTauM_Py",        "KinGenTauM_p4.Py()")
                .Define("KinGenTauM_Pz",        "KinGenTauM_p4.Pz()")
                .Define("KinGenTauM_P",        "KinGenTauM_p4.P()")
                .Define("KinGenTauM_Pt",        "KinGenTauM_p4.Pt()")
                .Define("KinGenTauM_E",        "KinGenTauM_p4.E()")
                .Define("KinGenTauM_M",        "KinGenTauM_p4.M()")
                .Define("KinGenTauM_DPhi",       "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::deltaPhi(Kin_TauM_p4.Phi(), HadGenTau_p4.at(1).Phi()); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return FCCAnalyses::ZHfunctions::deltaPhi(Kin_TauM_p4.Phi(), HadGenTau_p4.at(0).Phi()); \
                                                else return float(-99);")
                .Define("KinGenTauM_DEta",      "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return (Kin_TauM_p4.Eta()-(HadGenTau_p4.at(1)).Eta()); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return (Kin_TauM_p4.Eta()-(HadGenTau_p4.at(0)).Eta()); \
                                                else return double(-99);")
                .Define("KinGenTauM_DTheta",      "if (n_GenTau_had==2 and HadGenTau_charge.at(0)==1) return ((Kin_TauM_p4.Vect()).Angle(HadGenTau_p4.at(1).Vect())); \
                                                else if (n_GenTau_had==2 and HadGenTau_charge.at(0)==(-1)) return ((Kin_TauM_p4.Vect()).Angle(HadGenTau_p4.at(0).Vect())); \
                                                else return double(-99.);")

                .Define("KinGenNuM_p4",       "(Kin_NuM_p4-GenNuM_p4)")
                .Define("KinGenNuM_Px",        "KinGenNuM_p4.Px()")
                .Define("KinGenNuM_Py",        "KinGenNuM_p4.Py()")
                .Define("KinGenNuM_Pz",        "KinGenNuM_p4.Pz()")
                .Define("KinGenNuM_P",        "KinGenNuM_p4.P()")
                .Define("KinGenNuM_Pt",        "KinGenNuM_p4.Pt()")
                .Define("KinGenNuM_M",        "KinGenNuM_p4.M()")
                .Define("KinGenNuM_E",        "KinGenNuM_p4.E()")
                .Define("KinGenNuM_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(Kin_NuM_p4.Phi(), GenNuM_p4.Phi())")
                .Define("KinGenNuM_DEta",      "(Kin_NuM_p4.Eta()-(GenNuM_p4).Eta())")
                .Define("KinGenNuM_DTheta",     "((Kin_NuM_p4.Vect()).Angle(GenNuM_p4.Vect()))")

                .Define("TauMRF_KinGenNuM_p4",       "(TauMRF_KinNuM_p4-TauMRF_GenNuM_p4)")
                .Define("TauMRF_KinGenNuM_Px",        "TauMRF_KinGenNuM_p4.Px()")
                .Define("TauMRF_KinGenNuM_Py",        "TauMRF_KinGenNuM_p4.Py()")
                .Define("TauMRF_KinGenNuM_Pz",        "TauMRF_KinGenNuM_p4.Pz()")
                .Define("TauMRF_KinGenNuM_P",        "TauMRF_KinGenNuM_p4.P()")
                .Define("TauMRF_KinGenNuM_Pt",        "TauMRF_KinGenNuM_p4.Pt()")
                .Define("TauMRF_KinGenNuM_E",        "TauMRF_KinGenNuM_p4.E()")
                .Define("TauMRF_KinGenNuM_M",        "TauMRF_KinGenNuM_p4.M()")
                .Define("TauMRF_KinGenNuM_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(TauMRF_KinNuM_p4.Phi(), TauMRF_GenNuM_p4.Phi())")
                .Define("TauMRF_KinGenNuM_DEta",      "(TauMRF_KinNuM_p4.Eta()-(TauMRF_GenNuM_p4).Eta())")
                .Define("TauMRF_KinGenNuM_DTheta",      "((TauMRF_KinNuM_p4.Vect()).Angle(TauMRF_GenNuM_p4.Vect()))")

                .Define("TauMRF_KinGenPiM_p4",       "(TauMRF_KinPiM_p4-TauMRF_GenPiM_p4)")
                .Define("TauMRF_KinGenPiM_Px",        "TauMRF_KinGenPiM_p4.Px()")
                .Define("TauMRF_KinGenPiM_Py",        "TauMRF_KinGenPiM_p4.Py()")
                .Define("TauMRF_KinGenPiM_Pz",        "TauMRF_KinGenPiM_p4.Pz()")
                .Define("TauMRF_KinGenPiM_P",        "TauMRF_KinGenPiM_p4.P()")
                .Define("TauMRF_KinGenPiM_Pt",        "TauMRF_KinGenPiM_p4.Pt()")
                .Define("TauMRF_KinGenPiM_M",        "TauMRF_KinGenPiM_p4.M()")
                .Define("TauMRF_KinGenPiM_E",        "TauMRF_KinGenPiM_p4.E()")
                .Define("TauMRF_KinGenPiM_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(TauMRF_KinPiM_p4.Phi(), TauMRF_GenPiM_p4.Phi())")
                .Define("TauMRF_KinGenPiM_DEta",      "(TauMRF_KinPiM_p4.Eta()-(TauMRF_GenPiM_p4).Eta())")
                .Define("TauMRF_KinGenPiM_DTheta",      "((TauMRF_KinPiM_p4.Vect()).Angle(TauMRF_GenPiM_p4.Vect()))")

                .Define("HRF_KinGenTauM_p4",       "(RecoilKin_TauM_p4-HRF_HadGenTauM_p4)")
                .Define("HRF_KinGenTauM_Px",        "HRF_KinGenTauM_p4.Px()")
                .Define("HRF_KinGenTauM_Py",        "HRF_KinGenTauM_p4.Py()")
                .Define("HRF_KinGenTauM_Pz",        "HRF_KinGenTauM_p4.Pz()")
                .Define("HRF_KinGenTauM_P",        "HRF_KinGenTauM_p4.P()")
                .Define("HRF_KinGenTauM_Pt",        "HRF_KinGenTauM_p4.Pt()")
                .Define("HRF_KinGenTauM_M",        "HRF_KinGenTauM_p4.M()")
                .Define("HRF_KinGenTauM_E",        "HRF_KinGenTauM_p4.E()")
                .Define("HRF_KinGenTauM_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(RecoilKin_TauM_p4.Phi(), HRF_HadGenTauM_p4.Phi())")
                .Define("HRF_KinGenTauM_DEta",      "(RecoilKin_TauM_p4.Eta()-(HRF_HadGenTauM_p4).Eta())")
                .Define("HRF_KinGenTauM_DTheta",     "((RecoilKin_TauM_p4.Vect()).Angle(HRF_HadGenTauM_p4.Vect()))")

                .Define("KinGen_hMnorm_p3",       "(hMnormKin-GenhMnorm)")
                .Define("KinGen_hMnorm_Px",        "KinGen_hMnorm_p3.Px()")
                .Define("KinGen_hMnorm_Py",        "KinGen_hMnorm_p3.Py()")
                .Define("KinGen_hMnorm_Pz",        "KinGen_hMnorm_p3.Pz()")
                .Define("KinGen_hMnorm_P",        "KinGen_hMnorm_p3.Mag()")
                .Define("KinGen_hMnorm_Pt",        "KinGen_hMnorm_p3.Pt()")
                .Define("KinGen_hMnorm_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(hMnormKin.Phi(), GenhMnorm.Phi())")
                .Define("KinGen_hMnorm_DEta",      "(hMnormKin.Eta()-(GenhMnorm).Eta())")
                .Define("KinGen_hMnorm_DTheta",     "(hMnormKin.Angle(GenhMnorm))")

                .Define("KinGen_hh_norm_p3",       "(hh_normKin-Genhh_norm)")
                .Define("KinGen_hh_norm_Px",        "KinGen_hh_norm_p3.Px()")
                .Define("KinGen_hh_norm_Py",        "KinGen_hh_norm_p3.Py()")
                .Define("KinGen_hh_norm_Pz",        "KinGen_hh_norm_p3.Pz()")
                .Define("KinGen_hh_norm_P",        "KinGen_hh_norm_p3.Mag()")
                .Define("KinGen_hh_norm_Pt",        "KinGen_hh_norm_p3.Pt()")
                .Define("KinGen_hh_norm_DPhi",       "FCCAnalyses::ZHfunctions::deltaPhi(hh_normKin.Phi(), Genhh_norm.Phi())")
                .Define("KinGen_hh_norm_DEta",      "(hh_normKin.Eta()-(Genhh_norm).Eta())")
                .Define("KinGen_hh_norm_DTheta",     "(hh_normKin.Angle(Genhh_norm))")

                .Define("KinGen_CosDelta",       "(CosDeltaPhiKin-GenCosDeltaPhi)")
                .Define("KinGen_SinDelta",       "(SinDeltaPhiKin-GenSinDeltaPhi)")
                .Define("KinGen_Delta",       "(DeltaPhiKin-GenDeltaPhi)")

                ##########################

                .Define("TauP_diff",        "(RecoPiP_p4 + RecoPi0P_p4) - TauP_p4")

                .Define("Perp_check",       "if (n_ChargedHadron>0) return (ChargedHadronImpact_p4.at(0).Vect()-RecoIP_p4.Vect()).Unit().Dot(ChargedHadron_p4.at(0).Vect().Unit()); else return double(-99.)")
                .Define("Perp_check_old",       "if (n_ChargedHadron>0) return ChargedHadronImpact_p4.at(0).Vect().Unit().Dot(ChargedHadron_p4.at(0).Vect().Unit()); else return double(-99.);")
                .Define("D0IP",        "if (n_ChargedHadron>0) return FCCAnalyses::ZHfunctions::ImpactFromIP(ChargedHadronImpact_p4.at(0), ChargedHadron_p4.at(0), RecoIP_p4); else return TLorentzVector{};")
                .Define("D0IP_perp",        "if (n_ChargedHadron>0) return D0IP.Vect().Unit().Dot(ChargedHadron_p4.at(0).Vect().Unit()); else return double(-99.);")
                .Define("D0IP_IP",        "if (n_ChargedHadron>0)return (D0IP + RecoIP_p4);else return TLorentzVector{};")
                .Define("D0IP_IP_perp",        "if (n_ChargedHadron>0) return D0IP_IP.Vect().Unit().Dot(ChargedHadron_p4.at(0).Vect().Unit()); else return double(-99.);")
                .Define("D0IP_D0_perp",        "if (n_ChargedHadron>0) return D0IP.Vect().Unit().Dot(ChargedHadronImpact_p4.at(0).Vect().Unit()); else return double(-99.);")
                .Define("D0IP_D0_diff",          "if (n_ChargedHadron>0) return D0IP.Vect()-ChargedHadronImpact_p4.at(0).Vect(); else return TVector3{};")
                .Define("D0IP_D0_dphi",          "if (n_ChargedHadron>0) return FCCAnalyses::ZHfunctions::deltaPhi(D0IP.Vect().Phi(),ChargedHadronImpact_p4.at(0).Vect().Phi()); else return float(-99.);")
                .Define("XY_perp",      "if (n_ChargedHadron>0) return (ChargedHadronImpact_p4.at(0).Vect().Unit().X() * ChargedHadron_p4.at(0).Vect().Unit().X() + ChargedHadronImpact_p4.at(0).Vect().Unit().Y() * ChargedHadron_p4.at(0).Vect().Unit().Y()); else return double(-99.);")

                .Define("PiP_diff",      "if (n_ChargedHadron==2 && ChargedHadron_charge.at(0)==1) return (ChargedHadron_p4.at(0)-RecoPiP_p4); else if (n_ChargedHadron==2 && ChargedHadron_charge.at(1)==1) return (ChargedHadron_p4.at(1)-RecoPiP_p4); else return TLorentzVector(-9,-9,-9,-9);")
                .Define("PiP_diff_opp",      "if (n_ChargedHadron==2 && ChargedHadron_charge.at(0)==1) return (ChargedHadron_p4.at(1)-RecoPiP_p4); else if (n_ChargedHadron==2 && ChargedHadron_charge.at(1)==1) return (ChargedHadron_p4.at(0)-RecoPiP_p4); else return TLorentzVector(-9,-9,-9,-9);")
                .Define("PiPD0_diff",      "if (n_ChargedHadron==2 && ChargedHadron_charge.at(0)==1) return (ChargedHadronImpact_p4.at(0)-ChargedTauImpactP_p4); else if (n_ChargedHadron==2 && ChargedHadron_charge.at(1)==1) return (ChargedHadronImpact_p4.at(1)-ChargedTauImpactP_p4); else return TLorentzVector(-9,-9,-9,-9);") 


        branchList += [

            "Kin_TauP_p4", 
            "Kin_TauM_p4", 
            "Kin_chi2", 
            "Kin_NuP_p4", 
            "Kin_NuM_p4",  
            "Kin_TauNuP_DR", 
            "Kin_TauNuM_DR",
            "TauPRF_KinPiP_p4",  
            "TauPRF_KinNuP_p4",
            "TauMRF_KinPiM_p4",  
            "TauMRF_KinNuM_p4",
            "RecoilKin_TauM_p4",
            "hPnormKin", 
            "hMnormKin",
            "hh_normKin", 
            "CosDeltaPhiKin",   
            "SinDeltaPhiKin",   
            "DeltaPhiKin",  

            "KinGenTauP_p4",  
            "KinGenTauP_Px",
            "KinGenTauP_Py",
            "KinGenTauP_Pz",
            "KinGenTauP_Pt",
            "KinGenTauP_P",
            "KinGenTauP_E", 
            "KinGenTauP_M",   
            "KinGenTauP_DPhi",
            "KinGenTauP_DEta", 
            "KinGenTauP_DTheta",  

            "KinGenNuP_p4", 
            "KinGenNuP_Px",
            "KinGenNuP_Py",
            "KinGenNuP_Pz",
            "KinGenNuP_Pt",
            "KinGenNuP_P",
            "KinGenNuP_E", 
            "KinGenNuP_M",       
            "KinGenNuP_DPhi",      
            "KinGenNuP_DEta",   
            "KinGenNuP_DTheta",      

            "TauPRF_KinGenNuP_p4", 
            "TauPRF_KinGenNuP_Px",
            "TauPRF_KinGenNuP_Py",
            "TauPRF_KinGenNuP_Pz",
            "TauPRF_KinGenNuP_Pt",
            "TauPRF_KinGenNuP_P",
            "TauPRF_KinGenNuP_M",
            "TauPRF_KinGenNuP_E",      
            "TauPRF_KinGenNuP_DPhi",      
            "TauPRF_KinGenNuP_DEta",  
            "TauPRF_KinGenNuP_DTheta",       

            "TauPRF_KinGenPiP_p4", 
            "TauPRF_KinGenPiP_Px",
            "TauPRF_KinGenPiP_Py",
            "TauPRF_KinGenPiP_Pz",
            "TauPRF_KinGenPiP_P",
            "TauPRF_KinGenPiP_Pt",
            "TauPRF_KinGenPiP_M",
            "TauPRF_KinGenPiP_E",      
            "TauPRF_KinGenPiP_DPhi",       
            "TauPRF_KinGenPiP_DEta",   
            "TauPRF_KinGenPiP_DTheta",

            "KinGen_hPnorm_p3", 
            "KinGen_hPnorm_Px",
            "KinGen_hPnorm_Py",
            "KinGen_hPnorm_Pz",
            "KinGen_hPnorm_P",
            "KinGen_hPnorm_Pt",         
            "KinGen_hPnorm_DPhi",     
            "KinGen_hPnorm_DEta", 
            "KinGen_hPnorm_DTheta",     

            "KinGenTauM_p4", 
            "KinGenTauM_Px",
            "KinGenTauM_Py",
            "KinGenTauM_Pz",
            "KinGenTauM_P",
            "KinGenTauM_Pt",
            "KinGenTauM_E",
            "KinGenTauM_M",         
            "KinGenTauM_DPhi",
            "KinGenTauM_DEta", 
            "KinGenTauM_DTheta",

            "KinGenNuM_p4",
            "KinGenNuM_Px",
            "KinGenNuM_Py",
            "KinGenNuM_Pz",
            "KinGenNuM_P",
            "KinGenNuM_E",
            "KinGenNuM_M",
            "KinGenNuM_Pt",      
            "KinGenNuM_DPhi",      
            "KinGenNuM_DEta",     
            "KinGenNuM_DTheta", 

            "TauMRF_KinGenNuM_p4",    
            "TauMRF_KinGenNuM_Px",
            "TauMRF_KinGenNuM_Py",
            "TauMRF_KinGenNuM_Pz",
            "TauMRF_KinGenNuM_P",
            "TauMRF_KinGenNuM_E",
            "TauMRF_KinGenNuM_M",
            "TauMRF_KinGenNuM_Pt",
            "TauMRF_KinGenNuM_DPhi",      
            "TauMRF_KinGenNuM_DEta",      
            "TauMRF_KinGenNuM_DTheta",

            "TauMRF_KinGenPiM_p4",
            "TauMRF_KinGenPiM_Px",
            "TauMRF_KinGenPiM_Py",
            "TauMRF_KinGenPiM_Pz",
            "TauMRF_KinGenPiM_P",
            "TauMRF_KinGenPiM_Pt",
            "TauMRF_KinGenPiM_E",
            "TauMRF_KinGenPiM_M",      
            "TauMRF_KinGenPiM_DPhi",       
            "TauMRF_KinGenPiM_DEta",    
            "TauMRF_KinGenPiM_DTheta",  

            "HRF_KinGenTauM_p4", 
            "HRF_KinGenTauM_Px",
            "HRF_KinGenTauM_Py",
            "HRF_KinGenTauM_Pz",
            "HRF_KinGenTauM_Pt",
            "HRF_KinGenTauM_P",
            "HRF_KinGenTauM_E",
            "HRF_KinGenTauM_M",            
            "HRF_KinGenTauM_DPhi",       
            "HRF_KinGenTauM_DEta",   
            "HRF_KinGenTauM_DTheta",

            "KinGen_hMnorm_p3",
            "KinGen_hMnorm_Px",
            "KinGen_hMnorm_Py",
            "KinGen_hMnorm_Pz",
            "KinGen_hMnorm_P",
            "KinGen_hMnorm_Pt",      
            "KinGen_hMnorm_DPhi",     
            "KinGen_hMnorm_DEta",   
            "KinGen_hMnorm_DTheta",

            "KinGen_hh_norm_p3",      
            "KinGen_hh_norm_Px",
            "KinGen_hh_norm_Py",
            "KinGen_hh_norm_Pz",
            "KinGen_hh_norm_P",
            "KinGen_hh_norm_Pt",                              
            "KinGen_hh_norm_DPhi",     
            "KinGen_hh_norm_DEta",    
            "KinGen_hh_norm_DTheta",

            "KinGen_CosDelta",     
            "KinGen_SinDelta",    
            "KinGen_Delta",     

            "Kin_TauP_Px", "Kin_TauP_Py", "Kin_TauP_Pz", "Kin_TauP_E",
            "Kin_TauP_M", "Kin_TauP_Eta", "Kin_TauP_Phi", "Kin_TauP_P", 
            "Kin_TauP_Pt", "Kin_TauP_Theta", "Kin_TauP_Rapidity",
            
            "Kin_TauM_Px", "Kin_TauM_Py", "Kin_TauM_Pz", "Kin_TauM_E",
            "Kin_TauM_M", "Kin_TauM_Eta", "Kin_TauM_Phi", "Kin_TauM_P", 
            "Kin_TauM_Pt", "Kin_TauM_Theta", "Kin_TauM_Rapidity",

            "Kin_NuP_Px", "Kin_NuP_Py", "Kin_NuP_Pz", "Kin_NuP_E",
            "Kin_NuP_M", "Kin_NuP_Eta", "Kin_NuP_Phi", "Kin_NuP_P", 
            "Kin_NuP_Pt", "Kin_NuP_Theta", "Kin_NuP_Rapidity",

            "Kin_NuM_Px", "Kin_NuM_Py", "Kin_NuM_Pz", "Kin_NuM_E",
            "Kin_NuM_M", "Kin_NuM_Eta", "Kin_NuM_Phi", "Kin_NuM_P", 
            "Kin_NuM_Pt", "Kin_NuM_Theta", "Kin_NuM_Rapidity",

            "TauPRF_KinPiP_Px", "TauPRF_KinPiP_Py", "TauPRF_KinPiP_Pz", "TauPRF_KinPiP_E",
            "TauPRF_KinPiP_M", "TauPRF_KinPiP_Eta", "TauPRF_KinPiP_Phi", "TauPRF_KinPiP_P", 
            "TauPRF_KinPiP_Pt", "TauPRF_KinPiP_Theta", "TauPRF_KinPiP_Rapidity",

            "TauPRF_KinNuP_Px", "TauPRF_KinNuP_Py", "TauPRF_KinNuP_Pz", "TauPRF_KinNuP_E",
            "TauPRF_KinNuP_M", "TauPRF_KinNuP_Eta", "TauPRF_KinNuP_Phi", "TauPRF_KinNuP_P", 
            "TauPRF_KinNuP_Pt", "TauPRF_KinNuP_Theta", "TauPRF_KinNuP_Rapidity",

            "TauMRF_KinPiM_Px", "TauMRF_KinPiM_Py", "TauMRF_KinPiM_Pz", "TauMRF_KinPiM_E",
            "TauMRF_KinPiM_M", "TauMRF_KinPiM_Eta", "TauMRF_KinPiM_Phi", "TauMRF_KinPiM_P", 
            "TauMRF_KinPiM_Pt", "TauMRF_KinPiM_Theta", "TauMRF_KinPiM_Rapidity",

            "TauMRF_KinNuM_Px", "TauMRF_KinNuM_Py", "TauMRF_KinNuM_Pz", "TauMRF_KinNuM_E",
            "TauMRF_KinNuM_M", "TauMRF_KinNuM_Eta", "TauMRF_KinNuM_Phi", "TauMRF_KinNuM_P", 
            "TauMRF_KinNuM_Pt", "TauMRF_KinNuM_Theta", "TauMRF_KinNuM_Rapidity",

            "RecoilKin_TauM_Px", "RecoilKin_TauM_Py", "RecoilKin_TauM_Pz", "RecoilKin_TauM_E",
            "RecoilKin_TauM_M", "RecoilKin_TauM_Eta", "RecoilKin_TauM_Phi", "RecoilKin_TauM_P", 
            "RecoilKin_TauM_Pt", "RecoilKin_TauM_Theta", "RecoilKin_TauM_Rapidity",

            "hPnormKin_Px", "hPnormKin_Py", "hPnormKin_Pz", "hPnormKin_Pt", "hPnormKin_P", "hPnormKin_Phi", "hPnormKin_Eta", "hPnormKin_Theta",
            "hMnormKin_Px", "hMnormKin_Py", "hMnormKin_Pz", "hMnormKin_Pt", "hMnormKin_P", "hMnormKin_Phi", "hMnormKin_Eta", "hMnormKin_Theta",
            "hh_normKin_Px", "hh_normKin_Py", "hh_normKin_Pz", "hh_normKin_Pt", "hh_normKin_P", "hh_normKin_Phi", "hh_normKin_Eta", "hh_normKin_Theta",

        ]


                ##############################
                ######## FINAL ##############
                #############################

                "Kin_TauP_Px": {"name": "Kin_TauP_Px", "title": "P_{x}(#tau^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauP_Py": {"name": "Kin_TauP_Py", "title": "P_{y}(#tau^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauP_Pz": {"name": "Kin_TauP_Pz", "title": "P_{z}(#tau^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauP_E": {"name": "Kin_TauP_E", "title": "E(#tau^{+})", "bin": 240, "xmin": 0, "xmax": 120},
    "Kin_TauP_M": {"name": "Kin_TauP_M", "title": "M(#tau^{+})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "Kin_TauP_Eta": {"name": "Kin_TauP_Eta", "title": "#eta(#tau^{+})", "bin": 100, "xmin": -5, "xmax": 5},
    "Kin_TauP_Phi": {"name": "Kin_TauP_Phi", "title": "#phi(#tau^{+})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "Kin_TauP_P": {"name": "Kin_TauP_P", "title": "P(#tau^{+})", "bin": 200, "xmin": 0, "xmax": 120},
    "Kin_TauP_Pt": {"name": "Kin_TauP_Pt", "title": "P_{T}(#tau^{+})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_TauP_Theta": {"name": "Kin_TauP_Theta", "title": "#theta(#tau^{+})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "Kin_TauP_Rapidity": {"name": "Kin_TauP_Rapidity", "title": "y(#tau^{+})", "bin": 100, "xmin": -5, "xmax": 5},

    "Kin_TauM_Px": {"name": "Kin_TauM_Px", "title": "P_{x}(#tau^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauM_Py": {"name": "Kin_TauM_Py", "title": "P_{y}(#tau^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauM_Pz": {"name": "Kin_TauM_Pz", "title": "P_{z}(#tau^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_TauM_E": {"name": "Kin_TauM_E", "title": "E(#tau^{-})", "bin": 240, "xmin": 0, "xmax": 120},
    "Kin_TauM_M": {"name": "Kin_TauM_M", "title": "M(#tau^{-})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "Kin_TauM_Eta": {"name": "Kin_TauM_Eta", "title": "#eta(#tau^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    "Kin_TauM_Phi": {"name": "Kin_TauM_Phi", "title": "#phi(#tau^{-})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "Kin_TauM_P": {"name": "Kin_TauM_P", "title": "P(#tau^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_TauM_Pt": {"name": "Kin_TauM_Pt", "title": "P_{T}(#tau^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_TauM_Theta": {"name": "Kin_TauM_Theta", "title": "#theta(#tau^{-})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "Kin_TauM_Rapidity": {"name": "Kin_TauM_Rapidity", "title": "y(#tau^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    
    "Kin_NuP_Px": {"name": "Kin_NuP_Px", "title": "P_{x}(#nu^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuP_Py": {"name": "Kin_NuP_Py", "title": "P_{y}(#nu^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuP_Pz": {"name": "Kin_NuP_Pz", "title": "P_{z}(#nu^{+})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuP_E": {"name": "Kin_NuP_E", "title": "E(#nu^{+})", "bin": 240, "xmin": 0, "xmax": 120},
    "Kin_NuP_M": {"name": "Kin_NuP_M", "title": "M(#nu^{+})",  "bin": 100, "xmin": -0.01, "xmax": 0.01},
    "Kin_NuP_Eta": {"name": "Kin_NuP_Eta", "title": "#eta(#nu^{+})", "bin": 100, "xmin": -5, "xmax": 5},
    "Kin_NuP_Phi": {"name": "Kin_NuP_Phi", "title": "#phi(#nu^{+})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "Kin_NuP_P": {"name": "Kin_NuP_P", "title": "P(#nu^{+})", "bin": 200, "xmin": 0, "xmax": 120},
    "Kin_NuP_Pt": {"name": "Kin_NuP_Pt", "title": "P_{T}(#nu^{+})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_NuP_Theta": {"name": "Kin_NuP_Theta", "title": "#theta(#nu^{+})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "Kin_NuP_Rapidity": {"name": "Kin_NuP_Rapidity", "title": "y(#nu^{+})", "bin": 100, "xmin": -5, "xmax": 5},

    "Kin_NuM_Px": {"name": "Kin_NuM_Px", "title": "P_{x}(#nu^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuM_Py": {"name": "Kin_NuM_Py", "title": "P_{y}(#nu^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuM_Pz": {"name": "Kin_NuM_Pz", "title": "P_{z}(#nu^{-})", "bin": 240, "xmin": -120, "xmax": 120},
    "Kin_NuM_E": {"name": "Kin_NuM_E", "title": "E(#nu^{-})", "bin": 240, "xmin": 0, "xmax": 120},
    "Kin_NuM_M": {"name": "Kin_NuM_M", "title": "M(#nu^{-})",  "bin": 100, "xmin": -0.01, "xmax": 0.01},
    "Kin_NuM_Eta": {"name": "Kin_NuM_Eta", "title": "#eta(#nu^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    "Kin_NuM_Phi": {"name": "Kin_NuM_Phi", "title": "#phi(#nu^{-})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "Kin_NuM_P": {"name": "Kin_NuM_P", "title": "P(#nu^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_NuM_Pt": {"name": "Kin_NuM_Pt", "title": "P_{T}(#nu^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "Kin_NuM_Theta": {"name": "Kin_NuM_Theta", "title": "#theta(#nu^{-})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "Kin_NuM_Rapidity": {"name": "Kin_NuM_Rapidity", "title": "y(#nu^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    
    "Kin_TauNuP_DR": {"name": "Kin_TauNuP_DR", "title": "#DeltaR(#tau^{+},#nu^{+})", "bin": 50, "xmin": 0, "xmax": 5},
    "Kin_TauNuM_DR": {"name": "Kin_TauNuM_DR", "title": "#DeltaR(#tau^{-},#nu^{-})", "bin": 50, "xmin": 0, "xmax": 5},

    "TauPRF_KinPiP_Px": {"name": "TauPRF_KinPiP_Px", "title": "P_{x}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinPiP_Py": {"name": "TauPRF_KinPiP_Py", "title": "P_{y}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinPiP_Pz": {"name": "TauPRF_KinPiP_Pz", "title": "P_{z}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinPiP_E": {"name": "TauPRF_KinPiP_E", "title": "E(#pi^{+})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauPRF_KinPiP_M": {"name": "TauPRF_KinPiP_M", "title": "M(#pi^{+})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "TauPRF_KinPiP_Eta": {"name": "TauPRF_KinPiP_Eta", "title": "#eta(#pi^{+})", "bin": 100, "xmin": -5, "xmax": 5},
    "TauPRF_KinPiP_Phi": {"name": "TauPRF_KinPiP_Phi", "title": "#phi(#pi^{+})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "TauPRF_KinPiP_P": {"name": "TauPRF_KinPiP_P", "title": "P(#pi^{+})", "bin": 200, "xmin": 0, "xmax": 10},
    "TauPRF_KinPiP_Pt": {"name": "TauPRF_KinPiP_Pt", "title": "P_{T}(#pi^{+})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinPiP_Theta": {"name": "TauPRF_KinPiP_Theta", "title": "#theta(#pi^{+})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinPiP_Rapidity": {"name": "TauPRF_KinPiP_Rapidity", "title": "y(#pi^{+})", "bin": 100, "xmin": -5, "xmax": 5},

    "TauMRF_KinPiM_Px": {"name": "TauMRF_KinPiM_Px", "title": "P_{x}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinPiM_Py": {"name": "TauMRF_KinPiM_Py", "title": "P_{y}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinPiM_Pz": {"name": "TauMRF_KinPiM_Pz", "title": "P_{z}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinPiM_E": {"name": "TauMRF_KinPiM_E", "title": "E(#pi^{-})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauMRF_KinPiM_M": {"name": "TauMRF_KinPiM_M", "title": "M(#pi^{-})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "TauMRF_KinPiM_Eta": {"name": "TauMRF_KinPiM_Eta", "title": "#eta(#pi^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    "TauMRF_KinPiM_Phi": {"name": "TauMRF_KinPiM_Phi", "title": "#phi(#pi^{-})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "TauMRF_KinPiM_P": {"name": "TauMRF_KinPiM_P", "title": "P(#pi^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinPiM_Pt": {"name": "TauMRF_KinPiM_Pt", "title": "P_{T}(#pi^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinPiM_Theta": {"name": "TauMRF_KinPiM_Theta", "title": "#theta(#pi^{-})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinPiM_Rapidity": {"name": "TauMRF_KinPiM_Rapidity", "title": "y(#pi^{-})", "bin": 100, "xmin": -5, "xmax": 5},

    "TauPRF_KinNuP_Px": {"name": "TauPRF_KinNuP_Px", "title": "P_{x}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinNuP_Py": {"name": "TauPRF_KinNuP_Py", "title": "P_{y}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinNuP_Pz": {"name": "TauPRF_KinNuP_Pz", "title": "P_{z}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinNuP_E": {"name": "TauPRF_KinNuP_E", "title": "E(#nu^{+})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauPRF_KinNuP_M": {"name": "TauPRF_KinNuP_M", "title": "M(#nu^{+})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "TauPRF_KinNuP_Eta": {"name": "TauPRF_KinNuP_Eta", "title": "#eta(#nu^{+})", "bin": 100, "xmin": -5, "xmax": 5},
    "TauPRF_KinNuP_Phi": {"name": "TauPRF_KinNuP_Phi", "title": "#phi(#nu^{+})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "TauPRF_KinNuP_P": {"name": "TauPRF_KinNuP_P", "title": "P(#nu^{+})", "bin": 200, "xmin": 0, "xmax": 10},
    "TauPRF_KinNuP_Pt": {"name": "TauPRF_KinNuP_Pt", "title": "P_{T}(#nu^{+})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinNuP_Theta": {"name": "TauPRF_KinNuP_Theta", "title": "#theta(#nu^{+})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinNuP_Rapidity": {"name": "TauPRF_KinNuP_Rapidity", "title": "y(#nu^{+})", "bin": 100, "xmin": -5, "xmax": 5},

    "TauMRF_KinNuM_Px": {"name": "TauMRF_KinNuM_Px", "title": "P_{x}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinNuM_Py": {"name": "TauMRF_KinNuM_Py", "title": "P_{y}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinNuM_Pz": {"name": "TauMRF_KinNuM_Pz", "title": "P_{z}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinNuM_E": {"name": "TauMRF_KinNuM_E", "title": "E(#nu^{-})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauMRF_KinNuM_M": {"name": "TauMRF_KinNuM_M", "title": "M(#nu^{-})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "TauMRF_KinNuM_Eta": {"name": "TauMRF_KinNuM_Eta", "title": "#eta(#nu^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    "TauMRF_KinNuM_Phi": {"name": "TauMRF_KinNuM_Phi", "title": "#phi(#nu^{-})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "TauMRF_KinNuM_P": {"name": "TauMRF_KinNuM_P", "title": "P(#nu^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinNuM_Pt": {"name": "TauMRF_KinNuM_Pt", "title": "P_{T}(#nu^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinNuM_Theta": {"name": "TauMRF_KinNuM_Theta", "title": "#theta(#nu^{-})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinNuM_Rapidity": {"name": "TauMRF_KinNuM_Rapidity", "title": "y(#nu^{-})", "bin": 100, "xmin": -5, "xmax": 5},

    "RecoilKin_TauM_Px": {"name": "RecoilKin_TauM_Px", "title": "P_{x}(#tau^{-})", "bin": 140, "xmin": -70, "xmax": 70},
    "RecoilKin_TauM_Py": {"name": "RecoilKin_TauM_Py", "title": "P_{y}(#tau^{-})", "bin": 140, "xmin": -70, "xmax": 70},
    "RecoilKin_TauM_Pz": {"name": "RecoilKin_TauM_Pz", "title": "P_{z}(#tau^{-})", "bin": 140, "xmin": -70, "xmax": 70},
    "RecoilKin_TauM_E": {"name": "RecoilKin_TauM_E", "title": "E(#tau^{-})", "bin": 140, "xmin": 0, "xmax": 70},
    "RecoilKin_TauM_M": {"name": "RecoilKin_TauM_M", "title": "M(#tau^{-})", "bin": 100, "xmin": 1.5, "xmax": 2.5},
    "RecoilKin_TauM_Eta": {"name": "RecoilKin_TauM_Eta", "title": "#eta(#tau^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    "RecoilKin_TauM_Phi": {"name": "RecoilKin_TauM_Phi", "title": "#phi(#tau^{-})", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "RecoilKin_TauM_P": {"name": "RecoilKin_TauM_P", "title": "P(#tau^{-})", "bin": 140, "xmin": 0, "xmax": 70},
    "RecoilKin_TauM_Pt": {"name": "RecoilKin_TauM_Pt", "title": "P_{T}(#tau^{-})", "bin": 140, "xmin": 0, "xmax": 70},
    "RecoilKin_TauM_Theta": {"name": "RecoilKin_TauM_Theta", "title": "#theta(#tau^{-})", "bin": 100, "xmin": 0, "xmax": 3.2},
    "RecoilKin_TauM_Rapidity": {"name": "RecoilKin_TauM_Rapidity", "title": "y(#tau^{-})", "bin": 100, "xmin": -5, "xmax": 5},
    
    "hPnormKin_Px": {"name": "hPnormKin_Px", "title": "p_{x} of hPnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hPnormKin_Py": {"name": "hPnormKin_Py", "title": "p_{y} of hPnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hPnormKin_Pz": {"name": "hPnormKin_Pz", "title": "p_{z} of hPnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hPnormKin_P": {"name": "hPnormKin_P", "title": "p of hPnormKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hPnormKin_Pt": {"name": "hPnormKin_Pt", "title": "p_{T} of hPnormKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hPnormKin_Eta": {"name": "hPnormKin_Eta", "title": "#eta of hPnormKin", "bin": 100, "xmin": -5, "xmax": 5},
    "hPnormKin_Phi": {"name": "hPnormKin_Phi", "title": "#phi of hPnormKin", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "hPnormKin_Theta": {"name": "hPnormKin_Theta", "title": "#theta of hPnormKin", "bin": 100, "xmin": 0, "xmax": 3.2},

    "hMnormKin_Px": {"name": "hMnormKin_Px", "title": "p_{x} of hMnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hMnormKin_Py": {"name": "hMnormKin_Py", "title": "p_{y} of hMnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hMnormKin_Pz": {"name": "hMnormKin_Pz", "title": "p_{z} of hMnormKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hMnormKin_P": {"name": "hMnormKin_P", "title": "p of hMnormKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hMnormKin_Pt": {"name": "hMnormKin_Pt", "title": "p_{T} of hMnormKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hMnormKin_Eta": {"name": "hMnormKin_Eta", "title": "#eta of hMnormKin", "bin": 100, "xmin": -5, "xmax": 5},
    "hMnormKin_Phi": {"name": "hMnormKin_Phi", "title": "#phi of hMnormKin", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "hMnormKin_Theta": {"name": "hMnormKin_Theta", "title": "#theta of hMnormKin", "bin": 100, "xmin": 0, "xmax": 3.2},
    
    "hh_normKin_Px": {"name": "hh_normKin_Px", "title": "p_{x} of hh_normKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hh_normKin_Py": {"name": "hh_normKin_Py", "title": "p_{y} of hh_normKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hh_normKin_Pz": {"name": "hh_normKin_Pz", "title": "p_{z} of hh_normKin", "bin": 50, "xmin": -1, "xmax": 1},
    "hh_normKin_P": {"name": "hh_normKin_P", "title": "p of hh_normKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hh_normKin_Pt": {"name": "hh_normKin_Pt", "title": "p_{T} of hh_normKin", "bin": 25, "xmin": 0, "xmax": 1},
    "hh_normKin_Eta": {"name": "hh_normKin_Eta", "title": "#eta of hh_normKin", "bin": 100, "xmin": -5, "xmax": 5},
    "hh_normKin_Phi": {"name": "hh_normKin_Phi", "title": "#phi of hh_normKin", "bin": 200, "xmin": -3.2, "xmax": 3.2},
    "hh_normKin_Theta": {"name": "hh_normKin_Theta", "title": "#theta of hh_normKin", "bin": 100, "xmin": 0, "xmax": 3.2},
    
    "CosDeltaPhiKin": {"name": "CosDeltaPhiKin", "title": "cos(#Delta#phi_{CP}) Kin", "bin": 50, "xmin": -1, "xmax": 1},
    "SinDeltaPhiKin": {"name": "SinDeltaPhiKin", "title": "sin(#Delta#phi_{CP}) Kin", "bin": 50, "xmin": -1, "xmax": 1},
    "DeltaPhiKin":                             {"name":"DeltaPhiKin",           "title":"#Delta#Phi_{CP} Kin",                  "bin":64, "xmin":-3.14,"xmax":3.14},

    "GenCosDeltaPhi": {"name": "GenCosDeltaPhi", "title": "Reco cos(#Delta#phi_{CP})", "bin": 50, "xmin": -1, "xmax": 1},
    "GenSinDeltaPhi": {"name": "GenSinDeltaPhi", "title": "Reco sin(#Delta#phi_{CP})", "bin": 50, "xmin": -1, "xmax": 1},
    "GenDeltaPhi":                             {"name":"GenDeltaPhi",           "title":"Reco #Delta#Phi_{CP}",                  "bin":64, "xmin":-3.14,"xmax":3.14},

    "KinGenTauP_Px": {"name": "KinGenTauP_Px", "title": "P_{x}(#tau^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauP_Py": {"name": "KinGenTauP_Py", "title": "P_{y}(#tau^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauP_Pz": {"name": "KinGenTauP_Pz", "title": "P_{z}(#tau^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauP_E": {"name": "KinGenTauP_E", "title": "E(#tau^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauP_M": {"name": "KinGenTauP_M", "title": "M(#tau^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauP_DEta": {"name": "KinGenTauP_DEta", "title": "#eta(#tau^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenTauP_DPhi": {"name": "KinGenTauP_DPhi", "title": "#phi(#tau^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenTauP_P": {"name": "KinGenTauP_P", "title": "P(#tau^{+})", "bin": 200, "xmin": 0, "xmax": 120},
    "KinGenTauP_Pt": {"name": "KinGenTauP_Pt", "title": "P_{T}(#tau^{+})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenTauP_DTheta": {"name": "KinGenTauP_DTheta", "title": "#theta(#tau^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "KinGenTauM_Px": {"name": "KinGenTauM_Px", "title": "P_{x}(#tau^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauM_Py": {"name": "KinGenTauM_Py", "title": "P_{y}(#tau^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauM_Pz": {"name": "KinGenTauM_Pz", "title": "P_{z}(#tau^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauM_E": {"name": "KinGenTauM_E", "title": "E(#tau^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauM_M": {"name": "KinGenTauM_M", "title": "M(#tau^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenTauM_DEta": {"name": "KinGenTauM_DEta", "title": "#eta(#tau^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenTauM_DPhi": {"name": "KinGenTauM_DPhi", "title": "#phi(#tau^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenTauM_P": {"name": "KinGenTauM_P", "title": "P(#tau^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenTauM_Pt": {"name": "KinGenTauM_Pt", "title": "P_{T}(#tau^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenTauM_DTheta": {"name": "KinGenTauM_DTheta", "title": "#theta(#tau^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    
    "KinGenNuP_Px": {"name": "KinGenNuP_Px", "title": "P_{x}(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuP_Py": {"name": "KinGenNuP_Py", "title": "P_{y}(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuP_Pz": {"name": "KinGenNuP_Pz", "title": "P_{z}(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuP_E": {"name": "KinGenNuP_E", "title": "E(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuP_M": {"name": "KinGenNuP_M", "title": "M(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuP_DEta": {"name": "KinGenNuP_DEta", "title": "#eta(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenNuP_DPhi": {"name": "KinGenNuP_DPhi", "title": "#phi(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenNuP_P": {"name": "KinGenNuP_P", "title": "P(#nu^{+})", "bin": 200, "xmin": 0, "xmax": 120},
    "KinGenNuP_Pt": {"name": "KinGenNuP_Pt", "title": "P_{T}(#nu^{+})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenNuP_DTheta": {"name": "KinGenNuP_DTheta", "title": "#theta(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "KinGenNuM_Px": {"name": "KinGenNuM_Px", "title": "P_{x}(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuM_Py": {"name": "KinGenNuM_Py", "title": "P_{y}(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuM_Pz": {"name": "KinGenNuM_Pz", "title": "P_{z}(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuM_E": {"name": "KinGenNuM_E", "title": "E(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuM_M": {"name": "KinGenNuM_M", "title": "M(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGenNuM_DEta": {"name": "KinGenNuM_DEta", "title": "#eta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenNuM_DPhi": {"name": "KinGenNuM_DPhi", "title": "#phi(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "KinGenNuM_P": {"name": "KinGenNuM_P", "title": "P(#nu^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenNuM_Pt": {"name": "KinGenNuM_Pt", "title": "P_{T}(#nu^{-})", "bin": 120, "xmin": 0, "xmax": 120},
    "KinGenNuM_DTheta": {"name": "KinGenNuM_DTheta", "title": "#theta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "TauPRF_KinGenPiP_Px": {"name": "TauPRF_KinGenPiP_Px", "title": "P_{x}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_Py": {"name": "TauPRF_KinGenPiP_Py", "title": "P_{y}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_Pz": {"name": "TauPRF_KinGenPiP_Pz", "title": "P_{z}(#pi^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_E": {"name": "TauPRF_KinGenPiP_E", "title": "E(#pi^{+})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauPRF_KinGenPiP_M": {"name": "TauPRF_KinGenPiP_M", "title": "M(#pi^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_DEta": {"name": "TauPRF_KinGenPiP_DEta", "title": "#eta(#pi^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinGenPiP_DPhi": {"name": "TauPRF_KinGenPiP_DPhi", "title": "#phi(#pi^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinGenPiP_P": {"name": "TauPRF_KinGenPiP_P", "title": "P(#pi^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_Pt": {"name": "TauPRF_KinGenPiP_Pt", "title": "P_{T}(#pi^{+})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenPiP_DTheta": {"name": "TauPRF_KinGenPiP_DTheta", "title": "#theta(#pi^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "TauMRF_KinGenPiM_Px": {"name": "TauMRF_KinGenPiM_Px", "title": "P_{x}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_Py": {"name": "TauMRF_KinGenPiM_Py", "title": "P_{y}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_Pz": {"name": "TauMRF_KinGenPiM_Pz", "title": "P_{z}(#pi^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_E": {"name": "TauMRF_KinGenPiM_E", "title": "E(#pi^{-})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauMRF_KinGenPiM_M": {"name": "TauMRF_KinGenPiM_M", "title": "M(#pi^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_DEta": {"name": "TauMRF_KinGenPiM_DEta", "title": "#eta(#pi^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinGenPiM_DPhi": {"name": "TauMRF_KinGenPiM_DPhi", "title": "#phi(#pi^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinGenPiM_P": {"name": "TauMRF_KinGenPiM_P", "title": "P(#pi^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_Pt": {"name": "TauMRF_KinGenPiM_Pt", "title": "P_{T}(#pi^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenPiM_DTheta": {"name": "TauMRF_KinGenPiM_DTheta", "title": "#theta(#pi^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "TauPRF_KinGenNuP_Px": {"name": "TauPRF_KinGenNuP_Px", "title": "P_{x}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_Py": {"name": "TauPRF_KinGenNuP_Py", "title": "P_{y}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_Pz": {"name": "TauPRF_KinGenNuP_Pz", "title": "P_{z}(#nu^{+})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_E": {"name": "TauPRF_KinGenNuP_E", "title": "E(#nu^{+})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauPRF_KinGenNuP_M": {"name": "TauPRF_KinGenNuP_M", "title": "M(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_DEta": {"name": "TauPRF_KinGenNuP_DEta", "title": "#eta(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinGenNuP_DPhi": {"name": "TauPRF_KinGenNuP_DPhi", "title": "#phi(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauPRF_KinGenNuP_P": {"name": "TauPRF_KinGenNuP_P", "title": "P(#nu^{+})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_Pt": {"name": "TauPRF_KinGenNuP_Pt", "title": "P_{T}(#nu^{+})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauPRF_KinGenNuP_DTheta": {"name": "TauPRF_KinGenNuP_DTheta", "title": "#theta(#nu^{+})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "TauMRF_KinGenNuM_Px": {"name": "TauMRF_KinGenNuM_Px", "title": "P_{x}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_Py": {"name": "TauMRF_KinGenNuM_Py", "title": "P_{y}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_Pz": {"name": "TauMRF_KinGenNuM_Pz", "title": "P_{z}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_E": {"name": "TauMRF_KinGenNuM_E", "title": "E(#nu^{-})", "bin": 100, "xmin": 0, "xmax": 10},
    "TauMRF_KinGenNuM_M": {"name": "TauMRF_KinGenNuM_M", "title": "M(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_DEta": {"name": "TauMRF_KinGenNuM_DEta", "title": "#eta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinGenNuM_DPhi": {"name": "TauMRF_KinGenNuM_DPhi", "title": "#phi(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "TauMRF_KinGenNuM_P": {"name": "TauMRF_KinGenNuM_P", "title": "P(#nu^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_Pt": {"name": "TauMRF_KinGenNuM_Pt", "title": "P_{T}(#nu^{-})",  "bin": 100, "xmin": -10, "xmax": 10},
    "TauMRF_KinGenNuM_DTheta": {"name": "TauMRF_KinGenNuM_DTheta", "title": "#theta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "HRF_KinGenTauM_Px": {"name": "HRF_KinGenTauM_Px", "title": "P_{x}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_Py": {"name": "HRF_KinGenTauM_Py", "title": "P_{y}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_Pz": {"name": "HRF_KinGenTauM_Pz", "title": "P_{z}(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_E": {"name": "HRF_KinGenTauM_E", "title": "E(#nu^{-})", "bin": 100, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_M": {"name": "HRF_KinGenTauM_M", "title": "M(#nu^{-})", "bin": 50, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_DEta": {"name": "HRF_KinGenTauM_DEta", "title": "#eta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "HRF_KinGenTauM_DPhi": {"name": "HRF_KinGenTauM_DPhi", "title": "#phi(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},
    "HRF_KinGenTauM_P": {"name": "HRF_KinGenTauM_P", "title": "P(#nu^{-})", "bin": 10, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_Pt": {"name": "HRF_KinGenTauM_Pt", "title": "P_{T}(#nu^{-})", "bin": 10, "xmin": -10, "xmax": 10},
    "HRF_KinGenTauM_DTheta": {"name": "HRF_KinGenTauM_DTheta", "title": "#theta(#nu^{-})", "bin": 50, "xmin": 0, "xmax": 3.2},

    "KinGen_hPnorm_Px": {"name": "KinGen_hPnorm_Px", "title": "p_{x} of hPnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hPnorm_Py": {"name": "KinGen_hPnorm_Py", "title": "p_{y} of hPnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hPnorm_Pz": {"name": "KinGen_hPnorm_Pz", "title": "p_{z} of hPnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hPnorm_P": {"name": "KinGen_hPnorm_P", "title": "p of hPnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hPnorm_Pt": {"name": "KinGen_hPnorm_Pt", "title": "p_{T} of hPnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hPnorm_DEta": {"name": "KinGen_hPnorm_DEta", "title": "#eta of hPnorm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hPnorm_DPhi": {"name": "KinGen_hPnorm_DPhi", "title": "#phi of hPnorm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hPnorm_DTheta": {"name": "KinGen_hPnorm_DTheta", "title": "#theta of hPnorm", "bin": 50, "xmin":0, "xmax": 3.2},

    "KinGen_hMnorm_Px": {"name": "KinGen_hMnorm_Px", "title": "p_{x} of hMnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hMnorm_Py": {"name": "KinGen_hMnorm_Py", "title": "p_{y} of hMnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hMnorm_Pz": {"name": "KinGen_hMnorm_Pz", "title": "p_{z} of hMnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hMnorm_P": {"name": "KinGen_hMnorm_P", "title": "p of hMnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hMnorm_Pt": {"name": "KinGen_hMnorm_Pt", "title": "p_{T} of hMnorm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hMnorm_DEta": {"name": "KinGen_hMnorm_DEta", "title": "#eta of hMnorm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hMnorm_DPhi": {"name": "KinGen_hMnorm_DPhi", "title": "#phi of hMnorm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hMnorm_DTheta": {"name": "KinGen_hMnorm_DTheta", "title": "#theta of hMnorm", "bin": 50, "xmin":0, "xmax": 3.2},
    
    "KinGen_hh_norm_Px": {"name": "KinGen_hh_norm_Px", "title": "p_{x} of hh_norm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hh_norm_Py": {"name": "KinGen_hh_norm_Py", "title": "p_{y} of hh_norm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hh_norm_Pz": {"name": "KinGen_hh_norm_Pz", "title": "p_{z} of hh_norm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hh_norm_P": {"name": "KinGen_hh_norm_P", "title": "p of hh_norm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hh_norm_Pt": {"name": "KinGen_hh_norm_Pt", "title": "p_{T} of hh_norm", "bin": 50, "xmin": -10, "xmax": 10},
    "KinGen_hh_norm_DEta": {"name": "KinGen_hh_norm_DEta", "title": "#eta of hh_norm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hh_norm_DPhi": {"name": "KinGen_hh_norm_DPhi", "title": "#phi of hh_norm", "bin": 50, "xmin":0, "xmax": 3.2},
    "KinGen_hh_norm_DTheta": {"name": "KinGen_hh_norm_DTheta", "title": "#theta of hh_norm", "bin": 50, "xmin":0, "xmax": 3.2},


    "KinGen_CosDelta": {"name": "KinGen_CosDelta", "title": "cos(#Delta#phi_{CP}) Kin", "bin": 50, "xmin": -2, "xmax": 2},
    "KinGen_SinDelta": {"name": "KinGen_SinDelta", "title": "sin(#Delta#phi_{CP}) Kin", "bin": 50, "xmin": -2, "xmax": 2},
    "KinGen_Delta":                             {"name":"KinGen_Delta",           "title":"#Delta#Phi_{CP} Kin",                  "bin":64, "xmin":-6.28,"xmax":6.28},


                #############################
                ####### FUNCTIONS  ##########
                #############################

// Chi-squared function on event kinematics and tau mass to be minimized, does not handle two fold ambiguity of the tau system
class Chi2Function : public ROOT::Minuit2::FCNBase {
public:
    Chi2Function(const TLorentzVector& Pi_plus, const TLorentzVector& Pi_minus, const TLorentzVector& EMiss)
        : Pi_plus_(Pi_plus), Pi_minus_(Pi_minus), EMiss_(EMiss) {}

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

        // Total chi-squared
        return chi2_mass + chi2_met;
    }

    // Minuit2 interface to call the chi2 function
    virtual double Up() const { return 0.0; }  // Returns the unweighted function
    virtual double operator()(const double *xx) const { return operator()(std::vector<double>(xx, xx + 6)); }

private:
    TLorentzVector Pi_plus_;
    TLorentzVector Pi_minus_;
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

ROOT::VecOps::RVec<TLorentzVector> build_nu_kin(const TLorentzVector& EMiss,
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
    Chi2Function chi2Function(Pi_plus, Pi_minus, EMiss);
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

    double fval = minimizer.MinValue();
    
    TLorentzVector Tau_plus_fit = Nu_plus_fit + Pi_plus;
    TLorentzVector Tau_minus_fit = Nu_minus_fit + Pi_minus;
    TLorentzVector chi;
    chi.SetPxPyPzE(fval, 0, 0, 0);

    result.push_back(Tau_plus_fit);
    result.push_back(Tau_minus_fit);
    result.push_back(chi);
    
    return result;
}


ROOT::VecOps::RVec<TLorentzVector> build_tau_p4 (TLorentzVector Recoil, TLorentzVector EMiss, ROOT::VecOps::RVec<TLorentzVector> Tau_vis, ROOT::VecOps::RVec<float> charge){
    
    //following Belle reconstruction https://arxiv.org/pdf/1310.8503
    // first of all, build the visible taus from pi and pi0 with either jet tagger or the explciit reconstruction
    // both should be built from the same jets so keeping the order as it is reuslts in the two taus which will be identified later by the charge of the pi
    // does handles the two fold ambiguity but the tau have mostly 5 gev more enrgy than they should
    // could be "fixed" by considering the decay lenght if then the solution picked is best, similar as what we're doing with the ILC method but at that point that's a better method
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
        //std::cerr << "Error: Invalid values encountered while solving the quadratic equation." << std::endl;
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

// version with decay lenght consideration at la ILC, somehow it works even worst than without

ROOT::VecOps::RVec<TLorentzVector> build_tau_p4 (TLorentzVector Recoil, TLorentzVector EMiss, ROOT::VecOps::RVec<TLorentzVector> Tau_vis, ROOT::VecOps::RVec<TLorentzVector> Impact_p4, TLorentzVector IP){
    
    //following Belle reconstruction https://arxiv.org/pdf/1310.8503
    // first of all, build the visible taus from pi and pi0 with either jet tagger or the explciit reconstruction
    // both should be built from the same jets so keeping the order as it is reuslts in the two taus which will be identified later by the charge of the pi
    // does handles the two fold ambiguity but the tau have mostly 5 gev more enrgy than they should
    // could be "fixed" by considering the decay lenght if then the solution picked is best, similar as what we're doing with the ILC method but at that point that's a better method
    ROOT::VecOps::RVec<TLorentzVector> result;
    TLorentzVector temp1;
    TLorentzVector temp2;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H_temp;
    ROOT::VecOps::RVec<TLorentzVector> Tau_vis_H;
    // final vectors to store based on decay lenght arguments
    TLorentzVector TauP_p4, TauM_p4, TauP_nu_p4, TauM_nu_p4;
    double DL_M, DL_P, LambdaM_1_, LambdaM_2_, LambdaP_1_, LambdaP_2_;

    double E_tau = Recoil.E()/2; //energy of the single taus in the higgs rest frame

    for (size_t i = 0; i < Tau_vis.size(); ++i) {

        // boost the visible taus to the recoil frame / "true" higgs rest frame
        // assumes that the first elememnt is the plus and second is minus
        TLorentzVector boostedTau = Tau_vis[i]; 
        boostedTau.Boost(-Recoil.BoostVector()); 
        Tau_vis_H.push_back(boostedTau);
    }

    TLorentzVector TauP_d_p4 = Impact_p4[0];
    TLorentzVector TauM_d_p4 = Impact_p4[1];
    
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
        //std::cerr << "Error: Invalid values encountered while solving the quadratic equation." << std::endl;
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
    TLorentzVector TauP1_p4;
    TauP1_p4.SetPxPyPzE(P_tau * x1, P_tau * y1, P_tau * z1, E_tau);
    TLorentzVector TauP2_p4;
    TauP2_p4.SetPxPyPzE(P_tau * x2, P_tau * y2, P_tau * z2, E_tau);
    TLorentzVector TauM1_p4;
    TauM1_p4.SetPxPyPzE(-P_tau * x1, -P_tau * y1, -P_tau * z1, E_tau);
    TLorentzVector TauM2_p4;
    TauM2_p4.SetPxPyPzE(-P_tau * x2, -P_tau * y2, -P_tau * z2, E_tau);

    if (discriminant > 0) {

        // boost back the solutions to figure out the best one against the recoil frame
        TauP1_p4.Boost( Recoil.BoostVector());
        TauP2_p4.Boost( Recoil.BoostVector());
        TauM1_p4.Boost( Recoil.BoostVector());
        TauM2_p4.Boost( Recoil.BoostVector());

        TLorentzVector TauP_p_p4 = Tau_vis[0];
        TLorentzVector TauM_p_p4 = Tau_vis[1];

        TVector3 TauP_p_dir = (TauP_p_p4.Vect()).Unit();
        TVector3 TauP_p_pt = TauP_d_p4.Vect(); 

        TVector3 TauP1_dir = (TauP1_p4.Vect()).Unit();
        TVector3 TauP2_dir = (TauP2_p4.Vect()).Unit();
    
        TVector3 intP_1 = findIntersection(TauP_p_pt, TauP_p_dir, IP.Vect(), TauP1_dir);
        TVector3 intP_2 = findIntersection(TauP_p_pt, TauP_p_dir, IP.Vect(), TauP2_dir);

        TVector3 IP_intP_1 = intP_1 - IP.Vect();
        TVector3 IP_intP_2 = intP_2 - IP.Vect();

        double TauP1_L = IP_intP_1.Mag();
        double TauP2_L = IP_intP_2.Mag();
        
        double dotP_1 = TauP1_dir.Dot((IP_intP_1).Unit());
        double dotP_2 = TauP2_dir.Dot((IP_intP_2).Unit());

        double LambdaP_1 = 0, LambdaP_2 = 0;

        if (dotP_1>0) LambdaP_1 = std::exp(- TauP1_L / ( TauP1_p4.Beta() * TauP1_p4.Gamma() * 87.0 * 1e-3)); 
        if (dotP_2>0) LambdaP_2 = std::exp(- TauP2_L / ( TauP2_p4.Beta() * TauP2_p4.Gamma() * 87.0 * 1e-3));

        TVector3 TauM_p_dir = (TauM_p_p4.Vect()).Unit();
        TVector3 TauM_p_pt = TauM_d_p4.Vect();

        TVector3 TauM1_dir = (TauM1_p4.Vect()).Unit();
        TVector3 TauM2_dir = (TauM2_p4.Vect()).Unit();
    
        TVector3 intM_1 = findIntersection(TauM_p_pt, TauM_p_dir, IP.Vect(), TauM1_dir);
        TVector3 intM_2 = findIntersection(TauM_p_pt, TauM_p_dir, IP.Vect(), TauM2_dir);

        TVector3 IP_intM_1 = intM_1 - IP.Vect();
        TVector3 IP_intM_2 = intM_2 - IP.Vect();

        double TauM1_L = IP_intM_1.Mag();
        double TauM2_L = IP_intM_2.Mag();

        double dotM_1 = TauM1_dir.Dot((IP_intM_1).Unit());
        double dotM_2 = TauM2_dir.Dot((IP_intM_2).Unit());

        double LambdaM_1 = 0, LambdaM_2 = 0;

        if (dotM_1>0) LambdaM_1 = std::exp(- TauM1_L / ( TauM1_p4.Beta() * TauM1_p4.Gamma() * 87.0 * 1e-3));
        if (dotM_2>0) LambdaM_2 = std::exp(- TauM2_L / ( TauM2_p4.Beta() * TauM2_p4.Gamma() * 87.0 * 1e-3));

        if (LambdaP_1>LambdaP_2) {
            TauP_p4 = TauP1_p4;
            DL_P = TauP1_L;
            if (LambdaM_1>LambdaM_2) {
                TauM_p4 = TauM1_p4;
                DL_M = TauM1_L;
            }
            else if (LambdaM_2>LambdaM_1) {
                TauM_p4 = TauM2_p4;
                DL_M = TauM2_L;
            }
            else {
                double mH_1 = std::abs((TauP_p4 + TauM1_p4).M() - Recoil.M());
                double mH_2 = std::abs((TauP_p4 + TauM2_p4).M() - Recoil.M());

                if (mH_1<mH_2) {
                    TauM_p4 = TauM1_p4;
                    DL_M = TauM1_L;
                }
                else {
                    TauM_p4 = TauM2_p4;
                    DL_M = TauM2_L;
                }
            }   
        }
        else if (LambdaP_2>LambdaP_1) {
            TauP_p4 = TauP2_p4;
            DL_P = TauP2_L;

            if (LambdaM_1>LambdaM_2) {
                TauM_p4 = TauM1_p4;
                DL_M = TauM1_L;
            }
            else if (LambdaM_2>LambdaM_1) {
                TauM_p4 = TauM2_p4;
                DL_M = TauM2_L;
            }
            else {
                double mH_1 = std::abs((TauP_p4 + TauM1_p4).M() - Recoil.M());
                double mH_2 = std::abs((TauP_p4 + TauM2_p4).M() - Recoil.M());

                if (mH_1<mH_2) {
                    TauM_p4 = TauM1_p4;
                    DL_M = TauM1_L;
                }
                else {
                    TauM_p4 = TauM2_p4;
                    DL_M = TauM2_L;
                }
            }   
        }
        else {
            if (LambdaM_1>LambdaM_2) {
                TauM_p4 = TauM1_p4;
                DL_M = TauM1_L;

                double mH_1 = std::abs((TauM_p4 + TauP1_p4).M() - Recoil.M());
                double mH_2 = std::abs((TauM_p4 + TauP2_p4).M() - Recoil.M());

                if (mH_1<mH_2) {
                    TauP_p4 = TauP1_p4;
                    DL_P = TauP1_L;
                }
                else {
                    TauP_p4 = TauP2_p4;
                    DL_P = TauP2_L;
                }
            }
            else if (LambdaM_2>LambdaM_1) {
                TauM_p4 = TauM2_p4;
                DL_M = TauM2_L;

                double mH_1 = std::abs((TauM_p4 + TauP1_p4).M() - Recoil.M());
                double mH_2 = std::abs((TauM_p4 + TauP2_p4).M() - Recoil.M());

                if (mH_1<mH_2) {
                    TauP_p4 = TauP1_p4;
                    DL_P = TauP1_L;
                }
                else {
                    TauP_p4 = TauP2_p4;
                    DL_P = TauP2_L;
                }
            }
            else {
                //compare the di-tau invariant mass with the recoil
                double mH_11 = std::abs((TauP1_p4 + TauM1_p4).M() - Recoil.M());
                double mH_12 = std::abs((TauP1_p4 + TauM2_p4).M() - Recoil.M());
                double mH_21 = std::abs((TauP2_p4 + TauM1_p4).M() - Recoil.M());
                double mH_22 = std::abs((TauP2_p4 + TauM2_p4).M() - Recoil.M());

                std::vector<std::tuple<double, TLorentzVector, double, TLorentzVector, double>> configs = {
                    {mH_11, TauP1_p4, TauP1_L, TauM1_p4, TauM1_L},
                    {mH_12, TauP1_p4, TauP1_L, TauM2_p4, TauM2_L},
                    {mH_21, TauP2_p4, TauP2_L, TauM1_p4, TauM1_L},
                    {mH_22, TauP2_p4, TauP2_L, TauM2_p4, TauM2_L},
                };

                // Find the tuple with the minimum mH value
                auto min_config = *std::min_element(
                    configs.begin(), configs.end(),
                    [](const auto& a, const auto& b) { return std::get<0>(a) < std::get<0>(b); });

                TauP_p4 = std::get<1>(min_config);
                DL_P = std::get<2>(min_config);
                TauM_p4 = std::get<3>(min_config);
                DL_M = std::get<4>(min_config);
            }
        }

        if ((LambdaP_1>0 || LambdaP_2>0) && (LambdaM_1>0 || LambdaM_2>0)) {
            result.push_back(TauP_p4);
            result.push_back(TauM_p4);   
        }
        else {
            result.push_back(temp1);
            result.push_back(temp2);
        }

    }

    return result;
}