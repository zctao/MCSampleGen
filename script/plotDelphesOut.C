// ROOT macro to plot histograms from Delphes output

#ifdef __CLING__
R__ADD_LIBRARY_PATH(MG5_aMC/Delphes)
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#endif

GenParticle* getParticle(Int_t, TClonesArray*);
GenParticle* getAfterFSR(GenParticle*, TClonesArray*);
bool isHadronicTop(GenParticle*, TClonesArray*);

void plotDelphesOut(const char *inputFile, const char *outputFile,
                    bool weighted=true, bool applyCuts=false)
{
  //gSystem->Load("libDelphes");

  // Create chain of root trees
  TChain chain("Delphes");
  chain.Add(inputFile);

  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();

  // Get pointers to branches used in this analysis
  //TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  //TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchMet = treeReader->UseBranch("MissingET");
  //TClonesArray *branchHT = treeReader->UseBranch("ScalarHT");
  TClonesArray *branchEvent = treeReader->UseBranch("Event");

  TClonesArray *branchParticle = treeReader->UseBranch("Particle");

  // Book histograms
  TFile foutput(outputFile, "RECREATE");
  TH1::SetDefaultSumw2();

  TH1 *histJetPT = new TH1F("jet_pt", "jet p_{T}", 25, 0, 500);
  TH1 *histJet0PT = new TH1F("jet0_pt", "Leading jet p_{T}", 25, 0, 500);
  TH1 *histJet1PT = new TH1F("jet1_pt", "Sub-leading jet p_{T}", 25, 0, 500);
  TH1 *histNJets = new TH1F("njets", "Number of Jets", 15, -0.5, 14.5);
  TH1 *histMET = new TH1F("met", "Missing E_{T}", 25, 0, 500);
  
  // Parton
  TH1 *histTopPT = new TH1F("t_pt_mc", "Top p_{T}", 25, 0, 500);
  TH1 *histTopY = new TH1F("t_y_mc", "Top rapidity", 20, -5, 5);
  TH1 *histTbarPT = new TH1F("tbar_pt_mc", "Anti-top p_{T}", 25, 0, 500);
  TH1 *histTbarY = new TH1F("tbar_y_mc", "Anti-top rapidity", 20, -5, 5);
  //TH1 *histTopHPT = new TH1F("th_pt_mc", "Hadronic top p_{T}", 25, 0, 500);
  //TH1 *histTopHY = new TH1F("th_y_mc", "Hadronic top rapidity", 20, -5, 5);
  //TH1 *histTopLPT = new TH1F("tl_pt_mc", "Leptonic top p_{T}", 25, 0, 500);
  //TH1 *histTopLY = new TH1F("tl_y_mc", "Leptonic top rapidity", 20, -5, 5);
  TH1 *histTTbarM = new TH1F("ttbar_m_mc", "TTbar mass", 25, 0, 1500);
  TH1 *histTTbarPT = new TH1F("ttbar_pt_mc", "TTbar p_{T}", 25, 0, 500);
  TH1 *histTTbarDPHI = new TH1F("ttbar_dphi_mc", "TTbar dPhi", 20, 0, 3.15);

  // Decay modes
  TH2 *histTTbarMode = new TH2F("ttbar_decaymode", "Decay Mode", 2, -0.5, 1.5, 2, -0.5, 1.5);
  histTTbarMode->GetXaxis()->SetTitle("hadronic top");
  histTTbarMode->GetYaxis()->SetTitle("hadronic anti-top");

  // Loop over events
  for (Int_t entry = 0; entry < numberOfEntries; ++entry) {
    // Load selected branches with data from the event
    treeReader->ReadEntry(entry);

    if (applyCuts) {
      //TODO
    }
    
    HepMCEvent *event = (HepMCEvent*) branchEvent -> At(0);
    Float_t weight = weighted ? event->Weight : 1;

    // Loop over jets
    Int_t njets = branchJet->GetEntriesFast();
    histNJets->Fill(njets, weight);

    for (Int_t i = 0; i < njets; ++i) {
      Jet* jet = (Jet*) branchJet->At(i);
      histJetPT->Fill(jet->PT, weight);
      if (i==0) histJet0PT->Fill(jet->PT, weight);
      if (i==1) histJet1PT->Fill(jet->PT, weight);
    }

    // MET
    MissingET* met = (MissingET*) branchMet->At(0);
    histMET->Fill(met->MET, weight);

    // partons
    // top
    GenParticle* t_afterFSR = getParticle(6, branchParticle);
    TLorentzVector t_p4;
    t_p4.SetPxPyPzE(t_afterFSR->Px, t_afterFSR->Py, t_afterFSR->Pz, t_afterFSR->E);
    histTopPT->Fill(t_p4.Pt(), weight);
    histTopY->Fill(t_p4.Rapidity(), weight);

    // antitop
    GenParticle* tbar_afterFSR = getParticle(-6, branchParticle);
    TLorentzVector tbar_p4;
    tbar_p4.SetPxPyPzE(tbar_afterFSR->Px, tbar_afterFSR->Py, tbar_afterFSR->Pz, tbar_afterFSR->E);
    histTbarPT->Fill(tbar_p4.Pt(), weight);
    histTbarY->Fill(tbar_p4.Rapidity(), weight);

    // ttbar
    TLorentzVector ttbar_p4 = t_p4 + tbar_p4;
    histTTbarM->Fill(ttbar_p4.M(), weight);
    histTTbarPT->Fill(ttbar_p4.Pt(), weight);
    histTTbarDPHI->Fill(abs(t_p4.DeltaPhi(tbar_p4)), weight);

    // decay mode
    bool isTHadronic = isHadronicTop(t_afterFSR, branchParticle);
    bool isTbarHadronic = isHadronicTop(tbar_afterFSR, branchParticle);
    histTTbarMode->Fill(isTHadronic, isTbarHadronic, weight);
  }

  // Write histograms to the output file
  foutput.cd();
  foutput.Write();
  foutput.Close();
}

