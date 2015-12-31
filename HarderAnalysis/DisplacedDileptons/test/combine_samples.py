#!/bin/env python

# script to create final plots and numbers for the displaced dilepton analysis
# Kristian Harder, RAL
# with contributions from Mark Baber, RAL/U Bristol

do_all_plots=0
draw_overflow=1
log_plots=1

import os,sys,math
import ROOT
import time

test = False
if len(sys.argv) == 2 and sys.argv[1] == "test":
    test = True

from HarderAnalysis.DisplacedDileptons.mergeSamples import *
from HarderAnalysis.DisplacedDileptons.pileupReweighting import *
from DisplacedLeptons.Samples.sampletools import srm_path
from HarderAnalysis.DisplacedDileptons.common import *
#from common import CMSPlotDecoration,setAxisRange, setHistNBins, setHistXLegend, setHistTitle, setAxisTitle, setLegendEntry, setHistColour
#from common import replace_trig_name, set_ana_folder


#set desired plot format
fformat = ".gif"

#set folder structure
folder = set_ana_folder()
benchmarkfolder = folder[0]
plotfolder      = folder[1]

#get list of samples to use:

myDir = os.environ["LOCALRT"]+"/src/workdirs/"
get_samples(myDir)

wdir = getWorkdirs(myDir, test)
workdirs_data_mu       =  wdir.workdirs_data_mu
workdirs_data_e        =  wdir.workdirs_data_e
workdirs_background_mu =  wdir.workdirs_background_mu
workdirs_background_e  =  wdir.workdirs_background_e
workdirs_signal        =  wdir.workdirs_signal
workdirs_benchmark     =  wdir.workdirs_signal

workdirs_benchmark_mu  =  wdir.workdirs_benchmark_mu
workdirs_benchmark_e   =  wdir.workdirs_benchmark_e 

#print_s(workdirs_signal,"signal")

# define analysis channels

muAnalysis="muTrackAnalysis"
eAnalysis="eTrackAnalysis"

ePtCut33=38
ePtCut38=41
ePtCut43=46
muPtCut23=25 # <- note this was lower!
muPtCut30=33


#replace trigger names for mc
replacementTrigger=replace_trig_name()

#set up tools for plot decoration
axisRange=setAxisRange()
histNBins=setHistNBins()
histXLegend=setHistXLegend()
histTitle=setHistTitle()
axisTitle=setAxisTitle()
legendEntry=setLegendEntry()
histColour=setHistColour()



# draw data/mc overlay plot from histograms
def overlayPlot(SampleTriggerCombination,backgrounddirs,weights,\
                histname,filename,lumisum,use_color=1):
    if len(backgrounddirs)!=len(weights):
        print "overlayPlot: list of weights does not match list of workdirs"
        sys.exit(1)
        pass

    # find list of triggers for MC
    mctriggers=[]
    for [dataworkdir,trigger,lumi] in SampleTriggerCombination:
        mctrig=replacementTrigger[trigger]
        if not mctrig in mctriggers: mctriggers.append(mctrig)
    if len(mctriggers)==0:
        mctriggers.append("anyTrigger")
    if len(mctriggers)!=1:
        # need to trim list of MC triggers down to one.
        # pick the one with highest p_t threshold.
        # this threshold needs to be exceeded by an offline cut!
        highestpt=0
        highestpttrigger=""
        for trigger in mctriggers:
            if trigger_threshold(trigger)>highestpt:
                highestpt=trigger_threshold(trigger)
                highestpttrigger=trigger
                pass
            pass
        mctriggers=[highestpttrigger]
        pass
    # construct corresponding sample/trigger combinations for MC
    MCSampleTriggerCombination=[]
    for i in range(len(backgrounddirs)):
        for trigger in mctriggers:
            MCSampleTriggerCombination.append([backgrounddirs[i],trigger,weights[i]])
 
    # fill histogram for data samples
    datahisto=0
    for [workdir,trigger,lumi] in SampleTriggerCombination:
        if not datahisto:
            histfile=ROOT.TFile.Open(workdir+"/histograms.root","R")
            try:
                datahisto=histfile.Get(histname.replace("TRIGGER",trigger)).Clone()
            except:
                print "WARNING: histogram",histname,"not found in",workdir
                return
            datahisto.SetDirectory(0)
            histfile.Close()
        else:
            histfile=ROOT.TFile.Open(workdir+"/histograms.root","R")
            datahisto.Add(histfile.Get(histname.replace("TRIGGER",trigger)))
            histfile.Close()
            pass
        pass

    # background MC plots: certain samples are split in pthat bins.
    # these should show up only as a single contribution in the plots.
    # thus define groups of samples to be plotted as one:
    groupList = []
    
    # Initialise a dictionary of histograms for each group
    valHistList = {}

    # fill histogram for background samples
    for [workdir,trigger,weight] in MCSampleTriggerCombination:
        if weight<=0: continue
        histfile=ROOT.TFile.Open(workdir+"/histograms.root","R")
        try:
            valhist=histfile.Get(histname.replace("TRIGGER",trigger)).Clone()
        except:
            valhist=0
            pass
        if not valhist: continue
        valhist.SetDirectory(0)
        histfile.Close()
        # Extract the file name from the workdir name
        fileName = workdir.split("/")[-1].split("analysis")[0]
        # Sort the file into a group.
        # if group does not exist add its name as a new group and add a
        # histogram to the histogram lists
        groupName=""
        for group in groupList:
            if fileName.find(group)>=0:
                groupName = group
                pass
            pass
        if groupName=="":
            # File does not fit in any defined group

            # background MC plots: certain samples are split in pthat bins.
            # these should show up only as a single contribution in the plots.
            # thus define groups of samples to be plotted as one:
            if fileName.find("QCDem")>=0:
                groupName = "QCDem_"
            elif fileName.find("QCDmu")>=0:
                groupName = "QCDmu_"
            elif fileName.find("ZeeJets")>=0:
                groupName = "ZeeJets_"
            elif fileName.find("ZmumuJets")>=0:
                groupName = "ZmumuJets_"
            else:
                groupName = fileName
                pass

                
            groupList.append(groupName)

           
            # Add a histogram to each of the histogram lists
            valHistList[groupName]=ROOT.TH1F()
            pass
        
        # Add the values to the respective group histogram
        if valHistList[groupName].GetEntries()==0:
            valHistList[groupName]=valhist
            valHistList[groupName].Scale(weight)
        else:
            valHistList[groupName].Add(valhist,weight)
            pass
        pass


    #Move the signal MC to the back of list to ensure it is plotted on top of the other distributions
    for group in groupList:
        if group.find("Signal") >= 0:
            groupList.append(groupList.pop(groupList.index(group))) #Remove element and append to end of the list
            pass
        pass



    # Make the histograms cumulative, with the first histogram containing
    # just its own values and the last histogram containing total sum of
    # all the histograms
    for i in range(1,len(groupList)):

###########################################################
        valHistList[groupList[i]]+=valHistList[groupList[i-1]]
        
        if groupList[i].find("Signal") >= 0: 
             valHistList[groupList[i]].SetLineColor(2)  # Make the line colour unique
        else:
            valHistList[group].SetFillColor(histColour[group])
            pass
        pass
    # Reverse order of the list so that when plotted the first element is on top
    groupList.reverse()

    canv=ROOT.TCanvas("tmpcanv")

    # define legend
    if use_color:
        valLegend = ROOT.TLegend(histXLegend[histname.split("/")[-1]],0.4,histXLegend[histname.split("/")[-1]]+0.3,0.7)
    else:
        valLegend = ROOT.TLegend(histXLegend[histname.split("/")[-1]],0.55,histXLegend[histname.split("/")[-1]]+0.3,0.7)
        pass
    valLegend.SetFillColor(ROOT.kWhite)
    
    # draw background for each of the groups on the same histogram
    scalefactor=1.0
    if not use_color:
        valLegend.AddEntry(valHistList[groupList[0]],"MC","f")
    for group in groupList:
        if use_color:
            if group.find("Signal")>=0:
                valLegend.AddEntry(valHistList[group],legendEntry[group],"l")
                pass
            else:
                valLegend.AddEntry(valHistList[group],legendEntry[group],"f")
                pass
            pass
        valHistList[group].SetMarkerStyle(0)
        if (groupList.index(group) == 0):
            # first histogram to be drawn
            try:
                scalefactor=datahisto.Integral()/valHistList[group].Integral()
            except:
                pass
            print "WARNING: MC scale factor",scalefactor
            valHistList[group].Scale(scalefactor)
            xmin=valHistList[group].GetXaxis().GetXmin()
            xmax=valHistList[group].GetXaxis().GetXmax()
            try:
                ymax=max(datahisto.GetMaximum(),valHistList[group].GetMaximum())*1.3
            except:
                ymax=valHistList[group].GetMaximum()*1.3
                pass
            valHistList[group].SetMaximum(ymax)
            valHistList[group].GetXaxis().SetTitle(axisTitle[histname.split("/")[-1]])
            valHistList[group].GetYaxis().SetTitle("Entries")
            if ymax>1e5: valHistList[group].GetYaxis().SetTitleOffset(1.5)
            valHistList[group].SetTitle(histTitle[histname.split("/")[-1]])
            drawhist(valHistList[group],"h")
        elif use_color:
            # overlay
            valHistList[group].Scale(scalefactor)
            drawhist(valHistList[group],"hsame")
            pass
        pass

    if datahisto:
        datahisto.SetMarkerStyle(21)
        drawhist(datahisto,"esame")
        valLegend.AddEntry(datahisto,"data","p")
        pass
    valLegend.Draw()
    CMSPlotDecoration(histname.split("/")[0],lumisum)
    canv.Update()
    canv.Print(filename)

    valHistList.clear()
    if datahisto: datahisto.Delete()
    canv.Close()
    return


#############################################
### GET HISTOGRAM OF A TREE QUANTITY
#############################################

# note that this is a particularly complicated way of doing things.
# it would be a lot more elegant to read the tree in this python script
# and fill the histogram right here. however, reading the tree event by
# event in python is way too slow, and using functions like TTree::Project
# or TTree::Draw seems to be associated with massive memory leaks, leading
# to crashes of this script when running into the 4G memory limit per process...

