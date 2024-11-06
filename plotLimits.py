import ROOT
import json
import copy
import sys
from TwoDAlphabet.ext import CMS_lumi


mass_points = [
  (1000, 300), (1000, 600), (1000, 800),
  (1200, 300), (1200, 600), (1200, 800), (1200, 1000),
  (1600, 300), (1600, 600), (1600, 800), (1600, 1000), (1600, 1200), (1600, 1400),
  (2000, 300), (2000, 600), (2000, 800), (2000, 1000), (2000, 1200), (2000, 1600), (2000, 1800),
  (2500, 300), (2500, 600), (2500, 800), (2500, 1000), (2500, 1200), (2500, 1600), (2500, 2000), (2500, 2200), (2500, 2300),
  (3000, 300), (3000, 600), (3000, 800), (3000, 1000), (3000, 1200), (3000, 1600), (3000, 2000), (3000, 2500), (3000, 2800),
  (3500, 300), (3500, 600), (3500, 800), (3500, 1000), (3500, 1200), (3500, 1600), (3500, 2000), (3500, 2500), (3500, 2800), (3500, 3000), (3500, 3300),
  (4000, 300), (4000, 600), (4000, 800), (4000, 1000), (4000, 1200), (4000, 1600), (4000, 2000), (4000, 2500), (4000, 2800), (4000, 3500), (4000, 3800)
]


def makePlot(fit_area, year, config, polyOrder):

    channel = 'boosted'
    if 'semiboosted' in fit_area:
        channel = 'semiboosted'
    elif 'combined' in fit_area:
        channel = 'combined'

    gr_limit = copy.deepcopy(ROOT.TGraph2D())
    gr_limit.SetTitle(";m_{X} [GeV];m_{Y} [GeV];95% CL expected upper limit (" + channel + ") [fb]")

    max_xs_limit = 0.
    n = 0
    for (mX, mY) in mass_points:
        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0}...".format(sample))

        xsec = config[year][sample]["xsec"]
        #print("xsec = {0}".format(xsec))

        file_path = '{0}/{1}_area_{2}/higgsCombineTest.AsymptoticLimits.mH120.root'.format(fit_area, polyOrder, sample)

        f = ROOT.TFile.Open(file_path)

        t = f.limit
        #for e in t:
            #print(e.quantileExpected, e.limit)
        t.GetEntry(2) # get median expected limit
        limit = t.limit

        xs_limit = limit * xsec * 1000
        if xs_limit == 0.:
            print("WARNING: Limit calculation failed. xs_limit = {0}".format(xs_limit))
            continue
        else:
            print("xs_limit = {0}".format(xs_limit))

        if xs_limit > max_xs_limit:
            max_xs_limit = xs_limit

        gr_limit.SetPoint(n,mX,mY,xs_limit)

        n += 1

    print("\nMaximum xs_limit: {0}\n".format(max_xs_limit))

    c = ROOT.TCanvas("c", "",1000,900)
    c.cd()

    gr_limit.SetMinimum(0.1) # for now put by hand
    gr_limit.SetMaximum(1000) # for now put by hand

    gr_limit.Draw("cont4z")

    CMS_lumi.cmsTextSize = 0.4
    CMS_lumi.cmsTextOffset = 0.2
    CMS_lumi.lumiTextSize = 0.4
    CMS_lumi.CMS_lumi(c, 1, 11)

    c.SetLogz()

    c.SaveAs('{0}_{1}_expected_limits_2D.pdf'.format(year, channel))


if __name__ == '__main__':
    # to run in the batch mode (to prevent canvases from popping up)
    ROOT.gROOT.SetBatch()

    # set plot style
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetPalette(57)

    ROOT.gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

    # tweak margins
    ROOT.gStyle.SetPadTopMargin(0.1);
    ROOT.gStyle.SetPadBottomMargin(0.1);
    ROOT.gStyle.SetPadLeftMargin(0.12);
    ROOT.gStyle.SetPadRightMargin(0.15);

    # tweak axis title offsets
    ROOT.gStyle.SetTitleOffset(1.5, "Y");
    ROOT.gStyle.SetTitleOffset(1.25, "Z");

    # set nicer fonts
    ROOT.gStyle.SetTitleFont(42, "")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gROOT.ForceStyle()

    year = sys.argv[1]

    json_file = open("../H3PO/Analysis/xsecs.json")
    config = json.load(json_file)

    makePlot('{0}_boosted_SR_pass_toy_multiSignal'.format(year), year, config, '1')
    makePlot('{0}_semiboosted_SR_pass_toy_multiSignal'.format(year), year, config, '2')
    makePlot('{0}_combined_SR_pass_toy_multiSignal'.format(year), year, config, '1-b_2-sb')
