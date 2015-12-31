import FWCore.ParameterSet.Config as cms

KinematicVariables = cms.PSet(
    pt  = cms.string("pt"),
    p   = cms.string("p"),
    eta = cms.string("eta"),
    phi = cms.string("phi"),
    abseta = cms.string("abs(eta)"),
    charge = cms.string("charge")
)
IsolationVariables = cms.PSet(
    tkIso  = cms.string("isolationR03.sumPt"),
    combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
)
MuonIDVariables = cms.PSet(
    caloCompatibility = cms.string("? isCaloCompatibilityValid ? caloCompatibility : -1"),
    numberOfMatches   = cms.string("? isMatchesValid ? numberOfMatches : -1"),
    numberOfMatchedStations = cms.string("? isMatchesValid ? numberOfMatchedStations : -1"),
)
TrackQualityVariables = cms.PSet(
    dB          = cms.string("dB"),
    tkValidHits = cms.string("? track.isNull ? 0 : track.numberOfValidHits"),
    tkHit       = cms.string("? track.isNull ? 0 : track.hitPattern.trackerLayersWithMeasurement"),
    tk3DHits    = cms.string("? track.isNull ? 0 : track.hitPattern.pixelLayersWithMeasurement + track.hitPattern.numberOfValidStripLayersWithMonoAndStereo"),
    tkpt        = cms.string("? track.isNull ? 0 : track.pt"),
    tketa       = cms.string("? track.isNull ? 0 : track.eta"),
    tktip       = cms.string("? track.isNull ? 0 : track.dxy"),
    tklip       = cms.string("? track.isNull ? 0 : track.dsz"),
    tkChi2      = cms.string("? track.isNull ? 0 : track.normalizedChi2"),
    tkPixelLay  = cms.string("? track.isNull ? 0 : track.hitPattern.pixelLayersWithMeasurement"),
    tkExpHitIn  = cms.string("? track.isNull ? 0 : track.trackerExpectedHitsInner.numberOfLostHits"),
    tkExpHitOut = cms.string("? track.isNull ? 0 : track.trackerExpectedHitsOuter.numberOfLostHits"),
    tkHitFract  = cms.string("? track.isNull ? 0 : track.hitPattern.numberOfValidHits/(track.hitPattern.numberOfValidHits+track.hitPattern.numberOfLostHits+track.trackerExpectedHitsInner.numberOfLostHits+track.trackerExpectedHitsOuter.numberOfLostHits)"),
    tkIPSig = cms.string("? track.isNull ? 0 : abs(track.dxy)/abs(track.dxyError)"),
)

L1Variables = cms.PSet(
    l1pt = cms.string("? userCand('muonL1Info').isNull ? 0 : userCand('muonL1Info').pt"),
    l1q  = cms.string("userInt('muonL1Info:quality')"),
    l1dr = cms.string("userFloat('muonL1Info:deltaR')"),
)
L2Variables = cms.PSet(
    l2pt  = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).pt"),
    l2eta = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta"),
    l2dr  = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 999 : "+
                      " deltaR( eta, phi, " +
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta, "+
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).phi ) ")
)
L3Variables = cms.PSet(
    l3pt = cms.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).pt"),
    l3dr = cms.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 999 : "+
                      " deltaR( eta, phi, " +
                      "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).eta, "+
                      "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).phi ) ")
)
TriggerVariables = cms.PSet(L1Variables, L2Variables, L3Variables)
AllVariables = cms.PSet(KinematicVariables, IsolationVariables, MuonIDVariables, TrackQualityVariables, L1Variables, L2Variables, L3Variables)

TrackQualityFlags = cms.PSet(
    Track_HP  = cms.string("? track.isNonnull ? track.quality('highPurity') : 0"),
    Track_Qual = cms.string("track.hitPattern.trackerLayersWithMeasurement >= 6 && (track.hitPattern.pixelLayersWithMeasurement + track.hitPattern.numberOfValidStripLayersWithMonoAndStereo) >= 2 && abs(track.dxy) <= 30 && abs(track.dsz )<= 30"),
    IP_Significance = cms.string("abs(track.dxy)/abs(track.dxyError) < 2 "),
    Track_IP = cms.string("abs(track.dxy) < 2"),		
)
MuonIDFlags = cms.PSet(
    Calo   = cms.string("isCaloMuon"),
    Glb    = cms.string("isGlobalMuon"),
    GlbPT  = cms.string("muonID('GlobalMuonPromptTight')"),
    TM     = cms.string("isTrackerMuon"),
    TMA    = cms.string("muonID('TrackerMuonArbitrated')"),
    TMLSAT = cms.string("muonID('TMLastStationAngTight')"),
    TMOSL  = cms.string("muonID('TMOneStationLoose')"),
    TMOST  = cms.string("muonID('TMOneStationTight')"),
    VBTF   = cms.string("numberOfMatchedStations > 1 && muonID('GlobalMuonPromptTight') && abs(dB) < 0.2 && "+
                        "track.numberOfValidHits > 10 && track.hitPattern.numberOfValidPixelHits > 0"),
    TQ = cms.string("track.numberOfValidHits > 10 && track.hitPattern.numberOfValidPixelHits > 0"),		
)

