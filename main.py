# coding=utf-8
#! /usr/bin/env python3.4

"""
This code migrate wordnet data between LMF and Princeton format
input file is stored in data/input folder
outputs files will be saved in data/output folder

Chakaveh.saedi@di.fc.ul.pt
"""

import os
from modules.lmf2princeton import *
from modules.princeton2lmf import *

# ------------------------------------------ Variables to SET
main_path = os.getcwd() + "/data/output/"                # the main path to save the ooutput
process = "l2p"                                          # l2p --> LMF to Princeton           p2l  --> princeton to LMF

input_file = ["input-file.lmf"]               # name of files that are going to be migrated   (should be in data/input folder)
id_prefix = "prefix-"                          # Synset id prefix
sim_id_prefix = ""


#-----------------------------------------------------------

if process == "l2p":
    lmf2pri(input_file, id_prefix, sim_id_prefix, main_path)
elif process == "p2l":
    pri2lmf(input_file)
else:
    print("Wrong Process Name")
