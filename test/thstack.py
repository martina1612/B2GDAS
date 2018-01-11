#!/bin/python
import ROOT
import copy
import os.path
from optparse import OptionParser
# Taken from https://root.cern.ch/doc/v608/classTHStack.html
# Converted to python just for you!

#This is where we build our command line options
parser = OptionParser()
parser.add_option('--isE', action='store_true',
                      dest='isE',
                      default = False,help='Selects Electrons')
parser.add_option('--isM', action='store_true',
                      dest='isM',
                      default = False,help='Selects Muons')
parser.add_option('--log', action='store_true',
                      dest='log',
                      default = False,help='Set log Y')

(options, args) = parser.parse_args()

print ""

#Decides Colors based on bkg
def decideColor(filename):
    if "WJets" in filename:
        return ROOT.kRed
    if "ttbar" in filename:
        return ROOT.kBlue
    if "singletop" in filename:
        return ROOT.kGreen
    if "QCD" in filename:
        return ROOT.kCyan

#Dictionary with weights
weights = {"ttbar_ALL":"0.387","WJetsToLNu_Wpt-0To50":"20.567","WJetsToLNu_Wpt-50To100":"1.744","WJetsToLNu_Pt-100To250":"0.202","WJetsToLNu_Pt-250To400":"0.071","WJetsToLNu_Pt-400To600":"0.05\
6","WJetsToLNu_Pt-600ToInf":"0.008","singletop_schan":"0.012","singletop_tchan_top":"0.815","singletop_tchan_antitop":"0.740","singletop_tWchan_top":".183","QCD_Pt_300to470_TuneCUETP8M1_13TeV_\
pythia8":"67.664","QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8":"5.876","QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8":"1.722","QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8":".290","QCD_Pt_100\
0to1400_TuneCUETP8M1_13TeV_pythia8":".113","QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8":".076","QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8":".010","QCD_Pt_2400to3200_TuneCUETP8M1_13TeV\
_pythia8":".0006","QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8":".0002"}

#Initializes weight to 1, will stay 1 for signal
weight = 1.0

# Create the THStack
stack_lepPt = ROOT.THStack("lepPt","lepPt");
stack_lepEta = ROOT.THStack("lepEta","lepEta");
stack_lepPhi = ROOT.THStack("lepPhi","lepPhi");
stack_AK8Pt = ROOT.THStack("AK8Pt","AK8Pt");
stack_AK8Eta = ROOT.THStack("AK8Eta","AK8Eta");
stack_AK8Phi = ROOT.THStack("AK8Phi","AK8Phi");
stack_AK4Pt = ROOT.THStack("AK4Pt","AK4Pt");
stack_AK4Eta = ROOT.THStack("AK4Eta","AK4Eta");
stack_AK4Phi = ROOT.THStack("AK4Phi","AK4Phi");
stack_AK4M = ROOT.THStack("AK4M","AK4M");
stack_AK4BDisc = ROOT.THStack("AK4BDisc","AK4BDisc");
stack_mttbar = ROOT.THStack("mttbar","mttbar")

#Define the data histograms
h_lepPtdata   = ROOT.TH1F()
h_lepEtadata  = ROOT.TH1F()
h_lepPhidata  = ROOT.TH1F()
h_AK8Ptdata   = ROOT.TH1F()
h_AK8Etadata  = ROOT.TH1F()
h_AK8Phidata  = ROOT.TH1F()
h_AK4Ptdata   = ROOT.TH1F()
h_AK4Etadata  = ROOT.TH1F()
h_AK4Phidata  = ROOT.TH1F()
h_AK4Mdata    = ROOT.TH1F()
h_AK4BDiscdata = ROOT.TH1F() 
h_mttbardata = ROOT.TH1F()

