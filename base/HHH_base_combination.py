from TwoDAlphabet import plot
from TwoDAlphabet.twoDalphabet import MakeCard, TwoDAlphabet
from TwoDAlphabet.alphawrap import BinnedDistribution, ParametricFunction
from TwoDAlphabet.helpers import make_env_tarball, cd, execute_cmd
from TwoDAlphabet.ftest import FstatCalc

'''--------------------------Helper functions---------------------------'''
def _gof_for_FTest(twoD, subtag, card_or_w='card.txt'):

    run_dir = twoD.tag+'/'+subtag
    
    with cd(run_dir):
        gof_data_cmd = [
            'combine -M GoodnessOfFit',
            '-d '+card_or_w,
            '--algo=saturated',
            '-n _gof_data'
        ]

        gof_data_cmd = ' '.join(gof_data_cmd)
        execute_cmd(gof_data_cmd)

def _get_other_region_names(pass_reg_name):
    return pass_reg_name, pass_reg_name.replace('pass','loose'),pass_reg_name.replace('pass','fail')

def _select_bkg(row, args):
    '''Used by the Ledger.select() method to create a subset of a Ledger.
    This function provides the logic to determine which entries/rows of the Ledger
    to keep for the subset. The first argument should always be the row to process.
    The arguments that follow will be the other arguments of Ledger.select().
    This function should ALWAYS return a bool that signals whether to keep (True)
    or drop (False) the row.

    To check if entries in the Ledger pass, we can access a given row's
    column value via attributes which are named after the columns (ex. row.process
    gets the "process" column). One can also access them as keys (ex. row["process"]).

    In this example, we want to select for signals that have a specific string
    in their name ("process"). Thus, the first element of `args` contains the string
    we want to find.

    We also want to pick a TF to use so the second element of `args` contains a
    string to specify the Background_args[1] process we want to use.

    Args:
        row (pandas.Series): The row to evaluate.
        args (list): Arguments to pass in for the evaluation.

    Returns:
        Bool: True if keeping the row, False if dropping.
    '''
    polyOrderB  = args[0]
    polyOrderSB = args[1]
    if row.process_type == 'SIGNAL':
        if len(args)>2:
            signame = args[2]
            if signame in row.process:
                return True
            else:
                return False
        else:
            return True
    elif 'qcd_' in row.process:
        if row.process == 'qcd_b_'+polyOrderB:
            print("Keeping ", row.process)
            return True
        elif row.process == 'qcd_sb_'+polyOrderSB:
            print("Keeping ", row.process)
            return True
        else:
            return False
    else:
        return True

def _load_CR_rpf(poly_order):
    twoD_CRonly = TwoDAlphabet('XHYfits_CR','XHYbbWW.json', loadPrevious=True)
    params_to_set = twoD_CRonly.GetParamsOnMatch('rpf.*'+poly_order, 'MX_2000_MY_800_area', 'b')
    return {k:v['val'] for k,v in params_to_set.items()}


