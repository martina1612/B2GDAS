#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import array as array
from plot_mttbar import plot_mttbar
import subprocess
import errno
import os

# Dictionaries
signal = {
	'rsg' : [],
}
background = {
	'QCD' : [],
	'WJets' : [],
	'ttbar' : [],
	'singletop' : []
}
data = {
	'singleMuon' : [],
	'SingleElectron' : [],
	}

ttbar = {
	'ttbar' : []
}

run_all = {
	'QCD' : [],
	'singleMuon' : [],
	'SingleElectron' : [],
	'WJets' : [],
	'rsg' : [],
	'ttbar' : [],
	'singletop' : []
}
outnames = {
	'QCD' : [],
	'singleMuon' : [],
	'SingleElectron' : [],
	'WJets' : [],
	'rsg' : [],
	'ttbar' : [],
	'singletop' : []
}

def make_dirs(dirname):
    """
    Ensure that a named directory exists; if it does not, attempt to create it.
    """
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise


# Extract file names
def names(path):
	for name in run_all.keys():
		files, outfiles = [], []
		batcmd="xrdfs root://cmseos.fnal.gov ls -u " + path
		temps = subprocess.check_output(batcmd, shell=True)
		for file in temps.split("\n"):
		    #print file.split("/")
		    if file.split("/")[-1].startswith(name) :
		        run_all[name].append(file)
		        outnames[name].append(file.split("/")[-1][0:-5])
	return run_all, outnames

# Compile function inputs
def inputs(outnames, files=run_all, dir_name="root_files", corrs=False):
	ins = []
	if corrs == True: correlations = ["--jer", "--jec", "--sf"]
	else: correlations = [""]
	for corr in correlations:
		for shape in ["up", "down"]:
			for leptype in ['mu', 'el']:
				for typ in files.keys(): 
					for i, n in enumerate(run_all[typ]):
						data = "False"
						if typ == 'singleMuon' or typ == 'SingleElectron': data = "True"
						if typ == 'singleMuon' and leptype == 'el': continue
						if typ == 'SingleElectron' and leptype == 'mu': continue
						if data == "True":
							if shape == "down": continue
							if "all" not in outnames[typ][i].lower(): continue
						print outnames[typ][i]
						in_file = run_all[typ][i]					
						make_dirs(dir_name)
						# Raw files
						if corrs == False: 
							out_file = "root_files/"+outnames[typ][i]+"_plots_"+leptype+".root"
							ins.append(["--file_in", in_file, "--file_out", out_file, "--lepton", leptype, '--isData', data ]) 
						else:
						# Systematic modified files
							if data == "True": continue
							out_file = "root_files/"+outnames[typ][i]+"_plots_"+leptype+"_"+corr[2:]+"_"+shape+".root"
							ins.append(["--file_in", in_file, "--file_out", out_file, "--lepton", leptype, corr, shape, '--isData', data]) 
	return ins
#############
#############
# Run
if __name__ == "__main__" :
	path = "/store/user/cmsdas/2018/long_exercises/B2GTTbar/"
	run_all, outnames = names(path)
	ins = inputs(outnames, files=data, corrs=False)
	# Run in parallel
	from multiprocessing import Pool
	p = Pool(22)
	control_passs = (p.map(plot_mttbar, ins))
