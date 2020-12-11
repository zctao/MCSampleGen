#!/bin/bash

export MCSampleGen_Dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# cf. https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself

export Output_Dir=${MCSampleGen_Dir}/output

lcgVersion=LCG_97
arch=x86_64-centos7-gcc8-opt

# Get a compatible version of python and ROOT for MadGraph and Delphes
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh ${lcgVersion} ${arch}

# PDF
export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current/:/cvmfs/sft.cern.ch/lcg/views/${lcgVersion}/${arch}/share/LHAPDF/

# texlive needed for MadAnalysis5, optional
export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux/:$PATH

# python path
export PYTHONPATH=${MCSampleGen_Dir}/python:$PYTHONPATH

# set up Delphes analysis environment
export Delphes_Dir=${MCSampleGen_Dir}/MG5_aMC/Delphes
export PYTHONPATH=${Delphes_Dir}/python:${PYTHONPATH}
export LD_LIBRARY_PATH=${Delphes_Dir}:${LD_LIBRARY_PATH}
