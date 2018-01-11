#!/bin/python
import ROOT
import copy
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
#parser.add_option('--sig', action='store', dest='sig', type='int' ,
#		      default = '0', help='Integer selects signal sample to plot')

(options, args) = parser.parse_args()

#sig = options.sig

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
weights = {"ttbar_ALL":"3.87","WJetsToLNu_Wpt-0To50":"205.67","WJetsToLNu_Wpt-50To100":"17.44","WJetsToLNu_Pt-100To250":"2.02","WJetsToLNu_Pt-250To400":"0.71","WJetsToLNu_Pt-400To600":"0.5\
6","WJetsToLNu_Pt-600ToInf":"0.08","singletop_schan":"0.12","singletop_tchan_top":"8.15","singletop_tchan_antitop":"7.40","singletop_tWchan_top":"1.83","QCD_Pt_300to470_TuneCUETP8M1_13TeV_\
pythia8":"676.64","QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8":"58.76","QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8":"17.22","QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8":"2.90","QCD_Pt_100\
0to1400_TuneCUETP8M1_13TeV_pythia8":"1.13","QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8":"0.76","QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8":"0.10","QCD_Pt_2400to3200_TuneCUETP8M1_13TeV\
_pythia8":"0.006","QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8":"0.002"}

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

#if sig >= len(filelistdata) :
#    print "--sig not valid. Choose one from 0 to %d." % (len(filelistdata)-1)
#    exit()
#else :
#    filelistdata = [ filelistdata[sig] ]

# Bkg Input files
filelistbkg = [
"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_plots_ele.root",
"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_plots_mu.root",
"WJetsToLNu_Pt-100To250_plots_ele.root",
"WJetsToLNu_Pt-100To250_plots_mu.root",
"WJetsToLNu_Pt-250To400_plots_ele.root",
"WJetsToLNu_Pt-250To400_plots_mu.root",
"WJetsToLNu_Pt-400To600_plots_ele.root",
"WJetsToLNu_Pt-400To600_plots_mu.root",
"WJetsToLNu_Pt-600ToInf_plots_ele.root",
"WJetsToLNu_Pt-600ToInf_plots_mu.root",
"WJetsToLNu_Wpt-0To50_plots_ele.root",
"WJetsToLNu_Wpt-0To50_plots_mu.root",
"WJetsToLNu_Wpt-50To100_plots_ele.root",
"WJetsToLNu_Wpt-50To100_plots_mu.root",
"singletop_schan_plots_ele.root",
"singletop_schan_plots_mu.root",
"singletop_tWchan_antitop_plots_ele.root",
"singletop_tWchan_antitop_plots_mu.root",
"singletop_tWchan_top_plots_ele.root",
"singletop_tWchan_top_plots_mu.root",
"singletop_tchan_antitop_plots_ele.root",
"singletop_tchan_antitop_plots_mu.root",
"singletop_tchan_top_plots_ele.root",
"singletop_tchan_top_plots_mu.root",
"ttbar_ALL_plots_ele.root",
"ttbar_ALL_plots_mu.root"]

#Where we decide if we want elections and Muons
findMe = "_ele"
if options.isE:
    findMe = "_ele"
elif options.isM:
    findMe = "_mu"
    
#Just to work with the list
i=0;
for inp in filelistbkg:
    filelistbkg[i] = "inputfolder/CMSDAS/"+inp
    i += 1


outname = "stacked_plots"+findMe

# Filling with bkg hists
for filename  in filelistbkg:
    if findMe in filename:
        tag = filename.replace("_plots_"+findMe+".root","")
        if tag in weights:
            weight = float(weights[tag])
    else:
        continue
    color = decideColor(filename)
#    print color
    file = ROOT.TFile(filename);
