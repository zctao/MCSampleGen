from ROOT import gROOT, TH1, TH1F, TH2F
gROOT.SetBatch(True)

class HistogramsTTbar():
    def __init__(self):
        TH1.SetDefaultSumw2()
        self.histJetPT = TH1F("jet_pt", "jet p_{T}", 25, 0, 500)
        self.histJet0PT = TH1F("jet0_pt", "Leading jet p_{T}", 25, 0, 500)
        self.histJet1PT = TH1F("jet1_pt", "Sub-leading jet p_{T}", 25, 0, 500)
        self.histNJets = TH1F("njets", "Number of Jets", 15, -0.5, 14.5)
        self.histMET = TH1F("met", "Missing E_{T}", 25, 0, 500)
        #self.histLepPT = TH1F("lep_pt", "lepton p_{T}", 25, 0, 500)
        self.histElePT = TH1F("ele_pt", "Electron p_{T}", 25, 0, 500)
        self.histMuPT = TH1F("mu_pt", "Muon p_{T}", 25, 0, 500)

        # Parton
        self.histTopPT = TH1F("t_pt_mc", "Top p_{T} (truth)", 25, 0, 500)
        self.histTopY = TH1F("t_y_mc", "Top rapidity (truth)", 20, -5, 5)
        self.histTbarPT = TH1F("tbar_pt_mc", "Anti-top p_{T} (truth)", 25, 0, 500)
        self.histTbarY = TH1F("tbar_y_mc", "Anti-top rapidity (truth)", 20, -5, 5)
        #self.histTopHPT = TH1F("th_pt_mc", "Hadronic top p_{T} (truth)", 25, 0, 500)
        #self.histTopHY = TH1F("th_y_mc", "Hadronic top rapidity (truth)", 20, -5, 5)
        #self.histTopLPT = TH1F("tl_pt_mc", "Leptonic top p_{T} (truth)", 25, 0, 500)
        #self.histTopLY = TH1F("tl_y_mc", "Leptonic top rapidity (truth)", 20, -5, 5)
        self.histTTbarM = TH1F("ttbar_m_mc", "TTbar mass (truth)", 25, 0, 1500)
        self.histTTbarPT = TH1F("ttbar_pt_mc", "TTbar p_{T} (truth)", 25, 0, 500)
        self.histTTbarDPHI = TH1F("ttbar_dphi_mc", "TTbar dPhi (truth)", 20, 0, 3.15)
        
        # decay mode
        self.histTTbarMode = TH2F("ttbar_decaymode", "Decay Mode", 2, -0.5, 1.5, 2, -0.5, 1.5)
        self.histTTbarMode.GetXaxis().SetTitle("hadronic top")
        self.histTTbarMode.GetYaxis().SetTitle("hadronic anti-top")
