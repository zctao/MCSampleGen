#!/usr/bin/env python
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('nevents', type=int,
                    help="Number of events to generate")
parser.add_argument('-m', '--mode', choices=['LO', 'NLO'], default='NLO',
                    help="Leading Order or Next to Leading Order")
parser.add_argument('-f', '--filename', default='run_mg5_aMC.txt',
                    help="Name of the text file written by this script")
parser.add_argument('-s', '--seed', default=0,
                    help="Random number generator seed for MadGraph")
parser.add_argument('-p', '--ncores', default=None,
                    help="number of cores")
parser.add_argument('-o', '--runoutdir', default='.',
                    help="Output directory for mg5_aMC run")
parser.add_argument('-r', '--runname', default='run_tt',
                    help="Run name")
parser.add_argument('-t', '--tagname', default='tag_1',
                    help="Tag name")
parser.add_argument('-d', '--madspin-card', dest='madspin_card', default=None,
                    help="Madspin card file path")
parser.add_argument('-c', '--shower-card', dest='shower_card', default=None,
                    help="Shower card file path")
parser.add_argument('--delphes-card', dest='delphes_card', default=None,
                    help="Delphes card file path for LO mode")

args = parser.parse_args()

ttbar_aMCatNLO_template = """# MadGraph5 configuration
# multicore mode
set run_mode 2
# number of cores, default None ( = all)
set nb_core %(number_cores)s
# generate process
generate p p > t t~ [QCD]
output %(outputdir)s
launch -n %(run_name)s
shower = PYTHIA8
%(madspin_switch)s
#order = NLO
done
set run_card nevents %(nevents)s
set run_card iseed %(rng_seed)s
set run_card run_tag %(tag_name)s
set pdlabel lhapdf
set lhaid 260000 # NNPDF30_nlo_as_0118
#set param_card MT 172
%(madspin_card)s
%(shower_card)s
done
"""

ttbar_MG5_template = """# MadGraph5 configuration
# multicore mode
set run_mode 2
# number of cores, default None ( = all)
set nb_core %(number_cores)s
# generate process
generate p p > t t~
output %(outputdir)s
launch -n %(run_name)s
shower = Pythia8
detector = Delphes
%(madspin_switch)s
analysis = OFF
done
set run_card nevents %(nevents)s
set run_card iseed %(rng_seed)s
set run_card run_tag %(tag_name)s
set pdlabel lhapdf
set lhaid 260000 # NNPDF30_nlo_as_0118
#set param_card MT 172
%(madspin_card)s
%(shower_card)s
%(delphes_card)s
done
"""

vd = {}
vd['nevents'] = args.nevents
vd['rng_seed'] = args.seed
vd['outputdir'] = args.runoutdir
vd['run_name'] = args.runname
vd['tag_name'] = args.tagname

if args.madspin_card:
    assert(os.path.isfile(args.madspin_card))
    vd['madspin_switch'] = 'madspin = ON'
    vd['madspin_card'] = os.path.abspath(args.madspin_card)
else:
    vd['madspin_switch'] = '#'
    vd['madspin_card'] = '#'

if args.shower_card:
    assert(os.path.isfile(args.shower_card))
    vd['shower_card'] = os.path.abspath(args.shower_card)
else:
    vd['shower_card'] = '#'

if args.delphes_card:
    assert(os.path.isfile(args.delphes_card))
    vd['delphes_card'] = os.path.abspath(args.delphes_card)
else:
    vd['delphes_card'] = '#'

if args.ncores:
    vd['number_cores'] = args.ncores
else:
    vd['number_cores'] = 'None'

if args.mode == 'NLO':
    open(args.filename,'w').write(ttbar_aMCatNLO_template % vd)
else:
    open(args.filename,'w').write(ttbar_MG5_template % vd)
