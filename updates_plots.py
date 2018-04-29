from plotter import plotter


if(__name__=='__main__'):

    #plots=[('rootdir','histname','XaxisTitle',logY),...]
    channel='ZZ'
    plots=[
           # VV
           ('tau21sel','eta_AK8','#eta^{two leading AK8}',True,[channel],True,0),
           ('tau21sel','M_jj_AK4','M_{jj-AK4}',True,[channel],True,0)
    ]

    for args in plots:
        plotter(*args)
