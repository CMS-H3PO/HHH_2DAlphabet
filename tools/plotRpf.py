import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ROOT
from argparse import ArgumentParser
from configs.rpfs import rpf_boosted, rpf_semiboosted


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y Run2 -r VR"

    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year(s) (e.g. 2017, Run2)",
                        required=True,
                        metavar="YEAR")
    parser.add_argument("-r", "--region", dest="region",
                        help="Analysis region (e.g. VR, VR_pass_toy, SR_pass_toy)",
                        required=True,
                        choices=["VR", "VR_pass_toy", "SR_pass_toy"],
                        metavar="REGION")
    parser.add_argument("--ext", dest="ext",
                        help="Output file extension(s) i.e. format(s) in which it should be saved (default: %(default)s)",
                        nargs='*',
                        default=[".pdf", ".png"],
                        metavar="EXT")

    (options, args) = parser.parse_known_args()

    year   = options.year
    region = options.region
    ext    = options.ext

    # to run in the batch mode (to prevent canvases from popping up)
    ROOT.gROOT.SetBatch()

    # tweak margins
    #ROOT.gStyle.SetPadTopMargin(0.10);
    #ROOT.gStyle.SetPadBottomMargin(0.10);
    #ROOT.gStyle.SetPadLeftMargin(0.10);
    ROOT.gStyle.SetPadRightMargin(0.15);

    # tweak axis title offsets
    ROOT.gStyle.SetTitleOffset(1.45, "Y")

    c = ROOT.TCanvas("c", "",1000,800)
    c.cd()

    rpf_boosted[year][region].Draw("colz")
    for e in ext:
        c.SaveAs(f"rpf_{year}_boosted_{region}{e}")

    rpf_semiboosted[year][region].Draw("colz")
    for e in ext:
        c.SaveAs(f"rpf_{year}_semiboosted_{region}{e}")
