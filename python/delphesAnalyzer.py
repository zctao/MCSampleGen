from __future__ import print_function
import os
import time
import numpy as np
import ROOT
from ROOT import TChain, TTree, TFile, TLorentzVector
import DelphesAnalysis.Delphes as Delphes
from partonHistory import getTopAfterFSR, getAntiTopAfterFSR, getWfromTopDecay, isHadronicTop
from variables import varTTbarLJets

def passMETCuts(event):
    # MET > 20 GeV
    return event.MissingET[0].MET > 20.

def passJetCuts(event):
    # NJets >= 4 and pT > 25 GeV
    nJet25 = 0
    # NBtag >= 2
    nBtags = 0

    for jet in event.Jet:
        if jet.PT > 25.:
            nJet25 += 1
            if jet.BTag:
                nBtags += 1

    return nJet25 >= 4 and nBtags >= 2

def passElectronCuts(event):
    #Exactly one electron with pt > 25 GeV
    nEle25 = 0

    for ele in event.Electron:
        if ele.PT > 25.:
            nEle25 += 1

    return nEle25 == 1

def passMuonCuts(event):
    # Exactly one muon with pt > 25 GeV
    nMu25 = 0

    for mu in event.Muon:
        if mu.PT > 25.:
            nMu25 += 1

    return nMu25 == 1

def passEventSelection(event, channel='ttbar_ljets'):
    if channel=='ttbar_ljets':
        # MET > 20 GeV
        if not passMETCuts(event):
            return False
        # MET + MWT > 60. ?

        # NJets >= 4
        # Jet Pt > 25 GeV
        # NBtag >= 2
        if not passJetCuts(event):
            return False

        # Exactly one electron with pt > 25 GeV
        # or exactly one muon with pt > 25 GeV
        isEleJets = passElectronCuts(event) and not passMuonCuts(event)
        isMuJets = not passElectronCuts(event) and passMuonCuts(event)
        if not (isEleJets or isMuJets):
            return False

        # passed all cuts
        return True
    else:
        return True

def getFileList(inputFiles):
    if isinstance(inputFiles, list):
        files = []
        for infile in inputFiles:
            files += getFileList(infile)
    elif os.path.isdir(inputFiles):
        files = [os.path.join(inputFiles, fname) for fname in os.listdir(inputFiles) if fname.endswith('.root')]
    elif os.path.isfile(inputFiles):
        files = [inputFiles]
    else:
        files = []

    return files

