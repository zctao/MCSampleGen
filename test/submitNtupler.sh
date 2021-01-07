# process Delphes output to make flat ntuples
# and also convert to h5 datasets
# Input: 40 Delphes output files, each with 1,000,000 ttbar l+jets events
# Split into 5 jobs each processing 8 files
# submit to cluster: qsub submitNtupler.sh

#!/bin/bash
#PBS -t 0-4
#PBS -o /home/ztao/data/batch_output/MCSampleGen/20210105/ntuples/${PBS_JOBID}.out
#PBS -j oe
#PBS -m abe
#PBS -M ztao@phas.ubc.ca
#PBS -l walltime=05:00:00
#PBS -V

# set up environment
source ${HOME}/MCSampleGen/setupEnv.sh
echo MCSampleGen_Dir=${MCSampleGen_Dir}
echo "PWD = $PWD"

# local disk of the node
if [ ! -v PBS_JOBID ]; then PBS_JOBID=43; fi    # for local testing
if [ ! -v PBS_ARRAYID ]; then PBS_ARRAYID=0; fi # for local testing

TmpWorkDir=/tmp/${USER}/${PBS_JOBID}
mkdir -p $TmpWorkDir
cd $TmpWorkDir
echo "Work directory: $TmpWorkDir"

# input
sample_dir='/home/ztao/data/batch_output/MCSampleGen/20210105'
#sample_dir='/home/ztao/data/batch_output/MCSampleGen/test'

inputfiles=""
for index in {0..3}; do
    for subch in lpj lmj; do
        newfile=${sample_dir}/ttbar_nlo_madspin_${subch}/ttbar_nlo_madspin_${subch}_delphes_events_$(($PBS_ARRAYID+$index*5)).root

        # check if the file exists
        if [ ! -f "$newfile" ]; then
            echo "$newfile does not exists! skipping..."
            continue
        fi

        echo "Adding to input file list: $newfile"
        inputfiles="$inputfiles $newfile"
    done
done
#echo $inputfiles

# output directory
outdir="$sample_dir/ntuples"
if [ ! -d "$outdir" ]; then
    echo "Create directory $outdir"
    mkdir -p $outdir
fi

# make ntuple
outfile=${outdir}/ntuple_ttbar_ljets_${PBS_ARRAYID}
python ${MCSampleGen_Dir}/script/makeDelphesNtuple.py $inputfiles -o $outfile -f h5 #-n 100000

# clean up tmp work area
rm -rf $TmpWorkDir
