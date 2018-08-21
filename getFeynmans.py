import sys, os, subprocess,glob
path='/nfs/dust/cms/user/albrechs/production/genproductions/bin/MadGraph5_aMCatNLO/aQGC_ZhadZhadJJ_EWK_LO_NPle1/aQGC_ZhadZhadJJ_EWK_LO_NPle1_gridpack/work/aQGC_ZhadZhadJJ_EWK_LO_NPle1/SubProcesses/'
# os.chdir(path)
outdir=path.rsplit('/',2)[0]+'/FeynmanDiagrams/'
outfile='allDiagrams.ps'
os.system('rm -rf '+outdir)
os.system('rm '+outfile)

if not os.path.exists(outdir):
    os.makedirs(outdir)        
dirs=os.walk(path)

files=[]
for subdir in dirs:
    files.append(glob.glob(subdir[0]+'/*.ps'))
# print files
for diagrams in files:
    for f in diagrams:
        command='cp '
        newf=f.split('/')[-2]+'_'+f.split('/')[-1]
        command+=f +' '+outdir+newf
        print command
        os.system(command)
merge_command='psmerge -o'+outfile+' '+outdir+'*.ps'
os.system(merge_command)
