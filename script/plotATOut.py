#!/usr/bin/env python

# script to make the same set of histograms as plotDelphesOut.C from AnalysisTop output file

from ROOT import gROOT, TFile, TLorentzVector, TH1, TH1F, TH2F
gROOT.SetBatch(True)

from histograms import HistogramsTTbar

def isSelected(event):
    # reco level ttbar event selection should already been applied
    # otherwise, do it here

    # only select semi-leptonic ttbar events
    return event.MC_th_eta>-100

def plotATOut(inputname, outputname, weighted=True, treename='nominal'):
    infile = TFile.Open(inputname, 'read')
    tree = infile.Get(treename)

    foutput = TFile(outputname, 'recreate')

    # histograms
    histsToPlot = HistogramsTTbar()

    # loop over all events in the tree
    for event in tree:
        if not isSelected(event):
            continue

        weight = event.weight_mc if weighted else 1.

        # jets
        njets = len(event.jet_pt)
        histsToPlot.histNJets.Fill(njets, weight)

        for i in range(njets):
            histsToPlot.histJetPT.Fill(event.jet_pt[i]*1e-3, weight)
            if i==0:
                histsToPlot.histJet0PT.Fill(event.jet_pt[i]*1e-3, weight)
            if i==1:
                histsToPlot.histJet1PT.Fill(event.jet_pt[i]*1e-3, weight)

        # MET
        histsToPlot.histMET.Fill(event.met_met*1e-3, weight)

        # lepton
        if event.el_pt.size() > 0:
            histsToPlot.histElePT.Fill(event.el_pt[0]*1e-3)
        if event.mu_pt.size() > 0:
            histsToPlot.histMuPT.Fill(event.mu_pt[0]*1e-3)

        # parton
        # top
        t_p4 = TLorentzVector()
        t_p4.SetPtEtaPhiM(event.MC_t_afterFSR_pt*1e-3,
                          event.MC_t_afterFSR_eta,
                          event.MC_t_afterFSR_phi,
                          event.MC_t_afterFSR_m*1e-3)

        histsToPlot.histTopPT.Fill(t_p4.Pt(), weight)
        histsToPlot.histTopY.Fill(t_p4.Rapidity(), weight)

        # anti-top
        tbar_p4 = TLorentzVector()
        tbar_p4.SetPtEtaPhiM(event.MC_tbar_afterFSR_pt*1e-3,
                             event.MC_tbar_afterFSR_eta,
                             event.MC_tbar_afterFSR_phi,
                             event.MC_tbar_afterFSR_m*1e-3)

        histsToPlot.histTbarPT.Fill(tbar_p4.Pt(), weight)
        histsToPlot.histTbarY.Fill(tbar_p4.Rapidity(), weight)

        # ttbar
        ttbar_p4 = t_p4 + tbar_p4
        histsToPlot.histTTbarM.Fill(ttbar_p4.M(), weight)
        histsToPlot.histTTbarPT.Fill(ttbar_p4.Pt(), weight)
        histsToPlot.histTTbarDPHI.Fill(abs(t_p4.DeltaPhi(tbar_p4)), weight)

    # Write histograms to the output file
    foutput.cd()
    foutput.Write()
    foutput.Close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('outputfile', type=str)
    parser.add_argument('-w', '--weighted', action='store_true')
    parser.add_argument('-t', '--treename', default='nominal')
    args = parser.parse_args()

    plotATOut(args.inputfile, args.outputfile, weighted=args.weighted, treename=args.treename)
