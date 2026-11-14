from argparse import ArgumentParser
from base.helpers import get_fit_config
from base.helpers import submit_condor_job
from configs.config import SIGNAL_NAMES
from configs.fit_configs import *
from pathlib import Path
import os


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
                        help="Analysis region (e.g. VR, VR_pass_toy, SR, SR_pass_toy, SR_pass_toy)",
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
    parser.add_argument("-e", "--extra", dest="extra",
                        help="Extra fit options (default: %(default)s)",
                        default="",
                        metavar="EXTRA")
    parser.add_argument("-s", "--signals", dest="signals",
                        help="Space-separated list of signal processes (default: %(default)s)",
                        nargs="*",
                        choices=SIGNAL_NAMES,
                        default=SIGNAL_NAMES)
    parser.add_argument("--multi", dest="multi", action="store_true",
                        help="Run in multi-signal mode (default: %(default)s)",
                        default=False)
    parser.add_argument("--syst", dest="syst", action="store_true",
                        help="Enable systematics i.e. float nuisance parameters in limit computation (default: %(default)s)",
                        default=False)
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
    extra   = (" " + options.extra) if options.extra else ""
    multi   = (options.multi or len(options.signals)>1)

    if channel == "combined":
        from base.HHH_base_combination import *
        FIT_DEFAULTS       = FIT_DEFAULTS_COMBINED
        BESTORDER_DEFAULT  = BESTORDER_DEFAULT_COMBINED
        options.polyOrders = [BESTORDER_DEFAULT_COMBINED]
        options.skipFTest  = True
        jsonConfig = 'configs/combined.json'
    else:
        from base.HHH_base_singleChannel import *
        FIT_DEFAULTS          = FIT_DEFAULTS_SINGLE
        if channel == "boosted":
            BESTORDER_DEFAULT = BESTORDER_DEFAULT_BOOSTED
        else:
            BESTORDER_DEFAULT = BESTORDER_DEFAULT_SEMIBOOSTED
        jsonConfig = 'configs/single.json'

    yearDict = {
        "2017": 17,
        "Run2": 2
    }

    findReplace = {
        "HIST":      "mjj_vs_mjjj_{0}R_$region{1}_nominal".format(region[0], f"_{channel}" if channel!="combined" else ""),
        "HIST_UP":   "mjj_vs_mjjj_{0}R_$region{1}_$systUp".format(region[0], f"_{channel}" if channel!="combined" else ""),
        "HIST_DOWN": "mjj_vs_mjjj_{0}R_$region{1}_$systDown".format(region[0], f"_{channel}" if channel!="combined" else ""),
        "CHANNEL":   f"{channel}",
        "DATAFILE":  "JetHT_Histograms{0}.root".format(f"_{region}" if "pass_toy" in region else ""),
        "SIGNAME":   options.signals,
        "YEAR":      yearDict[year]
    }

    suffix = ("_multiSignal" if multi else "") + ("_syst" if options.syst else "")
    working_area = f"{year}_{channel}_{region}{suffix}"
    bestOrder = {working_area:BESTORDER_DEFAULT}
    if working_area in BESTORDER_OVERRIDES:
        bestOrder[working_area] = BESTORDER_OVERRIDES[working_area]

    if not options.skipCreation and not multi:
        test_make(working_area,jsonConfig,findreplace=findReplace)

    for polyOrder in options.polyOrders:
        if multi and polyOrder != bestOrder[working_area]:
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

        if extra:
            fit_config["extra"] = (fit_config["extra"] + extra)

        if multi:
            for sig in options.signals:
                sig_working_area = os.path.join(working_area,sig)
                os.makedirs(sig_working_area,exist_ok=True)

                if options.condor:
                    args = f'-y={year} -c {channel} -r {region} -s={sig}'
                    submit_condor_job(sig,working_area,Path(__file__).name,options.memory,args,options.dry_run)
                else:
                    print(f"\nProcessing {sig}...\n")

                    if not options.skipCreation:
                        findReplace["SIGNAME"] = [sig]
                        test_make(sig_working_area,jsonConfig,findreplace=findReplace)
                    test_fit(
                        sig_working_area,
                        *_polyOrder,
                        sigName=sig,
                        **fit_config,
                        add_tt_mistag_sf=(not options.dropInSituTTBarSFs)
                    )

                    if sig in SIGNAL_OVERRIDES:
                        fit_config.update(SIGNAL_OVERRIDES[sig])

                    extra = fit_config["extra"] + " --rMin=-1 --rMax={0}".format(fit_config["rMax"])
                    if options.syst and "--freezeParameters allConstrainedNuisances" in extra:
                        extra.replace("--freezeParameters allConstrainedNuisances", "")

                    test_limit(sig_working_area,*_polyOrder,f'{sig_working_area}/runConfig.json',blind=True,defMinStrat=fit_config["defMinStrat"],extra=extra)

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
                    extra = fit_config["extra"] + " --rMin=-1 --rMax={0}".format(fit_config["rMax"])
                    if options.syst and "--freezeParameters allConstrainedNuisances" in extra:
                        extra.replace("--freezeParameters allConstrainedNuisances", "")
                    test_limit(working_area,*_polyOrder,f'{working_area}/runConfig.json',blind=True,defMinStrat=fit_config["defMinStrat"],extra=extra)
                if options.runImpacts:
                    test_Impacts(working_area,*_polyOrder,rMin=fit_config["rMin"],rMax=fit_config["rMax"],defMinStrat=fit_config["defMinStrat"],extra=fit_config["extra"])

    if channel == "combined":
        if not options.skipFTest and not multi:
            test_FTest(["0","0"],["0","1"])
            test_FTest(["0","0"],["1","0"])
            test_FTest(["0","1"],["1","1"])
            test_FTest(["1","0"],["1","1"])
            test_FTest(["1","1"],["1","2"])
            test_FTest(["1","1"],["2","1"])
            test_FTest(["2","1"],["2","2"])
            test_FTest(["1","2"],["2","2"])
    else:
        if not options.skipFTest and not multi:
            test_FTest(working_area,"0","1")
            test_FTest(working_area,"1","2")
            test_FTest(working_area,"2","3")