def makeNtuple_ttbar_ljets(inputFiles, outputname, treename="Delphes", arrayFormat=None, maxevents=None):
    # inputs
    infiles = getFileList(inputFiles)

    chain = TChain(treename)
    for finput in infiles:
        chain.Add(finput)
    nevents = chain.GetEntries()
    print('Total number of entries:', nevents)

    foutput = TFile(outputname+'.root', "recreate")
    # tree
    tree = TTree("ntuple", "ntuple")
    # variables
    variables = varTTbarLJets()
    variables.set_up_branches(tree)

    # loop over events
    t_tree_start = time.time()
    for ievt, event in enumerate(chain):
        if maxevents is not None and ievt >= maxevents:
            break

        if not ievt%10000:
            print("processing event {}/{}".format(ievt, nevents))

        if not passEventSelection(event):
            continue

        variables.set_default()

        # event weight
        variables.w[0] = event.Event[0].Weight

        # partons
        # top
        t_afterFSR = getTopAfterFSR(event.Particle)
        t_p4 = TLorentzVector()
        t_p4.SetPxPyPzE(t_afterFSR.Px, t_afterFSR.Py, t_afterFSR.Pz, t_afterFSR.E)
        t_ishadronic = isHadronicTop(t_afterFSR, event.Particle)

        W_fromT = getWfromTopDecay(t_afterFSR, event.Particle, afterFSR=True)
        W_fromT_p4 = TLorentzVector()
        W_fromT_p4.SetPxPyPzE(W_fromT.Px, W_fromT.Py, W_fromT.Pz, W_fromT.E)

        # antitop
        tbar_afterFSR = getAntiTopAfterFSR(event.Particle)
        tbar_p4 = TLorentzVector()
        tbar_p4.SetPxPyPzE(tbar_afterFSR.Px, tbar_afterFSR.Py, tbar_afterFSR.Pz, tbar_afterFSR.E)
        tbar_ishadronic = isHadronicTop(tbar_afterFSR, event.Particle)

        W_fromTbar = getWfromTopDecay(tbar_afterFSR, event.Particle, afterFSR=True)
        W_fromTbar_p4 = TLorentzVector()
        W_fromTbar_p4.SetPxPyPzE(W_fromTbar.Px, W_fromTbar.Py, W_fromTbar.Pz, W_fromTbar.E)

        th_p4, tl_p4 = None, None
        wh_p4, wl_p4 = None, None
        if t_ishadronic and not tbar_ishadronic:
            th_p4 = t_p4
            tl_p4 = tbar_p4
            wh_p4 = W_fromT_p4
            wl_p4 = W_fromTbar_p4
        elif not t_ishadronic and tbar_ishadronic:
            th_p4 = tbar_p4
            tl_p4 = t_p4
            wh_p4 = W_fromTbar_p4
            wl_p4 = W_fromT_p4

        if th_p4 is not None:
            variables.th_pt[0] = th_p4.Pt()
            variables.th_eta[0] = th_p4.Eta()
            variables.th_y[0] = th_p4.Rapidity()
            variables.th_phi[0] = th_p4.Phi()
            variables.th_m[0] = th_p4.M()
            variables.th_e[0] = th_p4.E()

        if tl_p4 is not None:
            variables.tl_pt[0] = tl_p4.Pt()
            variables.tl_eta[0] = tl_p4.Eta()
            variables.tl_y[0] = tl_p4.Rapidity()
            variables.tl_phi[0] = tl_p4.Phi()
            variables.tl_m[0] = tl_p4.M()
            variables.tl_e[0] = tl_p4.E()

        if wh_p4 is not None:
            variables.wh_pt[0] = wh_p4.Pt()
            variables.wh_eta[0] = wh_p4.Eta()
            variables.wh_phi[0] = wh_p4.Phi()
            variables.wh_m[0] = wh_p4.M()
            variables.wh_e[0] = wh_p4.E()

        if wl_p4 is not None:
            variables.wl_pt[0] = wl_p4.Pt()
            variables.wl_eta[0] = wl_p4.Eta()
            variables.wl_phi[0] = wl_p4.Phi()
            variables.wl_m[0] = wl_p4.M()
            variables.wl_e[0] = wl_p4.E()

        # lepton
        if passElectronCuts(event) and not passMuonCuts(event):
            variables.lep_pt[0] = event.Electron[0].PT
            variables.lep_eta[0] = event.Electron[0].Eta
            variables.lep_phi[0] = event.Electron[0].Phi
        elif passMuonCuts(event) and not passElectronCuts(event):
            variables.lep_pt[0] = event.Muon[0].PT
            variables.lep_eta[0] = event.Muon[0].Eta
            variables.lep_phi[0] = event.Muon[0].Phi

        # jets
        for i, jet in enumerate(event.Jet):
            if i==0:
                variables.j1_pt[0] = jet.PT
                variables.j1_eta[0] = jet.Eta
                variables.j1_phi[0] = jet.Phi
                variables.j1_m[0] = jet.Mass
                variables.j1_isbtag[0] = jet.BTag
            if i==1:
                variables.j2_pt[0] = jet.PT
                variables.j2_eta[0] = jet.Eta
                variables.j2_phi[0] = jet.Phi
                variables.j2_m[0] = jet.Mass
                variables.j2_isbtag[0] = jet.BTag
            if i==2:
                variables.j3_pt[0] = jet.PT
                variables.j3_eta[0] = jet.Eta
                variables.j3_phi[0] = jet.Phi
                variables.j3_m[0] = jet.Mass
                variables.j3_isbtag[0] = jet.BTag
            if i==3:
                variables.j4_pt[0] = jet.PT
                variables.j4_eta[0] = jet.Eta
                variables.j4_phi[0] = jet.Phi
                variables.j4_m[0] = jet.Mass
                variables.j4_isbtag[0] = jet.BTag
            if i==4:
                variables.j5_pt[0] = jet.PT
                variables.j5_eta[0] = jet.Eta
                variables.j5_phi[0] = jet.Phi
                variables.j5_m[0] = jet.Mass
                variables.j5_isbtag[0] = jet.BTag
            if i==5:
                variables.j6_pt[0] = jet.PT
                variables.j6_eta[0] = jet.Eta
                variables.j6_phi[0] = jet.Phi
                variables.j6_m[0] = jet.Mass
                variables.j6_isbtag[0] = jet.BTag

        # MET
        variables.met_met[0] = event.MissingET[0].MET
        variables.met_phi[0] = event.MissingET[0].Phi

        tree.Fill()

    t_tree_done = time.time()
    print("Making flat nutple took {:.2f} seconds ({:.3f} ms/event)".format(t_tree_done-t_tree_start, (t_tree_done-t_tree_start)*1000/nevents))

    print("Finish writing tree to file")
    foutput.Write()

    if arrayFormat is not None:
        print("Save tree as array")
        # convert tree to array
        import resource
        ROOT.ROOT.EnableImplicitMT()
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print("Current RAM usage: {:.3f} GB".format(usage*1e-6))
        t_arr_start = time.time()

        ntuple_arr_dict = ROOT.RDataFrame(tree).AsNumpy()

        t_arr_done = time.time()
        print("Converting TTree took {:.2f} seconds".format(t_arr_done-t_arr_start))
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print("Current RAM usage: {:.3f} GB".format(usage*1e-6))

        if arrayFormat == "npz":
            np.savez(outputname+'.npz', **ntuple_arr)
        elif arrayFormat == "h5":
            import h5py
            with h5py.File(outputname+'.h5', 'w') as hf:
                for var_name, var_arr in ntuple_arr_dict.items():
                    hf.create_dataset(var_name, data=var_arr)
        else:
            raise RuntimeError("Current supported format: 'npz' or 'h5'")
