# https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#nuisance-parameter-impacts
# https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/tutorial2023/parametric_exercise/?h=impacts#impacts_1

combineTool.py -M Impacts -d ws.root -m 125 --doInitialFit --cminDefaultMinimizerStrategy 0 --robustFit 1 -t -1 
combineTool.py -M Impacts -d ws.root -m 125 --doFits --cminDefaultMinimizerStrategy 0 --robustFit 1 -t -1 --parallel 30 
combineTool.py -M Impacts -d ws.root -m 125 -o impacts.json 
plotImpacts.py -i impacts.json -o impacts_r_ZH --POI r_ZH 

