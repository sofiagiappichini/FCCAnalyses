# https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#nuisance-parameter-impacts
# https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/tutorial2023/parametric_exercise/?h=impacts#impacts_1

# impact plot
combineTool.py -M Impacts -d ws.root -m 125 --doInitialFit --cminDefaultMinimizerStrategy 0 --robustFit 1 -t -1 -P r_ZH -P r_VBF --setParameterRanges r_ZH=-1,2:r_VBF=-5,5 --setParameters r_ZH=1,r_VBF=1  
combineTool.py -M Impacts -d ws.root -m 125 --doFits --cminDefaultMinimizerStrategy 0 --robustFit 1 -t -1 --parallel 30 -P r_ZH -P r_VBF --setParameterRanges r_ZH=-1,2:r_VBF=-5,5 --setParameters r_ZH=1,r_VBF=1 
combineTool.py -M Impacts -d ws.root -m 125 -o impacts.json -P r_ZH -P r_VBF --setParameterRanges r_ZH=-1,2:r_VBF=-5,5 --setParameters r_ZH=1,r_VBF=1 
plotImpacts.py -i impacts.json -o impacts_r_ZH --POI r_ZH
plotImpacts.py -i impacts.json -o impacts_r_VBF --POI r_VBF

# 2d scan plot
combine -M MultiDimFit ws.root -m 125 -n .scan --algo grid --points 800 --robustFit 1 -t -1 --cminDefaultMinimizerStrategy 0 -P r_ZH -P r_VBF --setParameterRanges r_ZH=-1,2:r_VBF=-5,5 --setParameters r_ZH=1,r_VBF=1
python3 /work/sgiappic/CMSSW_14_1_0_pre4/src/HiggsAnalysis/CombinedLimit/data/tutorials/parametric_exercise/plot_2D_scan.py