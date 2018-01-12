#!/bin/python
import ROOT
import copy
import os.path
import CMS_lumi_lep, tdrstyle
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
parser.add_option('--rebin', action='store', type='int',
                      dest='rebin',
                      default = 2,help='Set rebin (ngroup)')

(options, args) = parser.parse_args()

print ""

# CMS Lumi
tdrstyle.setTDRStyle()
CMS_lumi_lep.extraText = "LPC DAS 2018"
CMS_lumi_lep.lumi_sqrtS = "36 fb^{-1} (13 TeV)"
iPos = 11
if( iPos==0 ): CMS_lumi_lep.relPosX = 0.12
iPeriod = 0

# Print lepton channel
chan = True      #electrons
if options.isM :
    chan = False #muons
if options.isE :
    chan = True  #electrons


# Decides Colors based on bkg
def decideColor(filename):
    if "WJets" in filename:
        col = ROOT.kRed
        return col
    if "ttbar" in filename:
        col = ROOT.kBlue
        return col
    if "singletop" in filename:
        col = ROOT.kGreen
        return col
    if "QCD" in filename:
        col = ROOT.kCyan
        return col

directory = "./StackedPngFiles"
if not os.path.exists(directory):
    os.makedirs(directory)

# Dummy hists for legend
col = ROOT.kRed
h_Red = ROOT.TH1F()
h_Red.SetFillColor(col)
h_Red.SetLineColor(col)
t_Red = "W jets"

col = ROOT.kBlue
h_Blue = ROOT.TH1F()
h_Blue.SetFillColor(col)
h_Blue.SetLineColor(col)
t_Blue = "ttbar"

col = ROOT.kGreen
h_Green = ROOT.TH1F()
h_Green.SetFillColor(col)
h_Green.SetLineColor(col)
t_Green = "Single top"

col = ROOT.kCyan
h_Cyan = ROOT.TH1F()
h_Cyan.SetFillColor(col)
h_Cyan.SetLineColor(col)
t_Cyan = "QCD"

#Dictionary with weights
weights = {"ttbar_ALL":"0.387","WJetsToLNu_Wpt-0To50":"20.567","WJetsToLNu_Wpt-50To100":"1.744","WJetsToLNu_Pt-100To250":"0.202","WJetsToLNu_Pt-250To400":"0.071","WJetsToLNu_Pt-400To600":"0.05\
6","WJetsToLNu_Pt-600ToInf":"0.008","singletop_schan":"0.012","singletop_tchan_top":"0.815","singletop_tchan_antitop":"0.740","singletop_tWchan_top":".183","QCD_Pt_300to470_TuneCUETP8M1_13TeV_\
pythia8":"67.664","QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8":"5.876","QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8":"1.722","QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8":".290","QCD_Pt_100\
0to1400_TuneCUETP8M1_13TeV_pythia8":".113","QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8":".076","QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8":".010","QCD_Pt_2400to3200_TuneCUETP8M1_13TeV\
_pythia8":".0006","QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8":".0002"}

#Initializes weight to 1, will stay 1 for signal
weight = 1.0

# Create the THStack
stack_lepPt          = ROOT.THStack("lepPt","")
stack_lepEta         = ROOT.THStack("lepEta","")
stack_lepPhi         = ROOT.THStack("lepPhi","")
stack_AK8Pt          = ROOT.THStack("AK8Pt","")
stack_AK8Eta         = ROOT.THStack("AK8Eta","")
stack_AK8Phi         = ROOT.THStack("AK8Phi","")
stack_AK4Pt          = ROOT.THStack("AK4Pt","")
stack_AK4Eta         = ROOT.THStack("AK4Eta","")
stack_AK4Phi         = ROOT.THStack("AK4Phi","")
stack_AK4M           = ROOT.THStack("AK4M","")
stack_AK4BDisc       = ROOT.THStack("AK4BDisc","")
stack_mttbar         = ROOT.THStack("mttbar","")
stack_AK8Tau32PreSel = ROOT.THStack("AK8Tau32PreSel","")
stack_AK8Tau21PreSel = ROOT.THStack("AK8Tau21PreSel","")
stack_AK4BdiscPreSel = ROOT.THStack("AK4BdiscPreSel","")
stack_mtopHadGroomed = ROOT.THStack("AK8Tau32PreSel","")