# Bkg Input files
filelistbkg = [
"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_plots_el.root",
"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"WJetsToLNu_Pt-100To250_plots_el.root",
"WJetsToLNu_Pt-100To250_plots_mu.root",
"WJetsToLNu_Pt-250To400_plots_el.root",
"WJetsToLNu_Pt-250To400_plots_mu.root",
"WJetsToLNu_Pt-400To600_plots_el.root",
"WJetsToLNu_Pt-400To600_plots_mu.root",
"WJetsToLNu_Pt-600ToInf_plots_el.root",
"WJetsToLNu_Pt-600ToInf_plots_mu.root",
"WJetsToLNu_Wpt-0To50_plots_el.root",
"WJetsToLNu_Wpt-0To50_plots_mu.root",
"WJetsToLNu_Wpt-50To100_plots_el.root",
"WJetsToLNu_Wpt-50To100_plots_mu.root",
"singletop_schan_plots_el.root",
"singletop_schan_plots_mu.root",
"singletop_tWchan_antitop_plots_el.root",
"singletop_tWchan_antitop_plots_mu.root",
"singletop_tWchan_top_plots_el.root",
"singletop_tWchan_top_plots_mu.root",
"singletop_tchan_antitop_plots_el.root",
"singletop_tchan_antitop_plots_mu.root",
"singletop_tchan_top_plots_el.root",
"singletop_tchan_top_plots_mu.root",
"ttbar_ALL_plots_el.root",
"ttbar_ALL_plots_mu.root"]

#Where we decide if we want elections and Muons
findMe = "_el"
if options.isE:
    findMe = "_el"
    extra  = "_el"#yes,this is redundant. 
elif options.isM:
    findMe = "_mu"
    extra  = "_mu"

#Just to work with the list
i=0;
for inp in filelistbkg:
    filelistbkg[i] = "root://cmseos.fnal.gov//store/user/anovak/CMSDAS/"+inp
    i += 1

#Define the name of our saved file
outname = "stacked_plots"+findMe

skippedCount = 0

# Filling with bkg hists
for filename  in filelistbkg:
    if findMe in filename:
        tag = filename[filename.rfind("/")+1:filename.rfind("_plots")]
        if tag in weights:
            weight = float(weights[tag])
    else:
        continue

#    if not (os.path.isfile(filename)) :
#        print "!!! ERROR !!! %s does not exist. Skipping file." % filename
#        skippedCount += 1
#        continue
#    if ( os.path.getsize(filename) == 0 ) :
#        print "!!! ERROR !!! %s has size 0. Skipping file." % filename
#        skippedCount += 1
#        continue

    print "Reading %s" % filename
    color = decideColor(filename)
    file = ROOT.TFile.Open(filename);
    # Reading hists from file
    h_lepPt   = file.Get("h_lepPt"+extra);
    h_lepEta  = file.Get("h_lepEta"+extra);
    h_lepPhi  = file.Get("h_lepPhi"+extra);
    h_AK8Pt   = file.Get("h_AK8Pt"+extra);
    h_AK8Eta  = file.Get("h_AK8Eta"+extra);
    h_AK8Phi  = file.Get("h_AK8Phi"+extra);
    h_AK4Pt   = file.Get("h_AK4Pt"+extra);
    h_AK4Eta  = file.Get("h_AK4Eta"+extra);
    h_AK4Phi  = file.Get("h_AK4Phi"+extra);
    h_AK4M    = file.Get("h_AK4M"+extra);
    h_AK4BDisc = file.Get("h_AK4Bdisc"+extra);
    h_mttbar   = file.Get("h_mttbar"+extra)

    #Scale
    h_lepPt.Scale(weight);
    h_lepEta.Scale(weight);
    h_lepPhi.Scale(weight);
    h_AK8Pt.Scale(weight);
    h_AK8Eta.Scale(weight);
    h_AK8Phi.Scale(weight);
    h_AK4Pt.Scale(weight);
    h_AK4Eta.Scale(weight);
    h_AK4Phi.Scale(weight);
    h_AK4M.Scale(weight);
    h_AK4BDisc.Scale(weight);
    h_mttbar.Scale(weight)

    # Set color for this process
    h_lepPt.SetFillColor(color);
    h_lepEta.SetFillColor(color);
    h_lepPhi.SetFillColor(color);
    h_AK8Pt.SetFillColor(color);
    h_AK8Eta.SetFillColor(color);
    h_AK8Phi.SetFillColor(color);
    h_AK4Pt.SetFillColor(color);
    h_AK4Eta.SetFillColor(color);
    h_AK4Phi.SetFillColor(color);
    h_AK4M.SetFillColor(color);
    h_AK4BDisc.SetFillColor(color);
    h_mttbar.SetFillColor(color)

    h_lepPt.SetLineColor(color);
    h_lepEta.SetLineColor(color);
    h_lepPhi.SetLineColor(color);
    h_AK8Pt.SetLineColor(color);
    h_AK8Eta.SetLineColor(color);
    h_AK8Phi.SetLineColor(color);
    h_AK4Pt.SetLineColor(color);
    h_AK4Eta.SetLineColor(color);
    h_AK4Phi.SetLineColor(color);
    h_AK4M.SetLineColor(color);
    h_AK4BDisc.SetLineColor(color);
    h_mttbar.SetLineColor(color)

    # Filling stacks
    stack_lepPt.Add(copy.deepcopy(h_lepPt));
    stack_lepEta.Add(copy.deepcopy(h_lepEta));
    stack_lepPhi.Add(copy.deepcopy(h_lepPhi));
    stack_AK8Pt.Add(copy.deepcopy(h_AK8Pt));
    stack_AK8Eta.Add(copy.deepcopy(h_AK8Eta));
    stack_AK8Phi.Add(copy.deepcopy(h_AK8Phi));
    stack_AK4Pt.Add(copy.deepcopy(h_AK4Pt));
    stack_AK4Eta.Add(copy.deepcopy(h_AK4Eta));
    stack_AK4Phi.Add(copy.deepcopy(h_AK4Phi));
    stack_AK4M.Add(copy.deepcopy(h_AK4M));
    stack_AK4BDisc.Add(copy.deepcopy(h_AK4BDisc));
    stack_mttbar.Add(copy.deepcopy(h_mttbar))