def get_histogram(workdir,treedir,varname,nbins,minval,maxval,minmass,maxmass,ptCut):
    # get temporary root file name
    tempfilename="/tmp/temproot_"+os.getenv("USER","default")+".root"
    
    command="TFile* infile = new TFile(\""+workdir+"/histograms.root\");\n"\
             +"TTree* tree = infile->Get(\""+treedir+"/bigTree\");\n"\
             +"TFile* outfile = new TFile(\""+tempfilename+"\",\"RECREATE\");\n"\
             +"TH1F* valhist = new TH1F(\"valhist\",\"valhist\","\
             +str(nbins)+","+str(minval)+","+str(maxval)+");\n"\
             +"TH1F* vhloose = new TH1F(\"vhloose\",\"vhloose\","\
             +str(nbins)+","+str(minval)+","+str(maxval)+");\n"\
             +"TH1F* masspasshist = new TH1F(\"masspasshist\",\"masspasshist\","\
             +str(100)+","+str(minmass)+","+str(maxmass)+");\n"\
             +"TH1F* massfailhist = new TH1F(\"massfailhist\",\"massfailhist\","\
             +str(100)+","+str(minmass)+","+str(maxmass)+");\n"\
             +"vector<string> conditions;\n"\
             +"TObjArray* branches = tree->GetListOfBranches();\n"\
             +"for (int i=0; i<branches->GetEntries(); i++) {\n"\
             +" const char* branchName=branches->At(i)->GetName();\n"\
             +" if (strstr(branchName,\"_pass\")) conditions.push_back(branchName);\n"\
             +"}\n"\
             +"string passesAllOtherCuts=\"\";\n"\
             +"string passesAllOtherCutsIgnoreLifetime=\"\";\n"\
             +"for (int i=0; i<conditions.size(); i++) {\n"\
             +" if (!strstr(conditions[i].c_str(),\""+varname+"\")) passesAllOtherCuts+=conditions[i]+\" && \";\n"\
             +" bool lifetimecut=false;\n"\
             +" lifetimecut|=(strstr(conditions[i].c_str(),\"leptonT0\")!=0);\n"\
             +" lifetimecut|=(strstr(conditions[i].c_str(),\"leptonD0\")!=0);\n"\
             +" lifetimecut|=(strstr(conditions[i].c_str(),\"leptonAbsD0\")!=0);\n"\
             +" lifetimecut|=(strstr(conditions[i].c_str(),\"decayLength\")!=0);\n"\
             +" lifetimecut|=(strstr(conditions[i].c_str(),\"dPhi\")!=0);\n"\
             +" if (!lifetimecut) passesAllOtherCutsIgnoreLifetime+=conditions[i]+\" && \";\n"\
             +"}\n"\
             +"passesAllOtherCuts+=\"leptonPtL>"+str(ptCut)+"\";\n"\
             +"passesAllOtherCutsIgnoreLifetime+=\"leptonPtL>"+str(ptCut)+"\";\n"\
             +"tree->Project(\"valhist\",\""+varname+"\",(\"_weight*(\"+passesAllOtherCuts+\")\").c_str());\n"\
             +"tree->Project(\"vhloose\",\""+varname+"\",(\"_weight*(\"+passesAllOtherCutsIgnoreLifetime+\")\").c_str());\n"\
             +"tree->Project(\"masspasshist\",\"_mass\",\"_weight*(passesAllCuts)\");\n"
    if maxmass<10 or varname[0]=="_":
        command+="tree->Project(\"massfailhist\",\"_mass\",(\"_weight*(\"+passesAllOtherCuts+\")\").c_str());\n"
    else:
        command+="tree->Project(\"massfailhist\",\"_mass\",(\"_weight*(!"+varname+"_pass && \"+passesAllOtherCutsIgnoreLifetime+\")\").c_str());\n"
        pass
    command+="valhist->Write();\n"\
             +"vhloose->Write();\n"\
             +"masspasshist->Write();\n"\
             +"massfailhist->Write();\n"\
             +"outfile.Close();\n"\
             +"infile.Close();\n"\
             +"gApplication->Terminate();\n"
    result=os.popen("root -b -l << EOF\n"+command+"\nEOF\n").readlines()
    histfile=ROOT.TFile.Open(tempfilename)
    valhist=histfile.Get("valhist")
    clonedvalhist=valhist.Clone("tmpval")
    clonedvalhist.SetDirectory(0)
    vhloose=histfile.Get("vhloose")
    clonedvhloose=vhloose.Clone("tmpvalloose")
    clonedvhloose.SetDirectory(0)
    masspasshist=histfile.Get("masspasshist")
    clonedmasspasshist=masspasshist.Clone("tmpmasspass")
    clonedmasspasshist.SetDirectory(0)
    massfailhist=histfile.Get("massfailhist")
    clonedmassfailhist=massfailhist.Clone("tmpmassfail")
    clonedmassfailhist.SetDirectory(0)
    histfile.Close()
    os.system("rm "+tempfilename)
    return [clonedvalhist,clonedvhloose,clonedmasspasshist,clonedmassfailhist]


def get_masses(workdir,treedir,weight=1.0):
    command="TFile* infile = new TFile(\""+workdir+"/histograms.root\");\n"\
             +"TTree* tree = infile->Get(\""+treedir+"/bigTree\");\n"\
             +"tree->SetScanField(0);\n"\
             +"tree->Scan(\"_mass:_weight\","\
             +"\"passesAllCuts\"\n);"\
             +"infile.Close();\n"\
             +"gApplication->Terminate();\n"
    result=os.popen("root -b -l << EOF\n"+command+"\nEOF\n").readlines()
    masslist=[]
    for entry in result:
        fields=entry.replace("*","").strip().split()
        if len(fields)!=3: continue
        try:
            newmass=float(fields[1].strip())
            newweight=float(fields[2].strip())*weight
            masslist.append([newmass,newweight])
        except:
            pass
        pass
    return masslist


#############################################
### DRAW DATA/MC OVERLAY PLOT FROM ROOT TREE
#############################################



