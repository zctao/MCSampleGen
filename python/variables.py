import numpy as np

class varTTbarLJets():
    def __init__(self):
        # event weight
        self.w = np.empty((1), dtype="float32")
        # partons
        ## hadronic top
        self.th_pt = np.empty((1), dtype="float32")
        self.th_eta = np.empty((1), dtype="float32")
        self.th_y = np.empty((1), dtype="float32")
        self.th_phi = np.empty((1), dtype="float32")
        self.th_m = np.empty((1), dtype="float32")
        self.th_e = np.empty((1), dtype="float32")
        ## leptonic top
        self.tl_pt = np.empty((1), dtype="float32")
        self.tl_eta = np.empty((1), dtype="float32")
        self.tl_y = np.empty((1), dtype="float32")
        self.tl_phi = np.empty((1), dtype="float32")
        self.tl_m = np.empty((1), dtype="float32")
        self.tl_e = np.empty((1), dtype="float32")
        ## hadronic W
        self.wh_pt = np.empty((1), dtype="float32")
        self.wh_eta = np.empty((1), dtype="float32")
        self.wh_phi = np.empty((1), dtype="float32")
        self.wh_m = np.empty((1), dtype="float32")
        self.wh_e = np.empty((1), dtype="float32")
        ## leptonic W
        self.wl_pt = np.empty((1), dtype="float32")
        self.wl_eta = np.empty((1), dtype="float32")
        self.wl_phi = np.empty((1), dtype="float32")
        self.wl_m = np.empty((1), dtype="float32")
        self.wl_e = np.empty((1), dtype="float32")
        # reco objects
        ## lepton
        self.lep_pt = np.empty((1), dtype="float32")
        self.lep_eta = np.empty((1), dtype="float32")
        self.lep_phi = np.empty((1), dtype="float32")
        ## jets
        self.j1_pt = np.empty((1), dtype="float32")
        self.j1_eta = np.empty((1), dtype="float32")
        self.j1_phi = np.empty((1), dtype="float32")
        self.j1_m = np.empty((1), dtype="float32")
        self.j1_isbtag = np.empty((1), dtype="float32")
        self.j2_pt = np.empty((1), dtype="float32")
        self.j2_eta = np.empty((1), dtype="float32")
        self.j2_phi = np.empty((1), dtype="float32")
        self.j2_m = np.empty((1), dtype="float32")
        self.j2_isbtag = np.empty((1), dtype="float32")
        self.j3_pt = np.empty((1), dtype="float32")
        self.j3_eta = np.empty((1), dtype="float32")
        self.j3_phi = np.empty((1), dtype="float32")
        self.j3_m = np.empty((1), dtype="float32")
        self.j3_isbtag = np.empty((1), dtype="float32")
        self.j4_pt = np.empty((1), dtype="float32")
        self.j4_eta = np.empty((1), dtype="float32")
        self.j4_phi = np.empty((1), dtype="float32")
        self.j4_m = np.empty((1), dtype="float32")
        self.j4_isbtag = np.empty((1), dtype="float32")
        self.j5_pt = np.empty((1),  dtype="float32")
        self.j5_eta = np.empty((1), dtype="float32")
        self.j5_phi = np.empty((1), dtype="float32")
        self.j5_m = np.empty((1), dtype="float32")
        self.j5_isbtag = np.empty((1), dtype="float32")
        self.j6_pt = np.empty((1), dtype="float32")
        self.j6_eta = np.empty((1), dtype="float32")
        self.j6_phi = np.empty((1), dtype="float32")
        self.j6_m = np.empty((1), dtype="float32")
        self.j6_isbtag = np.empty((1), dtype="float32")
        ## MET
        self.met_met = np.empty((1), dtype="float32")
        self.met_phi = np.empty((1), dtype="float32")

    def set_up_branches(self, tree):
        tree.Branch("w", self.w, "w/F")

        tree.Branch("th_pt", self.th_pt, "th_pt/F")
        tree.Branch("th_eta", self.th_eta, "th_eta/F")
        tree.Branch("th_y", self.th_y, "th_y/F")
        tree.Branch("th_phi", self.th_phi, "th_phi/F")
        tree.Branch("th_m", self.th_m, "th_m/F")
        tree.Branch("th_e", self.th_e, "th_e/F")

        tree.Branch("tl_pt", self.tl_pt, "tl_pt/F")
        tree.Branch("tl_eta", self.tl_eta, "tl_eta/F")
        tree.Branch("tl_y", self.tl_y, "tl_y/F")
        tree.Branch("tl_phi", self.tl_phi, "tl_phi/F")
        tree.Branch("tl_m", self.tl_m, "tl_m/F")
        tree.Branch("tl_e", self.tl_e, "tl_e/F")

        tree.Branch("wh_pt", self.wh_pt, "wh_pt/F")
        tree.Branch("wh_eta", self.wh_eta, "wh_eta/F")
        tree.Branch("wh_phi", self.wh_phi, "wh_phi/F")
        tree.Branch("wh_m", self.wh_m, "wh_m/F")
        tree.Branch("wh_e", self.wh_e, "wh_e/F")

        tree.Branch("wl_pt", self.wl_pt, "wl_pt/F")
        tree.Branch("wl_eta", self.wl_eta, "wl_eta/F")
        tree.Branch("wl_phi", self.wl_phi, "wl_phi/F")
        tree.Branch("wl_m", self.wl_m, "wl_m/F")
        tree.Branch("wl_e", self.wl_e, "wl_e/F")

        tree.Branch("lep_pt", self.lep_pt, "lep_pt/F")
        tree.Branch("lep_eta", self.lep_eta, "lep_eta/F")
        tree.Branch("lep_phi", self.lep_phi, "lep_phi/F")

        tree.Branch("j1_pt", self.j1_pt, "j1_pt/F")
        tree.Branch("j1_eta", self.j1_eta, "j1_eta/F")
        tree.Branch("j1_phi", self.j1_phi, "j1_phi/F")
        tree.Branch("j1_m", self.j1_m, "j1_m/F")
        tree.Branch("j1_isbtag", self.j1_isbtag, "j1_isbtag/F")

        tree.Branch("j2_pt", self.j2_pt, "j2_pt/F")
        tree.Branch("j2_eta", self.j2_eta, "j2_eta/F")
        tree.Branch("j2_phi", self.j2_phi, "j2_phi/F")
        tree.Branch("j2_m", self.j2_m, "j2_m/F")
        tree.Branch("j2_isbtag", self.j2_isbtag, "j2_isbtag/F")

        tree.Branch("j3_pt", self.j3_pt, "j3_pt/F")
        tree.Branch("j3_eta", self.j3_eta, "j3_eta/F")
        tree.Branch("j3_phi", self.j3_phi, "j3_phi/F")
        tree.Branch("j3_m", self.j3_m, "j3_m/F")
        tree.Branch("j3_isbtag", self.j3_isbtag, "j3_isbtag/F")

        tree.Branch("j4_pt", self.j4_pt, "j4_pt/F")
        tree.Branch("j4_eta", self.j4_eta, "j4_eta/F")
        tree.Branch("j4_phi", self.j4_phi, "j4_phi/F")
        tree.Branch("j4_m", self.j4_m, "j4_m/F")
        tree.Branch("j4_isbtag", self.j4_isbtag, "j4_isbtag/F")

        tree.Branch("j5_pt", self.j5_pt, "j5_pt/F")
        tree.Branch("j5_eta", self.j5_eta, "j5_eta/F")
        tree.Branch("j5_phi", self.j5_phi, "j5_phi/F")
        tree.Branch("j5_m", self.j5_m, "j5_m/F")
        tree.Branch("j5_isbtag", self.j5_isbtag, "j5_isbtag/F")

        tree.Branch("j6_pt", self.j6_pt, "j6_pt/F")
        tree.Branch("j6_eta", self.j6_eta, "j6_eta/F")
        tree.Branch("j6_phi", self.j6_phi, "j6_phi/F")
        tree.Branch("j6_m", self.j6_m, "j6_m/F")
        tree.Branch("j6_isbtag", self.j6_isbtag, "j6_isbtag/F")

        tree.Branch("met_met", self.met_met, "met_met/F")
        tree.Branch("met_phi", self.met_phi, "met_phi/F")

    def set_default(self):
        self.w[0] = -5000.

        self.th_pt[0] = -5000.
        self.th_eta[0] = -5000.
        self.th_y[0] = -5000.
        self.th_phi[0] = -5000.
        self.th_m[0] = -5000.
        self.th_e[0] = -5000.

        self.tl_pt[0] = -5000.
        self.tl_eta[0] = -5000.
        self.tl_y[0] = -5000.
        self.tl_phi[0] = -5000.
        self.tl_m[0] = -5000.
        self.tl_e[0] = -5000.

        self.wh_pt[0] = -5000.
        self.wh_eta[0] = -5000.
        self.wh_phi[0] = -5000.
        self.wh_m[0] = -5000.
        self.wh_e[0] = -5000.

        self.wl_pt[0] = -5000.
        self.wl_eta[0] = -5000.
        self.wl_phi[0] = -5000.
        self.wl_m[0] = -5000.
        self.wl_e[0] = -5000.

        self.lep_pt[0] = -5000.
        self.lep_eta[0] = -5000.
        self.lep_phi[0] = -5000.

        self.j1_pt[0] = -5000.
        self.j1_eta[0] = -5000.
        self.j1_phi[0] = -5000.
        self.j1_m[0] = -5000.
        self.j1_isbtag[0] = -5000.
        self.j2_pt[0] = -5000.
        self.j2_eta[0] = -5000.
        self.j2_phi[0] = -5000.
        self.j2_m[0] = -5000.
        self.j2_isbtag[0] = -5000.
        self.j3_pt[0] = -5000.
        self.j3_eta[0] = -5000.
        self.j3_phi[0] = -5000.
        self.j3_m[0] = -5000.
        self.j3_isbtag[0] = -5000.
        self.j4_pt[0] = -5000.
        self.j4_eta[0] = -5000.
        self.j4_phi[0] = -5000.
        self.j4_m[0] = -5000.
        self.j4_isbtag[0] = -5000.
        self.j5_pt = np.empty((1),  dtype="float32")
        self.j5_eta[0] = -5000.
        self.j5_phi[0] = -5000.
        self.j5_m[0] = -5000.
        self.j5_isbtag[0] = -5000.
        self.j6_pt[0] = -5000.
        self.j6_eta[0] = -5000.
        self.j6_phi[0] = -5000.
        self.j6_m[0] = -5000.
        self.j6_isbtag[0] = -5000.

        self.met_met[0] = -5000.
        self.met_phi[0] = -5000.

    def get_variable_names(self):
        return [var for var in dir(self) if not callable(getattr(self, var)) and not var.startswith("__")]
