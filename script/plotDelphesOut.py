#!/usr/bin/env python
from __future__ import print_function
from ROOT import TFile, TChain, TLorentzVector
import DelphesAnalysis.Delphes as Delphes

from histograms import HistogramsTTbar
from partonHistory import getTopAfterFSR, getAntiTopAfterFSR, isHadronicTop
from delphesAnalyzer import passEventSelection, getFileList

def plotDelphesOut(inputFiles, outputFile, weighted=True, applyCuts=False):
    # inputs
    files = getFileList(inputFiles)

    chain = TChain("Delphes")
    for infile in files:
        chain.Add(infile)
    nevents = chain.GetEntries()
    #print(nevents)

    # output
    foutput = TFile(outputFile, "RECREATE")

    # book histograms
    histsToPlot = HistogramsTTbar()

    # loop over events
    for event in chain:
        if applyCuts and not passEventSelection(event):
            continue

        weight = event.Event[0].Weight if weighted else 1.

        # jets
        njets = event.Jet.GetEntries()
        histsToPlot.histNJets.Fill(njets)

        for i, jet in enumerate(event.Jet):
            histsToPlot.histJetPT.Fill(jet.PT, weight)
            if i==0:
                histsToPlot.histJet0PT.Fill(jet.PT, weight)
            if i==1:
                histsToPlot.histJet1PT.Fill(jet.PT, weight)

        # MET
        if event.MissingET.GetEntries() > 0:
            histsToPlot.histMET.Fill(event.MissingET[0].MET, weight)

        # lepton if l+jets channel selected
        if event.Electron.GetEntries() > 0:
            histsToPlot.histElePT.Fill(event.Electron[0].PT, weight)
        if event.Muon.GetEntries() > 0:
            histsToPlot.histMuPT.Fill(event.Muon[0].PT, weight)

        # partons
        # top
        t_afterFSR = getTopAfterFSR(event.Particle)
        t_p4 = TLorentzVector()
        t_p4.SetPxPyPzE(t_afterFSR.Px, t_afterFSR.Py, t_afterFSR.Pz, t_afterFSR.E)
        histsToPlot.histTopPT.Fill(t_p4.Pt(), weight)
        histsToPlot.histTopY.Fill(t_p4.Rapidity(), weight)

        # antitop
        tbar_afterFSR = getAntiTopAfterFSR(event.Particle)
        tbar_p4 = TLorentzVector()
        tbar_p4.SetPxPyPzE(tbar_afterFSR.Px, tbar_afterFSR.Py, tbar_afterFSR.Pz, tbar_afterFSR.E)
        histsToPlot.histTbarPT.Fill(tbar_p4.Pt(), weight)
        histsToPlot.histTbarY.Fill(tbar_p4.Rapidity(), weight)

        # ttbar
        ttbar_p4 = t_p4 + tbar_p4
        histsToPlot.histTTbarM.Fill(ttbar_p4.M(), weight)
        histsToPlot.histTTbarPT.Fill(ttbar_p4.Pt(), weight)
        histsToPlot.histTTbarDPHI.Fill(abs(t_p4.DeltaPhi(tbar_p4)), weight)

        # decay mode
        isTHadronic = isHadronicTop(t_afterFSR, event.Particle)
        isTbarHadronic = isHadronicTop(tbar_afterFSR, event.Particle)
        histsToPlot.histTTbarMode.Fill(isTHadronic, isTbarHadronic, weight)

    foutput.cd()
    foutput.Write()
    foutput.Close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfiles", nargs='+', help="Input file paths")
    parser.add_argument("-o", "--output", default="histograms.root")
    parser.add_argument("-w", "--weighted", action='store_true')
    parser.add_argument('-s', "--applyCuts", action='store_true')
    args = parser.parse_args()

    plotDelphesOut(args.inputfiles, args.output, weighted=args.weighted, applyCuts=args.applyCuts)

    #plotDelphesOut("/home/ztao/data/batch_output/MCSampleGen/20201209/ttbar_nlo_lpj", 'test.root')
    #plotDelphesOut('/home/ztao/MCSampleGen/output/ttbar_lo_incl/Events/run_01/tag_1_delphes_events.root', 'test.root', weighted=True, applyCuts=True)
