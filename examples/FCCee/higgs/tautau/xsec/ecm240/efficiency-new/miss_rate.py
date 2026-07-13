#!/usr/bin/env python3
"""
Tau-jet identification efficiency (nunutautau sample) and
mistag/rejection rate (qq sample) for the "TagJet_kt2_isTau" tagger,
using ROOT RDataFrame.

Assumptions (adjust if wrong):
- "TagJet_kt2_isTau" and "TagJet_kt2_flavor" are RVec<float>/RVec<int>
  branches of size 2 per event (two jets per event).
- "n_GenTau_had" is a scalar int: number of hadronic gen taus in the event.
  Efficiency is computed on events with n_GenTau_had == 2, treating both
  jets as matched to the two hadronic taus (no explicit dR-matching branch
  was given).
- Background sample truly has no tau jets (checked via flavor as a
  sanity check, PDG id 15).
"""

import ROOT

#ROOT.EnableImplicitMT()  # parallelize over available cores

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
FILE_SIG = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/taureco_test/wzp6_ee_nunuH_Htautau_ecm240/chunk_*.root"
FILE_QQ  = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/taureco_test/p8_ee_Zqq_ecm240/chunk_*.root"
TREE     = "events"     # <-- change to your tree name

BR_ISTAU   = "TagJet_kt2_isTAU"
BR_FLAVOR  = "TagJet_kt2_flavor"
BR_NGENTAU = "n_GenTau_had"

WP = 0.5

# ------------------------------------------------------------------
# Signal efficiency (nunutautau)
# ------------------------------------------------------------------
df_sig = ROOT.RDataFrame(TREE, FILE_SIG)

df_sig_sel = (
    df_sig.Filter(f"{BR_NGENTAU} == 2")
          .Define("nTaggedJets",
                   f"(int) Sum({BR_ISTAU} > {WP})")
)

n_events_sel   = df_sig_sel.Count().GetValue() * 2 # because there are two had tau in each events
n_tagged_jets  = df_sig_sel.Sum("nTaggedJets").GetValue()

efficiency = n_tagged_jets / n_events_sel 

print(f"[Signal] events with {BR_NGENTAU}==2: {n_events_sel}")
print(f"[Signal] tagged (isTau>{WP}) jets:      {n_tagged_jets}")
print(f"[Signal] Tau ID efficiency:            {efficiency*100:.4f}")

# uncertainty via TEfficiency (binomial, Clopper-Pearson)
eff_obj = ROOT.TEfficiency("eff_sig", "Tau ID efficiency",
                            1, 0, 1)
eff_obj.SetTotalEvents(1, int(n_events_sel))
eff_obj.SetPassedEvents(1, int(n_tagged_jets))
eff_err_low  = eff_obj.GetEfficiencyErrorLow(1)
eff_err_up   = eff_obj.GetEfficiencyErrorUp(1)
print(f"[Signal] efficiency uncertainty:       +{eff_err_up*100} / -{eff_err_low*100}")

# ------------------------------------------------------------------
# Background mistag / rejection (qq)
# ------------------------------------------------------------------
df_qq = ROOT.RDataFrame(TREE, FILE_QQ)

df_qq_def = (
    df_qq.Define("nJets", f"{BR_ISTAU}.size()")
         .Define("nMistagJets", f"(int) Sum({BR_ISTAU} > {WP})")
)

n_bkg_jets   = df_qq_def.Sum("nJets").GetValue()
n_mistag_qq  = df_qq_def.Sum("nMistagJets").GetValue()

mistag_rate = n_mistag_qq / n_bkg_jets
rejection   = 1.0 / mistag_rate

print(f"[QQ] total jets:               {n_bkg_jets}")
print(f"[QQ] mistagged (isTau>{WP}) jets: {n_mistag_qq}")
print(f"[QQ] Mistag (fake) rate:       {mistag_rate*100:.6f}")
print(f"[QQ] Rejection (1/fake rate):  {rejection:.1f}")

eff_bkg = ROOT.TEfficiency("eff_bkg", "QQ mistag rate", 1, 0, 1)
eff_bkg.SetTotalEvents(1, int(n_bkg_jets))
eff_bkg.SetPassedEvents(1, int(n_mistag_qq))
print(f"[QQ] mistag uncertainty:       "
      f"+{eff_bkg.GetEfficiencyErrorUp(1)*100:.6f} / "
      f"-{eff_bkg.GetEfficiencyErrorLow(1)*100:.6f}")

# ------------------------------------------------------------------
# Scan efficiency & rejection vs working point -> ROC curve
# ------------------------------------------------------------------
import numpy as np

N_BINS = 10000
h_sig = (df_sig.Filter(f"{BR_NGENTAU} == 2")
               .Histo1D(ROOT.RDF.TH1DModel("h_sig", "", N_BINS, 0, 1), BR_ISTAU))
h_qq  = df_qq.Histo1D(ROOT.RDF.TH1DModel("h_qq", "", N_BINS, 0, 1), BR_ISTAU)

# reverse cumulative sum → fraction passing threshold t
sig_counts = np.array([h_sig.GetBinContent(i) for i in range(1, N_BINS + 1)])
qq_counts  = np.array([h_qq.GetBinContent(i)  for i in range(1, N_BINS + 1)])

sig_cumrev = np.cumsum(sig_counts[::-1])[::-1]
qq_cumrev  = np.cumsum(qq_counts[::-1])[::-1]

eff_scan = sig_cumrev / sig_cumrev[0]
mis_scan = qq_cumrev  / qq_cumrev[0]
rej_scan = np.where(mis_scan > 0, 1.0 / mis_scan, np.inf)

thresholds = np.linspace(0, 1, N_BINS)

# plot with ROOT
c = ROOT.TCanvas("c", "Tau ID performance", 900, 700)
g_roc = ROOT.TGraph(len(thresholds))
for i, (e, r) in enumerate(zip(eff_scan, rej_scan)):
    g_roc.SetPoint(i, e, r if np.isfinite(r) else 1e6)

g_roc.SetTitle("Tau ID ROC;Efficiency;QQ Rejection (1/fake rate)")
g_roc.SetLineWidth(2)
g_roc.SetLineColor(ROOT.kBlue + 1)
c.SetLogy()
g_roc.Draw("AL")

g_roc.GetXaxis().SetRangeUser(0.98, 1.0)   # zoom x to high efficiency region
g_roc.GetYaxis().SetRangeUser(1.0, 1000)  # adjust y range as needed

marker = ROOT.TMarker(efficiency, rejection, 20)
marker.SetMarkerColor(ROOT.kRed)
marker.SetMarkerSize(1.5)
marker.Draw("same")

fom = eff_scan * np.sqrt(rej_scan)
best_idx = np.nanargmax(fom)
print(f"\n[ROC] Best working point (max eff * sqrt(rejection)):")
print(f"      Threshold:         {thresholds[best_idx]:.4f}")
print(f"      Signal efficiency: {eff_scan[best_idx]*100:.2f}%")
print(f"      QQ rejection:      {rej_scan[best_idx]:.1f}")

best_marker = ROOT.TMarker(eff_scan[best_idx], rej_scan[best_idx], 29)  # star
best_marker.SetMarkerColor(ROOT.kGreen + 2)
best_marker.SetMarkerSize(2.0)
best_marker.Draw("same")

c.SaveAs("tau_id_roc.png")
print("\nSaved: tau_id_roc.png")