def treeOverlayPlot(SampleTriggerCombination,backgrounddirs,signaldirs,weights,\
                    signalWeights,lepton_name,treedir,varname,filename,ptCut,lumisum,
                    efficiencyListData=[],
                    efficiencyListMC=[],efficiencyListSignal=[]):
    if len(backgrounddirs)!=len(weights):
        print "treeOverlayPlot: list of weights does not match list of workdirs"
        sys.exit(1)
        pass
    if len(signaldirs)!=len(signalWeights):
        print "treeOverlayPlot: list of signal weights"+\
              "does not match list of signal workdirs"
        sys.exit(1)
        pass

    # Keep only the signal MC we are interested in
    for i in range(len(signaldirs)):
        if signaldirs[i].find("Signal_1000_350F") >= 0:

            tempDir = signaldirs[i]
            tempWeight = signalWeights[i]
            signaldirs = [tempDir]
            signalWeights =[tempWeight]
            break


    
    #####################################################################

    # find list of triggers for MC
    mctriggers=[]
    for [dataworkdir,trigger,lumi] in SampleTriggerCombination:
        mctrig=replacementTrigger[trigger]
        if not mctrig in mctriggers: mctriggers.append(mctrig)
    if len(mctriggers)!=1:
        # need to trim list of MC triggers down to one.
        # pick the one with highest p_t threshold.
        # this threshold needs to be exceeded by an offline cut!
        highestpt=0
        highestpttrigger=""
        for trigger in mctriggers:
            if trigger_threshold(trigger)>highestpt:
                highestpt=trigger_threshold(trigger)
                highestpttrigger=trigger
                pass
            pass
        mctriggers=[highestpttrigger]
        pass

    # construct corresponding sample/trigger combinations for MC
    MCSampleTriggerCombination=[]
    for i in range(len(backgrounddirs)):
        for trigger in mctriggers:
            MCSampleTriggerCombination.append([backgrounddirs[i],trigger,weights[i]])

    ########################################################################
    MCSignalSampleTriggerCombination=[]
    for i in range(len(signaldirs)):
        for trigger in mctriggers:
            MCSignalSampleTriggerCombination.append([signaldirs[i],trigger,signalWeights[i]])
            
        
    # now loop over all trees to get minimum and maximum values (for histogram boundaries)
    found_tree=0
    files_with_data_trigger=[]
    files_with_no_trigger_whatsoever=[]
    for [workdir,trigger,lumi] in SampleTriggerCombination+MCSampleTriggerCombination+MCSignalSampleTriggerCombination:
        histfile=ROOT.TFile.Open(workdir+"/histograms.root")
        try:
            roottree=histfile.Get(treedir.replace("TRIGGER",trigger)+"/bigTree")
            numentries=roottree.GetEntries()
            files_with_data_trigger.append(workdir)
        except:
            numentries=-1
            files_with_no_trigger_whatsoever.append(workdir)
            pass
        if numentries>=0:
            newMinValue=roottree.GetMinimum(varname)
            newMaxValue=roottree.GetMaximum(varname)
            try:
                if newMinValue<minValue: minValue=newMinValue
                if newMaxValue<maxValue: maxValue=newMaxValue
                pass
            except:
                minValue=newMinValue
                maxValue=newMaxValue
                pass
            newMinMass=roottree.GetMinimum("mass")
            newMaxMass=roottree.GetMaximum("mass")
            try:
                if newMinMass<minMass: minMass=newMinMass
                if newMaxMass<maxMass: maxMass=newMaxMass
                pass
            except:
                minMass=newMinMass
                maxMass=newMaxMass
                pass
            pass
        if histfile: histfile.Close()
        pass


    if len(files_with_data_trigger)==0:
        print "ERROR: variable",varname,"not found in data samples"
        return [[],[]]
    if len(files_with_no_trigger_whatsoever)>0:
        print "WARNING: the following samples have no suitable trigger information whatsoever:"
        for sample in files_with_no_trigger_whatsoever:
            print "        ",sample

    # create histogram
    histname=varname.split("/")[-1]
    nbins=histNBins[histname]
    histMinMass=axisRange["mass"][0]
    histMaxMass=axisRange["mass"][1]
    if (minMass>=0 and minMass<histMinMass) or maxMass>histMaxMass:
        print "WARNING: candidate masses outside of histogram boundaries:",histname,
        print "histo range",histMinMass,"-",histMaxMass,", actual range",minMass,"-",maxMass 
        pass
    if axisRange.has_key(histname):
        histMinValue=axisRange[histname][0]
        histMaxValue=axisRange[histname][1]
    else:
        # round extreme values to two significant digits
        histMinValue=float("%.2e"%minValue)
        histMaxValue=float("%.2e"%maxValue)
        print "WARNING: no user-defined histogram boundaries:",histname
        pass

    if varname=="deltaRBetweenLeptons": histMaxMass=5 # J/psi

    datahisto=ROOT.TH1F(histname,varname,nbins,histMinValue,histMaxValue)
    datahisto_loose=ROOT.TH1F(histname+"_loose",varname+" loose",nbins,histMinValue,histMaxValue)
    mchisto=ROOT.TH1F(histname+"_mc",varname,nbins,histMinValue,histMaxValue)
    mchisto_loose=ROOT.TH1F(histname+"_mcloose",varname+" loose",nbins,histMinValue,histMaxValue)
    nbins_mass=100
    datahistoMassPass=ROOT.TH1F(histname+"_MassPass",varname,nbins_mass,histMinMass,histMaxMass)
    mchistoMassPass=ROOT.TH1F(histname+"_MassPass_mc",varname,nbins_mass,histMinMass,histMaxMass)
    datahistoMassFail=ROOT.TH1F(histname+"_MassFail",varname,nbins_mass,histMinMass,histMaxMass)
    mchistoMassFail=ROOT.TH1F(histname+"_MassFail_mc",varname,nbins_mass,histMinMass,histMaxMass)

    # determine whether we want to fill mass plots as well
    massplots=0
    if varname=="decayLengthSignificance2D": massplots=1
    if varname=="deltaRBetweenLeptons": massplots=1
    datamasslist=[]
    bkgmasslist=[]

    # Initialise the efficiency variables
    passesThisAndAllOtherCuts_data = 0
    passesAllOtherCuts_data        = 0

    # fill histogram for data samples
    for [workdir,trigger,lumi] in SampleTriggerCombination:
            
        [valhist,valhist_loose,masspasshist,massfailhist]=get_histogram(workdir,treedir.replace("TRIGGER",trigger),varname,nbins,histMinValue,histMaxValue,histMinMass,histMaxMass,ptCut)
        datahisto.Add(valhist)
        datahisto_loose.Add(valhist_loose)
        datahistoMassPass.Add(masspasshist)
        datahistoMassFail.Add(massfailhist)

        # Store variables to calculate the cut efficiencies
        passesThisAndAllOtherCuts_data += valhist_loose.Integral()\
                                          -massfailhist.Integral()
        passesAllOtherCuts_data        += valhist_loose.Integral()

        valhist.Delete()
        valhist_loose.Delete()
        masspasshist.Delete()
        massfailhist.Delete()
        if massplots:
            datamasslist+=get_masses(workdir,treedir.replace("TRIGGER",trigger))
            pass
        pass


    groupList = []
    
    # Initialise the efficiency variables
    passesThisAndAllOtherCuts_bkg = 0
    passesAllOtherCuts_bkg        = 0
    passesThisAndAllOtherCuts_sig = 0
    passesAllOtherCuts_sig        = 0

    # Initialise a dictionary of histograms for each group
    valHistList = {}
    valHistList_loose = {}
    massPassHistList = {}
    massFailHistList = {}

    # fill histogram for background samples
    for [workdir,trigger,weight] in MCSampleTriggerCombination + MCSignalSampleTriggerCombination:
        if weight<=0: continue



        #Generate list of types to iterate through 
        if workdir.find("Signal") >= 0:
            #Sample is signal
            
            #Account for fact that 'leptons' does not contain a 'partial' tree
            if varname.find("dileptons") >= 0:
                #Tree is dileptons
                typeList = ["_background","_signal","_partial"]
            else:
                #Tree is leptons
                typeList = ["_background","_signal"]
                pass
            pass
           
        else:
            #Sample is background
            typeList = ["_background"]
            pass
        pass
    
    
        for type in typeList:
                  
             #print "\n", varname.replace("_background",type).replace("TRIGGER",trigger), "\n"

             [tempvalhist,tempvalhist_loose,tempmasspasshist,tempmassfailhist]=get_histogram(workdir,treedir.replace("_background",type).replace("TRIGGER",trigger),varname,nbins,histMinValue,histMaxValue,histMinMass,histMaxMass,ptCut)

             
             if type == "_background":
                 #Initialise histograms
                 valhist = tempvalhist.Clone()
                 valhist_loose = tempvalhist_loose.Clone()
                 masspasshist = tempmasspasshist.Clone()
                 massfailhist = tempmassfailhist.Clone()
             else:
                 valhist.Add(tempvalhist)
                 valhist_loose.Add(tempvalhist_loose)
                 masspasshist.Add(tempmasspasshist)
                 massfailhist.Add(tempmassfailhist)
                 pass
             if type=="_signal":
                 passesThisAndAllOtherCuts_sig += tempvalhist_loose.Integral()\
                                                  -tempmassfailhist.Integral()
                 passesAllOtherCuts_sig        += tempvalhist_loose.Integral()

             tempvalhist.Delete()
             tempvalhist_loose.Delete()
             tempmasspasshist.Delete()
             tempmassfailhist.Delete()


     
       
        # Extract the file name from the workdir name
        fileName = workdir.split("/")[-1].split("analysis")[0]
        # Sort the file into a group.
        # if group does not exist add its name as a new group and add a
        # histogram to the histogram lists
        for group in groupList:
            if fileName.find(group.strip("_"))>=0:
                groupName = group
                break
            pass
        else:
            # File does not fit in any defined group

            # background MC plots: certain samples are split in pthat bins.
            # these should show up only as a single contribution in the plots.
            # thus define groups of samples to be plotted as one:

            if fileName.find("QCDem")>=0:
                groupName = "QCDem_"
            elif fileName.find("QCDmu")>=0:
                groupName = "QCDmu_"
            elif fileName.find("ZeeJets")>=0:
                groupName = "ZeeJets_"
            elif fileName.find("ZmumuJets")>=0:
                groupName = "ZmumuJets_"
            else:
                groupName = fileName
                
            groupList.append(groupName)

           
            # Add a histogram to each of the histogram lists
            valHistList[groupName]= ROOT.TH1F(histname+"_mc_"+groupName,varname,
                                              nbins,histMinValue,histMaxValue)
            valHistList_loose[groupName]= ROOT.TH1F(histname+"_mcloose_"+groupName,
                                                    varname+" loose",
                                                    nbins,histMinValue,histMaxValue)
            massPassHistList[groupName]= ROOT.TH1F(histname+"_MassPass_mc_"+
                                                   groupName,varname,100,
                                                   histMinMass,histMaxMass)
            massFailHistList[groupName]= ROOT.TH1F(histname+"_MassFail_mc_"+
                                                   groupName,varname,100,
                                                   histMinMass,histMaxMass)
            pass
        
        # Add the values to the respective group histogram
        valHistList[groupName].Add(valhist,weight)
        valHistList_loose[groupName].Add(valhist_loose,weight)
        massPassHistList[groupName].Add(masspasshist,weight)
        massFailHistList[groupName].Add(massfailhist,weight)

        # Store variables to calculate the efficiency
        if workdir.find("Signal")<0:
            passesThisAndAllOtherCuts_bkg += valhist_loose.Integral()\
                                             -massfailhist.Integral()
            passesAllOtherCuts_bkg        += valhist_loose.Integral()
            pass
        
        valhist.Delete()
        valhist_loose.Delete()
        masspasshist.Delete()
        massfailhist.Delete()
        if massplots:
            if workdir.find("Signal")>=0:
                #The sample is signal do not add it to bkgmasslist
                pass
            else:
                bkgmasslist+=get_masses(workdir,treedir.replace("TRIGGER",trigger),weight)
                pass
            
            pass
        pass




    #---------------------
    # cut efficiencies
    #---------------------
   
    cutName = varname.split("/")[-1]
 
    #Calculate the cut efficiency for data
    if (passesAllOtherCuts_data > 0):
        efficiency_data = 100.*float(passesThisAndAllOtherCuts_data)/float(passesAllOtherCuts_data) 
    else:
        efficiency_data = 0
          
    #Store data in a dictionary for easy passing later 
    efficiencyData = {'cutName': cutName,'passesThisAndAllOtherCuts': passesThisAndAllOtherCuts_data,
                      'passesAllOtherCuts': passesAllOtherCuts_data,'efficiency': efficiency_data}

    efficiencyListData.append(efficiencyData)

    #Calculate the cut efficiency for background MC
    if (passesAllOtherCuts_bkg > 0):
        efficiency_bkg = 100.*float(passesThisAndAllOtherCuts_bkg)/float(passesAllOtherCuts_bkg) 
    else:
        efficiency_bkg = 0
          
    #Store data in a dictionary for easy passing later 
    efficiencyMC = {'cutName': cutName,'passesThisAndAllOtherCuts': passesThisAndAllOtherCuts_bkg,
                      'passesAllOtherCuts': passesAllOtherCuts_bkg,'efficiency': efficiency_bkg}

    efficiencyListMC.append(efficiencyMC)

    
    #Calculate the cut efficiency for signal MC
    if (passesAllOtherCuts_sig > 0):
        efficiency_sig = 100.*float(passesThisAndAllOtherCuts_sig)/float(passesAllOtherCuts_sig) 
    else:
        efficiency_sig = 0
          
    #Store data in a dictionary for easy passing later 
    efficiencySignal = {'cutName': cutName,'passesThisAndAllOtherCuts': passesThisAndAllOtherCuts_sig,
                      'passesAllOtherCuts': passesAllOtherCuts_sig,'efficiency': efficiency_sig}

    efficiencyListSignal.append(efficiencySignal)

    
    # Make the histograms cumulative, with the first histogram containing
    # just its own values and the last histogram containing total sum of
    # all the histograms





