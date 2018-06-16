import os,sys,glob
from ROOT import TFile, TH1F,gROOT

def update_progress(iteration,complete):
    barLength = 30
    status = ""
    progress=float(iteration)/float(complete)
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rFiles processed: %i/%i [%s] %s"%(int(iteration),int(complete),"#"*block+"-"*(barLength-block),status)
    sys.stdout.write(text)
    sys.stdout.flush()

def getNEvents(path,filename=''):
    scriptdir=os.getcwd()
    print('-----------------------------------------------------------------')
    print('-----------------------------------------------------------------')
    print('getting Number of Events from file(s) in ' + path +filename)
    print('-----------------------------------------------------------------')
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel=2001;")
    os.chdir(path)
    files=[]
    if(filename==''):
        files=glob.glob('*.root')
        files.sort()
        if(len(ntuples)==0):
            print("couldn't find any root-Files to extract Number of Events! Setting N=0.")
            return 0
    else:
        files.append(path+'/'+filename)
        print(files)
    NEvents=0
    for i in range(len(files)):
        rootFile=TFile(files[i])
        hist=TH1F('hist','hist',1,0,10000)
        if(filename==''):
            rootFile.Get('AnalysisTree').Draw('run>>hist')
        else:
            hist=rootFile.Get('tau21sel/N_AK4')
        # NEvents=NEvents+int(hist.GetEntries())
        NEvents=int(hist.Integral())
        print('Integral:',NEvents)
        targetlumi=36814.0
        if("W" in filename):
            datasetlumi=10476.098
        elif("Z" in filename):
            datasetlumi=170354.67
        elif("QCD" in filename):
            datasetlumi=458.91148
        if(not "Data" in filename):
            print('expected: (Entries*(targetlumi/datasetlumi)):' ,hist.GetEntries()*(targetlumi/datasetlumi))
        update_progress(i+1,len(files))
    os.chdir(scriptdir)
    print('-----------------------------------------------------------------')
    return float(NEvents)

if(__name__=='__main__'):
    # WJetspath = '/pnfs/desy.de/cms/tier2/store/user/salbrech/RunII_80X_v3/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToQQ_HT-600ToInf/180418_091054/0000'
    # ZJetspath = '/pnfs/desy.de/cms/tier2/store/user/salbrech/RunII_80X_v3/ZJetsToQQ_HT600toInf_13TeV-madgraph/crab_ZJetsToQQ_HT600toInf_13TeV-madgraph/180418_093627/0000'
    # NWJets='Total Number of Events in WJets-NTuple: %i \n'%getNEvents(WJetspath)
    # NZJets='Total Number of Events in ZJets-NTuple: %i \n'%getNEvents(ZJetspath)
    # with open('NEvents.txt','w') as outputfile:
    #     outputfile.write(NWJets)
    #     outputfile.write(NZJets)

    uhh2path='/nfs/dust/cms/user/albrechs/UHH2_Output/SignalRegion/tau21_45/'
    WJetsfilename = 'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_HT600ToInf.root'
    ZJetsfilename = 'uhh2.AnalysisModuleRunner.MC.MC_ZJetsToQQ_HT600ToInf.root'
    QCDfilename  = 'uhh2.AnalysisModuleRunner.MC.MC_QCD.root'
    Datafilename  = 'uhh2.AnalysisModuleRunner.Data.DATA_JetHT.root'

    
    NData=getNEvents(uhh2path,Datafilename)
    NWJets=getNEvents(uhh2path,WJetsfilename)
    NZJets=getNEvents(uhh2path,ZJetsfilename)
    NQCD=getNEvents(uhh2path,QCDfilename)

    print('NData:',NData,'NWJets:',NWJets,'NZJets:',NZJets)
    print('NQCD_expected',(NData-NWJets-NZJets),'NQCD_actual:',NQCD)
    print('scale for QCD:', '(',NData,'-',NWJets,'-',NZJets,')/',NQCD,'=',(NData-NWJets-NZJets)/NQCD)
