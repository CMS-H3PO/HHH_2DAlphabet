import os
from argparse import ArgumentParser
import ROOT


def process_bin(ch, rnd, x_min, x_max, y_min, y_max, i, j, rpf, mjj_vs_mjjj_fail_ttbar, mjj_vs_mjjj_pass_ttbar, mjj_vs_mjjj_fail_data, mjj_vs_mjjj_pass_data):

    x_center = mjj_vs_mjjj_pass_data.GetXaxis().GetBinCenter(i)
    y_center = mjj_vs_mjjj_pass_data.GetYaxis().GetBinCenter(j)

    if x_center < x_min or x_center > x_max: return
    if y_center < y_min or y_center > y_max: return

    data_fail = mjj_vs_mjjj_fail_data.GetBinContent(i,j)
    ttbar_fail = mjj_vs_mjjj_fail_ttbar.GetBinContent(i,j)
    ttbar_pass = mjj_vs_mjjj_pass_ttbar.GetBinContent(i,j)

    qcd_fail = (data_fail - ttbar_fail)

    if qcd_fail < 0.:
        print(f'WARNING: qcd_fail_{ch} negative for (mjjj, mjj)=({x_center}, {y_center}). Manually set to 0 (data_fail_{ch}={data_fail}, ttbar_fail_{ch}={ttbar_fail})')
        qcd_fail = 0.

    qcd_pass_exp = qcd_fail * rpf.Eval(x_center, y_center)

    # in case the transfer function becomes negative (it shouldn't in the phase space of interest)
    if qcd_pass_exp < 0.:
        print(f'WARNING: Transfer function negative for (mjjj, mjj)=({x_center}, {y_center})')
        qcd_pass_exp = 0.

    data_pass_exp = (qcd_pass_exp + ttbar_pass)

    data_pass = (rnd.PoissonD(data_pass_exp) if data_pass_exp>0. else 0.)

    print(f'i={i}, j={j}, x_center={x_center}, y_center={y_center}, data_fail_{ch}={data_fail}, ttbar_fail_{ch}={ttbar_fail}, ttbar_pass_{ch}={ttbar_pass}, qcd_pass_{ch}_exp={qcd_pass_exp}, data_pass_{ch}_exp={data_pass_exp}, data_pass_{ch}={data_pass}')

    mjj_vs_mjjj_pass_data.SetBinContent(i,j, data_pass)

    return


def generate(year, ttbar_path, data_path, seed, region):
    from plotRpf import x_min_b, x_max_b, y_min_b, y_max_b, x_min_sb, x_max_sb, y_min_sb, y_max_sb, rpf_boosted, rpf_semiboosted

    print(f'Processing {region} region for {year}...\n')

    print(f'INFO: Random number generator seed: {seed}')

    # random number generator
    rnd = ROOT.TRandom3(seed)

    data_toy_file = os.path.splitext(os.path.basename(data_path))[0] + f"_{region}_pass_toy.root"
    
    cmd = f"cp {data_path} {data_toy_file}"
    print(cmd + '\n')
    os.system(cmd)
    
    # histogram files
    ttbar_file = ROOT.TFile.Open(ttbar_path, 'READ')
    data_file = ROOT.TFile.Open(data_toy_file, 'UPDATE')

    # histograms: boosted
    mjj_vs_mjjj_fail_b_ttbar = ttbar_file.Get(f'mjj_vs_mjjj_{region}_fail_boosted_nominal')
    mjj_vs_mjjj_pass_b_ttbar = ttbar_file.Get(f'mjj_vs_mjjj_{region}_pass_boosted_nominal')

    mjj_vs_mjjj_fail_b_data = data_file.Get(f'mjj_vs_mjjj_{region}_fail_boosted_nominal')
    mjj_vs_mjjj_pass_b_data = data_file.Get(f'mjj_vs_mjjj_{region}_pass_boosted_nominal')

    # histograms: semiboosted
    mjj_vs_mjjj_fail_sb_ttbar = ttbar_file.Get(f'mjj_vs_mjjj_{region}_fail_semiboosted_nominal')
    mjj_vs_mjjj_pass_sb_ttbar = ttbar_file.Get(f'mjj_vs_mjjj_{region}_pass_semiboosted_nominal')

    mjj_vs_mjjj_fail_sb_data = data_file.Get(f'mjj_vs_mjjj_{region}_fail_semiboosted_nominal')
    mjj_vs_mjjj_pass_sb_data = data_file.Get(f'mjj_vs_mjjj_{region}_pass_semiboosted_nominal')

    # loop over histogram bins (boosted and semiboosted histograms have the same layout)
    for i in range(1,mjj_vs_mjjj_pass_b_data.GetNbinsX() + 1):
        for j in range(1,mjj_vs_mjjj_pass_b_data.GetNbinsY() + 1):

            # boosted
            process_bin('b', rnd, x_min_b, x_max_b, y_min_b, y_max_b, i, j, rpf_boosted[year]["VR"], mjj_vs_mjjj_fail_b_ttbar, mjj_vs_mjjj_pass_b_ttbar, mjj_vs_mjjj_fail_b_data, mjj_vs_mjjj_pass_b_data)

            # semiboosted
            process_bin('sb', rnd, x_min_sb, x_max_sb, y_min_sb, y_max_sb, i, j, rpf_semiboosted[year]["VR"], mjj_vs_mjjj_fail_sb_ttbar, mjj_vs_mjjj_pass_sb_ttbar, mjj_vs_mjjj_fail_sb_data, mjj_vs_mjjj_pass_sb_data)

    # write histograms
    data_file.cd()
    mjj_vs_mjjj_pass_b_data.Write("", ROOT.TObject.kOverwrite)
    mjj_vs_mjjj_pass_sb_data.Write("", ROOT.TObject.kOverwrite)


    ttbar_file.Close()
    data_file.Close()
    print(f'\n{region} region processing done.\n')


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y Run2 -t symlink2histograms_Run2/TTbar_Histograms.root -d symlink2histograms_Run2/JetHT_Histograms.root"
    
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
