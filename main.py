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
input_file = ["omw-arb.lmf"]  # name of files that are going to be migrated   (should be in data/input folder)
main_path = os.path.join(os.getcwd(), "data/output/", input_file[0].split(".")[0])  # the main path to save the ooutput
process = "l2p"  # l2p --> LMF to Princeton           p2l  --> princeton to LMF

id_prefix = ""  # Synset id prefix. THIS IS IMPORTANT because the file will only be written to if `id_prefix` prefixes the input_file name.
sim_id_prefix = ""

# -----------------------------------------------------------
os.makedirs(main_path, exist_ok=True)

if process == "l2p":
    lmf2pri(input_file, id_prefix, sim_id_prefix, main_path)
elif process == "p2l":
    pri2lmf(input_file)
else:
    print("Wrong Process Name")
