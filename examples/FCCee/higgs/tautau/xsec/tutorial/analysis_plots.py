import ROOT

# global parameters
intLumi        = 10.8e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow #tau #tau'
delphesVersion = '3.4.2'
energy         = 240
collider       = 'FCC-ee'
inputDir       = '/final/'
outdir         = '/plots/'
## you can save the plots in png or pdf or both
formats        = ['png']
#formats        = ['pdf']
## you can choose to plot in logarithmic or linear scale the y axis
#yaxis          = ['lin','log']
yaxis          = ['log']
## hree you can choose to stack or not your signals and backgrounds separately
stacksig       = ['nostack']
stackbkg       = ['stack']
splitLeg       = True ### to split legend for backgrounds and signals ###


## add the list of variable that you want to plot here, the name correspond to the name of the histogram saved in final
variables = [
    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_px",
    "RecoElectron_py",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
]

    
#Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
## add your selections from final
selections['']  = [
    "selNone",
]

extralabel = {}
## pretty labels for the selections, they will appear on your plots
extralabel['selNone'] = "Before selection"

colors = {}
## colors are from the ROOT color wheel or color table, assigned to each process
colors['ee_Htautau'] = ROOT.kCyan-7

plots = {}
## we decide what is going to be plotted as a signal (line histogram) or background (filled histogram)
## remember that you have to have at least one background for this to work
plots[''] = {'signal':{
                    'ee_Htautau':['ee_Htautau'],
                },
                'backgrounds':{
                    'ee_Htautau':['ee_Htautau'],
                },
                }

legend = {}
## pretty names for the processes, the format is TLatex https://root.cern.ch/doc/master/classTLatex.html
legend['ee_Htautau'] = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow #tau #tau'