# Stack X axis labels
xlabels = [ "lepton Pt [GeV]", "lepton #eta", "lepton #phi", 
            "AK8 Pt [GeV]", "AK8 #eta", "AK8 #phi", 
            "AK4 Pt [GeV]", "AK4 #eta", "AK4 #phi", 
            "AK4 Mass [GeV]", "AK4 Btag discriminator", "mttbar [GeV]",
            "AK8 jet #tau_{32}", "AK8 jet #tau_{21}", "AK4 Btag discriminator",
            "AK8 jet soft-drop mass [GeV]"
          ]

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
    h_AK8Tau32PreSel = file.Get("h_AK8Tau32PreSel"+extra)
    h_AK8Tau21PreSel = file.Get("h_AK8Tau21PreSel"+extra)
    h_AK4BdiscPreSel = file.Get("h_AK4BdiscPreSel"+extra)
    h_mtopHadGroomed = file.Get("h_mtopHadGroomed"+extra)

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
    h_AK8Tau32PreSel.Scale(weight)
    h_AK8Tau21PreSel.Scale(weight)
    h_AK4BdiscPreSel.Scale(weight)
    h_mtopHadGroomed.Scale(weight)

    #Rebin
    h_lepPt.Rebin(options.rebin);
    h_lepEta.Rebin(options.rebin);
    h_lepPhi.Rebin(options.rebin);
    h_AK8Pt.Rebin(options.rebin);
    h_AK8Eta.Rebin(options.rebin);
    h_AK8Phi.Rebin(options.rebin);
    h_AK4Pt.Rebin(options.rebin);
    h_AK4Eta.Rebin(options.rebin);
    h_AK4Phi.Rebin(options.rebin);
    h_AK4M.Rebin(options.rebin);
    h_AK4BDisc.Rebin(options.rebin);
    h_mttbar.Rebin(options.rebin)
    h_AK8Tau32PreSel.Rebin(options.rebin)  
    h_AK8Tau21PreSel.Rebin(options.rebin)  
    h_AK4BdiscPreSel.Rebin(options.rebin)
    h_mtopHadGroomed.Rebin(options.rebin)
 
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
    h_AK8Tau32PreSel.SetFillColor(color)
    h_AK8Tau21PreSel.SetFillColor(color)
    h_AK4BdiscPreSel.SetFillColor(color)
    h_mtopHadGroomed.SetFillColor(color)

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
    h_AK8Tau32PreSel.SetLineColor(color)
    h_AK8Tau21PreSel.SetLineColor(color)
    h_AK4BdiscPreSel.SetLineColor(color)
    h_mtopHadGroomed.SetLineColor(color)

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
    stack_AK8Tau32PreSel.Add(copy.deepcopy(h_AK8Tau32PreSel))
    stack_AK8Tau21PreSel.Add(copy.deepcopy(h_AK8Tau21PreSel))
    stack_AK4BdiscPreSel.Add(copy.deepcopy(h_AK4BdiscPreSel))
    stack_mtopHadGroomed.Add(copy.deepcopy(h_mtopHadGroomed))


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
    h_AK8Tau32PreSeldata= file.Get("h_AK8Tau32PreSel"+extra)
    h_AK8Tau21PreSeldata= file.Get("h_AK8Tau21PreSel"+extra)
    h_AK4BdiscPreSeldata= file.Get("h_AK4BdiscPreSel"+extra)
    h_mtopHadGroomeddata= file.Get("h_mtopHadGroomed"+extra)

    h_lepPtdata.Rebin(options.rebin);
    h_lepEtadata.Rebin(options.rebin);
    h_lepPhidata.Rebin(options.rebin);
    h_AK8Ptdata.Rebin(options.rebin);
    h_AK8Etadata.Rebin(options.rebin);
    h_AK8Phidata.Rebin(options.rebin);
    h_AK4Ptdata.Rebin(options.rebin);
    h_AK4Etadata.Rebin(options.rebin);
    h_AK4Phidata.Rebin(options.rebin);
    h_AK4Mdata.Rebin(options.rebin);
    h_AK4BDiscdata.Rebin(options.rebin);
    h_mttbardata.Rebin(options.rebin)
    h_AK8Tau32PreSeldata.Rebin(options.rebin)
    h_AK8Tau21PreSeldata.Rebin(options.rebin)
    h_AK4BdiscPreSeldata.Rebin(options.rebin)
    h_mtopHadGroomeddata.Rebin(options.rebin)

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
    h_AK8Tau32PreSeldata.SetMarkerStyle(20)
    h_AK8Tau21PreSeldata.SetMarkerStyle(20)
    h_AK4BdiscPreSeldata.SetMarkerStyle(20)
    h_mtopHadGroomeddata.SetMarkerStyle(20)

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
    h_AK8Tau32PreSeldata.SetMarkerColor(color)
    h_AK8Tau21PreSeldata.SetMarkerColor(color)
    h_AK4BdiscPreSeldata.SetMarkerColor(color)
    h_mtopHadGroomeddata.SetMarkerColor(color)

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
    h_AK8Tau32PreSeldata.SetLineColor(color)
    h_AK8Tau21PreSeldata.SetLineColor(color)
    h_AK4BdiscPreSeldata.SetLineColor(color)
    h_mtopHadGroomeddata.SetLineColor(color)

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
    h_AK8Tau32PreSeldata.SetMarkerSize(0.7)
    h_AK8Tau21PreSeldata.SetMarkerSize(0.7)
    h_AK4BdiscPreSeldata.SetMarkerSize(0.7)
    h_mtopHadGroomeddata.SetMarkerSize(0.7)

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
    stack_mttbar,
    stack_AK8Tau32PreSel,
    stack_AK8Tau21PreSel,
    stack_AK4BdiscPreSel,
    stack_mtopHadGroomed
    ]
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
    h_mttbardata,
    h_AK8Tau32PreSeldata,
    h_AK8Tau21PreSeldata,
    h_AK4BdiscPreSeldata,
    h_mtopHadGroomeddata
    ]

