#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:01:12 2020

@author: schorb
"""


from tkinter import *
from tkinter import ttk
import os

def calculate(*args):
    numcpus.set(int(numcpus.get()*2))
def calculate1(*args):
    numcpus.set(int(numcpus.get()/2))



def cluster_fiji(*args):
    timelim = s_t.get()
    memlim = s_mem.get()
    n_cpu = s_cpu.get()

    callcmd = 'srun -N1 --pty --x11 n'

    callcmd += n_cpu

    callcmd += ' --mem '+memlim+'G '

    callcmd += '-t 0-'+timelim+':00'

    callcmd += 'bash /g/emcf/schorb/code/cluster/fijicluster.sh'


    os.system('cp /g/emcf/schorb/code/cluster/ImageJ.cfg  cp /g/emcf/schorb/code/cluster/ImageJ.cfg.orig')

    os.system('echo -Xmx'+memlim+'g > /g/emcf/schorb/code/cluster/ImageJ.cfg')
    os.system('cat /g/emcf/schorb/code/cluster/ImageJ.cfg.orig >> /g/emcf/schorb/code/cluster/ImageJ.cfg')

    print(callcmd)
    root.destroy()
    exit()







root = Tk()
root.title("Cluster Parameters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Set Parameters for Cluster Fiji").grid(column=2, row=1, sticky=W)

numcpus = DoubleVar()
numcpus.set(2)
s_cpu = Spinbox(mainframe, from_=1, to=100, textvariable=numcpus)
s_cpu.grid(column=1, row=2, sticky=E)


# ttk.Label(mainframe, text="Number of CPUs").grid(column=2, row=2, sticky=W)


mem = DoubleVar()
mem.set(4)
s_mem = Spinbox(mainframe, from_=1, to=128, textvariable=mem)
s_mem.grid(column=1, row=3, sticky=E)


ttk.Label(mainframe, text="Memory (GB)").grid(column=2, row=3, sticky=W)


time = DoubleVar()
time.set(24)
s_t = Spinbox(mainframe, from_=1, to=240, increment=6, textvariable=time)
s_t.grid(column=1, row=4, sticky=E)

ttk.Label(mainframe, text="Job time limit (h)").grid(column=2, row=4, sticky=W)


ttk.Button(mainframe, text="Go",command=cluster_fiji).grid(column=2, row=5, sticky=W)

# ttk.Label(mainframe, text="blabla").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', calculate)
root.bind('<minus>', calculate1)

root.mainloop()
