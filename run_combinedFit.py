from base.HHH_base_combination import *
from argparse import ArgumentParser
from base.helpers import get_fit_config


FIT_DEFAULTS = {
    "defMinStrat": 2,
    "rMin": -1,
    "rMax": 2,
    "extra": "--cminDefaultMinimizerTolerance 0.01",
}

FIT_OVERRIDES = {
    ("2017", "*", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":  "-1.00",
            "qcd_b_rpfT_1_par2":  "-0.50",
            "qcd_sb_rpfT_1_par0":  "5.60",
            "qcd_sb_rpfT_1_par1": "-4.20",
            "qcd_sb_rpfT_1_par2":  "0.15"
        },
    },

    ("Run2", "*", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "7.08",
            "qcd_b_rpfT_1_par1":  "-2.76",
            "qcd_b_rpfT_1_par2":  "-0.06",
            "qcd_sb_rpfT_1_par0":  "5.30",
            "qcd_sb_rpfT_1_par1": "-3.50",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },

    ("Run2", "*", "VR_pass_toy", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "7.08",
            "qcd_b_rpfT_1_par1":  "-2.76",
            "qcd_b_rpfT_1_par2":  "-0.06",
            "qcd_sb_rpfT_1_par0":  "5.30",
            "qcd_sb_rpfT_1_par1": "-3.50",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },
}


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
                        help="Analysis region (e.g. VR, VR_pass_toy, SR, SR_pass_toy)",
                        required=True,
                        metavar="REGION")
    parser.add_argument("-p", "--polyOrders", dest="polyOrders",
                        help="Space-separated list of polynomial orders (default: %(default)s).",
                        nargs='*',
                        default=["1:1"],
                        metavar="POLYORDERS")
    parser.add_argument("--skipCreation", dest="skipCreation", action='store_true',
                        help="Skip workspace creation (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipGoFTest", dest="skipGoFTest", action='store_true',
                        help="Skip GoF test (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipFTest", dest="skipFTest",
                        help="Skip F-test (default: %(default)s)",
                        default=True)

    (options, args) = parser.parse_known_args()

    year    = options.year
    region  = options.region

    working_area = f"{year}_combined_{region}"
    bestOrders = {working_area:"1:1"}

    jsonConfig = f'configs/{working_area}.json'

    if not options.skipCreation:
        test_make(working_area,jsonConfig)

    for polyOrders in options.polyOrders:
        orders = polyOrders.split(":")
        orderB  = orders[0]
        orderSB = orders[-1]
        fit_config = get_fit_config(
            year,
            "*",
            region,
            polyOrders,
            FIT_DEFAULTS,
            FIT_OVERRIDES
        )
        test_fit(
            working_area,
            orderB,orderSB,
            **fit_config,
        )
        test_plot(working_area,orderB,orderSB)
        if polyOrders==bestOrders[working_area] and not options.skipGoFTest:
            test_GoF(working_area,orderB,orderSB) # this waits for toy fits on Condor to finish
            test_GoF_plot(working_area,orderB,orderSB)

    if not options.skipFTest:
        test_FTest(["0","0"],["0","1"])
        test_FTest(["0","0"],["1","0"])
        test_FTest(["0","1"],["1","1"])
        test_FTest(["1","0"],["1","1"])
        test_FTest(["1","1"],["1","2"])
        test_FTest(["1","1"],["2","1"])
        test_FTest(["2","1"],["2","2"])
        test_FTest(["1","2"],["2","2"])
