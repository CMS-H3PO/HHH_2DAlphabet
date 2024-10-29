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
rpf_boosted_VR = {}
rpf_semiboosted_VR = {}

# fail-to-pass transfer functions
# 2017 boosted (best order)
p_b["2017"] = Pol_1()
rpf_boosted_VR["2017"] = ROOT.TF2("rpf_2017_boosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_b["2017"],x_min,x_max,y_min,y_max,3)
rpf_boosted_VR["2017"].SetParameter(0, 6.8436666543)
rpf_boosted_VR["2017"].SetParameter(1,-3.6156471188)
rpf_boosted_VR["2017"].SetParameter(2, 1.5817990449)

# 2017 semiboosted (best order)
p_sb["2017"] = Pol_2()
rpf_semiboosted_VR["2017"] = ROOT.TF2("rpf_2017_semiboosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["2017"],x_min,x_max,y_min,y_max,6)
rpf_semiboosted_VR["2017"].SetParameter(0,  7.0566158433)
rpf_semiboosted_VR["2017"].SetParameter(1,-12.5188265625)
rpf_semiboosted_VR["2017"].SetParameter(2,  0.3226356388)
rpf_semiboosted_VR["2017"].SetParameter(3, 13.4650381833)
rpf_semiboosted_VR["2017"].SetParameter(4,  6.3150490979)
rpf_semiboosted_VR["2017"].SetParameter(5,-11.5925476469)

# Run2 boosted (best order)
p_b["Run2"] = Pol_1()
rpf_boosted_VR["Run2"] = ROOT.TF2("rpf_Run2_boosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min,x_max,y_min,y_max,3)
rpf_boosted_VR["Run2"].SetParameter(0, 6.6233835282)
rpf_boosted_VR["Run2"].SetParameter(1,-1.7767097306)
rpf_boosted_VR["Run2"].SetParameter(2,-0.7376929257)

# Run2 semiboosted (best order)
p_sb["Run2"] = Pol_1()
rpf_semiboosted_VR["Run2"] = ROOT.TF2("rpf_Run2_semiboosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min,x_max,y_min,y_max,3)
rpf_semiboosted_VR["Run2"].SetParameter(0, 5.9068958750)
rpf_semiboosted_VR["Run2"].SetParameter(1,-4.5963924421)
rpf_semiboosted_VR["Run2"].SetParameter(2,-0.0621328287)


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
    
    rpf_boosted_VR[options.year].Draw("colz")

    c.SaveAs("rpf_{}_boosted_VR_pass_toy.png".format(options.year))

    rpf_semiboosted_VR[options.year].Draw("colz")

    c.SaveAs("rpf_{}_semiboosted_VR_pass_toy.png".format(options.year))
