import os,sys,glob,math
from array import array
from ROOT import TFile, TH1F,gROOT,gStyle,TCanvas,TGraph,TProfile,TLegend,TF1,TLatex,TLine,TPad,gPad,TObject
import ROOT as rt
from PointName import getPointNameI
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTextFont(43)

gStyle.SetTitleOffset(0.86,"X")
gStyle.SetTitleOffset(1.6,"Y")
# gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadLeftMargin(0.1)
# gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadTopMargin(0.08)
# gStyle.SetPadRightMargin(0.08)
gStyle.SetPadRightMargin(0.1)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.05, "XYZ")
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

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

if(__name__=='__main__'):
    channels=['WPWP','WMWM','WPWM','WPZ','WMZ','ZZ']
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/PDFStudy/'
    # gStyle.SetOptStat(0)
    # gStyle.SetOptFit(0000)    
    # gStyle.SetOptTitle(0)
    Point=0
    xTitle="M_{jj,AK8}"
    xLabelSize=18.
    yLabelSize=18.
    xTitleSize=20.
    yTitleSize=22.
    xTitleOffset=4.
    yTitleOffset=1.3
    xRangeMin=100
    xRangeMax=11000
    filename='uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic_%i.root'%(channels[5],Point)

    f=TFile(path+'/'+filename)

    binning=array('d')
    # binwidth=200
    # #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
    # NBins=(14000/binwidth)
    NBins=35
    binwidth=14000./float(NBins)

    for i in range(NBins+1):
        binning.append(int(i*binwidth))
    
    #getting pdf4lhc hists
    if(Point>0):
        pdf4lhcHistDir=f.GetDirectory('PDFHists_invMAk4sel_1p0')
    else:
        pdf4lhcHistDir=f.GetDirectory('UncertaintiesHists_invMAk4sel_1p0')
    pdf4lhcHistKeys=pdf4lhcHistDir.GetListOfKeys()
    pdf4lhcHists=[]
    for key in pdf4lhcHistKeys:
        OrigHist=key.ReadObj()
        if('pdf' not in OrigHist.GetName()):
            continue
        # print OrigHist.GetName()
        RebinHist=OrigHist.Rebin(NBins,OrigHist.GetName(),binning)
        pdf4lhcHists.append(RebinHist)

    #getting nnpdf hists
    nnpdfHistDir=f.GetDirectory('MjjHists_invMAk4sel_1p0')
    nnpdfHistKeys=nnpdfHistDir.GetListOfKeys()
    nnpdfHists=[]
    for key in nnpdfHistKeys:
        OrigHist=key.ReadObj()
        if('AK8_' in OrigHist.GetName()):
            RebinHist=OrigHist.Rebin(NBins,OrigHist.GetName(),binning)
            nnpdfHists.append(RebinHist)


    nnpdf=TH1F('nnpdf_nom','nnpdf_nom',NBins,binning)
    pdf4lhc=TH1F('pdf4lhc_nom','pdf4lhc_nom',NBins,binning)
    pdf4lhcRoot=TH1F('pdf4lhc_nom_root','pdf4lhc_nom_root',NBins,binning)
    pdf4lhcRMS=TH1F('pdf4lhc_rms','pdf4lhc_rms',NBins,binning)
    pdf4lhcRootRMS=TH1F('pdf4lhc_rootrms','pdf4lhc_rootrms',NBins,binning)

    pdf4lhc=pdf4lhcHists[0].Clone()
    pdf4lhcRoot=pdf4lhcHists[0].Clone()
    nnpdf=nnpdfHists[Point].Clone()
    
    linewidth=3
    pdf4lhc.SetLineWidth(linewidth)
    pdf4lhc.SetLineStyle(1)
    pdf4lhc.SetLineColor(31)
    pdf4lhcRoot.SetLineWidth(linewidth)
    pdf4lhcRoot.SetLineStyle(1)
    pdf4lhcRoot.SetLineColor(31)
    nnpdf.SetLineWidth(linewidth)
    nnpdf.SetLineStyle(1)
    nnpdf.SetLineColor(1)

        
    NPDFVariations=100
    for i in range(1,NBins+1):
        x=pdf4lhcHists[0].GetBinCenter(i)
        mean=pdf4lhcHists[0].GetBinContent(i)
        # slice_title='Bin: %i (%.0f GeV #leq M_{jj,AK8} < %.0f GeV)'%(i,Hists[0].GetBinLowEdge(i),Hists[0].GetBinLowEdge(i)+Hists[0].GetBinWidth(i))
        slice_title='test'
        h_slice=TH1F(slice_title,slice_title,100,0,1)
        h_slice.GetXaxis().SetTitle("Events in M_{jj} Bin")
        h_slice.GetYaxis().SetTitle("#")
        for j in range(1,NPDFVariations+1):
            h_slice.Fill(pdf4lhcHists[j].GetBinContent(i),1)
        #StandardDeviation of Variations to NOMINAL
        sigma2=0
        for j in range(1,NPDFVariations+1):
            sigma2+=(pdf4lhcHists[j].GetBinContent(i)-mean)**2
        sigma2=sigma2/(NPDFVariations)
        # RMS=mean**2+sigma2
        RMS=sigma2
        RMS=math.sqrt(RMS)       
        pdf4lhc.SetBinError(i,RMS)
        pdf4lhcRoot.SetBinError(i,h_slice.GetRMS())
        pdf4lhcRMS.Fill(x,RMS)
        pdf4lhcRootRMS.Fill(x,h_slice.GetRMS())
        del h_slice
        
    gStyle.SetOptStat(0)


    #constructing ErrorHists:
    nnpdfUnc=TH1F('nnpdf_Unc','nnpdf_Unc',NBins,binning)
    pdf4lhcUnc=TH1F('pdf4lhc_Unc','pdf4lhc_Unc',NBins,binning)
    pdf4lhcUncRoot=TH1F('pdf4lhc_Unc_root','pdf4lhc_Unc_root',NBins,binning)

    nnpdfUnc=nnpdf.Clone()
    pdf4lhcUnc=pdf4lhc.Clone()
    pdf4lhcUncRoot=pdf4lhcRoot.Clone()

    nnpdfUnc.SetFillStyle(3204)
    nnpdfUnc.SetFillColor(rt.kGray+2)
    nnpdfUnc.SetLineColor(1)

    pdf4lhcUnc.SetFillStyle(3214)
    pdf4lhcUnc.SetFillColor(46)
    pdf4lhcUnc.SetLineColor(47)

    pdf4lhcUncRoot.SetFillStyle(3365)
    pdf4lhcUncRoot.SetFillColor(46)
    pdf4lhcUncRoot.SetLineColor(46)

    canv=TCanvas('canv','canv',600,600)

    yplot=0.7
    yratio=0.3
    ymax=1.0
    xmax=1.0
    xmin=0.0
    plotpad=TPad("plotpad","Plot",xmin,ymax-yplot,xmax,ymax)
    ratiopad=TPad("ratiopad","Ratio",xmin,ymax-yplot-yratio,xmax,ymax-yplot)


    plotpad.SetTopMargin(0.08)
    plotpad.SetBottomMargin(0.016)
    plotpad.SetLeftMargin(0.1)
    plotpad.SetRightMargin(0.05)
    plotpad.SetTicks()

    ratiopad.SetTopMargin(0.016)
    ratiopad.SetBottomMargin(0.35)
    ratiopad.SetLeftMargin(0.1)
    ratiopad.SetRightMargin(0.05)
    ratiopad.SetTicks()
    plotpad.Draw()
    ratiopad.Draw()
    plotpad.SetLogy()
    canv.SetLogy()
    ratiopad.SetGrid()
    plotpad.cd()
    leg = TLegend(0.55,0.66,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    # leg.AddEntry(pdf4lhc,'#splitline{PDF4LHC15_nlo_100_pdfas nominal}{#alpha_{s}(MZ)=0.118}','l')
    leg.AddEntry(pdf4lhc,'#splitline{PDF4LHC15 nominal = x_{n}}{(#alpha_{s}(M_{Z})=0.118)}','l')
    leg.AddEntry(TH1F(),'','')
    leg.AddEntry(pdf4lhcUnc,'x_{n} #pm RMS = x_{n} #pm #frac{#Sigma^{N}_{i=1} (x_{i}-x_{n})^{2}}{N}','f')
    leg.AddEntry(TH1F(),'','')
    # leg.AddEntry(pdf4lhcRoot,'#splitline{PDF4LHC15 nominal = x_{n}}{#alpha_{s}(MZ)=0.118}','l')
    # leg.AddEntry(pdf4lhcUncRoot,'x_{n} #pm RootRMS','f') 
    # leg.AddEntry(TH1F(),'','')
    # leg.AddEntry(nnpdf,'#splitline{NNPDF30_lo_as_0130_nf_4 nominal}{#alpha_{s}(MZ)= 0.2544}','l')
    leg.AddEntry(nnpdf,'#splitline{NNPDF30 nominal}{(#alpha_{s}(M_{Z})= 0.2544)}','l')
    leg.AddEntry(TH1F(),'','')
    leg.AddEntry(nnpdfUnc,'stat. Unc. of NNPDF','f')
    leg.SetTextSize(0.025)
    leg.SetMargin(0.3)
    
    drawoptions='Hist'
    nnpdfUnc.GetXaxis().SetRangeUser(xRangeMin,xRangeMax)
    nnpdfUnc.GetYaxis().SetTitleFont(43)
    nnpdfUnc.GetYaxis().SetTitleSize(yTitleSize)
    nnpdfUnc.GetYaxis().SetTitleOffset(yTitleOffset)
    nnpdfUnc.GetYaxis().SetLabelFont(43)
    nnpdfUnc.GetYaxis().SetLabelSize(yLabelSize)
    nnpdfUnc.GetXaxis().SetTitleSize(0.0)
    nnpdfUnc.GetXaxis().SetLabelSize(0.0)
    nnpdfUnc.GetYaxis().SetRangeUser(1.1*10**(-4),100)
    nnpdfUnc.GetXaxis().SetTitle(xTitle)
    nnpdfUnc.GetYaxis().SetTitle("Events")
    nnpdfUnc.SetTitle('PDF Uncertainty')
    nnpdfUnc.Draw('E2')
    nnpdf.Draw(drawoptions+'SAME')
    nnpdfUnc.Draw('E2SAME')
    pdf4lhcUnc.Draw('E2SAME')
    pdf4lhc.Draw(drawoptions+'SAME')
    pdf4lhcUnc.Draw('E2SAME')
    # pdf4lhcUncRoot.Draw('E2SAME')
    
    plotpad.RedrawAxis()
    
    ratiopad.cd()
    #RatioHist
    pdf4lhcRatio=TH1F('pdf4lhc_Ratio','pdf4lhc_Ratio',NBins,binning)
    pdf4lhcRatio=pdf4lhcRMS.Clone()
    pdf4lhcRatio.Divide(pdf4lhc)

    # pdf4lhcRatioRoot=TH1F('pdf4lhc_RatioRoot','pdf4lhc_RatioRoot',NBins,binning)
    # pdf4lhcRatioRoot=pdf4lhcRootRMS.Clone()
    # pdf4lhcRatioRoot.Divide(pdf4lhcRoot)

    for i in range(1,NBins):
        pdf4lhcRatio.SetBinError(i,.1)
        # pdf4lhcRatioRoot.SetBinError(i,.1)
    
    
    pdf4lhcRatio.SetLineColor(46)
    pdf4lhcRatio.SetMarkerColor(46)
    pdf4lhcRatio.SetStats(0)
    pdf4lhcRatio.SetMarkerStyle(21)
    pdf4lhcRatio.SetMarkerSize(0.7)

    # pdf4lhcRatioRoot.SetLineColor(46)
    # pdf4lhcRatioRoot.SetMarkerColor(46)
    # pdf4lhcRatioRoot.SetStats(0)
    # pdf4lhcRatioRoot.SetMarkerStyle(21)
    # pdf4lhcRatioRoot.SetMarkerSize(0.7)

    #Yaxis
    pdf4lhcRatio.GetYaxis().SetRangeUser(0.001,0.7)
    pdf4lhcRatio.GetYaxis().SetTitle("RMS/x_{n}")
    pdf4lhcRatio.GetYaxis().CenterTitle()
    pdf4lhcRatio.GetYaxis().SetTitleFont(43)
    pdf4lhcRatio.GetYaxis().SetTitleSize(yTitleSize)
    pdf4lhcRatio.GetYaxis().SetTitleOffset(yTitleOffset)
    pdf4lhcRatio.GetYaxis().SetLabelFont(43)
    pdf4lhcRatio.GetYaxis().SetLabelSize(yLabelSize)
    pdf4lhcRatio.GetYaxis().SetNdivisions(506)
    #Xaxis
    pdf4lhcRatio.GetXaxis().SetRangeUser(xRangeMin,xRangeMax)
    pdf4lhcRatio.GetXaxis().SetTitle(xTitle)
    pdf4lhcRatio.GetXaxis().SetTitleFont(43)
    pdf4lhcRatio.GetXaxis().SetTitleSize(xTitleSize)
    pdf4lhcRatio.GetXaxis().SetTitleOffset(xTitleOffset)
    pdf4lhcRatio.GetXaxis().SetLabelFont(43)
    pdf4lhcRatio.GetXaxis().SetLabelSize(xLabelSize)
    pdf4lhcRatio.GetXaxis().SetTickLength(0.08)
    pdf4lhcRatio.GetXaxis().SetNdivisions(506)

    pdf4lhcRatio.Draw("ep")
    # pdf4lhcratioroot.Draw("epsame")

    # zeropercent=TLine(ratioXMin,1,ratioXMax,1)
    # zeropercent.Draw()
    # plus10percent=TLine(ratioXMin,1.1,ratioXMax,1.1)
    # plus10percent.SetLineStyle(rt.kDashed)
    # plus10percent.Draw()
    # minus10percent=TLine(ratioXMin,0.9,ratioXMax,0.9)
    # minus10percent.SetLineStyle(rt.kDashed)
    # minus10percent.Draw()

    canv.cd()
    gPad.RedrawAxis()
    leg.Draw('SAME')

    canv.Print("PDFStudy/pdfstudy.eps")


        
