import FWCore.ParameterSet.Config as cms

process = cms.Process("TrackingEfficiencyFromCosmics")

# # initialize MessageLogger and output report
# process.load("FWCore.MessageLogger.MessageLogger_cfi")
# # process.MessageLogger.cerr.threshold = 'INFO'
# # process.MessageLogger.categories.append('Demo')
# # process.MessageLogger.cerr.INFO = cms.untracked.PSet(
# #     limit = cms.untracked.int32(-1)
# # )

process.load("FWCore.MessageService.test.Services_cff")
# Here is the configuration of the MessgeLogger Service:
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('Message'),
    Message = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    )
)

process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.StandardSequences.Reconstruction_cff')

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
# process.load('Configuration.StandardSequences.MagneticField_cff')

# Careful, this needs to be changed for the data
process.GlobalTag.globaltag = 'START42_V11::All'

# process.load("MagneticField.Engine.uniformMagneticField_cfi")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'root://xrootd.rcac.purdue.edu//store/user/demattia/DisplacedVertex/Cosmics/Simulation/Run170547//reco_RAW2DIGI_L1Reco_RECO_DQM_1.root'
    )
)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.TFileService=cms.Service('TFileService',
                                 fileName=cms.string('TrackingEfficiencyFromCosmics.root')
                                 )



# Testing the new smart propagator with IP
# process.load("Analysis.TrackingEfficiencyFromCosmics.SmartPropagatorWithIP_cff")

# PropagatorWithMaterialESProducer
# process.load("TrackingTools.MaterialEffects.MaterialPropagator_cfi")
# PropagatorWithMaterialESProducer
# from TrackingTools.MaterialEffects.OppositeMaterialPropagator_cfi import *

# Tracker's propagators
# from TrackingTools.MaterialEffects.RungeKuttaTrackerPropagator_cfi import *
# from TrackingTools.MaterialEffects.RungeKuttaTrackerPropagatorOpposite_cfi import *

# Muon's propagators
# from TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi import *
# from TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi import *
# process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")

process.MaterialPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
                                            MaxDPhi = cms.double(1.6),
                                            ComponentName = cms.string('PropagatorWithMaterial'),
                                            Mass = cms.double(0.105),
                                            PropagationDirection = cms.string('alongMomentum'),
                                            useRungeKutta = cms.bool(False),
                                            # If ptMin > 0, uncertainty in reconstructed momentum will be taken into account when estimating rms scattering angle.
                                            # (By default, it is neglected). However, it will also be assumed that the track pt can't be below specified value,
                                            # to prevent this scattering angle becoming too big.
                                            ptMin = cms.double(-1.)
                                            )

process.SteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
                                                    ComponentName = cms.string('SteppingHelixPropagatorAny'),
                                                    NoErrorPropagation = cms.bool(False),
                                                    PropagationDirection = cms.string('anyDirection'),
                                                    useTuningForL2Speed = cms.bool(False),
                                                    useIsYokeFlag = cms.bool(True),
                                                    endcapShiftInZNeg = cms.double(0.0),
                                                    SetVBFPointer = cms.bool(False),
                                                    AssumeNoMaterial = cms.bool(False),
                                                    endcapShiftInZPos = cms.double(0.0),
                                                    useInTeslaFromMagField = cms.bool(False),
                                                    VBFName = cms.string('VolumeBasedMagneticField'),
                                                    useEndcapShiftsInZ = cms.bool(False),
                                                    sendLogWarning = cms.bool(False),
                                                    useMatVolumes = cms.bool(True),
                                                    debug = cms.bool(False),
                                                    #This sort of works but assumes a measurement at propagation origin
                                                    ApplyRadX0Correction = cms.bool(True),
                                                    useMagVolumes = cms.bool(True),
                                                    returnTangentPlane = cms.bool(True)
                                                    )

# Smart propagator with IP
process.smartPropagatorWithIPESProducer = cms.ESProducer("SmartPropagatorWithIPESProducer",
                                                         ComponentName = cms.string('SmartPropagatorWithIP'),
                                                         TrackerPropagator = cms.string('PropagatorWithMaterial'),
                                                         # TrackerPropagator = cms.string('RungeKuttaTrackerPropagator'),
                                                         MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
                                                         PropagationDirection = cms.string('alongMomentum'),
                                                         Epsilon = cms.double(10.0) # the standard one has 5., but uses 10 hardcoded internally...
                                                         )



process.demo = cms.EDAnalyzer('TrackingEfficiencyFromCosmics',
                              EffDxyMin = cms.double(0),
                              EffDxyMax = cms.double(100),
                              EffDzMin = cms.double(0),
                              EffDzMax = cms.double(100),
                              EffPtMin = cms.double(0),
                              EffPtMax = cms.double(200),
                              
                              MaxDeltaR = cms.double(1),
                              SimMaxDeltaR = cms.double(1000),
                              DzMinCut = cms.double(0),
                              DzMaxCut = cms.double(1000000),
                              DxyCut = cms.double(50),
                              Chi2Cut = cms.double(1000000),
                              TrackPtCut = cms.double(25),
                              StandAlonePtCut = cms.double(0),
                              HighPurity = cms.bool(True),
                              
                              MatchTwoLegs = cms.bool(True),

                              DeltaDxyCut = cms.double(15), # only if matching two legs
                              DeltaDzCut = cms.double(30),  # only if matching two legs
                              DeltaPtCut = cms.double(1000),  # only if matching two legs
                              DeltaPhiCut = cms.double(1),  # only if matching two legs
                              MinimumValidHits = cms.int32(0),

                              UseMCtruth = cms.bool(False),

                              EffOutputFileName = cms.string("Efficiency.root"),
                              EffCleanedOutputFileName = cms.string("EfficiencyCleaned.root"),
                              GenToStandAloneEffOutputFileName = cms.string("GenToStandAloneEfficiency.root"),
                              GenToTrackEffOutputFileName = cms.string("GenToTrackEfficiency.root"),

                              RecomputeIP = cms.bool(False),

                              SingleLegMuon = cms.bool(True),
                              CountOppoSide = cms.bool(True),
                              CountSameSide = cms.bool(True),
                              PhiRegion = cms.bool(False),
                              PhiMinCut = cms.double(-3.2),
                              PhiMaxCut = cms.double(0),

                              # MuonCollection = cms.InputTag("standAloneMuons"),
                              MuonCollection = cms.InputTag("cosmicMuons1Leg"),
                              TrackCollection = cms.InputTag("generalTracks"),

                              UseAllTracks = cms.bool(False),
                              UseTrackParameters = cms.bool(False),
                              DxyErrorCut = cms.bool(False),
                              DzErrorCut = cms.bool(False),
                              DxyCutForNoDzCut = cms.double(4),

                              # The propagator used is different outside and inside the Tracker volume
                              GenInsideTkVol = cms.bool(False)
                              )

process.p = cms.Path(process.demo)
