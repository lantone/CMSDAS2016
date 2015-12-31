sampleDataSet = '/WWTo2L2Nu_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM'
sampleCMSEnergy = 7000

sampleRelease = "CMSSW_4_2_3_patch3" # original (i.e. RECO file) release, not the one we plan to process them with
sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleNumEvents = 210667

sampleXSec = 2.927 # pb

# global tag can be extracted from file using edmProvDump filename|grep globaltag
# note however that this is the tag for *further* processing, not the original tag
sampleGlobalTag = 'START42_V13::All'
sampleHLTProcess = '*'

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/WW"

sampleRecoFiles = [ ]

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_6oH.root",
  sampleBaseDir+"/pat/PATtuple_2_1_www.root",
  sampleBaseDir+"/pat/PATtuple_3_0_rDZ.root",
  sampleBaseDir+"/pat/PATtuple_4_0_xfd.root",
  sampleBaseDir+"/pat/PATtuple_5_0_T3j.root",
  sampleBaseDir+"/pat/PATtuple_6_0_EPJ.root",
  sampleBaseDir+"/pat/PATtuple_7_0_TFt.root",
  sampleBaseDir+"/pat/PATtuple_8_0_G21.root",
  sampleBaseDir+"/pat/PATtuple_9_0_aF3.root",
  sampleBaseDir+"/pat/PATtuple_10_0_AyC.root",
  sampleBaseDir+"/pat/PATtuple_11_0_QFW.root",
  sampleBaseDir+"/pat/PATtuple_12_0_a4e.root",
  sampleBaseDir+"/pat/PATtuple_13_0_KpV.root",
  sampleBaseDir+"/pat/PATtuple_14_0_lzE.root",
  sampleBaseDir+"/pat/PATtuple_15_0_QR6.root",
  sampleBaseDir+"/pat/PATtuple_16_0_9Cj.root",
  sampleBaseDir+"/pat/PATtuple_17_0_uvZ.root",
  sampleBaseDir+"/pat/PATtuple_18_0_c0O.root",
  sampleBaseDir+"/pat/PATtuple_19_0_4Ba.root",
  sampleBaseDir+"/pat/PATtuple_20_0_kT0.root",
  sampleBaseDir+"/pat/PATtuple_21_0_KW4.root",
  sampleBaseDir+"/pat/PATtuple_22_0_1u2.root"
]

sampleDuplicateCheckMode = 'checkAllFilesOpened'

sampleType = "MC"