#    print filename
    # Reading hists from file
    h_lepPt   = file.Get("h_lepPt");
    h_lepEta  = file.Get("h_lepEta");
    h_lepPhi  = file.Get("h_lepPhi");
    h_AK8Pt   = file.Get("h_AK8Pt");
    h_AK8Eta  = file.Get("h_AK8Eta");
    h_AK8Phi  = file.Get("h_AK8Phi");
    h_AK4Pt   = file.Get("h_AK4Pt");
    h_AK4Eta  = file.Get("h_AK4Eta");
    h_AK4Phi  = file.Get("h_AK4Phi");
    h_AK4M    = file.Get("h_AK4M");
    h_AK4BDisc = file.Get("h_AK4Bdisc");

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



# Create a canvas to print to
cs1 = ROOT.TCanvas("cs1","cs1",10,10,700,900);
T = ROOT.TText();
T.SetTextFont(42);
T.SetTextAlign(21);
cs1.Divide(2,2);

cs2 = ROOT.TCanvas("cs2","cs2",10,10,700,900);
T = ROOT.TText();
T.SetTextFont(42);
T.SetTextAlign(21);
cs2.Divide(2,2);

cs3 = ROOT.TCanvas("cs3","cs3",10,10,700,900);
T = ROOT.TText();
T.SetTextFont(42);
T.SetTextAlign(21);
cs3.Divide(2,2);


# Select each canvas, draw bkg stacks
cs1.cd(1);
stack_lepPt.Draw();
cs1.cd(2);
stack_lepEta.Draw();
cs1.cd(3);
stack_lepPhi.Draw();
cs1.cd(4);
stack_AK8Pt.Draw();

cs2.cd(1);
stack_AK8Eta.Draw();
cs2.cd(2);
stack_AK8Phi.Draw();
cs2.cd(3);
stack_AK4Pt.Draw();
cs2.cd(4);
stack_AK4Eta.Draw();

cs3.cd(1);
stack_AK4Phi.Draw();
cs3.cd(2);
stack_AK4M.Draw();
cs3.cd(3);
stack_AK4BDisc.Draw();

#T.DrawTextNDC(.5,.95,"Default drawing option"); # use the default option
#
#cs.cd(2);
#stack.Draw("nostack");
#T.DrawTextNDC(.5,.95,"Option \"nostack\""); # use the "no stack" option
#
#cs.cd(3);
#stack.Draw("nostackb");
#T.DrawTextNDC(.5,.95,"Option \"nostackb\""); # use the no stack + bar chart option
#
#cs.cd(4);
#stack.Draw("lego1");
#T.DrawTextNDC(.5,.95,"Option \"lego1\""); # use the "lego" plot option (just for fun)


# Filling with Signal graphs
if options.isE :
    filelistdata = ["inputfolder/CMSDAS/SingleElectron_2016_All_plots_ele.root"]
if options.isM :
    filelistdata = ["inputfolder/CMSDAS/SingleElectron_2016_All_plots_mu.root"]

for filename  in filelistdata:
    print filename
    if findMe in filename:
        tag = filename.replace("_plots_"+findMe+".root","")
    else:
        continue
    color = ROOT.kBlack;
#    print color
    file = ROOT.TFile(filename);
