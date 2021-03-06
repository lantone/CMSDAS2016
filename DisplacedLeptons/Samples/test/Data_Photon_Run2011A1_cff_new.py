sampleDataSet = '/Photon/Run2011A-May10ReReco-v1/AOD'
sampleNumEvents = 16323959 # according to DBS, 18 June 2011

# global tag needs to be chosen to match release, trigger menu and alignment conditions.
# see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
sampleGlobalTag = 'GR_R_42_V18::All'
sampleHLTProcess = '*'

# data quality run/lumi section selection
sampleJSON = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions11/7TeV/Reprocessing/Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON.txt"

# restrict run range (mainly to get a sample with consistent trigger configuration)
sampleRunRange = [160000,999999]

# use checkAllFilesOpened whenever possible, and noDuplicateCheck when necessary
sampleDuplicateCheckMode = "checkAllFilesOpened"

# "DATA" or "MC"
sampleType = "DATA"

sampleRelease = "CMSSW_4_2_3" # original (i.e. RECO file) release,
                              # not the one we plan to process them with

sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/Data_Mu_Run2011A1"
sampleRecoFiles = []

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_yKI.root",
  sampleBaseDir+"/pat/PATtuple_2_1_WZH.root",
  sampleBaseDir+"/pat/PATtuple_3_1_KCO.root",
  sampleBaseDir+"/pat/PATtuple_4_1_q0k.root",
  sampleBaseDir+"/pat/PATtuple_5_1_6lQ.root",
  sampleBaseDir+"/pat/PATtuple_6_1_tta.root",
  sampleBaseDir+"/pat/PATtuple_7_1_ydj.root",
  sampleBaseDir+"/pat/PATtuple_8_1_PP9.root",
  sampleBaseDir+"/pat/PATtuple_9_1_lDW.root",
  sampleBaseDir+"/pat/PATtuple_10_1_JA5.root",
  sampleBaseDir+"/pat/PATtuple_11_1_16K.root",
  sampleBaseDir+"/pat/PATtuple_12_1_OFC.root",
  sampleBaseDir+"/pat/PATtuple_13_1_3Kp.root",
  sampleBaseDir+"/pat/PATtuple_14_1_bMm.root",
  sampleBaseDir+"/pat/PATtuple_15_1_x7E.root",
  sampleBaseDir+"/pat/PATtuple_16_1_d9p.root",
  sampleBaseDir+"/pat/PATtuple_17_1_dIJ.root",
  sampleBaseDir+"/pat/PATtuple_18_1_QZf.root",
  sampleBaseDir+"/pat/PATtuple_19_1_hKN.root",
  sampleBaseDir+"/pat/PATtuple_20_1_S1o.root",
  sampleBaseDir+"/pat/PATtuple_21_1_vhH.root",
  sampleBaseDir+"/pat/PATtuple_22_1_Jja.root",
  sampleBaseDir+"/pat/PATtuple_23_1_CYS.root",
  sampleBaseDir+"/pat/PATtuple_24_1_TMl.root",
  sampleBaseDir+"/pat/PATtuple_25_1_BdN.root",
  sampleBaseDir+"/pat/PATtuple_26_1_dn8.root",
  sampleBaseDir+"/pat/PATtuple_27_1_5Kl.root",
  sampleBaseDir+"/pat/PATtuple_28_1_mSf.root",
  sampleBaseDir+"/pat/PATtuple_29_1_OKo.root",
  sampleBaseDir+"/pat/PATtuple_30_1_HM6.root",
  sampleBaseDir+"/pat/PATtuple_31_1_J1Y.root",
  sampleBaseDir+"/pat/PATtuple_32_1_6yH.root",
  sampleBaseDir+"/pat/PATtuple_33_1_prE.root",
  sampleBaseDir+"/pat/PATtuple_34_1_ShU.root",
  sampleBaseDir+"/pat/PATtuple_35_1_n5H.root",
  sampleBaseDir+"/pat/PATtuple_36_1_zPJ.root",
  sampleBaseDir+"/pat/PATtuple_37_1_0O7.root",
  sampleBaseDir+"/pat/PATtuple_38_1_Xtm.root",
  sampleBaseDir+"/pat/PATtuple_39_1_Ew8.root",
  sampleBaseDir+"/pat/PATtuple_40_1_2aG.root",
  sampleBaseDir+"/pat/PATtuple_41_1_ZaO.root",
  sampleBaseDir+"/pat/PATtuple_42_1_R1i.root",
  sampleBaseDir+"/pat/PATtuple_43_1_ypu.root",
  sampleBaseDir+"/pat/PATtuple_44_1_QTk.root",
  sampleBaseDir+"/pat/PATtuple_45_1_ID4.root",
  sampleBaseDir+"/pat/PATtuple_46_1_VuA.root",
  sampleBaseDir+"/pat/PATtuple_47_1_2Zo.root",
  sampleBaseDir+"/pat/PATtuple_48_1_bdW.root",
  sampleBaseDir+"/pat/PATtuple_49_1_Hnt.root",
  sampleBaseDir+"/pat/PATtuple_50_1_wFw.root",
  sampleBaseDir+"/pat/PATtuple_51_1_enU.root",
  sampleBaseDir+"/pat/PATtuple_52_1_de1.root",
  sampleBaseDir+"/pat/PATtuple_53_1_HQl.root",
  sampleBaseDir+"/pat/PATtuple_54_1_Mwu.root",
  sampleBaseDir+"/pat/PATtuple_55_1_RZF.root",
  sampleBaseDir+"/pat/PATtuple_56_1_6HA.root",
  sampleBaseDir+"/pat/PATtuple_57_1_ZrU.root",
  sampleBaseDir+"/pat/PATtuple_58_1_uZE.root",
  sampleBaseDir+"/pat/PATtuple_59_1_RLk.root",
  sampleBaseDir+"/pat/PATtuple_60_1_Vox.root",
  sampleBaseDir+"/pat/PATtuple_61_1_Sge.root",
  sampleBaseDir+"/pat/PATtuple_62_1_k6v.root",
  sampleBaseDir+"/pat/PATtuple_63_1_SYq.root",
  sampleBaseDir+"/pat/PATtuple_64_1_obU.root",
  sampleBaseDir+"/pat/PATtuple_65_1_71V.root",
  sampleBaseDir+"/pat/PATtuple_66_1_3EP.root",
  sampleBaseDir+"/pat/PATtuple_67_1_lHX.root",
  sampleBaseDir+"/pat/PATtuple_68_1_Jts.root",
  sampleBaseDir+"/pat/PATtuple_69_1_zeU.root",
  sampleBaseDir+"/pat/PATtuple_70_1_Yr3.root",
  sampleBaseDir+"/pat/PATtuple_71_1_sAP.root",
  sampleBaseDir+"/pat/PATtuple_72_1_10p.root",
  sampleBaseDir+"/pat/PATtuple_73_1_0Bh.root",
  sampleBaseDir+"/pat/PATtuple_74_1_N7T.root",
  sampleBaseDir+"/pat/PATtuple_75_1_RNR.root",
  sampleBaseDir+"/pat/PATtuple_76_1_rbs.root",
  sampleBaseDir+"/pat/PATtuple_77_1_F7x.root",
  sampleBaseDir+"/pat/PATtuple_78_1_v9T.root",
  sampleBaseDir+"/pat/PATtuple_79_1_CEg.root",
  sampleBaseDir+"/pat/PATtuple_80_1_kob.root",
  sampleBaseDir+"/pat/PATtuple_81_1_HUW.root",
  sampleBaseDir+"/pat/PATtuple_82_1_h3w.root",
  sampleBaseDir+"/pat/PATtuple_83_1_RsJ.root",
  sampleBaseDir+"/pat/PATtuple_84_1_2tR.root",
  sampleBaseDir+"/pat/PATtuple_85_1_0mF.root",
  sampleBaseDir+"/pat/PATtuple_86_1_atP.root",
  sampleBaseDir+"/pat/PATtuple_87_1_fv7.root",
  sampleBaseDir+"/pat/PATtuple_88_1_04E.root",
  sampleBaseDir+"/pat/PATtuple_89_1_IQm.root",
  sampleBaseDir+"/pat/PATtuple_90_1_wAD.root",
  sampleBaseDir+"/pat/PATtuple_91_1_Bn1.root",
  sampleBaseDir+"/pat/PATtuple_92_1_q99.root",
  sampleBaseDir+"/pat/PATtuple_93_1_FFf.root",
  sampleBaseDir+"/pat/PATtuple_94_1_Jvx.root",
  sampleBaseDir+"/pat/PATtuple_95_1_Gcr.root",
  sampleBaseDir+"/pat/PATtuple_96_1_rRN.root",
  sampleBaseDir+"/pat/PATtuple_97_1_rqH.root",
  sampleBaseDir+"/pat/PATtuple_98_1_YyF.root",
  sampleBaseDir+"/pat/PATtuple_99_1_cRD.root",
  sampleBaseDir+"/pat/PATtuple_100_1_2mW.root",
  sampleBaseDir+"/pat/PATtuple_101_1_M5J.root",
  sampleBaseDir+"/pat/PATtuple_102_1_kf0.root",
  sampleBaseDir+"/pat/PATtuple_103_1_KuQ.root",
  sampleBaseDir+"/pat/PATtuple_104_1_7GA.root",
  sampleBaseDir+"/pat/PATtuple_105_1_QM6.root",
  sampleBaseDir+"/pat/PATtuple_106_1_bxt.root",
  sampleBaseDir+"/pat/PATtuple_107_1_fHK.root",
  sampleBaseDir+"/pat/PATtuple_108_1_7eJ.root",
  sampleBaseDir+"/pat/PATtuple_109_1_CfK.root",
  sampleBaseDir+"/pat/PATtuple_110_1_FKc.root",
  sampleBaseDir+"/pat/PATtuple_111_1_tnX.root",
  sampleBaseDir+"/pat/PATtuple_112_1_LqO.root",
  sampleBaseDir+"/pat/PATtuple_113_1_YvS.root",
  sampleBaseDir+"/pat/PATtuple_114_1_NCH.root",
  sampleBaseDir+"/pat/PATtuple_115_1_psP.root",
  sampleBaseDir+"/pat/PATtuple_116_1_Ksn.root",
  sampleBaseDir+"/pat/PATtuple_117_1_LN6.root",
  sampleBaseDir+"/pat/PATtuple_118_1_GEH.root",
  sampleBaseDir+"/pat/PATtuple_119_1_Fnn.root",
  sampleBaseDir+"/pat/PATtuple_120_1_VJI.root",
  sampleBaseDir+"/pat/PATtuple_121_1_e3Y.root",
  sampleBaseDir+"/pat/PATtuple_122_1_xvM.root",
  sampleBaseDir+"/pat/PATtuple_123_1_ZvJ.root",
  sampleBaseDir+"/pat/PATtuple_124_1_YHn.root",
  sampleBaseDir+"/pat/PATtuple_125_1_fMW.root",
  sampleBaseDir+"/pat/PATtuple_126_1_v4J.root",
  sampleBaseDir+"/pat/PATtuple_127_1_Ua4.root",
  sampleBaseDir+"/pat/PATtuple_128_1_w3E.root",
  sampleBaseDir+"/pat/PATtuple_129_1_SWA.root",
  sampleBaseDir+"/pat/PATtuple_130_1_EeY.root",
  sampleBaseDir+"/pat/PATtuple_131_1_60i.root",
  sampleBaseDir+"/pat/PATtuple_132_1_N57.root",
  sampleBaseDir+"/pat/PATtuple_133_1_0t8.root",
  sampleBaseDir+"/pat/PATtuple_134_1_7vB.root",
  sampleBaseDir+"/pat/PATtuple_135_1_myq.root",
  sampleBaseDir+"/pat/PATtuple_136_1_Mve.root",
  sampleBaseDir+"/pat/PATtuple_137_1_E6Z.root",
  sampleBaseDir+"/pat/PATtuple_138_1_oa2.root",
  sampleBaseDir+"/pat/PATtuple_139_1_rmj.root",
  sampleBaseDir+"/pat/PATtuple_140_1_A4o.root",
  sampleBaseDir+"/pat/PATtuple_141_1_2Sl.root",
  sampleBaseDir+"/pat/PATtuple_142_1_IVx.root",
  sampleBaseDir+"/pat/PATtuple_143_1_Bf3.root",
  sampleBaseDir+"/pat/PATtuple_144_1_0k0.root",
  sampleBaseDir+"/pat/PATtuple_145_1_3jt.root",
  sampleBaseDir+"/pat/PATtuple_146_1_Aei.root",
  sampleBaseDir+"/pat/PATtuple_147_1_10Y.root",
  sampleBaseDir+"/pat/PATtuple_148_1_nNd.root",
  sampleBaseDir+"/pat/PATtuple_149_1_auB.root",
  sampleBaseDir+"/pat/PATtuple_150_1_hJx.root",
  sampleBaseDir+"/pat/PATtuple_151_1_bsB.root",
  sampleBaseDir+"/pat/PATtuple_152_1_40R.root",
  sampleBaseDir+"/pat/PATtuple_153_1_mmw.root",
  sampleBaseDir+"/pat/PATtuple_154_1_dra.root",
  sampleBaseDir+"/pat/PATtuple_155_1_f2t.root",
  sampleBaseDir+"/pat/PATtuple_156_1_a8k.root",
  sampleBaseDir+"/pat/PATtuple_157_1_S2G.root",
  sampleBaseDir+"/pat/PATtuple_158_1_TYY.root",
  sampleBaseDir+"/pat/PATtuple_159_1_edD.root",
  sampleBaseDir+"/pat/PATtuple_160_1_dmL.root",
  sampleBaseDir+"/pat/PATtuple_161_1_iGS.root",
  sampleBaseDir+"/pat/PATtuple_162_1_LJD.root",
  sampleBaseDir+"/pat/PATtuple_163_1_q45.root",
  sampleBaseDir+"/pat/PATtuple_164_1_SCS.root",
  sampleBaseDir+"/pat/PATtuple_165_1_LpQ.root",
  sampleBaseDir+"/pat/PATtuple_166_1_fJA.root",
  sampleBaseDir+"/pat/PATtuple_167_1_1Zk.root",
  sampleBaseDir+"/pat/PATtuple_168_1_Ffa.root",
  sampleBaseDir+"/pat/PATtuple_169_1_EPj.root",
  sampleBaseDir+"/pat/PATtuple_170_1_VOX.root",
  sampleBaseDir+"/pat/PATtuple_171_1_2g5.root",
  sampleBaseDir+"/pat/PATtuple_172_1_cIo.root",
  sampleBaseDir+"/pat/PATtuple_173_1_mlm.root",
  sampleBaseDir+"/pat/PATtuple_174_1_NKx.root",
  sampleBaseDir+"/pat/PATtuple_175_1_V4o.root",
  sampleBaseDir+"/pat/PATtuple_176_1_FSo.root",
  sampleBaseDir+"/pat/PATtuple_177_1_Z4e.root",
  sampleBaseDir+"/pat/PATtuple_178_1_tmk.root",
  sampleBaseDir+"/pat/PATtuple_179_1_tKo.root",
  sampleBaseDir+"/pat/PATtuple_180_1_ZTR.root",
  sampleBaseDir+"/pat/PATtuple_181_1_axf.root",
  sampleBaseDir+"/pat/PATtuple_182_1_ZiE.root",
  sampleBaseDir+"/pat/PATtuple_183_1_Gzc.root",
  sampleBaseDir+"/pat/PATtuple_184_1_XQI.root",
  sampleBaseDir+"/pat/PATtuple_185_1_oIU.root",
  sampleBaseDir+"/pat/PATtuple_186_1_feD.root",
  sampleBaseDir+"/pat/PATtuple_187_1_qGn.root",
  sampleBaseDir+"/pat/PATtuple_188_1_cjU.root",
  sampleBaseDir+"/pat/PATtuple_189_1_Eq0.root",
  sampleBaseDir+"/pat/PATtuple_190_1_9g7.root",
  sampleBaseDir+"/pat/PATtuple_191_1_Kik.root",
  sampleBaseDir+"/pat/PATtuple_192_1_drj.root",
  sampleBaseDir+"/pat/PATtuple_193_1_aCw.root",
  sampleBaseDir+"/pat/PATtuple_194_1_url.root",
  sampleBaseDir+"/pat/PATtuple_195_1_Lc1.root",
  sampleBaseDir+"/pat/PATtuple_196_1_RCJ.root",
  sampleBaseDir+"/pat/PATtuple_197_1_wNQ.root",
  sampleBaseDir+"/pat/PATtuple_198_1_U8F.root",
  sampleBaseDir+"/pat/PATtuple_199_1_wmk.root",
  sampleBaseDir+"/pat/PATtuple_200_1_moY.root",
  sampleBaseDir+"/pat/PATtuple_201_1_dsF.root",
  sampleBaseDir+"/pat/PATtuple_202_1_ZNz.root",
  sampleBaseDir+"/pat/PATtuple_203_1_Yz2.root",
  sampleBaseDir+"/pat/PATtuple_204_1_6k9.root",
  sampleBaseDir+"/pat/PATtuple_205_1_pZ2.root",
  sampleBaseDir+"/pat/PATtuple_206_1_sRp.root",
  sampleBaseDir+"/pat/PATtuple_207_1_0rv.root",
  sampleBaseDir+"/pat/PATtuple_208_1_sgm.root",
  sampleBaseDir+"/pat/PATtuple_209_1_qHf.root",
  sampleBaseDir+"/pat/PATtuple_210_1_hum.root",
  sampleBaseDir+"/pat/PATtuple_211_1_qj6.root",
  sampleBaseDir+"/pat/PATtuple_212_1_IF2.root",
  sampleBaseDir+"/pat/PATtuple_213_1_j98.root",
  sampleBaseDir+"/pat/PATtuple_214_1_42G.root",
  sampleBaseDir+"/pat/PATtuple_215_1_2vx.root",
  sampleBaseDir+"/pat/PATtuple_216_1_ABv.root",
  sampleBaseDir+"/pat/PATtuple_217_1_rrY.root",
  sampleBaseDir+"/pat/PATtuple_218_1_kdI.root",
  sampleBaseDir+"/pat/PATtuple_219_1_AoF.root",
  sampleBaseDir+"/pat/PATtuple_220_1_MgH.root",
  sampleBaseDir+"/pat/PATtuple_221_1_Bs1.root",
  sampleBaseDir+"/pat/PATtuple_222_1_8Si.root",
  sampleBaseDir+"/pat/PATtuple_223_1_IFM.root",
  sampleBaseDir+"/pat/PATtuple_224_1_JQv.root",
  sampleBaseDir+"/pat/PATtuple_225_1_B6n.root",
  sampleBaseDir+"/pat/PATtuple_226_1_Eeh.root",
  sampleBaseDir+"/pat/PATtuple_227_1_nLo.root",
  sampleBaseDir+"/pat/PATtuple_228_1_Kvt.root",
  sampleBaseDir+"/pat/PATtuple_229_1_Lei.root",
  sampleBaseDir+"/pat/PATtuple_230_1_SQE.root",
  sampleBaseDir+"/pat/PATtuple_231_1_vnW.root",
  sampleBaseDir+"/pat/PATtuple_232_1_E43.root",
  sampleBaseDir+"/pat/PATtuple_233_1_NzI.root",
  sampleBaseDir+"/pat/PATtuple_234_1_qHQ.root",
  sampleBaseDir+"/pat/PATtuple_235_1_9AU.root",
  sampleBaseDir+"/pat/PATtuple_236_1_GNv.root",
  sampleBaseDir+"/pat/PATtuple_237_1_RXN.root",
  sampleBaseDir+"/pat/PATtuple_238_1_1Qt.root",
  sampleBaseDir+"/pat/PATtuple_239_1_5u0.root",
  sampleBaseDir+"/pat/PATtuple_240_1_whN.root",
  sampleBaseDir+"/pat/PATtuple_241_1_2xR.root",
  sampleBaseDir+"/pat/PATtuple_242_1_Tza.root",
  sampleBaseDir+"/pat/PATtuple_243_1_t4P.root",
  sampleBaseDir+"/pat/PATtuple_244_1_9EY.root",
  sampleBaseDir+"/pat/PATtuple_245_1_1G1.root",
  sampleBaseDir+"/pat/PATtuple_246_1_QM1.root",
  sampleBaseDir+"/pat/PATtuple_247_1_igB.root",
  sampleBaseDir+"/pat/PATtuple_248_1_JY8.root",
  sampleBaseDir+"/pat/PATtuple_249_1_dpf.root",
  sampleBaseDir+"/pat/PATtuple_250_1_HgK.root",
  sampleBaseDir+"/pat/PATtuple_251_1_GHR.root",
  sampleBaseDir+"/pat/PATtuple_252_1_4qS.root",
  sampleBaseDir+"/pat/PATtuple_253_1_4t0.root",
  sampleBaseDir+"/pat/PATtuple_254_1_fAW.root",
  sampleBaseDir+"/pat/PATtuple_255_1_jqT.root",
  sampleBaseDir+"/pat/PATtuple_256_1_UbY.root",
  sampleBaseDir+"/pat/PATtuple_257_1_rhC.root",
  sampleBaseDir+"/pat/PATtuple_258_1_HLc.root",
  sampleBaseDir+"/pat/PATtuple_259_1_rTe.root",
  sampleBaseDir+"/pat/PATtuple_260_1_Kat.root",
  sampleBaseDir+"/pat/PATtuple_261_1_kyx.root",
  sampleBaseDir+"/pat/PATtuple_262_1_JHM.root",
  sampleBaseDir+"/pat/PATtuple_263_1_fST.root",
  sampleBaseDir+"/pat/PATtuple_264_1_akM.root",
  sampleBaseDir+"/pat/PATtuple_265_1_S9b.root",
  sampleBaseDir+"/pat/PATtuple_266_1_O6C.root",
  sampleBaseDir+"/pat/PATtuple_267_1_pAX.root",
  sampleBaseDir+"/pat/PATtuple_268_1_j17.root",
  sampleBaseDir+"/pat/PATtuple_269_1_PQ8.root",
  sampleBaseDir+"/pat/PATtuple_270_1_7t0.root",
  sampleBaseDir+"/pat/PATtuple_271_1_kLM.root",
  sampleBaseDir+"/pat/PATtuple_272_1_dmD.root",
  sampleBaseDir+"/pat/PATtuple_273_1_w0p.root",
  sampleBaseDir+"/pat/PATtuple_274_1_G0G.root",
  sampleBaseDir+"/pat/PATtuple_275_1_FrQ.root",
  sampleBaseDir+"/pat/PATtuple_276_1_9Uc.root",
  sampleBaseDir+"/pat/PATtuple_277_1_Ol2.root",
  sampleBaseDir+"/pat/PATtuple_278_1_JwQ.root",
  sampleBaseDir+"/pat/PATtuple_279_1_hEM.root",
  sampleBaseDir+"/pat/PATtuple_280_1_2GO.root",
  sampleBaseDir+"/pat/PATtuple_281_1_4CI.root",
  sampleBaseDir+"/pat/PATtuple_282_1_H39.root",
  sampleBaseDir+"/pat/PATtuple_283_1_Wix.root",
  sampleBaseDir+"/pat/PATtuple_284_1_1zF.root",
  sampleBaseDir+"/pat/PATtuple_285_1_UgE.root",
  sampleBaseDir+"/pat/PATtuple_286_1_3yF.root",
  sampleBaseDir+"/pat/PATtuple_287_1_258.root",
  sampleBaseDir+"/pat/PATtuple_288_1_7qB.root",
  sampleBaseDir+"/pat/PATtuple_289_1_wov.root",
  sampleBaseDir+"/pat/PATtuple_290_1_ti9.root",
  sampleBaseDir+"/pat/PATtuple_291_1_D8B.root",
  sampleBaseDir+"/pat/PATtuple_292_1_E9N.root",
  sampleBaseDir+"/pat/PATtuple_293_1_pwN.root",
  sampleBaseDir+"/pat/PATtuple_294_1_Vo0.root",
  sampleBaseDir+"/pat/PATtuple_295_1_CI5.root",
  sampleBaseDir+"/pat/PATtuple_296_1_TLx.root",
  sampleBaseDir+"/pat/PATtuple_297_1_YG9.root"
]
