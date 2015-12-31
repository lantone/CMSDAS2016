{
  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  gStyle->SetOptStat(0);
  gStyle->SetTitle(0);


  TH2F *h;
  TH2F *hh;
  TFile f("eff0327_MCFall11_L2DiMu30_tagMu20_2d.root");//effMaps_JPsi_MC_Trigger_L2DiMu30fromTk.root");
  f->cd("");
  gDirectory->Cd("tpTree/L2DiMu30fromTk_TagAny1M/fit_eff_plots");
  char cname[150], outname[150];
  sprintf(cname,"pt_abseta_PLOT_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_IsolTk4_pass_&_tag_Mu20_pass");
  TCanvas c1;
  c1 = (TCanvas*)gROOT->FindObject(cname);
  h= (TH2F*)c1->GetPrimitive("pt_abseta_PLOT_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_IsolTk4_pass_&_tag_Mu20_pass");
  cout<<"check"<<endl;   

  TFile f2("eff0424_L2DiMu30_v5v6_2d.root");//effMaps_JPsi_Data_Trigger_L2DiMu30fromTk.root");
  f2->cd("");
  gDirectory->Cd("tpTree/L2DiMu30fromTk_TagAny1M/fit_eff_plots");
  char cname1[150], outname[150];
  sprintf(cname1,"pt_abseta_PLOT_pair_drM2_bin0_&_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_HLT_Any1M_pass_&_tag_IsolTk4_pass");
  TCanvas c2;
  c2 = (TCanvas*)gROOT->FindObject(cname1);
  hh= (TH2F*)c2->GetPrimitive("pt_abseta_PLOT_pair_drM2_bin0_&_IsolTk4_pass_&_Track_HP_pass_&_Track_IP_pass_&_Track_Qual_pass_&_tag_HLT_Any1M_pass_&_tag_IsolTk4_pass");
   

  Double_t ptbins[6]={15,25,33,40,50,70};
  Double_t absetabins[6]={0.0,0.4,0.8,1.2,1.6,2.0};

  TH2F* diff = new TH2F("diff","diff",5,ptbins,5,absetabins);
  TH2F* Rat = diff->Clone("Rat");

  for(Int_t i = 1; i <= h->GetNbinsX();i++){
     for(Int_t j = 1; j <= h->GetNbinsY();j++){
        double Diff = hh->GetBinContent(i,j) - h->GetBinContent(i,j);
	double err = sqrt (hh->GetBinError(i,j)*hh->GetBinError(i,j) + h->GetBinError(i,j) * h->GetBinError(i,j));
	double err_rat = (hh->GetBinError(i,j)*h->GetBinContent(i,j) - hh->GetBinContent(i,j)*h->GetBinError(i,j))/(TMath::Power(h->GetBinContent(i,j),2));
	diff->SetBinContent(i,j,Diff);
	diff->SetBinError(i,j,err);
	double rat = Diff/h->GetBinContent(i,j);
	Rat->SetBinContent(i,j,rat);
	Rat->SetBinError(i,j,err_rat);
     }
  }
  TFile outfile("diff_2D.root","recreate"); 
  h->SetName("hmc");
  hh->SetName("hdata");
  h->Write();
  hh->Write();
  diff->Write();
  Rat->Write();
  outfile.Close();

}

