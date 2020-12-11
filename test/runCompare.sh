#!/bin/bash
# MadGraph+Pythia+Delphes events
sample_dir=/home/ztao/data/batch_output/MCSampleGen/20201209
delphes_events_ttbar_lo_incl=$sample_dir/ttbar_lo_incl
delphes_events_ttbar_lo_lpj=$sample_dir/ttbar_lo_lpj
delphes_events_ttbar_lo_lmj=$sample_dir/ttbar_lo_lmj
delphes_events_ttbar_nlo_incl=$sample_dir/ttbar_nlo_incl
delphes_events_ttbar_nlo_lpj=$sample_dir/ttbar_nlo_lpj
delphes_events_ttbar_nlo_lmj=$sample_dir/ttbar_nlo_lmj

# ATLAS TOPQ1 410470
topq1mc=/home/ztao/data/grid_output/test/user.ztao.23232618._000782.output.root

# weighted
# ttbar inclusive NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_incl -o output/histograms_ttbar_nlo_incl_w.root -w
# ttbar inclusive LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_incl -o output/histograms_ttbar_lo_incl_w.root -w
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_incl_w.root output/histograms_ttbar_lo_incl_w.root -l NLO LO -n -o output/compare_incl_weighted.pdf

# ttbar l+jets NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_lpj $delphes_events_ttbar_nlo_lmj -o output/histograms_ttbar_nlo_ljets_w.root -w
# ttbar l+jets LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_lpj $delphes_events_ttbar_lo_lmj -o output/histograms_ttbar_lo_ljets_w.root -w
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_ljets_w.root output/histograms_ttbar_lo_ljets_w.root -l NLO LO -n -o output/compare_ljets_weighted.pdf

# alternative
#python script/comparePlots.py output/histograms_ttbar_lo_lpj.root output/histograms_ttbar_lo_lpj_alt.root -l PyDecay MGDecay -n -o output/compare_lo_decay_weighted.pdf

#################
# unweighted
# ttbar inclusive NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_incl -o output/histograms_ttbar_nlo_incl_uw.root
# ttbar inclusive LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_incl -o output/histograms_ttbar_lo_incl_uw.root
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_incl_uw.root output/histograms_ttbar_lo_incl_uw.root -l NLO LO -n -o output/compare_incl_unweighted.pdf

# ttbar l+jets NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_lpj $delphes_events_ttbar_nlo_lmj -o output/histograms_ttbar_nlo_ljets_uw.root
# ttbar l+jets LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_lpj $delphes_events_ttbar_lo_lmj -o output/histograms_ttbar_lo_ljets_uw.root
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_ljets_uw.root output/histograms_ttbar_lo_ljets_uw.root -l NLO LO -n -o output/compare_ljets_unweighted.pdf

# Compare with ATLAS TOPQ1 410470
# with event selection
# weighted
# ttbar l+jets NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_lpj $delphes_events_ttbar_nlo_lmj -w -s -o output/histograms_ttbar_nlo_ljets_w_sel.root
# ttbar l+jets LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_lpj $delphes_events_ttbar_lo_lmj -w -s -o output/histograms_ttbar_lo_ljets_w_sel.root
# ATLAS TOPQ1 410470
python script/plotATOut.py $topq1mc output/histograms_ttbar_AT.root -w
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_ljets_w_sel.root output/histograms_ttbar_lo_ljets_w_sel.root output/histograms_ttbar_AT.root -l 'aMcAtNlo+Py8+Delphes' 'MG5+Py8+Delphes' 'TOPQ1_410470' -n -o output/compare_atlas_ljets_weighted_wRecoCuts.pdf

# unweighted
# ttbar l+jets NLO
python script/plotDelphesOut.py $delphes_events_ttbar_nlo_lpj $delphes_events_ttbar_nlo_lmj -s -o output/histograms_ttbar_nlo_ljets_uw_sel.root
# ttbar l+jets LO
python script/plotDelphesOut.py $delphes_events_ttbar_lo_lpj $delphes_events_ttbar_lo_lmj -s -o output/histograms_ttbar_lo_ljets_uw_sel.root
# ATLAS TOPQ1 410470
python script/plotATOut.py $topq1mc output/histograms_ttbar_AT.root
# plot comparison
python script/comparePlots.py output/histograms_ttbar_nlo_ljets_uw_sel.root output/histograms_ttbar_lo_ljets_uw_sel.root output/histograms_ttbar_AT.root -l 'aMcAtNlo+Py8+Delphes' 'MG5+Py8+Delphes' 'TOPQ1_410470' -n -o output/compare_atlas_ljets_unweighted_wRecoCuts.pdf
