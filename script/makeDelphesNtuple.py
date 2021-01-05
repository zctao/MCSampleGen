from delphesAnalyzer import makeNtuple_ttbar_ljets
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfiles", nargs='+', help="Input file paths")
parser.add_argument("-o", "--outputname", default="ntuple")
parser.add_argument("-t", "--treename", default="Delphes")
parser.add_argument("-f", "--format", choices=['npz','h5'])
args = parser.parse_args()

makeNtuple_ttbar_ljets(args.inputfiles, args.outputname, treename=args.treename,
                       arrayFormat=args.format)
