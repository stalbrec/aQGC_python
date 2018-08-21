from ROOT import TFile
import glob
# files=glob.glob("/nfs/dust/cms/user/albrechs/UHH2_Output/PreSelection/workdir_preselection/uhh2.AnalysisModuleRunner.MC.MC_QCD_HT700to1000_*.root")
files=glob.glob("/nfs/dust/cms/user/albrechs/UHH2_Output/PreSelection/workdir_preselection/*MC_ZZ*.root")
# files=glob.glob("/nfs/dust/cms/user/albrechs/UHH2_Output/PreSelection/workdir_preselection/*.root")
files.sort()
N_Events=0
failed=[]
succeded=[]
lastSample=''
print 'Files: ', files
for f in files:
    currentSample=str(f.split('.')[-2].split('_')[:-2])
    index=f.split('_')[-1].split('.')[0]
    if(currentSample!=lastSample):
        N_Events=0
        print 'Failed: ',failed
        failed=[]
        lastSample=currentSample
        # print currentSample+':'
        
    # print 'trying to open:',f
    rootFile=TFile(f)
    # rootFile.ls()    file=TFile(filename)
    # tree=rootFile.Get('AnalysisTree')
    tree=rootFile.Get('uhh2_meta')
    if(tree==None):
        # print 'File #',index,' is missing the uhh2_meta Tree'
        failed.append(index)
        continue
    N_Events+=tree.GetEntries()
    if '300' in currentSample:
        succeded.append(currentSample+'_'+index)
    # print 'NEvents:',N_Events, ' Fileindex:', index
    rootFile.Close()
print succeded
