import os,sys,glob,math
from array import array
from ROOT import TFile, TH1F,gROOT,gStyle,TCanvas,TGraph,TProfile,TLegend,TF1,TLatex,TLine,TPad,gPad,TObject,TGraphAsymmErrors
import ROOT as rt
from PointName import getPointNameI
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTextFont(43)

gStyle.SetTitleOffset(0.96,"X")
gStyle.SetTitleOffset(.6,"Y")
# gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadLeftMargin(0.1)
# gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadTopMargin(0.08)
# gStyle.SetPadRightMargin(0.08)
gStyle.SetPadRightMargin(0.1)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.06, "XYZ")
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

    legnames=['#mu_{r}=1,   #mu_{F}=1',  #0
              '#mu_{r}=1,   #mu_{F}=2',  #1
              '#mu_{r}=1,   #mu_{F}=0.5',#2
              '#mu_{r}=2,   #mu_{F}=1',  #3
              '#mu_{r}=2,   #mu_{F}=2',  #4
              '#mu_{r}=2,   #mu_{F}=0.5',#5 Do not use!
              '#mu_{r}=0.5, #mu_{F}=1',  #6
              '#mu_{r}=0.5, #mu_{F}=2',  #7
              '#mu_{r}=0.5, #mu_{F}=0.5' #8 Do not use!
    ]
    
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
    pdf4lhcHistDir=f.GetDirectory('UncertaintiesHists_invMAk4sel_1p0')
    pdf4lhcHistKeys=pdf4lhcHistDir.GetListOfKeys()
    scaleHists=[]
    for key in pdf4lhcHistKeys:
        OrigHist=key.ReadObj()
        if('scale' not in OrigHist.GetName()):
            continue
        RebinHist=OrigHist.Rebin(NBins,OrigHist.GetName(),binning)
        
        scaleHists.append(RebinHist)

    NBins=scaleHists[0].GetNbinsX()
    envelope=TGraphAsymmErrors(NBins)
    # indices=[1,2,3,4,6,8]
    indices=[1,4,2,8,3,6]
    for i in range(NBins):
        VariationMin=10**(10)
        VariationMinHist=0
        VariationMax=-10**(10)
        VariationMaxHist=0
        for j in indices:
            CurrentBinContent=scaleHists[j].GetBinContent(i)
            if( CurrentBinContent < VariationMin):
                VariationMin=CurrentBinContent
                VariationMinHist=j
            if( CurrentBinContent > VariationMax):
                VariationMax=CurrentBinContent
                VariationMaxHist=j
        x=scaleHists[0].GetBinCenter(i)
        y=scaleHists[0].GetBinContent(i)
        binwidth=scaleHists[0].GetBinWidth(i)
        envelope.SetPoint(i,x,y)
        envelope.SetPointError(i,binwidth/2,binwidth/2,y-VariationMin,VariationMax-y)

    canv=TCanvas('test','test',600,600)
    yplot=0.7
    yratio=0.3
    ymax=1.0
    xmax=1.0
    xmin=0.0

    plotpad=TPad("plotpad","Plot",xmin,ymax-yplot,xmax,ymax)
    ratiopad=TPad("ratiopad","Ratio",xmin,ymax-yplot-yratio,xmax,ymax-yplot)

    plotpad.SetTopMargin(0.08)
    plotpad.SetLeftMargin(0.1)
    plotpad.SetRightMargin(0.05)
    plotpad.SetTicks()
    plotpad.SetBottomMargin(0.016)
    ratiopad.SetTopMargin(0.016)
    ratiopad.SetBottomMargin(0.35)
    ratiopad.SetLeftMargin(0.1)
    ratiopad.SetRightMargin(0.05)
    ratiopad.SetTicks()
    plotpad.Draw()
    ratiopad.Draw()
    plotpad.cd()

    leg = TLegend(0.55,0.66,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    # canv.SetLogy()
    # plotpad.SetLogy()
    envelope.SetMarkerStyle(21)
    envelope.SetMarkerSize(1)
    envelope.Draw('ape1')
    envelope.GetXaxis().SetTitleSize(0.0)
    envelope.GetXaxis().SetLabelSize(0.0)
    envelope.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    envelope.GetXaxis().SetRangeUser(0,9000)
    envelope.GetYaxis().SetTitle('Events')
    # envelope.GetYaxis().SetRangeUser(10**(-3),10**2)
    # leg.AddEntry(envelope,'%s'%scaleHists[0].GetName(),'lep')
    leg.AddEntry(envelope,'%s'%legnames[0],'lep')
    k=1

    colors=[rt.kRed,rt.kRed+2,rt.kBlue,rt.kBlue-2,rt.kOrange,rt.kOrange+2]
    
    for o in range(len(indices)):
        l=indices[o]
        scaleHists[l].SetLineColor(colors[o])
        # scaleHists[l].SetLineWidth(k)
        print scaleHists[l].GetName()
        if((o-1)%2==0):
            scaleHists[l].SetLineStyle(rt.kDashed)
            scaleHists[l].SetLineWidth(2)            
            k+=1
        scaleHists[l].Draw('histSAME')
        # leg.AddEntry(scaleHists[l],'%s'%scaleHists[l].GetName(),'l')
        leg.AddEntry(scaleHists[l],'%s'%legnames[l],'l')

    # envelope.Draw('ape1same')

    plotpad.RedrawAxis()
    ratiopad.cd()
    ratiopad.SetGrid()

    ratioHist=scaleHists[0].Clone()
    ratioHist1=scaleHists[0].Clone()
    for i in range(ratioHist.GetNbinsX()):
        ratioHist.SetBinContent(i,envelope.GetErrorYhigh(i))
        ratioHist1.SetBinContent(i,envelope.GetErrorYlow(i))
    ratioHist.Divide(scaleHists[0])
    ratioHist1.Divide(scaleHists[0])
    for i in range(ratioHist.GetNbinsX()):
        ratioHist.SetBinError(i,0)
        ratioHist1.SetBinError(i,0)

    ratioHist.SetLineColor(rt.kBlack)
    ratioHist.SetMarkerColor(rt.kBlack)
    ratioHist.SetStats(0)
    ratioHist.SetMarkerStyle(21)
    ratioHist.SetMarkerSize(0.7)   
    ratioHist1.SetLineColor(13)
    ratioHist.SetMarkerColor(13)
    ratioHist1.SetStats(0)
    ratioHist1.SetMarkerStyle(21)
    ratioHist1.SetMarkerSize(0.7)   
    #Yaxis
    ratioHist.GetYaxis().SetRangeUser(0.0,1.0)
    ratioHist.GetYaxis().SetTitle("error/nom.")
    ratioHist.GetYaxis().CenterTitle()
    ratioHist.GetYaxis().SetTitleFont(43)
    # ratioHist.GetYaxis().SetTitleSize(yTitleSize)
    ratioHist.GetYaxis().SetTitleSize(18.)
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

    rleg = TLegend(0.6,0.6,0.9,0.9)
    rleg.SetBorderSize(0)
    rleg.SetFillStyle(0)
    rleg.AddEntry(ratioHist,'errorHigh/nominal','ep')
    rleg.AddEntry(ratioHist1,'errorLow/nominal','ep')
    ratioHist.Draw("ep")
    ratioHist1.Draw("epsame")
    rleg.Draw('same')

    ratioXMin=ratioHist.GetXaxis().GetXmin()
    ratioXMax=ratioHist.GetXaxis().GetXmax()

    zeropercent=TLine(ratioXMin,1,ratioXMax,1)
    zeropercent.Draw()
    # plus10percent=TLine(ratioXMin,1.1,ratioXMax,1.1)
    # plus10percent.SetLineStyle(rt.kDashed)
    # plus10percent.Draw()
    # minus10percent=TLine(ratioXMin,0.9,ratioXMax,0.9)
    # minus10percent.SetLineStyle(rt.kDashed)
    # minus10percent.Draw()

    canv.cd()
    gPad.RedrawAxis()
    leg.Draw('SAME')

    canv.Print('qcdscale_envelope.eps')
