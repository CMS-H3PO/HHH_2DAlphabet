from argparse import ArgumentParser
from base.helpers import get_fit_config
from base.helpers import submit_condor_job
from configs.config import SIGNAL_NAMES
from pathlib import Path
import os


FIT_DEFAULTS_SINGLE = {
    "defMinStrat": 2,
    "rMin": -5,
    "rMax": 5
}

FIT_DEFAULTS_COMBINED = {
    "defMinStrat": 2,
    "rMin": -1,
    "rMax": 2,
    "extra": "--cminDefaultMinimizerTolerance 0.01",
}

FIT_OVERRIDES = {
    ("Run2", "*", "*", "*"): {
        "extra": "--cminDefaultMinimizerTolerance 0.01",
    },

    ("*", "*", "SR_pass_toy", "*"): {
        "rMin": -1,
        "rMax": 1
    },

    ("*", "*", "SR_pass_toy_multiSignal", "*"): {
        "rMin": -1,
        "rMax": 1
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

    ("Run2", "semiboosted", "SR_pass_toy", "3"): {
        "defMinStrat": 1,
        "extra": "--cminDefaultMinimizerTolerance 0.1",
    },

    ("2017", "combined", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":  "-1.00",
            "qcd_b_rpfT_1_par2":  "-0.50",
            "qcd_sb_rpfT_1_par0":  "5.60",
            "qcd_sb_rpfT_1_par1": "-4.20",
            "qcd_sb_rpfT_1_par2":  "0.15"
        },
    },

    ("Run2", "combined", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "7.08",
            "qcd_b_rpfT_1_par1":  "-2.76",
            "qcd_b_rpfT_1_par2":  "-0.06",
            "qcd_sb_rpfT_1_par0":  "5.30",
            "qcd_sb_rpfT_1_par1": "-3.50",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },

    ("Run2", "combined", "VR_pass_toy", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "7.08",
            "qcd_b_rpfT_1_par1":  "-2.76",
            "qcd_b_rpfT_1_par2":  "-0.06",
            "qcd_sb_rpfT_1_par0":  "5.30",
            "qcd_sb_rpfT_1_par1": "-3.50",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },

    ("Run2", "combined", "SR_pass_toy", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "6.7624302571",
            "qcd_b_rpfT_1_par1":  "-2.8011230263",
            "qcd_b_rpfT_1_par2":   "0.0354370388",
            "qcd_sb_rpfT_1_par0":  "4.6950150436",
            "qcd_sb_rpfT_1_par1": "-2.8553262242",
            "qcd_sb_rpfT_1_par2":  "0.7527774280"
        },
    },

    ("Run2", "combined", "SR_pass_toy_multiSignal", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "6.7624302571",
            "qcd_b_rpfT_1_par1":  "-2.8011230263",
            "qcd_b_rpfT_1_par2":   "0.0354370388",
            "qcd_sb_rpfT_1_par0":  "4.6950150436",
            "qcd_sb_rpfT_1_par1": "-2.8553262242",
            "qcd_sb_rpfT_1_par2":  "0.7527774280"
        },
    },
}

BESTORDER_DEFAULT_BOOSTED     = "1"
BESTORDER_DEFAULT_SEMIBOOSTED = "1"
BESTORDER_DEFAULT_COMBINED    = "1:1"

BESTORDER_OVERRIDES = {
    "2017_boosted_VR": "0"
}

