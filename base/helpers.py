from TwoDAlphabet.config import Config
import ROOT


def get_bin_content_by_name(hist, name):
    axis = hist.GetXaxis()
    bin_number = axis.FindBin(name)
    return hist.GetBinContent(bin_number)


def add_tt_pnet_sf_to_card(working_area,subtag):
    if 'combined' in working_area:
        combined = True
    else:
        combined = False

    jsonConfig = f"{working_area}/runConfig.json"
    config = Config(jsonConfig)
    df = config.FullTable()

    source_filename = df.loc[
        df["process"] == "TTbar",
        "source_filename"
    ].dropna().unique()[0]

    inFile = ROOT.TFile.Open(source_filename)

    regions = ["pass"]
    suffixes = [""]

    if combined:
        regions = ["pass_boosted", "pass_semiboosted"]
        suffixes = ["_b", "_sb"]

    eff = []

    for r in regions:
        source_histname = df.loc[
            (df["process"] == "TTbar") &
            (df["region"] == r) &
            (df["variation"] == "nominal"),
            "source_histname"
        ].dropna().unique()[0]

        histname = source_histname.replace("mjj_vs_mjjj","cutFlowHisto").replace("_pass","")

        cutFlowHisto = inFile.Get(histname)

        _pass = get_bin_content_by_name(cutFlowHisto, "Pass")
        _fail = get_bin_content_by_name(cutFlowHisto, "Fail")
        
        eff.append(_pass/(_pass + _fail))

    datacard_path = f"{working_area}/{subtag}/card.txt"
    with open(datacard_path, 'a+') as datacard:
        datacard.seek(0)
    
        for i, r in enumerate(regions):
            suffix = suffixes[i]
            rate_param_pass = f'CMS_ttbar_mistag_PNet{suffix}'
            rate_param_fail = f'tt_scale_fail{suffix}'
            efficiency = "%.4f" % eff[i]
            channel = r.split("_")[-1] if "_" in r else ""

            pass_line = f'{rate_param_pass} rateParam pass_{channel}* TTbar 1.0 [0.0,3.0]\n'
            fail_line = f'{rate_param_fail} rateParam fail_{channel}* TTbar (1-{efficiency}*@0)/(1-{efficiency}) {rate_param_pass}\n'

            datacard.write(pass_line)
            datacard.write(fail_line)
