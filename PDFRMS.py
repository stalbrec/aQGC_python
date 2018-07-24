import os,sys,glob,math
from array import array
from ROOT import TFile, TH1F,gROOT,gStyle,TCanvas,TGraph,TProfile,TLegend,TF1
from PointName import getPointNameI
gROOT.SetBatch(True)


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

def FitGaus(hist,Bin):
    gStyle.SetOptStat(1)
    gStyle.SetOptFit(1111)    

    fitcanv=TCanvas("fitcanv","fitcanv",600,600)
    fitcanv.cd()

    gaus_sigma=0

    hist_mean=hist.GetMean()
    hist_RMS=hist.GetRMS()

    range_width_par=3
 
    xmin=hist_mean-range_width_par*hist_RMS
    xmax=hist_mean+range_width_par*hist_RMS
    # hist.GetXaxis().SetRangeUser(xmin,xmax)
    hist.GetXaxis().SetRangeUser(0,hist_mean+10*hist_RMS)

    f_gaus=TF1("f1","gaus",xmin,xmax)

    # f_gaus.SetParameters(1,Hists[0].GetBinContent(i),Hists[0].GetBinContent(i))
    f_gaus.SetParameters(1,hist.GetMean(),hist.GetRMS())
    hist.Fit(f_gaus,"R")
    gaus_sigma=f_gaus.GetParameter(1)
    fitcanv.Print("PDFStudy/PDFRMS_GausFit_Bin_%i.eps"%Bin)
    # hist.Draw
    # raw_input("press enter to continue")
    # gStyle.SetOptStat(0)
    # gStyle.SetOptFit(0000)    
    return gaus_sigma


    

    
