from HHH_base_singleChannel import *
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

    bestOrder = {"{}_semiboosted_SR_pass_toy".format(options.year):"1"}
    for working_area in ["{}_semiboosted_SR_pass_toy".format(options.year)]:

        jsonConfig   = 'configs/{0}.json'.format(working_area)

        #test_make(working_area,jsonConfig)

        for polyOrder in ["2","3"]:
            if options.year == "2017":
                if polyOrder in ["1"]:
                    test_fit(working_area,polyOrder,strategy=2, rMin=-1, rMax=1)
                elif polyOrder in ["2"]:
                    test_fit(working_area,polyOrder,strategy=1, rMin=-5, rMax=5, setParams={'qcd_rpfT_2_par0':'7.0','qcd_rpfT_2_par1':'-10.0','qcd_rpfT_2_par2':'-0.4','qcd_rpfT_2_par3':'3.0','qcd_rpfT_2_par4':'5.0','qcd_rpfT_2_par5':'0.6'})
                elif polyOrder in ["3"]:
                    continue
                else:
                    test_fit(working_area,polyOrder,strategy=1, rMin=-5, rMax=5)
            else:
                if polyOrder in ["2","3"]:
                    test_fit(working_area,polyOrder,strategy=2, rMin=-1, rMax=1)
                else:
                    test_fit(working_area,polyOrder,strategy=1, rMin=-5, rMax=5)
            test_plot(working_area,polyOrder)
            if polyOrder==bestOrder[working_area]:
                test_GoF(working_area,polyOrder) # this waits for toy fits on Condor to finish
                test_GoF_plot(working_area,polyOrder)
                test_limit(working_area,polyOrder,'%s/runConfig.json'%working_area,blind=True,strategy=2,extra="--rMin=-1 --rMax=5")

        #test_FTest(working_area,"0","1")
        test_FTest(working_area,"1","2")
        if options.year!="2017":
            test_FTest(working_area,"2","3")