SIGNAL_OVERRIDES = {
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
                        help="Analysis channel (e.g. boosted, semiboosted, combined)",
                        required=True,
                        choices=["boosted", "semiboosted", "combined"],
                        metavar="CHANNEL")
    parser.add_argument("-r", "--region", dest="region",
                        help="Analysis region (e.g. VR, VR_pass_toy, SR, SR_pass_toy, SR_pass_toy_multiSignal)",
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
    parser.add_argument("--skipFitPlots", dest="skipFitPlots", action='store_true',
                        help="Skip creating fit plots (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipGoFTest", dest="skipGoFTest", action='store_true',
                        help="Skip GoF test (default: %(default)s)",
                        default=False)
    parser.add_argument("--runLimits", dest="runLimits", action='store_true',
                        help="Run limit calculation (default: %(default)s)",
                        default=False)
    parser.add_argument("--runImpacts", dest="runImpacts", action='store_true',
                        help="Run impacts calculation (default: %(default)s)",
                        default=False)
    parser.add_argument("--skipFTest", dest="skipFTest", action='store_true',
                        help="Skip F-test (default: %(default)s)",
                        default=False)
    parser.add_argument("--dropInSituTTBarSFs", dest="dropInSituTTBarSFs", action='store_true',
                        help="Drop in-situ scale factors for ttbar Xbb mistags (default: %(default)s)",
                        default=False)
    parser.add_argument("-s", "--signals", dest="signals",
                        help="Space-separated list of signal processes (default: %(default)s)",
                        nargs="*",
                        choices=SIGNAL_NAMES,
                        default=SIGNAL_NAMES)
    parser.add_argument("--condor", dest="condor", action="store_true",
                        help="Submit Condor jobs (default: %(default)s)",
                        default=False)
    parser.add_argument("--dry_run", dest="dry_run", action="store_true",
                        help="Dry run without submitting Condor jobs (default: %(default)s)",
                        default=False)
    parser.add_argument("-m", "--memory", dest="memory",
                        help="Requested memory in MB for Condor jobs (default: %(default)s)",
                        default="2000",
                        metavar="MEMORY")

    (options, args) = parser.parse_known_args()

    year    = options.year
    channel = options.channel
    region  = options.region

    if channel == "combined":
        from base.HHH_base_combination import *
        FIT_DEFAULTS       = FIT_DEFAULTS_COMBINED
        BESTORDER_DEFAULT  = BESTORDER_DEFAULT_COMBINED
        options.polyOrders = [BESTORDER_DEFAULT_COMBINED]
        options.skipFTest  = True
    else:
        from base.HHH_base_singleChannel import *
        FIT_DEFAULTS          = FIT_DEFAULTS_SINGLE
        if channel == "boosted":
            BESTORDER_DEFAULT = BESTORDER_DEFAULT_BOOSTED
        else:
            BESTORDER_DEFAULT = BESTORDER_DEFAULT_SEMIBOOSTED

    working_area = f"{year}_{channel}_{region}"
    bestOrder = {working_area:BESTORDER_DEFAULT}
    if working_area in BESTORDER_OVERRIDES:
        bestOrder[working_area] = BESTORDER_OVERRIDES[working_area]

    jsonConfig = f'configs/{working_area}.json'

    if not options.skipCreation and "multi" not in region:
        test_make(working_area,jsonConfig)

    for polyOrder in options.polyOrders:
        if "multi" in region and polyOrder != bestOrder[working_area]:
            continue

        if channel == "combined":
            orders = polyOrder.split(":")
            orderB  = orders[0]
            orderSB = orders[-1]
            _polyOrder = (orderB, orderSB)
        else:
            _polyOrder = (polyOrder,)

        fit_config = get_fit_config(
            year,
            channel,
            region,
            polyOrder,
            FIT_DEFAULTS,
            FIT_OVERRIDES
        )

        if "multi" in region:
            for sig in options.signals:
                sig_working_area = os.path.join(working_area,sig)
                os.makedirs(sig_working_area,exist_ok=True)

                if options.condor:
                    args = f'-y={year} -c {channel} -r {region} -s={sig}'
                    submit_condor_job(sig,working_area,Path(__file__).name,options.memory,args,options.dry_run)
                else:
                    print(f"\nProcessing {sig}...\n")

                    test_make(sig_working_area,jsonConfig)
                    test_fit(
                        sig_working_area,
                        *_polyOrder,
                        sigName=sig,
                        **fit_config,
                        add_tt_mistag_sf=(not options.dropInSituTTBarSFs)
                    )

                    if sig in SIGNAL_OVERRIDES:
                        fit_config.update(SIGNAL_OVERRIDES[sig])

                    test_limit(sig_working_area,*_polyOrder,f'{sig_working_area}/runConfig.json',blind=True,defMinStrat=fit_config["defMinStrat"],extra="--rMin=-1 --rMax={0}".format(fit_config["rMax"]))

                    print(f"\nDone processing {sig}\n")
        else:
            test_fit(
                working_area,
                *_polyOrder,
                **fit_config,
                add_tt_mistag_sf=(not options.dropInSituTTBarSFs)
            )

            if not options.skipFitPlots:
                test_plot(working_area,*_polyOrder)

            if polyOrder==bestOrder[working_area]:
                if not options.skipGoFTest:
                    test_GoF(working_area,*_polyOrder) # this waits for toy fits on Condor to finish
                    test_GoF_plot(working_area,*_polyOrder)
                if options.runLimits:
                    test_limit(working_area,*_polyOrder,f'{working_area}/runConfig.json',blind=True,defMinStrat=fit_config["defMinStrat"],extra="--rMin=-1 --rMax={0}".format(fit_config["rMax"]))
                if options.runImpacts:
                    test_Impacts(working_area,*_polyOrder,rMin=fit_config["rMin"],rMax=fit_config["rMax"],defMinStrat=fit_config["defMinStrat"],extra=fit_config["extra"])

    if channel == "combined":
        if not options.skipFTest and "multi" not in region:
            test_FTest(["0","0"],["0","1"])
            test_FTest(["0","0"],["1","0"])
            test_FTest(["0","1"],["1","1"])
            test_FTest(["1","0"],["1","1"])
            test_FTest(["1","1"],["1","2"])
            test_FTest(["1","1"],["2","1"])
            test_FTest(["2","1"],["2","2"])
            test_FTest(["1","2"],["2","2"])
    else:
        if not options.skipFTest and "multi" not in region:
            test_FTest(working_area,"0","1")
            test_FTest(working_area,"1","2")
            test_FTest(working_area,"2","3")
