# Installation (Lorien)

The following steps need to be done only once for the initial installation
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone -b v10.0.1 --depth 1 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone -b CMSWW_14_1_0_pre4 --depth 1 https://github.com/JHU-Tools/CombineHarvester.git
scram b clean
scram b -j 8
cd -

python3 -m venv twoD-env
source twoD-env/bin/activate
git clone https://github.com/JHU-Tools/2DAlphabet.git
cd 2DAlphabet
git checkout 74daef1
python setup.py develop

git clone git clone git@github.com:CMS-H3PO/HHH_2DAlphabet.git
cd HHH_2DAlphabet

mkdir -p logs
```
You now have all the required software installed and the enviroment set up.

To set up environment in a new shell, run the following
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_14_1_0_pre4
cmsenv
cd -
source twoD-env/bin/activate
cd HHH_2DAlphabet
```
or alternatively just source the activation script
```
cd HHH_2DAlphabet
source activate_env
```

# Running fits

First, define year for which you want to run the fits, e.g.
```
export YEAR=2017
export RND_SEED=1234567
```
or
```
export YEAR=Run2
export RND_SEED=95147
```
For running fits and making plots for the boosted validation region, run
```
python -u HHH_boosted_VR.py -y ${YEAR} |& tee logs/${YEAR}_boosted_VR_`date "+%Y%m%d_%H%M%S"`.log
```
To do the same for the semiboosted validation region, run
```
python -u HHH_semiboosted_VR.py -y ${YEAR} |& tee logs/${YEAR}_semiboosted_VR_`date "+%Y%m%d_%H%M%S"`.log
```
Note that piping output to the `tee` command will both print it to the terminal and save it in a log file. The log file name will contain a timestamp.

Now set the best polynomial orders for both `2017` and `Run2`
```
export BEST_B=1
export BEST_SB=1
```
To calculate expected limits, we first need to generate toy data in the pass category of the signal regions. For this we use the pass-to-fail transfer functions (Rpf) obtained from the validation region fits. First we need to extract the fit parameter values which can be done using the following commands
```
echo -e "Boosted VR:\nOrder ${BEST_B} (best)" |& tee logs/printFitParameters_${YEAR}_VR_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_boosted_VR/${BEST_B}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_VR_`date "+%Y%m%d"`.log
echo -e "\n\nSemiboosted VR:\nOrder ${BEST_SB} (best)" |& tee -a logs/printFitParameters_${YEAR}_VR_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_semiboosted_VR/${BEST_SB}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_VR_`date "+%Y%m%d"`.log
```
The printed fit parameter values need to be put into `plotRpf_VR.py` in order to plot the transfer functions
```
python plotRpf_VR.py -y ${YEAR}
```
The toy data is generated using the `generateToys.py` script which imports the transfer functions from `plotRpf_VR.py`
```
python generateToys.py -y ${YEAR} -s ${RND_SEED} -t symlink2histograms_${YEAR}/TTbar_Histograms.root -d symlink2histograms_${YEAR}/JetHT_Histograms.root |& tee logs/generateToys_${YEAR}_`date "+%Y%m%d"`.log
```
Two output files are produced, `JetHT_Histograms_VR_pass_toy.root` with the toy data in the pass category of the validation regions and `JetHT_Histograms_SR_pass_toy.root` with the toy data in the pass category of the signal regions. These files need to be moved to the same folder with the other histogram files
```
mv -v JetHT_Histograms_*_pass_toy.root symlink2histograms_${YEAR}
```
The toy data in the validation regions is used in `HHH_boosted_VR_pass_toy.py` and `HHH_semiboosted_VR_pass_toy.py` as a sort of sanity check (closure test) to check whether the toy data fits converge to parameter values similar to those used in the generation of the toy data
```
python -u HHH_boosted_VR_pass_toy.py -y ${YEAR} |& tee logs/${YEAR}_boosted_VR_pass_toy_`date "+%Y%m%d_%H%M%S"`.log
python -u HHH_semiboosted_VR_pass_toy.py -y ${YEAR} |& tee logs/${YEAR}_semiboosted_VR_pass_toy_`date "+%Y%m%d_%H%M%S"`.log
```
The Rpf parameter values can be printed with the following commands
```
echo -e "Boosted VR pass toy:\nOrder ${BEST_B} (best)" |& tee logs/printFitParameters_${YEAR}_VR_pass_toy_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_boosted_VR_pass_toy/${BEST_B}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_VR_pass_toy_`date "+%Y%m%d"`.log
echo -e "\n\nSemiboosted VR pass toy:\nOrder ${BEST_SB} (best)" |& tee -a logs/printFitParameters_${YEAR}_VR_pass_toy_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_semiboosted_VR_pass_toy/${BEST_SB}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_VR_pass_toy_`date "+%Y%m%d"`.log
```
The printed fit parameter values need to be put into `plotRpf_VR_pass_toy.py` in order to plot the transfer functions
```
python plotRpf_VR_pass_toy.py -y ${YEAR}
```

