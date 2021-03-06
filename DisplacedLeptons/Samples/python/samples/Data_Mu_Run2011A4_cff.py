sampleDataSet = '/DoubleMu/Run2011A-PromptReco-v6/AOD'
sampleNumEvents = 6854601 # according to DBS, as of 03 October 2011

# global tag needs to be chosen to match release, trigger menu and alignment conditions.
# see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
sampleGlobalTag = 'GR_R_42_V21A::All'
sampleHLTProcess = '*'

# data quality run/lumi section selection
sampleJSON = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON_MuonPhys.txt"

# restrict run range (mainly to get a sample with consistent trigger configuration)
sampleRunRange = [160000,999999]

# use checkAllFilesOpened whenever possible, and noDuplicateCheck when necessary
sampleDuplicateCheckMode = "checkAllFilesOpened"

# "DATA" or "MC"
sampleType = "DATA"

sampleRelease = "CMSSW_4_2_7" # original (i.e. RECO file) release,
                              # not the one we plan to process them with

sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/Data_Mu_Run2011A4"

sampleRecoFiles = []

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_tnZ.root",
  sampleBaseDir+"/pat/PATtuple_2_1_Qd6.root",
  sampleBaseDir+"/pat/PATtuple_3_1_0NE.root",
  sampleBaseDir+"/pat/PATtuple_4_0_Dmt.root",
  sampleBaseDir+"/pat/PATtuple_5_0_1iv.root",
  sampleBaseDir+"/pat/PATtuple_6_0_qdu.root",
  sampleBaseDir+"/pat/PATtuple_7_0_zKh.root",
  sampleBaseDir+"/pat/PATtuple_8_0_pAp.root",
  sampleBaseDir+"/pat/PATtuple_9_0_Fvu.root",
  sampleBaseDir+"/pat/PATtuple_10_0_JRR.root",
  sampleBaseDir+"/pat/PATtuple_11_0_rl8.root",
  sampleBaseDir+"/pat/PATtuple_12_0_YmB.root",
  sampleBaseDir+"/pat/PATtuple_13_0_cUX.root",
  sampleBaseDir+"/pat/PATtuple_14_0_GgZ.root",
  sampleBaseDir+"/pat/PATtuple_15_0_0V3.root",
  sampleBaseDir+"/pat/PATtuple_16_0_6YT.root",
  sampleBaseDir+"/pat/PATtuple_17_1_t4G.root",
  sampleBaseDir+"/pat/PATtuple_18_1_fdN.root",
  sampleBaseDir+"/pat/PATtuple_19_1_O97.root",
  sampleBaseDir+"/pat/PATtuple_20_1_Sma.root",
  sampleBaseDir+"/pat/PATtuple_21_1_Zpw.root",
  sampleBaseDir+"/pat/PATtuple_22_1_ha7.root",
  sampleBaseDir+"/pat/PATtuple_23_1_uCQ.root",
  sampleBaseDir+"/pat/PATtuple_24_1_eVT.root",
  sampleBaseDir+"/pat/PATtuple_25_1_ZFH.root",
  sampleBaseDir+"/pat/PATtuple_26_1_KOi.root",
  sampleBaseDir+"/pat/PATtuple_27_1_HWf.root",
  sampleBaseDir+"/pat/PATtuple_28_1_tFd.root",
  sampleBaseDir+"/pat/PATtuple_29_1_NLs.root",
  sampleBaseDir+"/pat/PATtuple_30_1_M4g.root",
  sampleBaseDir+"/pat/PATtuple_31_1_73u.root",
  sampleBaseDir+"/pat/PATtuple_32_1_1qu.root",
  sampleBaseDir+"/pat/PATtuple_33_1_Jx9.root",
  sampleBaseDir+"/pat/PATtuple_34_1_wgv.root",
  sampleBaseDir+"/pat/PATtuple_35_1_r1I.root",
  sampleBaseDir+"/pat/PATtuple_36_1_s1b.root",
  sampleBaseDir+"/pat/PATtuple_37_1_e4d.root",
  sampleBaseDir+"/pat/PATtuple_38_1_qhL.root",
  sampleBaseDir+"/pat/PATtuple_39_1_QQx.root",
  sampleBaseDir+"/pat/PATtuple_40_1_8JX.root",
  sampleBaseDir+"/pat/PATtuple_41_1_pkr.root",
  sampleBaseDir+"/pat/PATtuple_42_1_2EO.root",
  sampleBaseDir+"/pat/PATtuple_43_1_lbg.root",
  sampleBaseDir+"/pat/PATtuple_44_1_6NK.root",
  sampleBaseDir+"/pat/PATtuple_45_1_qfR.root",
  sampleBaseDir+"/pat/PATtuple_46_1_NxW.root",
  sampleBaseDir+"/pat/PATtuple_47_1_XE6.root",
  sampleBaseDir+"/pat/PATtuple_48_1_0jR.root",
  sampleBaseDir+"/pat/PATtuple_49_1_eAM.root",
  sampleBaseDir+"/pat/PATtuple_50_1_sKd.root",
  sampleBaseDir+"/pat/PATtuple_51_1_29z.root",
  sampleBaseDir+"/pat/PATtuple_52_1_Atr.root",
  sampleBaseDir+"/pat/PATtuple_53_1_1Lj.root",
  sampleBaseDir+"/pat/PATtuple_54_1_Fdd.root",
  sampleBaseDir+"/pat/PATtuple_55_1_Fkr.root",
  sampleBaseDir+"/pat/PATtuple_56_1_XrN.root",
  sampleBaseDir+"/pat/PATtuple_57_1_1XY.root",
  sampleBaseDir+"/pat/PATtuple_58_1_38J.root",
  sampleBaseDir+"/pat/PATtuple_59_1_W7Z.root",
  sampleBaseDir+"/pat/PATtuple_60_1_vnz.root",
  sampleBaseDir+"/pat/PATtuple_61_1_ibH.root",
  sampleBaseDir+"/pat/PATtuple_62_1_Ve7.root",
  sampleBaseDir+"/pat/PATtuple_63_1_4qy.root",
  sampleBaseDir+"/pat/PATtuple_64_1_w3G.root",
  sampleBaseDir+"/pat/PATtuple_65_1_r0i.root",
  sampleBaseDir+"/pat/PATtuple_66_1_xKk.root",
  sampleBaseDir+"/pat/PATtuple_67_0_O5w.root",
  sampleBaseDir+"/pat/PATtuple_68_0_22c.root",
  sampleBaseDir+"/pat/PATtuple_69_0_l7R.root",
  sampleBaseDir+"/pat/PATtuple_70_1_2dF.root",
  sampleBaseDir+"/pat/PATtuple_71_0_X5N.root",
  sampleBaseDir+"/pat/PATtuple_72_0_6Kt.root",
  sampleBaseDir+"/pat/PATtuple_73_0_UOf.root",
  sampleBaseDir+"/pat/PATtuple_74_0_BCy.root",
  sampleBaseDir+"/pat/PATtuple_75_0_eUp.root",
  sampleBaseDir+"/pat/PATtuple_76_0_YPS.root",
  sampleBaseDir+"/pat/PATtuple_77_0_jUt.root",
  sampleBaseDir+"/pat/PATtuple_78_0_eMV.root",
  sampleBaseDir+"/pat/PATtuple_79_0_8a5.root",
  sampleBaseDir+"/pat/PATtuple_80_0_zWN.root",
  sampleBaseDir+"/pat/PATtuple_81_0_Iud.root",
  sampleBaseDir+"/pat/PATtuple_82_0_HHd.root",
  sampleBaseDir+"/pat/PATtuple_83_0_Dh0.root",
  sampleBaseDir+"/pat/PATtuple_84_0_GSv.root",
  sampleBaseDir+"/pat/PATtuple_85_0_nyU.root",
  sampleBaseDir+"/pat/PATtuple_86_0_Bie.root",
  sampleBaseDir+"/pat/PATtuple_87_0_ckO.root",
  sampleBaseDir+"/pat/PATtuple_88_0_RKW.root",
  sampleBaseDir+"/pat/PATtuple_89_1_zvf.root",
  sampleBaseDir+"/pat/PATtuple_90_0_EEj.root",
  sampleBaseDir+"/pat/PATtuple_91_0_yP1.root",
  sampleBaseDir+"/pat/PATtuple_92_0_aK5.root",
  sampleBaseDir+"/pat/PATtuple_93_0_b5H.root",
  sampleBaseDir+"/pat/PATtuple_94_0_id9.root",
  sampleBaseDir+"/pat/PATtuple_95_0_Ynb.root",
  sampleBaseDir+"/pat/PATtuple_96_0_Tb9.root",
  sampleBaseDir+"/pat/PATtuple_97_0_We9.root",
  sampleBaseDir+"/pat/PATtuple_98_0_AxM.root",
  sampleBaseDir+"/pat/PATtuple_99_1_vBO.root",
  sampleBaseDir+"/pat/PATtuple_100_0_yNu.root",
  sampleBaseDir+"/pat/PATtuple_101_1_tpP.root",
  sampleBaseDir+"/pat/PATtuple_102_1_yYz.root",
  sampleBaseDir+"/pat/PATtuple_103_1_yEi.root",
  sampleBaseDir+"/pat/PATtuple_104_1_2Ml.root",
  sampleBaseDir+"/pat/PATtuple_105_1_Kuy.root",
  sampleBaseDir+"/pat/PATtuple_106_1_1yA.root",
  sampleBaseDir+"/pat/PATtuple_107_1_k31.root",
  sampleBaseDir+"/pat/PATtuple_108_1_q3N.root",
  sampleBaseDir+"/pat/PATtuple_109_1_O3n.root",
  sampleBaseDir+"/pat/PATtuple_110_1_tQf.root",
  sampleBaseDir+"/pat/PATtuple_111_1_5hs.root",
  sampleBaseDir+"/pat/PATtuple_112_1_Xt6.root",
  sampleBaseDir+"/pat/PATtuple_113_1_BZz.root"
]