cs1 = ROOT.TCanvas("cs1","cs1",400,500)
#pad1 = ROOT.TPad("pad1","pad1",0,0.35,1.0,1.0)
pad1 = ROOT.TPad("pad1","pad1",0,0.30,1.0,1.0)
pad1.SetLeftMargin(0.15)
pad1.SetRightMargin(0.05)
pad1.SetBottomMargin(0.2) #0.12
if options.log :
    pad1.SetLogy();
pad1.Draw()
#pad2 = ROOT.TPad("pad1","pad2",0,0,1.0,0.35)
pad2 = ROOT.TPad("pad1","pad2",0,0,1.0,0.30)
pad2.SetLeftMargin(0.15)
pad2.SetRightMargin(0.05)
pad2.SetBottomMargin(0.12)
pad2.Draw()


# Legend
#leg = ROOT.TLegend(0.79,0.69,0.99,0.99)
leg = ROOT.TLegend(0.15,0.01,0.95,0.1)
leg.SetNColumns(3)
leg.SetBorderSize(0)
leg.AddEntry(h_Red,t_Red,"f")
leg.AddEntry(h_Blue,t_Blue,"f")
leg.AddEntry(h_Green,t_Green,"f")
leg.AddEntry(h_Cyan,t_Cyan,"f")
leg.AddEntry(data_list[0], "Data", "pl")

count = 0
for stack in stack_list:
    #Plot Stacked with Data
    pad1.cd()
    pad1.SetGridy()
    pad1.SetGridx()
    stack.SetMaximum(1.2*stack.GetMaximum())
    stack.Draw("hist")
    stack.GetXaxis().SetNdivisions(305);
    stack.GetXaxis().SetTitle(xlabels[count])
    stack.GetXaxis().SetTitleSize(0.05)
    stack.GetXaxis().SetTitleOffset(0.83)
    stack.GetYaxis().SetTitle("Counts")
    stack.GetYaxis().SetTitleSize(0.055)
    stack.GetYaxis().SetTitleOffset(1.30)
    stack.GetXaxis().SetLabelSize(0.045)
    stack.GetYaxis().SetLabelSize(0.045)
    if options.log :
        stack.SetMinimum(1e-3)
    h_data = copy.deepcopy(data_list[count])
    print data_list[count]
    count += 1
    h_data.Draw("SAMEPE")
    leg.Draw()
    CMS_lumi_lep.CMS_lumi(pad1, iPeriod, iPos, chan)
    cs1.Update()

    #Make and Plot Ratio
    pad2.cd()
    pad2.SetGridy()
    h_ratio = stack.GetHistogram()
    for hist in stack.GetHists():
        h_ratio.Add(hist)
    #h_data.Sumw2()
    #h_ratio.Sumw2()
    h_dataC = h_data.Clone() 
    h_dataC.Divide(h_dataC, h_ratio, 1, 1, "B")
    h_dataC.SetStats(ROOT.kFALSE)
    h_dataC.GetYaxis().SetRangeUser(0,2)
    h_dataC.GetXaxis().SetTitle("");
    h_dataC.GetXaxis().SetNdivisions(305);
    h_dataC.GetYaxis().SetTitle("Ratio");
    h_dataC.GetYaxis().SetTitleSize(0.105);
    h_dataC.GetYaxis().SetTitleOffset(0.68);
    h_dataC.GetYaxis().SetLabelOffset(0.02);
    h_dataC.GetXaxis().SetLabelSize(0.09);
    h_dataC.GetYaxis().SetLabelSize(0.09);
    h_dataC.Draw("PE")
 
    xmin = h_dataC.GetBinLowEdge(1)
    xmax = h_dataC.GetBinLowEdge(h_dataC.GetNbinsX())+h_dataC.GetBinWidth(h_dataC.GetNbinsX())
    line = ROOT.TLine(xmin,1,xmax,1)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("SAME")

    cs1.Update()
    cs1.Write(str(stack));

    # save png file
    first = (str(stack).find("\""))+1
    second = str(stack).find("\"",first)
    savename = str(stack)[first:second]
    spec = "_el"
    if options.isM :
        spec = "_mu"
    if options.log :
        spec += "_log"
    else :
        spec += "_linear"
    savename += spec
    cs1.SaveAs(directory+"/"+savename+".png")
    cs1.SaveAs(directory+"/"+savename+".root")


file.Close();
