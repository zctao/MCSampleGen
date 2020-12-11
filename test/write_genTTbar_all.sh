#!/bin/bash

nEvents=10000
nJobs=10
nCores=16
Outdir=/home/ztao/data/batch_output/MCSampleGen/20201209/

# ttbar NLO inclusive
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_nlo_incl \
       -f generateTTbar_nlo_incl.sh \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar NLO l+,jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_nlo_lpj \
       -f generateTTbar_nlo_lpj.sh \
       -c ${MCSampleGen_Dir}/config/shower_card_tt_lpjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar NLO l-,jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_nlo_lmj \
       -f generateTTbar_nlo_lmj.sh \
       -c ${MCSampleGen_Dir}/config/shower_card_tt_lmjets.dat \
       -m NLO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar LO inclusive
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_lo_incl \
       -f generateTTbar_lo_incl.sh \
       -m LO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar LO l+,jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_lo_lpj \
       -f generateTTbar_lo_lpj.sh \
       -c ${MCSampleGen_Dir}/config/shower_card_tt_lpjets.dat \
       -m LO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}

# ttbar LO l-,jets
python ${MCSampleGen_Dir}/script/writeJobFile.py \
       ttbar_lo_lmj \
       -f generateTTbar_lo_lmj.sh \
       -c ${MCSampleGen_Dir}/config/shower_card_tt_lmjets.dat \
       -m LO -n ${nEvents} -o ${Outdir} -j ${nJobs} -p ${nCores}