############################################################################################################
#
# ADDING SIGNAL MC CONTRIBUTION
#
# This requires that a Signal sample is added to SampleTriggerCombination, this can be achieved by
# either: adding Signal as another function argument or by adding a Signal workdir to the list of
# background workdirs. Would this lead to problems elsewhere where signal is not required?
############################################################################################################

    #Move the signal MC to the back of list to ensure it is plotted on top of the other distributions
    tempGroupList = []
    for group in groupList:
        if group.find("Signal") >= 0:
            tempGroupList.append(group)
        else:
            tempGroupList.insert(0,group)
            pass
        pass

    groupList = tempGroupList
   
    tempHist = {}
    for group in groupList:
        for histList in [valHistList,valHistList_loose,massPassHistList,massFailHistList]:

            histIndex = [valHistList,valHistList_loose,massPassHistList,massFailHistList].index(histList)
            groupIndex = groupList.index(group)
       
            if (groupList.index(group) == 0):
                # first histogram index
                tempHist[histIndex] = histList[group].Clone()
                histList[group].SetFillColor(histColour[group])
            else:    
                tempHist[histIndex].Add(histList[group])  
                histList[group]=tempHist[histIndex].Clone()

                if group.find("Signal") >= 0:        # Sample is signal MC
                    histList[group].SetLineColor(2)  # Make the line colour unique
                    #histList[group].SetFillColor(0)  # Make the fill white
                else:                    
                    # Pick a color relative to the position in the list
                    #histList[group].SetFillColor(groupIndex+2)


                    histList[group].SetFillColor(histColour[group])
                    pass
                pass
            pass
        pass
    tempHist.clear()
    # Reverse order of the list so that when plotted the first element is on top
    groupList.reverse()

    canv=ROOT.TCanvas("tmpcanv")
    if log_plots: canv.SetLogy()

    # determine histogram boundaries
    ymax=max(datahisto.GetMaximum(),valHistList[groupList[0]].GetMaximum())
    ymax_loose=max(datahisto_loose.GetMaximum(),valHistList_loose[groupList[0]].GetMaximum())
    if log_plots:
        ymax*=10
        ymax_loose*=10
    else:
        ymax*=1.2
        ymax_loose*=1.2
        pass

    # define legend
    valLegend = ROOT.TLegend(histXLegend[cutName],0.62,histXLegend[cutName]+0.3,0.92)
    valLegend.SetFillColor(ROOT.kWhite)

    # draw background for each of the groups on the same histogram
    for group in groupList:

        ############################################################
        
        if group.find("Signal")>=0:
            valLegend.AddEntry(valHistList[group],legendEntry[group],"l")
            pass
        else:
            valLegend.AddEntry(valHistList[group],legendEntry[group],"f")
            pass
        
        ############################################################

        
        valHistList[group].SetMaximum(ymax)
        valHistList[group].SetMarkerStyle(0)
        if (groupList.index(group) == 0):
            # first histogram to be drawn
            valHistList[group].GetXaxis().SetTitle(axisTitle[cutName])
            valHistList[group].GetYaxis().SetTitle("Entries")
            valHistList[group].SetTitle(histTitle[histname]+", "+lepton_name+" channel")
            drawhist(valHistList[group],"h")
        else:
            # overlay
            drawhist(valHistList[group],"hsame")
            pass
        pass
    
    datahisto.SetMarkerStyle(21)
    drawhist(datahisto,"esame")
    valLegend.AddEntry(datahisto,"data","p")
    valLegend.Draw()
    CMSPlotDecoration(lepton_name,lumisum)
    canv.Update()
    canv.Print(filename)

    # also dump these histograms into a root file
    plotfile=ROOT.TFile.Open(filename.replace(fformat,".root"),"RECREATE")
    datahisto.Write()
    for group in groupList:
        if group.find("Signal")>=0:
            signalHisto=valHistList[group].Clone(datahisto.GetName()+"_SignalMC")
            continue
        backgroundHisto=valHistList[group].Clone(datahisto.GetName()+"_BackgroundMC")
        break
    for i in range(signalHisto.GetNbinsX()):
        sumval=signalHisto.GetBinContent(i+1)
        sumerr=signalHisto.GetBinError(i+1)
        bkgval=backgroundHisto.GetBinContent(i+1)
        bkgerr=backgroundHisto.GetBinError(i+1)
        signalHisto.SetBinContent(i+1,sumval-bkgval)
        signalHisto.SetBinError(i+1,math.sqrt(sumerr*sumerr-bkgerr*bkgerr))
        pass
    signalHisto.Write()
    backgroundHisto.Write()
    plotfile.Close()

    # draw background for each of the groups on the same histogram
    for group in groupList:

        valHistList_loose[group].SetMaximum(ymax_loose)
        valHistList_loose[group].SetMarkerStyle(0)
        if (groupList.index(group) == 0):
            # first histogram to be drawn
            valHistList_loose[group].GetXaxis().SetTitle(axisTitle[cutName])
            valHistList_loose[group].GetYaxis().SetTitle("Entries")
            valHistList_loose[group].SetTitle(histTitle[histname]+", "+lepton_name+" channel, prompt")
            drawhist(valHistList_loose[group],"h")
        else:
            # overlay
            drawhist(valHistList_loose[group],"hsame")
            pass
        pass
    
    datahisto_loose.SetMarkerStyle(21)
    drawhist(datahisto_loose,"esame")
    valLegend.Draw()
    CMSPlotDecoration(lepton_name,lumisum)
    canv.Update()
    canv.Print(filename.replace(".","_prompt."))

    # also dump these histograms into a root file
    plotfile=ROOT.TFile.Open(filename.replace(".","_prompt.").replace(fformat,".root"),"RECREATE")
    datahisto_loose.Write()
    for group in groupList:
        if group.find("Signal")>=0:
            signalHisto=valHistList_loose[group].Clone(datahisto.GetName()+"_SignalMC")
            continue
        backgroundHisto=valHistList_loose[group].Clone(datahisto.GetName()+"_BackgroundMC")
        break
    for i in range(signalHisto.GetNbinsX()):
        sumval=signalHisto.GetBinContent(i+1)
        sumerr=signalHisto.GetBinError(i+1)
        bkgval=backgroundHisto.GetBinContent(i+1)
        bkgerr=backgroundHisto.GetBinError(i+1)
        signalHisto.SetBinContent(i+1,sumval-bkgval)
        signalHisto.SetBinError(i+1,math.sqrt(sumerr*sumerr-bkgerr*bkgerr))
        pass
    signalHisto.Write()
    backgroundHisto.Write()
    plotfile.Close()

    if massplots:
        # draw mass distribution for candidates passing all cuts
        ymax=max(datahistoMassPass.GetMaximum(),massPassHistList[groupList[0]].GetMaximum())
        if log_plots:
            ymax*=10
        else:
            ymax*=1.2
            pass
        
        # legend
        massPassLegend = ROOT.TLegend(histXLegend["mass"],0.62,histXLegend["mass"]+0.3,0.92)
        massPassLegend.SetFillColor(ROOT.kWhite)
                          
        # draw background for each of the groups on the same histogram
        for group in groupList:
                      
############################################################
            if group.find("Signal")>=0:
                massPassLegend.AddEntry(massPassHistList[group],legendEntry[group],"l")
                pass
            else:
                massPassLegend.AddEntry(massPassHistList[group],legendEntry[group],"f")
                pass
              ############################################################


            
            massPassHistList[group].SetMaximum(ymax)
            massPassHistList[group].SetMarkerStyle(0)
            if (groupList.index(group) == 0):
                massPassHistList[group].SetTitle("di"+lepton_name+" invariant mass, passing all cuts")
                massPassHistList[group].GetXaxis().SetTitle("mass [GeV/c^{2}]")
                massPassHistList[group].GetXaxis().SetNdivisions(1005)
                massPassHistList[group].GetYaxis().SetTitle("Entries")
                drawhist(massPassHistList[group],"h")
            else:
                drawhist(massPassHistList[group],"hsame")
                pass
            pass
        # draw data
        datahistoMassPass.SetMarkerStyle(21)
        drawhist(datahistoMassPass,"esame")
        massPassLegend.AddEntry(datahistoMassPass,"data","p")
        massPassLegend.Draw()
        CMSPlotDecoration(lepton_name,lumisum)
        canv.Update()
        if filename.find("deltaRBetweenLeptons")<0:
            canv.Print(filename.replace("decayLengthSignificance2D","massDisplaced"))
            pass
        
        # draw mass distribution for candidates passing all other cuts but failing this one
        ymax=max(datahistoMassFail.GetMaximum(),massFailHistList[groupList[0]].GetMaximum())
        if log_plots:
            ymax*=10
        else:
            ymax*=1.2
            pass
        
        # legend
        massFailLegend = ROOT.TLegend(histXLegend["massPrompt"],0.62,histXLegend["massPrompt"]+0.3,0.92)
        massFailLegend.SetFillColor(ROOT.kWhite)

        # Draw background for each of the groups on the same histogram
        for group in groupList:

            ############################################################
        
            if group.find("Signal")>=0:
                massFailLegend.AddEntry(massFailHistList[group],legendEntry[group],"l")
                pass
            else:
                massFailLegend.AddEntry(massFailHistList[group],legendEntry[group],"f")
                pass
        
        ############################################################
            
            massFailHistList[group].SetMaximum(ymax)
            massFailHistList[group].SetMarkerStyle(0)
            if (groupList.index(group) == 0):
                massFailHistList[group].SetTitle("di"+lepton_name+" mass, prompt candidates")
                massFailHistList[group].GetXaxis().SetTitle("mass [GeV/c^{2}]")
                massFailHistList[group].GetXaxis().SetNdivisions(1005)
                massFailHistList[group].GetYaxis().SetTitle("Entries")
                drawhist(massFailHistList[group],"h")
            else:
                drawhist(massFailHistList[group],"hsame")
                pass
            pass
        # draw data
        datahistoMassFail.SetMarkerStyle(21)
        drawhist(datahistoMassFail,"esame")
        massFailLegend.AddEntry(datahistoMassFail,"data","p")
        massFailLegend.Draw()
        CMSPlotDecoration(lepton_name,lumisum)
        canv.Update()
        canv.Print(filename.replace("decayLengthSignificance2D","massPrompt").replace("deltaRBetweenLeptons","massDisplacedNoDeltaR"))
        pass
        
    valHistList.clear()
    massPassHistList.clear()
    massFailHistList.clear()
    datahisto.Delete()
    datahistoMassPass.Delete()
    datahistoMassFail.Delete()
    canv.Close()
    return [datamasslist,bkgmasslist]


###################################################
### GET WEIGHTED NUMBER OF CANDIDATES PASSING CUTS
###################################################

def number_of_surviving_candidates(SampleTriggerCombination,candtype,analysis_directory,cuts):
    print "KHDEBUG: disabled"
    return 1
    if candtype!="background" and candtype!="signal":
        print "ERROR: illegal candidate category"
        sys.exit(1)
        pass
    overall_integral=0.0
    for [workdir,trigger,weight] in SampleTriggerCombination:
        # if this is real data then the weight is actually luminosity
        if workdir.find("Data")>=0: weight=1.0
        # the big tree containing cut results for all variables
        treename=analysis_directory+"/dileptons_"+candtype+"_"+trigger\
                  +"/bigTree"
        # make ROOT print the number of entries passing a cut.
        # in order to do this, we plot an arbitrary quantity of which
        # we definitely know the range of values (e.g. oppositeCharge)
        # into a dummy histogram with just one bin
        command="TFile* infile = new TFile(\""+workdir+"/histograms.root\");\n"\
                 +"TTree* tree = infile->Get(\""+treename+"\");\n"\
                 +"TH1F* valhist = new TH1F(\"valhist\",\"valhist\","\
                 +"1,-10.,10.);\n"\
                 +"tree->Project(\"valhist\",\"oppositeCharge\",\"_weight*("+cuts+")\");\n"\
                 +"cout << \"RES\" << \"ULT \" << valhist->Integral() << endl;\n"\
                 +"infile.Close();\n"\
                 +"gApplication->Terminate();\n"
        result=os.popen("root -b -l << EOF\n"+command+"\nEOF\n").readlines()
        integral=-999;
        for line in result:
            if line.find("RESULT")>=0:
                integral=float(line.split()[1])
                pass
            pass
        if (integral>=0):
            overall_integral+=integral*weight
        else:
            print "ERROR for",workdir,trigger
            pass
        pass
    return overall_integral
   
    

#############################################
### SCAN SAMPLE DESCRIPTION FILE
#############################################

def sample_cff_code(workdir):
    # find sample description file
    if not os.path.isdir(workdir):
        print "ERROR: directory",workdir,"does not exist"
        sys.exit(1)
    sample_cff = ""
    for filename in os.listdir(workdir):
        if filename.find("_cff.py")>0:
            sample_cff=filename
            pass
        pass
    if sample_cff=="":
        print "ERROR: sample description file not found in",workdir
        sys.exit(1)
        pass
    samplefile=open(workdir+"/"+sample_cff,"r")
    content=""
    for line in samplefile.readlines():
        content+=line
        pass
    samplefile.close()
    code=compile(content,"<string>","exec")
    return code


#############################################
### GET MC SAMPLE SIZE AND CROSS-SECTION
#############################################

