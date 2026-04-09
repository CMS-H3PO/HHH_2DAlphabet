import ROOT
import json
import copy
import sys
from TwoDAlphabet.ext import CMS_lumi
from os.path import isfile, join
from argparse import ArgumentParser


mass_points = [
  (1000, 300), (1000, 600), (1000, 800),
  (1200, 300), (1200, 600), (1200, 800), (1200, 1000),
  (1600, 300), (1600, 600), (1600, 800), (1600, 1000), (1600, 1200), (1600, 1400),
  (2000, 300), (2000, 600), (2000, 800), (2000, 1000), (2000, 1200), (2000, 1600), (2000, 1800),
  (2500, 300), (2500, 600), (2500, 800), (2500, 1000), (2500, 1200), (2500, 1600), (2500, 2000), (2500, 2200), (2500, 2300),
  (3000, 300), (3000, 600), (3000, 800), (3000, 1000), (3000, 1200), (3000, 1600), (3000, 2000), (3000, 2500), (3000, 2800),
  (3500, 300), (3500, 600), (3500, 800), (3500, 1000), (3500, 1200), (3500, 1600), (3500, 2000), (3500, 2500), (3500, 2800), (3500, 3000), (3500, 3300),
  (4000, 300), (4000, 600), (4000, 800), (4000, 1000), (4000, 1200), (4000, 1600), (4000, 2000), (4000, 2500), (4000, 2800), (4000, 3000), (4000, 3500), (4000, 3800)
]


def makePlot(fit_area, year, config, polyOrder, plotDimension, mX_fixed, mY_fixed, logY, inputDir, minY, maxY):

    channel = 'boosted'
    if 'semiboosted' in fit_area:
        channel = 'semiboosted'
    elif 'combined' in fit_area:
        channel = 'combined'
        
    if (plotDimension == "2D"):
        gr_limit = copy.deepcopy(ROOT.TGraph2D())
        title = ";m_{{X}} [GeV];m_{{Y}} [GeV];95% CL expected upper limit ({0}) [fb]".format(channel)
    else:
        gr_limit = copy.deepcopy(ROOT.TGraph())
        if (mX_fixed is not None):
            title = "m_{{X}} = {0};m_{{Y}} [GeV];95% CL expected upper limit ({1}) [fb]".format(mX_fixed, channel)
        else:
            title = "m_{{Y}} = {0};m_{{X}} [GeV];95% CL expected upper limit ({1}) [fb]".format(mY_fixed, channel)
            
    gr_limit.SetTitle(title) 

    max_xs_limit = 0.
    n = 0
    
    for (mX, mY) in mass_points:
        
        if (plotDimension == "1D"):
            if (mX_fixed is not None) and mX != mX_fixed:
                continue
            if (mY_fixed is not None) and mY != mY_fixed:
                continue
        
        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0}...".format(sample))

        xsec = config[year][sample]["xsec"]
        #print("xsec = {0}".format(xsec))

        file_path = join(inputDir,'{0}/{1}/{2}_area/higgsCombineTest.AsymptoticLimits.mH120.root'.format(fit_area, sample, polyOrder))
        #print(file_path)

        if not isfile(file_path):
               print ("Sample file for ({0}, {1}) not found".format(mX, mY))
               continue

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
            
        if (plotDimension == "2D"):   
            gr_limit.SetPoint(n, mX, mY, xs_limit)
        else:
            if (mX_fixed is not None):
                gr_limit.SetPoint(n, mY, xs_limit)
            else:
                gr_limit.SetPoint(n, mX, xs_limit)

        n += 1
        
    if (n == 0):
        print("No (mX, mY) points were found for specified mX (or mY) value")
        sys.exit(1)

    print("\nNumber of points: {0}\n".format(n))
    print("\nMaximum xs_limit: {0}\n".format(max_xs_limit))

    c = ROOT.TCanvas("c", "",1000,900)
    c.cd()
    if (plotDimension == "1D") and (logY == True): 
        c.SetLogy()

    if (plotDimension == "1D"):
        if (minY is not None): 
           gr_limit.SetMinimum(minY)
        if (maxY is not None):
           gr_limit.SetMaximum(maxY) 

    if (plotDimension == "2D"):
        gr_limit.Draw("cont4z")
    else:
        gr_limit.Draw("AL*")

    CMS_lumi.cmsTextSize = 0.4
    CMS_lumi.cmsTextOffset = 0.2
    CMS_lumi.lumiTextSize = 0.4
    CMS_lumi.CMS_lumi(c, 1, 11)

    c.SetLogz()
    
    if (plotDimension == "2D"):
        plotTitle = "{0}_{1}_expected_limits_2D.pdf".format(year, channel)
    else:
        if (mX_fixed is not None):
            plotTitle = "{0}_{1}_expected_limits_1D_for_mX_{2}.pdf".format(year, channel, mX_fixed)
        else:
            plotTitle = "{0}_{1}_expected_limits_1D_for_mY_{2}.pdf".format(year, channel, mY_fixed)

    c.SaveAs(plotTitle)
    
    
