"""
This code migrate wordnet data from Princeton format to LMF

Chakaveh.saedi@di.fc.ul.pt
"""

from modules.input_output import *


def pri2lmf(source_files):
    rel_name_symbol = rel_name_symbol_loader("p2l")

    for src_file in source_files:
        print(src_file)