def get_sample_weight(mcworkdir):
    
    # get cross-section and sample size from sample description file
    sampleXSec=-1
    sampleNumEvents=0
    sampleBaseDir=""
    samplePatFiles=[]
    exec(sample_cff_code(mcworkdir))
    if sampleXSec==-1:
        print "ERROR: sample description file does not contain sampleXSec"
        sys.exit(1)
        pass
    if sampleBaseDir=="":
        print "ERROR: sample description file does not contain sampleBaseDir"
        sys.exit(1)
        pass
    if sampleNumEvents==0:
        print "ERROR: sample description file does not contain sampleNumEvents"
        sys.exit(1)
        pass
    if len(samplePatFiles)==0:
        print "ERROR: sample description file does not contain samplePatFiles"
        sys.exit(1)
        pass

    # check number of processed events (after prefilter, if any)
    histfile=ROOT.TFile.Open(mcworkdir+"/histograms.root")
    num_events_processed=0
    try:
        num_events_processed=histfile.Get("prefilterPassTwo/numSignalPass").GetEntries()
    except:
        pass

    # how many of them ended up being analyzed? (= not rejected by goodcoll)
    num_events_analyzed=0
    found=0
    try:
        num_events_analyzed=histfile.Get(eAnalysis+"/trig/eventsVsRun").GetEntries()
        found=1
    except:
        pass
    try:
        num_events_analyzed=histfile.Get(muAnalysis+"/trig/eventsVsRun").GetEntries()
        found=1
    except:
        pass
    if not found:
        print "ERROR: unable to retrieve histogram with number of events from",mcworkdir
        return 0.0

    # check number of events before prefilter (if any)
    numevents_before_prefilter=-num_events_processed
    numevents_after_prefilter=-num_events_processed
    if os.path.exists(mcworkdir+"/prefilter.root"):
        histfile=ROOT.TFile.Open(mcworkdir+"/prefilter.root","R")
        try:
            numevents_before_prefilter=histfile.Get("isoTrackPrefilter/numSignal").GetEntries()
            numevents_after_prefilter=histfile.Get("isoTrackPrefilter/numSignalPass").GetEntries()
        except:
            print "ERROR: prefilter file in",mcworkdir,"seems to be corrupt"
            pass
        pass

    # this weight will have to be multiplied with integrated lumi to get the
    # expected number of events from this physics process
    sampleweight=sampleXSec/(num_events_processed*1.0\
                             *numevents_before_prefilter\
                             /numevents_after_prefilter)

    print "MC sample",mcworkdir.split("/")[-1],":"
    print "   "\
          +str(int(.5+abs(numevents_before_prefilter)/sampleNumEvents*100.))\
          +"% ("+str(abs(int(numevents_before_prefilter)))\
          +"/"+str(sampleNumEvents)\
          +") of total sample size available in PAT"
    print "   resulting sample weight (to be multiplied by integrated lumi):",\
          sampleweight
    if numevents_before_prefilter>0:
        print "   fraction of events passing the prefilter: ",\
              float(numevents_after_prefilter)/numevents_before_prefilter
    else:
        print "   no prefilter applied"
        pass
    print "   fraction of events passing the goodcollision filter:",\
          float(num_events_analyzed)/num_events_processed

    # cross-check that we didn't lose any events in analysis stage
    # (through exceptions or unreadable files). the problem is that
    # we do lose a small number of events from the primary vertex filter.
    # to be addressed.
    if num_events_processed!=abs(numevents_after_prefilter):
        print "ERROR:",mcworkdir,"has",numevents_after_prefilter,\
              "passing the prefilter, but",\
              num_events_processed,"events processed in analysis"

    return sampleweight
    

def trigger_threshold(hltpath):
    barename=hltpath.replace("HLT_","")
    if barename.find("_v")>0: barename=barename[:barename.find("_v")]
    specifiers=barename.split("_")
    threshold=-1
    for entry in specifiers:
        if not entry[-1].isdigit(): continue
        pos=-2
        while entry[pos].isdigit() and abs(pos)<len(entry): pos-=1
        threshold=int(entry[pos+1:])
    return threshold


#############################################
### PROCESS INDIVIDUAL DATASET
#############################################


def modifyString(line):
    modifiedString = ""
    foundQuote = False
    for char in line:
        if char == "\"":
            foundQuote = not foundQuote
        if char == "," and foundQuote:
            modifiedString += "###"
        else:
            modifiedString += char
    return modifiedString

def analyze_lumi_and_trigger(dataworkdir,lepton_name,analysis_directory):

    # get dCache directory of this sample from sample description file
    sampleBaseDir=""
    exec(sample_cff_code(dataworkdir))
    if sampleBaseDir=="":
        print "ERROR: sample description file does not contain sampleBaseDir"
        sys.exit(1)
        pass

    # now get analysis config file (for the list of triggers that was looked at)
    if not os.path.exists(dataworkdir+"/main_cfg.py"):
        print "ERROR: could not find main_cfg.py in workdir"
        sys.exit(1)
        pass
    ehltPaths=[]
    muhltPaths=[]
    configfile=open(dataworkdir+"/main_cfg.py","r")
    content=""
    for line in configfile.readlines():
        if line.find("HLT")>0 and line.find("pathNames")<0:
            content+=line.replace("process.","").replace("Analysis.","").replace("cms.vstring(","[").replace(")","]")
            pass
        pass
    configfile.close()
    code=compile(content,"<string>","exec")
    exec(code)
    if len(ehltPaths)==0 or len(muhltPaths)==0:
        print "ERROR: process.eTrackAnalysis.hltPaths or process.muTrackAnalysis.hltPaths not found in main_cfg.py"
        sys.exit(1)
        pass
    if lepton_name=="muon":
        selectedHLTPaths=muhltPaths
        unbiasedHLTPaths=ehltPaths
    else:
        selectedHLTPaths=ehltPaths
        unbiasedHLTPaths=muhltPaths
        pass

    # get maximum run range from histogram file
    histfile=ROOT.TFile.Open(dataworkdir+"/histograms.root")
    runrangehist=histfile.Get(analysis_directory+"/trig/eventsVsRun")
    try:
        runMin=int(runrangehist.GetXaxis().GetXmin())
        runMax=int(runrangehist.GetXaxis().GetXmax())
    except:
        # looks like this histogram file is corrupt or otherwise unusable
        print "ERROR: histogram.root unusable."
        sys.exit(1)
    histfile.Close()



    
    # get luminosity information
    lumiOverview=dataworkdir+"/lumiOverview.csv"
    lumiDetails=dataworkdir+"/lumiResult.csv"

    # FIXME: uncomment
    #os.system("rm -f "+lumiOverview+" "+lumiDetails)

    if not os.path.exists(lumiOverview):
        cmd = "srmcp -2 \""+sampleBaseDir.replace("root://xrootd.rcac.purdue.edu", "srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN=")+"/lumiOverview.csv\" \"file:///"+lumiOverview+"\""
        print cmd
        os.system(cmd)
    
    if not os.path.exists(lumiOverview):
        # ok, for some reason we cannot get these files from dcache.
        # check whether the make_pat working directory still exists
        # where those files were probably created in
        patdirs=os.popen("ls -1rtd "+dataworkdir[:dataworkdir.find("_analysis")]\
                         +"_pat*").readlines()
        if len(patdirs)>0:
            print "WARNING: using lumiOverview.csv from",patdirs[-1].strip()
            os.system("cp "+patdirs[-1].strip()+"/lumiOverview.csv "\
                      +lumiOverview+" &> /dev/null")
            pass
        pass

    # FIXME: uncomment
    if not os.path.exists(lumiDetails):
        cmd = "srmcp -2 \""+sampleBaseDir.replace("root://xrootd.rcac.purdue.edu", "srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN=")+"/lumiResult.csv\" \"file:///"+lumiDetails+"\""
        os.system(cmd)
    
    if not os.path.exists(lumiDetails):
        # same procedure as above
        patdirs=os.popen("ls -1rtd "+dataworkdir[:dataworkdir.find("_analysis")]\
                         +"_pat*").readlines()
        if len(patdirs)>0:
            print "WARNING: using lumiResult.csv from",patdirs[-1].strip()
            os.system("cp "+patdirs[-1].strip()+"/lumiResult.csv "\
                      +lumiDetails+" &> /dev/null")
            pass
        pass
    if not os.path.exists(lumiOverview) or not os.path.exists(lumiDetails):
        # ok, now give up
        print "ERROR: unable to retrieve lumi files from "+sampleBaseDir
        sys.exit(1)
        pass

    # read resulting csv file for delivered lumi and overall recorded lumi
    lumiCSV=open(lumiOverview)
    lumi_delivered=0.0
    lumi_recorded=0.0
    recLumiPerRun={}
    for line in lumiCSV.readlines():
        # if len(line.split(","))==4:
        #     # old lumiCalc format
        #     (run,dlumi,rlumi,hlumi)=line.split(",")
        # else:
        # lumiCalc2.py format
        #     entries=line.split(",")
        #     run=entries[0]
        #     dlumi=entries[2]
        #     rlumi=entries[-1]
        #     pass
        modifiedString = modifyString(line)
        entries=modifiedString.split(",")
        run=entries[0].replace("###", ",")
        dlumi=entries[2].replace("###", ",")
        rlumi=entries[-1].replace("###", ",")
        try:
            run=int(run)
            dlumi=float(dlumi)/1e6 # convert from /microbarn to /picobarn
            rlumi=float(rlumi)/1e6 # convert from /microbarn to /picobarn
        except:
            continue
        if run<runMin or run>runMax:
            print "ERROR: json contains run",run,"outside expected range [",\
                  runMin,",",runMax,"]"
            #sys.exit(1)
            pass
        lumi_delivered+=dlumi
        lumi_recorded+=rlumi
        recLumiPerRun[run]=rlumi
        pass
    lumiCSV.close()
    print "  delivered lumi for this dataset:",lumi_delivered,"/pb"
    print "  recorded lumi for this dataset:",lumi_recorded,"/pb"

    # read and analyze resulting csv file for recorded lumi
    lumiCSV=open(lumiDetails)
    lumiPerRun={}
    lumiPerTrigger={}
    firstRun={}
    lastRun={}
    maxLumi={}
    previousBestTrigger="None"
    triggerWithMaxLumi={}
    for line in lumiCSV.readlines():
        if line.startswith("Run"):
            continue
        # read line from csv
        if len(line.split(","))==3:
            # old style lumiCalc result
            (run,hltpath,lumi)=line.split(",")
        else:
            # new style lumiCalc2.py
            # print "line = "+line
            modifiedString = modifyString(line)
            (run, lumiSL, recorded, hltpath, l1bit, lumi) = modifiedString.split(",")
            run = run.replace("###", ",")
            lumiSL = lumiSL.replace("###", ",")
            recorded = recorded.replace("###", ",")
            hltpath = hltpath.replace("###", ",").split("(")[0]
            l1bit = l1bit.replace("###", ",")
            lumi = lumi.replace("###", ",")
            # print run
            # print hltpath.split("(")[0]
            # print l1bit
            # print lumi
            pass
        if not hltpath in selectedHLTPaths: continue
        try:
            run=int(run)
            lumi=float(lumi)/1e6 # convert from /microbarn to /picobarn
        except:
            continue
        # accumulate luminosity for each trigger
        if not lumiPerTrigger.has_key(hltpath):
            lumiPerTrigger[hltpath]=0.0
            lumiPerRun[hltpath]=ROOT.TH1F("lumiPerRun_"+hltpath,
                                          "recorded lumi per run for "+hltpath,
                                          runMax-runMin+1,runMin,runMax)
            firstRun[hltpath]=runMax+1
            lastRun[hltpath]=0
            pass
        lumiPerTrigger[hltpath]+=lumi
        lumiPerRun[hltpath].Fill(run,lumi)
        if lumi>0:
            if run<firstRun[hltpath]: firstRun[hltpath]=run
            if run>lastRun[hltpath]: lastRun[hltpath]=run
            pass
        # find best trigger for each run
        if not maxLumi.has_key(run):
            maxLumi[run]=0.0
            triggerWithMaxLumi[run]="None"
            pass
        if lumi>maxLumi[run]:
            if maxLumi[run]>0:
                # there already was one active trigger from our selection here.
                # this is potentially dangerous because we might double-count
                # data from this run when looking at selections with different
                # triggers. (Though we will double-count the luminosity too,
                # and thus things might be ok except for statistical correlation)
                print "WARNING: more than one analysis trigger in run",run
            maxLumi[run]=lumi
            triggerWithMaxLumi[run]=hltpath
            pass
        # if there is more than one option, take the one with lower threshold
        if lumi==maxLumi[run] and trigger_threshold(hltpath)<trigger_threshold(triggerWithMaxLumi[run]):
            triggerWithMaxLumi[run]=hltpath
            pass
            
        # always give preference to the trigger that we used beforehand
        if lumi==maxLumi[run] and hltpath==previousBestTrigger:
            triggerWithMaxLumi[run]=hltpath
        previousBestTrigger=triggerWithMaxLumi[run]
        pass
    lumiCSV.close()

    # summarize results by trigger
    for trigger in selectedHLTPaths:
        if not lumiPerTrigger.has_key(trigger):
            lumiPerTrigger[trigger]=0.0
            firstRun[trigger]=0
            lastRun[trigger]=0
            pass
        if lumiPerTrigger[trigger]>0:
            print "  recorded lumi for %40s : %10.8f in run range %i-%i"\
                  %(trigger,lumiPerTrigger[trigger],firstRun[trigger],lastRun[trigger])
            pass
        pass
    # add dummy trigger
    lumiPerTrigger["anyTrigger"]=lumi_recorded
    firstRun["anyTrigger"]=runMin
    lastRun["anyTrigger"]=runMax
    
    # summarize results by run
    runlist=[]
    lumisum=0.0
    best_triggers=[]
    for run in maxLumi.keys():
        if recLumiPerRun[run]>0:
            if not triggerWithMaxLumi[run] in best_triggers:
                best_triggers.append(triggerWithMaxLumi[run])
                pass
            runlist.append("  run "+str(run)+": best trigger "+triggerWithMaxLumi[run]+" live %4.1f%%"%(100*maxLumi[run]/recLumiPerRun[run]))
        else:
            runlist.append("  run "+str(run)+": no data recorded")
        lumisum+=maxLumi[run]
        pass
    runlist.sort()
    for line in runlist:
        print line
        pass
    
    print "  => total lumi with best triggers (",best_triggers,") is",lumisum,\
          "/pb out of",lumi_recorded,"/pb\n"
    if (lumisum-lumi_recorded)>1e-5:
        print "ERROR: sum of trigger lumis (",lumisum,") exceeds total recorded (",\
              lumi_recorded,")"
        sys.exit(1)

    best_trigger_lumi=[]
    for trigger in best_triggers:
        best_trigger_lumi.append(lumiPerTrigger[trigger])
    return [lumisum,best_triggers,best_trigger_lumi]