def safe_int(value, name):   # convert input options to integers
    try:
        return int(value)
    except (TypeError, ValueError):
        print(f"Warning: {name} must be an integer.")
        return None


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
    
    # set graph title position for 1D plots
    ROOT.gStyle.SetTitleX(0.38)   # horizontal position (0 = left, 1 = right)
    ROOT.gStyle.SetTitleY(0.98)  # vertical position (0 = bottom, 1 = top)
    ROOT.gStyle.SetTitleBorderSize(0)
    #ROOT.gStyle.SetTitleAlign(23)
    
    parser = ArgumentParser(description="To create a 2D plot leave both mX and mY unspecified. To create a 1D plot for a fixed mX or mY value, specify the corresponding value of mX or mY. You can not specify both mX and mY.")
    
    # input parameters
    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year (default: %(default)s)",
                        default="2017",
                        metavar="YEAR")

    parser.add_argument("-mX", "--massX", dest="mX",
                        help="Integer value of X mass for which 1D plot is created (default: %(default)s)",
                        default=None,
                        metavar="X mass")
    
    parser.add_argument("-mY", "--massY", dest="mY",
                        help="Integer value of Y mass for which 1D plot is created (default: %(default)s)",
                        default=None,
                        metavar="Y mass")
    
    parser.add_argument("-logY", dest="logY", action='store_true',
                        help="Sets log scale for Y-axis of 1D plots (default: %(default)s)",
                        default=False)
    
    parser.add_argument("-i", "--input", dest="input",
                        help="Input directory path (default: %(default)s)",
                        default="/users/ferencek/HHH/HHH_2DAlphabet/20260401/",
                        metavar="INPUT")
    
    parser.add_argument("-minY", dest="minY",
                        help="Y-axis minimum for 1D plot (None means automatic) (default: %(default)s)",
                        default=None,
                        metavar="Y_MIN")
    
    parser.add_argument("-maxY", dest="maxY",
                        help="Y-axis maximum for 1D plot (None means automatic) (default: %(default)s)",
                        default=None,
                        metavar="Y_MAX")
    
    (options, args) = parser.parse_known_args()
    
    year = options.year
    mX_fixed = safe_int(options.mX, "mX") if options.mX is not None else None
    mY_fixed = safe_int(options.mY, "mY") if options.mY is not None else None
    minY = safe_int(options.minY, "minY") if options.minY is not None else None
    maxY = safe_int(options.maxY, "maxY") if options.maxY is not None else None
    
     # If conversion failed, stop
    if ((options.mX is not None and mX_fixed is None) or (options.mY is not None and mY_fixed is None) or (options.minY is not None and minY is None) or (options.maxY is not None and maxY is None)):
        print("Invalid input: some arguments could not be parsed as integers.")
        sys.exit(1)
        
    if ((minY is not None) and (maxY is not None) and (minY >= maxY)):
        print("Warning: minY >= maxY")
        sys.exit(1)
    
    print("year = ", year, "   mX = ", mX_fixed, "    mY = ", mY_fixed, "  logY = ", options.logY, "     input folder = ", options.input, "   minY = ", minY, "   maxY = ", maxY)
    
    if (mX_fixed is None) and (mX_fixed is None):
        plotDimension="2D"
    if (mX_fixed is not None) and (mY_fixed is None):
        plotDimension="1D"
    if (mX_fixed is None) and (mY_fixed is not None):
        plotDimension="1D"
    if (mX_fixed is not None) and (mY_fixed is not None):
        print ("Warning: You can not specify both mX and mY parameters. To create a 2D plot leave both mX and mY unspecified. To create a 1D plot for a fixed mX or mY value, specify the corresponding value of mX or mY.")
        sys.exit(1)


    json_file = open("../H3PO/Analysis/config/xsecs.json")
    
    config = json.load(json_file)

    makePlot('{0}_boosted_SR_pass_toy_multiSignal'.format(year), year, config, '1', plotDimension, mX_fixed, mY_fixed, options.logY, options.input, minY, maxY)
    makePlot('{0}_semiboosted_SR_pass_toy_multiSignal'.format(year), year, config, '1', plotDimension, mX_fixed, mY_fixed, options.logY, options.input, minY, maxY)
    makePlot('{0}_combined_SR_pass_toy_multiSignal'.format(year), year, config, '1-b_1-sb', plotDimension, mX_fixed, mY_fixed, options.logY, options.input, minY, maxY)
    

