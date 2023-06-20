"""
This code migrate wordnet data between LMF and Princeton format
input file is stored in data/input folder
outputs files will be saved in data/output folder

Chakaveh.saedi@di.fc.ul.pt
"""

import os
import argparse
from typing import List

from modules.lmf2princeton import *
from modules.princeton2lmf import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I",
        "--INPUT_FILES",
        type=str,
        nargs="+",
        default=["omw-arb.lmf", "omw-es.lmf", "omw-he.lmf", "omw-pl.lmf", "odenet.lmf"],
        help="List of names of input lmf format files to be migrated. (should be in data/input folder)",
    )
    parser.add_argument(
        "-P",
        "--PROCESS",
        type=str,
        default="l2p",
        choices=["l2p", "p2l"],
        help="Whether to go from lmf to princeton (l2p) or princeton to lmf (p2l)",
    )
    parser.add_argument(
        "-IP",
        "--ID_PREFIX",
        type=str,
        default="",
        help="Prefix for the id of the input wordnets/Synset id prefix. THIS IS IMPORTANT because the file will only be written to if `id_prefix` prefixes the input_file name.",
    )
    parser.add_argument("-SP", "--SIM_ID_PREFIX", type=str, default="", help="Prefix for ??")

    return parser.parse_args()


def main():
    args = get_args()
    INPUT_FILES = args.INPUT_FILES
    PROCESS = args.PROCESS
    ID_PREFIX = args.ID_PREFIX
    SIM_ID_PREFIX = args.SIM_ID_PREFIX

    print(f"Converting files: {INPUT_FILES}")
    convert_wn_format(INPUT_FILES=INPUT_FILES, PROCESS=PROCESS, ID_PREFIX=ID_PREFIX, SIM_ID_PREFIX=SIM_ID_PREFIX)


def convert_wn_format(
    INPUT_FILES: List[str],
    PROCESS: str,
    ID_PREFIX: str,
    SIM_ID_PREFIX: str,
):
    if PROCESS == "l2p":
        lmf2pri(INPUT_FILES, ID_PREFIX, SIM_ID_PREFIX)
    elif PROCESS == "p2l":
        pri2lmf(INPUT_FILES)
    else:
        print("Wrong Process Name")


if __name__ == "__main__":
    main()