#############################################
### HISTOGRAMS OF RECONSTRUCTED SIGNAL SHAPE
#############################################

def dump_signal_shape_histos(lepton_name,ptCut,limitfolder):

    # signal shape for limit setting code
    for workdir in workdirs_signal:
        sampleID=workdir.split("/")[-1].replace("_analysis","")
        masspeak=float(sampleID.split("_")[2].replace("F","").replace("L",""))
        lowerbound=0.5*masspeak
        if lowerbound<50: lowerbound=0
        upperbound=1.5*masspeak
        if upperbound<100: upperbound=2*masspeak
        histfile=ROOT.TFile.Open(workdir+"/histograms.root")
        if lepton_name.find("mu")>=0:
            treedir=muAnalysis+"/dileptons_signal_HLT_L2DoubleMu23_NoVertex_v1"
        else:
            treedir=eAnalysis+"/dileptons_signal_HLT_DoublePhoton33_v2"
            pass
        [valhist,valhist_loose,masshist,rejecthist]=get_histogram(workdir,treedir,"_mass",
                                                                  100,0,100,
                                                                  lowerbound,upperbound,
                                                                  ptCut)
        masshist.SetTitle("di"+lepton_name+" mass distribution, signal")
        masshist.SetName("dileptonmass_signal")
        outfile=ROOT.TFile.Open(limitfolder+"/signal_shape_"+lepton_name+"_"+sampleID+".root",
                                "RECREATE")
        masshist.Write()
        outfile.Close()

        histfile.Close()
        pass
    return


#############################################
### PREPARE DATA/MC OVERLAY PLOTS
#############################################

def makePlots(SampleTriggerCombination,ptCut,
              workdirs_background,workdirs_signal,
              mcweights,mcSignalWeights,
              lepton_name,analysis_directory,plotfolder):


    begintime=time.time()

    # get total luminosity for this set of samples
    lumisum=0.0
    for [dataworkdir,trigger,lumi] in SampleTriggerCombination:
        lumisum+=lumi
        sampleID=lepton_name+"_pt%i"%ptCut
        pass

    # corresponding normalization for background samples
    mcfactors=[]
    for weight in mcweights:
        mcfactors.append(weight*lumisum)
        pass

#################################################################
    # corresponding normalization for signal samples
    mcfactorsSignal=[]
    for weight in mcSignalWeights:
        mcfactorsSignal.append(weight*lumisum)
        pass
