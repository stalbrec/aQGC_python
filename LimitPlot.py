from ROOT import gROOT, gStyle, TCanvas, TColor, TF1, TFile, TLegend, THStack,TGraph,TText,TLatex,kTRUE
from array import array


gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTitleOffset(1.4,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.08)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)


if(__name__=="__main__"):
    SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/parameterscan/uhh2.AnalysisModuleRunner.MC.MC_aQGC_ZZjj_hadronic.root")
    BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/parameterscan/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")

    #rebin stuff

    boundaries=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383,1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808,7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
    dijetbinning = array( 'd' )
    for i in range(1,len(boundaries)):
        dijetbinning.append(boundaries[i]) 
    
    #ZZ 
    #S(S0=-80)=7.30636672491
    #(B=10.0067629665)
    #S has to be 7.5312
    #S0 -> -81.17

    #BinCenter 1376.5
    #S(S=-0.54)=7.91794830631
    #T1->-0.53


    mjj_interest=1376.5

    # SHist = SFile.Get("MjjHists_invMAk4sel_1p0_ZRange/M_jj_AK8_S0_m40p0").Rebin(len(dijetbinning)-1,"new binning",dijetbinning)
    # BHist = BFile.Get("invMAk4sel_1p0/M_jj_AK8_highbin").Rebin(len(dijetbinning)-1,"new binning",dijetbinning)
    # print SHist
    # print BHist

    SHist = SFile.Get("MjjHists_invMAk4sel_1p0/M_jj_AK8_T1_m0p54").Rebin(len(dijetbinning)-1,"new binning",dijetbinning)
    BHist = BFile.Get("invMAk4sel_1p0/M_jj_AK8_highbin").Rebin(len(dijetbinning)-1,"new binning",dijetbinning)
    print SHist
    print BHist


    plottitle = "invariant Mass of AK8 Jets (FT1)"

    canv = TCanvas(plottitle, plottitle, 600, 600)
    canv.SetLogy()


    legend = TLegend(0.5,0.76,0.9,0.9)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)

    drawOpt="HE"

    BHist.SetFillColor(867)
    BHist.SetLineColor(867)

    BHist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    BHist.GetXaxis().SetRangeUser(0,7500)

    BHist.GetYaxis().SetTitle('Events')
    BHist.GetYaxis().SetTitleOffset(1.5)
    BHist.GetYaxis().SetRangeUser(10**(-3),10**5)
 
    BHist.Draw(""+drawOpt)
    legend.AddEntry(BHist,"QCD","f")

    # stack = THStack("qcdstack",plottitle)
    # stack.Add(BHist)
    # stack.Draw(""+drawOpt)

    # stack.GetXaxis().SetLimits(0,7500)
    # stack.GetYaxis().SetRangeUser(10**(-3),10**5)
    #stack.Draw(""+drawOpt)
    #legend.AddEntry(stack,"QCD","l")
        
    SHist.SetLineColor(1)
    SHist.SetLineWidth(2)
    SHist.Draw("SAME"+drawOpt)
    legend.AddEntry(SHist,"ZZjj (F_{T1}=-0.54TeV^{-4})  ","l")


    latex=TLatex()
    latex.SetTextSize(0.04)

    latex.SetNDC(kTRUE)
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.24,0.87,"private work")    

    # latex.SetNDC(kFALSE)
    # latex.DrawLatex(mjj_interest+300,100,"#rightarrow B=10")
    # # latex.DrawLatex(mjj_interest+300,10,"#rightarrow S=7.31")

    
    # g=TGraph("test")
    # g.SetPoint(0,mjj_interest,0.001)
    # #g.SetPoint(1,4750,6.42069659951)
    # g.SetPoint(1,mjj_interest,1000)
    # g.Draw("LSAME")
    

    canv.SetTitle(plottitle)
    legend.Draw()
    canv.Update()
    canv.Print("output/plots/LimitPlot.eps")
