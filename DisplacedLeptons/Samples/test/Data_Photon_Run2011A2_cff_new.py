sampleDataSet = '/Photon/Run2011A-PromptReco-v4/AOD'
sampleNumEvents = 35611946 # according to DBS, 04 July 2011

# global tag needs to be chosen to match release, trigger menu and alignment conditions.
# see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
sampleGlobalTag = 'GR_R_42_V18::All'
sampleHLTProcess = '*'

# data quality run/lumi section selection
sampleJSON = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions11/7TeV/Prompt/Cert_160404-170307_7TeV_PromptReco_Collisions11_JSON.txt"

# restrict run range (mainly to get a sample with consistent trigger configuration)
sampleRunRange = [160000,999999]

# use checkAllFilesOpened whenever possible, and noDuplicateCheck when necessary
sampleDuplicateCheckMode = "checkAllFilesOpened"

# "DATA" or "MC"
sampleType = "DATA"

sampleRelease = "CMSSW_4_2_7" # original (i.e. RECO file) release,
                              # not the one we plan to process them with

sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/Data_Mu_Run2011A1"
sampleRecoFiles = []

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_3N6.root",
  sampleBaseDir+"/pat/PATtuple_2_1_NEy.root",
  sampleBaseDir+"/pat/PATtuple_3_1_RMc.root",
  sampleBaseDir+"/pat/PATtuple_4_1_skf.root",
  sampleBaseDir+"/pat/PATtuple_5_0_gev.root",
  sampleBaseDir+"/pat/PATtuple_6_0_Wl6.root",
  sampleBaseDir+"/pat/PATtuple_7_0_6AB.root",
  sampleBaseDir+"/pat/PATtuple_8_0_1IT.root",
  sampleBaseDir+"/pat/PATtuple_9_0_4I2.root",
  sampleBaseDir+"/pat/PATtuple_10_0_EyC.root",
  sampleBaseDir+"/pat/PATtuple_11_0_aMN.root",
  sampleBaseDir+"/pat/PATtuple_12_0_ANM.root",
  sampleBaseDir+"/pat/PATtuple_13_0_wWZ.root",
  sampleBaseDir+"/pat/PATtuple_14_0_W3g.root",
  sampleBaseDir+"/pat/PATtuple_15_1_Gyr.root",
  sampleBaseDir+"/pat/PATtuple_16_1_fhn.root",
  sampleBaseDir+"/pat/PATtuple_17_1_DQV.root",
  sampleBaseDir+"/pat/PATtuple_18_1_468.root",
  sampleBaseDir+"/pat/PATtuple_19_1_QUX.root",
  sampleBaseDir+"/pat/PATtuple_20_1_kri.root",
  sampleBaseDir+"/pat/PATtuple_21_1_J96.root",
  sampleBaseDir+"/pat/PATtuple_22_1_U1R.root",
  sampleBaseDir+"/pat/PATtuple_23_1_mJJ.root",
  sampleBaseDir+"/pat/PATtuple_24_1_wra.root",
  sampleBaseDir+"/pat/PATtuple_25_1_hk4.root",
  sampleBaseDir+"/pat/PATtuple_26_1_42t.root",
  sampleBaseDir+"/pat/PATtuple_27_1_K8u.root",
  sampleBaseDir+"/pat/PATtuple_28_1_Mjs.root",
  sampleBaseDir+"/pat/PATtuple_29_0_JKi.root",
  sampleBaseDir+"/pat/PATtuple_30_0_Fab.root",
  sampleBaseDir+"/pat/PATtuple_31_0_sKf.root",
  sampleBaseDir+"/pat/PATtuple_32_0_Cvb.root",
  sampleBaseDir+"/pat/PATtuple_33_0_B0y.root",
  sampleBaseDir+"/pat/PATtuple_34_0_qg8.root",
  sampleBaseDir+"/pat/PATtuple_35_0_yQA.root",
  sampleBaseDir+"/pat/PATtuple_36_0_GYg.root",
  sampleBaseDir+"/pat/PATtuple_37_0_IUm.root",
  sampleBaseDir+"/pat/PATtuple_38_0_LFs.root",
  sampleBaseDir+"/pat/PATtuple_39_0_X0R.root",
  sampleBaseDir+"/pat/PATtuple_40_0_YBa.root",
  sampleBaseDir+"/pat/PATtuple_41_0_oU0.root",
  sampleBaseDir+"/pat/PATtuple_42_0_Hu4.root",
  sampleBaseDir+"/pat/PATtuple_43_0_mfN.root",
  sampleBaseDir+"/pat/PATtuple_44_0_xpd.root",
  sampleBaseDir+"/pat/PATtuple_45_0_BwQ.root",
  sampleBaseDir+"/pat/PATtuple_46_0_94C.root",
  sampleBaseDir+"/pat/PATtuple_47_0_kui.root",
  sampleBaseDir+"/pat/PATtuple_48_0_HJh.root",
  sampleBaseDir+"/pat/PATtuple_49_0_5v3.root",
  sampleBaseDir+"/pat/PATtuple_50_0_MFf.root",
  sampleBaseDir+"/pat/PATtuple_51_0_7EW.root",
  sampleBaseDir+"/pat/PATtuple_52_0_NVH.root",
  sampleBaseDir+"/pat/PATtuple_53_1_c0R.root",
  sampleBaseDir+"/pat/PATtuple_54_1_sfO.root",
  sampleBaseDir+"/pat/PATtuple_55_1_Zeu.root",
  sampleBaseDir+"/pat/PATtuple_56_1_WkG.root",
  sampleBaseDir+"/pat/PATtuple_57_1_nue.root",
  sampleBaseDir+"/pat/PATtuple_58_1_PPA.root",
  sampleBaseDir+"/pat/PATtuple_59_1_8nu.root",
  sampleBaseDir+"/pat/PATtuple_60_1_fcy.root",
  sampleBaseDir+"/pat/PATtuple_61_1_upo.root",
  sampleBaseDir+"/pat/PATtuple_62_1_n2B.root",
  sampleBaseDir+"/pat/PATtuple_63_1_hfD.root",
  sampleBaseDir+"/pat/PATtuple_64_0_1eG.root",
  sampleBaseDir+"/pat/PATtuple_65_0_9NK.root",
  sampleBaseDir+"/pat/PATtuple_66_0_cmo.root",
  sampleBaseDir+"/pat/PATtuple_67_1_Nar.root",
  sampleBaseDir+"/pat/PATtuple_68_1_nCg.root",
  sampleBaseDir+"/pat/PATtuple_69_1_YBC.root",
  sampleBaseDir+"/pat/PATtuple_70_1_IOj.root",
  sampleBaseDir+"/pat/PATtuple_71_1_TiH.root",
  sampleBaseDir+"/pat/PATtuple_72_1_RWV.root",
  sampleBaseDir+"/pat/PATtuple_73_1_gTy.root",
  sampleBaseDir+"/pat/PATtuple_74_1_CoB.root",
  sampleBaseDir+"/pat/PATtuple_75_1_wU4.root",
  sampleBaseDir+"/pat/PATtuple_76_1_EkL.root",
  sampleBaseDir+"/pat/PATtuple_77_1_cfv.root",
  sampleBaseDir+"/pat/PATtuple_78_1_v31.root",
  sampleBaseDir+"/pat/PATtuple_79_1_SCq.root",
  sampleBaseDir+"/pat/PATtuple_80_0_YzF.root",
  sampleBaseDir+"/pat/PATtuple_81_0_MjJ.root",
  sampleBaseDir+"/pat/PATtuple_82_0_ixL.root",
  sampleBaseDir+"/pat/PATtuple_83_0_YZg.root",
  sampleBaseDir+"/pat/PATtuple_84_0_OL9.root",
  sampleBaseDir+"/pat/PATtuple_85_0_3k1.root",
  sampleBaseDir+"/pat/PATtuple_86_0_zDb.root",
  sampleBaseDir+"/pat/PATtuple_87_0_nes.root",
  sampleBaseDir+"/pat/PATtuple_88_1_LRv.root",
  sampleBaseDir+"/pat/PATtuple_89_1_vP3.root",
  sampleBaseDir+"/pat/PATtuple_90_1_6KH.root",
  sampleBaseDir+"/pat/PATtuple_91_1_YCF.root",
  sampleBaseDir+"/pat/PATtuple_92_1_bwG.root",
  sampleBaseDir+"/pat/PATtuple_93_1_btc.root",
  sampleBaseDir+"/pat/PATtuple_94_1_BQ5.root",
  sampleBaseDir+"/pat/PATtuple_95_1_I2v.root",
  sampleBaseDir+"/pat/PATtuple_96_1_iH6.root",
  sampleBaseDir+"/pat/PATtuple_97_1_pvo.root",
  sampleBaseDir+"/pat/PATtuple_98_1_Ico.root",
  sampleBaseDir+"/pat/PATtuple_99_1_fSG.root",
  sampleBaseDir+"/pat/PATtuple_100_0_xxr.root",
  sampleBaseDir+"/pat/PATtuple_101_0_9bv.root",
  sampleBaseDir+"/pat/PATtuple_102_0_tJ1.root",
  sampleBaseDir+"/pat/PATtuple_103_0_8tI.root",
  sampleBaseDir+"/pat/PATtuple_104_1_anD.root",
  sampleBaseDir+"/pat/PATtuple_105_1_Q0R.root",
  sampleBaseDir+"/pat/PATtuple_106_1_fnw.root",
  sampleBaseDir+"/pat/PATtuple_107_1_JbZ.root",
  sampleBaseDir+"/pat/PATtuple_108_1_RxQ.root",
  sampleBaseDir+"/pat/PATtuple_109_1_BIc.root",
  sampleBaseDir+"/pat/PATtuple_110_1_Bt4.root",
  sampleBaseDir+"/pat/PATtuple_111_1_0q0.root",
  sampleBaseDir+"/pat/PATtuple_112_1_Aiq.root",
  sampleBaseDir+"/pat/PATtuple_113_1_Q0Y.root",
  sampleBaseDir+"/pat/PATtuple_114_1_WBb.root",
  sampleBaseDir+"/pat/PATtuple_115_1_3Vx.root",
  sampleBaseDir+"/pat/PATtuple_116_1_NFL.root",
  sampleBaseDir+"/pat/PATtuple_117_1_WIw.root",
  sampleBaseDir+"/pat/PATtuple_118_1_Y2H.root",
  sampleBaseDir+"/pat/PATtuple_119_1_lMf.root",
  sampleBaseDir+"/pat/PATtuple_120_1_D0V.root",
  sampleBaseDir+"/pat/PATtuple_121_1_m9n.root",
  sampleBaseDir+"/pat/PATtuple_122_1_jOo.root",
  sampleBaseDir+"/pat/PATtuple_123_1_K2p.root",
  sampleBaseDir+"/pat/PATtuple_124_1_AIt.root",
  sampleBaseDir+"/pat/PATtuple_125_1_8yv.root",
  sampleBaseDir+"/pat/PATtuple_126_1_qvr.root",
  sampleBaseDir+"/pat/PATtuple_127_1_zvc.root",
  sampleBaseDir+"/pat/PATtuple_128_1_Con.root",
  sampleBaseDir+"/pat/PATtuple_129_1_XGo.root",
  sampleBaseDir+"/pat/PATtuple_130_1_TfH.root",
  sampleBaseDir+"/pat/PATtuple_131_1_Ozh.root",
  sampleBaseDir+"/pat/PATtuple_132_0_g2H.root",
  sampleBaseDir+"/pat/PATtuple_133_1_LSo.root",
  sampleBaseDir+"/pat/PATtuple_134_1_7eN.root",
  sampleBaseDir+"/pat/PATtuple_135_1_1Xm.root",
  sampleBaseDir+"/pat/PATtuple_136_1_2aE.root",
  sampleBaseDir+"/pat/PATtuple_137_1_J7N.root",
  sampleBaseDir+"/pat/PATtuple_138_1_vNy.root",
  sampleBaseDir+"/pat/PATtuple_139_1_ffV.root",
  sampleBaseDir+"/pat/PATtuple_140_1_uqS.root",
  sampleBaseDir+"/pat/PATtuple_141_1_5pm.root",
  sampleBaseDir+"/pat/PATtuple_142_1_CIx.root",
  sampleBaseDir+"/pat/PATtuple_143_1_sI4.root",
  sampleBaseDir+"/pat/PATtuple_144_1_mDe.root",
  sampleBaseDir+"/pat/PATtuple_145_1_Yi4.root",
  sampleBaseDir+"/pat/PATtuple_146_1_klr.root",
  sampleBaseDir+"/pat/PATtuple_147_1_sep.root",
  sampleBaseDir+"/pat/PATtuple_148_1_zSf.root",
  sampleBaseDir+"/pat/PATtuple_149_1_6rZ.root",
  sampleBaseDir+"/pat/PATtuple_150_1_OGj.root",
  sampleBaseDir+"/pat/PATtuple_151_1_fRn.root",
  sampleBaseDir+"/pat/PATtuple_152_0_V35.root",
  sampleBaseDir+"/pat/PATtuple_153_0_u17.root",
  sampleBaseDir+"/pat/PATtuple_154_0_EeY.root",
  sampleBaseDir+"/pat/PATtuple_155_0_RLC.root",
  sampleBaseDir+"/pat/PATtuple_156_0_X8A.root",
  sampleBaseDir+"/pat/PATtuple_157_0_mvJ.root",
  sampleBaseDir+"/pat/PATtuple_158_0_q3I.root",
  sampleBaseDir+"/pat/PATtuple_159_0_UpY.root",
  sampleBaseDir+"/pat/PATtuple_160_0_Ero.root",
  sampleBaseDir+"/pat/PATtuple_161_0_srJ.root",
  sampleBaseDir+"/pat/PATtuple_162_1_6NP.root",
  sampleBaseDir+"/pat/PATtuple_163_0_KrB.root",
  sampleBaseDir+"/pat/PATtuple_164_1_h21.root",
  sampleBaseDir+"/pat/PATtuple_165_1_ryo.root",
  sampleBaseDir+"/pat/PATtuple_166_0_7jC.root",
  sampleBaseDir+"/pat/PATtuple_167_0_0lP.root",
  sampleBaseDir+"/pat/PATtuple_168_0_3zG.root",
  sampleBaseDir+"/pat/PATtuple_169_0_ZDA.root",
  sampleBaseDir+"/pat/PATtuple_170_0_V5j.root",
  sampleBaseDir+"/pat/PATtuple_171_0_DGy.root",
  sampleBaseDir+"/pat/PATtuple_172_0_eZ4.root",
  sampleBaseDir+"/pat/PATtuple_173_0_NpN.root",
  sampleBaseDir+"/pat/PATtuple_174_0_4Iy.root",
  sampleBaseDir+"/pat/PATtuple_175_0_VwJ.root",
  sampleBaseDir+"/pat/PATtuple_176_0_dal.root",
  sampleBaseDir+"/pat/PATtuple_177_0_OFk.root",
  sampleBaseDir+"/pat/PATtuple_178_0_hc9.root",
  sampleBaseDir+"/pat/PATtuple_179_0_zgL.root",
  sampleBaseDir+"/pat/PATtuple_180_0_BjF.root",
  sampleBaseDir+"/pat/PATtuple_181_0_qed.root",
  sampleBaseDir+"/pat/PATtuple_182_0_wUv.root",
  sampleBaseDir+"/pat/PATtuple_183_0_JIk.root",
  sampleBaseDir+"/pat/PATtuple_184_0_ZVp.root",
  sampleBaseDir+"/pat/PATtuple_185_0_MWE.root",
  sampleBaseDir+"/pat/PATtuple_186_0_Mer.root",
  sampleBaseDir+"/pat/PATtuple_187_0_sUT.root",
  sampleBaseDir+"/pat/PATtuple_188_0_w0P.root",
  sampleBaseDir+"/pat/PATtuple_189_1_tb3.root",
  sampleBaseDir+"/pat/PATtuple_190_1_XRn.root",
  sampleBaseDir+"/pat/PATtuple_191_1_zHu.root",
  sampleBaseDir+"/pat/PATtuple_192_1_w2a.root",
  sampleBaseDir+"/pat/PATtuple_193_1_cEj.root",
  sampleBaseDir+"/pat/PATtuple_194_1_4AR.root",
  sampleBaseDir+"/pat/PATtuple_195_1_lLb.root",
  sampleBaseDir+"/pat/PATtuple_196_1_n2F.root",
  sampleBaseDir+"/pat/PATtuple_197_1_Rg8.root",
  sampleBaseDir+"/pat/PATtuple_198_1_1fy.root",
  sampleBaseDir+"/pat/PATtuple_199_1_UIG.root",
  sampleBaseDir+"/pat/PATtuple_200_1_6Eo.root",
  sampleBaseDir+"/pat/PATtuple_201_1_GJD.root",
  sampleBaseDir+"/pat/PATtuple_202_1_ybT.root",
  sampleBaseDir+"/pat/PATtuple_203_1_934.root",
  sampleBaseDir+"/pat/PATtuple_204_1_P02.root",
  sampleBaseDir+"/pat/PATtuple_205_1_pl1.root",
  sampleBaseDir+"/pat/PATtuple_206_1_onR.root",
  sampleBaseDir+"/pat/PATtuple_207_1_PaW.root",
  sampleBaseDir+"/pat/PATtuple_208_1_5xf.root",
  sampleBaseDir+"/pat/PATtuple_209_1_X8R.root",
  sampleBaseDir+"/pat/PATtuple_210_1_ILV.root",
  sampleBaseDir+"/pat/PATtuple_211_1_DJg.root",
  sampleBaseDir+"/pat/PATtuple_212_1_Ers.root",
  sampleBaseDir+"/pat/PATtuple_213_1_K69.root",
  sampleBaseDir+"/pat/PATtuple_214_1_zhd.root",
  sampleBaseDir+"/pat/PATtuple_215_1_Eho.root",
  sampleBaseDir+"/pat/PATtuple_216_1_j3m.root",
  sampleBaseDir+"/pat/PATtuple_217_1_yix.root",
  sampleBaseDir+"/pat/PATtuple_218_1_FuH.root",
  sampleBaseDir+"/pat/PATtuple_219_1_R4o.root",
  sampleBaseDir+"/pat/PATtuple_220_1_JqJ.root",
  sampleBaseDir+"/pat/PATtuple_221_0_hWz.root",
  sampleBaseDir+"/pat/PATtuple_222_0_rLP.root",
  sampleBaseDir+"/pat/PATtuple_223_0_Rss.root",
  sampleBaseDir+"/pat/PATtuple_224_1_k46.root",
  sampleBaseDir+"/pat/PATtuple_225_1_GiW.root",
  sampleBaseDir+"/pat/PATtuple_226_1_hnS.root",
  sampleBaseDir+"/pat/PATtuple_227_1_i6I.root",
  sampleBaseDir+"/pat/PATtuple_228_1_9SH.root",
  sampleBaseDir+"/pat/PATtuple_229_1_NU3.root",
  sampleBaseDir+"/pat/PATtuple_230_1_nSa.root",
  sampleBaseDir+"/pat/PATtuple_231_1_ISU.root",
  sampleBaseDir+"/pat/PATtuple_232_1_iFC.root",
  sampleBaseDir+"/pat/PATtuple_233_1_kVZ.root",
  sampleBaseDir+"/pat/PATtuple_234_1_oeP.root",
  sampleBaseDir+"/pat/PATtuple_235_1_Lo6.root",
  sampleBaseDir+"/pat/PATtuple_236_1_TaN.root",
  sampleBaseDir+"/pat/PATtuple_237_1_5Hm.root",
  sampleBaseDir+"/pat/PATtuple_238_1_DF0.root",
  sampleBaseDir+"/pat/PATtuple_239_1_fcU.root",
  sampleBaseDir+"/pat/PATtuple_240_1_5Ss.root",
  sampleBaseDir+"/pat/PATtuple_241_1_6ZG.root",
  sampleBaseDir+"/pat/PATtuple_242_1_gME.root",
  sampleBaseDir+"/pat/PATtuple_243_1_Y4d.root",
  sampleBaseDir+"/pat/PATtuple_244_1_y1l.root",
  sampleBaseDir+"/pat/PATtuple_245_1_1sb.root",
  sampleBaseDir+"/pat/PATtuple_246_1_7Nv.root",
  sampleBaseDir+"/pat/PATtuple_247_0_6vI.root",
  sampleBaseDir+"/pat/PATtuple_248_0_fxo.root",
  sampleBaseDir+"/pat/PATtuple_249_0_uWJ.root",
  sampleBaseDir+"/pat/PATtuple_250_0_ccr.root",
  sampleBaseDir+"/pat/PATtuple_251_0_t3z.root",
  sampleBaseDir+"/pat/PATtuple_252_0_wcM.root",
  sampleBaseDir+"/pat/PATtuple_253_0_sdX.root",
  sampleBaseDir+"/pat/PATtuple_254_0_C9f.root",
  sampleBaseDir+"/pat/PATtuple_255_0_k3m.root",
  sampleBaseDir+"/pat/PATtuple_256_0_SBG.root",
  sampleBaseDir+"/pat/PATtuple_257_0_knL.root",
  sampleBaseDir+"/pat/PATtuple_258_0_2Jb.root",
  sampleBaseDir+"/pat/PATtuple_259_0_6cX.root",
  sampleBaseDir+"/pat/PATtuple_260_0_U5I.root",
  sampleBaseDir+"/pat/PATtuple_261_0_4Pl.root",
  sampleBaseDir+"/pat/PATtuple_262_1_FRz.root",
  sampleBaseDir+"/pat/PATtuple_263_1_bQT.root",
  sampleBaseDir+"/pat/PATtuple_264_1_gFi.root",
  sampleBaseDir+"/pat/PATtuple_265_1_2aV.root",
  sampleBaseDir+"/pat/PATtuple_266_1_TQl.root",
  sampleBaseDir+"/pat/PATtuple_267_1_itH.root",
  sampleBaseDir+"/pat/PATtuple_268_0_2HR.root",
  sampleBaseDir+"/pat/PATtuple_269_0_F4G.root",
  sampleBaseDir+"/pat/PATtuple_270_0_bE1.root",
  sampleBaseDir+"/pat/PATtuple_271_0_k82.root",
  sampleBaseDir+"/pat/PATtuple_272_0_ajT.root",
  sampleBaseDir+"/pat/PATtuple_273_0_G72.root",
  sampleBaseDir+"/pat/PATtuple_274_0_e9R.root",
  sampleBaseDir+"/pat/PATtuple_275_0_njp.root",
  sampleBaseDir+"/pat/PATtuple_276_0_hTB.root",
  sampleBaseDir+"/pat/PATtuple_277_0_I3l.root",
  sampleBaseDir+"/pat/PATtuple_278_0_Hd0.root",
  sampleBaseDir+"/pat/PATtuple_279_0_vkc.root",
  sampleBaseDir+"/pat/PATtuple_280_0_RgZ.root",
  sampleBaseDir+"/pat/PATtuple_281_0_NEh.root",
  sampleBaseDir+"/pat/PATtuple_282_0_HY0.root",
  sampleBaseDir+"/pat/PATtuple_283_0_f04.root",
  sampleBaseDir+"/pat/PATtuple_284_0_eU5.root",
  sampleBaseDir+"/pat/PATtuple_285_0_7Ae.root",
  sampleBaseDir+"/pat/PATtuple_286_0_HX4.root",
  sampleBaseDir+"/pat/PATtuple_287_0_FbU.root",
  sampleBaseDir+"/pat/PATtuple_288_0_yDn.root",
  sampleBaseDir+"/pat/PATtuple_289_1_JMS.root",
  sampleBaseDir+"/pat/PATtuple_290_1_kyN.root",
  sampleBaseDir+"/pat/PATtuple_291_1_3T1.root",
  sampleBaseDir+"/pat/PATtuple_292_1_hoA.root",
  sampleBaseDir+"/pat/PATtuple_293_1_35p.root",
  sampleBaseDir+"/pat/PATtuple_294_1_vO8.root",
  sampleBaseDir+"/pat/PATtuple_295_1_Aac.root",
  sampleBaseDir+"/pat/PATtuple_296_1_mMO.root",
  sampleBaseDir+"/pat/PATtuple_297_1_81D.root",
  sampleBaseDir+"/pat/PATtuple_298_1_x3z.root",
  sampleBaseDir+"/pat/PATtuple_299_1_ySH.root",
  sampleBaseDir+"/pat/PATtuple_300_1_65l.root",
  sampleBaseDir+"/pat/PATtuple_301_1_ok5.root",
  sampleBaseDir+"/pat/PATtuple_302_1_Kz2.root",
  sampleBaseDir+"/pat/PATtuple_303_1_xc3.root",
  sampleBaseDir+"/pat/PATtuple_304_1_rrZ.root",
  sampleBaseDir+"/pat/PATtuple_305_1_R3o.root",
  sampleBaseDir+"/pat/PATtuple_306_1_t28.root",
  sampleBaseDir+"/pat/PATtuple_307_1_vh9.root",
  sampleBaseDir+"/pat/PATtuple_308_1_6wS.root",
  sampleBaseDir+"/pat/PATtuple_309_1_C0t.root",
  sampleBaseDir+"/pat/PATtuple_310_1_9cj.root",
  sampleBaseDir+"/pat/PATtuple_311_1_yJJ.root",
  sampleBaseDir+"/pat/PATtuple_312_1_KJw.root",
  sampleBaseDir+"/pat/PATtuple_313_1_DVc.root",
  sampleBaseDir+"/pat/PATtuple_314_1_4la.root",
  sampleBaseDir+"/pat/PATtuple_315_1_6Ze.root",
  sampleBaseDir+"/pat/PATtuple_316_1_gYL.root",
  sampleBaseDir+"/pat/PATtuple_317_1_ldv.root",
  sampleBaseDir+"/pat/PATtuple_318_0_pdV.root",
  sampleBaseDir+"/pat/PATtuple_319_0_seV.root",
  sampleBaseDir+"/pat/PATtuple_320_0_nou.root",
  sampleBaseDir+"/pat/PATtuple_321_0_lbr.root",
  sampleBaseDir+"/pat/PATtuple_322_1_cbo.root",
  sampleBaseDir+"/pat/PATtuple_323_1_9km.root",
  sampleBaseDir+"/pat/PATtuple_324_1_l9Y.root",
  sampleBaseDir+"/pat/PATtuple_325_1_lLG.root",
  sampleBaseDir+"/pat/PATtuple_326_0_zIj.root",
  sampleBaseDir+"/pat/PATtuple_327_0_6SV.root",
  sampleBaseDir+"/pat/PATtuple_328_0_6Fy.root",
  sampleBaseDir+"/pat/PATtuple_329_0_WW1.root",
  sampleBaseDir+"/pat/PATtuple_330_1_AlY.root",
  sampleBaseDir+"/pat/PATtuple_331_1_AN4.root",
  sampleBaseDir+"/pat/PATtuple_332_1_vwR.root",
  sampleBaseDir+"/pat/PATtuple_333_1_dlr.root",
  sampleBaseDir+"/pat/PATtuple_334_1_sEp.root",
  sampleBaseDir+"/pat/PATtuple_335_1_XxQ.root",
  sampleBaseDir+"/pat/PATtuple_336_1_cdO.root",
  sampleBaseDir+"/pat/PATtuple_337_1_yZS.root",
  sampleBaseDir+"/pat/PATtuple_338_1_Lzm.root",
  sampleBaseDir+"/pat/PATtuple_339_1_u0w.root",
  sampleBaseDir+"/pat/PATtuple_340_1_b9o.root",
  sampleBaseDir+"/pat/PATtuple_341_1_YKY.root",
  sampleBaseDir+"/pat/PATtuple_342_0_DxM.root",
  sampleBaseDir+"/pat/PATtuple_343_1_sDS.root",
  sampleBaseDir+"/pat/PATtuple_344_1_G70.root",
  sampleBaseDir+"/pat/PATtuple_345_1_n7Q.root",
  sampleBaseDir+"/pat/PATtuple_346_1_7r5.root",
  sampleBaseDir+"/pat/PATtuple_347_0_3UZ.root",
  sampleBaseDir+"/pat/PATtuple_348_1_zS0.root",
  sampleBaseDir+"/pat/PATtuple_349_1_fhS.root",
  sampleBaseDir+"/pat/PATtuple_350_1_lNC.root",
  sampleBaseDir+"/pat/PATtuple_351_1_CyE.root",
  sampleBaseDir+"/pat/PATtuple_352_1_E5Z.root",
  sampleBaseDir+"/pat/PATtuple_353_1_IH3.root",
  sampleBaseDir+"/pat/PATtuple_354_1_Atq.root",
  sampleBaseDir+"/pat/PATtuple_355_1_4zF.root",
  sampleBaseDir+"/pat/PATtuple_356_1_Bi2.root",
  sampleBaseDir+"/pat/PATtuple_357_1_zdY.root",
  sampleBaseDir+"/pat/PATtuple_358_1_1g3.root",
  sampleBaseDir+"/pat/PATtuple_359_1_6yW.root",
  sampleBaseDir+"/pat/PATtuple_360_1_452.root",
  sampleBaseDir+"/pat/PATtuple_361_1_kra.root",
  sampleBaseDir+"/pat/PATtuple_362_1_cmS.root",
  sampleBaseDir+"/pat/PATtuple_363_1_sWG.root",
  sampleBaseDir+"/pat/PATtuple_364_1_LDZ.root",
  sampleBaseDir+"/pat/PATtuple_365_1_qec.root",
  sampleBaseDir+"/pat/PATtuple_366_1_sqW.root",
  sampleBaseDir+"/pat/PATtuple_367_1_o4K.root",
  sampleBaseDir+"/pat/PATtuple_368_1_xOC.root",
  sampleBaseDir+"/pat/PATtuple_369_1_dc0.root",
  sampleBaseDir+"/pat/PATtuple_370_1_Rjd.root",
  sampleBaseDir+"/pat/PATtuple_371_1_oql.root",
  sampleBaseDir+"/pat/PATtuple_372_1_ndi.root",
  sampleBaseDir+"/pat/PATtuple_374_1_miy.root",
  sampleBaseDir+"/pat/PATtuple_375_1_bAY.root",
  sampleBaseDir+"/pat/PATtuple_376_1_Frm.root",
  sampleBaseDir+"/pat/PATtuple_377_0_tFF.root",
  sampleBaseDir+"/pat/PATtuple_378_0_csQ.root",
  sampleBaseDir+"/pat/PATtuple_379_0_Y7v.root",
  sampleBaseDir+"/pat/PATtuple_380_0_Ubg.root",
  sampleBaseDir+"/pat/PATtuple_381_0_Bui.root",
  sampleBaseDir+"/pat/PATtuple_382_0_RrV.root",
  sampleBaseDir+"/pat/PATtuple_383_0_TQy.root",
  sampleBaseDir+"/pat/PATtuple_384_0_MKT.root",
  sampleBaseDir+"/pat/PATtuple_385_0_RNO.root",
  sampleBaseDir+"/pat/PATtuple_386_0_n5T.root",
  sampleBaseDir+"/pat/PATtuple_387_1_9Oz.root",
  sampleBaseDir+"/pat/PATtuple_388_1_sjy.root",
  sampleBaseDir+"/pat/PATtuple_389_1_hZz.root",
  sampleBaseDir+"/pat/PATtuple_390_1_jF3.root",
  sampleBaseDir+"/pat/PATtuple_391_1_vZX.root",
  sampleBaseDir+"/pat/PATtuple_392_1_0VY.root",
  sampleBaseDir+"/pat/PATtuple_393_1_TPl.root",
  sampleBaseDir+"/pat/PATtuple_394_1_ACq.root",
  sampleBaseDir+"/pat/PATtuple_395_0_xKG.root",
  sampleBaseDir+"/pat/PATtuple_396_0_5Yl.root",
  sampleBaseDir+"/pat/PATtuple_397_0_zQZ.root",
  sampleBaseDir+"/pat/PATtuple_398_0_Dil.root",
  sampleBaseDir+"/pat/PATtuple_399_0_3gO.root",
  sampleBaseDir+"/pat/PATtuple_400_0_XSu.root",
  sampleBaseDir+"/pat/PATtuple_401_0_qIF.root",
  sampleBaseDir+"/pat/PATtuple_402_0_Gru.root",
  sampleBaseDir+"/pat/PATtuple_403_0_ejS.root",
  sampleBaseDir+"/pat/PATtuple_404_0_X20.root",
  sampleBaseDir+"/pat/PATtuple_405_0_rgq.root",
  sampleBaseDir+"/pat/PATtuple_406_0_Rtc.root",
  sampleBaseDir+"/pat/PATtuple_407_0_ju8.root",
  sampleBaseDir+"/pat/PATtuple_408_0_IMy.root",
  sampleBaseDir+"/pat/PATtuple_409_0_c7Z.root",
  sampleBaseDir+"/pat/PATtuple_410_0_aqN.root",
  sampleBaseDir+"/pat/PATtuple_411_0_PB8.root",
  sampleBaseDir+"/pat/PATtuple_412_0_DdO.root",
  sampleBaseDir+"/pat/PATtuple_413_0_atK.root",
  sampleBaseDir+"/pat/PATtuple_414_1_meo.root",
  sampleBaseDir+"/pat/PATtuple_415_1_joP.root",
  sampleBaseDir+"/pat/PATtuple_416_1_6jo.root",
  sampleBaseDir+"/pat/PATtuple_417_0_ziy.root",
  sampleBaseDir+"/pat/PATtuple_418_0_k55.root",
  sampleBaseDir+"/pat/PATtuple_419_1_M2W.root",
  sampleBaseDir+"/pat/PATtuple_420_1_0ZU.root",
  sampleBaseDir+"/pat/PATtuple_421_1_nO2.root",
  sampleBaseDir+"/pat/PATtuple_422_1_gVC.root",
  sampleBaseDir+"/pat/PATtuple_423_1_fTk.root",
  sampleBaseDir+"/pat/PATtuple_424_1_cTc.root",
  sampleBaseDir+"/pat/PATtuple_425_1_C0v.root",
  sampleBaseDir+"/pat/PATtuple_426_1_cHC.root",
  sampleBaseDir+"/pat/PATtuple_427_1_OyI.root",
  sampleBaseDir+"/pat/PATtuple_428_1_pxq.root",
  sampleBaseDir+"/pat/PATtuple_429_0_0dg.root",
  sampleBaseDir+"/pat/PATtuple_430_0_awz.root",
  sampleBaseDir+"/pat/PATtuple_431_0_d7h.root",
  sampleBaseDir+"/pat/PATtuple_432_0_kbo.root",
  sampleBaseDir+"/pat/PATtuple_433_0_1Yi.root",
  sampleBaseDir+"/pat/PATtuple_434_0_5kB.root",
  sampleBaseDir+"/pat/PATtuple_435_0_CW9.root",
  sampleBaseDir+"/pat/PATtuple_436_0_Usi.root",
  sampleBaseDir+"/pat/PATtuple_437_1_rpu.root",
  sampleBaseDir+"/pat/PATtuple_438_1_RFG.root",
  sampleBaseDir+"/pat/PATtuple_439_1_tps.root",
  sampleBaseDir+"/pat/PATtuple_440_1_GMB.root",
  sampleBaseDir+"/pat/PATtuple_441_1_jRK.root",
  sampleBaseDir+"/pat/PATtuple_442_1_FGj.root",
  sampleBaseDir+"/pat/PATtuple_443_0_Ewo.root",
  sampleBaseDir+"/pat/PATtuple_444_1_y2b.root",
  sampleBaseDir+"/pat/PATtuple_445_1_iKS.root",
  sampleBaseDir+"/pat/PATtuple_446_1_kpj.root",
  sampleBaseDir+"/pat/PATtuple_447_1_d5Q.root",
  sampleBaseDir+"/pat/PATtuple_448_1_L4A.root",
  sampleBaseDir+"/pat/PATtuple_449_1_8IR.root",
  sampleBaseDir+"/pat/PATtuple_450_1_UI1.root",
  sampleBaseDir+"/pat/PATtuple_451_1_nwN.root",
  sampleBaseDir+"/pat/PATtuple_452_1_OT2.root",
  sampleBaseDir+"/pat/PATtuple_453_1_nPG.root",
  sampleBaseDir+"/pat/PATtuple_454_1_Oab.root",
  sampleBaseDir+"/pat/PATtuple_455_1_pXG.root",
  sampleBaseDir+"/pat/PATtuple_456_1_WTy.root",
  sampleBaseDir+"/pat/PATtuple_457_1_bCI.root",
  sampleBaseDir+"/pat/PATtuple_458_1_DWh.root",
  sampleBaseDir+"/pat/PATtuple_459_1_7JB.root",
  sampleBaseDir+"/pat/PATtuple_460_1_VbE.root",
  sampleBaseDir+"/pat/PATtuple_461_1_JTh.root",
  sampleBaseDir+"/pat/PATtuple_462_1_4fb.root",
  sampleBaseDir+"/pat/PATtuple_463_1_SXN.root",
  sampleBaseDir+"/pat/PATtuple_464_1_FDP.root",
  sampleBaseDir+"/pat/PATtuple_465_1_SVS.root",
  sampleBaseDir+"/pat/PATtuple_466_1_FDx.root",
  sampleBaseDir+"/pat/PATtuple_467_1_DhI.root",
  sampleBaseDir+"/pat/PATtuple_468_1_kJQ.root",
  sampleBaseDir+"/pat/PATtuple_469_1_woc.root",
  sampleBaseDir+"/pat/PATtuple_470_1_Ld3.root",
  sampleBaseDir+"/pat/PATtuple_471_1_ZjV.root",
  sampleBaseDir+"/pat/PATtuple_472_1_g5m.root",
  sampleBaseDir+"/pat/PATtuple_473_0_U8J.root",
  sampleBaseDir+"/pat/PATtuple_474_0_PNT.root",
  sampleBaseDir+"/pat/PATtuple_475_0_NVi.root",
  sampleBaseDir+"/pat/PATtuple_476_0_aks.root",
  sampleBaseDir+"/pat/PATtuple_477_0_pQa.root",
  sampleBaseDir+"/pat/PATtuple_478_0_JPx.root",
  sampleBaseDir+"/pat/PATtuple_479_0_U6h.root",
  sampleBaseDir+"/pat/PATtuple_480_0_pqd.root",
  sampleBaseDir+"/pat/PATtuple_481_0_ZI2.root",
  sampleBaseDir+"/pat/PATtuple_482_0_vbe.root",
  sampleBaseDir+"/pat/PATtuple_483_0_iXP.root",
  sampleBaseDir+"/pat/PATtuple_484_0_9OY.root",
  sampleBaseDir+"/pat/PATtuple_485_1_Gsz.root",
  sampleBaseDir+"/pat/PATtuple_486_1_Lh0.root",
  sampleBaseDir+"/pat/PATtuple_487_1_O1D.root",
  sampleBaseDir+"/pat/PATtuple_488_1_usN.root",
  sampleBaseDir+"/pat/PATtuple_489_1_0mq.root",
  sampleBaseDir+"/pat/PATtuple_490_1_Yr4.root",
  sampleBaseDir+"/pat/PATtuple_491_1_zvg.root",
  sampleBaseDir+"/pat/PATtuple_492_1_Vn0.root",
  sampleBaseDir+"/pat/PATtuple_493_1_54r.root",
  sampleBaseDir+"/pat/PATtuple_494_1_9ad.root",
  sampleBaseDir+"/pat/PATtuple_495_1_gfg.root",
  sampleBaseDir+"/pat/PATtuple_496_1_ipK.root",
  sampleBaseDir+"/pat/PATtuple_497_1_F8F.root",
  sampleBaseDir+"/pat/PATtuple_498_1_FtZ.root",
  sampleBaseDir+"/pat/PATtuple_499_1_J79.root",
  sampleBaseDir+"/pat/PATtuple_500_1_Wuz.root",
  sampleBaseDir+"/pat/PATtuple_501_1_sfi.root",
  sampleBaseDir+"/pat/PATtuple_502_1_In7.root",
  sampleBaseDir+"/pat/PATtuple_503_1_mrd.root",
  sampleBaseDir+"/pat/PATtuple_504_1_Hfn.root",
  sampleBaseDir+"/pat/PATtuple_505_1_Dnl.root",
  sampleBaseDir+"/pat/PATtuple_506_1_9Im.root",
  sampleBaseDir+"/pat/PATtuple_507_1_2Q7.root",
  sampleBaseDir+"/pat/PATtuple_508_0_UwM.root",
  sampleBaseDir+"/pat/PATtuple_509_0_2Jv.root",
  sampleBaseDir+"/pat/PATtuple_510_1_CEd.root",
  sampleBaseDir+"/pat/PATtuple_511_1_mv5.root",
  sampleBaseDir+"/pat/PATtuple_512_1_xiB.root",
  sampleBaseDir+"/pat/PATtuple_513_1_XtC.root",
  sampleBaseDir+"/pat/PATtuple_514_1_nxl.root",
  sampleBaseDir+"/pat/PATtuple_515_1_Olc.root",
  sampleBaseDir+"/pat/PATtuple_516_1_x98.root",
  sampleBaseDir+"/pat/PATtuple_517_1_7wI.root",
  sampleBaseDir+"/pat/PATtuple_518_1_GaC.root",
  sampleBaseDir+"/pat/PATtuple_519_1_6h2.root",
  sampleBaseDir+"/pat/PATtuple_520_1_s6f.root",
  sampleBaseDir+"/pat/PATtuple_521_1_jlQ.root",
  sampleBaseDir+"/pat/PATtuple_522_1_aBz.root",
  sampleBaseDir+"/pat/PATtuple_523_1_f37.root",
  sampleBaseDir+"/pat/PATtuple_524_1_ZAo.root",
  sampleBaseDir+"/pat/PATtuple_525_1_mxA.root",
  sampleBaseDir+"/pat/PATtuple_526_1_Dos.root",
  sampleBaseDir+"/pat/PATtuple_527_1_Gut.root",
  sampleBaseDir+"/pat/PATtuple_528_1_F9V.root",
  sampleBaseDir+"/pat/PATtuple_529_1_lGV.root",
  sampleBaseDir+"/pat/PATtuple_530_1_HeL.root",
  sampleBaseDir+"/pat/PATtuple_531_0_lhp.root",
  sampleBaseDir+"/pat/PATtuple_532_0_kzT.root",
  sampleBaseDir+"/pat/PATtuple_533_0_iNh.root",
  sampleBaseDir+"/pat/PATtuple_534_0_SYC.root",
  sampleBaseDir+"/pat/PATtuple_535_0_xGH.root",
  sampleBaseDir+"/pat/PATtuple_536_0_sZW.root",
  sampleBaseDir+"/pat/PATtuple_537_0_1X7.root",
  sampleBaseDir+"/pat/PATtuple_538_0_Ae0.root",
  sampleBaseDir+"/pat/PATtuple_539_0_zFO.root",
  sampleBaseDir+"/pat/PATtuple_540_0_gIc.root",
  sampleBaseDir+"/pat/PATtuple_541_0_8Bb.root",
  sampleBaseDir+"/pat/PATtuple_542_0_5XE.root",
  sampleBaseDir+"/pat/PATtuple_543_0_nUH.root",
  sampleBaseDir+"/pat/PATtuple_544_1_gVt.root",
  sampleBaseDir+"/pat/PATtuple_545_1_a3O.root",
  sampleBaseDir+"/pat/PATtuple_546_1_UT1.root",
  sampleBaseDir+"/pat/PATtuple_547_1_9KO.root",
  sampleBaseDir+"/pat/PATtuple_548_1_tV6.root",
  sampleBaseDir+"/pat/PATtuple_549_1_7Hv.root",
  sampleBaseDir+"/pat/PATtuple_550_1_wYP.root",
  sampleBaseDir+"/pat/PATtuple_551_1_02v.root",
  sampleBaseDir+"/pat/PATtuple_552_1_0Ry.root",
  sampleBaseDir+"/pat/PATtuple_553_1_Jbg.root",
  sampleBaseDir+"/pat/PATtuple_554_1_qMf.root",
  sampleBaseDir+"/pat/PATtuple_555_1_N3x.root",
  sampleBaseDir+"/pat/PATtuple_556_1_oNx.root",
  sampleBaseDir+"/pat/PATtuple_557_1_aR8.root",
  sampleBaseDir+"/pat/PATtuple_558_1_ziv.root",
  sampleBaseDir+"/pat/PATtuple_559_1_euz.root",
  sampleBaseDir+"/pat/PATtuple_560_1_4Bl.root",
  sampleBaseDir+"/pat/PATtuple_561_1_cyO.root",
  sampleBaseDir+"/pat/PATtuple_562_1_jTg.root",
  sampleBaseDir+"/pat/PATtuple_563_1_AMS.root",
  sampleBaseDir+"/pat/PATtuple_564_1_fhS.root",
  sampleBaseDir+"/pat/PATtuple_565_1_DlN.root",
  sampleBaseDir+"/pat/PATtuple_566_1_2Hv.root",
  sampleBaseDir+"/pat/PATtuple_567_1_QX4.root",
  sampleBaseDir+"/pat/PATtuple_568_1_RZI.root",
  sampleBaseDir+"/pat/PATtuple_569_1_lMM.root",
  sampleBaseDir+"/pat/PATtuple_570_1_x37.root",
  sampleBaseDir+"/pat/PATtuple_571_0_gDk.root",
  sampleBaseDir+"/pat/PATtuple_572_0_mFF.root"
]