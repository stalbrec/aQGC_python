import os,sys,glob,numpy
from checkRootFiles import checkChannelFiles
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

def getCrossSection(file):
    handle_start='Original cross-section: '
    handle_end=' pb (cross-section'

    with open(file,'r') as logfile:
        for line in logfile:
            if(handle_start in line):
                xsect=line[line.index(handle_start)+len(handle_start):line.index(handle_end)]
                xsect_tuple=(float(xsect[:xsect.index(' +-')]),float(xsect[xsect.index('+- ')+3:]))
                return xsect_tuple

def getCrossSections(channel,indices):
    scriptdir=os.getcwd()
    os.chdir('/nfs/dust/cms/user/albrechs/production/ntuples/split_LHE/%s'%channel)
    xsections=[]
    print('getting Cross-Sections from LHE-Logs..')
    for i in range(0,len(indices),1):
        if(os.path.isdir(str(i))):
            files=glob.glob('%i/*.o*'%indices[i])
            latest_file = max(files, key=os.path.getctime)
            xsect=getCrossSection(latest_file)
            if(xsect!=None):
                xsections.append(xsect)
        update_progress(i+1,len(indices))
        if(len(xsections)==0):
            print("couldn't find any Log-Files to extract cross-section! Continuing with next Channel...")
            continue
    os.chdir(scriptdir)
    return xsections

def getNEvents(channel,indices):
    scriptdir=os.getcwd()
    print('getting Number of Events from Ntuples...')
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel=2001;")
    os.chdir('/nfs/dust/cms/user/albrechs/production/ntuples/NT_%s'%channel)
    ntuples=glob.glob('*.root')
    ntuples.sort()
    NEvents=0
    if(len(ntuples)==0):
        print("couldn't find any root-Files to extract Number of Events! Setting N=0.")
        return 0
    for i in range(0,len(indices)):
        rootFile=TFile('Ntuple_%s_%i.root'%(channel,indices[i]))
        hist=TH1F('hist','hist',1,0,10000)
        rootFile.Get('AnalysisTree').Draw('run>>hist')
        NEvents=NEvents+int(hist.GetEntries())
        update_progress(i+1,len(indices))
    os.chdir(scriptdir)
    return NEvents

def writeConfig_old(channel,failed_jobs,lumi):
    path="/nfs/dust/cms/user/albrechs/production/ntuples/NT_%s"%channel
    with open('UHH2Configs/aQGC%sjjhadronic.conf'%channel,'wt') as fout:
        fout.write('<InputData Lumi="%0.f" NEventsMax="-1" Type="MC" Version="MC_aQGC_%sjj_hadronic" Cacheable="False">\n'%(lumi,channel))
        indices1=range(0,100)
        for i in indices1:
            if(i in failed_jobs):
                fout.write('<!-- <In FileName="%s/Ntuple_%s_%i.root" Lumi="0.0"/> -->\n'%(path,channel,i))
            else:
                fout.write('<In FileName="%s/Ntuple_%s_%i.root" Lumi="0.0"/>\n'%(path,channel,i))
        fout.write('    <InputTree Name="AnalysisTree" />\n</InputData>')
def writeConfig(luminosities,Region):
    with open('UHH2Configs/aQGCVVjjhadronic_REGION.xml','r') as template:
        filedata = template.read()
        for (channel,lumi) in luminosities:
            print('replacing %sLUMI with %.2f'%(channel,lumi))
            filedata=filedata.replace('%sLUMI'%channel,'%.2f'%lumi)
        print('replacing REGION with %s'%Region)
        filedata=filedata.replace('REGION',Region)
        with open('UHH2Configs/aQGCVVjjhadronic_%s.xml'%Region,'w') as configFile:
            configFile.write(filedata)

if(__name__=='__main__'):
    channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    regions=['SignalRegion','LOWSidebandRegion','HIGHSidebandRegion']
    # channels=['ZZ']
    luminosities=[]
    for channel in channels:
        print('-----------------%s-----------------'%channel)
        failed_jobs=checkChannelFiles(channel)
        indices=range(0,100)
        for i in indices:
            if( ((not (os.path.exists('/nfs/dust/cms/user/albrechs/production/ntuples/NT_%s/Ntuple_%s_%i.root'%(channel,channel,i)))) or not( os.stat('/nfs/dust/cms/user/albrechs/production/ntuples/NT_%s/Ntuple_%s_%i.root'%(channel,channel,i)).st_size>1000000  )) and (i not in failed_jobs) ):
                failed_jobs.append(i)
        failed_jobs.sort()
        for i in failed_jobs:
            indices.remove(i)
        print(len(failed_jobs),'->',failed_jobs)
        NEvents=getNEvents(channel,indices)
        xsections=getCrossSections(channel,indices)
        sum_nom=0
        sum_den=0
        for xsect in xsections:
            sum_nom=sum_nom+(xsect[0]/(xsect[1]**2))
            sum_den=sum_den+(1/(xsect[1]**2))
        if(sum_den>0):
            mean=sum_nom/sum_den
            mean_err=1/(numpy.sqrt(sum_den))
            lumi=NEvents/mean
            luminosities.append((channel,lumi))
            #writeConfig(channel,failed_jobs,lumi)
        else:
            mean=0
            mean_err=0
            lumi=0
        print('N_xsection=',len(xsections))
        print('gewichteter Mittelwert=',mean,'+-',mean_err,'pb')
        print('N_Events:',NEvents)
        print('resulting Luminosity:',lumi,'pb^-1')
        print('--------------------------------------\n\n')

    for region in regions:
        writeConfig(luminosities,region)
