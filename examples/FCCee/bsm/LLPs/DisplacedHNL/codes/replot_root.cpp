/// plots root histograms from trees
/// root -l EleTrack.C
#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <TH1.h>
#include <TLatex.h>
#include "TSystem.h"
#include "TMath.h"

using namespace std;
 
void replot_root(){

/////input files
TFile *f1 = TFile::Open("/eos/user/s/sgiappic/2HNL_ana/final/HNL_2.86e-12_30gev_sel2Reco_vetoes.root");
TH1 *h1 = new TH1F("", "", 100, 0, 2000);
TTree *tree1 = dynamic_cast<TTree*>(f1->Get("events;1"));
tree1->Draw("Reco_Lxyz>>h1");

TFile *f2 = TFile::Open("/eos/user/s/sgiappic/2HNL_ana/final/HNL_2.86e-7_30gev_sel2Reco_vetoes.root");
TH1 *h2 = new TH1F("", "", 100, 0, 2000);
TTree *tree2 = dynamic_cast<TTree*>(f2->Get("events;1"));
tree2->Draw("Reco_Lxyz>>h2");

TFile *f3 = TFile::Open("/eos/user/s/sgiappic/2HNL_ana/final/HNL_6.67e-8_60gev_sel2Reco_vetoes.root");
TH1 *h3 = new TH1F("", "", 100, 0, 2000);
TTree *tree3 = dynamic_cast<TTree*>(f3->Get("events;1"));
tree3->Draw("Reco_Lxyz>>h3");

TFile *f4 = TFile::Open("/eos/user/s/sgiappic/2HNL_ana/final/HNL_2.86e-8_80gev_sel2Reco_vetoes.root");
TH1 *h4 = new TH1F("", "", 100, 0, 2000);
TTree *tree4 = dynamic_cast<TTree*>(f4->Get("events;1"));
tree4->Draw("Reco_Lxyz>>h4");

TCanvas* canvas = new TCanvas("", "", 800, 800);

h1->SetLineColor(kRed-4); //blue
h1->SetLineWidth(3);
h1->SetStats(kFALSE);
h1->Scale(1e10);
h1->Draw("HIST");

h2->SetLineColor(kPink-4); //red
h2->SetLineWidth(3);
h2->SetStats(kFALSE);
h2->Scale(1e10);
h2->Draw("HIST SAME");

h3->SetLineColor(kViolet); //red
h3->SetLineWidth(3);
h3->SetStats(kFALSE);
h3->Scale(1e10);
h3->Draw("HIST SAME");

h4->SetLineColor(kAzure-2);
h4->SetLineWidth(3);
h4->SetStats(kFALSE);
h4->Scale(1e10);
h4->Draw("HIST SAME");

h1->GetYaxis()->SetTitle("Events");
h1->GetXaxis()->SetTitle("Reco HNL L_{xyz} [mm]");
h1->GetYaxis()->SetRangeUser(1e-6,1e15);
//h1->GetYaxis()->SetTitleOffset(1.5);
h1->GetXaxis()->SetTitleOffset(1.2);
//h1->GetXaxis()->SetLimits(1, 1000);

// draw text around the canvas and then the proper legend
TLatex latex;
latex.SetNDC();
latex.SetTextSize(0.03);
latex.DrawLatex(0.18, 0.84, "#bf{#it{#sqrt{s} = 91 GeV, L = 180 ab^{-1}}}");
latex.DrawLatex(0.18, 0.80, "#bf{#it{e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu}}");
latex.SetTextSize(0.02);
latex.DrawLatex(0.18, 0.76, "#bf{#it{Two leptons, no photons, no jets}}");

latex.SetTextAlign(31);
latex.SetTextSize(0.03);
latex.DrawLatex(0.92, 0.92, "#it{FCCAnalyses: FCC-ee Simulation (Delphes)}");

auto legend = new TLegend(0.16, 0.72 - 4*0.04, 0.45, 0.74);
legend->SetBorderSize(0);
legend->SetShadowColor(0);
legend->SetFillColor(0);
//legend->SetNColumns(2);
//legend->SetHeader("Same flavour", "C"); // option "C" allows to center the header
legend->AddEntry(h1, "M_{N}=30 GeV, U^{2}=2.86e-12", "l"); 
legend->AddEntry(h2, "M_{N}=30 GeV, U^{2}=2.86e-7", "l");
legend->AddEntry(h3, "M_{N}=60 GeV, U^{2}=6.67e-8", "l"); 
legend->AddEntry(h4, "M_{N}=80 GeV, U^{2}=2.86e-8", "l");
legend->SetTextSize(0.025);
legend->SetTextFont(42);
legend->Draw();

canvas->SetLogy();
canvas->SetLogx();
canvas->SetTicks(1, 1);
canvas->SetLeftMargin(0.14);
canvas->SetRightMargin(0.08);
canvas->GetFrame()->SetBorderSize(12);

canvas->Print("/eos/user/s/sgiappic/2HNL_ana/plots/Reco_Lxyz.png", "png");
canvas->Print("/eos/user/s/sgiappic/2HNL_ana/plots/Reco_Lxyz.pdf", "pdf");

return;
}