#################################################################

    # Make directory to store plots
    folder = plotfolder + "/" + sampleID + "/"
    if not os.path.isdir(folder):
        os.mkdir(folder)
        pass
    # subfolder for outputs related to limit calculation
    limitfolder=folder+"/limits"
    if not os.path.isdir(limitfolder):
        os.mkdir(limitfolder)
        pass


    print "preparing plots for the following samples and triggers:"
    for [dataworkdir,trigger,lumi] in SampleTriggerCombination:
        print "   ",trigger,"in",dataworkdir
        pass
    print "corresponding integrated luminosity:",lumisum
    print "-> using directory",folder
        
    #----------------------
    # EFFICIENCY TEXT FILES
    #----------------------

    #pileupReweighting.
    dump_reweighted_efficiencies(lepton_name,ptCut,limitfolder,eAnalysis,muAnalysis,workdirs_signal)
    dump_signal_shape_histos(lepton_name,ptCut,limitfolder)

    #---------------------
    # PLOTS
    #---------------------

    # primary vertex distributions
    for plot in ["numPV_central","numPV_low","numPV_high","numPV_veryhigh"]:
        overlayPlot(SampleTriggerCombination,workdirs_background,mcfactors,
                    analysis_directory+"/weights/"+plot,
                    folder+lepton_name+"_"+plot+fformat,lumisum,0)
        pass

    # fraction of actual true leptons in candidate (MC only)
    overlayPlot([],workdirs_background,mcfactors,
                analysis_directory+"/dileptons/number_of_actual_leptons",
                folder+"number_of_actual_"+lepton_name+"s"+fformat,0)
    
    # Lists to store all the required data about the cut efficiencies
    efficiencyListData = []
    efficiencyListMC = []
    efficiencyListSignal = []
           
    # decay length significance. we treat this cut in a special way
    # because its inversion gives us the control distribution of prompt
    # candidates, and thus we want additional plots/diagnostics here
    [datamasslist,bkgmasslist]=treeOverlayPlot(SampleTriggerCombination,
                                               workdirs_background,
                                               workdirs_signal,mcfactors,
                                               mcfactorsSignal,
                                               lepton_name,
                                               analysis_directory+\
                                               "/dileptons_background_TRIGGER/",
                                               "decayLengthSignificance2D",
                                               folder+"di"+lepton_name+\
                                               "_decayLengthSignificance2D"+fformat,
                                               ptCut,lumisum,
                                               efficiencyListData,
                                               efficiencyListMC,
                                               efficiencyListSignal)
    
    # store mass lists for limit calculation
    minmass=999
    maxmass=0
    datalistfile=open(limitfolder+"/masses_data_"+lepton_name+".txt","w")
    for entry in datamasslist:
        datalistfile.write("%10.4f %10.4f\n"%(entry[0],entry[1]))
        if entry[0]>maxmass: maxmass=entry[0]
        if entry[0]<minmass: minmass=entry[0]
        pass
    datalistfile.close()
    bkglistfile=open(limitfolder+"/masses_backgroundMC_"+lepton_name+".txt","w")
    for entry in bkgmasslist:
        bkglistfile.write("%10.4f %10.4f\n"%(entry[0],entry[1]))
        if entry[0]>maxmass: maxmass=entry[0]
        if entry[0]<minmass: minmass=entry[0]
        pass
    bkglistfile.close()
    # now also create histograms
    datahist=ROOT.TH1F("datamass","mass distribution of candidates in data",
                       100,minmass*0.9,maxmass*1.1)
    for entry in datamasslist: datahist.Fill(entry[0],entry[1])
    outfile=ROOT.TFile.Open(limitfolder+"/masses_data_"+lepton_name+".root",
                            "RECREATE")
    datahist.Write()
    outfile.Close()
    bkghist=ROOT.TH1F("backgroundmass","mass distribution of candidates in MC",
                       100,minmass*0.9,maxmass*1.1)
    for entry in bkgmasslist: bkghist.Fill(entry[0],entry[1])
    outfile=ROOT.TFile.Open(limitfolder+"/masses_backgroundMC_"+lepton_name+".root",
                            "RECREATE")
    bkghist.Write()
    outfile.Close()

    # get list of all quantities that are available to plot
    cutNames=[]
    for [workdir,trigger,lumi] in SampleTriggerCombination:
        histfile=ROOT.TFile.Open(workdir+"/histograms.root")
        for analysisDir in [eAnalysis,muAnalysis]:
            if histfile.Get("/"+analysisDir+"/dileptons_background_"+trigger):
                histfile.cd("/"+analysisDir+"/dileptons_background_"+trigger)
                branchlist=ROOT.gDirectory.Get("bigTree").GetListOfBranches()
                for branch in branchlist:
                    entry=branch.GetName()
                    if entry[0]=="_": continue
                    if entry.find("_pass")>0: continue
                    # exclude certain entries we definitely do not want
                    if entry in ["decayLengthSignificance2D", # already done
                                 "dPhitriggerCorr",
                                 "differentTrigObjects",
                                 "leptonQualityL",
                                 "leptonQualityH",
                                 "passesAllCuts",
                                 "passesAllCutsIgnoreLifetime",
                                 "mass_calocorr", # masses taken from elsewhere
                                 "mass_corr",
                                 "mass_scalecorr",
                                 "mass_triggercorr",
                                 "validTracks",
                                 "validVertex"]: continue
                    if not entry in cutNames: cutNames.append(entry)
                    pass
                pass
            pass
        histfile.Close()
        pass


    if not do_all_plots:
        # only do the most important plots (for the PAS)
        cutNames=["trackerIsolationL","trackerIsolationH","dPhicorr"]
        pass
    
    for cutName in cutNames:
        treeOverlayPlot(SampleTriggerCombination,workdirs_background,workdirs_signal,
                        mcfactors,mcfactorsSignal,lepton_name,
                        analysis_directory+"/dileptons_background_TRIGGER/",cutName,
                        folder+"di"+lepton_name+"_"+cutName+fformat,ptCut,lumisum,
                        efficiencyListData,
                        efficiencyListMC,efficiencyListSignal)
        pass

    listOfCuts=[
        "eta_cand_pass",
        "numStandAloneMuons_pass",
        "leptonPtL_pass && leptonPtH_pass",
        "leptonEtaL_pass && leptonEtaH_pass",
        "leptonAbsD0significanceL_pass && leptonAbsD0significanceH_pass",
        "trackerIsolationL_pass && trackerIsolationH_pass",
        "oppositeCharge_pass",
        "vetoBackToBack_pass",
        "deltaRBetweenLeptons_pass",
        "numCaloMatches_pass",
        "numTrigMatches_pass",
        "differentTrigObjects_pass",
        "validTracks_pass && validVertex_pass && vertexChi2_pass",
        "dPhicorr_pass",
        "maxHitsBeforeVertex_pass",
        "decayLengthSignificance2D_pass",
        "passesAllCuts"
        ]
    if analysis_directory.find("mu")>=0:
        listOfCuts.remove("numCaloMatches_pass")
        pass

    print "==========efficiency output for data,",analysis_directory
    appliedCuts="eta_cand_pass"
    for additionalCut in listOfCuts:
        appliedCuts+=" && "+additionalCut
        sum=number_of_surviving_candidates(SampleTriggerCombination,"background",
                                           analysis_directory,appliedCuts)
        print "%-50s"%additionalCut,sum
        pass
    print "======================================"

    # now measure efficiency to find a matching supercluster
    # for candidates passing all cuts except trigger match
    if analysis_directory[0]=="e":
        print "==========efficiency to match supercluster in data"
        appliedCuts="eta_cand_pass"
        for additionalCut in listOfCuts:
            if additionalCut=="numTrigMatches_pass": continue
            if additionalCut=="numCaloMatches_pass": continue
            if additionalCut=="differentTrigObjects_pass": continue
            if additionalCut=="decayLengthSignificance2D_pass": continue
            if additionalCut.find("leptonAbsD0significance")>=0: continue
            if additionalCut=="dPhicorr_pass": continue
            if additionalCut=="passesAllCuts": continue
            appliedCuts+=" && "+additionalCut
            pass
        sum1=number_of_surviving_candidates(SampleTriggerCombination,
                                            "background",
                                            analysis_directory,appliedCuts)
        appliedCuts+=" && numCaloMatches_pass"
        sum2=number_of_surviving_candidates(SampleTriggerCombination,
                                            "background",
                                            analysis_directory,appliedCuts)
        print "fraction of candidates with matching supercluster:",\
              sum2,"/",sum1
        print "======================================"
        pass

    # find list of triggers for MC
    mctriggers=[]
    for [dataworkdir,trigger,lumi] in SampleTriggerCombination:
        mctrig=replacementTrigger[trigger]
        if not mctrig in mctriggers: mctriggers.append(mctrig)
    if len(mctriggers)==0:
        mctriggers.append("anyTrigger")
    if len(mctriggers)!=1:
        # need to trim list of MC triggers down to one.
        # pick the one with highest p_t threshold.
        # this threshold needs to be exceeded by an offline cut!
        highestpt=0
        highestpttrigger=""
        for trigger in mctriggers:
            if trigger_threshold(trigger)>highestpt:
                highestpt=trigger_threshold(trigger)
                highestpttrigger=trigger
                pass
            pass
        mctriggers=[highestpttrigger]
        pass
    # construct corresponding sample/trigger combinations for background MC
    MCSampleTriggerCombination=[]
    for i in range(len(workdirs_background)):
        for trigger in mctriggers:
            MCSampleTriggerCombination.append([workdirs_background[i],trigger,mcfactors[i]])
 
    print "==========efficiency output for background MC,",analysis_directory
    appliedCuts="eta_cand_pass"
    for additionalCut in listOfCuts:
        appliedCuts+=" && "+additionalCut
        sum=number_of_surviving_candidates(MCSampleTriggerCombination,
                                           "background",
                                           analysis_directory,appliedCuts)
        print "%-50s"%additionalCut,sum
        pass
    print "======================================"

    # construct corresponding sample/trigger combinations for signal MC
    for i in range(len(workdirs_signal)):
        MCSampleTriggerCombination=[]
        for trigger in mctriggers:
            MCSampleTriggerCombination.append([workdirs_signal[i],trigger,1.0])
            pass
        print "==========efficiency output for "+workdirs_signal[i].split("/")[-1],",",analysis_directory
        appliedCuts="eta_cand_pass"
        for additionalCut in listOfCuts:
            appliedCuts+=" && "+additionalCut
            sum=number_of_surviving_candidates(MCSampleTriggerCombination,
                                               "signal",
                                               analysis_directory,appliedCuts)
            print "%-50s"%additionalCut,sum
            pass
        print "======================================"
        pass
    
    
    #---------------------
    # Efficiency Output
    #---------------------

    #Widths of each column
    col1Width = 26
    col2Width = 25
    col3Width = 30
    col4Width = 21

    #Print header for efficiency table
    print "\n"
    print "CUT EFFICIENCIES: DATA",lepton_name
    print " "*(col1Width - len("CutName"))                        +"CutName",
    print " "*(10 + col2Width - len("PassesThisAndAllOtherCuts"))+"PassesThisAndAllOtherCuts",
    print " "*(-6 + col3Width - len("PassesAllOtherCuts"))       +"PassesAllOtherCuts",
    print " "*(-4 + col4Width - len("Efficiency"))               +"Efficiency"
    print "#"*104

    #Print the efficiency data
    for data in efficiencyListData:

        #The string below contains a single row of the table with all elements alligned
        formattedStr = " "*(col1Width - len(data['cutName']))+str(data['cutName'])
        formattedStr+= " "*(col2Width - len(str(data['passesThisAndAllOtherCuts'])))
        formattedStr+= str(data['passesThisAndAllOtherCuts'])
        formattedStr+= " "*(col3Width - len(str(data['passesAllOtherCuts'])))+str(data['passesAllOtherCuts'])
        formattedStr+= " "*(col4Width - len(str(float("%.2e"%data['efficiency']))))
        formattedStr+= str(float("%.2e"%data['efficiency']))+"%"    
        print formattedStr
    
    #Print header for efficiency table
    print "\n"
    print "CUT EFFICIENCIES: BACKGROUND MC", lepton_name
    print " "*(col1Width - len("CutName"))                        +"CutName",
    print " "*(10 + col2Width - len("PassesThisAndAllOtherCuts"))+"PassesThisAndAllOtherCuts",
    print " "*(-6 + col3Width - len("PassesAllOtherCuts"))       +"PassesAllOtherCuts",
    print " "*(-4 + col4Width - len("Efficiency"))               +"Efficiency"
    print "#"*104

    #Print the efficiency data
    for data in efficiencyListMC:

        #The string below contains a single row of the table with all elements alligned
        formattedStr = " "*(col1Width - len(data['cutName']))+str(data['cutName'])
        formattedStr+= " "*(col2Width - len(str(data['passesThisAndAllOtherCuts'])))
        formattedStr+= str(data['passesThisAndAllOtherCuts'])
        formattedStr+= " "*(col3Width - len(str(data['passesAllOtherCuts'])))+str(data['passesAllOtherCuts'])
        formattedStr+= " "*(col4Width - len(str(float("%.2e"%data['efficiency']))))
        formattedStr+= str(float("%.2e"%data['efficiency']))+"%"    
        print formattedStr
    
    #Print header for efficiency table
    print "\n"
    print "CUT EFFICIENCIES: SIGNAL MC", lepton_name
    print " "*(col1Width - len("CutName"))                        +"CutName",
    print " "*(10 + col2Width - len("PassesThisAndAllOtherCuts"))+"PassesThisAndAllOtherCuts",
    print " "*(-6 + col3Width - len("PassesAllOtherCuts"))       +"PassesAllOtherCuts",
    print " "*(-4 + col4Width - len("Efficiency"))               +"Efficiency"
    print "#"*104

    #Print the efficiency data
    for data in efficiencyListSignal:

        #The string below contains a single row of the table with all elements alligned
        formattedStr = " "*(col1Width - len(data['cutName']))+str(data['cutName'])
        formattedStr+= " "*(col2Width - len(str(data['passesThisAndAllOtherCuts'])))
        formattedStr+= str(data['passesThisAndAllOtherCuts'])
        formattedStr+= " "*(col3Width - len(str(data['passesAllOtherCuts'])))+str(data['passesAllOtherCuts'])
        formattedStr+= " "*(col4Width - len(str(float("%.2e"%data['efficiency']))))
        formattedStr+= str(float("%.2e"%data['efficiency']))+"%"    
        print formattedStr
        pass
    
    endtime=time.time()
    print "+++this took",endtime-begintime,"seconds"
    return



# trigger efficiency measurements on unbiased sample
def triggerEfficiency(SampleTriggerCombination,treeDir):
    
    # Initialise the count of the number of events for the different triggers
    sumTrig = 0
    anyTrig = 0

    curDir = ""
    
    for [workdir,trigger,lumi] in SampleTriggerCombination:
        if curDir != workdir: #Check the file is not already open
            f = ROOT.TFile.Open(workdir + "/histograms.root")
            anyTrig += f.Get(treeDir+"/dileptons_background_anyTrigger/"
                             +"numTrigMatches").GetEntries("passesAllOtherCutsIgnoreLifetime")
            curDir = workdir
            pass
        
        sumTrig += f.Get(treeDir+"/dileptons_background_"+trigger+"/"
                         +"numTrigMatches").GetEntries("passesAllOtherCutsIgnoreLifetime")
        pass

    # Calculate the trigger efficiency
    if (anyTrig > 0):
        efficiency = 100.*float(sumTrig)/float(anyTrig)
        pass
    else:
        efficiency = 0
        pass
    
    # Print filename
    print "\nTrigger efficiency results\n"
   
    # Print header for efficiency table
    print " "*(8  - len("sumTrig"))    + "sumTrig",
    print " "*(6  - len("anyTig"))     + "anyTrig",
    print " "*(11 - len("Efficiency")) + "Efficiency"
    print "#"*28

    # Print the efficiency data
    outputStr =  " "*(8  - len(str(sumTrig)))+ str(sumTrig)
    outputStr+=  " "*(8  - len(str(anyTrig)))+ str(anyTrig)
    outputStr+=  " "*(11 - len(str(float("%.2e"%efficiency))))+ str(float("%.2e"%efficiency))+"%\n"
    print outputStr

    f.Close()
    return
    

#=======================================================================
#=======================================================================
#==== MAIN
#=======================================================================
#=======================================================================


    
#############################################
### PREPARATIONS
#############################################

ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch()
ROOT.TH1.SetDefaultSumw2()
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.Macro( os.environ["LOCALRT"]+'/src/HarderAnalysis/DisplacedDileptons/test/tdrstyle.C' )
ROOT.gStyle.SetPadTopMargin(0.1);
ROOT.gStyle.SetPadLeftMargin(0.15);
ROOT.gStyle.SetPadRightMargin(0.05);
#ROOT.gStyle.SetOptTitle(1)
#ROOT.gStyle.SetTitleYOffset(1.5)


#############################################
### OBTAIN BACKGROUND MC SCALE FACTORS
#############################################

print "=============================================="
print "EVALUATING MC SAMPLE WEIGHTS: ELECTRON CHANNEL"
print "=============================================="
mcweights_e=[]
for workdir in workdirs_background_e:
    mcweights_e.append(get_sample_weight(workdir))
print "=============================================="
print "EVALUATING MC SAMPLE WEIGHTS: MUON CHANNEL"
print "=============================================="
mcweights_mu=[]
for workdir in workdirs_background_mu:
    mcweights_mu.append(get_sample_weight(workdir))
print "=============================================="
print "EVALUATING MC SAMPLE WEIGHTS: SIGNAL MC"
print "=============================================="
mcweights_sig=[]
for workdir in workdirs_signal:
    # signal cross-section unknown, but we define some value
    # for making signal drawn on top of background MC look good
    mcweights_sig.append(get_sample_weight(workdir))