print "\n%d background file(s) skipped.\n" % skippedCount

# Filling with Data graphs
if options.isE :
    filelistdata = ["root://cmseos.fnal.gov//store/user/anovak/CMSDAS/SingleElectron_2016_All_plots_el.root"]
if options.isM :
    filelistdata = ["root://cmseos.fnal.gov//store/user/anovak/CMSDAS/singleMuon_ALL_plots_mu.root"]
else :
    filelistdata = ["root://cmseos.fnal.gov//store/user/anovak/CMSDAS/SingleElectron_2016_All_plots_el.root"]

for filename  in filelistdata:
    print "Using Data file: %s.\n" % filename
    if findMe in filename:
        tag = filename.replace("_plots_"+findMe+".root","")
    else:
        continue
    color = ROOT.kBlack;
    file = ROOT.TFile.Open(filename);
    # Reading hists from file
    print "h_lepPt"+extra
    h_lepPtdata   = file.Get("h_lepPt"+extra);
    h_lepEtadata  = file.Get("h_lepEta"+extra);
    h_lepPhidata  = file.Get("h_lepPhi"+extra);
    h_AK8Ptdata   = file.Get("h_AK8Pt"+extra);
    h_AK8Etadata  = file.Get("h_AK8Eta"+extra);
    h_AK8Phidata  = file.Get("h_AK8Phi"+extra);
    h_AK4Ptdata   = file.Get("h_AK4Pt"+extra);
    h_AK4Etadata  = file.Get("h_AK4Eta"+extra);
    h_AK4Phidata  = file.Get("h_AK4Phi"+extra);
    h_AK4Mdata    = file.Get("h_AK4M"+extra);
    h_AK4BDiscdata = file.Get("h_AK4Bdisc"+extra);
    h_mttbardata = file.Get("h_mttbar"+extra)

    h_lepPtdata.SetMarkerStyle(20);
    h_lepEtadata.SetMarkerStyle(20);
    h_lepPhidata.SetMarkerStyle(20);
    h_AK8Ptdata.SetMarkerStyle(20);
    h_AK8Etadata.SetMarkerStyle(20);
    h_AK8Phidata.SetMarkerStyle(20);
    h_AK4Ptdata.SetMarkerStyle(20);
    h_AK4Etadata.SetMarkerStyle(20);
    h_AK4Phidata.SetMarkerStyle(20);
    h_AK4Mdata.SetMarkerStyle(20);
    h_AK4BDiscdata.SetMarkerStyle(20);
    h_mttbardata.SetMarkerStyle(20)

    # Set color for this process
    h_lepPtdata.SetMarkerColor(color);
    h_lepEtadata.SetMarkerColor(color);
    h_lepPhidata.SetMarkerColor(color);
    h_AK8Ptdata.SetMarkerColor(color);
    h_AK8Etadata.SetMarkerColor(color);
    h_AK8Phidata.SetMarkerColor(color);
    h_AK4Ptdata.SetMarkerColor(color);
    h_AK4Etadata.SetMarkerColor(color);
    h_AK4Phidata.SetMarkerColor(color);
    h_AK4Mdata.SetMarkerColor(color);
    h_AK4BDiscdata.SetMarkerColor(color);
    h_mttbardata.SetMarkerColor(color)

    h_lepPtdata.SetLineColor(color);
    h_lepEtadata.SetLineColor(color);
    h_lepPhidata.SetLineColor(color);
    h_AK8Ptdata.SetLineColor(color);
    h_AK8Etadata.SetLineColor(color);
    h_AK8Phidata.SetLineColor(color);
    h_AK4Ptdata.SetLineColor(color);
    h_AK4Etadata.SetLineColor(color);
    h_AK4Phidata.SetLineColor(color);
    h_AK4Mdata.SetLineColor(color);
    h_AK4BDiscdata.SetLineColor(color);
    h_mttbardata.SetLineColor(color)

    h_lepPtdata.SetMarkerSize(0.7);
    h_lepEtadata.SetMarkerSize(0.7);
    h_lepPhidata.SetMarkerSize(0.7);
    h_AK8Ptdata.SetMarkerSize(0.7);
    h_AK8Etadata.SetMarkerSize(0.7);
    h_AK8Phidata.SetMarkerSize(0.7);
    h_AK4Ptdata.SetMarkerSize(0.7);
    h_AK4Etadata.SetMarkerSize(0.7);
    h_AK4Phidata.SetMarkerSize(0.7);
    h_AK4Mdata.SetMarkerSize(0.7);
    h_AK4BDiscdata.SetMarkerSize(0.7);
    h_mttbardata.SetMarkerSize(0.7)

