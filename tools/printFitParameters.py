from argparse import ArgumentParser
import re
import ROOT


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -i fitDiagnosticsTest.root"

    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-i", "--input", dest="input",
                      help="Input fit diagnostics file",
                      metavar="INPUT",
                      required=True)

    parser.add_argument("-f", "--fit", dest="fit",
                      help="Fit type (default: %(default)s)",
                      default="fit_b",
                      metavar="FIT")

    parser.add_argument("-r", "--regex", dest="regex",
                        help="Regex string for fit parameter name. Use '.*' to get all parameters (default: %(default)s)",
                        default="rpf",
                        metavar="REGEX")

    parser.add_argument("-o", "--output", dest="output",
                        help="Output text file (default: %(default)s)",
                        default=None,
                        metavar="OUTPUT")

    (options, args) = parser.parse_known_args()

    fIn = ROOT.TFile.Open(options.input)
    fit = fIn.Get(options.fit)
    final_pars = ROOT.RooArgList(fit.floatParsFinal())

    par_info = []
    values = {}

    for i in range(final_pars.getSize()):
        par = final_pars[i]
        name  = par.GetName()
        value = par.getVal()
        error = par.getError()
        if re.search(options.regex, name):
            par_info.append([name, value, error])
            values[name] = value

    # print fit status
    print('\nFit status: {0}\n'.format(fit.status()))

    # print parameters and their values
    headers = ['Parameter', 'Value', 'Error']
    print("{: >30} {: >20} {: >20}".format(*headers))
    print("-"*72)
    for row in par_info:
        print("{: >30} {: >20.10f} {: >20.10f}".format(*row))

    if options.output is not None:
        with open(options.output, "w") as fOut:
            fOut.write(",".join(
                f"{name}={value:.12g}"
                for name, value in sorted(values.items())
            ))

        print(f"Wrote {len(values)} parameters to {options.output}")

    fIn.Close()
