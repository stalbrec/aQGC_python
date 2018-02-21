from ROOT import gROOT, gStyle, TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph
from array import array
import csv,collections
#import myutils,shutil,os
gROOT.Reset()

sets=collections.OrderedDict()

class Set:
    def __init__(self, dim8op,channelname,Cut):
        gROOT.SetBatch(True)
        with open("ReweightingRanges/"+channelname+'Range.csv','rb') as csvfile:
            setreader=csv.DictReader(csvfile)
            for row in setreader:
                sets.update({row['parameter']:[
                            int(row['Npoints']),
                            float(row['start']),
                            float(row['stepsize'])
                            ]})
        self.channel=channelname
        gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
        self.SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root"%self.channel)
        self.BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
        gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")
        self.SHistNames=[]
        self.OpName=dim8op
        self.LastCut=Cut
        fillHistNames(self.SHistNames,self.OpName)
        self.SHists=[]
        
        SHistDir=self.SFile.GetDirectory('MjjHists_%s_%s'%(self.LastCut,self.channel))
        SHistkeys=SHistDir.GetListOfKeys()
        for key in SHistkeys:
            if ( (dim8op not in str(key)) or ('AK8' not in str(key))): 
                continue
            self.SHists.append(key.ReadObj())

        self.BHist=self.BFile.Get('%s/M_jj_AK8'%self.LastCut)

    def exportPlot(self,logY=True,path="./output/plots"):
        plottitle="invariant Mass of AK8 Jets (%s-Operator) in %s"%(self.OpName,self.channel)
        canv = TCanvas(plottitle,plottitle,600,600)
        
        #turning off the standard Statistic-Box
        gStyle.SetOptStat(0)

        legend = TLegend(0.5,0.7,0.9,0.9)
        
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
        
        histcounter=1
        
        #number of Parameters to plot:        
        n=6
        med=(sets[self.OpName][0]-1)/2 -1
        # starti=(sets[self.OpName][0]-1)/2-n

        # for i in range(0,2*n+1):
            # index=starti+i
        for i in range(n):
            index= i * med/n
            hist=self.SHists[index]
            hist.SetLineColor(histcounter)
            hist.Draw("SAME"+drawOptions)
            legend.AddEntry(hist,"%sjj (%s=%.1fTeV^{-4})"%(self.channel,self.OpName,self.getPoint(index)))
            histcounter+=1
        
        canv.SetTitle(plottitle)
        legend.Draw()        
        canv.Update()
        canv.Print("%s/%s_%s.eps"%(path,self.channel,self.OpName))
        

    def calcLimits(self,path="./output/plots"):
        Nbins = self.BHist.GetNbinsX()
        bin=0
        BSum=0
        SSums=[]
        for hist in self.SHists:
            SSums.append(0)
        for i in list(reversed(range(Nbins))):
            if(BSum>=10):
                break
            BSum+=self.BHist.GetBinContent(i)
            
            for j in range(0,len(self.SHists)):
                SSums[j]+=self.SHists[j].GetBinContent(i)
            bin=i
        print 'BSum=',BSum,' -> bin:',bin,';BinCenter:',self.BHist.GetBinCenter(bin)


        #Save SSums to file

        # integraloutput=open('%s_%s_integral.txt'%(self.channel,self.OpName),'wt')
        # integraloutput.write('\n--------------bin %i (%.0f GeV)--------------\n'%(bin,self.BHist.GetBinCenter(bin)))
        # integraloutput.write('BSum=%.2f\n'%BSum)
        # for i in range(0,len(SSums)):
        #     integraloutput.write('SSum(%s)=%.2f\n'%(self.SHists[i],SSums[i]))

        lower_limit_index= -1
        upper_limit_index= -1

        expectedLimit_S=0
        if(self.LastCut=='detaAk4sel'):
            expectedLimit_S=7.8750 #for B=11.084414348
        elif(self.LastCut=='invMAk4sel_1p5_allcuts'):
            expectedLimit_S=7.9688 #for B=11.3923148662
        elif(self.LastCut=='invMAk4sel_2p0_allcuts'):
            expectedLimit_S=8.6250 #for B=13.8555178046
        else:
            expectedLimit_S=1000 


        #expectedLimit_S=7.8438 #for B=11.08
        #expectedLimit_S=7.5312 #for B=10
        #expectedLimit_S=7.5312 #for B=10
        #expectedLimit_S=20.8750 #for B=100
        #expectedLimit_S=63.2500 #for B=1000

        for i in range(0,len(SSums)):           
            if(lower_limit_index==-1):
                if( SSums[i]<=expectedLimit_S):
                    lower_limit_index=i
            elif(upper_limit_index==-1):
                if( SSums[i]>=expectedLimit_S):
                    upper_limit_index=i-1

        # for i in range(0,len(SSums)):           
        #     if(i<=(len(SSums)/2)):
        #         if( SSums[i]<=expectedLimit_S and lower_limit_index==-1):
        #             lower_limit_index=i
        #     elif(i>(len(SSums)/2)):
        #         if( SSums[i]>=expectedLimit_S and upper_limit_index==-1):
        #             upper_limit_index=i-1
        
        # if(lower_limit_index==-1 and upper_limit_index==-1):
        #     print 'COUDLNT EXCLUDE ANYTHING'
        # elif(lower_limit_index==-1):
        #     print 'COUDLNT DETERMINE LOWER LIMIT'
        # elif(upper_limit_index==-1):
        #     print 'COUDLNT DETERMINE UPPER LIMIT'

        self.limitCalc_succeeded=(lower_limit_index!=-1 and upper_limit_index!=-1)

        #print self.OpName,'/',lower_limit_index,'-',SSums[lower_limit_index],'-',self.getPoint(lower_limit_index) 
        #print self.OpName,'/',upper_limit_index,'-',SSums[upper_limit_index],'-',self.getPoint(upper_limit_index)
        
        lower_limit=approxLimit(expectedLimit_S,self.getPoint(lower_limit_index-1),SSums[lower_limit_index-1],self.getPoint(lower_limit_index),SSums[lower_limit_index])
        upper_limit=approxLimit(expectedLimit_S,self.getPoint(upper_limit_index),SSums[upper_limit_index],self.getPoint(upper_limit_index+1),SSums[upper_limit_index+1])

        self.Limits=(lower_limit,upper_limit)


        #Plot SSums and 'calculated limits'
        plot1=TCanvas('parameterIntegral','EventYields for Parameter %s (%s)'%(self.OpName,self.channel),600,600)
        plot1.SetLogy()
        limit_legend = TLegend(0.6,0.12,0.9,0.3)

        x, y = array( 'd' ), array( 'd' )
        for i in range(0,len(SSums)):
            x.append(self.getPoint(i))
            y.append(SSums[i])
        graph=TGraph(len(SSums),x,y)
        graph.SetLineColor( 2 )
        graph.SetLineWidth( 2 )
        graph.SetMarkerColor( 1 )
        graph.SetMarkerStyle( 3 )
        graph.SetTitle('EventYields for Parameter F_{%s}'%self.OpName)
        graph.GetXaxis().SetTitle('F_{%s}/#Lambda^{4} [TeV^{-4}]'%self.OpName)
        graph.GetYaxis().SetTitle('S')
        graph.Draw( 'AP' )
        limit_legend.AddEntry(graph,"S (for B=%.2f)"%BSum,'p')


        #plot Line at expectedLimit_S for the given B
        slimit=TGraph()
        slimit.SetPoint(0,self.getPoint(0),expectedLimit_S)
        slimit.SetPoint(1,self.getPoint(sets[self.OpName][0]-1),expectedLimit_S)
        slimit.SetLineWidth(2)
        slimit.SetLineStyle(2)
        slimit.Draw("LSAME")
        
        if(self.limitCalc_succeeded):
            #plot the first points where S<...
            llimit=TGraph()
            llimit.SetPoint(0,self.getPoint(lower_limit_index),0)
            llimit.SetPoint(1,self.getPoint(lower_limit_index),100)
            llimit.SetLineWidth(2)
            llimit.SetLineStyle(2)
            llimit.Draw("LSAME")

            ulimit=TGraph()
            ulimit.SetPoint(0,self.getPoint(upper_limit_index),0)
            ulimit.SetPoint(1,self.getPoint(upper_limit_index),100)
            ulimit.SetLineWidth(2)
            ulimit.SetLineStyle(2)
            ulimit.Draw("LSAME")
        
            limit_legend.AddEntry(ulimit,'first points where S<%.2f'%expectedLimit_S,'l')

            #plot the interpolated Limits
            llimit_interpolated=TGraph()
            llimit_interpolated.SetPoint(0,self.Limits[0],0)
            llimit_interpolated.SetPoint(1,self.Limits[0],100)
            llimit_interpolated.SetLineWidth(2)
            llimit_interpolated.SetLineStyle(2)
            llimit_interpolated.SetLineColor(4)
            llimit_interpolated.Draw("LSAME")

            ulimit_interpolated=TGraph()
            ulimit_interpolated.SetPoint(0,self.Limits[1],0)
            ulimit_interpolated.SetPoint(1,self.Limits[1],100)
            ulimit_interpolated.SetLineWidth(2)
            ulimit_interpolated.SetLineStyle(2)
            ulimit_interpolated.SetLineColor(4)
            ulimit_interpolated.Draw("LSAME")

            limit_legend.AddEntry(ulimit_interpolated,'interpolated limits','l')


        #Plot the best Limits from CMS/ATLAS
        llimit_best=TGraph()
        ulimit_best=TGraph()
        with open('best_limits_ssWW.csv','rb') as limitcsv:
            limitreader=csv.DictReader(limitcsv)
            for row in limitreader:
                if(row['parameter']==self.OpName):
                    llimit_best.SetPoint(0,float(row['mob']),0)
                    llimit_best.SetPoint(1,float(row['mob']),100)
                    ulimit_best.SetPoint(0,float(row['pob']),0)
                    ulimit_best.SetPoint(1,float(row['pob']),100)
        llimit_best.SetLineWidth(2)
        llimit_best.SetLineStyle(2)
        llimit_best.SetLineColor(2)
        llimit_best.Draw("LSAME")
        ulimit_best.SetLineWidth(2)
        ulimit_best.SetLineStyle(2)
        ulimit_best.SetLineColor(2)
        ulimit_best.Draw("LSAME")
        
        limit_legend.AddEntry(ulimit_best,'ssWW Limits (SMP-17-004)','l')
        
        limit_legend.Draw()

        plot1.Update()
        plot1.GetFrame().SetBorderSize( 12 )
        plot1.Modified()
        plot1.Update()        
        plot1.Print('%s/SPlot_%s_%s_%s.eps'%(path,self.channel,self.OpName,self.LastCut))
        

    def getPoint(self,i):
        return sets[self.OpName][1]+i*sets[self.OpName][2]


def approxLimit(S,X1,Y1,X2,Y2):
    m=(Y2-Y1)/(X2-X1)
    if(m==0):
        return 0
    b=(Y1*X2-Y2*X1)/(X2-X1)
    return (S-b)/m




def getParName(OpName,startx, increment, i):
    name="M_jj_AK8_%s_"%OpName
    parameter=100*startx+i*100*increment
    if(parameter>=0):
        name+="%ip%i"%(parameter/100,parameter%100)
    else:
        name+="m%ip%i"%(-parameter/100,-parameter%100)
    return name

def fillHistNames(HistNames,OpName):
    for i in range(sets[OpName][0]):
        HistNames.append(getParName(OpName,sets[OpName][1],sets[OpName][2],i))
