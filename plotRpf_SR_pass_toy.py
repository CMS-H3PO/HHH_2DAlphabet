import ROOT
from argparse import ArgumentParser

# variable ranges
x_min = 1000.
x_max = 4500.
y_min = 200.
y_max = 4500.

# polynomials
class Pol_1:
    def __call__(self, arr, par):
        # variable transformations to [0,1] range
        x = (arr[0]-x_min)/(x_max-x_min)
        y = (arr[1]-y_min)/(y_max-y_min)
        
        return 0.01*(par[0]+par[1]*x+par[2]*y)


class Pol_2:
    def __call__(self, arr, par):
        # variable transformations to [0,1] range
        x = (arr[0]-x_min)/(x_max-x_min)
        y = (arr[1]-y_min)/(y_max-y_min)
        
        return 0.01*(par[0]+par[1]*x+par[2]*y+par[3]*x*y+par[4]*x**2+par[5]*y**2)


# various dictionaries
p_b = {}
p_sb = {}
rpf_boosted_SR = {}
rpf_semiboosted_SR = {}

# fail-to-pass transfer functions
# 2017 boosted (best order)
p_b["2017"] = Pol_1()
rpf_boosted_SR["2017"] = ROOT.TF2("rpf_2017_boosted_SR;m_{jjj} [GeV];m_{jj} [GeV]",p_b["2017"],x_min,x_max,y_min,y_max,3)
rpf_boosted_SR["2017"].SetParameter(0, 6.9722293911)
rpf_boosted_SR["2017"].SetParameter(1,-2.6216322625)
rpf_boosted_SR["2017"].SetParameter(2, 1.1057040331)

# 2017 semiboosted (best order)
p_sb["2017"] = Pol_1()
rpf_semiboosted_SR["2017"] = ROOT.TF2("rpf_2017_semiboosted_SR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["2017"],x_min,x_max,y_min,y_max,3)
rpf_semiboosted_SR["2017"].SetParameter(0, 6.3419944445)
rpf_semiboosted_SR["2017"].SetParameter(1,-7.9777135785)
rpf_semiboosted_SR["2017"].SetParameter(2, 2.0819610327)

# Run2 boosted (best order)
p_b["Run2"] = Pol_1()
rpf_boosted_SR["Run2"] = ROOT.TF2("rpf_Run2_boosted_SR;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min,x_max,y_min,y_max,3)
rpf_boosted_SR["Run2"].SetParameter(0, 6.5297055558)
rpf_boosted_SR["Run2"].SetParameter(1,-2.5859269353)
rpf_boosted_SR["Run2"].SetParameter(2, 0.7874599276)

# Run2 semiboosted (best order)
p_sb["Run2"] = Pol_1()
rpf_semiboosted_SR["Run2"] = ROOT.TF2("rpf_Run2_semiboosted_SR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min,x_max,y_min,y_max,3)
rpf_semiboosted_SR["Run2"].SetParameter(0, 5.9207814471)
rpf_semiboosted_SR["Run2"].SetParameter(1,-4.5875310779)
rpf_semiboosted_SR["Run2"].SetParameter(2,-0.2105124716)


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y 2017"

    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year(s) (e.g. 2017, Run2)",
                        required=True,
                        metavar="YEAR")

    (options, args) = parser.parse_known_args()

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
    
    rpf_boosted_SR[options.year].Draw("colz")

    c.SaveAs("rpf_{}_boosted_SR_pass_toy.png".format(options.year))

    rpf_semiboosted_SR[options.year].Draw("colz")

    c.SaveAs("rpf_{}_semiboosted_SR_pass_toy.png".format(options.year))
