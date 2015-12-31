import FWCore.ParameterSet.Config as cms

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),
    NumCPU = cms.uint32(8),
    SaveWorkspace = cms.bool(False),
    Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "50", "130", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("Probe |#eta|", "-2.5", "2.5", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
        tag_pt = cms.vstring("Tag p_{T}", "2.6", "1000", "GeV/c"),
        pair_drM2 = cms.vstring("dR in 2nd MS", "-1e6", "1e6", ""),#deltaR between tag and probe
        # Isolation Variables
#        tkIso = cms.vstring("tkIso SumPt","0.0","4.0","GeV/c"),
    ),
    Categories = cms.PSet(
        # Muon selectors
        TM     = cms.vstring("TM", "dummy[pass=1,fail=0]"),
        Glb    = cms.vstring("Glb", "dummy[pass=1,fail=0]"),
        GlbPT  = cms.vstring("GlbPT", "dummy[pass=1,fail=0]"),
        Calo   = cms.vstring("Calo", "dummy[pass=1,fail=0]"),
       
        # Track Quality Cuts
	Track_HP = cms.vstring("Track_HP", "dummy[pass=1,fail=0]"),#high purity	
	Track_IP = cms.vstring("Track_HP", "dummy[pass=1,fail=0]"),#abs(dxy)
        Track_Qual = cms.vstring("Track_Qual", "dummy[pass=1,fail=0]"),
        VBTF = cms.vstring("VBTF", "dummy[pass=1,fail=0]"),
        TQ = cms.vstring("TQ", "dummy[pass=1,fail=0]"),
        IsolTk4 = cms.vstring("IsolTk4", "dummy[pass=1,fail=0]"),#isolation
	tag_IsolTk4 = cms.vstring("tag_IsolTk4", "dummy[pass=1,fail=0]"),#tag isolation
        # Trigger for the tag muon
        tag_Mu30                   = cms.vstring("tag_Mu30", "dummy[pass=1,fail=0]"),                
        tag_Mu40		   = cms.vstring("tag_Mu40", "dummy[pass=1,fail=0]"),
        tag_Mu15		   = cms.vstring("tag_Mu15", "dummy[pass=1,fail=0]"),
	tag_Mu20                   = cms.vstring("tag_Mu15", "dummy[pass=1,fail=0]"),
        tag_IsoMu15   		   = cms.vstring("tag_IsoMu15", "dummy[pass=1,fail=0]"),
        tag_IsoMu17 		   = cms.vstring("tag_IsoMu17","dummy[pass=1,fail=0]"),
        tag_IsoMu24		   = cms.vstring("tag_IsoMu24","dummy[pass=1,fail=0]"),
        tag_IsoMu30		   = cms.vstring("tag_IsoMu30","dummy[pass=1,fail=0]"),
        tag_IsoMu20_eta2p1 	   = cms.vstring("tag_IsoMu20_eta2p1","dummy[pass=1,fail=0]"),
        tag_HLT_Any1M		   = cms.vstring("tag_HLT_Any1M","dummy[pass=1,fail=0]"),
	tag_L2DoubleMu23_Novtx = cms.vstring("tag_L2DoubleMu23_Novtx","dummy[pass=1,fail=0]"),
        # Trigger for the probes
        DoubleMu7         = cms.vstring("DoubleMu7", "dummy[pass=1,fail=0]"),
        L2DoubleMu23_Novtx= cms.vstring("L2DoubleMu23_Novtx", "dummy[pass=1,fail=0]"),
        L2DoubleMu30_Novtx= cms.vstring("L2DoubleMu30_Novtx", "dummy[pass=1,fail=0]"), 
   ),
#    Cuts = cms.PSet(
#        matched = cms.vstring("Matched", "L1dR", "0.3"),
#    ),
    ## The PDF is a Gaussian  (peak) + Exponential (background) 
    PDFs = cms.PSet(
        gaussPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),
    Efficiencies = cms.PSet(),
    binsForMassPlots = cms.uint32(20),
#    binnedFit = cms.bool(True),
#    binsForFit = cms.uint32(20),
)

