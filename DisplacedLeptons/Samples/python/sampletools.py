import os,sys,time
import subprocess
import ROOT
from gridsites import *


class AnalysisSample:

    ############################################################
    # INITIALISATION: read and check sample description cff file
    ############################################################
    def __init__(self, cff_name):

        # first of all, it might be that the argument is *not* a cff file,
        # but an existing working directory. in that case, proceed to
        # monitor existing jobs
        if os.path.isdir(cff_name):
            job_watcher(cff_name)
            sys.exit(0)

        # check that the file exists
        if not os.path.isfile(cff_name):
            print "error: file", cff_name, "not found"
            sys.exit(1)
        # the following is equivalent to os.path.abspath on most systems, but not at RAL...
        self.cff = os.path.normpath(os.path.join(os.getenv("PWD", ""), cff_name))
        # more RAL specialty...
        self.cff = self.cff.replace("/net/unixfsrv", "/home")

        # find out where we are logged on
        self.where_am_i = where_am_i()

        # check that CMSSW area is set up
        self.cmssw_base = os.getenv("CMSSW_BASE", "NONE")
        # RAL specialty...
        self.cmssw_base = self.cmssw_base.replace("/net/unixfsrv", "/home")
        if self.cmssw_base == "NONE":
            print "error: need to run cmsenv beforehand"
            sys.exit(1)

        # check that the cff file is actually in the CMSSW area
        if self.cff.find(self.cmssw_base) != 0:
            print "error: cff file is not in the release area currently set up"
            print self.cff
            print self.cmssw_base
            sys.exit(1)

        # initialise variables to be read from sample cff file
        sampleDataSet = ""
        sampleJSON = ""
        sampleRunRange = []
        sampleSimFiles = []
        sampleRecoFiles = []
        samplePatFiles = []
        sampleGeneratorConfig = ""
        sampleGeneratorReference = ""
        sampleCMSEnergy = 0
        sampleGlobalTag = ""
        sampleHLTProcess = ""
        sampleRelease = ""
        sampleNumEvents = 0
        sampleLumiNumberOffset = 0
        sampleType = ""
        sampleSignalPID = 0
        sampleRequireCollision = 1
        sampleRunE = 1
        sampleRunMu = 1

        # read and interpret the file
        samplefile = open(self.cff, "r")
        content = ""
        for line in samplefile.readlines():
            content += line
        samplefile.close()
        code = compile(content, "<string>", "exec")
        exec(code)

        # check that the mandatory information is there
        if sampleGlobalTag == "":
            print "error: sampleGlobalTag not set in", self.cff
            sys.exit(1)
        if sampleHLTProcess == "":
            print "error: sampleHLTProcess not set in", self.cff
            sys.exit(1)
        if sampleRelease == "":
            print "error: sampleRelease not set in", self.cff
            sys.exit(1)
        if sampleNumEvents == 0:
            print "error: sampleNumEvents not set in", self.cff
            sys.exit(1)
        if sampleType != "MC" and sampleType != "DATA":
            print "error: sampleType must be set to MC or DATA in", self.cff

        # store cff information in class members
        self.sampleDataSet = sampleDataSet
        self.sampleJSON = sampleJSON
        self.sampleRunRange = sampleRunRange
        self.sampleSimFiles = sampleSimFiles
        self.sampleRecoFiles = sampleRecoFiles
        self.samplePatFiles = samplePatFiles
        self.sampleGeneratorConfig = sampleGeneratorConfig
        self.sampleGeneratorReference = sampleGeneratorReference
        self.sampleCMSEnergy = sampleCMSEnergy
        self.sampleGlobalTag = sampleGlobalTag
        self.sampleRelease = sampleRelease
        self.sampleNumEvents = sampleNumEvents
        self.sampleLumiNumberOffset = sampleLumiNumberOffset
        self.sampleType = sampleType
        self.sampleSignalPID = sampleSignalPID
        self.sampleRequireCollision = sampleRequireCollision
        self.sampleRunE = sampleRunE
        self.sampleRunMu = sampleRunMu

        # create a unique sample ID and get the name of the CMSSW package
        self.id = self.cff.split("/")[-1].replace("_cff.py", "")
        levels = self.cff.replace(self.cmssw_base, "").strip("/").split("/")
        self.packageName = levels[1] + "/" + levels[2]
        self.packageNamePython = self.packageName.replace("/", ".")

        # check directories for sim, reco, pat files.
        self.sampleSimFileDir = self.get_directory(self.sampleSimFiles)
        self.sampleRecoFileDir = self.get_directory(self.sampleRecoFiles)
        self.samplePatFileDir = self.get_directory(self.samplePatFiles)

        # enforce a clean directory structure: all files from one sample
        # must be in the same directory or at most one directory level below
        refdir = ""
        for entry in [self.sampleSimFileDir, self.sampleRecoFileDir,\
                      self.samplePatFileDir]:
            if len(entry) == 0:
                continue
            sharedpath = entry[:entry.rfind("/")]
            if refdir == "":
                refdir = sharedpath
            if refdir != sharedpath:
                # print "inconsistent directory structure:", refdir, sharedpath
                if self.cff.find("Debug") < 0:
                    sys.exit(1)

        # general initialisation
        self.workdir = ""
        self.driverconf = ""

    ##################################
    # CHECK DIRECTORY OF FILES IN LIST
    ##################################
    def get_directory(self, filelist):
        dirname = ""
        for entry in filelist:
            newdir = entry[:entry.rfind("/")]
            if newdir != dirname and dirname != "":
                print "error: multiple directories in file list"
                sys.exit(1)
            dirname = newdir
        return dirname

    #########################################
    # GET LIST OF EXISTING FILES IN DIRECTORY
    #########################################
    def get_dir_content(self, filelist):
        dirname = self.get_directory(filelist)
        existing_files = []
        if dirname.find("/castor/") >= 0:
            # this is a castor directory
            if self.where_am_i == "CERN":
                # storage on castor requested. check output dir
                topdir = dirname[:dirname.rfind("/")]
                lastlevel = dirname[dirname.rfind("/") + 1:]
                found = 0
                for entry in os.popen("rfdir " + topdir).readlines():
                    if entry.split()[-1] == lastlevel:
                        found = 1
                if found:
                    # directory exists. check for existing files
                    for entry in os.popen("rfdir " + dirname).readlines():
                        existing_files.append(entry.split()[-1])
                    os.system("rfchmod 775 " + dirname)
            else:
                print "error: cannot check castor dir content from outside CERN"
                sys.exit(1)
        elif dirname.find("rl.ac.uk/") > 0:
            # RAL dCache directory requested
            if self.where_am_i == "RAL":
                ensure_grid_proxy()
                interactive_path = dirname.replace("dcap:", "").replace("srm:", "")
                interactive_path = interactive_path.replace("//heplnx204.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace("//heplnx209.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace("//dcap.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace(":8443", "")
                interactive_path = interactive_path.replace("/cms/user/", "/cms/store/user/")
                if os.path.isdir(interactive_path):
                    # directory exists. check for existing files
                    for entry in os.listdir(interactive_path):
                        existing_files.append(dirname + "/" + entry)
            else:
                print "error: cannot check RAL dCache dir content from outside RAL"
                sys.exit(1)
        else:
            # check on local disk (well, or AFS)
            actual_dir = dirname.replace("file:", "")
            if os.path.isdir(actual_dir):
                # directory exists. check for existing files
                for entry in os.listdir(actual_dir):
                    existing_files.append(dirname + "/" + entry)
        return existing_files

    ###################################################################
    # CHECK OUTPUT DIRECTORY FOR EXISTING FILES AND CREATE IF NECESSARY
    ###################################################################
    def check_dir(self, filelist, inout, allow_partial = 0):
        inout = inout.lower()
        if inout != "input" and inout != "output":
            print "error: check_dir argument needs to be \"input\" or \"output\""
            sys.exit(1)
        dirname = self.get_directory(filelist)
        existing = []
        filenames = []
        for entry in filelist:
            filenames.append(entry.split("/")[-1])
        if dirname.find("/castor/") >= 0:
            # this is a castor directory
            dirlocation = "CERN"
            if self.where_am_i == "CERN":
                # storage on castor requested. check output dir
                topdir = dirname[:dirname.rfind("/")]
                lastlevel = dirname[dirname.rfind("/") + 1:]
                found = 0
                for entry in os.popen("rfdir " + topdir).readlines():
                    if entry.split()[-1] == lastlevel: found = 1
                if found:
                    # directory exists. check for existing files
                    for entry in os.popen("rfdir " + dirname).readlines():
                        if entry.split()[-1] in filenames: existing.append(dirname + "/" + entry.split()[-1])
                    os.system("rfchmod 775 " + dirname)
                elif inout == "output":
                    os.system("rfmkdir " + dirname + " &> /dev/null")
                    os.system("rfchmod 775 " + dirname)
            elif self.run_on == "GRID":
                print "warning: cannot check castor output directory from this site"
            else:
                print "error: cannot run non-GRID jobs outside CERN to access castor"
                sys.exit(1)
        elif dirname.find("rl.ac.uk/") > 0:
            # storage on RAL dCache requested
            dirlocation = "RAL"
            if self.where_am_i == "RAL":
                interactive_path = dirname.replace("dcap:", "").replace("srm:", "")
                interactive_path = interactive_path.replace("//heplnx204.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace("//heplnx209.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace("//dcap.pp.rl.ac.uk", "")
                interactive_path = interactive_path.replace(":8443", "")
                interactive_path = interactive_path.replace("/cms/user/", "/cms/store/user/")
                if os.path.isdir(interactive_path):
                    # directory exists. check for existing files
                    for entry in os.listdir(interactive_path):
                        if entry in filenames:
                            existing.append(dirname + "/" + entry)
                else:
                    # no need to do anything. directory will be created automatically by dCache
                    pass
            elif self.run_on == "GRID":
                # print "warning: cannot check RAL dCache output dir from this site"
				pass
            else:
                # no need to do anything. directory will be created automatically by dCache
                pass
            pass
        elif dirname.find("rcac.purdue.edu")>0:
            dirlocation="FNAL"
            interactive_path=dirname.replace("root://xrootd.rcac.purdue.edu", "srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN=")
            addToList = True
            srmOffset = 0
            while addToList:
                result = subprocess.Popen(['srmls', "-2 -offset "+str(srmOffset)+" \""+interactive_path+"\""], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
                # result = subprocess.check_output("srmls -2 -offset "+str(srmOffset)+" \""+interactive_path+"\"", stderr=subprocess.STDOUT, shell=True)
                # result, stdin = os.popen("srmls -2 -offset "+str(srmOffset)+" \""+interactive_path+"\"").readlines()
                # print "srmls -2 \""+interactive_path+"\""
                # print "result:"
                srmTooManyFiles = False
                # for line in result:
                for line in result.splitlines():
                    # print "LINE = "+line
                    if line.find("SRM_TOO_MANY_RESULTS") > 0:
                        srmTooManyFiles = True
                        # print "TOO MANY FILES!"
                    # print line.split("//")
                    if len(line.split("//")) > 1:
                        entry = line.split("/")[-1].rstrip("\n")
                        print "entry = "+entry
                        if entry in filenames:
                            print "file "+entry+" exists"
                            existing.append(dirname+"/"+entry)
                if srmTooManyFiles:
                    "ADDING TO THE LIST AN OFFSET OF 1000"
                    srmOffset = srmOffset + 1000
                else:
                    "ALL FILES LISTED"
                    addToList = False
        else:
            # store on local disk (well, or AFS)
            dirlocation = "LOCAL"
            actual_dir = dirname.replace("file:", "")
            if os.path.isdir(actual_dir):
                # directory exists. check for existing files
                for entry in os.listdir(actual_dir):
                    if entry in filenames:
                        existing.append(dirname + "/" + entry)
            elif inout == "output":
                os.system("mkdir -p " + actual_dir)

        # interpret result
        if inout == "input":
            self.read_from = dirlocation
            if len(existing) != len(filelist):
                if (allow_partial and len(existing) > 0) or self.cff.find("Debug") >= 0:
                    print "warning", len(filelist) - len(existing), "missing input files in", dirname
                else:
                    print "error:", len(filelist) - len(existing), "missing input files in", dirname
                    sys.exit(1)
        else:
            self.store_at = dirlocation
            if len(existing) > 0:
                print "error:", len(existing), "output files already exist in", dirname
                sys.exit(1)
        return existing

    ##################################
    # MAKE SURE RUN NUMBERS ARE UNIQUE
    ##################################
    def check_run_number(self):
        cffdir = self.cff[:self.cff.rfind("/")]
        for filename in os.listdir(cffdir):
            if filename[-7:] != "_cff.py":
                continue
            sampleLumiNumberOffset = 0
            sampleSimFiles = []
            samplefile = open(cffdir + "/" + filename, "r")
            content = ""
            for line in samplefile.readlines():
                content += line
            samplefile.close()
            code = compile(content, "<string>", "exec")
            exec(code)
            file_lumimin = sampleLumiNumberOffset
            file_luminums = len(sampleSimFiles)  # crab assigns one run number per file
            # special case: different reco variants of sample sample should have same run numbers
            if filename.replace("_std", "").replace("_mod", "").replace("_re", "")\
                   == self.cff.split("/")[-1].replace("_std", "").replace("_mod", "").replace("_re", ""):
                if file_lumimin != self.sampleLumiNumberOffset:
                    print "error: expected same run section offset in", filename
                    sys.exit(1)
            # general case: run numbers should not overlap
            elif abs(file_lumimin - self.sampleLumiNumberOffset)\
                   < max(file_luminums, len(self.sampleSimFiles)):
                print "potential lumi section number conflict with", filename
                sys.exit(1)

    ############################
    # CREATE A WORKING DIRECTORY
    ############################
    def create_work_dir(self, process):
        if self.workdir != "":
            print "error: working directory already created"
            return
        workbasedir = self.cmssw_base + "/src/workdirs/"
        if not os.path.exists(workbasedir):
            os.system("mkdir -p " + workbasedir)
        self.workdir = workbasedir + self.id + "_" + process\
                       + time.strftime("_%Y%m%d")
        if os.path.exists(self.workdir):
            num = 0
            while os.path.exists(self.workdir + "_" + str(num)):
                num += 1
            self.workdir += "_" + str(num)
        os.system("mkdir -p " + self.workdir)
        os.system("cp -p " + self.cff + " " + self.workdir)
        print "working directory:", self.workdir

    ############################
    # CREATE A WORKING DIRECTORY
    ############################
    def create_work_dir_temp(self, process, tempDir):
        if self.workdir != "":
            print "error: working directory already created"
            return
        workbasedir = tempDir
        if not os.path.exists(workbasedir):
            os.system("mkdir -p " + workbasedir)
        self.workdir = workbasedir + self.id + "_" + process\
                       + time.strftime("_%Y%m%d")
        if os.path.exists(self.workdir):
            num = 0
            while os.path.exists(self.workdir + "_" + str(num)):
                num += 1
            self.workdir += "_" + str(num)
        os.system("mkdir -p " + self.workdir)
        os.system("cp -p " + self.cff + " " + self.workdir)
        print "working directory:", self.workdir


    ##################
    # LAUNCH CMSDRIVER
    ##################
    def run_cmsDriver(self, configfile, steps, tier, eventcontent):

        # first make sure we have a kerberos ticket (needed for access to CVS)
        if not have_kerberos_ticket():
            print "error: no valid kerberos ticket found. run kinit first."
            sys.exit(1)

        # create a dummy Configuration/Generator package because this is where cmsDriver expects
        # to find the configuration
        configdir = self.cmssw_base + "/src/Configuration/Generator/python"
        if os.path.exists(configdir):
            os.system("mv " + configdir + " " + configdir + ".bak")
            os.system("mkdir -p " + configdir)
        else:
            os.system("mkdir -p " + configdir)
        os.system("cp " + os.getenv("CMSSW_RELEASE_BASE")
                  + "/src/Configuration/Generator/python/PythiaUESettings_cfi.py " + configdir)
        os.system("cp " + configfile + " " + self.cmssw_base + "/src/Configuration/Generator/python/")

        # make sure we have a working directory ready
        if self.workdir == "":
            print "error: must create working directory before calling run_cmsDriver"
            sys.exit(1)

        # run cmsDriver for this sample
        os.system("cd " + self.cmssw_base + "; scram b > /dev/null")
        print "Running: cmsDriver.py " + configfile.split("/")[-1] +\
                  " --step=" + steps +\
                  " --conditions=" + self.sampleGlobalTag + " --datatier " + tier +\
                  " --eventcontent=" + eventcontent +\
                  " --number=" + str(self.sampleNumEvents) + " --no_exec" # ).readlines()
        result = os.popen("cd " + self.workdir + "; cmsDriver.py " + configfile.split("/")[-1] +\
                          " --step=" + steps +\
                          " --conditions=" + self.sampleGlobalTag + " --datatier " + tier +\
                          " --eventcontent=" + eventcontent +\
                          " --number=" + str(self.sampleNumEvents) + " --no_exec").readlines()

        # remove the dummy Configuration/Generator package
        if os.path.exists(configdir+".bak"):
            os.system("rm -rf "+configdir)
            os.system("mv "+configdir+".bak "+configdir)
        else:
            os.system("rm -rf "+configdir)
        if os.listdir(self.cmssw_base+"/src/Configuration/Generator")==['CVS']:
            os.system("rm -rf "+self.cmssw_base+"/src/Configuration/Generator")
        if os.listdir(self.cmssw_base+"/src/Configuration")==['CVS']:
            os.system("rm -rf "+self.cmssw_base+"/src/Configuration")

        # check whether cmsDriver succeeded
        self.driverconf=""
        for line in result:
            if line.find("Config file")==0 and line.find("created")>0:
                fields=line.split()
                for entry in fields:
                    if entry.find(".py")>0:
                        self.driverconf=self.workdir+"/"+entry
        if not os.path.isfile(self.driverconf):
            print "cmsDriver seems to have failed. output follows:"
            for line in result:
                print line,
            sys.exit(1)


    #########################
    # CREATE CRAB CONFIG FILE
    #########################
    def run_crab(self,outputfiles,events_per_job):
        if self.workdir=="":
            print "error: need to create working dir before creating crab.cfg"
            sys.exit(1)
        if len(outputfiles)==0:
            print "error: no output files given for crab.cfg"
            sys.exit(1)
        if self.driverconf=="":
            print "error: need to run cmsDriver first"
            sys.exit(1)
        submit_sites=[]
        if self.sampleDataSet!="":
            # check which sites the sample is stored at
            sitelist_favoured=[]
            sitelist_neutral=[]
            sitelist_all=[]
            for line in os.popen("dbs search --query=\"find site where dataset="\
                                 +self.sampleDataSet+"\""):
                if line.find(".")<0: continue
                if line.find("Using DBS")>=0: continue
                if line.find("Error")>=0: continue
                newsite=line.strip("\n")
                good=0
                bad=0
                for entry in gridsites_good:
                    if newsite.find(entry)>=0: good=1
                for entry in gridsites_bad:
                    if newsite.find(entry)>=0: bad=1
                if good:
                    sitelist_favoured.append(newsite)
                elif not bad:
                    sitelist_neutral.append(newsite)
                sitelist_all.append(newsite)
            submit_sites=sitelist_favoured
            submit_sites+=sitelist_neutral
            #if len(submit_sites)==0: submit_sites=sitelist_neutral
            if len(submit_sites)==0: submit_sites=sitelist_all
            if len(submit_sites)==0:
                print "error: no valid GRID sites found for this sample"
                sys.exit(1)
            print "available GRID sites:",sitelist_all
            print "submission whitelist:",submit_sites
        # create crab file
        crabfile=open(self.workdir+"/crab.cfg","w")
        crabfile.write("[CMSSW]\n")
        crabfile.write("get_edm_output=1\n")
        crabfile.write("pset="+self.driverconf.split("/")[-1]+"\n")
        numjobs=int(self.sampleNumEvents/events_per_job)
        if numjobs==0: numjobs=1
        if self.sampleDataSet!="":
            crabfile.write("datasetpath="+self.sampleDataSet+"\n")
        else:
            crabfile.write("datasetpath=None\n")
        if self.sampleJSON!="":
            crabfile.write("number_of_jobs="+str(numjobs)+"\n")
            crabfile.write("lumi_mask=json.txt\n")
            crabfile.write("total_number_of_lumis = -1\n")
        elif self.sampleDataSet=="":
            crabfile.write("number_of_jobs="+str(numjobs)+"\n")
            crabfile.write("total_number_of_events = %i\n"%self.sampleNumEvents)
        elif self.sampleType=="DATA":
            crabfile.write("total_number_of_lumis=-1\n")
            crabfile.write("lumis_per_job=10\n")
        else:
            crabfile.write("number_of_jobs="+str(numjobs)+"\n")
            crabfile.write("total_number_of_events = -1\n")
        if self.sampleType!="DATA":
            crabfile.write("increment_seeds=generator,g4SimHits\n")
            crabfile.write("first_lumi="+str(self.sampleLumiNumberOffset)+"\n")
        if len(self.sampleRunRange)==2:
            crabfile.write("runselection=%i-%i\n"%(self.sampleRunRange[0],self.sampleRunRange[1]))
        crabfile.write("[USER]\n")
        crabdir="workdir_"+self.workdir.split("/")[-1]
        crabfile.write("ui_working_dir="+crabdir+"\n")
        crabfile.write("return_data=0\n")
        crabfile.write("copy_data=1\n")
        if outputfiles[0].find("/castor/")>=0:
            # stageout to CERN castor
            castordir=outputfiles[0][:outputfiles[0].rfind("/")]
            castordir=castordir.replace("rfio:","")
            castordir=castordir.replace("///","/")
            castordir=castordir.replace("/castor/cern.ch","")
            crabfile.write("storage_element = srm-cms.cern.ch\n")
            crabfile.write("storage_path = /srm/managerv2?SFN=/castor/cern.ch/\n")
            crabfile.write("user_remote_dir = "+castordir+"\n")
            crabfile.write("check_user_remote_dir = 0\n")
        # elif outputfiles[0].find("pp.rl.ac.uk")>0:
        #     # stageout to RAL dCache
        #     dcachedir=outputfiles[0][:outputfiles[0].rfind("/")]
        #     dcachedir=dcachedir.replace("dcap://heplnx209.pp.rl.ac.uk","")
        #     dcachedir=dcachedir.replace("dcap://dcap.pp.rl.ac.uk","")
        #     dcachedir=dcachedir.replace("srm://heplnx204.pp.rl.ac.uk","")
        #     dcachedir=dcachedir.replace(":8443","")
        #     dcachedir=dcachedir.replace("/cms/store/user/","/cms/user/")
        #     dcachedir=dcachedir.replace("/pnfs/pp.rl.ac.uk/data/cms/user/harder","")
        #     # crabfile.write("storage_element = T2_UK_SGrid_RALPP\n")
        #     crabfile.write("storage_element = T2_UK_SGrid_RALPP\n")
        #     crabfile.write("user_remote_dir = "+dcachedir+"\n")
        elif outputfiles[0].find("pp.rl.ac.uk")>0:
            # stageout to FNAL dCache
            dcachedir=outputfiles[0][:outputfiles[0].rfind("/")]
            dcachedir=dcachedir.replace("dcap://heplnx209.pp.rl.ac.uk","")
            dcachedir=dcachedir.replace("dcap://dcap.pp.rl.ac.uk","")
            dcachedir=dcachedir.replace("srm://heplnx204.pp.rl.ac.uk","")
            dcachedir=dcachedir.replace(":8443","")
            dcachedir=dcachedir.replace("/cms/store/user/","/cms/user/")
            dcachedir=dcachedir.replace("/pnfs/pp.rl.ac.uk/data/cms/user/harder","")
            crabfile.write("storage_element = T2_US_Purdue\n")
            # print "sampleDataSet ="+self.sampleDataSet
            publishName=(self.sampleDataSet[:self.sampleDataSet.rfind("/")]).replace("/", "_")
            # print "publishName = "+publishName
            if publishName.startswith("_"):
                publishName = publishName[1:]
                # print "Reduced publishName = "+publishName
            if dcachedir.endswith("pat"):
                publishName = publishName+"_PAT_v1"
            crabfile.write("publish_data_name = "+publishName+"\n")
            crabfile.write("user_remote_dir = "+dcachedir+"\n")
            crabfile.write("dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet\n")
        else:
            # oops?
            print "error: unsupported destination for output files of crab job"
            sys.exit(1)
        # crabfile.write("eMail = Kristian.Harder@stfc.ac.uk\n")
        crabfile.write("eMail = marco.de.mattia@cern.ch\n")
        crabfile.write("thresholdLevel = 50\n")
        crabfile.write("publish_data=0\n")
        crabfile.write("[CRAB]\n")
        crabfile.write("cfg=crab.cfg\n")
        crabfile.write("jobtype=cmssw\n")
        crabfile.write("use_server = 1\n")
        crabfile.write("scheduler = glidein\n")
        if len(submit_sites)>0:
            crabfile.write("[GRID]\n")
            crabfile.write("se_white_list = "+submit_sites[0])
            for i in range(1,len(submit_sites)):
                crabfile.write(","+submit_sites[i])
            crabfile.write("\n")
        else:
            # this is probably a generator job without input. restrict that to RAL
            # crabfile.write("[GRID]\n")
            # crabfile.write("ce_white_list = T2_UK_SGrid_RALPP\n")
            pass
        crabfile.close()


        # get data quality definition if applicable
        if self.sampleJSON!="":
            os.system("cd "+self.workdir+"; wget --no-check-certificate -O json.txt "+self.sampleJSON)

        # create and submit the jobs
        print "creating crab jobs..."
        os.system("cd "+self.workdir+" ; crab -create -cfg crab.cfg")
        # os.system("cd "+self.workdir+"; source ~/bin/setup_crab ; crab -create -cfg crab.cfg")
        print "submitting jobs..."
        os.system("cd "+self.workdir+"; crab -submit -c "+crabdir)
        # os.system("cd "+self.workdir+"; source ~/bin/setup_crab ; crab -submit -c "+crabdir)
        print "crab submission done!"


    #################
    # COPY GRID PROXY
    #################
    def get_grid_proxy(self):
        # find file name of grid proxy file
        result=os.popen("grid-proxy-info").readlines()
        proxyfile=""
        for line in result:
            if line.find("path")==0:
                proxyfile=line.split(":")[1].strip("\n").strip()
        if not os.path.exists(proxyfile):
            print "error: could not find GRID proxy file"
            sys.exit(1)
        os.system("cp -p "+proxyfile+" "+self.workdir)
        self.proxyfile=self.workdir+"/"+proxyfile.split("/")[-1]


    ######################
    # CREATE BATCH SCRIPTS
    ######################
    def run_batch_jobs(self,inputfiles,outputfiles,runmode):

        # make sure we are not trying to apply DQM in batch jobs. this is not implemented yet.
        if self.sampleJSON!="" and len(outputfiles)>0:
            print "error: cannot use JSON file in batch jobs"
            sys.exit(1)

        # we need a grid proxy whenever we are either running on the grid or try to write
        # something to RAL tier2
        need_grid_proxy=0
        if runmode=="GRID": need_grid_proxy=1
        for entry in inputfiles+outputfiles:
            if entry.find("dcap:")>=0 or entry.find("srm:")>=0:
                need_grid_proxy=1
        if need_grid_proxy:
            ensure_grid_proxy()
            self.get_grid_proxy()

        # calculate number of input files per job
        numjobs=len(outputfiles)
        has_output=1
        if numjobs==0:
            # this is expected when running the final analysis jobs.
            # those have no real edm output files, just histogram files.
            # random choice for number of jobs therefore, judging from
            # expected CPU time etc, but limit to at most 250 jobs
            numjobs=min(250,(len(inputfiles)/3)+1)
            has_output=0
        numfilesperjob=len(inputfiles)/numjobs
        if len(inputfiles)%numjobs>0:
            numfilesperjob+=1
            # by processing a file more per job we might actually need fewer jobs
            while numfilesperjob*(numjobs-1)>=len(inputfiles): numjobs-=1
        if numjobs<len(outputfiles):
            print "error: only",numjobs,"output files would be produced instead of",\
                  len(outputfiles),"requested ones. please shorten output file list."
            sys.exit(1)

        # read original config file
        origconfigfile=open(self.driverconf,"r")
        origconfig=origconfigfile.readlines()
        origconfigfile.close()

        # try to determine name of PoolOutputModule (not very intelligent search yet...)
        outputmodule="out"
        has_prefilter=0
        for line in origconfig:
            if line.find("process.RECOSIMoutput")>=0: outputmodule="RECOSIMoutput"
            if line.find("process.output")>=0: outputmodule="output"
            if line.find("prefilter=1")>=0:
                has_prefilter=1

        # create one script per output file
        for i in range(numjobs):
            configfileName = self.workdir+"/job"+str(i+1)+"_cfg.py"
            configfile=open(configfileName,"w")
            for line in origconfig: configfile.write(line)
            if runmode=="RAL":
                tmp_dir="/scratch"
            else:
                tmp_dir="/tmp"
            tmp_dir+="/"+self.workdir.replace("/","_")
            if runmode=="FNAL":
                os.system("mkdir -p "+tmp_dir)
            configfile.write("process.source.fileNames = [\n")
            for k in range(i*numfilesperjob,min((i+1)*numfilesperjob,len(inputfiles))):
                configfile.write("  \""+inputfiles[k]+"\",\n")
            configfile.write("]\n")
            if has_output:
                # specify edm file name
                outputfilename=outputfiles[i].split("/")[-1]
                configfile.write("process."+outputmodule+".fileName = \""+tmp_dir+"/"\
                                 +outputfilename+"\"\n")
                if has_prefilter:
                    prefilterfile=outputfilename.replace(".root","_prefilter.root")
                    configfile.write("process.TFileService.fileName = \""+tmp_dir+"/"+prefilterfile+"\"\n")
            else:
                # specify histogram file name
                outputfilename="histograms_"+str(i+1)+".root"
                configfile.write("process.TFileService.fileName=\""\
                                 +tmp_dir+"/"+outputfilename+"\"\n")
            configfile.close()
            jobscriptName = self.workdir+"/job"+str(i+1)+".sh"
            jobscript=open(jobscriptName,"w")
            jobscript.write("#!/bin/bash\n")
            if runmode=="FNAL":
                if not os.path.isfile("/uscms/home/demattia/x509up_u45843"):
                    print "Error: missing grid certificate. Before you submit the job you should do voms-proxy-init;"
                    print "cp /tmp/x509_u##### $HOME where /tmp/x509_u#### is the name of your proxy file from vomx-proxy-info."
                    return
                jobscript.write("export X509_USER_PROXY=/uscms/home/demattia/x509up_u45843\n")
            jobscript.write("mkdir -p "+tmp_dir+"\n")
            jobscript.write("cd "+self.cmssw_base+"/src\n")
            jobscript.write("eval `scramv1 runtime -sh`\n")
            jobscript.write("cmsRun "+self.workdir+"/job"+str(i+1)+"_cfg.py\n")
            jobscript.write("cp "+tmp_dir+"/histograms_"+str(i+1)+".root "+self.workdir+"\n")
            if runmode=="CERN" and has_output:
                jobscript.write("rfcp "+tmp_dir+"/"+outputfilename+" "\
                                +outputfiles[i].replace("rfio:","").replace("///","/")+"\n")
            elif runmode=="RAL" and has_output:
                jobscript.write("cp -p "+self.proxyfile+" /tmp\n")
                if has_prefilter:
                    jobscript.write("lcg-cp "+tmp_dir+"/"+prefilterfile+" "\
                                    +srm_path(outputfiles[i].replace(outputfilename,prefilterfile))+"\n")
                jobscript.write("lcg-cp "+tmp_dir+"/"+outputfilename+" "\
                                +srm_path(outputfiles[i])+"\n")
            elif runmode=="FNAL" and has_output:
                srmOutput = srm_path(outputfiles[i]).replace("root://xrootd.rcac.purdue.edu", "srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN=")
                srmOutputPath = srmOutput.split(srmOutput.split("/")[-1])[0]
                # jobscript.write("source /uscmst1/prod/grid/gLite_SL5.sh\n")
                # jobscript.write("source /uscmst1/prod/grid/CRAB/crab.sh\n")
                # Do it only for the first file
                if srmOutput.split("_")[-1].split(".root")[0] == "1":
                    os.system("srmmkdir -2 "+srmOutputPath)
                if has_prefilter:
                    jobscript.write("/opt/d-cache/srm/bin/srmcp -2 \"file:///"+tmp_dir+"/"+prefilterfile+"\" \""+srmOutput.replace(outputfilename,prefilterfile)+"\"\n")
                jobscript.write("/opt/d-cache/srm/bin/srmcp -2 \"file:///"+tmp_dir+"/"+outputfilename+"\" \""+srmOutput+"\"\n")
            elif has_output:
                print "error: no idea how to run jobs at",runmode
                sys.exit(1)
            if has_output:
                jobscript.write("rm "+tmp_dir+"/"+outputfilename+"\n")
            jobscript.close()
            os.system("chmod u+x "+self.workdir+"/job"+str(i+1)+".sh")
            if runmode=="CERN":
                batchcommand="cd "+self.workdir+"; bsub -q 1nd job"+str(i+1)+".sh"
            elif runmode=="FNAL":
                condorScriptName=self.workdir+"/runOnCondor_"+str(i+1)
                jobScriptFileName = jobscriptName.split("/")[-1]
                cfgFileName = configfileName.split("/")[-1]
                condorScriptFile = open(condorScriptName, "w")
                condorScriptFile.write("universe = vanilla\n")
                condorScriptFile.write("Executable = "+jobScriptFileName+"\n")
                condorScriptFile.write("Requirements = Memory >= 199 &&OpSys == \"LINUX\"&& (Arch != \"DUMMY\" )&& Disk > 1000000\n")
                condorScriptFile.write("Should_Transfer_Files = YES\n")
                condorScriptFile.write("Transfer_Input_Files = "+jobScriptFileName+", "+cfgFileName+"\n")
                condorScriptFile.write("WhenToTransferOutput = ON_EXIT\n")
                # condorScriptFile.write("Output = condor_"+cfgFileName+"_$(Cluster)_$(Process).stdout\n")
                # condorScriptFile.write("Error = condor_"+cfgFileName+"_$(Cluster)_$(Process).stderr\n")
                condorScriptFile.write("Log = condor_"+cfgFileName+"_$(Cluster)_$(Process).log\n")
                #condorScriptFile.write("notify_user = demattia@FNAL.GOV\n")
                condorScriptFile.write("Queue 1\n")
                condorScriptFile.close()
                batchcommand="cd "+self.workdir+"; condor_submit "+condorScriptName
            else:
                batchcommand="cd "+self.workdir+"; qsub -q prod -l walltime=48:00:00 -M Kristian.Harder@stfc.ac.uk -m a job"+str(i+1)+".sh"
            result=os.popen(batchcommand).readlines()
            joblist=open(self.workdir+"/joblist","a")
            for line in result:
                joblist.write(line)
                print line,
            joblist.close()



##################################
# CHECK DIRECTORY OF FILES IN LIST
##################################
def get_directory(filelist):
    dirname=""
    for entry in filelist:
        newdir=entry[:entry.rfind("/")]
        if newdir!=dirname and dirname!="":
            print "error: multiple directories in file list"
            sys.exit(1)
            pass
        dirname=newdir
        pass
    return dirname


#########################################
# GET LIST OF EXISTING FILES IN DIRECTORY
#########################################
def get_dir_content(filelist):
    dirname=get_directory(filelist)
    existing_files=[]
    if dirname.find("rl.ac.uk")>0:
        ensure_grid_proxy()
        interactive_path=dirname.replace("dcap:","").replace("srm:","")
        interactive_path=interactive_path.replace("//heplnx204.pp.rl.ac.uk","")
        interactive_path=interactive_path.replace("//heplnx209.pp.rl.ac.uk","")
        interactive_path=interactive_path.replace("//dcap.pp.rl.ac.uk","")
        interactive_path=interactive_path.replace(":8443","")
        interactive_path=interactive_path.replace("/cms/user/","/cms/store/user/")
        if os.path.isdir(interactive_path):
            # directory exists. check for existing files
            for entry in os.listdir(interactive_path):
                existing_files.append(dirname+"/"+entry)
                pass
            pass
        pass
    else:
        # check on locally mounted file system
        actual_dir=dirname.replace("file:","")
        if os.path.isdir(actual_dir):
            # directory exists. check for existing files
            for entry in os.listdir(actual_dir):
                existing_files.append(dirname+"/"+entry)
                pass
            pass
        pass
    return existing_files


#########################
# DCACHE PATH CONVERSIONS
#########################
def srm_path(dcap_path):
    srm=dcap_path.replace("dcap:","srm:")
    srm=srm.replace("heplnx209.pp.rl.ac.uk","heplnx204.pp.rl.ac.uk")
    srm=srm.replace("dcap.pp.rl.ac.uk","heplnx204.pp.rl.ac.uk")
    srm=srm.replace("/cms/user/","/cms/store/user/")
    return srm


###########################
# CHECK FOR KERBEROS TICKET
###########################
def have_kerberos_ticket():
    result=os.popen("klist -s ; echo $?").readlines()
    valid=0
    for line in result:
        if line.strip("\n").strip()=="0": valid=1
    return valid


######################
# CHECK FOR GRID PROXY
######################
def ensure_grid_proxy():
    # result=os.popen("source ~/bin/setup_crab &> /dev/null ; voms-proxy-info -vo").readlines()
    result=os.popen("voms-proxy-info -vo").readlines()
    valid=0
    for line in result:
        if line.strip("\n").strip().lower()=="cms": valid=1
    if not valid:
        # os.system("source ~/bin/setup_crab &> /dev/null ; voms-proxy-init --voms cms")
        os.system("voms-proxy-init --voms cms")


#########################
# IDENTIFY LOGON LOCATION
#########################
def where_am_i():
    host=os.popen("/bin/hostname").readlines()[0].strip()
    if host.find("heplnx")==0 and host.find("pp.rl.ac.uk")>0:
        return "RAL"
    elif host.find("lxplus")==0 and host.find("cern.ch")>0:
        return "CERN"
    else:
        return "UNKNOWN"


##########################
# CHECK EDM FILE INTEGRITY
##########################
checkedm_retMISSING=-999
checkedm_retCORRUPT=-1
checkedm_retNOEDM=-2
checkedm_retCANNOTCHECK=-100

def read_attempt(filename):
    ROOT.gROOT.Reset()
    try:
        events = ROOT.TFile.Open(filename).Get("Events")
    except:
        numevents=checkedm_retCORRUPT
    try:
        numevents=events.GetEntries()
    except:
        numevents=checkedm_retNOEDM
    return numevents

def check_edm_file(filename,where_am_i):
    # check on castor
    if filename.find("/castor/cern.ch")>=0:
        if where_am_i=="CERN":
            result=os.popen("rfdir "+filename).readlines()
            if len(result)==0: return checkedm_retMISSING
            return read_attempt(filename)
        else:
            return checkedm_retCANNOTCHECK
    # check at RAL
    elif filename.find("pp.rl.ac.uk")>=0:
        if where_am_i=="RAL":
            ensure_grid_proxy()
            result=os.popen("srmls "+srm_path(filename)+" 2>/dev/null").readlines()
            if len(result)==0: return checkedm_retMISSING
            return read_attempt(filename)
        else:
            return checkedm_retCANNOTCHECK
    # check local file
    elif filename.find("file:")>=0:
        if not os.path.isfile(filename.replace("file:","")): return checkedm_retMISSING
        return read_attempt(filename.replace("file:",""))
    else:
        return checkedm_retCANNOTCHECK


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


#####################
# MONITOR SET OF JOBS
#####################
def job_watcher(workdir):
    # important info for the user
    print "beginning to watch jobs. it is safe to kill this script;",\
          "this will not affect the running jobs or their output"

    # check argument
    if os.path.isfile(workdir+"/joblist"):
        job_watcher_batch(workdir)
    elif os.path.isfile(workdir+"/crab.cfg"):
        job_watcher_grid(workdir)
    else:
        print "invalid directory for job_watcher"
        sys.exit(1)


def job_watcher_batch(workdir):
    # check argument
    filename=workdir+"/joblist"
    if not os.path.isfile(filename):
        print "error: invalid working directory",workdir
        sys.exit(1)
    joblist=[]
    joblistfile=open(filename,"r")
    for entry in joblistfile.readlines():
        joblist.append(entry.strip())
    numjobs=len(joblist)

    # check which batch system to use
    if where_am_i()=="CERN":
        lsf=1
    else:
        lsf=0

    # wait for jobs to finish
    nfound=len(joblist)
    print "waiting for batch jobs to be processed...."
    while nfound>0:
        if lsf:
            result=os.popen("bjobs").readlines()
        else:
            result=os.popen("qstat -u $USER").readlines()
        nqueued=0
        nrunning=0
        nfound=0
        for line in result:
            fields=line.split()
            if len(fields)==0: continue
            jobid=fields[0]
            found=0
            for entry in joblist:
                if entry.find(jobid)>=0: found=1
            if found:
                nfound+=1
                if lsf and line.find("RUN")>0:
                    nrunning+=1
                elif (not lsf) and line.find(" R ")>0:
                    nrunning+=1
                else:
                    nqueued+=1
        print nrunning,"running,",nqueued,"pending,",\
              len(joblist)-nfound,"done as of ",time.asctime()
        if nfound>0: time.sleep(60)


    # clean up job output
    if lsf:
        # clean up LSFJOB_* directories (save logfiles!)
        for jobid in joblist:
            lsfdir=workdir+"/LSFJOB_"+jobid
            if not os.path.isfile(lsfdir+"/LSFJOB"): continue
            lsffile=open(lsfdir+"/LSFJOB","r")
            for line in lsffile.readlines():
                if line.find(id)>0:
                    jobnum=line[line.rfind("_")+1:]
                    jobnum=jobnum.replace(".sh'","")
                    jobnum=jobnum.strip()
            lsffile.close()
            if os.path.exists(lsfdir+"/STDOUT"):
                os.system("mv "+lsfdir+"/STDOUT "+workdir+"/"+id+"_"+str(jobnum)+".log")
                os.system("gzip "+workdir+"/"+id+"_"+str(jobnum)+".log")
            os.system("rm -rf "+lsfdir)
    else:
        # for the RAL batch system all we need to do is gzip the log files
        # and check for jobs that were killed due to timeouts caused by slow dCache access
        killed_jobs=[]
        for i in range(numjobs):
            os.system("gzip "+workdir+"/job"+str(i+1)+".sh.* &>/dev/null")
            log=os.popen("gunzip -c `ls -1rt "+workdir+"/job"+str(i+1)+".sh.e*|tail -1`|grep \"job killed\"").readlines()
            killed=0
            for line in log:
                if line.find("job killed")>0: killed=1
            if killed: killed_jobs.append(i+1)
        if len(killed_jobs)>0:
            print "KILLED JOBS:",killed_jobs
            badjobfile=open(workdir+"/KILLED_JOBS","w")
            for jobnum in killed_jobs:
                badjobfile.write("qsub -q prod -l walltime=48:00:00 job"+str(jobnum)+".sh\n")
            badjobfile.close()
            # make no attempt to merge histogram files yet
            sys.exit(1)

    # check whether any histogram files were produced in this set of jobs
    has_histograms=0
    for filename in os.listdir(workdir):
        if filename.find("histograms_")>=0 and filename[-5:]==".root":
            has_histograms=1
            histlist+=" "+filename
            
    # if we have histogram files, create ROOT script to merge them
    if has_histograms:
        rootdir=os.getenv("ROOTSYS")
        command="cd "+workdir+"; "+rootdir+"/bin/hadd -f histograms.root"+histlist
        print "merging root files..."
        os.system(command)

    # read sample description file to get directory where PAT files are stored for this sample
    sampleBaseDir=""
    samplePatFiles=[]
    exec(sample_cff_code(workdir))
    if sampleBaseDir=="":
        print "ERROR: sample description file does not contain sampleBaseDir"
        sys.exit(1)
        pass
    if len(samplePatFiles)==0:
        print "ERROR: sample description file does not contain samplePatFiles"
        sys.exit(1)
        pass

    # check if there are any prefilter files in this directory. skip rest if not
    print "copying prefilter root file from dCache"
    os.system("srmcp "+srm_path(sampleBaseDir)+"/prefilter.root file:///"+workdir+"/prefilter.root")
    print "done"
    return


def job_watcher_grid(workdir,only_once=0):
    # check argument
    filename=workdir+"/crab.cfg"
    if not os.path.isfile(filename):
        print "error: invalid working directory",workdir
        sys.exit(1)
    # find crab working directory inside the sample working directory
    result=os.popen("grep ui_working_dir "+workdir+"/crab.cfg").readlines()
    if len(result)<1:
        print "error: ui_working_dir not defined in crab.cfg"
        sys.exit(1)
    crabdir=result[0].split("=")[1].strip()


    # wait for jobs to finish
    notready=999
    print "waiting for grid jobs to be processed...."
    while notready>0:
        # result=os.popen("source ~/bin/setup_crab ; crab -status -c "+workdir+"/"+crabdir).readlines()
        result=os.popen("crab -status -c "+workdir+"/"+crabdir).readlines()
        current_job=1
        notready=0
        request_status=[]
        failed_jobs=[]
        status_survey={}
        for line in result:
            items=line.split()
            if len(items)<2: continue
            if items[0]==str(current_job):
                job_status=items[2]
                # make a survey of what our jobs are currently doing
                if status_survey.has_key(job_status):
                    status_survey[job_status]+=1
                else:
                    status_survey[job_status]=1
                if job_status=="Done" or job_status=="Cleared" or job_status=="Retrieved":
                    # check job exit codes
                    if len(items)>5:
                        exe_status=items[4]
                        job_status=items[5]
                        if exe_status!="0" or (job_status!="0" and job_status!="60303"):
                            print "  job",current_job,"status",exe_status,job_status
                            failed_jobs.append(current_job)
                    else:
                        # have no exit code information yet. probably ran without server.
                        print "  job",current_job," done, but no status information yet"
                        request_status.append(current_job)
                        notready+=1
                else:
                    notready+=1
                current_job+=1
        if len(request_status)>0:
            joblist=str(request_status[0])
            for i in range(len(request_status)-1):
                joblist+=","+str(request_status[i+1])
            # os.system("source ~/bin/setup_crab &> /dev/null; crab -get "+joblist+" -c "\
            os.system("crab -get "+joblist+" -c "\
                      +workdir+"/"+crabdir+" &> /dev/null")
        if len(failed_jobs)>0:
            joblist=str(failed_jobs[0])
            for i in range(len(failed_jobs)-1):
                joblist+=","+str(failed_jobs[i+1])
            print "  => list of failed jobs:",joblist
            resubmitfile=open(workdir+"/RESUBMIT.sh","w")
            resubmitfile.write("crab -get "+joblist+" -c "+crabdir+"\n")
            resubmitfile.write("crab -forceResubmit "+joblist+" -c "+crabdir+"\n")
            resubmitfile.close()
        print "number of jobs not ready yet:",notready,"out of",current_job-1," - status:",
        for entry in status_survey:
            print status_survey[entry],entry+".",
        print ""
        if only_once: notready=0
        if notready>0: time.sleep(300)


def grid_cleanup(workdir):
    from xml.dom.minidom import parseString

    # check argument
    filename=workdir+"/crab.cfg"
    if not os.path.isfile(filename):
        print "error: invalid working directory",workdir
        sys.exit(1)
    # find crab working directory inside the sample working directory
    result=os.popen("grep ui_working_dir "+workdir+"/crab.cfg").readlines()
    if len(result)<1:
        print "error: ui_working_dir not defined in crab.cfg"
        sys.exit(1)
    crabdir=result[0].split("=")[1].strip()

    # retrieve job output
    print "retrieving job log files..."
    # result=os.popen("source ~/bin/setup_crab ; crab -get -c "+workdir+"/"+crabdir).readlines()
    result=os.popen("crab -get -c "+workdir+"/"+crabdir).readlines()

    # retrieve job status (this was mandatory before crab -report at least in mid-2010)
    print "updating job status..."
    # result=os.popen("source ~/bin/setup_crab ; crab -status -c "+workdir+"/"+crabdir).readlines()
    result=os.popen("crab -status -c "+workdir+"/"+crabdir).readlines()

    # get list of successful jobs that corresponds to lumiSummary.json content
    # (from crab_fjr.xml files)

    # note that there is a script called ListGoodOutputFiles.pl that should
    # make this easier
    
    print "scanning for output files..."
    filelist=os.popen("ls -1 "+workdir+"/"+crabdir+"/res/crab_fjr*.xml").\
              readlines()
    patfiles={}
    prefilterfiles=[]
    joblist=[]
    goodjobs=[]
    for entry in filelist:
        # get and check job number
        jobnum=int(entry.split("/")[-1].replace("crab_fjr_","").replace(".xml",""))
        if jobnum in joblist:
            print "WARNING: found multiple crab_fjr files for job",jobnum
        else:
            joblist.append(jobnum)
            pass
        # parse xml
        jobreport=open(entry.strip())
        dom=parseString(jobreport.read())
        jobreport.close()
        fjr=dom.getElementsByTagName("FrameworkJobReport")[0]
        # read status of job (there are two status codes. both should be 0)
        exitcodes=fjr.getElementsByTagName("FrameworkError")
        values=[]
        for entry in exitcodes:
            try:
                values.append(int(entry.getAttribute("ExitStatus")))
            except:
                # non-numeric exit status. this cannot be good :-)
                values.append(999)
                pass
            pass
        if len(values)==2:
            exitcode=abs(values[0])+abs(values[1])
        else:
            exitcode=999
            pass
        if exitcode!=0: continue
        if not jobnum in goodjobs: goodjobs.append(jobnum)
        # read output file names
        patfiles[jobnum]=fjr.getElementsByTagName("File")[0].\
                          getElementsByTagName("LFN")[0].firstChild.data.strip()
        try:
            prefilterfiles.append(fjr.getElementsByTagName("AnalysisFile")[0].\
                                  getElementsByTagName("LFN")[0].\
                                  getAttribute("Value").strip())
        except:
            pass
        pass

    # create list of PAT files for sample description file
    goodjobs.sort()
    baseDir=""
    if len(goodjobs)>0:
        name=patfiles[joblist[0]]
        baseDir=name[:name.rfind("/")]
        baseDir=baseDir[:baseDir.rfind("/")]
        pass
    print "basedir:",baseDir
    logfilename="filelist."+crabdir.replace("workdir_","")
    print "writing list of outputfiles of successful jobs into",logfilename
    logfile=open(logfilename,"w")
    rereco=0
    modreco=0
    for entry in goodjobs:
        logfile.write("  sampleBaseDir+\""+patfiles[entry].replace(baseDir,"")+"\",\n")
        if patfiles[entry].find("rereco")>=0: rereco=1
        if patfiles[entry].find("modreco")>=0: modreco=1
        pass
    logfile.close()

    tmpDir = "/tmp/demattia/" + workdir.split("/")[-1]
    # now merge prefilter files (in batches of 100 each, to increase reliability)
    # dcacheDir="dcap://dcap.pp.rl.ac.uk/pnfs/pp.rl.ac.uk/data/cms/"
    dcacheDir="srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN=/store/user/demattia/"
    os.system("rm "+tmpDir+"prefilterfile*")
    if len(prefilterfiles)>0:
        rootdir=os.getenv("ROOTSYS")
        numbatches=int(len(prefilterfiles)/100.+0.9999)
        processed_files=[]
        tmpPrefilterFileName=[]
        print "merging prefilter files (%i batches for %i files)..."%(numbatches,len(prefilterfiles))
        for ibatch in range(numbatches):
            command="cd "+workdir+"; "+rootdir+"/bin/hadd -f prefilter_%i.root"%ibatch
            print "range",ibatch*100+0,"-",ibatch*100+99
            for i in range(ibatch*100,min(ibatch*100+100,len(prefilterfiles))):
                tmpPrefilterFileName.append(tmpDir+"prefilterfile_"+str(i)+".root")
                print "Copying "+prefilterfiles[i]+" to "+tmpPrefilterFileName[i]
                # FIXME: uncomment
                os.system("srmcp -2 \"srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN="+prefilterfiles[i]+"\" \"file:///"+tmpPrefilterFileName[i]+"\"")
                # # command+=" "+dcacheDir+"/"+prefilterfiles[i]
                command+=" "+tmpPrefilterFileName[i]
                processed_files.append(prefilterfiles[i])
                pass
            os.system(command)
            pass
        # double-check we got all files
        if len(prefilterfiles)!=len(processed_files):
            print "ERROR: coding bug led to not all prefilter files being processed"
            sys.exit(1)
            pass
        # merge all the batches
        command="cd "+workdir+"; "+rootdir+"/bin/hadd -f prefilter.root"
        for ibatch in range(numbatches):
            command+=" prefilter_%i.root"%ibatch
            pass
        # FIXME: uncomment
        os.system(command)

        # now copy merged prefilter file back to dCache
        # dcachename="srm://heplnx204.pp.rl.ac.uk:8443/pnfs/pp.rl.ac.uk/data/cms"\
        #             +baseDir+"/prefilter.root"
        dcachename="srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN="\
                    +baseDir+"/prefilter.root"
        print "Merged file is ready, copy it to "+dcachename
        result=os.popen("srmrm "+dcachename)
        time.sleep(2)
        # # os.system("lcg-cp "+workdir+"/prefilter.root "+dcachename)
        print "srmcp -2 \"file:///"+workdir+"/prefilter.root\" \""+dcachename+"\""
        # FIXME: uncomment
        os.system("srmcp -2 \"file:///"+workdir+"/prefilter.root\" \""+dcachename+"\"")

    # if we used a json file, then we conclude this is a data job -> get lumi
    if os.path.exists(workdir+"/json.txt"):

        # create lumiSummary.json
        print "creating crab report..."
        # result=os.popen("source ~/bin/setup_crab ; crab -report -c "+workdir+"/"+crabdir).readlines()
        result=os.popen("crab -report -c "+workdir+"/"+crabdir).readlines()
        lumiSummary=workdir+"/"+crabdir+"/res/lumiSummary.json "
        # query delivered luminosity
        print "querying luminosity overview..."
        lumiOverview=workdir+"/lumiOverview.csv"
        if not os.path.exists(lumiOverview):
            result=os.popen("lumiCalc2.py -o "+lumiOverview+" -i "+lumiSummary+" overview").readlines()
            if not os.path.exists(lumiOverview):
                print "ERROR: lumiCalc2.py failed"
                print result
                sys.exit(1)
                pass
            pass

        # query recorded luminosity
        print "querying recorded luminosity per trigger..."
        lumiDetails=workdir+"/lumiResult.csv"
        if not os.path.exists(lumiDetails):
            result=os.popen("lumiCalc2.py -o "+lumiDetails+" -i "+lumiSummary+" recorded").readlines()
            if not os.path.exists(lumiDetails):
                print "ERROR: lumiCalc2.py failed"
                print result
                sys.exit(1)
                pass
            pass

        # copy lumiSummary.json and DB query results to output directory
        print "copying luminosity info to dCache..."
        for filename in [lumiSummary,lumiOverview,lumiDetails]:
            # dcachename="srm://heplnx204.pp.rl.ac.uk:8443/pnfs/pp.rl.ac.uk"+\
            #             "/data/cms"+baseDir+"/"+filename.split("/")[-1]
            dcachename="srm://srm-dcache.rcac.purdue.edu:8443/srm/managerv2?SFN="\
                        +baseDir+"/"+filename.split("/")[-1]
            result=os.popen("srmrm "+dcachename)
            time.sleep(2)
            # os.system("lcg-cp "+filename+" "+dcachename)
            print "Copy the luminosity info to dCache"
            print "srmcp -2 \"file:///"+filename+"\" \""+dcachename+"\""
            os.system("srmcp -2 \"file:///"+filename+"\" \""+dcachename+"\"")
            pass
        pass
    return


def get_file_qualifiers(filename):
    items=filename.replace(".root","").split("_")
    # is the is a crab >=2.7.3 style name (job number, retry id, 3 random characters)?
    try:
        jobID=int(items[-3])
        retryID=int(items[-2])
        randomID=items[-1]
        if len(randomID)!=3: throw
        basename=filename.replace("_%i_%i_%s.root"%(jobID,retryID,randomID),"")
    except:
        jobID=-1
    if jobID==-1:
        # is this a crab 2.7.2 style name (job number and retry ID)?
        try:
            jobID=int(items[-2])
            retryID=int(items[-1])
            basename=filename.replace("_%i_%i.root"%(jobID,retryID),"")
        except:
            jobID=-1
            retryID=0
    if jobID==-1:
        # is this a crab 2.6 style name (only job number specified)?
        try:
            jobID=int(items[-1])
            basename=filename.replace("_%i.root"%jobID,"")
        except:
            jobID=-1
            basename=filename.replace(".root","")
    return [jobID,retryID,basename]


def dense_list(list):
    output="["
    for entry in list:
        output+=str(entry)+","
    output=output[:-1]+"]"
    return output


def check_job_output_dir(filelist):
    # try to match up output files with a typical crab output file set
    #
    existing_files=get_dir_content(filelist)
    # sort files into edm files and prefilter files
    existing_edm_files=[]
    existing_prefilter_files=[]
    for entry in existing_files:
        if entry.find("prefilter")>=0:
            existing_prefilter_files.append(entry)
        elif entry[-5:]==".root":
            existing_edm_files.append(entry)
            pass
        pass
    # distinguish between edm files with and without matching prefilter
    edm_files_with_prefilter=[]
    edm_files_without_prefilter=[]
    for entry in existing_edm_files:
        if entry.replace("PATtuple","prefilter") in existing_prefilter_files:
            edm_files_with_prefilter.append(entry)
        else:
            edm_files_without_prefilter.append(entry)
            pass
        pass
    # if there is at least one matching prefilter file,
    # we assume that prefilter files should be avilable for all files
    if len(edm_files_with_prefilter)>0:
        relevant_files=edm_files_with_prefilter
    else:
        relevant_files=edm_files_without_prefilter
        pass
    # now sort files into job slots
    coded_names=[]
    jobIDs=[]
    for i in range(len(relevant_files)):
        [newJobID,newRetryID,newBasename]=get_file_qualifiers(relevant_files[i])
        jobIDs.append(newJobID)
        coded_names.append("%05i,%05i,%s,%05i"
                           %(newJobID,newRetryID,newBasename,i))
        pass
    coded_names.sort()
    coded_names.append("99999,99999,endmarker,99999")
    # look for missing jobs
    jobIDs.sort()
    lastID=0
    missing_jobs=[]
    for i in range(len(jobIDs)):
        if jobIDs[i]>lastID+1:
            for imissing in range(lastID+1,jobIDs[i]):
                missing_jobs.append(imissing)
        lastID=jobIDs[i]
    # loop over existing files and associate them with jobs
    best_file_list=[]
    last_jobNum=0
    matching_files=[]
    extra_files=[]
    for entry in coded_names:
        current_jobNum=int(entry.split(",")[0])
        if current_jobNum!=last_jobNum and len(matching_files)>0:
            maxRetryID=-1
            bestFiles=[]
            for match in matching_files:
                thisRetryID=int(match.split(",")[1])
                if thisRetryID>maxRetryID:
                    maxRetryID=thisRetryID
                    bestFiles=[match]
                elif thisRetryID==maxRetryID:
                    bestFiles.append(match)
            # if we have more than one file with latest retry ID, try to
            # match basenames
            bestFile=bestFiles[0]
            if len(bestFiles)>1:
                for cand in bestFiles:
                    for matchcand in relevant_files:
                      if matchcand.find(cand.split(",")[2])==0:
                          bestFile=cand
            best_file_list.append(relevant_files[int(bestFile.split(",")[3])])
            matching_files=[]
        matching_files.append(entry)
        last_jobNum=current_jobNum

    if len(missing_jobs)>0:
        print "  missing jobs:",dense_list(missing_jobs)
        print "  (disclaimer: this check will not find if the last job(s)"
        print "  in the list are missing because this code does not know"
        print "  the total number of jobs that were run!)"
    numExtra=len(relevant_files)-len(best_file_list)
    if numExtra>0:
        print numExtra,"extra files found in directory:"
        for entry in existing_files:
            if not entry in best_file_list:
                print "   ",entry
                pass
            pass
        pass
    return best_file_list

    
def check_files(sample,filelist,detailed_check):

    local_filelist=filelist[:]
    local_filelist.sort()
    best_file_list=check_job_output_dir(local_filelist)
    sorted_best_file_list=best_file_list[:]
    sorted_best_file_list.sort()

    # initialise categories
    missing=[]
    cantcheck=[]
    corrupt=[]
    good=[]
    total_num_events=0
    
    # loop over all files
    if detailed_check:
        print "checking edm files for integrity. this can take a loong time..."
    for filename in best_file_list:
        if detailed_check:
            result=check_edm_file(filename)
        else:
            result=checkedm_retCANNOTCHECK
        if result==checkedm_retMISSING:
            # this should never happen, but who knows...
            missing.append(filename)
        elif result==checkedm_retCORRUPT or result==checkedm_retNOEDM:
            corrupt.append(filename)
        elif result==checkedm_retCANNOTCHECK:
            cantcheck.append(filename)
        else:
            good.append(filename)
            total_num_events+=result

    print "    files queried: %4i"%len(best_file_list)
    if len(good)>0:
        print "    good files   : %4i"%len(good)
    if len(missing)>0:
        print "    missing files: %4i"%len(missing)
    if len(corrupt)>0:
        print "    corrupt files: %4i"%len(corrupt)
    if len(cantcheck)>0:
        print "    can't check  : %4i"%len(cantcheck)
    if len(best_file_list)!=len(filelist):
        print "    note discrepancy between requested file list and actual file list!"
        print "      %4i files requested in sample description file"%len(filelist)
        print "      %4i files found in directory"%len(best_file_list)
    if total_num_events!=sample.sampleNumEvents and detailed_check:
        print "    number of events",total_num_events,"( expected",sample.sampleNumEvents,")"
    elif not detailed_check:
        print "    warning: number of events not checked"
    if len(missing)>0:
        # get a list of job numbers for easy crab resubmission
        joblist=""
        for entry in missing:
            [jobID,retryID,basename]=get_file_qualifiers(entry)
            joblist+=str(jobID)+","
        joblist=joblist[:-1]
        print "    list of missing files:",joblist
    if len(corrupt)>0:
        # create a file that contains a list of corrupt files.
        # most likely you will want to delete those, and therefore we convert the
        # file paths to something most useful for piping into commands such as rm, lcg-del etc
        badfilename="corrupted_files_"+sample.id
        if os.path.exists(badfilename):
            num=0
            while os.path.exists(badfilename+"_%i"%num): num+=1
            badfilename=badfilename+"_%i"%num
        badfile=open(badfilename,"w")
        for entry in corrupt:
            if entry.find("file:")>=0:
                badfile.write("%s\n"%entry.replace("file:",""))
            elif entry.find("dcap:")>=0:
                badfile.write("%s\n"%srm_path(entry))
            else:
                badfile.write("%s\n"%entry)
        badfile.close()
    # print file list if it disagrees with what is in the sample description file
    if sorted_best_file_list!=local_filelist:
        print "  file names are different!"
        if len(best_file_list)>0:
            baseDir=best_file_list[0][:best_file_list[0].rfind("/")]
            baseDir=baseDir[:baseDir.rfind("/")]
            print "       base directory=",baseDir
            cff_file=open(sample.cff,"r")
            newfile=open(sample.cff.split("/")[-1],"w")
            in_patlist=0
            for line in cff_file.readlines():
                if not in_patlist:
                    newfile.write(line)
                    pass
                if line.split()==["samplePatFiles","=","["]:
                    in_patlist=1
                    count=len(best_file_list)
                    for entry in best_file_list:
                        count-=1
                        if count==0:
                            comma=""
                        else:
                            comma=","
                            pass
                        newfile.write("  sampleBaseDir+\""\
                                      +entry.replace(baseDir,"")+"\""+comma+"\n")
                        pass
                    pass
                if in_patlist and line.find("]")>=0:
                    newfile.write("    ]\n")
                    in_patlist=0
                    pass
                pass
            newfile.close()

