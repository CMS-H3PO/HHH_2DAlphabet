import ROOT
import json
import sys
from TwoDAlphabet.ext import CMS_lumi
from os.path import isfile, join, basename, normpath
from pathlib import Path
from argparse import ArgumentParser, BooleanOptionalAction

# Credits: Claude AI

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


def getChannel(inputDir):
    """Infer the channel from the name of the input folder (None if it can not be inferred)."""
    name = basename(normpath(inputDir))
    if 'semiboosted' in name:
        return 'semiboosted'
    if 'combined' in name:
        return 'combined'
    if 'boosted' in name:
        return 'boosted'
    return None


def getLimits(inputDir, fit_area, year, config, m_X=None, m_Y=None):
    """Collect median expected cross-section limits [fb] for all available mass points in inputDir.
       Returns a dict {(mX, mY): xs_limit} ordered as in mass_points."""

    print("\n==> Reading limits from {0}".format(inputDir))

    limits = {}

    for (mX, mY) in mass_points:

        if (m_X is not None) and m_X != mX:
            continue
        if (m_Y is not None) and m_Y != mY:
            continue

        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0}...".format(sample))

        xsec = config[year][sample]["xsec"]

        file_path = join(inputDir, sample, fit_area, 'higgsCombineTest.AsymptoticLimits.mH120.root')

        if not isfile(file_path):
            print("Sample file for ({0}, {1}) not found".format(mX, mY))
            continue

        f = ROOT.TFile.Open(file_path)
        if not f or f.IsZombie():
            print("WARNING: Could not open {0}".format(file_path))
            continue

        t = f.Get("limit")
        limit = None
        if t:
            for e in t:
                if abs(e.quantileExpected - 0.5) < 1e-3:  # median expected limit
                    limit = e.limit
                    break
        f.Close()

        if limit is None:
            print("WARNING: Median expected limit not found in {0}".format(file_path))
            continue

        xs_limit = limit * xsec * 1000
        if xs_limit == 0.:
            print("WARNING: Limit calculation failed. xs_limit = {0}".format(xs_limit))
            continue
        else:
            print("xs_limit = {0}".format(xs_limit))

        limits[(mX, mY)] = xs_limit

    print("\nNumber of points: {0}".format(len(limits)))
    if limits:
        print("Maximum xs_limit: {0}\n".format(max(limits.values())))

    return limits


def getRatios(num, den):
    """Ratio num/den for mass points present in both inputs."""
    ratios = {}
    for key in mass_points:
        if (key in num) and (key in den):
            ratios[key] = num[key] / den[key]
            print("({0}, {1}): {2}, {3}, {4}".format(key[0], key[1], num[key], den[key], ratios[key]))
        elif (key in num) or (key in den):
            print("WARNING: Point ({0}, {1}) missing in one of the inputs. Skipping it in the ratio.".format(*key))

    if ratios:
        print("\nNumber of points: {0}".format(len(ratios)))
        print("Minimum ratio: {0}".format(min(ratios.values())))
        print("Maximum ratio: {0}\n".format(max(ratios.values())))

    return ratios


def make1DGraph(values, m_X):
    """TGraph vs mY (if mX is fixed) or vs mX (if mY is fixed), sorted along the x-axis."""
    g = ROOT.TGraph()
    points = sorted(((mY if m_X is not None else mX), v) for (mX, mY), v in values.items())
    for i, (x, v) in enumerate(points):
        g.SetPoint(i, x, v)
    return g


def make2DGraph(values):
    g = ROOT.TGraph2D()
    for i, ((mX, mY), v) in enumerate(values.items()):
        g.SetPoint(i, mX, mY, v)
    return g


def getLegendLabels(legends, inputs, ratio):
    """Legend labels for 1D curves. In ratio mode either N-1 labels (used as given) or
       N labels (combined into 'label_i / label_0') are accepted."""
    names = legends if legends else [basename(normpath(d)) for d in inputs]
    if ratio:
        if len(names) == len(inputs) - 1:
            return names
        return ["{0} / {1}".format(n, names[0]) for n in names[1:]]
    return names


