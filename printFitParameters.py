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
                        help="Regex string for fit parameter name (default: %(default)s)",
                        default="rpf",
                        metavar="REGEX")
    
    (options, args) = parser.parse_known_args()
    
    f = ROOT.TFile.Open(options.input)
    fit = f.Get(options.fit)
    final_pars = ROOT.RooArgList(fit.floatParsFinal())

    par_info = []
    
    for i in range(final_pars.getSize()):
        par = final_pars[i]
        if re.search(options.regex, par.GetName()):
            par_info.append([par.GetName(), par.getValV(), par.getError()])

    # print fit status
    print('\nFit status: {0}\n'.format(fit.status()))
    
    # print parameters and their values
    headers = ['Parameter', 'Value', 'Error']
    print("{: >30} {: >20} {: >20}".format(*headers))
    print("-"*72)
    for row in par_info:
        print("{: >30} {: >20.10f} {: >20.10f}".format(*row))

    f.Close()
