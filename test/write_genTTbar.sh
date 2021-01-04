#!/bin/bash
nEvents=1000000
nJobs=20
nCores=16

Outdir=/home/ztao/data/batch_output/MCSampleGen/20210105/

# top decay with MadSpin
# ttbar NLO l+, jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_nlo_madspin_lpj \
       -f generateTTbar_nlo_madspin_lpj.sh \
       -d ${MCSampleGen_Dir}/config/madspin_card_lpjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar NLO l-, jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_nlo_madspin_lmj \
       -f generateTTbar_nlo_madspin_lmj.sh \
       -d ${MCSampleGen_Dir}/config/madspin_card_lmjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}