def makePlot(inputs, fit_area, year, config, plotDimension, m_X, m_Y, logY, minY, maxY, logZ, minZ, maxZ, ratio, legends, output, extensions):

    limits = []
    for inputDir in inputs:
        l = getLimits(inputDir, fit_area, year, config, m_X, m_Y)
        if not l:
            print("No (mX, mY) points were found in {0} (for the specified mX or mY value)".format(inputDir))
            sys.exit(1)
        limits.append(l)

    # channel label (only if it is unambiguous)
    channels = {getChannel(d) for d in inputs}
    channel = next(iter(channels)) if len(channels) == 1 else None
    chLabel = " ({0})".format(channel) if channel else ""

    c = ROOT.TCanvas("c", "", 1000, 900)
    c.cd()

    keep = []  # keep Python references to drawn objects until the canvas is saved

    if plotDimension == "2D":
        if len(inputs) == 1:
            graph = make2DGraph(limits[0])
            graph.SetTitle(";m_{X} [GeV];m_{Y} [GeV];95% CL expected upper limit" + chLabel + " [fb]")
            if logZ:
                c.SetLogz()
        else:
            print("\n==> Computing ratio (second input / first input)\n")
            values = getRatios(limits[1], limits[0])
            if not values:
                print("No common (mX, mY) points found in the two inputs")
                sys.exit(1)
            graph = make2DGraph(values)
            zTitle = "Ratio of 95% CL expected upper limits" + chLabel
            if legends and len(legends) == 2:
                zTitle += " ({1} / {0})".format(*legends)
            graph.SetTitle(";m_{X} [GeV];m_{Y} [GeV];" + zTitle)
            # default ratio range (as in plotRatio.py) unless explicitly specified
            if minZ is None:
                minZ = 0.7
            if maxZ is None:
                maxZ = 1.3

        if minZ is not None:
            graph.SetMinimum(minZ)
        if maxZ is not None:
            graph.SetMaximum(maxZ)

        graph.Draw("cont4z")
        keep.append(graph)

    else:
        c.SetGridx()
        c.SetGridy()
        if logY:
            c.SetLogy()

        if m_X is not None:
            fixed = "m_{{X}} = {0} GeV".format(m_X)
            xTitle = "m_{Y} [GeV]"
        else:
            fixed = "m_{{Y}} = {0} GeV".format(m_Y)
            xTitle = "m_{X} [GeV]"

        if ratio:
            curves = []
            for i, l in enumerate(limits[1:], start=1):
                print("\n==> Computing ratio (input {0} / input 0)\n".format(i))
                curves.append(getRatios(l, limits[0]))
            yTitle = "Ratio of 95% CL expected upper limits" + chLabel
        else:
            curves = limits
            yTitle = "95% CL expected upper limit" + chLabel + " [fb]"

        labels = getLegendLabels(legends, inputs, ratio)

        mg = ROOT.TMultiGraph()
        mg.SetTitle(fixed + ";" + xTitle + ";" + yTitle)

        drawLegend = len(curves) > 1 or bool(legends)
        nEntries = len(curves)
        leg = ROOT.TLegend(0.50, 0.88 - 0.05 * nEntries, 0.83, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.03)

        nGraphs = 0
        for i, values in enumerate(curves):
            if not values:
                print("WARNING: Curve '{0}' has no points. Skipping it.".format(labels[i]))
                continue
            g = make1DGraph(values, m_X)
            g.SetName("graph_{0}".format(i))
            g.SetLineStyle(i % 10 + 1)  # 1 = solid, then different dashing styles
            g.SetLineWidth(2)
            mg.Add(g)
            ROOT.SetOwnership(g, False)  # TMultiGraph owns its graphs
            leg.AddEntry(g, labels[i], "lp")
            nGraphs += 1

        if nGraphs == 0:
            print("Nothing to plot")
            sys.exit(1)

        if minY is not None:
            mg.SetMinimum(minY)
        if maxY is not None:
            mg.SetMaximum(maxY)

        mg.Draw("AL*")
        keep.append(mg)

        if drawLegend:
            leg.Draw()
            keep.append(leg)

    CMS_lumi.cmsTextSize = 0.4
    CMS_lumi.cmsTextOffset = 0.2
    CMS_lumi.lumiTextSize = 0.4
    CMS_lumi.CMS_lumi(c, 1, 11)

    # if requested, save the output file in more than one format
    suffix = Path(output).suffix
    if suffix not in extensions:
        extensions.append(suffix)
    for ext in extensions:
        c.SaveAs(str(Path(output).with_suffix('').with_suffix(ext)))
    c.Close()


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
    ROOT.gStyle.SetTitleX(0.3)   # horizontal position (0 = left, 1 = right)
    ROOT.gStyle.SetTitleY(0.99)  # vertical position (0 = bottom, 1 = top)
    ROOT.gStyle.SetTitleBorderSize(0)
    #ROOT.gStyle.SetTitleAlign(23)

    parser = ArgumentParser(description="To create a 2D plot leave both mX and mY unspecified. To create a 1D plot for a fixed mX or mY value, specify the corresponding value of mX or mY. You can not specify both mX and mY. "
                                        "2D: one input folder gives the limit plot, two input folders give the ratio plot (second/first). "
                                        "1D: N input folders give N overlaid curves, or N-1 overlaid ratios (input_i/first input) with --ratio.")

    # input parameters
    parser.add_argument("-i", "--input", dest="input",
                        help="Space-separated list of input folder paths (e.g. .../2017_combined_SR_pass_toy_multiSignal)",
                        nargs='*',
                        required=True,
                        metavar="INPUT")

    parser.add_argument("-f", "--fit_area", dest="fit_area",
                        help="Fit area subfolder name, typically '1_area' or '1-b_1-sb_area' (default: %(default)s)",
                        default="1_area",
                        metavar="FIT_AREA")

    parser.add_argument("-o", "--output", dest="output",
                        help="Output plot name including the extension (default: %(default)s)",
                        default="expected_limits.png",
                        metavar="OUTPUT")

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year (default: %(default)s)",
                        default="Run2",
                        metavar="YEAR")

    parser.add_argument("--mX", dest="mX",
                        help="Integer value of X mass for which 1D plot is created (default: %(default)s)",
                        default=None,
                        type=int,
                        metavar="X mass")

    parser.add_argument("--mY", dest="mY",
                        help="Integer value of Y mass for which 1D plot is created (default: %(default)s)",
                        default=None,
                        type=int,
                        metavar="Y mass")

    parser.add_argument("--ratio", dest="ratio", action='store_true',
                        help="For 1D plots with N>1 inputs, overlay N-1 ratios (input_i / first input) instead of the N original curves (default: %(default)s)",
                        default=False)

    parser.add_argument("-l", "--legend", dest="legend",
                        help="Space-separated list of legend entries for 1D curves: one per input folder (in ratio mode they are combined into 'entry_i / entry_0'), or one per ratio curve. "
                             "For a 2D ratio plot two entries can be given and are added to the Z-axis title. Defaults to the input folder names.",
                        nargs='*',
                        default=None,
                        metavar="LEGEND")

    parser.add_argument("--logY", dest="logY", action='store_true',
                        help="Sets log scale for Y-axis of 1D plots (default: %(default)s)",
                        default=False)

    parser.add_argument("--minY", dest="minY",
                        help="Y-axis minimum for 1D plot (None means automatic) (default: %(default)s)",
                        default=None,
                        type=float,
                        metavar="Y_MIN")

    parser.add_argument("--maxY", dest="maxY",
                        help="Y-axis maximum for 1D plot (None means automatic) (default: %(default)s)",
                        default=None,
                        type=float,
                        metavar="Y_MAX")

    parser.add_argument("--logZ", dest="logZ", action=BooleanOptionalAction,
                        help="Sets log scale for Z-axis of 2D plots (default: %(default)s). Use --no-logZ to disable it.",
                        default=True)

    parser.add_argument("--minZ", dest="minZ",
                        help="Z-axis minimum for 2D plot (None means automatic, 0.7 for ratio) (default: %(default)s)",
                        default=None,
                        type=float,
                        metavar="Z_MIN")

    parser.add_argument("--maxZ", dest="maxZ",
                        help="Z-axis maximum for 2D plot (None means automatic, 1.3 for ratio) (default: %(default)s)",
                        default=None,
                        type=float,
                        metavar="Z_MAX")

    parser.add_argument("--ext", dest="ext",
                        help="Output file extension(s) i.e. format(s) in which it should be saved (default: %(default)s)",
                        nargs='*',
                        default=[".pdf", ".png"],
                        metavar="EXT")

    options = parser.parse_args()

    inputs  = options.input
    year    = options.year
    mX      = options.mX
    mY      = options.mY
    minY    = options.minY
    maxY    = options.maxY
    minZ    = options.minZ
    maxZ    = options.maxZ
    ratio   = options.ratio
    legends = options.legend
    output  = options.output
    ext     = options.ext

    if len(inputs) == 0:
        print("Warning: At least one input folder has to be specified")
        sys.exit(1)

    if ((minY is not None) and (maxY is not None) and (minY >= maxY)):
        print("Warning: minY >= maxY")
        sys.exit(1)

    if ((minZ is not None) and (maxZ is not None) and (minZ >= maxZ)):
        print("Warning: minZ >= maxZ")
        sys.exit(1)

    if (mX is not None) and (mY is not None):
        print("Warning: You can not specify both mX and mY parameters. To create a 2D plot leave both mX and mY unspecified. To create a 1D plot for a fixed mX or mY value, specify the corresponding value of mX or mY.")
        sys.exit(1)

    plotDimension = "2D" if (mX is None and mY is None) else "1D"

    if plotDimension == "2D":
        if len(inputs) > 2:
            print("Warning: 2D plots accept either one input folder (limits) or two input folders (ratio)")
            sys.exit(1)
        if ratio:
            print("Note: --ratio is ignored for 2D plots. Specifying two input folders produces the ratio plot.")
        ratio = (len(inputs) == 2)
    else:
        if ratio and len(inputs) < 2:
            print("Warning: --ratio requires at least two input folders")
            sys.exit(1)
        if legends is not None:
            allowed = [len(inputs), len(inputs) - 1] if ratio else [len(inputs)]
            if len(legends) not in allowed:
                print("Warning: Number of legend entries ({0}) does not match the number of input folders ({1}){2}".format(
                    len(legends), len(inputs), " or the number of ratio curves ({0})".format(len(inputs) - 1) if ratio else ""))
                sys.exit(1)

    print(' '.join(f'{k}={v}' for k, v in vars(options).items()))

    with open("../H3PO/Analysis/config/xsecs.json") as json_file:
        config = json.load(json_file)

    makePlot(inputs, options.fit_area, year, config, plotDimension, mX, mY, options.logY,
             minY, maxY, options.logZ, minZ, maxZ, ratio, legends, output, ext)