GenParticle* getParticle(Int_t pdgid, TClonesArray* GenParticles)
{
  for (Int_t i = 0; i < GenParticles->GetEntriesFast(); i++) {
    GenParticle* p = (GenParticle*) GenParticles->At(i);
    if (p->PID != pdgid) continue;

    // get the one after FSR i.e. the last one
    return getAfterFSR(p, GenParticles);
  }

  return NULL;
}

GenParticle* getAfterFSR(GenParticle* particle, TClonesArray* particleCollection)
{
  Int_t PID = particle->PID;

  GenParticle* result = particle;
  bool isLast = true;

  while (result->Status != 1) {
    isLast = true;
    // loop over all daughers
    for (Int_t index = result->D1; index <= result->D2; index++) {
      if (index < 0) continue;
      GenParticle* daughter = (GenParticle*)particleCollection->At(index);
      Int_t DaugPID = daughter->PID;
      if (DaugPID == PID) {
        result = daughter;
        isLast = false;
        break;
      }
    }
    if (isLast) break;
  }

  return result;
}

bool isHadronicTop(GenParticle* top, TClonesArray* particleCollection)
{
  assert(abs(top->PID) == 6);

  // Get the W from top decay
  GenParticle* Wboson = NULL;

  for (Int_t index = top->D1; index <= top->D2; index++) {
    if (index < 0) continue;
    GenParticle* daughter = (GenParticle*)particleCollection->At(index);

    if (abs(daughter->PID) == 6) {
      // get the top after FSR
      GenParticle* tlast = getAfterFSR(top, particleCollection);
      return isHadronicTop(tlast, particleCollection);
    } else if (abs(daughter->PID) == 24) {
      Wboson = daughter;
      break;
    }
  }

  assert(Wboson);
  GenParticle* Wlast = getAfterFSR(Wboson, particleCollection);

  // Get the first daugher of W
  GenParticle* Wdaughter = (GenParticle*)particleCollection->At(Wlast->D1);

  if (abs(Wdaughter->PID) >= 11 && abs(Wdaughter->PID) <= 14) {
    return false;
  } else if (abs(Wdaughter->PID)==15 || abs(Wdaughter->PID)==16 ) {
    // W -> tau + nu_tau
    return false;
    // Differentiate leptonic and hadronic tau decay?
  } else {
    return true;
  }
}
