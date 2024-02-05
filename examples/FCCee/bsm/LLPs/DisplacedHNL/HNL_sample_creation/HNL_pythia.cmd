! File: HNL_pythia.cmd
Random:setSeed = on
Main:timesAllowErrors = 10         ! how many aborts before run stops
Main:numberOfEvents = 50000         ! number of events to generate


! 2) Settings related to output in init(), next() and stat().
Next:numberCount = 100             ! print message every n events
!Beams:idA = 11                     ! first beam, e+ = 11
!Beams:idB = -11                    ! second beam, e- = -11

Beams:frameType = 4                ! read info from a LHEF
! Change the LHE file here
Beams:LHEF = HNL_eenu_50GeV_1p41e-6Ve.lhe
! Beams:LHEF = HNL_ejj_50GeV_1p41e-6Ve.lhe

! 3) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

LesHouches:setLifetime = 2