HighPtTriggerFlags = cms.PSet(
   #SingleMu triggers  
   Mu8       = cms.string("!triggerObjectMatchesByFilter('hltSingleMu8L3Filtered8').empty()"),
   Mu15      = cms.string("!triggerObjectMatchesByFilter('hltL3Muon15').empty()"),
   Mu20      = cms.string("!triggerObjectMatchesByFilter('hltSingleMu20L3Filtered20').empty()"),
   Mu24      = cms.string("!triggerObjectMatchesByFilter('hltSingleMu24L3Filtered24').empty()"),
   Mu30      = cms.string("!triggerObjectMatchesByFilter('hltSingleMu30L3Filtered30').empty()"),
   Mu40	     = cms.string("!triggerObjectMatchesByFilter('hltSingleMu40L3Filtered40').empty()"),
   IsoMu15   = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered15').empty()"),
   IsoMu17   = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered17').empty()"),
   IsoMu24   = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered24').empty()"),
   IsoMu30   = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered30').empty()"),
   IsoMu20_eta2p1   = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered20Eta21').empty()"),
   HLT_Any1M    = cms.string("!triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered17').empty() || !triggerObjectMatchesByFilter('hltSingleMu24L3Filtered24').empty() || !triggerObjectMatchesByFilter('hltSingleMu30L3Filtered30').empty()  || !triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered17').empty() || !triggerObjectMatchesByFilter('hltSingleMuIsoL3IsoFiltered20Eta21').empty()"), 
   #DoubleMu triggers
   DoubleMu7 = cms.string("!triggerObjectMatchesByFilter('hltDiMuonL3PreFiltered7').empty()"),
   L2DoubleMu23_Novtx = cms.string("!triggerObjectMatchesByFilter('hltL2DoubleMu23NoVertexL2PreFiltered').empty()"),
   L2DoubleMu30_Novtx = cms.string("!triggerObjectMatchesByFilter('hltL2DoubleMu30NoVertexL2PreFiltered').empty()"),
)

LowPtTriggerFlagsPhysics = cms.PSet(
   DoubleMu0_Quarkonium  = cms.string("!triggerObjectMatchesByPath('HLT_DoubleMu0').empty() || "+
                                      "!triggerObjectMatchesByPath('HLT_DoubleMu0_Quarkonium').empty() || "+
                                      "!triggerObjectMatchesByPath('HLT_DoubleMu0_Quarkonium_v1').empty()"),
   DoubleMu3_Jpsi_A      = cms.string("!triggerObjectMatchesByFilter('hltDiMuonL3PreFiltered3Jpsi').empty()"),
   DoubleMu3_Jpsi_B      = cms.string("!triggerObjectMatchesByFilter('hltDoubleMu3JpsiL3Filtered').empty()"),
   DoubleMu3_Jpsi        = cms.string("!triggerObjectMatchesByPath('HLT_DoubleMu3_Jpsi_v*').empty()"),

)

LowPtTriggerFlagsEfficienciesTag = cms.PSet(
   ## Mu + Track will be added automatically (see below)
   ## Mu + L2Mu
   Mu5_L2Mu0_MU = cms.string("!triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() && "+
                             " triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).hasFilterLabel('hltMu5L2Mu0L3Filtered5')"),
   Mu5_L2Mu2_Jpsi_MU = cms.string("!triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() && "+
                                  " triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).hasFilterLabel('hltMu5L2Mu2JpsiTrackMassFiltered')"),
   Mu3 =                  cms.string("!triggerObjectMatchesByFilter('hltSingleMu3L3Filtered3').empty()"),
)

LowPtTriggerFlagsEfficienciesProbe = cms.PSet(
   ## Mu + Track will be added automatically (see below)
   ## Mu + L2Mu
   Mu5_L2Mu0_L2 = cms.string("!triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() && "+
                             " triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).hasFilterLabel('hltDiMuonL2PreFiltered0')"),
   Mu5_L2Mu2_Jpsi_L2 = cms.string("!triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() && "+
                             " triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).hasFilterLabel('hltMu5L2Mu2JpsiTrackMassFiltered')"),
)
for (ptMu,ptTk) in [ (5,0), (5,2), (3,3), (7,5), (7,7) ]:
   filter = "Mu%dTrack%d" % (ptMu,ptTk) if ptTk > 0 else "Mu%dTrack" % ptMu
   setattr(LowPtTriggerFlagsEfficienciesTag, "Mu%d_Track%d_Jpsi_MU" % (ptMu,ptTk), 
            cms.string("!triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() && "+
                       " triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).hasFilterLabel('hlt"+filter+"JpsiTrackMassFiltered')"))
   setattr(LowPtTriggerFlagsEfficienciesProbe, "Mu%d_Track%d_Jpsi_TK" % (ptMu,ptTk),
            cms.string("!triggerObjectMatchesByCollection('hltMuTrackJpsiCtfTrackCands').empty() && "+
                       " triggerObjectMatchesByCollection('hltMuTrackJpsiCtfTrackCands').at(0).hasFilterLabel('hlt"+filter+"JpsiTrackMassFiltered')"))

LowPtTriggerFlagsEfficiencies = cms.PSet(LowPtTriggerFlagsEfficienciesTag,LowPtTriggerFlagsEfficienciesProbe)
