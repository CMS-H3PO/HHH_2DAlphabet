import os
from argparse import ArgumentParser


def generate(year, ttbar_path, data_path, seed, region):
    from plotRpf_VR import x_min, x_max, y_min, y_max, rpf_boosted_VR, rpf_semiboosted_VR
    import ROOT

    print('Processing {0} region for {1}...\n'.format(region, year))

    print('INFO: Random number generator seed: {0}'.format(seed))

    # random number generator
    rnd = ROOT.TRandom3(seed)

    data_toy_file = os.path.splitext(os.path.basename(data_path))[0] + "_{0}_pass_toy.root".format(region)
    
    cmd = "cp {0} {1}".format(data_path, data_toy_file)
    print(cmd + '\n')
    os.system(cmd)
    
    # histogram files
    ttbar_file = ROOT.TFile.Open(ttbar_path, 'READ')
    data_file = ROOT.TFile.Open(data_toy_file, 'UPDATE')

    # histograms: boosted
    mjj_vs_mjjj_fail_b_ttbar = ttbar_file.Get('mjj_vs_mjjj_{0}_fail_boosted_nominal'.format(region))
    mjj_vs_mjjj_pass_b_ttbar = ttbar_file.Get('mjj_vs_mjjj_{0}_pass_boosted_nominal'.format(region))

    mjj_vs_mjjj_fail_b_data = data_file.Get('mjj_vs_mjjj_{0}_fail_boosted_nominal'.format(region))
    mjj_vs_mjjj_pass_b_data = data_file.Get('mjj_vs_mjjj_{0}_pass_boosted_nominal'.format(region))

    # histograms: semiboosted
    mjj_vs_mjjj_fail_sb_ttbar = ttbar_file.Get('mjj_vs_mjjj_{0}_fail_semiboosted_nominal'.format(region))
    mjj_vs_mjjj_pass_sb_ttbar = ttbar_file.Get('mjj_vs_mjjj_{0}_pass_semiboosted_nominal'.format(region))

    mjj_vs_mjjj_fail_sb_data = data_file.Get('mjj_vs_mjjj_{0}_fail_semiboosted_nominal'.format(region))
    mjj_vs_mjjj_pass_sb_data = data_file.Get('mjj_vs_mjjj_{0}_pass_semiboosted_nominal'.format(region))


    for i in range(1,mjj_vs_mjjj_pass_b_data.GetNbinsX() + 1):
        for j in range(1,mjj_vs_mjjj_pass_b_data.GetNbinsY() + 1):
            
            x_center = mjj_vs_mjjj_pass_b_data.GetXaxis().GetBinCenter(i)
            y_center = mjj_vs_mjjj_pass_b_data.GetYaxis().GetBinCenter(j)
            
            if x_center < x_min or x_center > x_max: continue
            if y_center < y_min or y_center > y_max: continue
            
            # boosted
            data_fail_b = mjj_vs_mjjj_fail_b_data.GetBinContent(i,j)
            ttbar_fail_b = mjj_vs_mjjj_fail_b_ttbar.GetBinContent(i,j)
            ttbar_pass_b = mjj_vs_mjjj_pass_b_ttbar.GetBinContent(i,j)
            
            qcd_fail_b = (data_fail_b - ttbar_fail_b)
            
            if qcd_fail_b < 0.:
                print('WARNING: qcd_fail_b negative for (mjjj, mjj)=({0}, {1}). Manually set to 0 (data_fail_b={2}, ttbar_fail_b={3})'.format(x_center, y_center, data_fail_b, ttbar_fail_b))
                qcd_fail_b = 0.

            qcd_pass_b_exp = qcd_fail_b * rpf_boosted_VR[year].Eval(x_center, y_center)
            
            # in case the transfer function becomes negative (it shouldn't in the phase space of interest)
            if qcd_pass_b_exp < 0.:
                print('WARNING: Boosted transfer function negative for (mjjj, mjj)=({0}, {1})'.format(x_center, y_center))
                qcd_pass_b_exp = 0.
            
            data_pass_b_exp = (qcd_pass_b_exp + ttbar_pass_b)
            
            data_pass_b = (rnd.PoissonD(data_pass_b_exp) if data_pass_b_exp>0. else 0.)
            
            #print('i={0}, j={1}, x_center={2}, y_center={3}, data_fail_b={4}, ttbar_fail_b={5}, ttbar_pass_b={6}, qcd_pass_b_exp={7}, data_pass_b_exp={8}, data_pass_b={9}'.format(i, j, x_center, y_center, data_fail_b, ttbar_fail_b, ttbar_pass_b, qcd_pass_b_exp, data_pass_b_exp, data_pass_b))
            
            mjj_vs_mjjj_pass_b_data.SetBinContent(i,j, data_pass_b)

            # semiboosted
            data_fail_sb = mjj_vs_mjjj_fail_sb_data.GetBinContent(i,j)
            ttbar_fail_sb = mjj_vs_mjjj_fail_sb_ttbar.GetBinContent(i,j)
            ttbar_pass_sb = mjj_vs_mjjj_pass_sb_ttbar.GetBinContent(i,j)
            
            qcd_fail_sb = (data_fail_sb - ttbar_fail_sb)
            
            if qcd_fail_sb < 0.:
                print('WARNING: qcd_fail_sb negative for (mjjj, mjj)=({0}, {1}). Manually set to 0 (data_fail_sb={2}, ttbar_fail_sb={3})'.format(x_center, y_center, data_fail_sb, ttbar_fail_sb))
                qcd_fail_sb = 0.

            qcd_pass_sb_exp = qcd_fail_sb * rpf_semiboosted_VR[year].Eval(x_center, y_center)
            
            # in case the transfer function becomes negative (it shouldn't in the phase space of interest)
            if qcd_pass_sb_exp < 0.:
                print('WARNING: Semiboosted transfer function negative for (mjjj, mjj)=({0}, {1})'.format(x_center, y_center))
                qcd_pass_sb_exp = 0.
            
            data_pass_sb_exp = (qcd_pass_sb_exp + ttbar_pass_sb)
            
            data_pass_sb = (rnd.PoissonD(data_pass_sb_exp) if data_pass_sb_exp>0. else 0.)
            
            #print('i={0}, j={1}, x_center={2}, y_center={3}, data_fail_sb={4}, ttbar_fail_sb={5}, ttbar_pass_sb={6}, qcd_pass_sb_exp={7}, data_pass_sb_exp={8}, data_pass_sb={9}'.format(i, j, x_center, y_center, data_fail_sb, ttbar_fail_sb, ttbar_pass_sb, qcd_pass_sb_exp, data_pass_sb_exp, data_pass_sb))
            
            mjj_vs_mjjj_pass_sb_data.SetBinContent(i,j, data_pass_sb)

            # write histograms
            data_file.cd()
            mjj_vs_mjjj_pass_b_data.Write("", ROOT.TObject.kOverwrite)
            mjj_vs_mjjj_pass_sb_data.Write("", ROOT.TObject.kOverwrite)


    ttbar_file.Close()
    data_file.Close()
    print('\n{0} region processing done.\n'.format(region))


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y 2017 -t symlink2histograms_2017/TTbar_Histograms.root -d symlink2histograms_2017/JetHT_Histograms.root"
    
    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year(s) (e.g. 2017, Run2)",
                        required=True,
                        metavar="YEAR")

    parser.add_argument("-t", "--ttbar", dest="ttbar",
                      help="Path to ttbar histograms",
                      metavar="TTBAR",
                      required=True)
    
    parser.add_argument("-d", "--data", dest="data",
                      help="Path to data histograms",
                      metavar="DATA",
                      required=True)
    
    parser.add_argument("-s", "--seed", dest="seed",
                      help="Random number generator seed",
                      metavar="SEED",
                      type=int,
                      default=4357) # according to https://root.cern.ch/doc/master/classTRandom3.html, the default value is 4357

    (options, args) = parser.parse_known_args()
    
    # generate toy data
    generate(options.year, options.ttbar, options.data, options.seed, 'VR')
    generate(options.year, options.ttbar, options.data, options.seed, 'SR')
