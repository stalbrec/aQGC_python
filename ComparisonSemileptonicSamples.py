from array import array
import os, sys, csv, collections, numpy, math, gc
from ROOT import gROOT, gSystem, gStyle, gPad, TCanvas, TColor, TF1, TH1F, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex, TPad, TLine
import ROOT as rt

def magnitude(x):
    return int(math.floor(math.log10(x)))

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


def make_plot(plot):
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/GenStudies'
    plotdir='genstudies'
    # plotdir='mjjCut'

    plottitle=plotdir+'_'+plot

    lumi=36.814
    xTitle='M_{ZZ} [GeV/c^{2}]'
    xLabelSize=18.
    yLabelSize=18.
    xTitleSize=20.
    yTitleSize=22.
    xTitleOffset=4.
    yTitleOffset=1.3

    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    
    aQGChadronic=TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_aQGC_ZZjj_hadronic.root")
    aQGCSMEWK=TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_aQGC_semileptonic.root")
    SMEWK=TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_SM_semileptonic.root")

    gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")

    aQGChadronicHist=aQGChadronic.Get(plotdir+'/'+plot)
    aQGCSMHist=aQGCSMEWK.Get(plotdir+'/'+plot)
    SMHist=SMEWK.Get(plotdir+'/'+plot)

    # r_binning=range(0,14000,200)
    # d_binning=array('d')
    # for b in r_binning:
    #     d_binning.append(b)
    # aQGChadronicHist=aQGChadronicHist.Rebin(len(d_binning)-1,'new binning',d_binning)
    # aQGCSMHist=aQGCSMHist.Rebin(len(d_binning)-1,'new binning',d_binning)
    # SMHist=SMHist.Rebin(len(d_binning)-1,'new binning',d_binning)
    
    # aQGChadronicHist.Scale(1./6.922467571046638)
    # aQGCSMHist.Scale(6.922467571046638)
    # SMHist.Scale(6.922467571046638)

    
    canv = TCanvas(plottitle,plottitle,600,600)

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
    # if('-logX' in xTitle):
    #     plotpad.SetLogx()
    #     ratiopad.SetLogx()
    #     canv.SetLogx()
        
    drawOptions="HE1"

    BHist=THStack(plottitle,plottitle)

    QCDColor=rt.kAzure+7
    WJetsColor=rt.kRed-4
    ZJetsColor=rt.kOrange-2
    TTColor=rt.kGreen+2
    

    aQGChadronicHist.SetLineColor(rt.kRed-2)  
    aQGCSMHist.SetLineColor(rt.kBlue-2)   
    aQGChadronicHist.SetLineWidth(2)  
    aQGCSMHist.SetLineWidth(2)   

    aQGChadronicHist.Add(SMHist)


    legend = TLegend(0.6,0.75,0.8,0.92)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.02)
    legend.SetMargin(0.4)
    # legend.SetNColumns(2)
    legend.SetColumnSeparation(0.3)


    legend.AddEntry(aQGChadronicHist,"A: c*aQGChadronic +  SM","l")
    legend.AddEntry(aQGCSMHist,      "B: aQGCsemilep and SM","l")
    legend.AddEntry(TH1F(),'c #approx #frac{0.033 * 3}{0.69}','')
    # legend.AddEntry(SMHist,"EWK SM","f")
    # legend.AddEntry(BHistErr,"stat. Uncertainty","f")

    canv.SetTitle(plottitle)


    aQGChadronicHist.GetYaxis().SetTitle('Events')
    # aQGChadronicHist.GetYaxis().SetRangeUser(MIN,MAX)
    aQGChadronicHist.GetYaxis().SetTitleFont(43)
    aQGChadronicHist.GetYaxis().SetTitleSize(yTitleSize)
    aQGChadronicHist.GetYaxis().SetTitleOffset(yTitleOffset)
    aQGChadronicHist.GetYaxis().SetLabelFont(43)
    aQGChadronicHist.GetYaxis().SetLabelSize(yLabelSize)

    aQGChadronicHist.GetXaxis().SetTitleSize(0.0)
    aQGChadronicHist.GetXaxis().SetLabelSize(0.0)

    # if(YRangeUser):
    #     BHistErr.GetYaxis().SetRangeUser(Ymin,Ymax)
    # if(XRangeUser):
    #     BHistErr.GetXaxis().SetRangeUser(Xmin,Xmax)

    plotpad.cd()
    aQGChadronicHist.Draw('H1')
    aQGCSMHist.Draw('H1SAME')
    plotpad.RedrawAxis()

    ratiopad.cd()

    ratioHist=aQGChadronicHist.Clone()
    ratioHist.Add(aQGCSMHist,-1)
    ratioHist.Divide(aQGChadronicHist)
    
    
    ratioHist.SetLineColor(rt.kBlack)
    # ratioHist.Sumw2()
    ratioHist.SetStats(0)
    ratioHist.SetMarkerStyle(21)
    ratioHist.SetMarkerSize(0.7)

    #Yaxis
    ratioHist.GetYaxis().SetRangeUser(0.,1.4)
    ratioHist.GetYaxis().SetTitle("(A-B)/A")
    ratioHist.GetYaxis().CenterTitle()
    ratioHist.GetYaxis().SetTitleFont(43)
    ratioHist.GetYaxis().SetTitleSize(yTitleSize)
    ratioHist.GetYaxis().SetTitleOffset(yTitleOffset)
    ratioHist.GetYaxis().SetLabelFont(43)
    ratioHist.GetYaxis().SetLabelSize(yLabelSize)
    ratioHist.GetYaxis().SetNdivisions(506)
    #Xaxis
    ratioHist.GetXaxis().SetTitle(xTitle)
    ratioHist.GetXaxis().SetTitleFont(43)
    ratioHist.GetXaxis().SetTitleSize(xTitleSize)
    ratioHist.GetXaxis().SetTitleOffset(xTitleOffset)
    ratioHist.GetXaxis().SetLabelFont(43)
    ratioHist.GetXaxis().SetLabelSize(xLabelSize)
    ratioHist.GetXaxis().SetTickLength(0.08)
    ratioHist.GetXaxis().SetNdivisions(506)

    # if(YRangeUser):
    #     ratioHist.GetYaxis().SetRangeUser(Ymin,Ymax)
    # if(XRangeUser):
    #     ratioHist.GetXaxis().SetRangeUser(Xmin,Xmax)
    #     ratioXMin=Xmin
    #     ratioXMax=Xmax
    # else:
    ratioXMin=ratioHist.GetXaxis().GetXmin()
    ratioXMax=ratioHist.GetXaxis().GetXmax()
    ratioHist.Draw("ep")



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
    legend.Draw()

    latex=TLatex()
    latex.SetNDC(kTRUE)
    latex.SetTextSize(20)
    latex.DrawLatex(0.69,0.953,"%.2f fb^{-1} (13 TeV)"%lumi)
    latex.DrawLatex(0.1,0.953,"private work")

    canv.Update()
    # canv.Print('Plots/%s_%s.png'%(plotdir,plot))
    canv.Print('Mjj_SampleComparison'+plot+'.eps')


    canv2 = TCanvas(plottitle+'_2',plottitle+'_2',600,600)
    ratioHist.GetYaxis().SetTitleOffset(1.)
    ratioHist.GetYaxis().CenterTitle(rt.kFALSE)
    ratioHist.GetXaxis().SetTitleOffset(1.)
    ratioHist.Draw('PE1')
    canv2.Print('MjjSampleInterference'+plot+'.eps')


    # canv.Print(outputPath+'/%s.eps'%(plot))
    # canv.Print('%s_%s.eps'%(plotdir,plot))
    #prevents memory leak in Canvas Creation/Deletion
    #see: https://root.cern.ch/root/roottalk/roottalk04/2484.html
    gSystem.ProcessEvents()
    del ratiopad,plotpad,canv
    # gc.collect()


if(__name__=='__main__'):
    for plot in ['M_VV_12','M_VV_12_nonequi','M_VV_12_highbin']:
        make_plot(plot)

