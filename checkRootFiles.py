import glob, os, csv, sys
from ROOT import TFile, TH1F, gROOT

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

def checkChannelFiles(channel):
    gROOT.SetBatch(True)
    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    scriptdir=os.getcwd()
    path="/nfs/dust/cms/user/albrechs/production/ntuples/split_LHE/"


    #extracting expected Number of Reweighting Points
    N_Reweight_expected=0
    # with open('ReweightingRanges/%sRange.csv'%channel,'r') as rangefile:
    with open('ReweightingRanges/ZZRange.csv','r') as rangefile:
        csvreader=csv.DictReader(rangefile)
        for row in csvreader:
            N_Reweight_expected+=int(row['Npoints'])
    os.chdir(path+channel)
    files=glob.glob("*.root")
    failed_jobs=range(0,100)
        
    print '%s (expected #ReweightingPoints %i):'%(channel,N_Reweight_expected)

    if(len(files)==0):
        print 'no files in this channel! exiting..'
        os.chdir(scriptdir)
        return -1

    print 'number of files:',len(files)

    for i in range(len(files)):
        size=os.stat(files[i]).st_size
        file_index=files[i][files[i].find("LHE_")+4:files[i].find(".root")]
        #if file is smaller than 47kB job definitely failed
        if(size<47000):
            # failed_jobs.append(int(file_index))
            update_progress(i+1,len(files))
            continue
        rootFile=TFile(files[i])
        gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")
        wgt_hist=TH1F('wgt_hist','systweights',1,0,100)
        rootFile.Get('Events').Draw('wgt>>wgt_hist')
        N_Reweight_actual=int(wgt_hist.GetEntries())/500
        
        # if('WPWP' in channel):
        #     N_Reweight_actual-=882
        # else:
        #     N_Reweight_actual-=1080
        N_Reweight_actual-=1080
        # print 'actual Reweight Points:',N_Reweight_actual
        if(N_Reweight_actual==N_Reweight_expected):
            failed_jobs.remove(int(file_index))
        update_progress(i+1,len(files))
    #print indices of failed jobs (negative indices belong to jobs which failed due to missing motivation of reweighting-procedure
    print 'Failed Jobs:'
    #print failed_jobs
    os.chdir(scriptdir)
    
        #print snippet for resubmit-script
    failed_jobs.sort()
    snippet='('
    for job in failed_jobs:
        snippet+='%i '%int(job)
    snippet=snippet[:-1]
    snippet+=')'
    print 'Number of failed Jobs:',len(failed_jobs)
    print snippet
    return failed_jobs
    
if(__name__=='__main__'):
    print 'checking Files of following channels:'
    # channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    channels=['WPWP']
    # channels=["WPZ","WMZ","ZZ"]
    # channels=["WPZ","WMZ","ZZ"]
    # channels=['WPZ']
    for channel in channels:
        checkChannelFiles(channel)
