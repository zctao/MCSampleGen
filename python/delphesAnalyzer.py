#
def passEventSelection(event, channel='ttbar_ljets'):
    if channel=='ttbar_ljets':
        # MET > 20 GeV
        if not (event.MissingET[0].MET > 20.):
            return False
        # MET + MWT > 60. ?
        
        # NJets >= 4
        if not (event.Jet.GetEntries() >= 4):
            return False

        # Jet Pt > 25 GeV
        if not (event.Jet[3].PT > 25.): # event.Jet is sorted by pt
            return False

        # NBtag >= 2
        nbtags = 0
        for j in range(4):
            if event.Jet[j].BTag:
                nbtags += 1
        if not (nbtags >= 2):
            return False

        # Exactly one electron with pt > 25 GeV
        nEle25 = 0
        for ele in event.Electron:
            if ele.PT > 25.:
                nEle25 += 1
        # or exactly one muon with pt > 25 GeV
        nMu25 = 0
        for mu in event.Muon:
            if mu.PT > 25.:
                nMu25 += 1
        if not ( (nEle25 == 1 and nMu25 == 0) or (nEle25 == 0 and nMu25 == 1) ): 
            return False

        # passed all cuts
        return True
    else:
        return True
    
