from ROOT import gROOT, gStyle, TCanvas, TColor, TF1, TFile, TLegend, THStack
#import myutils,shutil,os
gROOT.Reset()

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



class Set:
    def __init__(self, dim8op):
        self.SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_aQGC_WPWPjj_hadronic.root")
        self.BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
        self.SHistNames=[]
        self.OpName=dim8op
        fillHistNames(self.SHistNames,self.OpName)
        self.SHists=[]
        #print "getting %s Hists.."%self.OpName
        

        #getting S- and B-Hist from respective file:
        for histname in self.SHistNames:
            #print 'getting',histname,"..."
            current_hist=self.SFile.Get('MjjHists_invMAk4sel_allcuts/%s'%histname)
            current_hist.SetTitle(histname)
            self.SHists.append(current_hist)
            
        self.BHist=self.BFile.Get("invMAk4sel_allcuts/M_jj_AK8")



        #self.Limits=(,)

    def exportPlot(self,logY=True,path="./plots"):
        plottitle="invariant Mass of AK8 Jets (%s-Operator)"%self.OpName
        #canv = TCanvas(plottitle,plottitle,200,10,700,500)
        canv = TCanvas(plottitle,plottitle,600,600)
        
        #turning off the standard Statistic-Box
        gStyle.SetOptStat(0)

        legend = TLegend(0.5,0.7,0.9,0.9)
        #legend.SetHeader("Legend","C") #option "C" allows to center the header
     
        drawOptions="HE"
        if(logY):
            canv.SetLogy()

        #Cosmetics:
        self.BHist.SetFillColor(867)
        self.BHist.SetLineColor(867)

        self.BHist.SetTitle(plottitle)
        self.BHist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
        self.BHist.GetYaxis().SetTitle('Events')
        self.BHist.GetXaxis().SetRangeUser(0,7500)
        self.BHist.GetYaxis().SetRangeUser(10**(-3),10**5)
        self.BHist.GetYaxis().SetTitleOffset(1.3)

        legend.AddEntry(self.BHist,"QCD","f")
        self.BHist.Draw(""+drawOptions)
                
        
        # stack=THStack("qcdstack",plottitle)
        # stack.Add(self.BHist)
        # stack.Draw(""+drawOptions)

        # stack.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
        # stack.GetYaxis().SetTitle('Events')
        # stack.GetXaxis().SetLimits(0,7500)
        # stack.GetYaxis().SetLimits(10**(-10),10**5)

        
        # legend.AddEntry(stack,"QCD","l")
        # stack.Draw(""+drawOptions)
        #canv.Update()

        
        histcounter=2
        
        #number of Parameters to plot:
        
        n=(sets[self.OpName][0]-1)/2
        n=n/6
        for i in [0,n,2*n,4*n,5*n,6*n-1]:
            hist=self.SHists[i]
        #for hist in self.SHists:
            #hist.SetLineColor(TColor.kAzure+histcounter)
            hist.SetLineColor(histcounter)
            #hist.SetLineStyle(histcounter)
            #hist.Draw("H][SAME"+drawOptions)
            hist.Draw("SAME"+drawOptions)
            point=sets[self.OpName][1]+i*sets[self.OpName][2]
            legend.AddEntry(hist,"W^{+}W^{+}jj (%s=%.1fTeV^{-4})"%(self.OpName,point))
            histcounter+=1


        canv.SetTitle(plottitle)
        legend.Draw()        
        canv.Update()
        canv.Print("%s/%s.eps"%(path,self.OpName))
        

    def calcLimits(self):
        Nbins = self.BHist.GetNbinsX()
        bin=0
        BSum=0
        SSums=[]
        for hist in self.SHists:
            SSums.append(0)
        for i in list(reversed(range(Nbins))):
            #print 'SHists[0].GetBinError(',i,'):',self.SHists[0].GetBinError(i)
            if(BSum>=10):
                break
            BSum+=self.BHist.GetBinContent(i)
            for j in range(0,len(self.SHists)):
                SSums[j]+=self.SHists[j].GetBinContent(i)
            bin=i
        
        print 'BSum=',BSum,' -> bin:',bin,';BinCenter:',self.BHist.GetBinCenter(bin)


        lower_limit_index= -1
        upper_limit_index= -1

        expectedLimit_S=7.5312

        for i in range(0,len(SSums)):           
            if(i<=(len(SSums)/2)):
                if( SSums[i]<=expectedLimit_S and lower_limit_index==-1):
                    lower_limit_index=i
            elif(i>(len(SSums)/2)):
                if( SSums[i]>=expectedLimit_S and upper_limit_index==-1):
                    upper_limit_index=i-1


        print self.OpName,'-',SSums[lower_limit_index],'-',self.getPoint(lower_limit_index)
        
        lower_limit=approxLimit(expectedLimit_S,self.getPoint(lower_limit_index-1),SSums[lower_limit_index-1],self.getPoint(lower_limit_index),SSums[lower_limit_index])
        upper_limit=approxLimit(expectedLimit_S,self.getPoint(upper_limit_index),SSums[upper_limit_index],self.getPoint(upper_limit_index+1),SSums[upper_limit_index+1])

        self.Limits=(lower_limit,upper_limit)
        

    def getPoint(self,i):
        return sets[self.OpName][1]+i*sets[self.OpName][2]


def approxLimit(S,X1,Y1,X2,Y2):
    m=(Y2-Y1)/(X2-X1)
    b=(Y1*X2-Y2*X1)/(X2-X1)
    return (S-b)/m




def getParName(OpName,startx, increment, i):
    name="M_jj_AK8_%s_"%OpName
    parameter=10*startx+i*10*increment
    if(parameter>=0):
        name+="%ip%i"%(parameter/10,parameter%10)
    else:
        name+="m%ip%i"%(-parameter/10,-parameter%10)
    return name

def fillHistNames(HistNames,OpName):
    for i in range(sets[OpName][0]):
        HistNames.append(getParName(OpName,sets[OpName][1],sets[OpName][2],i))