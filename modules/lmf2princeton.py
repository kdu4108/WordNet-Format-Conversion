# coding=utf-8
#! /usr/bin/env python3.4

"""
This code migrate wordnet data from LMF format to Princeton

Chakaveh.saedi@di.fc.ul.pt
"""

# https://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

import os

from modules.input_output import *
from modules.all_xml_handlers import *

def lmf2pri(source_files, id_prefix, sim_id_prefix, main_path):
    rel_name_symbol = rel_name_symbol_loader("l2p")  # {key = relation_name: val = relation_symbol}

    for src_file in source_files:
        if "omw-nl" in id_prefix:
            all_senses, all_synsets, synset_with_words, comment = xml_handler_odwn(src_file, rel_name_symbol)
        elif "zho-" in id_prefix:
            all_senses, all_synsets, synset_with_words, comment = xml_handler_zho(src_file, rel_name_symbol)
        elif "jpn-" in id_prefix or "nld-" in id_prefix:
            all_senses, all_synsets, synset_with_words, comment = xml_handler_jpn(src_file, rel_name_symbol)
        elif "cmn-" in id_prefix:
            all_senses, all_synsets, synset_with_words, comment = xml_handler_chn(src_file, rel_name_symbol)
        else:
            # NOTE: comment will be improperly formatted if the XML includes a `&#10;` which omw-arb.lmf does in the citation, for some reason. (hotfix: manually delete the &#10; from that lmf file.)
            all_senses, all_synsets, synset_with_words, comment = xml_handler_general(src_file, rel_name_symbol)
        data_file_creator(synset_with_words, all_synsets, id_prefix, sim_id_prefix, comment, src_file, main_path)
        index_file_creator(main_path)


def data_file_creator(synset_with_words, all_synsets, id_prefix, sim_id_prefix, comment, src_file, main_path):
    # this function creates the 4 data files based on Princeton format
    print("\n * Creating Princeton data")
    # 1st:  dividing the synsets based on the POS
    pos = ["n", "a", "v", "r", "s", "c", "x", "u"]
    pos_name = {"n": "noun", "a": "adj", "r": "adv", "v": "verb"}
    wn_data={}
    for itm in pos:
        wn_data[itm] = []

    for key in all_synsets.keys():                   # keys are synset ids
        try:
            if all_synsets[key][1][0] != "":         # if there is at least one word in this synset
                if all_synsets[key][1][1] in pos:
                    wn_data[all_synsets[key][1][1]].append((key, all_synsets[key]))
        except:
            print("    Not accurate data in ****",key )#all_synsets[key])

    # comment section for all data files
    all_comments = "  01 This file is a derivation of the " + src_file + ' file; the original ' + id_prefix + ' wordnet\n'
    all_comments += "  02 Please refer to the Read_Me file which provides information about the developing team, licenses and the original project\n"
    line_num = 3
    for line in comment:
        line = "  " + str(line_num).zfill(2) + " " + line + "\n"
        all_comments += line
        line_num += 1

    similar_to_log = open(os.path.join(main_path, id_prefix + "_similar_to_" + sim_id_prefix), "w")

    mappings = {"n": {}, "v": {}, "r": {}, "a": {}}
    all_data = {"n": [], "v": [], "r": [], "a": []}

    for key in wn_data.keys():                # keys are seen POSes in the XML file
        if key in ["n","r","a","v"]:          # Princeton only needs noun, verb, adjective and adverb
            print("    Working on the " + pos_name[key] + " data")
            # 2nd: creating the data file with the LMF IDs

            prob_log = open(os.path.join(main_path, "synset_extraction_issue_" + pos_name[key]), "w")
            prob_log.write("the following synset information are either not extracted properly or were not complete in the LMF file\n\n")

            current_offset = len(all_comments.encode("utf8"))
            sorted_synsets = sorted(wn_data[key], key=lambda x: x[1][0])

            for synset in sorted_synsets:
                if id_prefix not in synset[0]:         # in case the XML files contains more than one wordnet, each wordnet must be taken care of separately
                    #print("    Not a %s synset: %s"%(id_prefix, str(synset)))
                    continue

                if str(type(synset[1])) == "<class 'str'>":                    # if the synset information is not extracted correctly
                    prob_log.write(str(synset) + "\n")
                    continue

                #print("    Working on ", synset)

                lex_filenum = " 00 "                                   #check for the field in the LMF format ??????????
                synset_words = synset[1][1][0].split("\t")
                synset_pos = synset[1][1][1]
                synset_rel_typ = synset[1][1][2]
                synset_connection = synset[1][1][3]
                connection_pos = synset[1][1][4]

                old_offset = synset[0].split("-")[2]
                mappings[synset_pos].update({str(old_offset).zfill(8): str(current_offset).zfill(8)})

                i = 0
                while i < len(synset_connection):                         # what is the code for similar_to relation????????
                    if id_prefix not in synset_connection[i]:             # if this synset does not belog to the target language
                        if sim_id_prefix in synset_connection[i]:         # similar_to relation in case it is identified in the Synset field
                            similar_to_log.write(id_prefix + key + "\t" + str(current_offset).zfill(8) + "\t" + sim_id_prefix + synset_connection[i].split("-")[3] + "\t" + str(synset_connection[i].split("-")[2]) +"\n")

                        del synset_rel_typ[i]
                        del synset_connection[i]
                        del connection_pos[i]

                    elif synset_connection[i] not in synset_with_words:   # if the target synset doesn't have any words
                        del synset_rel_typ[i]
                        del synset_connection[i]
                        del connection_pos[i]

                    else:
                        synset_connection[i] = synset_connection[i].split("-")[2]
                        i += 1
                gloss= synset[1][1][5]

                # data line format
                # synset_offset  lex_filenum  syn_type  w_cnt  [word  lex_id...]  p_cnt  [ptr...]  [frames...]  |   gloss
                #-------------------
                # 1st-section: synset_offset  lex_filenum  syn_type  w_cnt
                line = str(current_offset).zfill(8) + lex_filenum + synset_pos + " " + hex(len(synset_words)).split("x")[1].zfill(2) + " "

                # 2nd-section: [word  lex_id...]
                for wrd in synset_words:
                    line += wrd.replace(" ", "_") + " 0 "                    #check for the field in the LMF format ??????????

                # 3rd-section p_cnt  [ptr...]
                pt_cnt = len(synset_rel_typ)
                if pt_cnt == 0:
                    line += "000 "
                else:
                    line += str(pt_cnt).zfill(3) + " "
                    for rel_indx in range(len(synset_rel_typ)):
                        line += synset_rel_typ[rel_indx] + " " + synset_connection[rel_indx].replace(id_prefix,"") + " " + connection_pos[rel_indx] + " 0000 "     #check for the word connection in the LMF format ??????????

                # frame (just for verbs)
                if synset_pos == "v":                      # check for the frame in the LMF format ??????????
                    line += "01 + 00 00 "                  # 01:frame_num, +:fix parameter,  00:OUR way of saying unknown frame, 00: applies to all words in the synset

                #gloss
                line += "| " + gloss + "\n"

                all_data[synset_pos].append(line)

                # similar_to relation in case it is identified in the SenseAxes field
                for sim_to in synset[1][2]:
                    if sim_id_prefix in sim_to:
                        similar_to_log.write(id_prefix + key + "\t" + str(current_offset).zfill(8) + "\t" + sim_id_prefix + sim_to.split("-")[3] + "\t" + str(sim_to.split("-")[2]) + "\n")

                current_offset += len(line.encode("utf8"))

            prob_log.close()

    similar_to_log.close()

    # 3rd: replacing the offsets with Princetone offsets
    print("\n * Replacing old offsets with the new ones - This might take long")
    for file_key in all_data.keys():
        print("    working on %s file"%(str(file_key)))
        for indx in range(len(all_data[file_key])):
            for map_key in mappings.keys():
                for ele in mappings[map_key]:
                    all_data[file_key][indx] = all_data[file_key][indx].replace(ele + " " + map_key,mappings[map_key][ele] + " " + map_key)

    # 4th: creating the data file
    print("\n * Writing Princeton data files")
    for file_key in all_data.keys():
        data_file_writer(all_comments, all_data[file_key], main_path, file_key)

