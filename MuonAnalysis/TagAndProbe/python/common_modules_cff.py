import FWCore.ParameterSet.Config as cms

from MuonAnalysis.TagAndProbe.nearbyMuonsInfo_cfi import nearbyMuonsInfo as tagProbeSeparation

#########################################################################################
##        Object counting modules                                                      ##
#########################################################################################

nverticesModule = cms.EDProducer("VertexMultiplicityCounter", 
    probes = cms.InputTag("tagMuons"),
    objects = cms.InputTag("offlinePrimaryVertices"),
    objectSelection = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
)

njets15Module = cms.EDProducer("CandCleanedMultiplicityCounter", 
    pairs   = cms.InputTag("tpPairs"),
    objects = cms.InputTag("ak5PFJets"),
    objectSelection = cms.string("abs(eta) < 5 && pt > 15"), 
    minTagObjDR   = cms.double(0.3),
    minProbeObjDR = cms.double(0.3),
)

njets30Module = cms.EDProducer("CandCleanedMultiplicityCounter", 
    pairs   = cms.InputTag("tpPairs"),
    objects = cms.InputTag("ak5PFJets"),
    objectSelection = cms.string("abs(eta) < 5 && pt > 30"), 
    minTagObjDR   = cms.double(0.3),
    minProbeObjDR = cms.double(0.3),
)

mergedL1EG = cms.EDProducer("CandViewMerger",
    src = cms.VInputTag(cms.InputTag("l1extraParticles","Isolated"), cms.InputTag("l1extraParticles","NonIsolated")),
)
nL1EG5Module = cms.EDProducer("CandCleanedMultiplicityCounter", 
    pairs   = cms.InputTag("tpPairs"),
    objects = cms.InputTag("mergedL1EG"),
    objectSelection = cms.string("bx == 0 && pt >= 5"), 
    minTagObjDR   = cms.double(0.5),
    minProbeObjDR = cms.double(0.5),
)

#########################################################################################
##        Deterministic Annealing vertices (100um distance; 4.2.X config)              ##
#########################################################################################
offlinePrimaryVerticesDA100um = cms.EDProducer("PrimaryVertexProducer",
    verbose = cms.untracked.bool(False),
    algorithm = cms.string('AdaptiveVertexFitter'),
    TrackLabel = cms.InputTag("generalTracks"),
    useBeamConstraint = cms.bool(False),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    minNdof  = cms.double(0.0),
    PVSelParameters = cms.PSet(
        maxDistanceToBeam = cms.double(1.0)
    ),
    TkFilterParameters = cms.PSet(
        algorithm=cms.string('filter'),
        maxNormalizedChi2 = cms.double(20.0),
        minPixelLayersWithHits=cms.int32(2),
        minSiliconLayersWithHits = cms.int32(5),
        maxD0Significance = cms.double(5.0), 
        minPt = cms.double(0.0),
        trackQuality = cms.string("any")
    ),

    TkClusParameters = cms.PSet(
        algorithm   = cms.string("DA"),
        TkDAClusParameters = cms.PSet(
            coolingFactor = cms.double(0.6),  #  moderate annealing speed
            Tmin = cms.double(4.),            #  end of annealing
            vertexSize = cms.double(0.01),    #  ~ resolution / sqrt(Tmin)
            d0CutOff = cms.double(3.),        # downweight high IP tracks 
            dzCutOff = cms.double(4.)         # outlier rejection after freeze-out (T<Tmin)
        )
    )
)
nverticesDAModule = cms.EDProducer("VertexMultiplicityCounter",
    probes = cms.InputTag("tagMuons"),
    objects = cms.InputTag("offlinePrimaryVerticesDA100um"),
    objectSelection = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
)   


#########################################################################################
##        Tracking-related modules                                                     ##
#########################################################################################

## Now I have to define the passing probes for tracking
## first remove low pt tracks which will not make muons anyway
pCutTracks = cms.EDFilter("TrackSelector", 
    src = cms.InputTag("generalTracks"),      
    cut = cms.string("pt > 2 || (abs(eta) > 1 && p > 2)"),
)
tkTracks = cms.EDProducer("ConcreteChargedCandidateProducer", 
    src = cms.InputTag("pCutTracks"),
    particleType = cms.string("mu+"),
)

## Filter out the J/Psi's, to compute fake matching rate
tkTracksNoJPsi = cms.EDProducer("CandidateResonanceInefficiencyCreator",
    src = cms.InputTag("tkTracks"),
    tags = cms.InputTag("tagMuons"),
    mass    = cms.double(3.096),
    massMin = cms.double(2.85), ## Should cut away
    massMax = cms.double(3.25), ## 99.5% of signal
    onlyBestMatch = cms.bool(False),
    outputMode = cms.string("RefToBaseVector"),
)
tkTracksNoBestJPsi = tkTracksNoJPsi.clone(onlyBestMatch = True)

