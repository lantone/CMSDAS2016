sampleDataSet = '/HTo2LongLivedTo4F_MH-400_MFF-50_CTau-80_7TeV-pythia6/Summer11-PU_S4_START42_V11-v2/AODSIM'
sampleCMSEnergy = 7000
sampleXSec = 2 # this actually means 1 for the lepton channel # pb

# for signal MC: what is the abs(PDGid) of the long-lived signal particle?
sampleSignalPID = 6000113

sampleRelease = "CMSSW_4_2_3_patch3" # original (i.e. RECO file) release, not the one we plan to process them with
sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleNumEvents = 108438

# global tag can be extracted from file using edmProvDump filename|grep globaltag
# note however that this is the tag for *further* processing, not the original tag
sampleGlobalTag = 'START42_V13::All'
sampleHLTProcess = '*'

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/Signal_400_050F"

sampleRecoFiles = [ ]

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_qOs.root",
  sampleBaseDir+"/pat/PATtuple_2_1_yJr.root",
  sampleBaseDir+"/pat/PATtuple_3_1_usF.root",
  sampleBaseDir+"/pat/PATtuple_4_1_y2t.root",
  sampleBaseDir+"/pat/PATtuple_5_1_nBm.root",
  sampleBaseDir+"/pat/PATtuple_6_1_PdR.root",
  sampleBaseDir+"/pat/PATtuple_7_1_Ep2.root",
  sampleBaseDir+"/pat/PATtuple_8_1_uIK.root",
  sampleBaseDir+"/pat/PATtuple_9_1_nd6.root",
  sampleBaseDir+"/pat/PATtuple_10_1_nwe.root",
  sampleBaseDir+"/pat/PATtuple_11_1_R10.root",
  sampleBaseDir+"/pat/PATtuple_12_1_0gk.root"
]

sampleDuplicateCheckMode = 'checkAllFilesOpened'

sampleType = "MC"
