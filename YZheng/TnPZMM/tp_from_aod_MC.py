import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FEEED0D2-C97C-E011-A3A4-003048C692D6.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FE7B3836-C77C-E011-801A-003048C693E2.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FE39CCE8-EA7C-E011-AE3D-00237DDCBEA4.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FCF0A7FA-DE7C-E011-BE51-002481E0D708.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FCBBBA3D-D27C-E011-AB23-003048D436FE.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FC919915-C37C-E011-8F73-003048C693EC.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FC5F71A2-C77C-E011-9289-003048D2BB22.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FAD0C5B7-E47C-E011-9644-003048C693BA.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FA58CDCF-E77C-E011-AE79-003048C69406.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FA47F3C7-E47C-E011-B8CD-00237DDCBEA4.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FA3D3EBF-CF7C-E011-B702-0030487D7109.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FA2D47C3-BE7C-E011-9C66-0030487D5E53.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/FA20C924-CF7C-E011-9177-003048D4399E.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/F8FBF41E-CB7C-E011-875D-002481E0D480.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/F857BF90-E27C-E011-AE83-003048C693B8.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/F6A4F02F-C77C-E011-811C-003048C692DA.root',
        '/store/mc/Summer11/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/AODSIM/PU_S3_START42_V11-v2/0000/F495C603-D47C-E011-A212-003048D4DFA4.root'
    ),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )    

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = cms.string('MC_42_V13::All')#START311_V2::All')

##    __  __                       
##   |  \/  |_   _  ___  _ __  ___ 
##   | |\/| | | | |/ _ \| '_ \/ __|
##   | |  | | |_| | (_) | | | \__ \
##   |_|  |_|\__,_|\___/|_| |_|___/
##                                 
## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(False),
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
process.muonMatchHLTL2.maxDeltaR = 0.5
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
changeTriggerProcessName(process, "*") # auto-guess

from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 15 && "+MuonIDFlags.VBTF.value()+" && !triggerObjectMatchesByCollection('hltL3MuonCandidates').empty()"),
)

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull"),  # no real cut now
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('60 < mass < 140'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)

process.tagMuonsMCMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    src = cms.InputTag("tagMuons"),
    matched = cms.InputTag("genParticles"),
    pdgId = cms.vint32(13),
    distMin = cms.double(0.3),
)
process.probeMuonsMCMatch = process.tagMuonsMCMatch.clone(src = "probeMuons")

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
       LowPtTriggerFlagsEfficienciesTag,
       ## Isolation
       Isol    = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt < 0.15"), 
       IsolTk4 = cms.string("isolationR03.sumPt < 4"), 
       ## ParticleFlow
       PF = cms.InputTag("muonsPassingPF"),
       ## A few other flags
       Track_VBTF = cms.string("track.numberOfValidHits > 10 && track.hitPattern.pixelLayersWithMeasurement > 0 && abs(dB) < 0.2"),
    ),
    tagVariables = cms.PSet(
        nVertices   = cms.InputTag("nverticesModule"),
        nVerticesDA = cms.InputTag("nverticesDAModule"),
        combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
    ),
    tagFlags = cms.PSet(HighPtTriggerFlags,TrackQualityFlags,MuonIDFlags,IsolTk4 = cms.string("isolationR03.sumPt < 4")),
    pairVariables = cms.PSet(
        nJets15 = cms.InputTag("njets15Module"),
        nJets30 = cms.InputTag("njets30Module"),
        dz      = cms.string("daughter(0).vz - daughter(1).vz"),
        pt      = cms.string("pt"), # let's do some bump hunt in the T&P too
	drM2    = cms.InputTag("nearbyMuonsInfo", "drM2"),
    ),
    pairFlags = cms.PSet(),
    isMC           = cms.bool(True),
    tagMatches       = cms.InputTag("tagMuonsMCMatch"),
    probeMatches     = cms.InputTag("probeMuonsMCMatch"),
    motherPdgId      = cms.vint32(22, 23),
    makeMCUnbiasTree       = cms.bool(False), 
    checkMotherInUnbiasEff = cms.bool(True),
    allProbes              = cms.InputTag("probeMuons"),
)

