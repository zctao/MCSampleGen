#!/usr/bin/env python
from ROOT import gROOT, TFile, THStack, TCanvas, TLegend, TH1
gROOT.SetBatch(True)

def plotHistograms(histname, filenames, labels, canvas, legend, normalize=False):
    assert(len(filenames)==len(labels))
    TH1.SetDefaultSumw2()
    # get histograms from the files
    histograms = []
    for fname in filenames:
        f = TFile.Open(fname, "READ")
        h = f.Get(histname)
        h.SetDirectory(0)
        histograms.append(h)
        f.Close()

    # plot
    canvas.cd()
    hs = THStack()
    hs.Draw()
    norm = 1.
    for i, (hist, label) in enumerate(zip(histograms, labels)):
        hist.SetStats(0)
        hist.SetLineColor(i+1)
        hist.SetMarkerColor(i+1)

        # normalize to the first histogram if needed
        if normalize:
            if i==0:
                norm = hist.Integral()
            else:
                norm_i = hist.Integral()
                hist.Scale(norm/norm_i)

        hs.Add(hist)
        legend.AddEntry(hist, label)

    return hs

def compareAllHistograms(filenames, labels, outname, normalize=False):
    canvas = TCanvas("c")
    canvas.Print(outname+'[')

    histnamesToPlot = [
        'jet_pt', 'jet0_pt', 'jet1_pt', 'njets', 'met', 'ele_pt', 'mu_pt',
        't_pt_mc', 't_y_mc', 'tbar_pt_mc', 'tbar_y_mc',
        'ttbar_m_mc', 'ttbar_pt_mc', 'ttbar_dphi_mc'
    ]

    for hname in histnamesToPlot:
        leg = TLegend(0.7, 0.7, 0.85, 0.85)
        hs = plotHistograms(hname, filenames, labels, canvas, leg, normalize)
        hs.Draw("nostack")
        hs.SetTitle(hs.GetHists().At(0).GetTitle())
        #hs.GetXaxis().SetTitle(hs.GetHists().At(0).GetXaxis().GetTitle())
        #hs.GetYaxis().SetTitle(hs.GetHists().At(0).GetYaxis().GetTitle())

        leg.Draw()
        #canvas.BuildLegend()
        canvas.Print(outname)

    canvas.Print(outname+']')

if __name__ == "__main__":
    from os import path
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument('inputfiles', nargs='+')
    parser.add_argument('-l', '--labels', nargs='+')
    parser.add_argument('-o', '--outname', default='compare.pdf')
    parser.add_argument('-n', '--normalize', action='store_true')
    args = parser.parse_args()

    if not args.labels:
        args.labels = [path.basename(fname) for fname in args.inputfiles]

    compareAllHistograms(args.inputfiles, args.labels, args.outname, args.normalize)
