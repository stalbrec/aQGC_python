import ParSet,subprocess,os,shutil,csv,glob


if(__name__=="__main__"):
    path='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/input'
    
    # dim8op=["T0"]
    # dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    dim8op=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    
    # channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    region='SignalRegion'
    # channels=['VV']
    channels=['VV','ssWW','ZZ']
    # channels=['VV','ssWW','WZ','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    # cuts=['detaAk4sel','invMAk4sel_1p0','invMAk4sel_1p2','invMAk4sel_1p5_allcuts']
    cuts=['VVRegion','invMAk4sel_1p0']
    for channel in channels:
        for cut in cuts:
            for op in dim8op:
                # plot_dir='output/plots/Fits/%s/%s/'%(cut,op)
                # if not os.path.exists(plot_dir):
                #     os.makedirs(plot_dir)
                
                print('+++++++++++writing RootFiles - %s - %s+++++++++++'%(op,cut))
                current_Set=ParSet.Set(op,channel,cut,region)
                current_Set.CombinedRootFiles(path)
