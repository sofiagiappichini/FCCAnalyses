Random:setSeed = on
Main:timesAllowErrors = 10
Main:numberOfEvents = 1000000

Next:numberCount = 10000             ! print message every n events
!Beams:idA = 11                     ! first beam, e+ = 11
!Beams:idB = -11                    ! second beam, e- = -11

Beams:frameType = 4
Beams:LHEF = unweighted_events.lhe

! Beams:allowMomentumSpread  = off

Beams:allowVertexSpread = on
Beams:sigmaVertexX = 5.96E-3
Beams:sigmaVertexY = 23.8E-6
Beams:sigmaVertexZ = 0.397
Beams:sigmaTime = 10.89    !  36.3 ps

PartonLevel:ISR = on
PartonLevel:FSR = on

LesHouches:setLifetime = 2