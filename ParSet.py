from array import array
import csv,collections,numpy
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooCBShape,RooVoigtian,RooBreitWigner,RooFFTConvPdf,RooLandau,RooBifurGauss,RooPolynomial,RooChebychev

gROOT.ProcessLine('.L RooFit/RooLogistics.cxx+')
gROOT.ProcessLine('.L RooFit/RooExpAndGauss.C+')
from ROOT import RooLogistics,RooExpAndGauss

#import myutils,shutil,os
gROOT.Reset()

sets=collections.OrderedDict()

class Set:
    def __init__(self, dim8op,channelname,Cut,jR=8):
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
        self.OpName=dim8op
        self.LastCut=Cut
        self.jetRadius=int(jR)
        gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
        self.SFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root"%self.channel)
        # self.BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
        self.BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
        gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")

        self.SHistNames=[]
        self.SHists=[]
        self.chi2_dict={}
        self.best_n={}
        fillHistNames(self.SHistNames,self.OpName)

        Ranges={"WPWP":"WPWPRange",
            "WPWM":"WPMWMRange",
            "WMWM":"WPWMRange",
            "WPZ":"ZRange",
            "WMZ":"ZRange",
            "ZZ":"ZRange"}


        tmpCut=self.LastCut
        if('_allcuts' in tmpCut):
            tmpCut=tmpCut[:len(tmpCut)-len('_allcuts')]
        
        self.RefHist=self.SFile.Get('%s/M_jj_AK%i'%(self.LastCut,self.jetRadius))

        
        SHistDir=self.SFile.GetDirectory('MjjHists_%s_%s'%(tmpCut,Ranges[self.channel]))
        print 'MjjHists_%s_%s'%(tmpCut,Ranges[self.channel])
        SHistkeys=SHistDir.GetListOfKeys()
        for key in SHistkeys:
            # if(('("M_jj_AK%i")'%self.jetRadius) in str(key)):
            #        self.BHist=key.ReadObj()
            if ( (dim8op not in str(key)) or (('AK%i'%self.jetRadius) not in str(key))): 
                continue
            self.SHists.append(key.ReadObj())

        self.BHist=self.BFile.Get('%s/M_jj_AK%i_highbin'%(self.LastCut,self.jetRadius))
        # self.BHist=self.BFile.Get('nocuts/M_jj_AK%i_highbin'%(self.jetRadius))

        #Rebin Stuff
        boundaries=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]

        self.xbins = array( 'd' )
        for i in range(1,len(boundaries)):
	    self.xbins.append(boundaries[i])


    def RooFitSignal(self,path=''):
        gStyle.SetOptFit(1100)

        gStyle.SetOptTitle(0)
        RooFit.SumW2Error(kTRUE)

        # for i in range(len(self.SHists)):
        for i in [1]:
            hist=self.SHists[i].Rebin(len(self.xbins)-1,"%s_%s_%s"%(self.channel,self.LastCut,self.getPointName(i)),self.xbins)
            hist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
            hist.GetYaxis().SetTitle('Events')

            mjj=RooRealVar('mjj','M_{jj-AK8}',0,14000,'GeV')
            mjjral=RooArgList(mjj)
            sigdh=RooDataHist('sigdh','sigdh',mjjral,RooFit.Import(hist))

            shapes={}
            #CrystalBall
            mean = RooRealVar('#mu','mean',0,5000)
            sigma= RooRealVar('#sigma','sigma',0,5000)
            alpha=RooRealVar('#alpha','Gaussian tail',-10000,0)
            n=RooRealVar('n','Normalization',0,10000)            
            # mean.setConstant(kFALSE)
            # sigma.setConstant(kFALSE)
            # alpha.setConstant(kFALSE)
            # n.setConstant(kFALSE)
            cbshape=RooCBShape('cbshape','crystalball PDF',mjj,mean,sigma,alpha,n)
            shapes.update({'CrystalBall':cbshape})

            #Gaussian
            gaussmean = RooRealVar('#mu_{gauss}','mass mean value',0,5000)
            gausssigma= RooRealVar('#sigma_{gauss}','mass resolution',0,5000)            
            gauss=RooGaussian('gauss','gauss',mjj,gaussmean,gausssigma)
            shapes.update({'Gauss':gauss})

            #Voigt
            voigtmean = RooRealVar('#mu','mass mean value',0,5000)
            voigtwidth = RooRealVar('#gamma','width of voigt',0,5000)
            voigtsigma= RooRealVar('#sigma','mass resolution',0,5000)
            voigt=RooVoigtian('voigt','voigt',mjj,voigtmean,voigtwidth,voigtsigma)
            shapes.update({'Voigt':voigt})
            
            # #BreitWigner
            bwmean = RooRealVar('#mu','mass mean value',3800,0,5000)
            bwwidth = RooRealVar('#sigma','width of bw',1000,0,5000)            
            bw=RooBreitWigner('bw','bw',mjj,bwmean,bwwidth)
            shapes.update({'BreitWigner':bw})

            #Landau
            landaumean=RooRealVar('#mu_{landau}','mean landau',0,5000)
            landausigma= RooRealVar('#sigma_{landau}','mass resolution',0,5000)
            landau=RooLandau('landau','landau',mjj,landaumean,landausigma)
            shapes.update({'Landau':landau})

            #LandauGauss Convolution                        
            landaugauss=RooFFTConvPdf('landaugauss','landau x gauss',mjj,landau,gauss)            
            shapes.update({'LandauGauss':landaugauss})

            mjj.setRange("FitRange",1050.,9000.)
            
            for fname in ['Landau','CrystalBall','LandauGauss']:#,'BreitWigner']:
                plottitle='%sFit %s - %s - %s'%(fname,self.channel,self.OpName,self.getPointName(i))
            
                shape=shapes[fname]
                shape.fitTo(sigdh,RooFit.Range("FitRange"),RooFit.SumW2Error(True))

                frame=mjj.frame(RooFit.Title(plottitle))
                frame.GetYaxis().SetTitleOffset(2)
                #frame.SetName(plottitle)
                sigdh.plotOn(frame,RooFit.MarkerStyle(4))
                shape.plotOn(frame,RooFit.LineColor(2))
                            
                ndof=sigdh.numEntries()-5
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
                # canv.SetLogy()
                canv.SetLeftMargin(0.20) 
                canv.cd()

                frame.Draw()
                   
                canv.Print(path+'/%s_%s_%s_%s.eps'%(self.channel,self.LastCut,self.getPointName(i),fname))

    def RooFitRef(self,path=''):
        gStyle.SetOptFit(1100)

        gStyle.SetOptTitle(0)
        RooFit.SumW2Error(kTRUE)
        
        mjjref=RooRealVar('mjjref','M_{jj-AK8}',0,14000,'GeV')
        mjjralref=RooArgList(mjjref)
        refdh=RooDataHist('refdh','refdh',mjjralref,RooFit.Import(self.RefHist))
        
        shapes={}
        #CrystalBall
        mean = RooRealVar('#mu','mean',0,5000)
        sigma= RooRealVar('#sigma','sigma',0,5000)
        alpha=RooRealVar('#alpha','Gaussian tail',-10000,0)
        n=RooRealVar('n','Normalization',0,10000)            
        cbshape=RooCBShape('cbshape','crystalball PDF',mjjref,mean,sigma,alpha,n)
        shapes.update({'CrystalBall':cbshape})

        #Gaussian
        gaussmean = RooRealVar('#mu_{gauss}','mass mean value',0,5000)
        gausssigma= RooRealVar('#sigma_{gauss}','mass resolution',0,5000)            
        gauss=RooGaussian('gauss','gauss',mjjref,gaussmean,gausssigma)
        shapes.update({'Gauss':gauss})
            
        #Voigt
        voigtmean = RooRealVar('#mu','mass mean value',0,5000)
        voigtwidth = RooRealVar('#gamma','width of voigt',0,5000)
        voigtsigma= RooRealVar('#sigma','mass resolution',0,5000)
        voigt=RooVoigtian('voigt','voigt',mjjref,voigtmean,voigtwidth,voigtsigma)
        shapes.update({'Voigt':voigt})
            
        #BreitWigner
        bwmean = RooRealVar('#mu','mass mean value',3800,0,5000)
        bwwidth = RooRealVar('#sigma','width of bw',1000,0,5000)            
        bw=RooBreitWigner('bw','bw',mjjref,bwmean,bwwidth)
        shapes.update({'BreitWigner':bw})

        #Landau
        landaumean=RooRealVar('#mu_{landau}','mean landau',0,5000)
        landausigma= RooRealVar('#sigma_{landau}','mass resolution',0,5000)
        landau=RooLandau('landau','landau',mjjref,landaumean,landausigma)
        shapes.update({'Landau':landau})

        #LandauGauss Convolution                        
        landaugauss=RooFFTConvPdf('landaugauss','landau x gauss',mjjref,landau,gauss)            
        shapes.update({'LandauGauss':landaugauss})

        #Logistics
        logisticsmean=RooRealVar('#mu_{logistics}','mean logistics',0,5000)
        logisticssigma= RooRealVar('#sigma_{logistics}','mass resolution',0,5000)
        logistics=RooLogistics('logistics','logistics',mjjref,logisticsmean,logisticssigma)
        shapes.update({'Logistics':logistics})

        #ExpAndGauss
        expgaussmean=RooRealVar('#mu_{expgauss}','mean expgauss',0,5000)
        expgausssigma= RooRealVar('#sigma_{expgauss}','mass resolution',0,5000)
        expgausstrans= RooRealVar('trans','trans',0,100)
        expgauss=RooExpAndGauss('expgauss','expgauss',mjjref,expgaussmean,expgausssigma,expgausstrans)
        shapes.update({'ExpAndGauss':expgauss})

        #BifurGauss
        BifurGaussmean=RooRealVar('#mu_{BifurGauss}','mean BifurGauss',0,5000)
        BifurGausslsigma= RooRealVar('#sigma_{left}','mass resolution',0,5000)
        BifurGaussrsigma= RooRealVar('#sigma_{right}','mass resolution',0,5000)
        BifurGauss=RooBifurGauss('BifurGauss','BifurGauss',mjjref,BifurGaussmean,BifurGausslsigma,BifurGaussrsigma)
        shapes.update({'BifurGauss':BifurGauss})

        #Chebychev
        Chebychev1=RooRealVar('c0','Chebychev0',-1000,1000)
        Chebychev2= RooRealVar('c1','Chebychev1',-1000,1000)        
        Chebychev3= RooRealVar('c2','Chebychev2',2,-1000,1000)        
        Chebychev=RooChebychev('Chebychev','Chebychev',mjjref,RooArgList(Chebychev1,Chebychev2,Chebychev3))
        shapes.update({'Chebychev':Chebychev})

        #Polynomial
        Polynomial1=RooRealVar('Polynomial1','Polynomial1',100,0,1000)
        Polynomial2= RooRealVar('Polynomial2','Polynomial2',100,0,1000)
        Polynomial=RooPolynomial('Polynomial','Polynomial',mjjref,RooArgList(Polynomial1,Polynomial2))
        shapes.update({'Polynomial':Polynomial})

        mjjref.setRange("FitRange",1050.,9000.)
            
        for fname in ['Landau','Logistics','LandauGauss','ExpAndGauss','BifurGauss','Chebychev','Polynomial']:#,'BreitWigner']:
            plottitleref='%sFit %s - %s - refpoint'%(fname,self.channel,self.OpName)

            #Same for refPlot
            shaperef=shapes[fname]
            shaperef.fitTo(refdh,RooFit.Range("FitRange"),RooFit.SumW2Error(True))

            frameref=mjjref.frame(RooFit.Title(plottitleref))
            frameref.GetYaxis().SetTitleOffset(2)
            refdh.plotOn(frameref,RooFit.MarkerStyle(4))
            shaperef.plotOn(frameref,RooFit.LineColor(2))
                            
            ndofref=refdh.numEntries()-5
            #chiSquare legend
            chi2ref = frameref.chiSquare()
            probChi2ref = TMath.Prob(chi2ref*ndofref, ndofref)
            chi2ref = round(chi2ref,2)
            probChi2ref = round(probChi2ref,2)
            legref = TLegend(0.5,0.5,0.9,0.65)
            legref.SetBorderSize(0)
            legref.SetFillStyle(0)
            shaperef.paramOn(frameref, RooFit.Layout(0.5,0.9,0.9))
            legref.AddEntry(0,'#chi^{2} ='+str(chi2ref),'')
            legref.AddEntry(0,'Prob #chi^{2} = '+str(probChi2ref),'')
            legref.SetTextSize(0.04)
            frameref.addObject(legref)

            canvref=TCanvas(plottitleref,plottitleref,700,700)
            # canv.SetLogy()
            canvref.SetLeftMargin(0.20) 
            canvref.cd()

            frameref.Draw()
                
            # myaxis=rescale_frame(canvref,frameref,0.2,'Events/(137.225 GeV)')
            
            canvref.Print(path+'/%s_%s_%s_refpoint_%s.eps'%(self.channel,self.OpName,self.LastCut,fname))


            
            # hold=raw_input('Press Enter to continue...')
            
    def FitSignal(self,path=''):


        gStyle.SetOptFit(1100)

        gStyle.SetOptTitle(0)
        best_chi=100
        best_order=-1

        for i in range(1):
            for n in [-3,-2,-1,4,6]:
            # for n in range(-2,14):
                hist=self.SHists[i].Rebin(len(self.xbins)-1,"fit parameter",self.xbins)
                print len(self.xbins)
                plottitle='FitPlot %s - %s - %s - n:%i'%(self.channel,self.OpName,self.getPointName(i),n)
            
                canv=TCanvas(plottitle,plottitle,600,600)
                canv.SetLogy()
            
                hist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
                hist.GetYaxis().SetTitle('Events')
                hist.GetYaxis().SetTitleOffset(1.3)
                
                hist.Draw('HE1')

            #ploynom of nth degree
            #n=4
                #f(x) = p0*exp(-0.5*((x-p1)/p2)^2)). 
                fgaus='[0]*TMath::Gaus(x,[1],[2])'
                # fgaus='[0]*TMath::Exp(-0.5*TMath::Power((x-[1])/[2],2))'

                fpoln='[0]'
                fpolns=fpoln
                for j in range(1,n+1):
                    fpoln=fpoln+'+[%i]*x**%i'%(j,j)
                    fpolns=fpoln+'+(1/(x-14000))**[10]'
                
                # fpolgaus='[7]*(%s)'%fgaus+'+(1-[7])*([3]'

                #fpolgaus='[0]*([1]*TMath::Exp(-0.5*TMath::Power((x-[2])/[3],2)))+(1-[0]) * ( [4] + [5]*TMath::Power(x,1) + [6]*TMath::Power(x,2) + [7]*TMath::Power(x,3) + [8]*TMath::Power(x,4) + [9]*TMath::Power(x,5) + [10]*TMath::Power(x,6))'
                

                fvoigt='[0] * TMath::Voigt(x-[1],[2],[3], 4)'
                
                f3gaus='[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Gaus(x,[4],[5])'#+[6]*TMath::Gaus(x,[7],[8])'
                fpoisson='[0]*TMath::Poisson(x,[1])'
                if(n==-3):
                    fitfunc=TF1('fitfunc',fvoigt,1050,14000)
                    fitfunc.SetParameters(3e6,2500,1300,2e-14)
                    fitfunc.SetParLimits(0,0,10e7)
                    fitfunc.SetParLimits(1,0,10e7)
                    fitfunc.SetParLimits(2,0,10e7)
                    fitfunc.SetParLimits(3,0,10e7)
                    
                if(n==-2):
                    fitfunc=TF1('fitfunc',f3gaus,1050,14000)
                    fitfunc.SetParameters(4.37231e+02,3.78768e+03, 8.96384e+02, 1.41513e+03, 2.09320e+03,6.11704e+02)                        
                    # fitfunc.SetParameters(1000,2600,1500,1.5e-3,-2.3e5,0,0,0.14)                        
                elif(n==-1):
                    fitfunc=TF1('fitfunc',fgaus,1050,14000)
                    fitfunc.SetParameters(500,3500,1000)
                    # fitfunc.SetParameters(1,1,1)
                else:
                    fitfunc=TF1('fitfunc',fpoln,1050,14000)
                    # fitfunc.SetParameters(1,1,1,1,1,1,1,1,1,1,1)
                    # fitfunc.SetParameters(-70,-2e-1,5e-5,-5e-7,2e-10,-8e-14,2e-17,-2e-21,1.5e-25,-4e-30,0) # n=9


                # fitfunc=TF1('fitfunc',fpolns,1050,14000)


            # poisson=TF1('poisson','[0]*TMath::Power(([1]/[2]),(x/[2]))*(TMath::Exp( ([1]/[2])))/TMath::Gamma((x/[2])+1)',1050,14000);
                    
                hist.Fit(fitfunc)
                
                fit= hist.GetFunction("fitfunc");
                chi2 = fit.GetChisquare();
                ndf = fit.GetNDF()
                self.chi2_dict.update({n:'%8.4f'%(chi2/ndf)})
                print 'chi2',chi2,'/ndf',ndf,'-->',chi2/ndf
                if(chi2/ndf < best_chi):
                    best_chi=chi2/ndf
                    best_order=n
                canv.Print(path+'/FitPlot_%s_%s_%s_%s_n%i.eps'%(self.channel,self.LastCut,self.OpName,self.getPointName(i),n))
            print "best chi2/ndf:", best_chi,' @ n=',best_order
            self.best_n.update({self.LastCut:(best_order,best_chi)})
        # test=raw_input('Press Enter to continue...'
            




        
    def exportPlot(self,logY=True,path="./output/plots",rebin=True):

        plottitle="invariant Mass of AK%i Jets (%s-Operator) in %s - %s"%(self.jetRadius,self.OpName,self.channel,self.LastCut)
        canv = TCanvas(plottitle,plottitle,600,600)
        
        #turning off the standard Statistic-Box
        gStyle.SetOptStat(0)

        legend = TLegend(0.5,0.7,0.9,0.9)
        
        drawOptions="HE"
        if(logY):
            canv.SetLogy()
            
        stack=THStack(plottitle,plottitle)
            
        if(rebin):
            BGHist=self.BHist.Rebin(len(self.xbins)-1,"new binning",self.xbins)
        else:
            BGHist=self.BHist

        #Cosmetics:
        BGHist.SetFillColor(867)
        BGHist.SetLineColor(867)
        
        BGHist.SetTitle(plottitle)
        BGHist.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
        BGHist.GetYaxis().SetTitle('Events')
        BGHist.GetXaxis().SetRangeUser(0,7500)
        # BGHist.GetYaxis().SetRangeUser(10**(-3),10**5)
        BGHist.GetYaxis().SetTitleOffset(1.3)

        legend.AddEntry(BGHist,"QCD","f")
        # BGHist.Draw(""+drawOptions)

        stack=THStack('stack',plottitle)

        stack.Add(BGHist)

        histcounter=1
        
        #number of Parameters to plot:        
        n=6
        med=(sets[self.OpName][0]-1)/2 -1

        for i in range(n):
            index= i * med/n
            if(rebin):
                hist=self.SHists[index].Rebin(len(self.xbins)-1,"new binning",self.xbins)
            else:
                hist=self.SHists[index]
            hist.SetLineColor(histcounter)
            # hist.Draw("SAME"+drawOptions)
            stack.Add(hist)
            legend.AddEntry(hist,"%sjj (%s=%.1fTeV^{-4})"%(self.channel,self.OpName,self.getPoint(index)))
            histcounter+=1
        canv.SetTitle(plottitle)
        stack.Draw('nostack'+drawOptions)
        legend.Draw()        
        canv.Update()
        canv.Print("%s/%s_AK%i_%s.eps"%(path,self.channel,self.jetRadius,self.OpName))
        del stack

    def calcLimits(self,plot=False,path="./output/plots"):
        if(self.jetRadius!=8):
            print 'to calculate estimates of Limits use AK8 Jets!'
            return -1

        Nbins = self.BHist.GetNbinsX()
        bin=0
        BSum=0
        SSums=[]
        for hist in self.SHists:
            SSums.append(0)
        for i in list(reversed(range(Nbins))):
            if(BSum>=10):
                break
            if(i==8183):
                continue
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
            expectedLimit_S=7.5938 #for B=10.1607131213
        elif(self.LastCut=='invMAk4sel_1p5_allcuts'):
            expectedLimit_S=7.7188 #for B=10.6225637197
        elif(self.LastCut=='invMAk4sel_2p0_allcuts'):
            expectedLimit_S=7.5312 #for B=10.0067629367
        else:
            expectedLimit_S=1000 


        for i in range(0,len(SSums)):           
            if(lower_limit_index==-1):
                if( SSums[i]<=expectedLimit_S):
                    lower_limit_index=i
            elif(upper_limit_index==-1):
                if( SSums[i]>=expectedLimit_S):
                    upper_limit_index=i-1

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
        if(plot):
            plot1.Print('%s/SPlot_%s_%s_%s.eps'%(path,self.channel,self.OpName,self.LastCut))
        

    def getPoint(self,i):
        return sets[self.OpName][1]+i*sets[self.OpName][2]
        
    def getPointName(self,i):
        name="M_jj_AK8_%s_"%self.OpName

        parameter=100*sets[self.OpName][1]+i*100*sets[self.OpName][2]
        if(parameter>=0):
            name+="%ip%i"%(parameter/100,parameter%100)
        else:
            name+="m%ip%i"%(-parameter/100,-parameter%100)
        return name
        

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


def rescale_frame(canvas, frame, scale, title):
    """
    HACK
    Takes a frame and rescales it to arbitrary coordinates. 
    This is helpful when dealing with RooPlot to get the axes
    correct.  Returns axis in case anything else needs to be done.
    """
    import ROOT
    yaxis = frame.GetYaxis()
    yaxis.SetTickLength(0)
    yaxis.SetNdivisions(0)
    yaxis.SetLabelSize(0)
    yaxis.SetTitle("")
    yaxis.SetLabelColor(10)
    yaxis.SetAxisColor(10)
    frame.Draw()
    canvas.Update()
    amax = frame.GetMaximum()
    amin = frame.GetMinimum()
    new_max = amax*scale
    new_min = amin*scale
    x = canvas.PadtoX
    y = canvas.PadtoY
    
    axis = ROOT.TGaxis(x(canvas.GetUxmin()), y(canvas.GetUymin()),
                       x(canvas.GetUxmin()), y(canvas.GetUymax()),
                       new_min,new_max,510,"")
    axis.SetTitle(title)
    axis.Draw()
    canvas.Update()
    return axis
