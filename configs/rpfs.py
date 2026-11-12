import ROOT

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
rpf_boosted["Run2"]["VR"].SetParameter(0, 6.5221254682)
rpf_boosted["Run2"]["VR"].SetParameter(1,-2.2292609588)
rpf_boosted["Run2"]["VR"].SetParameter(2,-0.1130442721)

rpf_boosted["Run2"]["VR_pass_toy"] = ROOT.TF2("rpf_Run2_boosted_VR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min_b,x_max_b,y_min_b,y_max_b,3)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(0, 7.3064110847)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(1,-2.8506943216)
rpf_boosted["Run2"]["VR_pass_toy"].SetParameter(2, 0.0706637808)

rpf_boosted["Run2"]["SR_pass_toy"] = ROOT.TF2("rpf_Run2_boosted_SR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_b["Run2"],x_min_b,x_max_b,y_min_b,y_max_b,3)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(0, 6.1311405545)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(1, 0.2183682215)
rpf_boosted["Run2"]["SR_pass_toy"].SetParameter(2,-2.8427293524)

# Run2 semiboosted (best order)
p_sb["Run2"] = Pol_1(x_min_sb, x_max_sb, y_min_sb, y_max_sb)
rpf_semiboosted["Run2"] = {}
rpf_semiboosted["Run2"]["VR"] = ROOT.TF2("rpf_Run2_semiboosted_VR;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["VR"].SetParameter(0, 4.0018130130)
rpf_semiboosted["Run2"]["VR"].SetParameter(1,-1.9533907677)
rpf_semiboosted["Run2"]["VR"].SetParameter(2, 0.1348742549)

rpf_semiboosted["Run2"]["VR_pass_toy"] = ROOT.TF2("rpf_Run2_semiboosted_VR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(0, 3.9452572041)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(1,-1.4665994229)
rpf_semiboosted["Run2"]["VR_pass_toy"].SetParameter(2, 0.0280466268)

rpf_semiboosted["Run2"]["SR_pass_toy"] = ROOT.TF2("rpf_Run2_semiboosted_SR_pass_toy;m_{jjj} [GeV];m_{jj} [GeV]",p_sb["Run2"],x_min_sb,x_max_sb,y_min_sb,y_max_sb,3)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(0, 5.4446397560)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(1,-4.8612696498)
rpf_semiboosted["Run2"]["SR_pass_toy"].SetParameter(2, 1.6455114350)
