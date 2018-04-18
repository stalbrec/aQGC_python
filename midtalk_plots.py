from plotter import plotter


if(__name__=='__main__'):
    
    #plots=[('rootdir','histname','XaxisTitle',logY),...]
    channel='VV'

    # plots=[#('AK8_softdropAK8sel','tau21','#tau_{2}/#tau_{1}',True,[channel]),
    #        # ('detaAk8sel','M_softdrop_1','M_{SD, leading AK8} [GeV/c^{2}]',True,[channel]),
    #        ('nocuts','pT_AK8_1','p_{T}^{leading AK8} [GeV/c]',True,[channel],True),
    #        ('nocuts','pT_AK4_1','p_{T}^{leading AK4} [GeV/c]',True,[channel],True),
    #        ('nocuts','eta_AK8_1','#eta^{leading AK8}',False,[channel],True),
    #        ('nocuts','eta_AK4_1','#eta^{leading AK4}',False,[channel],True),
    #        ('nocuts','M_jj_AK8','M_{jj-AK8} [GeV/c^{2}]',True,[channel],True),
    #        ('nocuts','M_jj_AK4','M_{jj-AK4} [GeV/c^{2}]',True,[channel],True)
    #        ]
    plots=[
           # #Cleaner 
           # ('cleaner','N_pv','N_{PV}',True,[channel],True,0),
           # ('AK8_cleaner','pt','p_{T}^{AK8-jet}',True,[channel],True,0),
           # ('AK8_cleaner','eta','#eta^{AK8-jet}',False,[channel],True,10**2), 
           # ('AK8_cleaner','tau21','#tau_{2}/#tau_{1}',True,[channel],True,0), 
           # ('AK4_cleaner','pt_jet','p_{T}^{AK4-jet}',True,[channel],True,0),
           # ('AK4_cleaner','eta_jet','#eta^{AK4-jet}',False,[channel],True,10**2),
           # ('cleaner','M_jj_AK8','M_{jj-AK8}',True,[channel],True,0),
           # ('cleaner','pT_AK8','p_{T}^{two leading AK8}',True,[channel],True,0),
           # ('cleaner','eta_AK8','#eta^{two leading AK8}',False,[channel],True,10**2),
           # ('cleaner','M_jj_AK4','M_{jj-AK4}',True,[channel],True,0),
           # ('cleaner','pT_AK4','p_{T}^{two leading AK4}',True,[channel],True,0),
           # ('cleaner','eta_AK4','#eta^{two leading AK4}',False,[channel],True,10**2),
           # ('cleaner','M_softdrop_12','M_{SD}^{two leading AK8}',True,[channel],True,0),           
           # VV
           ('tau21sel','N_pv','N_{PV}',True,[channel],True,0),
           ('AK8_tau21sel','pt','p_{T}^{AK8-jet}',True,[channel],True,0),
           ('AK8_tau21sel','eta','#eta^{AK8-jet}',True,[channel],True,0), 
           ('AK8_tau21sel','tau21','#tau_{2}/#tau_{1}',True,[channel],True,0), 
           ('AK4_tau21sel','pt_jet','p_{T}^{AK4-jet}',True,[channel],True,0),
           ('AK4_tau21sel','eta_jet','#eta^{AK4-jet}',True,[channel],True,0),
           ('tau21sel','M_jj_AK8','M_{jj-AK8}',True,[channel],True,0),
           ('tau21sel','pT_AK8','p_{T}^{two leading AK8}',True,[channel],True,0),
           ('tau21sel','eta_AK8','#eta^{two leading AK8}',True,[channel],True,0),
           ('tau21sel','M_jj_AK4','M_{jj-AK4}',True,[channel],True,0),
           ('tau21sel','pT_AK4','p_{T}^{two leading AK4}',True,[channel],True,0),
           ('tau21sel','eta_AK4','#eta^{two leading AK4}',True,[channel],True,0),
           ('tau21sel','M_softdrop_12','M_{SD}^{two leading AK8}',True,[channel],True,0)
           # # VBF
           # ('invMAk4sel_1p0','N_pv','N_{PV}',True,[channel],True,0),
           # ('AK8_invMAk4sel_1p0','pt','p_{T}^{AK8-jet}',True,[channel],True,0),
           # ('AK8_invMAk4sel_1p0','eta','#eta^{AK8-jet}',True,[channel],True,0), 
           # ('AK8_invMAk4sel_1p0','tau21','#tau_{2}/#tau_{1}',True,[channel],True,0), 
           # ('AK4_invMAk4sel_1p0','pt_jet','p_{T}^{AK4-jet}',True,[channel],True,0),
           # ('AK4_invMAk4sel_1p0','eta_jet','#eta^{AK4-jet}',True,[channel],True,0),
           # ('invMAk4sel_1p0','M_jj_AK8','M_{jj-AK8}',True,[channel],True,0),
           # ('invMAk4sel_1p0','pT_AK8','p_{T}^{two leading AK8}',True,[channel],True,0),
           # ('invMAk4sel_1p0','eta_AK8','#eta^{two leading AK8}',True,[channel],True,0),
           # ('invMAk4sel_1p0','M_jj_AK4','M_{jj-AK4}',True,[channel],True,0),
           # ('invMAk4sel_1p0','pT_AK4','p_{T}^{two leading AK4}',True,[channel],True,0),
           # ('invMAk4sel_1p0','eta_AK4','#eta^{two leading AK4}',True,[channel],True,0),
           # ('invMAk4sel_1p0','M_softdrop_12','M_{SD}^{two leading AK8}',True,[channel],True,0)           
    ]

    for (dir,plot,xtitle,logY,channel,includeData,scaleSignal) in plots:
        plotter(dir,plot,xtitle,logY,channel,includeData,scaleSignal)
