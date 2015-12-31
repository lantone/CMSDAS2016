import FWCore.ParameterSet.Config as cms
process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

from MuonAnalysis.TagAndProbe.tagAndProbe import *

#ptBins = cms.vdouble(33,100)
#absetaBins = cms.vdouble(0.0,2.0)
ptBins = cms.vdouble(15, 25, 33,40,50,70)
absetaBins = cms.vdouble(0.0,0.4,0.8,1.2,1.6,2.0)

process.TnP = Template.clone(
    InputFileNames = cms.vstring("/tmp/zheng13/tnpZ_Data_Run2011A-PromptReco-v5v6.root"),
    OutputFileName = cms.string("eff0424_L2DiMu30_v5v6_2d.root"),
    Efficiencies = cms.PSet(
#        DiMu7fromTk_Tag30 = cms.PSet(
#            EfficiencyCategoryAndState = cms.vstring("DoubleMu7","pass"),
#            UnbinnedVariables = cms.vstring("mass"),
#            BinnedVariables = cms.PSet(
#                pt = ptBins,
#                abseta = absetaBins,
#                tag_Mu30 = cms.vstring("pass"),
#		Track_HP= cms.vstring("pass"),
##		Track_Qual = cms.vstring("pass"),
#                IsolTk4 = cms.vstring("pass"),
#                pair_drM2 = cms.vdouble(0.3, 5),
#            ),
#            BinToPDFmap = cms.vstring("gaussPlusExpo")
#        ),
        L2DiMu30fromTk_TagAny1M = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring("L2DoubleMu30_Novtx","pass"),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = cms.PSet(
                pt = ptBins,
                abseta = absetaBins,
                tag_HLT_Any1M = cms.vstring("pass"),
                tag_IsolTk4 = cms.vstring("pass"),
                Track_HP= cms.vstring("pass"),
                Track_Qual= cms.vstring("pass"),
                Track_IP = cms.vstring("pass"),
#               IP_Significance = cms.vstring("pass"),
                IsolTk4 = cms.vstring("pass"),
                pair_drM2 = cms.vdouble(0.2, 5),
            ),
            BinToPDFmap = cms.vstring("gaussPlusExpo")
        ),
        L2DiMu23fromTk_TagAny1M = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring("L2DoubleMu23_Novtx","pass"),
            UnbinnedVariables = cms.vstring("mass"),#
            BinnedVariables = cms.PSet(
                pt = ptBins,
                abseta = absetaBins,
                tag_HLT_Any1M = cms.vstring("pass"),
		tag_IsolTk4 = cms.vstring("pass"),
                Track_HP= cms.vstring("pass"),
                Track_Qual= cms.vstring("pass"),
		Track_IP = cms.vstring("pass"),
#		IP_Significance = cms.vstring("pass"),
                IsolTk4 = cms.vstring("pass"),
                pair_drM2 = cms.vdouble(0.2, 5),
            ),
            BinToPDFmap = cms.vstring("gaussPlusExpo")
        ),
#
	L2DiMu23fromTk_TagL2NoVtx = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring("L2DoubleMu23_Novtx","pass"),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = cms.PSet(
                pt = ptBins,
                abseta = absetaBins,
                tag_L2DoubleMu23_Novtx = cms.vstring("pass"),
                Track_HP= cms.vstring("pass"),
		Track_Qual= cms.vstring("pass"),
#		IP_Significance = cms.vstring("pass"),
                Track_IP = cms.vstring("pass"),
                tag_IsolTk4 = cms.vstring("pass"),
                IsolTk4 = cms.vstring("pass"),
                pair_drM2 = cms.vdouble(0.2, 5),
            ),
            BinToPDFmap = cms.vstring("gaussPlusExpo")
        ),
#
    ),
)

process.fit = cms.Path(
    process.TnP
)
