# coding=utf-8
#! /usr/bin/env python3.4

import os

def rel_name_symbol_loader(process):
    # To create a dictionary of relation_names and relation_symbols
    # if LMF to Princeton   {key = relation_name: val = relation_symbol}
    # if Princeton to LMF   {key = relation_symbol: val = relation_name}

    path = os.path.join(os.getcwd(), "data", "input", "settings", "relation_name_symbols")

    inp_f = open(path)
    src = inp_f.readlines()
    inp_f.close()

    rel_symbol = {}

    for line in src:
        if process == "l2p":
            temp = line.replace("\n","").split("\t")
            rel_symbol[temp[0]] = temp[1]
        else:
            temp = line.replace("\n", "").split("\t")
            rel_symbol[temp[1]] = temp[2]

    return(rel_symbol)

def data_file_writer(all_comments,data, main_path, pos_key):
    pos = {"n":"noun", "a":"adj", "r":"adv", "v":"verb"}
    data_file = open(main_path + "data." + pos[pos_key], "w")
    data_file.write(all_comments)
    for line in data:
        data_file.write(line)
    data_file.close()
