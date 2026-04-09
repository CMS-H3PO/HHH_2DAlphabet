from base.HHH_base_combination import *
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

    parser.add_argument("-s", "--sig", dest="sig",
                        help="Space-separated list of signal processes",
                        nargs="*",
                        default = None)

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

    # best-fit parameter values from individual fits
    setParams = {}
    if options.year == "2017":
        params_b = {'qcd_b_rpfT_1_par0':  '6.8275952807',
                    'qcd_b_rpfT_1_par1': '-1.9605923829',
                    'qcd_b_rpfT_1_par2': '-0.3810498683'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '5.5900153003',
                     'qcd_sb_rpfT_1_par1': '-3.9702916792',
                     'qcd_sb_rpfT_1_par2':  '0.8722600283'}

        setParams.update(params_b)
        setParams.update(params_sb)
    else:
        params_b = {'qcd_b_rpfT_1_par0':  '7.0160921619',
                    'qcd_b_rpfT_1_par1': '-3.1612126934',
                    'qcd_b_rpfT_1_par2':  '0.7536479427'}

        params_sb = {'qcd_sb_rpfT_1_par0':  '5.6019949458',
                     'qcd_sb_rpfT_1_par1': '-2.8926022265',
                     'qcd_sb_rpfT_1_par2': '-0.7081990841'}

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
    rMax_def = 5
    defMinStratFit_def = 2
    defMinStrat_def = 2

    # signal datasets that require special processing
    # dataset: (rMax, defMinStratFit, defMinStrat)
    spec_sigNames = {
        "XToYHTo6B_MX-3000_MY-600":  (1, 2, 2),
        "XToYHTo6B_MX-3000_MY-2000": (1, 2, 2),
        "XToYHTo6B_MX-3500_MY-1000": (1, 2, 2),
        "XToYHTo6B_MX-3500_MY-1200": (1, 2, 2),
        "XToYHTo6B_MX-4000_MY-800":  (1, 2, 2)
        }

    if options.sig is not None:
        sigNames = options.sig

    bestOrders = {"{}_combined_SR_pass_toy_multiSignal".format(options.year):["1","1"]}
    for working_area in ["{}_combined_SR_pass_toy_multiSignal".format(options.year)]:

        jsonConfig   = 'configs/{0}.json'.format(working_area)

        polyOrders = bestOrders[working_area]

        for sig in sigNames:
            (rMax, defMinStratFit, defMinStrat) = (rMax_def, defMinStratFit_def, defMinStrat_def)

            if sig in spec_sigNames:
                (rMax, defMinStratFit, defMinStrat) = spec_sigNames[sig]

            sig_working_area = os.path.join(working_area,sig)
            os.makedirs(sig_working_area,exist_ok=True)

            if options.condor:
                condor_dir = os.path.join(sig_working_area, "condor")
                os.makedirs(condor_dir,exist_ok=True)

                args = '-y={0} -s={1}'.format(options.year, sig)

                exec_file = os.path.join(condor_dir, 'run.sh')

                with open(exec_file, 'w') as e_file:
                    e_file.write('#!/bin/bash\n')
                    e_file.write('\n')
                    e_file.write('echo HHH_combined_SR_pass_toy_multiSignal.py $*\n')
                    e_file.write('python -u HHH_combined_SR_pass_toy_multiSignal.py $*\n')

                os.system('chmod +x ' + exec_file)

                job_desc = os.path.join(condor_dir, 'job_desc.txt')

                with open(job_desc, 'w') as j_file:
                    j_file.write('executable  = {0}\n'.format(exec_file))
                    j_file.write('universe    = vanilla\n')
                    j_file.write('getenv = True\n')
                    j_file.write('RequestMemory = {0}\n'.format(options.memory))
                    j_file.write('log    = ' + os.path.join(condor_dir, 'tmp.log') + '\n')
                    j_file.write('output = ' + os.path.join(condor_dir, 'tmp.out') + '\n')
                    j_file.write('error  = ' + os.path.join(condor_dir, 'tmp.err') + '\n')
                    j_file.write('arguments = "' + args + '"\n')
                    j_file.write('queue\n')
                if not options.dry_run:
                    os.system('condor_submit ' + job_desc)
            else:
                print("\nProcessing {0}...\n".format(sig))

                test_make(sig_working_area,jsonConfig)

                test_fit(sig_working_area,polyOrders[0],polyOrders[1],sigName=sig,defMinStrat=defMinStratFit,rMin=-1,rMax=1,setParams=setParams)

                test_limit(sig_working_area,polyOrders[0],polyOrders[1],'%s/runConfig.json'%sig_working_area,blind=True,defMinStrat=defMinStrat,extra=("--rMin=-1 --rMax={0}".format(rMax)))

                print("\nDone processing {0}\n".format(sig))