process.tnpSimpleSequence = cms.Sequence(
    process.tagMuons   * process.tagMuonsMCMatch   +
    process.probeMuons * process.probeMuonsMCMatch +
    process.tpPairs    +
    process.nverticesModule +
    process.offlinePrimaryVerticesDA100um * process.nverticesDAModule +
    process.njets15Module +
    process.njets30Module +
    process.muonsPassingPF +
    process.probeMuonsIsoSequence +
    process.tpTree
)

#process.fastFilter = cms.EDFilter("MuonSelector", src = cms.InputTag("muons"), cut = cms.string("pt > 15"), filter = cms.bool(True))
process.tagAndProbe = cms.Path( 
    #process.fastFilter                  *
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence +
    process.tnpSimpleSequence
)

##    _____               _    _             
##   |_   _| __ __ _  ___| | _(_)_ __   __ _ 
##     | || '__/ _` |/ __| |/ / | '_ \ / _` |
##     | || | | (_| | (__|   <| | | | | (_| |
##     |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
##                                     |___/ 

## Then make another collection for standalone muons, using standalone track to define the 4-momentum
process.muonsSta = cms.EDProducer("RedefineMuonP4FromTrack",
    src   = cms.InputTag("muons"),
    track = cms.string("outer"),
)
## Match to trigger, to measure the efficiency of HLT tracking
from PhysicsTools.PatAlgos.tools.helpers import *
process.patMuonsWithTriggerSequenceSta = cloneProcessingSnippet(process, process.patMuonsWithTriggerSequence, "Sta")
process.muonMatchHLTL2Sta.maxDeltaR = 0.5
process.muonMatchHLTL3Sta.maxDeltaR = 0.5
massSearchReplaceAnyInputTag(process.patMuonsWithTriggerSequenceSta, "mergedMuons", "muonsSta")

## Define probes and T&P pairs
process.probeMuonsSta = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTriggerSta"),
    cut = cms.string("outerTrack.isNonnull"), # no real cut now
)
process.probeMuonsMCMatchSta = process.tagMuonsMCMatch.clone(src = "probeMuonsSta")

process.tpPairsSta = process.tpPairs.clone(decay = "tagMuons@+ probeMuonsSta@-", cut = '40 < mass < 150')

process.staToTkMatch.maxDeltaR     = 0.3
process.staToTkMatch.maxDeltaPtRel = 2.
process.staToTkMatchNoZ.maxDeltaR     = 0.3
process.staToTkMatchNoZ.maxDeltaPtRel = 2.

process.tpTreeSta = process.tpTree.clone(
    tagProbePairs = "tpPairsSta",
    variables = cms.PSet(
        KinematicVariables, 
        ## track matching variables
        tk_deltaR     = cms.InputTag("staToTkMatch","deltaR"),
        tk_deltaEta   = cms.InputTag("staToTkMatch","deltaEta"),
        tk_deltaR_NoZ   = cms.InputTag("staToTkMatchNoZ","deltaR"),
        tk_deltaEta_NoZ = cms.InputTag("staToTkMatchNoZ","deltaEta"),
    ),
    flags = cms.PSet(
        outerValidHits = cms.string("outerTrack.numberOfValidHits > 0"),
        TM  = cms.string("isTrackerMuon"),
        Glb = cms.string("isGlobalMuon"),
    ),
    allProbes     = "probeMuonsSta",
    probeMatches  = "probeMuonsMCMatchSta",
)
process.tpTreeSta.pairVariables.nJets15 = "njets15ModuleSta"
process.tpTreeSta.pairVariables.nJets30 = "njets30ModuleSta"
process.njets15ModuleSta = process.njets15Module.clone(pairs = "tpPairsSta")
process.njets30ModuleSta = process.njets30Module.clone(pairs = "tpPairsSta")

process.tnpSimpleSequenceSta = cms.Sequence(
    process.tagMuons   * process.tagMuonsMCMatch   +
    process.probeMuonsSta * process.probeMuonsMCMatchSta +
    process.tpPairsSta      +
    process.nverticesModule +
    process.offlinePrimaryVerticesDA100um * process.nverticesDAModule +
    process.staToTkMatchSequenceZ +
    process.njets15ModuleSta +
    process.njets30ModuleSta +
    process.tpTreeSta
)

process.tagAndProbeSta = cms.Path( 
    #process.fastFilter                  *
    process.muonsSta                       +
    process.patMuonsWithTriggerSequenceSta +
    process.tnpSimpleSequenceSta
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpZ_MC.root"))
