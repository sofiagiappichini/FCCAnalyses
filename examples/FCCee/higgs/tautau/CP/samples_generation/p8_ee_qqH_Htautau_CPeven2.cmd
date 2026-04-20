! card adapted from winter23 ww_tautau
Random:setSeed = on
Random:seed = 3
Main:numberOfEvents = 500000         ! number of events to generate
Main:timesAllowErrors = 1000          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 10000             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0          ! print event record n times

Beams:idA = 11                   ! first beam, e+ = 11
Beams:idB = -11                   ! second beam, e- = -11

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 2.73e-2   !  27.3 mum
Beams:sigmaVertexY = 48.8E-6   !  48.8 nm
Beams:sigmaVertexZ = 1.33      !  1.33 mm

! 3) Hard process
Beams:eCM = 240  ! CM energy of collision
HiggsSM:ffbar2HZ = on !ZH events

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! no initial-state radiation
PartonLevel:FSR = on               ! no final-state radiation

23:onMode    = off                 ! switch off Z boson decays
23:onIfAny   = 1 2                  ! switch on Z boson decay to quarks

25:onMode    = off                 ! switch off H boson decays
25:onIfAny   = 15                  ! switch on H boson decay to taus

15:onMode    = off                 ! switch off tau boson decays
15:onIfMatch   = 211 16                 ! switch on tau boson decay to single pion only
15:onIfMatch   = 211 111 16                 ! switch on tau boson decay to single pion and neutral pion
15:onIfMatch   = 211 111 111 16                 ! switch on tau boson decay to single pion and two neutral pion
15:onIfMatch   = 211 211 211 16                 ! switch on tau boson decay to three pion 
15:onIfAny   = 13                 ! switch on tau boson decay to muon
15:onIfAny   = 11                 ! switch on tau boson decay to electron
! onIfAll allows more particles to be present
! onIfAny selects all decays where at least one of the particles is present
! onIfMatch selects the specific decay channel, all particles in the list need to match the decay, other particles are not allowed

! Higgs CP parity setting
HiggsH1:parity = 1
HiggsH2:parity = 1
HiggsA3:parity = 1
! 1 for even, 2 for odd