import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(
        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FCFA7A2C-CA7D-E011-8F26-1CC1DE1CDD02.root',
        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FAF326C9-DF7D-E011-A815-1CC1DE1CDDBC.root',
        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FAE083F7-997D-E011-B9E3-1CC1DE051060.root',
        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FAA2BA37-8E7D-E011-BEBA-00237DA12CEC.root',
        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FA5A22B2-5D7D-E011-99CE-00237DA12FFE.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/FA108ED1-677D-E011-B869-0017A4771018.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F8BF8F7C-867D-E011-8EF9-1CC1DE1D2028.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F8A6AD03-6E7D-E011-9CBE-001F29C4616E.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F819129A-C87D-E011-81DF-00237DA1985A.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F6A3DA72-A47D-E011-A4DA-1CC1DE053050.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F66D3361-0B7E-E011-A61A-1CC1DE040FA0.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F61505DB-907D-E011-AB60-002481A7329C.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F4D05480-927D-E011-BB88-1CC1DE1D03FC.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F45C5C45-857D-E011-AF9D-1CC1DE1CDDBC.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F2BA56E3-867D-E011-8D12-1CC1DE1CEAEE.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F2B1068D-5E7D-E011-B65F-1CC1DE1D03FC.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F2938D05-647D-E011-A1B2-1CC1DE052030.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F27AC9F7-DF7D-E011-9375-00237DA1FC56.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F23E9882-867D-E011-95F8-1CC1DE0437C8.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F23BA822-667D-E011-A0BD-00237DA1A66C.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F233D4D4-677D-E011-93E4-1CC1DE04FF48.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/F20831AF-657D-E011-9BE4-001F29C4A3A0.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/EED07AE9-687D-E011-8E98-0017A4771010.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/EECC101A-6F7D-E011-A16A-1CC1DE1CEDB2.root',
#        '/store/data/Run2011A/SingleMu/AOD/May10ReReco-v1/0005/EE957DFE-5E7D-E011-A066-001CC443B76C.root'
    ),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )    

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = cms.string('GR_R_42_V18::All')

## ==== Fast Filters ====
process.goodVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
    filter = cms.bool(True),
)
process.noScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)
process.fastFilter = cms.Sequence(process.goodVertexFilter + process.noScraping)
###    __  __                       
##   |  \/  |_   _  ___  _ __  ___ 
##   | |\/| | | | |/ _ \| '_ \/ __|
##   | |  | | |_| | (_) | | | \__ \
##   |_|  |_|\__,_|\___/|_| |_|___/
##                                 
## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"), 
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("pt > 5 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 5"),
    tracksCut    = cms.string("pt > 5"),
)

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
process.muonMatchHLTL2.matchedCuts = cms.string('coll("hltL2MuonCandidatesNoVtx")')
process.muonMatchHLTL2.maxDeltaR = 0.1
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")



from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 15 && "+MuonIDFlags.VBTF.value()+" && !triggerObjectMatchesByCollection('hltL3MuonCandidates').empty()"),
)

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull"),  # no real cut now
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('60 < mass < 140'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

from MuonAnalysis.TagAndProbe.nearbyMuonsInfo_cfi import *
process.load("MuonAnalysis.TagAndProbe.nearbyMuonsInfo_cfi")
process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("OneProbe"),
    # probe variables: all useful ones
    variables = cms.PSet(
        AllVariables,
        isoTrk03Abs = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsIsoFromDepsTk"),
        isoTrk03Rel = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsRelIsoFromDepsTk"),
    ),
    flags = cms.PSet(
       TrackQualityFlags,
       MuonIDFlags,
       HighPtTriggerFlags,
       # Extra triggers
       Mu8_forEMu  = cms.string("!triggerObjectMatchesByFilter('hltL1MuOpenEG5L3Filtered8').empty"),
       Mu17_forEMu = cms.string("!triggerObjectMatchesByFilter('hltL1MuOpenEG5L3Filtered17').empty"),
       ## Isolation
       Isol    = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt < 0.15"), 
       IsolTk3 = cms.string("isolationR03.sumPt < 3"), 
       IsolTk4 = cms.string("isolationR03.sumPt < 4"),
       ## ParticleFlow
       PF = cms.InputTag("muonsPassingPF"),
       Track_VBTF = cms.string("track.numberOfValidHits > 10 && track.hitPattern.pixelLayersWithMeasurement > 0 && abs(dB) < 0.2"),
    ),
    tagVariables = cms.PSet(
        nVertices   = cms.InputTag("nverticesModule"),
        nVerticesDA = cms.InputTag("nverticesDAModule"),
        combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
    ),
    tagFlags = cms.PSet(HighPtTriggerFlags,TrackQualityFlags,MuonIDFlags,IsolTk3 = cms.string("isolationR03.sumPt < 3"),IsolTk4 = cms.string("isolationR03.sumPt < 4")),
    pairVariables = cms.PSet(
        drM2    = cms.InputTag("nearbyMuonsInfo", "drM2"),
        nJets15 = cms.InputTag("njets15Module"),
        nJets30 = cms.InputTag("njets30Module"),
        dz      = cms.string("daughter(0).vz - daughter(1).vz"),
        nL1EG5  = cms.InputTag("nL1EG5Module"), # to unlock EMu triggers
        pt      = cms.string("pt"), # let's do some bump hunt in the T&P too
    ),
    pairFlags = cms.PSet(),
    isMC           = cms.bool(False),
    addRunLumiInfo = cms.bool(True),
)

process.tnpSimpleSequence = cms.Sequence(
    process.tagMuons +
    process.oneTag     +
    process.probeMuons +
    process.tpPairs    +
    process.onePair    +
    process.nverticesModule +
    process.offlinePrimaryVerticesDA100um * process.nverticesDAModule +
    process.njets15Module +
    process.njets30Module +
    process.mergedL1EG + process.nL1EG5Module +
    process.muonsPassingPF +
    process.probeMuonsIsoSequence +
    process.nearbyMuonsInfo +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence +
    process.tnpSimpleSequence
)


process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpZ_Data.root"))