#    print filename
    # Reading hists from file
    h_lepPt   = file.Get("h_lepPt");
    h_lepEta  = file.Get("h_lepEta");
    h_lepPhi  = file.Get("h_lepPhi");
    h_AK8Pt   = file.Get("h_AK8Pt");
    h_AK8Eta  = file.Get("h_AK8Eta");
    h_AK8Phi  = file.Get("h_AK8Phi");
    h_AK4Pt   = file.Get("h_AK4Pt");
    h_AK4Eta  = file.Get("h_AK4Eta");
    h_AK4Phi  = file.Get("h_AK4Phi");
    h_AK4M    = file.Get("h_AK4M");
    h_AK4BDisc = file.Get("h_AK4Bdisc");

    h_lepPt.SetMarkerStyle(20);
    h_lepEta.SetMarkerStyle(20);
    h_lepPhi.SetMarkerStyle(20);
    h_AK8Pt.SetMarkerStyle(20);
    h_AK8Eta.SetMarkerStyle(20);
    h_AK8Phi.SetMarkerStyle(20);
    h_AK4Pt.SetMarkerStyle(20);
    h_AK4Eta.SetMarkerStyle(20);
    h_AK4Phi.SetMarkerStyle(20);
    h_AK4M.SetMarkerStyle(20);
    h_AK4BDisc.SetMarkerStyle(20);

    # Set color for this process
    h_lepPt.SetMarkerColor(color);
    h_lepEta.SetMarkerColor(color);
    h_lepPhi.SetMarkerColor(color);
    h_AK8Pt.SetMarkerColor(color);
    h_AK8Eta.SetMarkerColor(color);
    h_AK8Phi.SetMarkerColor(color);
    h_AK4Pt.SetMarkerColor(color);
    h_AK4Eta.SetMarkerColor(color);
    h_AK4Phi.SetMarkerColor(color);
    h_AK4M.SetMarkerColor(color);
    h_AK4BDisc.SetMarkerColor(color);

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

    h_lepPt.SetMarkerSize(0.7);
    h_lepEta.SetMarkerSize(0.7);
    h_lepPhi.SetMarkerSize(0.7);
    h_AK8Pt.SetMarkerSize(0.7);
    h_AK8Eta.SetMarkerSize(0.7);
    h_AK8Phi.SetMarkerSize(0.7);
    h_AK4Pt.SetMarkerSize(0.7);
    h_AK4Eta.SetMarkerSize(0.7);
    h_AK4Phi.SetMarkerSize(0.7);
    h_AK4M.SetMarkerSize(0.7);
    h_AK4BDisc.SetMarkerSize(0.7);

    # Filling stacks
#    stack_lepPt.Add(copy.deepcopy(h_lepPt));
#    stack_lepEta.Add(copy.deepcopy(h_lepEta));
#    stack_lepPhi.Add(copy.deepcopy(h_lepPhi));
#    stack_AK8Pt.Add(copy.deepcopy(h_AK8Pt));
#    stack_AK8Eta.Add(copy.deepcopy(h_AK8Eta));
#    stack_AK8Phi.Add(copy.deepcopy(h_AK8Phi));
#    stack_AK4Pt.Add(copy.deepcopy(h_AK4Pt));
#    stack_AK4Eta.Add(copy.deepcopy(h_AK4Eta));
#    stack_AK4Phi.Add(copy.deepcopy(h_AK4Phi));
#    stack_AK4M.Add(copy.deepcopy(h_AK4M));
#    stack_AK4BDisc.Add(copy.deepcopy(h_AK4BDisc));

    cs1.cd(1);
    h_lepPt.Draw("PESAME");
    cs1.cd(2);
    h_lepEta.Draw("SAMEPE");
    cs1.cd(3);
    h_lepPhi.Draw("SAMEPE");
    cs1.cd(4);
    h_AK8Pt.Draw("SAMEPE");
    
    cs2.cd(1);
    h_AK8Eta.Draw("SAMEPE");
    cs2.cd(2);
    h_AK8Phi.Draw("SAMEPE");
    cs2.cd(3);
    h_AK4Pt.Draw("SAMEPE");
    cs2.cd(4);
    h_AK4Eta.Draw("SAMEPE");
    
    cs3.cd(1);
    h_AK4Phi.Draw("SAMEPE");
    cs3.cd(2);
    h_AK4M.Draw("SAMEPE");
    cs3.cd(3);
    h_AK4BDisc.Draw("SAMEPE");
    
# Output file
outfilename = outname+"_stacked.root"
outfile = ROOT.TFile(outfilename, "RECREATE");

# Save stacks to output file
#outfile.Write(stack_lepPt);
#outfile.Write(stack_lepEta);
#outfile.Write(stack_lepPhi);
#outfile.Write(stack_AK8Pt);
#outfile.Write(stack_AK8Eta);
#outfile.Write(stack_AK8Phi);
#outfile.Write(stack_AK4Pt);
#outfile.Write(stack_AK4Eta);
#outfile.Write(stack_AK4Phi);
#outfile.Write(stack_AK4M);
#outfile.Write(stack_AK4BDisc);

#stack_AK4BDisc.Write();
cs1.Write();
cs2.Write();
cs3.Write();
file.Close();
