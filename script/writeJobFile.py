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
parser.add_argument('-e', '--event-type', dest='event_type',
                    choices=['ttbar', 'zprime'], default='ttbar',
                    help="Which kind of events to generate")
parser.add_argument("-d", "--madspin-card", dest="madspin_card", type=str,
                    help="Madspin card file path")
parser.add_argument("-c", "--shower-card", dest='shower_card', type=str,
                    help="Shower card file path")
parser.add_argument("-f", "--filename", default='generateTTbar.sh',
                    help="Name of the job file to be submitted")
parser.add_argument("-t", "--tag", default=None,
                    help="Tag name")
parser.add_argument("--pileup", type=str,
                    help="Path to the pileup file for Delphes")

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
echo "PWD = $PWD"

BatchOutput=`realpath %(outdir)s/%(name)s`
# check output directory exists
if [ ! -d "$BatchOutput" ]; then
    echo "WARNING: Output directory $BatchOutput does not exist!"
    echo "Create directory $BatchOutput"
    mkdir -p $BatchOutput
fi

# move to the local disk of the node
if [ ! -v PBS_JOBID ]; then PBS_JOBID=42; fi
if [ ! -v PBS_ARRAYID ]; then PBS_ARRAYID=0; fi
TmpWorkDir=/tmp/${USER}/${PBS_JOBID}
mkdir -p ${TmpWorkDir}
cd ${TmpWorkDir}
echo "Work directory: $TmpWorkDir"

nevents=%(nevents)s
echo "Generate $nevents events"

seed=${RANDOM}
echo "seed = $seed"
"""

nlo_template = """
# write MG5_aMC run file
echo 'Write MC5_aMC run file'
python ${MCSampleGen_Dir}/script/writeMGRun.py ${nevents} -m NLO -e %(event_type)s -s ${seed} -p %(ncores)s -r run_${seed} -t %(tag)s -d %(decay_card)s -c %(shower_card)s -o ${TmpWorkDir}/%(name)s -f runMG5.txt

# run MG5_aMC
echo 'Start running mg5_aMC'
python ${MCSampleGen_Dir}/MG5_aMC/bin/mg5_aMC runMG5.txt

# run Delphes
Delphes_Dir=${MCSampleGen_Dir}/MG5_aMC/Delphes
file_hepmc="$TmpWorkDir/%(name)s/Events/%(runoutdir)s/events_PYTHIA8_0.hepmc"
file_hepmcgz="$file_hepmc".gz
echo "Unzip hepmc file: $file_hepmcgz"
gunzip $file_hepmcgz
echo 'Start running DelphesHepMC'
file_delphes=${BatchOutput}/%(tag)s_delphes_events_${PBS_ARRAYID}.root
%(copy_minbias)s
${Delphes_Dir}/DelphesHepMC %(delphes_card)s $file_delphes $file_hepmc

# Copy MadGraph run script from only the first job since they are identical
echo 'Copy MadGraph script to the output directory'
if [ "$PBS_ARRAYID" -eq "0" ]; then
    cp runMG5.txt ${BatchOutput}/.
fi

# Clean up
rm -rf ${TmpWorkDir}
#exit
"""

lo_template = """
# write MadGraph run file
echo 'Write MC5_aMC run file'
python ${MCSampleGen_Dir}/script/writeMGRun.py ${nevents} -m LO -s ${seed} -p %(ncores)s -r run_${seed} -t %(tag)s -d %(decay_card)s -c %(shower_card)s --delphes-card %(delphes_card)s -o ${BatchOutput}/%(name)s_${PBS_ARRAYID} -f runMG5.txt

# run MadGraph and Delphes
%(copy_minbias)s
echo 'Start running mg5_aMC'
python ${MCSampleGen_Dir}/MG5_aMC/bin/mg5_aMC runMG5.txt

# Move the output file
# copy the output to storage
file_delphes=${BatchOutput}/%(name)s_${PBS_ARRAYID}/Events/%(runoutdir)s/%(tag)s_delphes_events.root
echo "Move Delphes output file $file_delphes to ${BatchOutput}/%(tag)s_delphes_events_${PBS_ARRAYID}.root"
mv $file_delphes ${BatchOutput}/%(tag)s_delphes_events_${PBS_ARRAYID}.root

# Copy MadGraph run script from only the first job since they are identical
echo 'Copy MadGraph script to the output directory'
if [ "$PBS_ARRAYID" -eq "0" ]; then
    cp runMG5.txt ${BatchOutput}/.
fi

# Clean up
rm -rf ${TmpWorkDir}
#exit
"""
parser.add_argument("--delphes-card", dest='delphes_card', type=str,
                    default='${Delphes_Dir}/cards/delphes_card_CMS.tcl',
                    help="Delphes card file path")

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

if args.madspin_card:
    assert(os.path.isfile(args.madspin_card))
    vd['decay_card'] = os.path.abspath(args.madspin_card)
    vd['runoutdir'] = 'run_${seed}_decayed_1'
else:
    vd['decay_card'] = "''"
    vd['runoutdir'] = 'run_${seed}'

if args.shower_card:
    assert(os.path.isfile(args.shower_card))
    vd['shower_card'] = os.path.abspath(args.shower_card)
else:
    vd['shower_card'] = "''"

# Delphes card and pileup file
if args.pileup:
    assert(os.path.isfile(args.pileup))
    filepath_pileup = os.path.abspath(args.pileup)
    vd['delphes_card'] = '${Delphes_Dir}/cards/delphes_card_CMS_PileUp.tcl'
    vd['copy_minbias'] = 'cp {} .'.format(filepath_pileup)
else:
    vd['delphes_card'] = '${Delphes_Dir}/cards/delphes_card_CMS.tcl'
    vd['copy_minbias'] = '#'

vd['event_type'] = args.event_type

foutput = open(args.filename, 'w')
foutput.write(setup_template % vd)
if args.mode == 'NLO':
    foutput.write(nlo_template % vd)
else:
    foutput.write(lo_template % vd)
foutput.close()

print("Create job file:", args.filename)
print("To submit the job to cluster:")
print("qsub -l walltime=<hh:mm:ss>", args.filename)