def index_file_creator(main_path):
    print("\n * Creating Princeton index files")

    data_files = ["data.noun","data.adv","data.verb","data.adj"]

    for data_file in data_files:
        inputFile = open(os.path.join(main_path, data_file))
        src = inputFile.readlines()
        inputFile.close()

        f_name = "index." + data_file.split(".")[1]
        index_file = open(os.path.join(main_path, f_name), "w")

        seenWrds = set()
        wrdsInfos = {}

        commnt_cnt = 0
        while commnt_cnt <len(src) and src[commnt_cnt][0:2] == "  ":
            commnt_cnt += 1

        for i in range(commnt_cnt, len(src)):
            lineParts = src[i].split(" ")
            cur_synset = lineParts[0]
            cur_synset_pos = lineParts[2]

            cur_synset_wrdNum = int(lineParts[3], 16)

            cur_synset_wrds = []
            cur_synset_conTypes = []
            cur_synset_conSynset = []
            cur_synset_conPos = []

            "senses"
            indx = 4
            for cnt in range(cur_synset_wrdNum):
                cur_synset_wrds.append(lineParts[indx])
                indx += 2

            cur_synset_conNum = int(lineParts[indx])
            indx += 1

            "connected synsets"
            for cnt in range(cur_synset_conNum):
                cur_synset_conTypes.append(lineParts[indx])
                indx += 1

                cur_synset_conSynset.append(lineParts[indx])
                indx += 1

                cur_synset_conPos.append(lineParts[indx])
                indx += 2

            for wrd in cur_synset_wrds:
                # if wrdsInfos.has_key(wrd):
                if wrd in wrdsInfos.keys():
                    for conType in cur_synset_conTypes:
                        wrdsInfos[wrd][1].add(conType)
                    wrdsInfos[wrd][2].append(cur_synset)
                else:
                    ctype = set()
                    for conType in cur_synset_conTypes:
                        ctype.add(conType)
                    key = wrd
                    info = [cur_synset_pos, ctype, [cur_synset]]  # [pos, connection_types, List of synsets]
                    wrdsInfos.update({key: info})

        #print ("   \n%d words were extracted\n" % (len(wrdsInfos.keys())))
        cnt = 1

        for key in wrdsInfos.keys():
            temp = str(key).lower() + " " + wrdsInfos[key][0] + " " + str(len(wrdsInfos[key][2])) + " " + str(
                len(wrdsInfos[key][1])) + " "
            for conType in wrdsInfos[key][1]:
                temp += conType + " "
            temp += str(len(wrdsInfos[key][2])) + " 0 "
            for synset in wrdsInfos[key][2]:
                temp += synset + " "

            temp += "\n"
            temp = temp.replace(" \n", "\n")

            index_file.write(temp)

            cnt += 1

        index_file.close()
        print("    %s created"%(f_name))