def _load_fit_rpf(working_area,polyOrderB,polyOrderSB,json_file):
    twoD_blindFit = TwoDAlphabet(working_area,json_file, loadPrevious=True)
    params_to_set = twoD_blindFit.GetParamsOnMatch('rpf.*', '{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB), 'b')
    return {k:v['val'] for k,v in params_to_set.items()}

def _load_CR_rpf_as_SR(poly_order):
    params_to_set = {}
    for k,v in _load_CR_rpf(poly_order).items():
        params_to_set[k.replace('CR','SR')] = v
    return params_to_set

def _generate_constraints(nparams):
    out = {}
    for i in range(nparams):
        if i == 0:
            out[i] = {"MIN":0,"MAX":10,"NOM":1}
        else:
            out[i] = {"MIN":-100,"MAX":100,"NOM":0}
    return out


# we are working in a 2D space, so linear in X, linear in Y just change the shape of the transfer function
_b_rpf_options = {
    '0': {
        'form': '0.01*(@0)',
        'constraints': _generate_constraints(1)
    },
    '1': {
        'form': '0.01*(@0+@1*x+@2*y)',
        'constraints': _generate_constraints(3)
    },

    '2': {
        'form': '0.01*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2)',
        'constraints': _generate_constraints(6)
    },
    '3': {
        'form': '0.01*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3)',
        'constraints': _generate_constraints(9)
    }
    # '4': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4)',
    #     'constraints': _generate_constraints(12)
    # },
    # '5': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4+@12*x**5+@13*y*x**4+@14*y*y*x**3)',
    #     'constraints': _generate_constraints(15)
    # },
    # '6': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4+@12*x**5+@13*y*x**4+@14*y*y*x**3+@15*x**6+@16*x**5*y+@17*x**4*y*y)',
    #     'constraints': _generate_constraints(18)
    # }
}
    
_sb_rpf_options = {
    '0': {
        'form': '0.01*(@0)',
        'constraints': _generate_constraints(1)
    },
    '1': {
        'form': '0.01*(@0+@1*x+@2*y)',
        'constraints': _generate_constraints(3)
    },

    '2': {
        'form': '0.01*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2)',
        'constraints': _generate_constraints(6)
    },
    '3': {
        'form': '0.01*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3)',
        'constraints': _generate_constraints(9)
    }
    # '4': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4)',
    #     'constraints': _generate_constraints(12)
    # },
    # '5': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4+@12*x**5+@13*y*x**4+@14*y*y*x**3)',
    #     'constraints': _generate_constraints(15)
    # },
    # '6': {
    #     'form': '0.002*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y**2+@6*x*x*y+@7*x*y*y+@8*x**3+@9*x**3*y+@10*x*x*y*y+@11*x**4+@12*x**5+@13*y*x**4+@14*y*y*x**3+@15*x**6+@16*x**5*y+@17*x**4*y*y)',
    #     'constraints': _generate_constraints(18)
    # }
}

'''---------------Primary functions---------------------------'''
def test_make(working_area,jsonConfig,findreplace={}):

    # Create the twoD object which starts by reading the JSON config and input arguments to
    # grab input simulation and data histograms, rebin them if needed, and save them all
    # in one place (organized_hists.root). The modified JSON config (with find-replaces applied, etc)
    # is also saved as runConfig.json. This means, if you want to share your analysis with
    # someone, they can grab everything they need from this one spot - no need to have access to
    # the original files! (Note though that you'd have to change the config to point to organized_hists.root).
    twoD = TwoDAlphabet(working_area, jsonConfig, loadPrevious=False,findreplace=findreplace)
    qcd_hists = twoD.InitQCDHists() # Create the data - BKGs histograms

    # QCD for boosted
    binning_b_f, _ = twoD.GetBinningFor("fail_boosted")
    # QCD for semiboosted
    binning_sb_f, _ = twoD.GetBinningFor("fail_semiboosted")

    # Next we construct the Alphabet objects which all inherit from the Generic2D class.
    # This class constructs and stores RooAbsArg objects (RooRealVar, RooFormulaVar, etc)
    # which represent each bin in the space.

    # First we make a BinnedDistribution which is a collection of RooRealVars built from a starting
    # histogram (`qcd_hists[f]`). These can be set to be constants but, if not, they become free floating
    # parameters in the fit.
    
    # QCD for boosted
    fail_name_b = 'qcd_b_fail'
    qcd_b_f = BinnedDistribution(
                fail_name_b, qcd_hists["fail_boosted"],
                binning_b_f, constant=False
            )
    # QCD for semiboosted
    fail_name_sb = 'qcd_sb_fail'
    qcd_sb_f = BinnedDistribution(
                fail_name_sb, qcd_hists["fail_semiboosted"],
                binning_sb_f, constant=False
            )
    # We'll then book a flat TF which will be used to transfer between loose and pass
    # We keep it out of the loop below though because this will keep the same form
    # while the fail-to-loose TF changes with the different possible options.

    # We add it to `twoD` so its included when making the RooWorkspace and ledger.
    # We specify the name of the process, the region it lives in, and the object itself.
    # The process is assumed to be a background and colored yellow but this can be changed
    # with optional arguments.
    
    # QCD for boosted
    twoD.AddAlphaObj('qcd',"fail_boosted",qcd_b_f, title="Background")
    # QCD for semiboosted
    twoD.AddAlphaObj('qcd',"fail_semiboosted",qcd_sb_f, title="Background")

    # As a global variables, we've defined some different transfer function (TF) options.
    # We only want to include one of these at the time of fitting but we want to construct
    # them all right now so we can pick and choose later.
    
    # QCD for boosted
    for opt_name, opt in _b_rpf_options.items():
        # We have two regions determined by a TF, "pass" and "loose" with the "pass"
        # being a simple flat scaling of the loose. The functional form and the
        # dictionary of constraints is defined in _rpf_options so we just plug
        # these in, being careful to name the objects uniquely (this affects
        # the naming of the RooFormulaVars created, which need to be unique).

        # The ParametricFunction class is the same as the BinnedDistribution except
        # the bins are RooFormulaVars constructed from the input formula with the
        # "x" and "y" taken as the centers of each bin.
        # The constraints option takes as input a dictionary with keys that control
        # the minimum, maximum, and error (initial step) of each parameter. It can
        # also be used to specify if the parameter should be unconstrainted (flatParam)
        # or Gaussian constrained (param <mu> <sigma>).

        qcd_b_rpfT = ParametricFunction(
                    fail_name_b.replace('fail','rpfT')+'_'+opt_name,
                    binning_b_f, opt['form'],
                    constraints=opt['constraints']
            )

        qcd_b_t = qcd_b_f.Multiply(fail_name_b.replace('fail','pass')+'_'+opt_name, qcd_b_rpfT)

        # Now add the final models to the `twoD` object for tracking
        # Note that we have unique process names so they are identifiable
        # but we give them different titles so that they look pretty in
        # the final plot legends.

        twoD.AddAlphaObj('qcd_b_'+opt_name,"pass_boosted",qcd_b_t,title='Background')

    # QCD for semiboosted
    for opt_name, opt in _sb_rpf_options.items():
        # We have two regions determined by a TF, "pass" and "loose" with the "pass"
        # being a simple flat scaling of the loose. The functional form and the
        # dictionary of constraints is defined in _rpf_options so we just plug
        # these in, being careful to name the objects uniquely (this affects
        # the naming of the RooFormulaVars created, which need to be unique).

        # The ParametricFunction class is the same as the BinnedDistribution except
        # the bins are RooFormulaVars constructed from the input formula with the
        # "x" and "y" taken as the centers of each bin.
        # The constraints option takes as input a dictionary with keys that control
        # the minimum, maximum, and error (initial step) of each parameter. It can
        # also be used to specify if the parameter should be unconstrainted (flatParam)
        # or Gaussian constrained (param <mu> <sigma>).

        qcd_sb_rpfT = ParametricFunction(
                    fail_name_sb.replace('fail','rpfT')+'_'+opt_name,
                    binning_sb_f, opt['form'],
                    constraints=opt['constraints']
            )

        qcd_sb_t = qcd_sb_f.Multiply(fail_name_sb.replace('fail','pass')+'_'+opt_name, qcd_sb_rpfT)

        # Now add the final models to the `twoD` object for tracking
        # Note that we have unique process names so they are identifiable
        # but we give them different titles so that they look pretty in
        # the final plot legends.

        twoD.AddAlphaObj('qcd_sb_'+opt_name,"pass_semiboosted",qcd_sb_t,title='Background')

    # Save() will save the RooWorkspace and the ledgers and other associated pieces
    # so the twoD object can be reconstructed later. If this line doesn't run or
    # if something in the above needs to change, everything will need to be re-run to this point.
    twoD.Save()
    

def test_fit(working_area,polyOrderB,polyOrderSB,sigName=None,defMinStrat=0,rInit=0,rMin=-1,rMax=10,setParams={},extra=''):
    twoD = TwoDAlphabet(working_area, '%s/runConfig.json'%working_area, loadPrevious=True)
    if sigName is not None:
        subset = twoD.ledger.select(_select_bkg, polyOrderB, polyOrderSB, sigName)
    else:
        subset = twoD.ledger.select(_select_bkg, polyOrderB, polyOrderSB)
    twoD.MakeCard(subset, '{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB))
    twoD.MLfit('{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB),defMinStrat=defMinStrat,rInit=rInit,rMin=rMin,rMax=rMax,setParams=setParams,extra=extra,verbosity=0)

def test_limit(working_area,polyOrderB,polyOrderSB,json_file,blind=True,defMinStrat=0,extra=''):
    '''Perform a blinded limit. To be blinded, the Combine algorithm (via option `--run blind`)
    will create an Asimov toy dataset from the pre-fit model. Since the TF parameters are meaningless
    in our true "pre-fit", we need to load in the parameter values from a different fit so we have
    something reasonable to create the Asimov toy. 
    '''
    # Returns a dictionary of the TF parameters with the names as keys and the post-fit values as dict values.
    params_to_set = _load_fit_rpf(working_area,polyOrderB,polyOrderSB,json_file)
    print(params_to_set)
    twoD = TwoDAlphabet(working_area, json_file, loadPrevious=True)

    # Make a subset and card as in test_fit()
    #subset = twoD.ledger.select(_select_bkg,poly_order)
    #twoD.MakeCard(subset, poly_order+'_area')
    # Run the blinded limit with our dictionary of TF parameters
    twoD.Limit(
        subtag='{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB),
        blindData=blind,
        verbosity=1,
        defMinStrat=defMinStrat,
        setParams=params_to_set,
        condor=False,
        extra=extra
    )


def test_plot(working_area,polyOrderB,polyOrderSB):
    '''Load the twoD object again and run standard plots for a specific subtag.
    Assumes loading the Ledger in this sub-directory but a different one can
    be provided if desired.
    '''
    twoD = TwoDAlphabet(working_area, '%s/runConfig.json'%working_area, loadPrevious=True)
    subset = twoD.ledger.select(_select_bkg, polyOrderB, polyOrderSB)
    twoD.StdPlots('{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB), subset)

def test_GoF(working_area,polyOrderB,polyOrderSB):
    '''Perform a Goodness of Fit test using an existing working area.
    Requires using data so SRorCR is enforced to be 'CR' to avoid accidental unblinding.
    '''

    twoD = TwoDAlphabet(working_area, '%s/runConfig.json'%working_area, loadPrevious=True)
    # Run the Goodness of fit test with 500 toys, r floating, TF parameters set to prefit.
    # This method always runs the evaluation on data interactively but the toy generation and evaluation
    # can be sent to condor with condor=True and split over several jobs with njobs=<int>.
    # Note that running a GoF test without data is relatively meaningless so by using this method,
    # you must unblind data. If you wish to use a toy dataset instead, you should set that
    # up when making the card.
    twoD.GoodnessOfFit(
        '{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB), ntoys=500, freezeSignal=False,
        condor=True, njobs=10, card_or_w='card.txt', lorienTag=True
    )

    # Note that no plotting is done here since one needs to wait for the condor jobs to finish first.
    # See test_GoF_plot() for plotting (which will also collect the outputs from the jobs).


def test_GoF_plot(working_area,polyOrderB,polyOrderSB):
    plot.plot_gof(working_area,'{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB), condor=True,lorien=True)


def test_Impacts(working_area,polyOrderB,polyOrderSB):

    twoD = TwoDAlphabet(working_area, '%s/runConfig.json'%working_area, loadPrevious=True)
    subset = twoD.ledger.select(_select_bkg, polyOrderB, polyOrderSB)

    twoD.Impacts(
        '{0}-b_{1}-sb_area'.format(polyOrderB, polyOrderSB),
        cardOrW='TnP.root'
    )


def test_FTest(working_area,orders1,orders2):
    '''Perform an F-test using existing working areas.
    '''

    twoD    = TwoDAlphabet(working_area, '%s/runConfig.json'%working_area, loadPrevious=True)

    binning_b  = twoD.binnings["default"]
    binning_sb = twoD.binnings["default"]
    nBins   = (len(binning_b.xbinList)-1)*(len(binning_b.ybinList)-1)+(len(binning_sb.xbinList)-1)*(len(binning_sb.ybinList)-1)

    #Get number of RPF params and run GoF for orders1
    params1 = twoD.ledger.select(_select_bkg, orders1[0], orders1[1]).alphaParams
    rpfSet1 = params1[params1["name"].str.contains("rpf")]
    nRpfs1  = len(rpfSet1.index)
    _gof_for_FTest(twoD, "{0}-b_{1}-sb_area".format(orders1[0],orders1[1]), card_or_w='card.txt')
    gofFile1= working_area+"/{0}-b_{1}-sb_area/higgsCombine_gof_data.GoodnessOfFit.mH120.root".format(orders1[0],orders1[1])

    #Get number of RPF params and run GoF for orders2
    params2 = twoD.ledger.select(_select_bkg, orders2[0], orders2[1]).alphaParams
    rpfSet2 = params2[params2["name"].str.contains("rpf")]
    nRpfs2  = len(rpfSet2.index)
    _gof_for_FTest(twoD, "{0}-b_{1}-sb_area".format(orders2[0],orders2[1]), card_or_w='card.txt')
    gofFile2= working_area+"/{0}-b_{1}-sb_area/higgsCombine_gof_data.GoodnessOfFit.mH120.root".format(orders2[0],orders2[1])

    base_fstat = FstatCalc(gofFile1,gofFile2,nRpfs1,nRpfs2,nBins)
    print(base_fstat)

    def plot_FTest(base_fstat,nRpfs1,nRpfs2,nBins):
        from ROOT import TF1, TH1F, TLegend, TPaveText, TLatex, TArrow, TCanvas, kRed, kBlue, gStyle
        gStyle.SetOptStat(0000)
        gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
        gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

        if len(base_fstat) == 0: base_fstat = [0.0]

        ftest_p1    = min(nRpfs1,nRpfs2)
        ftest_p2    = max(nRpfs1,nRpfs2)
        ftest_nbins = nBins
        fdist       = TF1("fDist", "[0]*TMath::FDist(x, [1], [2])", 0,max(10,1.3*base_fstat[0]))
        fdist.SetParameter(0,1)
        fdist.SetParameter(1,ftest_p2-ftest_p1)
        fdist.SetParameter(2,ftest_nbins-ftest_p2)

        pval = fdist.Integral(0.0,base_fstat[0])
        print('P-value: %s'%pval)

        c = TCanvas('c','c',800,600)    
        c.SetLeftMargin(0.12) 
        c.SetBottomMargin(0.12)
        c.SetRightMargin(0.1)
        c.SetTopMargin(0.1)
        ftestHist_nbins = 30
        ftestHist = TH1F("Fhist","",ftestHist_nbins,0,max(10,1.3*base_fstat[0]))
        ftestHist.GetXaxis().SetTitle("F = #frac{-2log(#lambda_{1}/#lambda_{2})/(p_{2}-p_{1})}{-2log#lambda_{2}/(n-p_{2})}")
        ftestHist.GetXaxis().SetTitleSize(0.025)
        ftestHist.GetXaxis().SetTitleOffset(2)
        ftestHist.GetYaxis().SetTitleOffset(0.85)
        
        ftestHist.Draw("pez")
        ftestobs  = TArrow(base_fstat[0],0.25,base_fstat[0],0)
        ftestobs.SetLineColor(kBlue+1)
        ftestobs.SetLineWidth(2)
        fdist.SetLineColor(kRed)
        fdist.Draw('same')

        ftestobs.Draw()
        tLeg = TLegend(0.6,0.73,0.89,0.89)
        tLeg.SetLineWidth(0)
        tLeg.SetFillStyle(0)
        tLeg.SetTextFont(42)
        tLeg.SetTextSize(0.03)
        tLeg.AddEntry(ftestobs,"observed = %.3f"%base_fstat[0],"l")
        tLeg.AddEntry(fdist,"F-dist, ndf = (%.0f, %.0f) "%(fdist.GetParameter(1),fdist.GetParameter(2)),"l")
        tLeg.Draw("same")

        model_info = TPaveText(0.2,0.6,0.4,0.8,"brNDC")
        model_info.AddText('p1 = {0}-b_{1}-sb'.format(orders1[0],orders1[1]))
        model_info.AddText('p2 = {0}-b_{1}-sb'.format(orders2[0],orders2[1]))
        model_info.AddText("p-value = %.2f"%(1-pval))
        model_info.Draw('same')
        
        latex = TLatex()
        latex.SetTextAlign(11)
        latex.SetTextSize(0.06)
        latex.SetTextFont(62)
        latex.SetNDC()
        latex.DrawLatex(0.12,0.91,"CMS")
        latex.SetTextSize(0.05)
        latex.SetTextFont(52)
        latex.DrawLatex(0.65,0.91,"Work in Progress")
        latex.SetTextFont(42)
        latex.SetTextFont(52)
        latex.SetTextSize(0.045)
        for ext in ["png", "pdf"]:
            c.SaveAs(working_area+'/ftest_{0}{1}-bsb_vs_{2}{3}-bsb_notoys.{4}'.format(orders1[0],orders1[1],orders2[0],orders2[1],ext))

    plot_FTest(base_fstat,nRpfs1,nRpfs2,nBins)