endtime=time.time()
print "\n"


##############################################
### LUMI+TRIGGER ANALYSIS FOR ALL DATA SAMPLES
##############################################

begintime=time.time()
lumisum=0.0
eSampleTriggerCombination33=[]
eSampleTriggerCombination38=[]
eSampleTriggerCombination43=[]
for workdir in workdirs_data_e:
    print "====================================="
    print "DATA:",workdir
    print "====================================="
    [lumi,best_triggers,best_trigger_lumi]=analyze_lumi_and_trigger(workdir,
                                                                    "electron",
                                                                    eAnalysis)
    # now put the sample/trigger combinations into
    # categories that are being treated together
    for i in range(len(best_triggers)):
        if best_triggers[i].find("DoublePhoton33")>=0:
            eSampleTriggerCombination33.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
            eSampleTriggerCombination38.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
            eSampleTriggerCombination43.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
        elif best_triggers[i].find("DoublePhoton38")>=0:
            eSampleTriggerCombination38.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
            eSampleTriggerCombination43.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
        else:
            eSampleTriggerCombination43.append([workdir,best_triggers[i],
                                                best_trigger_lumi[i]])
            pass
        pass
    lumisum+=lumi
    print "\n"
    pass
print "------ total lumi processed in electron channel:",lumisum,"/pb ------"
endtime=time.time()
print "------ processing time:",endtime-begintime,"seconds\n\n"


begintime=time.time()
lumisum=0.0
muSampleTriggerCombination23=[]
muSampleTriggerCombination30=[]
for workdir in workdirs_data_mu:
    print "====================================="
    print "DATA:",workdir
    print "====================================="
    [lumi,best_triggers,best_trigger_lumi]=analyze_lumi_and_trigger(workdir,
                                                                    "muon",
                                                                    muAnalysis)
    # now put the sample/trigger combinations into
    # categories that are being treated together
    for i in range(len(best_triggers)):
        if best_triggers[i].find("HLT_L2DoubleMu23_NoVertex")>=0:
            muSampleTriggerCombination23.append([workdir,best_triggers[i],
                                                 best_trigger_lumi[i]])
            muSampleTriggerCombination30.append([workdir,best_triggers[i],
                                                 best_trigger_lumi[i]])
        else:
            muSampleTriggerCombination30.append([workdir,best_triggers[i],
                                                 best_trigger_lumi[i]])
            pass
        pass
    lumisum+=lumi
    print "\n"
    pass
print "------ total lumi processed in muon channel:",lumisum,"/pb --------\n\n"
endtime=time.time()
print "+++this took",endtime-begintime,"seconds"




##############################################
### DATA/MC PLOTS FOR SELECTED DATA/TRIGGERS
##############################################

if len(eSampleTriggerCombination33)>0:
    print "Doing the 33 GeV photon trigger"
    makePlots(eSampleTriggerCombination33,ePtCut33,workdirs_background_e,
              workdirs_signal,mcweights_e,mcweights_sig,
              "electron",eAnalysis,plotfolder)
    pass
if len(eSampleTriggerCombination38)>0:
    print "Doing the 38 GeV photon trigger"
    makePlots(eSampleTriggerCombination38,ePtCut38,workdirs_background_e,
              workdirs_signal,mcweights_e,mcweights_sig,
              "electron",eAnalysis,plotfolder)
    pass
if len(eSampleTriggerCombination43)>0:
    print "Doing the 43 GeV photon trigger"
    makePlots(eSampleTriggerCombination43,ePtCut43,workdirs_background_e,
              workdirs_signal,mcweights_e,mcweights_sig,
              "electron",eAnalysis,plotfolder)
    pass
if len(muSampleTriggerCombination23)>0:
    print "Doing the 23 GeV muon trigger"
    makePlots(muSampleTriggerCombination23,muPtCut23,workdirs_background_mu,
              workdirs_signal,mcweights_mu,mcweights_sig,
              "muon",muAnalysis,plotfolder)
    pass
if len(muSampleTriggerCombination30)>0:
    print "Doing the 30 GeV muon trigger"
    makePlots(muSampleTriggerCombination30,muPtCut30,workdirs_background_mu,
              workdirs_signal,mcweights_mu,mcweights_sig,
              "muon",muAnalysis,plotfolder)
    pass


#makeEfficiencyPlots()

# trigger efficiency in MC
mctriggers=[]
for datatrigger,mctrigger in replacementTrigger.iteritems():
    if not mctrigger in mctriggers: mctriggers.append(mctrigger)
for workdir in workdirs_signal:
    [edenom,edenom_loose,dm1,dm2]=get_histogram(workdir,eAnalysis\
                                   +"/dileptons_signal_anyTrigger","numTrigMatches",
                                   1,-10,10,0,3000,ePtCut38)
    [mudenom,mudenom_loose,dm1,dm2]=get_histogram(workdir,muAnalysis\
                                    +"/dileptons_signal_anyTrigger","numTrigMatches",
                                    1,-10,10,0,3000,muPtCut30)
    for mctrigger in mctriggers:
        if mctrigger.find("Photon")>=0 and edenom.Integral()>0:
            [enum,enum_loose,em1,em2]=get_histogram(workdir,eAnalysis\
                                         +"/dileptons_signal_%s"%mctrigger,"numTrigMatches",
                                         1,-10,10,0,3000,ePtCut38)
            print "MC trigger efficiency of",mctrigger,"in",eAnalysis,\
                  "channel of",workdir.split("/")[-1],\
                  ":",enum.Integral()/edenom.Integral()
        elif mctrigger.find("Mu")>=0 and mudenom.Integral()>0:
            [enum,enum_loose,em1,em2]=get_histogram(workdir,muAnalysis\
                                         +"/dileptons_signal_%s"%mctrigger,"numTrigMatches",
                                         1,-10,10,0,3000,muPtCut30)
            print "MC trigger efficiency of",mctrigger,"in",muAnalysis,\
                  "channel of",workdir.split("/")[-1],\
                  ":",enum.Integral()/mudenom.Integral()
            pass
        pass
    pass


    
#############################################
### SPECIFIC STUDIES
#############################################

# deltaR between muons. potential problem region for trigger at small deltaR
#print ""
#for workdir in workdirs_signal:
#    histfile=ROOT.TFile.Open(workdir+"/histograms.root")
#    treename=histfile.Get(muAnalysis+"/dileptons_signal_anyTrigger/deltaRBetweenLeptons")
#    canv=ROOT.TCanvas()
#    treename.Draw("deltaRBetweenLeptons","passesAllOtherCutsIgnoreLifetime")
#    hist=0
#    for item in canv.GetListOfPrimitives():
#        if item.IsA().InheritsFrom("TH1"): hist=item
#        pass
#    if hist:
#        hist.GetXaxis().SetTitle("deltaR")
#        title="#Delta R btw leptons, "+workdir.split("/")[-1]
#        title=title[:title.find("_analysis")]
#        hist.SetTitle(title)
#        pass
#    CMSPlotDecoration(muAnalysis)
#    canv.Update()
#    canv.Print(benchmarkfolder+"/deltaR_"+workdir.split("/")[-1]+fformat)
#    histfile.Close()
#    pass
    

# track isolation distributions
for workdir in workdirs_signal:
    histfile=ROOT.TFile.Open(workdir+"/histograms.root")
    for analysisDir in [eAnalysis,muAnalysis]:
        isolationTree=histfile.Get(analysisDir+"/dileptons_signal_anyTrigger/trackerIsolationL")
        if isolationTree:
            canv=ROOT.TCanvas()
            canv.SetLogy()
            isolationTree.Draw("value","passesAllOtherCuts && value<100","h")
            hist=0
            for item in canv.GetListOfPrimitives():
                if item.IsA().InheritsFrom("TH1"): hist=item
                pass
            if hist:
                hist.GetXaxis().SetTitle("#Sigma p_{t} [GeV/c]")
                title="track #Sigma p_{t} within a #Delta R < 0.3 cone, "+workdir.split("/")[-1]
                title=title[:title.find("_analysis")]
                if analysisDir==eAnalysis:
                    title+=", electron channel"
                else:
                    title+=", muon channel"
                    pass
                hist.SetTitle(title)
                pass
            CMSPlotDecoration(analysisDir)
            canv.Update()
            canv.Print(benchmarkfolder+"/isolation_"+analysisDir+"_"+workdir.split("/")[-1]+fformat)
            pass
        pass
    histfile.Close()
    pass
    
# track isolation dependence on number of pile-up events
for workdir in workdirs_signal:
    histfile=ROOT.TFile.Open(workdir+"/histograms.root")
    for analysisDir in [eAnalysis,muAnalysis]:
        isoHist=histfile.Get(analysisDir+"/dileptons/isolation_vs_pileup_signal")
        if not isoHist: continue
        canv=ROOT.TCanvas()
        hist=isoHist.ProfileY()
        hist.SetMarkerStyle(20)
        hist.SetMinimum(0)
        hist.GetXaxis().SetTitle("pile-up vertices")
        title="average isolation #Sigma p_{t} vs pile-up, "
        if analysisDir==eAnalysis:
            title+="electron channel"
        else:
            title+="muon channel"
            pass
        hist.SetTitle(title)
        hist.Draw()
        canv.Update()
        CMSPlotDecoration(analysisDir)
        canv.Print(benchmarkfolder+"/isolationVsPileup_"+analysisDir+"_"+workdir.split("/")[-1]+fformat)
        pass
    histfile.Close()
    pass

#############################################
### PHOTON TRIGGER EFFICIENCY MEASUREMENT
#############################################

#triggerEfficiency(eTriggerInMuSampleCombination1,"/eTrackAnalysis")

#############################################
### RESOLUTION+BIAS PLOTS FROM MC
#############################################

# currently not running muAnalysis!
sys.exit(0)

# muon momentum bias
for workdir in workdirs_benchmark_mu:
    histfile=ROOT.TFile.Open(workdir+"/histograms.root")
    # note these plots are not available in the mutrack histograms
    pt_vs_radius_standalone=histfile.Get("muAnalysis/leptons/pt_vs_radius_standalone")
    pt_vs_radius_matched=histfile.Get("muAnalysis/leptons/pt_vs_radius_allothers")
    canv=ROOT.TCanvas()
    pt_vs_radius_standalone.SetMarkerColor(ROOT.kBlue)
    if workdir.find("stdRECO")>0:
        pt_vs_radius_standalone.SetTitle("reconstructed p_t vs impact parameter, standard RECO")
    else:
        pt_vs_radius_standalone.SetTitle("reconstructed p_t vs impact parameter, no IP constraint")
        pass
    pt_vs_radius_standalone.GetXaxis().SetTitle("d_{xy} [cm]")
    pt_vs_radius_standalone.GetYaxis().SetTitle("p_{t} [GeV/c]")
    pt_vs_radius_standalone.Draw()
    line=ROOT.TLine(0,50,100,50)
    line.SetLineWidth(3)
    line.Draw("same")
    pt_vs_radius_matched.SetMarkerColor(ROOT.kRed)
    pt_vs_radius_matched.Draw("same")
    CMSPlotDecoration(muAnalysis)
    canv.Update()
    canv.Print(benchmarkfolder+"/muon_momentum_vs_radius_"+workdir.split("/")[-1]+fformat)
    canv.Close()
    pass
