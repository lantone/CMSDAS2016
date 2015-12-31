#include "TPaveStats.h"

void plotEff() {
   RooHist* h;
   RooHist* hh;

   TCanvas* c1;

   TCanvas* c;
   TFile f("../../../../../../CMSSW_4_2_6/src/MuonAnalysis/TagAndProbe/test/zmumu/eff0113_L2DiMu30_abseta.root","read");

   gDirectory->Cd("tpTree/L2DiMu30fromTk_TagAny1M/fit_eff_plots");
   char cname[150], outname[150]; 

   sprintf(cname,"pt_PLOT_abseta_bin0_&_pair_drM2_bin0_&_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_HLT_Any1M_pass_&_tag_IsolTk4_pass");
   c1 = (TCanvas*)gROOT->FindObject(cname);
   h = (RooHist*)c1->GetPrimitive("hxy_fit_eff");
   h->GetYaxis()->SetRangeUser(0,1.1);
   h->SetName("Data");
   c1->Clear();

   TFile f2("eff0327_MCFall11_L2DiMu30_abseta.root");
   gDirectory->Cd("tpTree/L2DiMu30fromTk_TagAny1M/fit_eff_plots");
   c = (TCanvas*)gROOT->FindObject("pt_PLOT_abseta_bin0_&_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_IsolTk4_pass_&_tag_Mu20_pass");
   ((RooHist*)c->GetPrimitive("hxy_fit_eff"))->SetMarkerSize(0.8);
   ((RooHist*)c->GetPrimitive("hxy_fit_eff"))->GetYaxis()->SetRangeUser(0,1.1);
   ((RooHist*)c->GetPrimitive("hxy_fit_eff"))->SetName("MC"); 
   gStyle->SetOptStat(0);
   gStyle->SetTitle(0);
   h->SetLineColor(2);
   h->SetMarkerColor(2);
   h->SetMarkerSize(0.8);
   h->Draw("ep");
   h->SetName("Data"); 
   h->SetTitle("Data");
   char ccname[150];
   sprintf(ccname,"DataMC_ID");
   c->SetName(ccname);
   TFile outfile("L2DiMu30_ptPlot.root","update");

   gStyle->SetOptStat(0);
   gStyle->SetTitle("");
   c->SetLogx();
   c->Write();
   char ccname[150];
   sprintf(ccname,"DataMC_ID.gif");
   c->SaveAs(ccname);
   outfile.Close();
}