## Filter out the J/Psi's, to compute fake matching rate
tkTracksNoZ = cms.EDProducer("CandidateResonanceInefficiencyCreator",
    src = cms.InputTag("tkTracks"),
    tags = cms.InputTag("tagMuons"),
    mass    = cms.double(91.2),
    massMin = cms.double(40),  ## Should cut away most
    massMax = cms.double(200), ## of the signal
    onlyBestMatch = cms.bool(True),
    outputMode = cms.string("RefToBaseVector"),
)

staToTkMatch = cms.EDProducer("MatcherUsingTracksWithTagAssoc",
    src     = cms.InputTag("probeMuonsSta"),
    matched = cms.InputTag("tkTracks"),  
    tags      = cms.InputTag("tagMuons"),
    tagDeltaZ = cms.double(1.0),
    algorithm = cms.string("byDirectComparison"), 
    srcTrack     = cms.string("muon"),    srcState = cms.string("atVertex"), 
    matchedTrack = cms.string("tracker"), matchedState = cms.string("atVertex"),
    maxDeltaR        = cms.double(1.),   # large range in DR (we can tighten it later)
    maxDeltaEta      = cms.double(0.4),  # small in eta, which is more precise
    maxDeltaLocalPos = cms.double(100),
    maxDeltaPtRel    = cms.double(5),   # |pt(sta) - pt(tk)|/pt(tk)
    sortBy           = cms.string("deltaR"),
    requireSameCharge = cms.bool(True),
)
staToTkMatchNoJPsi = staToTkMatch.clone(matched = 'tkTracksNoJPsi')
staToTkMatchNoBestJPsi = staToTkMatch.clone(matched = 'tkTracksNoBestJPsi')
staToTkMatchNoZ = staToTkMatch.clone(matched = 'tkTracksNoZ')

staToTkMatchSequenceJPsi = cms.Sequence(
    pCutTracks + 
    tkTracks           * staToTkMatch           +
    tkTracksNoJPsi     * staToTkMatchNoJPsi     +
    tkTracksNoBestJPsi * staToTkMatchNoBestJPsi 
)
staToTkMatchSequenceZ = cms.Sequence(
    pCutTracks +
    tkTracks    * staToTkMatch    +
    tkTracksNoZ * staToTkMatchNoZ     
)

#########################################################################################
##        Isolation modules                                                            ##
#########################################################################################

import RecoMuon.MuonIsolationProducers.muIsoDepositTk_cfi
probeMuonsIsoDepositTk = RecoMuon.MuonIsolationProducers.muIsoDepositTk_cfi.muIsoDepositTk.clone()
probeMuonsIsoDepositTk.IOPSet.inputMuonCollection = 'probeMuons'
probeMuonsIsoFromDepsTk = cms.EDProducer("CandIsolatorFromDeposits", 
    deposits = cms.VPSet( cms.PSet(
        src = cms.InputTag("probeMuonsIsoDepositTk"),
        mode = cms.string('sum'),
        weight = cms.string('1'),
        deltaR = cms.double(0.3),
        vetos = cms.vstring('0.01'),
        skipDefaultVeto = cms.bool(True),
        label = cms.string('tkDep'),
    ))
)
probeMuonsRelIsoFromDepsTk = probeMuonsIsoFromDepsTk.clone()
probeMuonsRelIsoFromDepsTk.deposits[0].mode = "sumRelative"
probeMuonsIsoValueMaps = cms.EDProducer("AnyNumbersToValueMaps",
    collection = cms.InputTag("probeMuons"),
    associations = cms.VInputTag(cms.InputTag("probeMuonsIsoFromDepsTk"), cms.InputTag("probeMuonsRelIsoFromDepsTk")),
)
probeMuonsIsoSequence = cms.Sequence(
    ( probeMuonsIsoDepositTk * 
        ( probeMuonsIsoFromDepsTk + probeMuonsRelIsoFromDepsTk) 
    ) * probeMuonsIsoValueMaps
)


#########################################################################################
##        Other modules                                                                ##
#########################################################################################

muonDxyPVdzmin = cms.EDProducer("MuonDxyPVdzmin",
    probes = cms.InputTag("probeMuons"),
)

muonsPassingPF = cms.EDProducer("MuonsPassingPF",
    muons = cms.InputTag("probeMuons"),
    pf    = cms.InputTag("particleFlow"),
    pfCut = cms.string("abs(pdgId) == 13"),
    matchByReference = cms.bool(False), # set to true only if your probeMuons are a subset by reference of the "muons" collection
)