To perform the same checks for the signal region fits and calculate expected limits for the benchmark XToYHTo6B_MX-2500_MY-800 case for the boosted channel, run
```
python -u HHH_boosted_SR_pass_toy.py -y ${YEAR} |& tee logs/${YEAR}_boosted_SR_pass_toy_`date "+%Y%m%d_%H%M%S"`.log
```
To do the same for the semiboosted channel, run
```
python -u HHH_semiboosted_SR_pass_toy.py -y ${YEAR} |& tee logs/${YEAR}_semiboosted_SR_pass_toy_`date "+%Y%m%d_%H%M%S"`.log
```
Set the best polynomial orders for both `2017` and `Run2`
```
export BEST_B=1
export BEST_SB=1
```
The Rpf parameter values can be printed with the following commands
```
echo -e "Boosted SR pass toy:\nOrder ${BEST_B} (best)" |& tee logs/printFitParameters_${YEAR}_SR_pass_toy_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_boosted_SR_pass_toy/${BEST_B}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_SR_pass_toy_`date "+%Y%m%d"`.log
echo -e "\n\nSemiboosted SR pass toy:\nOrder ${BEST_SB} (best)" |& tee -a logs/printFitParameters_${YEAR}_SR_pass_toy_`date "+%Y%m%d"`.log
python printFitParameters.py -i ${YEAR}_semiboosted_SR_pass_toy/${BEST_SB}_area/fitDiagnosticsTest.root |& tee -a logs/printFitParameters_${YEAR}_SR_pass_toy_`date "+%Y%m%d"`.log
```
The printed fit parameter values need to be put into `plotRpf_SR_pass_toy.py` in order to plot the transfer functions
```
python plotRpf_SR_pass_toy.py -y ${YEAR}
```
Note that the best polynomial order for the toy data fits might in general be different from the real data fits.

To perform the same calculations for the combination of boosted and semiboosted channels, run
```
python -u HHH_combined_SR_pass_toy.py -y ${YEAR} |& tee logs/${YEAR}_combined_SR_pass_toy_`date "+%Y%m%d_%H%M%S"`.log
```
To calculate expected limits for multiple signal samples for the boosted channel, run
```
python -u HHH_boosted_SR_pass_toy_multiSignal.py -y ${YEAR} |& tee logs/${YEAR}_boosted_SR_pass_toy_multiSignal_`date "+%Y%m%d_%H%M%S"`.log
```
To do the same for the semiboosted channel, run
```
python -u HHH_semiboosted_SR_pass_toy_multiSignal.py -y ${YEAR} |& tee logs/${YEAR}_semiboosted_SR_pass_toy_multiSignal_`date "+%Y%m%d_%H%M%S"`.log
```
Note that some samples might require special processing with a modified `rMax` value for the limit calculation to converge. To calculate expected limits for multiple signal samples for the combination of boosted and semiboosted channels, run
```
python -u HHH_combined_SR_pass_toy_multiSignal.py -y ${YEAR} |& tee logs/${YEAR}_combined_SR_pass_toy_multiSignal_`date "+%Y%m%d_%H%M%S"`.log
```
Finally, to produce the expected limit plots, run
```
python -u plotLimits.py ${YEAR} |& tee logs/plotLimits_${YEAR}_`date "+%Y%m%d_%H%M%S"`.log
```
