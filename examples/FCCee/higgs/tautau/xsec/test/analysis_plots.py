import ROOT

# global parameters
intLumi        = 180.0e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = '/final/'
outdir         = '/plots/'
formats        = ['png']
#formats        = ['pdf']
#yaxis          = ['lin','log']
yaxis          = ['log']
stacksig       = ['nostack']
stackbkg       = ['stack']
#legendCoord    = [0.68,0.76,0.96,0.88]
#plotStatUnc    = True ### to include statistical uncertainty ###
splitLeg       = True ### to split legend for backgrounds and signals ###

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
selections['']  = [
    "selNone",
]

extralabel = {}
extralabel['selNone'] = "Before selection"
colors = {}

colors['ee_Htautau'] = ROOT.kCyan-7
plots = {}
plots[''] = {'signal':{
                    'ee_Htautau':['ee_Htautau'],
                },
                'backgrounds':{
                },
                }

legend = {}

legend['ee_Htautau'] = 'e^+ e^- #rightarrow e^+ e^- H, H #rightarrow #tau #tau'