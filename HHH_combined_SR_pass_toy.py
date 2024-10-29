from HHH_base_combination import *
from argparse import ArgumentParser


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
        params_b = {'qcd_b_rpfT_1_par0':  '6.9722293911',
                    'qcd_b_rpfT_1_par1': '-2.6216322625',
                    'qcd_b_rpfT_1_par2':  '1.1057040331'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '6.3419944445',
                     'qcd_sb_rpfT_1_par1': '-7.9777135785',
                     'qcd_sb_rpfT_1_par2':  '2.0819610327'}

        setParams.update(params_b)
        setParams.update(params_sb)
    else:
        params_b = {'qcd_b_rpfT_1_par0':  '6.5297055558',
                    'qcd_b_rpfT_1_par1': '-2.5859269353',
                    'qcd_b_rpfT_1_par2':  '0.7874599276'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '5.9207814471',
                     'qcd_sb_rpfT_1_par1': '-4.5875310779',
                     'qcd_sb_rpfT_1_par2': '-0.2105124716'}

        setParams.update(params_b)
        setParams.update(params_sb)

    bestOrders = {"{}_combined_SR_pass_toy".format(options.year):["1","1"]}
    for working_area in ["{}_combined_SR_pass_toy".format(options.year)]:

        jsonConfig   = 'configs/{0}.json'.format(working_area)
        
        test_make(working_area,jsonConfig)

        for orderB in ["1"]:
            for orderSB in ["1"]:
                if options.year == "2017":
                    if [orderB,orderSB] in [["1","1"]]:
                        test_fit(working_area,orderB,orderSB,strategy=2,rMin=-1,rMax=1,setParams=setParams)
                    else:
                        test_fit(working_area,orderB,orderSB,strategy=1,rMin=-1,rMax=5)
                else:
                    if [orderB,orderSB] in [["1","1"]]:
                        test_fit(working_area,orderB,orderSB,strategy=2,rMin=-1,rMax=1,setParams=setParams)
                    else:
                        test_fit(working_area,orderB,orderSB,strategy=1,rMin=-1,rMax=5)
                test_plot(working_area,orderB,orderSB)
                if [orderB,orderSB]==bestOrders[working_area]:
                    test_GoF(working_area,orderB,orderSB) # this waits for toy fits on Condor to finish
                    test_GoF_plot(working_area,orderB,orderSB)
                    test_limit(working_area,orderB,orderSB,'%s/runConfig.json'%working_area,blind=True,strategy=2,extra="--rMin=-1 --rMax=3")

        #test_FTest(["0","0"],["0","1"])
        #test_FTest(["0","0"],["1","0"])
        #test_FTest(["0","1"],["1","1"])
        #test_FTest(["1","0"],["1","1"])
        #test_FTest(["1","1"],["1","2"])
        #test_FTest(["1","1"],["2","1"])
        #test_FTest(["2","1"],["2","2"])
        #test_FTest(["1","2"],["2","2"])
  
        # limit calculation put at the end in case it crashes when run right after GoF
        #test_limit(working_area,bestOrders[working_area][0],bestOrders[working_area][1],'%s/runConfig.json'%working_area,blind=True,strategy=2,extra="--rMin=-1 --rMax=3")
