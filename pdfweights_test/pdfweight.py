import os,sys

sets=[]
sets.append(None)
sets[0]=[]
pdfsetfile=open("test.lhaids")

setids=[]
using=[]
for line in pdfsetfile:
    if('orgpdf' in line):
        break
    if('ID' in line):
        setids.append(line.split(' ')[-1][:-1])
    if('Using' in line):
        using.append(line.split(' ')[1])
        
prevLine=""
for line in pdfsetfile:
    if(line[0]=='#'):
        continue
    if line.split(" ")[0]=='pdf':
        sets[-1].append(line.split(" ")[4][1:])
    if('min/max' in line and prevLine.split(" ")[0]=='pdf'):
        sets.append(None)
        sets[-1]=[]
    prevLine=line


first_index=[]
for set in sets[:-1]:   
    first_index.append(set[0])

pdfsetwebsite=open('website.lhaids')

correctnumbers={}

for line in pdfsetwebsite:
    if("<td>" in line):
        currentid=line.split("</td>")[0][4:]
        if line.split("</td>")[0][4:] in setids:
            currentnumber=line.split("</td>")[2][4:]
            currentname=line.split("</td>")[1][:-4]
            currentname=currentname[currentname.index('">')+2:]
            correctnumbers.update({currentid:(currentnumber,currentname)})
    
# print 'Inlcuding',len(setids),'PDF-Sets'

table=[]
for i in range(len(setids)):
    table.append((i,int(setids[i]),int(first_index[i]),int(using[i]),len(sets[i]),int(correctnumbers[setids[i]][0]),correctnumbers[setids[i]][1]))
    # print "Set Number: ",i,"Set-ID:",setids[i]
    # print "#Members: ",len(sets[i]) , "correct:",correctnumbers[setids[i]] 

print "%-12s%-12s%-12s%-12s%-12s%-12s%-12s"%("Index","SetID","first index","#using","#used","#avail","name")
for row in table:
    print '%-12i%-12i%-12i%-12i%-12i%-12i%-12s' % row
NTotal=0
for N in using:
    NTotal+=int(N)
print '#Weights Total:',NTotal
