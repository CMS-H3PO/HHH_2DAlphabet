import ROOT
from argparse import ArgumentParser

# variable ranges
x_min_b = 800.
x_min_sb = 600.
x_max_b = x_max_sb = 4500.
y_min_b = y_min_sb = 200.
y_max_b = y_max_sb = 4500.

# base class for polynomials
class Pol_base:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
# classes for polynomials
class Pol_0(Pol_base):
    def __call__(self, arr, par):
        # variable transformations to [0,1] range
        x = (arr[0]-self.x_min)/(self.x_max-self.x_min)
        y = (arr[1]-self.y_min)/(self.y_max-self.y_min)

        return 0.01*par[0]

class Pol_1(Pol_base):
    def __call__(self, arr, par):
        # variable transformations to [0,1] range
        x = (arr[0]-self.x_min)/(self.x_max-self.x_min)
        y = (arr[1]-self.y_min)/(self.y_max-self.y_min)

        return 0.01*(par[0]+par[1]*x+par[2]*y)

class Pol_2(Pol_base):
    def __call__(self, arr, par):
        # variable transformations to [0,1] range
        x = (arr[0]-self.x_min)/(self.x_max-self.x_min)
        y = (arr[1]-self.y_min)/(self.y_max-self.y_min)

        return 0.01*(par[0]+par[1]*x+par[2]*y+par[3]*x*y+par[4]*x**2+par[5]*y**2)


# various dictionaries
p_b = {}
p_sb = {}
rpf_boosted = {}
rpf_semiboosted = {}

# fail-to-pass transfer functions
# Run2 boosted (best order)
p_b["Run2"] = Pol_1(x_min_b, x_max_b, y_min_b, y_max_b)
rpf_boosted["Run2"] = {}
rpf_boosted["Run2"]["VR"] = ROOT.TF2("rpf_Run2_boosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min_b,x_max_b,y_min_b,y_max_b,3)
rpf_boosted["Run2"]["VR"].SetParameter(0, 6.5276795029)
rpf_boosted["Run2"]["VR"].SetParameter(1,-2.2344563476)
rpf_boosted["Run2"]["VR"].SetParameter(2,-0.1114032803)

rpf_boosted["Run2"]["VR_pass_toy"] = ROOT.TF2("rpf_Run2_boosted_VR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min_b,x_max_b,y_min_b,y_max_b,3)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(0, 7.3064110847)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(1,-2.8506943216)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(2, 0.0706637808)

rpf_boosted["Run2"]["SR_pass_toy"] = ROOT.TF2("rpf_Run2_boosted_SR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min_b,x_max_b,y_min_b,y_max_b,3)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(0, 6.5827028382)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(1,-1.1471642640)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(2,-1.7985999678)

# Run2 semiboosted (best order)
p_sb["Run2"] = Pol_1(x_min_sb, x_max_sb, y_min_sb, y_max_sb)
rpf_semiboosted["Run2"] = {}
rpf_semiboosted["Run2"]["VR"] = ROOT.TF2("rpf_Run2_semiboosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["VR"].SetParameter(0, 4.1038800774)
rpf_semiboosted["Run2"]["VR"].SetParameter(1,-2.0898134846)
rpf_semiboosted["Run2"]["VR"].SetParameter(2, 0.1379286225)

rpf_semiboosted["Run2"]["VR_pass_toy"] = ROOT.TF2("rpf_Run2_semiboosted_VR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(0, 3.9452572041)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(1,-1.4665994229)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(2, 0.0280466268)

rpf_semiboosted["Run2"]["SR_pass_toy"] = ROOT.TF2("rpf_Run2_semiboosted_SR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(0, 4.3327365420)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(1,-1.8069879838)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(2,-0.3402843551)

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

    (options, args) = parser.parse_known_args()

    year   = options.year
    region = options.region

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

    c.SaveAs(f"rpf_{year}_boosted_{region}.png")

    rpf_semiboosted[year][region].Draw("colz")

    c.SaveAs(f"rpf_{year}_semiboosted_{region}.png")
