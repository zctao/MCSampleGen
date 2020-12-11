#!/usr/bin/env python
from __future__ import print_function
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("name", type=str, help="Name of the run")
parser.add_argument("-n", "--nevents", type=int, default=1000,
                    help="Number of events to generate per job")
parser.add_argument("-j", "--jobs", type=int, default=1,
                    help="Number of jobs to run")
parser.add_argument("-o", "--outdir", type=str, default='.',
                    help="Output directory of the job")
parser.add_argument("-p", "--ncores", type=int, default=None,
                    help="Number of cores per job. (None = all)")
parser.add_argument("-m", "--mode", choices=['LO','NLO'], default='NLO',
                    help="Lead Order or Next to Leading Order")
parser.add_argument("-c", "--shower-card", dest='shower_card', type=str,
                    help="Shower card file path")
parser.add_argument("-f", "--filename", default='generateTTbar.sh',
                    help="Name of the job file to be submitted")
parser.add_argument("-t", "--tag", default=None,
                    help="Tag name")

args = parser.parse_args()

setup_template = """#!/bin/bash
#PBS -t 0-%(njobs)s
#PBS -o %(outdir)s/${PBS_JOBID}.out
#PBS -j oe
#PBS -l nodes=1:ppn=%(ncores)s
#PBS -m abe
#PBS -M %(email)s
#PBS -V

# set up environment
source ${HOME}/MCSampleGen/setupEnv.sh
echo MCSampleGen_Dir=${MCSampleGen_Dir}

# move to the local disk of the node
cd /tmp
mkdir -p ${PBS_JOBID}
cd ${PBS_JOBID}
echo "PWD = $PWD"
TMP_OutDir=${PWD}/output
mkdir -p ${TMP_OutDir}

nevents=%(nevents)s
echo "Generate $nevents events"

seed=${RANDOM}
echo "seed = $seed"

BatchOutput=%(outdir)s/%(name)s
# check output directory exists
if [ ! -d "$BatchOutput" ]; then
    echo "WARNING: Output directory $BatchOutput does not exist!"
    mkdir -p $BatchOutput
fi
"""

nlo_template = """
# write MG5_aMC run file
echo 'Write MC5_aMC run file'
python ${MCSampleGen_Dir}/script/writeMGRun.py ${nevents} -m NLO -s ${seed} -p %(ncores)s -r run_${seed} -t %(tag)s -c %(shower_card)s -o ${TMP_OutDir}/%(name)s -f runMG5.txt

# run MG5_aMC
echo 'Start running mg5_aMC'
python ${MCSampleGen_Dir}/MG5_aMC/bin/mg5_aMC runMG5.txt

# run Delphes
Delphes_Dir=${MCSampleGen_Dir}/MG5_aMC/Delphes
echo 'unzip hepmc file'
gunzip ${TMP_OutDir}/%(name)s/Events/run_${seed}/events_PYTHIA8_0.hepmc.gz
echo 'Start running DelphesHepMC'
${Delphes_Dir}/DelphesHepMC ${Delphes_Dir}/cards/delphes_card_CMS.tcl ${TMP_OutDir}/%(tag)s_delphes_events_${PBS_ARRAYID}.root ${TMP_OutDir}/%(name)s/Events/run_${seed}/events_PYTHIA8_0.hepmc

# copy the output to storage
echo 'Transfer Delphes output root file'
cp ${TMP_OutDir}/%(tag)s_delphes_events_${PBS_ARRAYID}.root ${BatchOutput}/.
# only copy madgraph file from one of the job
if [ "$PBS_ARRAYID" -eq "0" ]; then
    #echo "Transfer MadGraph directory $TMP_OutDir/%(name)s"
    #cp -r $TMP_OutDir/%(name)s ${BatchOutput}/
    cp runMG5.txt ${BatchOutput}/.
fi

#exit
"""

lo_template = """
# write MadGraph run file
echo 'Write MC5_aMC run file'
python ${MCSampleGen_Dir}/script/writeMGRun.py ${nevents} -m LO -s ${seed} -p %(ncores)s -r run_${seed} -t %(tag)s -c %(shower_card)s -o ${TMP_OutDir}/%(name)s -f runMG5.txt

# run MadGraph and Delphes
echo 'Start running mg5_aMC'
python ${MCSampleGen_Dir}/MG5_aMC/bin/mg5_aMC runMG5.txt

# copy the output to storage
echo 'Transfer Delphes output root file'
cp ${TMP_OutDir}/%(name)s/Events/run_${seed}/%(tag)s_delphes_events.root ${BatchOutput}/%(tag)s_delphes_events_${PBS_ARRAYID}.root
# only copy madgraph file from one of the job
if [ "$PBS_ARRAYID" -eq "0" ]; then
    #echo "Transfer MadGraph directory $TMP_OutDir/%(name)s"
    #cp -r $TMP_OutDir/%(name)s ${BatchOutput}/
    cp runMG5.txt ${BatchOutput}/.
fi

#exit
"""
joboutdir = os.path.join(args.outdir, args.name)
if not os.path.isdir(joboutdir):
    print("Create directory", joboutdir)
    os.makedirs(joboutdir)

vd = {}
vd['njobs'] = args.jobs - 1
vd['nevents'] = args.nevents
vd['name'] = args.name
vd['outdir'] = args.outdir
vd['email'] = 'ztao@phas.ubc.ca'

if args.ncores:
    vd['ncores'] = args.ncores
else:
    vd['ncores'] = "''"

if args.tag:
    vd['tag'] = args.tag
else:
    vd['tag'] = args.name

if args.shower_card:
    assert(os.path.isfile(args.shower_card))
    vd['shower_card'] = args.shower_card
else:
    vd['shower_card'] = "''"

foutput = open(args.filename, 'w')
foutput.write(setup_template % vd)
if args.mode == 'NLO':
    foutput.write(nlo_template % vd)
else:
    foutput.write(lo_template % vd)
foutput.close()

print("Create job file:", args.filename)
print("Submit to the cluster:")
print("qsub -l walltime=<hh:mm:ss>", args.filename)
