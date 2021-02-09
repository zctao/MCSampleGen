#!/bin/bash
nEvents=1000000
nJobs=20
nCores=8

Outdir=/home/ztao/data/batch_output/MCSampleGen/20210209/

# zprime > t tbar NLO
# top decay with MadSpin
# l+, jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       zprime_nlo_madspin_lpj \
       -e zprime \
       -f generateZprime_nlo_madspin_lpj.sh \
       -d ${MCSampleGen_Dir}/config/madspin_card_lpjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# l-, jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       zprime_nlo_madspin_lmj \
       -e zprime \
       -f generateZprime_nlo_madspin_lmj.sh \
       -d ${MCSampleGen_Dir}/config/madspin_card_lmjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}
