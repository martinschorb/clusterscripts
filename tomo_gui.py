#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:01:12 2020

@author: schorb
"""


from tkinter import * 

from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
import os

import subprocess

scriptdir = "/g/emcf/schorb/code/cluster/"

def calculate(*args):
    numcpus.set(int(numcpus.get()*2))
def calculate1(*args):
    numcpus.set(int(numcpus.get()/2))



def cluster_tomo(*args):
    timelim = s_t.get()
    memlim = s_mem.get()
    n_cpu = s_cpu.get()
    login = user.get()
    cwd = currdir.get()
    scriptdir = scripts_dir.get()
    directive = adoc.get()
    options = param_input.get()
    
    
    os.chdir(cwd)
    
    
    commands = list()
    commands.append('#!/bin/bash')
    commands.append('#SBATCH -N 1 ')
    commands.append('#SBATCH -n '+str(n_cpu))
    commands.append('#SBATCH --mem '+str(memlim)+'G')
    commands.append('#SBATCH -t 0-00:'+timelim+':00')
    commands.append('#SBATCH --mail-type=FAIL')
    commands.append('#SBATCH --mail-user='+login+'@embl.de') 
    commands.append('\n')
    commands.append('numcpu='+str(n_cpu))   
    commands.append('\n')
    
    with open('tomo_submit.sh','w') as file: file.writelines('\n'.join(commands))
    
    os.popen('tail -n+20 '+scriptdir+'tomo_submit.sh >> tomo_submit.sh')   
    
    callcmd = scriptdir+'cluster_tomo.sh `pwd` '
    callcmd += directive+' '
    callcmd += options
        
    os.popen(callcmd)

def browse_tomo_dir(*args):        
     conv_inputdir = filedialog.askdirectory(parent=root,title='Choose tomogram directory',initialdir=currdir)
     currdir.set(conv_inputdir)

def browse_adoc(*args):
    adoc_in = filedialog.askopenfilename(parent=root,title='Choose batch directive file',initialdir=currdir,filetypes=(('Batch directives','*.adoc'),('all files','*.*')))
    adoc.set(adoc_in)
    
def jobs(*args):
    p=subprocess.Popen('whoami',stdout=subprocess.PIPE,shell=True)
    user = p.communicate()[0].decode(encoding='utf8')    
    
    p=subprocess.Popen('squeue -u `whoami` -o "%.8i %.9P %.8j %.8u %.2t %.10M %.6C %.6D %16R %o"',stdout=subprocess.PIPE,shell=True)
    jobs = p.communicate()[0].decode(encoding='utf8')
    jobs_outtext.configure(state='normal')
    jobs_outtext.delete('1.0','end')
    jobs_outtext.insert('insert','Running cluster jobs for user: '+user)
    jobs_outtext.insert('end','\n'+'--'*12+'\n')
    jobs_outtext.insert('end',jobs)
    jobs_outtext.configure(state='disabled')
    


root = Tk()
root.title("Cluster Tomo Reconstruction")

thisdir = os.getcwd()

currdir = StringVar()
currdir.set(thisdir)

scripts_dir = StringVar()
scripts_dir.set(scriptdir)

adoc = StringVar()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Set Parameters for Cluster Tomo reconstruction").grid(column=1, row=1,columnspan=2)

p=subprocess.Popen('whoami',stdout=subprocess.PIPE,shell=True)
user = StringVar()
user.set(p.communicate()[0].decode(encoding='utf8'))


numcpus = DoubleVar()
numcpus.set(8)
s_cpu = Spinbox(mainframe, from_=1, to=100, textvariable=numcpus)
s_cpu.grid(column=1, row=2, sticky=E)


ttk.Label(mainframe, text="Number of CPUs").grid(column=2, row=2, sticky=W)


mem = DoubleVar()
mem.set(8)
s_mem = Spinbox(mainframe, from_=1, to=128, textvariable=mem)
s_mem.grid(column=1, row=3, sticky=E)


ttk.Label(mainframe, text="Memory (GB)").grid(column=2, row=3, sticky=W)


time_in = DoubleVar()
time_in.set(10)
s_t = Spinbox(mainframe, from_=1, to=240, increment=6, textvariable=time_in)
s_t.grid(column=1, row=4, sticky=E)

ttk.Label(mainframe, text="Job time limit (min)").grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, text="Choose Tomo input directory:").grid(column=1, row=5, sticky=E)
ttk.Button(mainframe, text="Browse",command=browse_tomo_dir).grid(column=2, row=5, sticky=W)

ttk.Label(mainframe, text="Choose batch directive file:").grid(column=1, row=6, sticky=E)
ttk.Button(mainframe, text="Browse",command=browse_adoc).grid(column=2, row=6, sticky=W)

param_input = StringVar()

ttk.Label(mainframe, text="Reconstruction parameters (d,m,p):").grid(column=1, row=7, sticky=E)
ttk.Entry(mainframe, textvariable=param_input).grid(column=2, row=7, sticky=W)

ttk.Button(mainframe, text="Go",command=cluster_tomo).grid(column=1, row=8,columnspan=2)

ttk.Label(mainframe, text="-"*50).grid(column=1, row=9,columnspan=2)


ttk.Button(mainframe, text="Update status",command=jobs).grid(column=1, row=10,columnspan=2)


jobs_outtext = scrolledtext.ScrolledText(mainframe)
jobs_outtext.configure(state='disabled')

jobs_outtext.grid(column=1, row=11,columnspan=2)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', calculate)
root.bind('<minus>', calculate1)

root.mainloop()
