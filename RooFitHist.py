from array import array
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TH1F,TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooCBShape,RooVoigtian,RooBreitWigner,RooFFTConvPdf,RooLandau,RooBifurGauss,RooPolynomial,RooChebychev

gROOT.ProcessLine('.L RooFit/RooLogistics.cxx+')
gROOT.ProcessLine('.L RooFit/RooExpAndGauss.C+')
from ROOT import RooLogistics,RooExpAndGauss


def RooFitHist(inputhist,title='title',path='.'):
    RooFit.gErrorIgnoreLevel = RooFit.kInfo
    fitbinning=array('d')
    binwidth=100
    #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
    NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
    for i in range(NBins+1):
        fitbinning.append(1050+i*binwidth)
    # print fitbinning

    hist=inputhist.Rebin(NBins,"fit parameter",fitbinning)

    meanstart=hist.GetBinCenter(hist.GetMaximumBin())
    sigmastart=hist.GetRMS()
    print 'meanstart:',meanstart,'sigmastart:',sigmastart

    
    # inputhist.Draw()  
    # hist.Draw()
    
    # hold=raw_input('press enter to exit.')

    gStyle.SetOptFit(1100)

    gStyle.SetOptTitle(0)
    RooFit.SumW2Error(kTRUE)
    
    mjj=RooRealVar('mjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
    mjjral=RooArgList(mjj)
    dh=RooDataHist('dh','dh',mjjral,RooFit.Import(hist))
    
    shapes={}

        #Gaussian
    gaussmean = RooRealVar('#mu_{gauss}','mass mean value',meanstart,0,2*meanstart)
    gausssigma= RooRealVar('#sigma_{gauss}','mass resolution',sigmastart,0,2*sigmastart)            
    gauss=RooGaussian('gauss','gauss',mjj,gaussmean,gausssigma)
    shapes.update({'Gauss':gauss})

        #CrystalBall
    mean = RooRealVar('#mu','mean',meanstart,0,2*meanstart)
    sigma= RooRealVar('#sigma','sigma',sigmastart,0,2*sigmastart)
    alpha=RooRealVar('#alpha','Gaussian tail',-1000,0)
    n=RooRealVar('n','Normalization',-1000,1000)            
    cbshape=RooCBShape('cbshape','crystalball PDF',mjj,mean,sigma,alpha,n)
    shapes.update({'CrystalBall':cbshape})
    
        #Voigt
    voigtmean = RooRealVar('#mu','mass mean value',meanstart,0,2*meanstart)
    voigtwidth = RooRealVar('#gamma','width of voigt',0,5000)
    voigtsigma= RooRealVar('#sigma','mass resolution',sigmastart,0,2*sigmastart)
    voigt=RooVoigtian('voigt','voigt',mjj,voigtmean,voigtwidth,voigtsigma)
    shapes.update({'Voigt':voigt})
    
        #BreitWigner
    bwmean = RooRealVar('#mu','mass mean value',meanstart,0,2*meanstart)
    bwwidth = RooRealVar('#sigma','width of bw',sigmastart,0,2*sigmastart)            
    bw=RooBreitWigner('bw','bw',mjj,bwmean,bwwidth)
    shapes.update({'BreitWigner':bw})

        #Landau
    landaumean=RooRealVar('#mu_{landau}','mean landau',meanstart,0,2*meanstart)
    landausigma= RooRealVar('#sigma_{landau}','mass resolution',sigmastart,0,2*sigmastart)
    landau=RooLandau('landau','landau',mjj,landaumean,landausigma)
    shapes.update({'Landau':landau})

        #LandauGauss Convolution                        
    landaugauss=RooFFTConvPdf('landaugauss','landau x gauss',mjj,landau,gauss)            
    shapes.update({'LandauGauss':landaugauss})

        #Logistics
    logisticsmean=RooRealVar('#mu_{logistics}','mean logistics',meanstart,0,2*meanstart)
    logisticssigma= RooRealVar('#sigma_{logistics}','mass resolution',sigmastart,0,2*sigmastart)
    logistics=RooLogistics('logistics','logistics',mjj,logisticsmean,logisticssigma)
    shapes.update({'Logistics':logistics})

        #ExpAndGauss
    expgaussmean=RooRealVar('#mu_{expgauss}','mean expgauss',meanstart,0,2*meanstart)
    expgausssigma= RooRealVar('#sigma_{expgauss}','mass resolution',sigmastart,0,2*sigmastart)
    expgausstrans= RooRealVar('trans','trans',0,100)
    expgauss=RooExpAndGauss('expgauss','expgauss',mjj,expgaussmean,expgausssigma,expgausstrans)
    shapes.update({'ExpAndGauss':expgauss})

        #BifurGauss
    BifurGaussmean=RooRealVar('#mu_{BifurGauss}','mean BifurGauss',meanstart,0,2*meanstart)
    BifurGausslsigma= RooRealVar('#sigma_{left}','mass resolution',sigmastart,0,2*sigmastart)
    BifurGaussrsigma= RooRealVar('#sigma_{right}','mass resolution',sigmastart,0,2*sigmastart)
    BifurGauss=RooBifurGauss('BifurGauss','BifurGauss',mjj,BifurGaussmean,BifurGausslsigma,BifurGaussrsigma)
    shapes.update({'BifurGauss':BifurGauss})

        #Chebychev
    Chebychev1=RooRealVar('c0','Chebychev0',-1000,1000)
    Chebychev2= RooRealVar('c1','Chebychev1',-1000,1000)        
    Chebychev3= RooRealVar('c2','Chebychev2',2,-1000,1000)        
    Chebychev=RooChebychev('Chebychev','Chebychev',mjj,RooArgList(Chebychev1,Chebychev2,Chebychev3))
    shapes.update({'Chebychev':Chebychev})

        #Polynomial
    Polynomial1=RooRealVar('Polynomial1','Polynomial1',100,0,1000)
    Polynomial2= RooRealVar('Polynomial2','Polynomial2',100,0,1000)
    Polynomial=RooPolynomial('Polynomial','Polynomial',mjj,RooArgList(Polynomial1,Polynomial2))
    shapes.update({'Polynomial':Polynomial})

        # mjj.setRange("FitRange",1050.,14000.)
            
    for fname in ['Gauss','Logistics','BifurGauss']:       

        plottitle='%s Fit of %s'%(fname,title)
        shape=shapes[fname]
        # shape.fitTo(dh,RooFit.Range("FitRange"),RooFit.SumW2Error(True))
        shape.fitTo(dh,RooFit.SumW2Error(True))
            
        frame=mjj.frame(RooFit.Title(plottitle))
        frame.GetYaxis().SetTitleOffset(2)

        dh.plotOn(frame,RooFit.MarkerStyle(4))
        shape.plotOn(frame,RooFit.LineColor(2))
        
        ndof=dh.numEntries()-5

        #chiSquare legend
        chi2 = frame.chiSquare()
        probChi2 = TMath.Prob(chi2*ndof, ndof)
        chi2 = round(chi2,2)
        probChi2 = round(probChi2,2)
        leg = TLegend(0.5,0.5,0.9,0.65)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        shape.paramOn(frame, RooFit.Layout(0.5,0.9,0.9))
        leg.AddEntry(0,'#chi^{2} ='+str(chi2),'')
        leg.AddEntry(0,'Prob #chi^{2} = '+str(probChi2),'')
        leg.SetTextSize(0.04)
        frame.addObject(leg)

        canv=TCanvas(plottitle,plottitle,700,700)
        canv.SetLogy()
        canv.SetLeftMargin(0.20) 
        canv.cd()

        frame.SetMinimum(10**(-3))

        frame.Draw()
        canv.Print(path+'/%s__%s.eps'%(title,fname))