if(__name__=='__main__'):
    channels=['WPWP','WMWM','WPWM','WPZ','WMZ','ZZ']
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/PDFStudy/'
    # gStyle.SetOptStat(0)
    # gStyle.SetOptFit(0000)    
    # gStyle.SetOptTitle(0)
    GausFit=True
    Point=0

    filename='uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic_%i.root'%(channels[5],Point)

    f=TFile(path+'/'+filename)

    # PDFHists_invMAk4sel_1p0/M_jj_AK8_PARAM_POINT_pdf_pdfIndex
    # PDFHists_invMAk4sel_1p0/M_jj_AK8_S0_328p0_pdf_0
    # for i in range(100):
    # histgroup='PDFHists_invMAk4sel_1p0/M_jj_AK8_%s_%s_pdf_'%getPointNameI(Point)
    # print histgroup+str(0)
    # h_nominal=f.Get(histgroup+str(0))
    # print h_nominal
    binning=array('d')
    # binwidth=200
    # #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
    # NBins=(14000/binwidth)
    NBins=35
    binwidth=14000./float(NBins)

    for i in range(NBins+1):
        binning.append(int(i*binwidth))
    print(binning)

    print("NBins:"+str(NBins)+" len(binning): "+str(len(binning)))
    HistDir=f.GetDirectory('PDFHists_invMAk4sel_1p0')
    Histkeys=HistDir.GetListOfKeys()
    Hists=[]
    profile=TProfile('prof','prof', NBins,binning)
    # graph=TGraph(NBins)
    RMSMean=TH1F('RMSMean','RMSMean',NBins,binning)
    RMSNoMean=TH1F('RMSNoMean','RMSNoMean',NBins,binning)
    RootRMS=TH1F('RootRMS','RootRMS',NBins,binning)
    GausSigma=TH1F('GausSigma','GausSigma',NBins,binning)
    Mean=TH1F('Mean','Mean',NBins,binning)

    RMSMean.SetLineColor(46)
    RMSNoMean.SetLineColor(38)
    RootRMS.SetLineColor(36)
    GausSigma.SetLineColor(42)
    Mean.SetLineColor(1)

    linewidth=3

    RMSMean.SetLineWidth(linewidth)
    RMSNoMean.SetLineWidth(linewidth)
    Mean.SetLineWidth(linewidth)
    RootRMS.SetLineWidth(linewidth)
    GausSigma.SetLineWidth(linewidth)   
    RMSMean.SetLineStyle(1)
    RMSNoMean.SetLineStyle(1)
    RootRMS.SetLineStyle(1)
    GausSigma.SetLineStyle(1)
    Mean.SetLineStyle(2)



    for key in Histkeys:
        OrigHist=key.ReadObj()

        #removing one statistical fluctuation
        OrigHist.SetBinContent(1887,0)
        #finding bin with stat fluc (in old ZZ-Sample this means BinContent is larger than 1)
        # for i in range(1,OrigHist.GetNbinsX()+1):
        #     if OrigHist.GetBinContent(i) >1:
        #         print i,' is larger than 1'
                
        RebinHist=OrigHist.Rebin(NBins,OrigHist.GetName(),binning)
        Hists.append(RebinHist)
    NPDFVariations=100
    for i in range(1,NBins+1):

        NonZero=False
        x=Hists[0].GetBinCenter(i)
        mean=Hists[0].GetBinContent(i)
        Mean.Fill(x,mean)
        slice_title='Bin: %i (%.0f GeV #leq M_{jj,AK8} < %.0f GeV)'%(i,Hists[0].GetBinLowEdge(i),Hists[0].GetBinLowEdge(i)+Hists[0].GetBinWidth(i))
        h_slice=TH1F(slice_title,slice_title,100,0,1)
        h_slice.GetXaxis().SetTitle("Events in M_{jj} Bin")
        h_slice.GetYaxis().SetTitle("#")
        for j in range(1,NPDFVariations+1):
            h_slice.Fill(Hists[j].GetBinContent(i),1)
            if(Hists[j].GetBinContent(i)>0):
                NonZero=True
        #RootRMS: StandardDeviation of Variations to HistMean
        RootRMS.Fill(x,h_slice.GetRMS())        

        #RootRMS: StandardDeviation of Gaus-Fit (Not trying to fit if Hist has no NonZero Bins)
        if(GausFit):
            if(NonZero):
                GausSigma.Fill(x,FitGaus(h_slice,i))
            else:
                GausSigma.Fill(x,0)           
        
        #StandardDeviation of Variations to NOMINAL
        sigma2=0
        for j in range(1,NPDFVariations+1):
            sigma2+=(Hists[j].GetBinContent(i)-mean)**2
        sigma2=sigma2/(NPDFVariations)
        # RMS=mean**2+sigma2
        RMS=sigma2
        RMS=math.sqrt(RMS)
        y=RMS

        RMSMean.Fill(x,y)
        
        #RMS: StandardDeviation of Variations to ZERO
        RMS=0
        for j in range(1,NPDFVariations+1):
            RMS+=(Hists[j].GetBinContent(i))**2
        RMS=RMS/(NPDFVariations)
        RMS=math.sqrt(RMS)
        y=RMS       
        RMSNoMean.Fill(x,y)
        del h_slice


    # for i in range(1,NBins+1):
    #     A=RMSMean.GetBinContent(i)
    #     B=RootRMS.GetBinContent(i)
    #     if(A>0):
    #         abweichung=(A-B)/A
    #     else:
    #         abweichung=-1
    #     print "Bin i: ",i," - Abweichung: ",abweichung
        
    gStyle.SetOptStat(0)
        
    canv=TCanvas('canv','canv',600,600)
    canv.SetLogy()
    leg = TLegend(0.7,0.6,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.AddEntry(Mean,'x_{n} (=x_{nominal})','l')
    leg.AddEntry(RMSMean,'#frac{#Sigma^{N}_{i=1} (x_{i}-x_{n})^{2}}{N}','l')
    # leg.AddEntry(RMSMean,'#bar{x} + #frac{#Sigma^{N}_{i=1} (x_{i}-#bar{x})^{2}}{N}','l')
    # leg.AddEntry(RMSNoMean,'#frac{#Sigma^{N}_{i=1} (x_{i})^{2}}{N}','l')
    # leg.AddEntry(RMSMean,'Standard-Deviation','l')
    # leg.AddEntry(RMSNoMean,'RootMeanSquared','l')
    leg.AddEntry(RootRMS,'RMS_{Root}','l')
    if(GausFit):
        leg.AddEntry(GausSigma,'#sigma_{gauss-fit}','l')
    leg.SetTextSize(0.03)
    
    drawoptions='Hist'
    Mean.GetXaxis().SetRangeUser(100,9000)
    Mean.GetXaxis().SetTitle("M_{jj,AK8}")
    Mean.GetYaxis().SetTitle("#")
    Mean.SetTitle('RMS Comparison')
    Mean.Draw(drawoptions)
    RMSMean.Draw(drawoptions+'SAME')
    # RMSNoMean.Draw(drawoptions+'SAME')
    RootRMS.Draw(drawoptions+'SAME')
    if(GausFit):
        GausSigma.Draw(drawoptions+'SAME')
    Mean.Draw(drawoptions+'SAME')
    leg.Draw('SAME')
    canv.Print("PDFStudy/comparison.eps")


        
