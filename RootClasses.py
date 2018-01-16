#from ROOT import gROOT, TCanvas, TF1, TFile
#import myutils,shutil,os
#gROOT.Reset()

class Set:
    def __init__(self, dim8op):
        #self.SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/testuhh2.AnalysisModuleRunner.MC.aQGC_WPWPjj_hadronic.root")
        #self.BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
        self.SHistNames=[]
        self.OpName=dim8op
        fillHistNames(self.SHistNames,self.OpName)
        self.SHists=[]
        print "getting %s Hists.."%self.OpName
        #for histname in self.SHistNames:
            #print 'getting',histname,"..."
            #self.SHists.append(SFile.Get('MjjHists_detaAk4sel_allcuts/%s'%histname))
        self.BHist=BFile.Get("detaAk4sel_allcuts/M_jj_AK8")
        self.binB10=GetBin10(self.BHist) #ist es sinnvoll es hier zu tun?
        
        #Sollte eigentlich funktionieren
        def exportPlot(self,logY,path="~/www/"):
            plottitle="invariant Mass of AK8 Jets (Scanned through %s-Operator)"%self.OpName
            canv = TCanvas(plottitle,plottitle,200,10,700,500)
            self.BHist.SetTitle(plottitle)
            self.BHist.Draw("HIST")
            for hist in SHists:
                hist.Draw("H][SAME")
            if(self.logY):
                canv.SetLogy()
            canv.SetTitle(plottitle)
            canv.Update()
            canv.Print("%s/%s.png"%path,self.OpName)
        

        def exportCalc():
            self.BHist.GetXaxis().SetRangeUser(BHist.GetBinCenter(self.binB10-1),7500)
        


def getParName(OpName,startx, increment, i):
    name="M_jj_AK8_%s_"%OpName
    parameter=10*startx+i*10*increment
    if(parameter>=0):
        name+="%ip%i"%(parameter/10,parameter%10)
    else:
        name+="m%ip%i"%(-parameter/10,-parameter%10)
    return name
        
def fillHistNames(HistNames,OpName):
    sets={
        "S0":[91,-900.0,20.0],
        "S1":[67,-330.0,10.0],
        "M0":[85,-42.0,1.0],
        "M1":[67,-165.0,5.0],
        "M6":[85,-84.0,2.0],
        "M7":[121,-300.0,5.0],
        "T0":[69,-6.8,0.2],
        "T1":[51,-12.5,0.5],
        "T2":[83,-20.5,0.5]}
    for i in range(0,sets[OpName][0]):
        HistNames.append(getParName(OpName,sets[OpName][1],sets[OpName][2],i))


def GetBin10(Hist):
    bin = 0
    content = 0
    crossed_first_non_zero=False
    for i in range(0,Hist.GetNbinsX()):
        bin = i
        content = Hist.GetBinContent(bin)
        if(content>0):
            crossed_first_non_zero=True
        if(crossed_first_non_zero && content <=10):
            break
    return bin
