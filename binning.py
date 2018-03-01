from ROOT import TGraph, TCanvas
from array import array

if(__name__=='__main__'):
	boundaries=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
	print 'NBins:', len(boundaries)

	canv=TCanvas('canv','Binning for dijet invariant Mass',600,600)
	canv.cd()
        x, y = array( 'd' ), array( 'd' )
        for i in range(1,len(boundaries)):
            x.append(i)
            y.append(boundaries[i]-boundaries[i-1])

        graph=TGraph(len(boundaries),x,y)
        graph.SetLineColor( 2 )
        graph.SetLineWidth( 2 )
        graph.SetMarkerColor( 1 )
        graph.SetMarkerStyle( 3 )
        graph.SetTitle('Binning for M_{jj} Plots')
        graph.GetXaxis().SetTitle('bin')
        graph.GetYaxis().SetTitle('bin width')
        graph.Draw( 'AP' )

	wait=raw_input('Press Enter to continue...')