# Output file
outfilename = outname+"_ratio.root"
outfile = ROOT.TFile(outfilename, "RECREATE");

#Plotting and Ratio Plot
#Define Canvases and Pads
stack_list = [stack_lepPt,
    stack_lepEta,
    stack_lepPhi,
    stack_AK8Pt,
    stack_AK8Eta,
    stack_AK8Phi,
    stack_AK4Pt,
    stack_AK4Eta,
    stack_AK4Phi,
    stack_AK4M,
    stack_AK4BDisc,
    stack_mttbar]
data_list  = [h_lepPtdata,
    h_lepEtadata,
    h_lepPhidata,
    h_AK8Ptdata,
    h_AK8Etadata,
    h_AK8Phidata,
    h_AK4Ptdata,
    h_AK4Etadata,
    h_AK4Phidata,
    h_AK4Mdata,
    h_AK4BDiscdata,
    h_mttbardata]

cs1 = ROOT.TCanvas("cs1","cs1",400,500)
pad1 = ROOT.TPad("pad1","pad1",0,0.35,1.0,1.0)
if options.log :
    pad1.SetLogy();
pad1.Draw()
pad2 = ROOT.TPad("pad1","pad2",0,0,1.0,0.35)
pad2.Draw()

count = 0
for stack in stack_list:
    #Plot Stacked with Data
    pad1.cd()
    stack.Draw("hist")
    h_data = copy.deepcopy(data_list[count])
    print data_list[count]
    count += 1
    h_data.Draw("SAMEPE")
    cs1.Update()

    #Make and Plot Ratio
    pad2.cd()
    h_ratio = stack.GetHistogram()
    for hist in stack.GetHists():
        h_ratio.Add(hist)
    #h_data.Sumw2()
    #h_ratio.Sumw2()
    h_dataC = h_data.Clone() 
    h_dataC.Divide(h_dataC, h_ratio, 1, 1, "B")
    h_dataC.SetStats(ROOT.kFALSE)
    h_dataC.Draw("PE")
    cs1.Update()
    cs1.Write(str(stack));

file.Close();
