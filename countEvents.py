import os,glob
from ROOT import TFile, TH1F,gROOT

def getNEvents(path):
    scriptdir=os.getcwd()
    print 'getting Number of Events from Ntuples in ' + path
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel=2001;")
    os.chdir(path)
    ntuples=glob.glob('*.root')
    ntuples.sort()
    NEvents=0
    if(len(ntuples)==0):
        print "couldn't find any root-Files to extract Number of Events! Setting N=0."
        return 0
    for i in len(ntuples):
        rootFile=TFile(ntuples[i])
        hist=TH1F('hist','hist',1,0,10000)
        rootFile.Get('AnalysisTree').Draw('run>>hist')
        NEvents=NEvents+int(hist.GetEntries())
        update_progress(i+1,len(ntuples))
    os.chdir(scriptdir)
    return NEvents

if(__name__=='__main__'):
    WJetspath = '/pnfs/desy.de/cms/tier2/store/user/salbrech/RunII_80X_v3/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToQQ_HT-600ToInf/180418_091054/0000'
    ZJetspath = '/pnfs/desy.de/cms/tier2/store/user/salbrech/RunII_80X_v3/ZJetsToQQ_HT600toInf_13TeV-madgraph/crab_ZJetsToQQ_HT600toInf_13TeV-madgraph/180418_093627/0000'
    NWJets='Total Number of Events in WJets-NTuple:' +getNEvents(WJetspath)
    NZJets='Total Number of Events in ZJets-NTuple:' +getNEvents(ZJetspath)
    with open('NEvents.txt','w') as outputfile:
        outputfile.write(NWJets)
        outputfile.write(NZJets)
