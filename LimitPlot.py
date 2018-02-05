from ROOT import gROOT, gStyle, TCanvas, TColor, TF1, TFile, TLegend, THStack,TGraph,TText

if(__name__=="__main__"):
    SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_aQGC_WPWPjj_hadronic.root")
    BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
    

    SHist = SFile.Get("MjjHists_detaAk4sel_allcuts/M_jj_AK8_S0_m40p0")
    BHist = BFile.Get("detaAk4sel_allcuts/M_jj_AK8")
    print SHist
    print BHist


    plottitle = "invariant Mass of AK8 Jets (FS0)"

    canv = TCanvas(plottitle, plottitle, 600, 600)
    canv.SetLogy()

    gStyle.SetOptStat(0)

    legend = TLegend(0.5,0.76,0.9,0.9)

    drawOpt="HE"

    BHist.SetFillColor(867)
    BHist.SetLineColor(867)

    BHist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    BHist.GetXaxis().SetRangeUser(0,7500)

    BHist.GetYaxis().SetTitle('Events')
    BHist.GetYaxis().SetTitleOffset(1.3)
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
    SHist.Draw("SAME"+drawOpt)
    legend.AddEntry(SHist,"W^{+}W^{+}jj (S0=-40TeV^{-4})  ","l")
    
    g=TGraph("test")
    g.SetPoint(0,4750,0.001)
    #g.SetPoint(1,4750,6.42069659951)
    g.SetPoint(1,4750,1000)
    g.Draw("LSAME")

    BText=TText(5000,100,"-> B=10")
    BText.Draw()
    SText=TText(5000,10,"-> S=6.42")
    SText.Draw()

    canv.SetTitle(plottitle)
    legend.Draw()
    canv.Update()
    #canv.Print("~/www/test.png") 
    canv.Print("plots/LimitPlot.eps")
