# MCSampleGen

## Prerequisites

CernVM-FS

## Setup 

    git clone https://github.com/zctao/MCSampleGen.git
    . setupEnv.sh 
    
Set up MadGraph5_aMC@NLO

    wget https://launchpad.net/mg5amcnlo/2.0/2.8.x/+download/MG5_aMC_v2.8.2.tar.gz
    tar -zxf MG5_aMC_v2.8.2.tar.gz
    mv MG5_aMC_v2_8_2 MG5_aMC
    
Install Pythia8, Delphes, MA5 from the MadGraph5_aMC@NLO prompt

    cd MG5_aMC
    python bin/mg5_aMC
    
    MG5_aMC>install pythia8
    MG5_aMC>install Delphes
    MG5_aMC>install MadAnalysis5
    
## Example

Generate a shell script to produce 10000 ttbar events (MadGraph5_aMC@NLO + Pythia8 + Delphes)

    python script/writeJobFile.py ttbar_test -n 10000 -f generateTTbar.sh
    
For more options

    python script/writeJobFile.py -h

Run the script to generate the ttbar events

    . generateTTbar.sh
    
Or submit it to the Torque cluster

    qsub -l walltime=<hh:mm:ss> generateTTbar.sh