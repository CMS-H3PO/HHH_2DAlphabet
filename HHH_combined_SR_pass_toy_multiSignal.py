from HHH_base_combination import *
from argparse import ArgumentParser
import os

if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y 2017"

    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year(s) (e.g. 2017, Run2)",
                        required=True,
                        metavar="YEAR")

    (options, args) = parser.parse_known_args()

    # best-fit values from individual fits
    params_b = {'qcd_b_rpfT_1_par0':  '6.9722293911',
                'qcd_b_rpfT_1_par1': '-2.6216322625',
                'qcd_b_rpfT_1_par2':  '1.1057040331'}

    params_sb = {'qcd_sb_rpfT_1_par0':  '6.3419944445',
                 'qcd_sb_rpfT_1_par1': '-7.9777135785',
                 'qcd_sb_rpfT_1_par2':  '2.0819610327'}

    setParams = {}
    setParams.update(params_b)
    setParams.update(params_sb)

    sigNames = [
        "XToYHTo6B_MX-1000_MY-300", "XToYHTo6B_MX-1000_MY-600", "XToYHTo6B_MX-1000_MY-800",
        "XToYHTo6B_MX-1200_MY-300", "XToYHTo6B_MX-1200_MY-600", "XToYHTo6B_MX-1200_MY-800", "XToYHTo6B_MX-1200_MY-1000",
        "XToYHTo6B_MX-1600_MY-300", "XToYHTo6B_MX-1600_MY-600", "XToYHTo6B_MX-1600_MY-800", "XToYHTo6B_MX-1600_MY-1000", "XToYHTo6B_MX-1600_MY-1200", "XToYHTo6B_MX-1600_MY-1400",
        "XToYHTo6B_MX-2000_MY-300", "XToYHTo6B_MX-2000_MY-600", "XToYHTo6B_MX-2000_MY-800", "XToYHTo6B_MX-2000_MY-1000", "XToYHTo6B_MX-2000_MY-1200", "XToYHTo6B_MX-2000_MY-1600", "XToYHTo6B_MX-2000_MY-1800",
        "XToYHTo6B_MX-2500_MY-300", "XToYHTo6B_MX-2500_MY-600", "XToYHTo6B_MX-2500_MY-800", "XToYHTo6B_MX-2500_MY-1000", "XToYHTo6B_MX-2500_MY-1200", "XToYHTo6B_MX-2500_MY-1600", "XToYHTo6B_MX-2500_MY-2000", "XToYHTo6B_MX-2500_MY-2200", "XToYHTo6B_MX-2500_MY-2300",
        "XToYHTo6B_MX-3000_MY-300", "XToYHTo6B_MX-3000_MY-600", "XToYHTo6B_MX-3000_MY-800", "XToYHTo6B_MX-3000_MY-1000", "XToYHTo6B_MX-3000_MY-1200", "XToYHTo6B_MX-3000_MY-1600", "XToYHTo6B_MX-3000_MY-2000", "XToYHTo6B_MX-3000_MY-2500", "XToYHTo6B_MX-3000_MY-2800",
        "XToYHTo6B_MX-3500_MY-300", "XToYHTo6B_MX-3500_MY-600", "XToYHTo6B_MX-3500_MY-800", "XToYHTo6B_MX-3500_MY-1000", "XToYHTo6B_MX-3500_MY-1200", "XToYHTo6B_MX-3500_MY-1600", "XToYHTo6B_MX-3500_MY-2000", "XToYHTo6B_MX-3500_MY-2500", "XToYHTo6B_MX-3500_MY-2800", "XToYHTo6B_MX-3500_MY-3000", "XToYHTo6B_MX-3500_MY-3300",
        "XToYHTo6B_MX-4000_MY-300", "XToYHTo6B_MX-4000_MY-600", "XToYHTo6B_MX-4000_MY-800", "XToYHTo6B_MX-4000_MY-1000", "XToYHTo6B_MX-4000_MY-1200", "XToYHTo6B_MX-4000_MY-1600", "XToYHTo6B_MX-4000_MY-2000", "XToYHTo6B_MX-4000_MY-2500", "XToYHTo6B_MX-4000_MY-2800", "XToYHTo6B_MX-4000_MY-3000", "XToYHTo6B_MX-4000_MY-3500", "XToYHTo6B_MX-4000_MY-3800"
    ]
    rMax = 5
    strategy = 2

    # datasets that require special processing
    #sigNames = ["XToYHTo6B_MX-1000_MY-300", "XToYHTo6B_MX-1200_MY-300", "XToYHTo6B_MX-2000_MY-1200", "XToYHTo6B_MX-3000_MY-300"]
    #rMax = 3
    #strategy = 2

    #sigNames = ["XToYHTo6B_MX-3000_MY-2800"]
    #rMax = 1
    #strategy = 2

    bestOrders = {"{}_combined_SR_pass_toy_multiSignal".format(options.year):["1","2"]}
    for working_area in ["{}_combined_SR_pass_toy_multiSignal".format(options.year)]:

        jsonConfig   = 'configs/{0}.json'.format(working_area)
        
        test_make(working_area,jsonConfig) # this line can be commented out when reprocessing a subset of signal samples if signal cross sections have not been modified
        polyOrders = bestOrders[working_area]

        for sig in sigNames:
            print("\nProcessing {0}...\n".format(sig))

            test_fit(working_area,polyOrders[0],polyOrders[1],sigName=sig,strategy=strategy,setParams=setParams)
            
            test_limit(working_area,polyOrders[0],polyOrders[1],'%s/runConfig.json'%working_area,blind=True,strategy=strategy,extra=("--rMin=-1 --rMax={0}".format(rMax)))

            fit_area = "{0}/{1}-b_{2}-sb_area".format(working_area,polyOrders[0],polyOrders[1])
            sig_area = "{0}_{1}".format(fit_area,sig)
            if os.path.exists(sig_area):
                print("\nSignal area {0} already exists. Removing".format(sig_area))
                os.system("rm -rf {0}".format(sig_area))
            cmd = "mv {0} {1}".format(fit_area,sig_area)
            print("\n" + cmd)
            os.system(cmd)

            print("\nDone processing {0}\n".format(sig))

