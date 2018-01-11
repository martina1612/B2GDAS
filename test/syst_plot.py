import os
import ROOT
from ROOT import *

path = 'root_files'
path = '/eos/uscms/store/user/anovak/CMSDAS'

all_f = os.listdir(path)
names = []
for name in all_f:
    if name.endswith('_mu_jer_down.root'):
        names.append(name[:-len('_mu_jer_down.root')])

for name in names[1:2]:
    systs = ["_jer", "_jer", "_sf"]
    for lep in ["_mu", "_el"]:
        for sys in systs:
            File = ROOT.TFile(path+'/'+name+lep+'.root')
            hist = File.Get("h_mttbar"+lep)
            File_u = ROOT.TFile(path+'/'+name+lep+sys+'_up.root')
            hist_u = File_u.Get('h_mttbar'+lep+sys+'_Up')
            File_d = ROOT.TFile(path+'/'+name+lep+sys+'_down.root')
            hist_d = File_d.Get('h_mttbar'+lep+sys+'_Down')

            hist.SetLineColor(kBlack)
            hist_u.SetLineColor(kRed)
            hist_u.SetLineStyle(3)
            hist_d.SetLineColor(kBlue)
            hist_d.SetLineStyle(3)

            hist.SetStats(0)

            C = TCanvas("test", "", 800,600)
            C.cd()
            hist.Draw("hist c")
            hist_u.Draw("hist same c")
            hist_d.Draw("hist same c")
            C.SaveAs("syst"+name+".png")