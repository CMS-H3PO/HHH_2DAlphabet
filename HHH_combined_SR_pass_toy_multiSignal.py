from utils.HHH_base_combination import *
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

    # best-fit parameter values from individual fits
    setParams = {}
    if options.year == "2017":
        params_b = {'qcd_b_rpfT_1_par0':  '7.4472843501',
                    'qcd_b_rpfT_1_par1': '-1.2225904300',
                    'qcd_b_rpfT_1_par2': '-3.1183407096'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '5.4947964137',
                     'qcd_sb_rpfT_1_par1': '-3.5582852528',
                     'qcd_sb_rpfT_1_par2': '-0.0780756126'}

        setParams.update(params_b)
        setParams.update(params_sb)
    else:
        params_b = {'qcd_b_rpfT_1_par0':  '7.1078935818',
                    'qcd_b_rpfT_1_par1': '-3.3944459268',
                    'qcd_b_rpfT_1_par2':  '0.0605185254'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '5.2953377262',
                     'qcd_sb_rpfT_1_par1': '-3.6739808143',
                     'qcd_sb_rpfT_1_par2':  '0.9656145041'}

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
    defMinStratFit = 2
    defMinStrat = 2

    # datasets that require special processing
    #sigNames = ["XToYHTo6B_MX-3000_MY-2000", "XToYHTo6B_MX-3500_MY-1000", "XToYHTo6B_MX-3500_MY-1200", "XToYHTo6B_MX-4000_MY-800"]
    #rMax = 1
    #defMinStratFit = 2
    #defMinStrat = 2


    bestOrders = {"{}_combined_SR_pass_toy_multiSignal".format(options.year):["1","1"]}
    for working_area in ["{}_combined_SR_pass_toy_multiSignal".format(options.year)]:

        jsonConfig   = 'configs/{0}.json'.format(working_area)
        
        test_make(working_area,jsonConfig) # this line can be commented out when reprocessing a subset of signal samples if signal cross sections have not been modified
        polyOrders = bestOrders[working_area]

        for sig in sigNames:
            print("\nProcessing {0}...\n".format(sig))

            test_fit(working_area,polyOrders[0],polyOrders[1],sigName=sig,defMinStrat=defMinStratFit,rMin=-1,rMax=1,setParams=setParams)
            
            test_limit(working_area,polyOrders[0],polyOrders[1],'%s/runConfig.json'%working_area,blind=True,defMinStrat=defMinStrat,extra=("--rMin=-1 --rMax={0}".format(rMax)))

            fit_area = "{0}/{1}-b_{2}-sb_area".format(working_area,polyOrders[0],polyOrders[1])
            sig_area = "{0}_{1}".format(fit_area,sig)
            if os.path.exists(sig_area):
                print("\nSignal area {0} already exists. Removing".format(sig_area))
                os.system("rm -rf {0}".format(sig_area))
            cmd = "mv {0} {1}".format(fit_area,sig_area)
            print("\n" + cmd)
            os.system(cmd)

            print("\nDone processing {0}\n".format(sig))

