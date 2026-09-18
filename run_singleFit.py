from base.HHH_base_singleChannel import *
from argparse import ArgumentParser
from base.helpers import get_fit_config


FIT_DEFAULTS = {
    "defMinStrat": 2,
    "rMin": -5,
    "rMax": 5
}

FIT_OVERRIDES = {
    ("Run2", "*", "*", "*"): {
        "extra": "--cminDefaultMinimizerTolerance 0.01",
    },

    ("2017", "boosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "5.80",
            "qcd_rpfT_1_par1": "-1.00",
            "qcd_rpfT_1_par2": "-0.50",
        },
    },

    ("2017", "semiboosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "5.60",
            "qcd_rpfT_1_par1": "-4.10",
            "qcd_rpfT_1_par2":  "0.10",
        },
    },

    ("2017", "semiboosted", "VR", "3"): {
        "defMinStrat": 1,
    },

    ("Run2", "boosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "6.20",
            "qcd_rpfT_1_par1": "-2.00",
            "qcd_rpfT_1_par2": "-0.10",
        },
    },

    ("Run2", "boosted", "VR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "6.20",
            "qcd_rpfT_1_par1": "-2.00",
            "qcd_rpfT_1_par2": "-0.10",
        },
    },

    ("Run2", "semiboosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "4.70",
            "qcd_rpfT_1_par1": "-2.90",
            "qcd_rpfT_1_par2":  "0.17",
        },
    },

    ("Run2", "semiboosted", "VR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "4.70",
            "qcd_rpfT_1_par1": "-2.90",
            "qcd_rpfT_1_par2":  "0.17",
        },
    },
}

BESTORDER_OVERRIDES = {
    "2017_boosted_VR": "0"
}


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y Run2 -c boosted -r VR"

    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year(s) (e.g. 2017, Run2)",
                        required=True,
                        metavar="YEAR")
    parser.add_argument("-c", "--channel", dest="channel",
                        help="Analysis channel (e.g. boosted, semiboosted)",
                        required=True,
                        metavar="CHANNEL")
    parser.add_argument("-r", "--region", dest="region",
                        help="Analysis region (e.g. VR, VR_pass_toy, SR, SR_pass_toy)",
                        required=True,
                        metavar="REGION")
    parser.add_argument("-p", "--polyOrders", dest="polyOrders",
                        help="Space-separated list of polynomial orders (default: %(default)s).",
                        nargs='*',
                        default=["0","1","2","3"],
                        metavar="POLYORDERS")
    parser.add_argument("--skipCreation", dest="skipCreation", action='store_true',
                        help="Skip workspace creation (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipGoFTest", dest="skipGoFTest", action='store_true',
                        help="Skip GoF test (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipFTest", dest="skipFTest", action='store_true',
                        help="Skip F-test (default: %(default)s)",
                        default=False)

    (options, args) = parser.parse_known_args()

    year    = options.year
    channel = options.channel
    region  = options.region

    working_area = f"{year}_{channel}_{region}"
    bestOrder = {working_area:"1"}
    if working_area in BESTORDER_OVERRIDES:
        bestOrder[working_area] = BESTORDER_OVERRIDES[working_area]

    jsonConfig   = f'configs/{working_area}.json'

    if not options.skipCreation:
        test_make(working_area,jsonConfig)

    for polyOrder in options.polyOrders:
        fit_config = get_fit_config(
            year,
            channel,
            region,
            polyOrder,
            FIT_DEFAULTS,
            FIT_OVERRIDES
        )
        test_fit(
            working_area,
            polyOrder,
            **fit_config,
        )
        test_plot(working_area,polyOrder)
        if polyOrder==bestOrder[working_area] and not options.skipGoFTest:
            test_GoF(working_area,polyOrder) # this waits for toy fits on Condor to finish
            test_GoF_plot(working_area,polyOrder)

    if not options.skipFTest:
        test_FTest(working_area,"0","1")
        test_FTest(working_area,"1","2")
        test_FTest(working_area,"2","3")
