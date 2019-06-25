# coding=utf-8
#! /usr/bin/env python3.4

"""
This code migrate wordnet data from LMF format to Princeton

Chakaveh.saedi@di.fc.ul.pt
"""

# https://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

import os

from modules.input_output import *
import xml.etree.cElementTree as ET

def xml_handler_odwn(src_file, rel_name_symbol):
    # this function reads the the Dutch xml file and saves the sense/synsets info
    # Synsets are saved in a dictionary as follows
    #    synsets[id] = (synset_num,[synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss],similar_to)
    # Senses are saved in a dictionary as follows
    # senses[id] = (lemma, word_pos, containing_synset)

    rel_name_symbol["has_hyponym"] = rel_name_symbol["hyponym"]
    rel_name_symbol["has_hyperonym"] = rel_name_symbol["hypernym"]
    rel_name_symbol["has_xpos_hyperonym"] = rel_name_symbol["instance_hypernym"]
    rel_name_symbol["has_xpos_hyponym"] = rel_name_symbol["instance_hyponym"]
    rel_name_symbol["has_holo_part"] = rel_name_symbol["holo_part"]
    rel_name_symbol["has_holo_madeof"] = rel_name_symbol["holo_substance"]
    rel_name_symbol["has_holo_member"] = rel_name_symbol["holo_member"]
    rel_name_symbol["has_mero_member"] = rel_name_symbol["mero_member"]
    rel_name_symbol["has_mero_part"] = rel_name_symbol["mero_part"]
    rel_name_symbol["has_mero_madeof"] = rel_name_symbol["mero_substance"]
    rel_name_symbol["near_antonym"] = rel_name_symbol["antonym"]
    rel_name_symbol["near_synonym"] = rel_name_symbol["similar"]

    senses = {}
    synsets = {}
    synset_num = 0
    seen_words = set()
    synset_with_words = set()
    unwanted_sections = set()
    comment = []

    tree = ET.ElementTree(file=os.getcwd() + "/data/input/" + src_file)
    root = tree.getroot()

    print(" * Reading the LMF file")

    for section in root:
        if section.tag not in unwanted_sections:
            print("  **  "  + section.tag)
            if section.tag == "Lexicon":                     # The "Lexicon" section is what we need
                if comment == []:
                    for attrib in section.attrib:
                        comment.append(str(attrib) + ": " + section.attrib[attrib])
                for element in section:                      # Each Lexicon has 2 elements "LexicalEntry" and "Synset"
                    # LexicalEntry
                    if element.tag == "LexicalEntry":
                        containing_synset = []
                        valid_sense = True                   # if a sense doesn't belong to a synset it is invalid
                        this_LexicalEntry = element          # just to make the code easier to follow
                        id = this_LexicalEntry.attrib["id"]
                        #print("    Current LexicalEntry: ", id)

                        for word_info in this_LexicalEntry:  # each lexical entry has Lemma, pos, sense1..n and the belonging synset
                            if word_info.tag == "Lemma":
                                lemma = word_info.attrib["writtenForm"]
                                seen_words.add(lemma)
                            pos_flag = False
                            if word_info.tag == "Sense":
                                try:
                                    syn = word_info.attrib["synset"]
                                    containing_synset.append(syn)
                                    synset_with_words.add(syn)
                                    if syn in synsets.keys():
                                        synsets[syn] += "\t" + lemma
                                    else:
                                        synsets[syn] = lemma

                                    if not pos_flag:
                                        word_pos = syn.split("-")[-1]
                                        pos_flag = True
                                except:
                                    valid_sense = False
                                    print("    Current LexicalEntry: ", id, word_info)
                        if valid_sense:
                            senses[id] = (lemma, word_pos, containing_synset)

                    #Synset
                    elif element.tag == "Synset":
                        gloss = ""
                        rel_type = []
                        target_synset = []
                        target_synset_pos = []

                        this_synset = element               # just to make the code easier to follow
                        id = this_synset.attrib["id"]
                        synset_pos = id.split("-")[-1]

                        for synset_info in this_synset:  # each synset has SynsetRelation and gloss
                            if synset_info.tag == "Definition" or synset_info.tag == "Statement":
                                if "gloss" in synset_info.attrib.keys():
                                    gloss += synset_info.attrib["gloss"] + "; "
                                elif "example" in synset_info.attrib.keys():
                                    gloss += '"' + synset_info.attrib["example"] + ';"'
                                else:
                                    gloss += synset_info.text + ";"
                            if synset_info.tag == "Definitions":
                                for defin in synset_info:
                                    if "gloss" in defin.attrib.keys():
                                        gloss += defin.attrib["gloss"] + "; "
                                    elif "example" in defin.attrib.keys():
                                        gloss += '"' + defin.attrib["example"] + ';"'
                                    else:
                                        gloss += synset_info.text + ";"
                            elif synset_info.tag == "SynsetRelations":
                                for syn_rel in synset_info:
                                    cur_rel = syn_rel.attrib["relType"]
                                    if cur_rel in rel_name_symbol.keys():
                                        rel_type.append(rel_name_symbol[cur_rel])
                                        target = syn_rel.attrib["target"]
                                        target_synset.append(target)
                                        target_synset_pos.append(target.split("-")[-1])

                        if id not in synsets.keys():
                            synset_words = ""
                        else:
                            synset_words = synsets[id]
                        synsets[id] = (synset_num, [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss[:gloss.rfind(";")]],[])
                        synset_num += 1

                    else:
                        print("    Unknown element in Lexicon: " + str(element.tag))
            else:
                print("    Unknown section in the input file: " + str(section.tag))
                unwanted_sections.add(section.tag)
    return senses, synsets, synset_with_words, comment

def xml_handler_zho(src_file, rel_name_symbol):
    # this function reads the the Dutch xml file and saves the sense/synsets info
    # Synsets are saved in a dictionary as follows
    #    synsets[id] = (synset_num,[synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss],similar_to)
    # Senses are saved in a dictionary as follows
    # senses[id] = (lemma, word_pos, containing_synset)

    rel_name_symbol["has_hyponym"] = rel_name_symbol["hyponym"]
    rel_name_symbol["has_hyperonym"] = rel_name_symbol["hypernym"]
    rel_name_symbol["eq_synonym"] = rel_name_symbol["similar"]

    senses = {}
    synsets = {}
    synset_num = 0
    seen_words = set()
    synset_with_words = set()
    unwanted_sections = set()
    comment = []

    tree = ET.ElementTree(file=os.getcwd() + "/data/input/" + src_file)
    root = tree.getroot()

    print(" * Reading the LMF file")

    for section in root:
        if section.tag not in unwanted_sections:
            print("  **  "  + section.tag)
            if section.tag == "Lexicon":                     # The "Lexicon" section is what we need
                if comment == []:
                    for attrib in section.attrib:
                        comment.append(str(attrib) + ": " + section.attrib[attrib])
                for element in section:                      # Each Lexicon has 2 elements "LexicalEntry" and "Synset"
                    # LexicalEntry
                    if element.tag == "LexicalEntry":
                        containing_synset = []
                        valid_sense = True                   # if a sense doesn't belong to a synset it is invalid
                        this_LexicalEntry = element          # just to make the code easier to follow
                        #print("    Current LexicalEntry: ", id)

                        for word_info in this_LexicalEntry:  # each lexical entry has Lemma, pos, sense1..n and the belonging synset
                            if word_info.tag == "Lemma":
                                lemma = word_info.attrib["writtenForm"]
                                seen_words.add(lemma)
                            pos_flag = False
                            if word_info.tag == "Sense":
                                try:
                                    id = word_info.attrib["id"]
                                    syn = word_info.attrib["synset"]
                                    containing_synset.append(syn)
                                    synset_with_words.add(syn)
                                    if syn in synsets.keys():
                                        synsets[syn] += "\t" + lemma
                                    else:
                                        synsets[syn] = lemma

                                    if not pos_flag:
                                        word_pos = syn.split("-")[-1]
                                        pos_flag = True
                                except:
                                    valid_sense = False
                                    print("    Current LexicalEntry: ", id, word_info)
                        if valid_sense:
                            senses[id] = (lemma, word_pos, containing_synset)

                    #Synset
                    elif element.tag == "Synset":
                        gloss = ""
                        rel_type = []
                        target_synset = []
                        target_synset_pos = []

                        this_synset = element               # just to make the code easier to follow
                        id = this_synset.attrib["id"]
                        synset_pos = id.split("-")[-1]

                        for synset_info in this_synset:  # each synset has SynsetRelation and gloss
                            if synset_info.tag == "Definition":
                                if "gloss" in synset_info.attrib.keys():
                                    gloss += synset_info.attrib["gloss"] + "; "
                                else:
                                    gloss += synset_info.text + ";"
                            elif synset_info.tag == "SynsetRelations":
                                for syn_rel in synset_info:
                                    cur_rel = syn_rel.attrib["relType"]
                                    if cur_rel in rel_name_symbol.keys():
                                        rel_type.append(rel_name_symbol[cur_rel])
                                        target = syn_rel.attrib["target"]
                                        target_synset.append(target)
                                        target_synset_pos.append(target.split("-")[-1])

                        if id not in synsets.keys():
                            synset_words = ""
                        else:
                            synset_words = synsets[id]
                        synsets[id] = (synset_num, [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss[:gloss.rfind(";")]],[])
                        synset_num += 1

                    else:
                        print("    Unknown element in Lexicon: " + str(element.tag))

            elif section.tag == "SenseAxes":
                for element in section:  # for similar  to relations
                    if element.tag == "SenseAxis" and element.attrib["relType"] == "eq_synonym":
                        temp = []
                        for sim in element:
                            temp.append(sim.attrib["ID"])
                        if temp[0] in synsets.keys():
                            synsets[temp[0]][2].append(temp[1])
            else:
                print("    Unknown section in the input file: " + str(section.tag))
                unwanted_sections.add(section.tag)
    return senses, synsets, synset_with_words, comment

def xml_handler_jpn(src_file, rel_name_symbol):
    # this function reads the Japanese xml file and saves the sense/synsets info
    # Synsets are saved in a dictionary as follows
    #    synsets[id] = (synset_num,[synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss],similar_to)
    # Senses are saved in a dictionary as follows
    # senses[id] = (lemma, word_pos, containing_synset)

    rel_name_symbol["hypo"] = rel_name_symbol["hyponym"]
    rel_name_symbol["hasi"] = rel_name_symbol["instance_hyponym"]
    rel_name_symbol["hype"] = rel_name_symbol["hypernym"]
    rel_name_symbol["inst"] = rel_name_symbol["instance_hypernym"]
    rel_name_symbol["enta"] = rel_name_symbol["entails"]
    rel_name_symbol["attr"] = rel_name_symbol["attribute"]
    rel_name_symbol["hprt"] = rel_name_symbol["holo_part"]
    rel_name_symbol["hsub"] = rel_name_symbol["holo_substance"]
    rel_name_symbol["hmem"] = rel_name_symbol["holo_member"]
    rel_name_symbol["mmem"] = rel_name_symbol["mero_member"]
    rel_name_symbol["mprt"] = rel_name_symbol["mero_part"]
    rel_name_symbol["msub"] = rel_name_symbol["mero_substance"]
    rel_name_symbol["caus"] = rel_name_symbol["causes"]
    rel_name_symbol["also"] = rel_name_symbol["also"]
    rel_name_symbol["antonym"] = rel_name_symbol["antonym"]
    rel_name_symbol["eq_synonym"] = rel_name_symbol["similar"]
    rel_name_symbol["dmtc"] = rel_name_symbol["has_domain_topic"]
    rel_name_symbol["dmnc"] = rel_name_symbol["domain_topic"]
    rel_name_symbol["dmtr"] = rel_name_symbol["has_domain_region"]
    rel_name_symbol["dmnr"] = rel_name_symbol["domain_region"]
    rel_name_symbol["dmtu"] = rel_name_symbol["USAG-Domain-Mem"]
    rel_name_symbol["dmnu"] = rel_name_symbol["USAG-syn-Domain"]

    senses = {}
    synsets = {}
    synset_num = 0
    seen_words = set()
    synset_with_words = set()
    unwanted_sections = set()
    comment = []
    similar_to_rel = set()

    tree = ET.ElementTree(file=os.getcwd() + "/data/input/" + src_file)
    root = tree.getroot()

    print(" * Reading the LMF file")

    for section in root:
        if section.tag not in unwanted_sections:
            print("  **  "  + section.tag)
            if section.tag == "Lexicon":                     # The "Lexicon" section is what we need
                if comment == []:
                    for attrib in section.attrib:
                        comment.append(str(attrib) + ": " + section.attrib[attrib])
                for element in section:                      # Each Lexicon has 2 elements "LexicalEntry" and "Synset"
                    # LexicalEntry
                    if element.tag == "LexicalEntry":
                        containing_synset = []
                        valid_sense = True                   # if a sense doesn't belong to a synset it is invalid
                        this_LexicalEntry = element          # just to make the code easier to follow
                        id = this_LexicalEntry.attrib["id"]
                        #print("    Current LexicalEntry: ", id)

                        for word_info in this_LexicalEntry:  # each lexical entry has Lemma, pos, sense1..n and the belonging synset
                            if word_info.tag == "Lemma":
                                lemma = word_info.attrib["writtenForm"]
                                word_pos = word_info.attrib["partOfSpeech"]
                                seen_words.add(lemma)
                            if word_info.tag == "Sense":
                                try:
                                    syn = word_info.attrib["synset"]
                                    containing_synset.append(syn)
                                    synset_with_words.add(syn)
                                    if syn in synsets.keys():
                                        synsets[syn] += "\t" + lemma
                                    else:
                                        synsets[syn] = lemma

                                except:
                                    valid_sense = False
                                    print("    Current LexicalEntry: ", id, word_info)
                        if valid_sense:
                            senses[id] = (lemma, word_pos, containing_synset)

                    #Synset
                    elif element.tag == "Synset":
                        gloss = ""
                        rel_type = []
                        target_synset = []
                        target_synset_pos = []

                        this_synset = element               # just to make the code easier to follow
                        id = this_synset.attrib["id"]
                        synset_pos = id.split("-")[-1]

                        for synset_info in this_synset:  # each synset has SynsetRelation and gloss
                            if synset_info.tag == "Definition" or synset_info.tag == "Statement":
                                if "gloss" in synset_info.attrib.keys():
                                    gloss += synset_info.attrib["gloss"] + "; "
                                elif "example" in synset_info.attrib.keys():
                                    gloss += '"' + synset_info.attrib["example"] + ';"'
                                else:
                                    gloss += synset_info.text + ";"
                            if synset_info.tag == "Definitions":
                                for defin in synset_info:
                                    if "gloss" in defin.attrib.keys():
                                        gloss += defin.attrib["gloss"] + "; "
                                    elif "example" in defin.attrib.keys():
                                        gloss += '"' + defin.attrib["example"] + ';"'
                                    else:
                                        gloss += synset_info.text + ";"
                            elif synset_info.tag == "SynsetRelations":
                                for syn_rel in synset_info:
                                    cur_rel = syn_rel.attrib["relType"]
                                    if cur_rel in rel_name_symbol.keys():
                                        rel_type.append(rel_name_symbol[cur_rel])
                                        target = syn_rel.attrib["targets"]
                                        target_synset.append(target)
                                        target_synset_pos.append(target.split("-")[-1])

                        if id not in synsets.keys():
                            synset_words = ""
                        else:
                            synset_words = synsets[id]
                        synsets[id] = (synset_num, [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss[:gloss.rfind(";")]],[])
                        synset_num += 1

                    else:
                        print("    Unknown element in Lexicon: " + str(element.tag))
            elif section.tag == "SenseAxes":
                for element in section:  # for similar  to relations
                    if element.tag == "SenseAxis" and element.attrib["relType"] == "eq_synonym":
                        temp = []
                        for sim in element:
                            temp.append(sim.attrib["ID"])
                        if temp[0] in synsets.keys():
                            synsets[temp[0]][2].append(temp[1])
            else:
                print("    Unknown section in the input file: " + str(section.tag))
                unwanted_sections.add(section.tag)
    return senses, synsets, synset_with_words, comment

def xml_handler_chn(src_file, rel_name_symbol):
    # this function reads the Japanese xml file and saves the sense/synsets info
    # Synsets are saved in a dictionary as follows
    #    synsets[id] = (synset_num,[synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss],similar_to)
    # Senses are saved in a dictionary as follows
    # senses[id] = (lemma, word_pos, containing_synset)

    rel_name_symbol["hypo"] = rel_name_symbol["hyponym"]
    rel_name_symbol["hasi"] = rel_name_symbol["instance_hyponym"]
    rel_name_symbol["hype"] = rel_name_symbol["hypernym"]
    rel_name_symbol["inst"] = rel_name_symbol["instance_hypernym"]
    rel_name_symbol["enta"] = rel_name_symbol["entails"]
    rel_name_symbol["attr"] = rel_name_symbol["attribute"]
    rel_name_symbol["hprt"] = rel_name_symbol["holo_part"]
    rel_name_symbol["hsub"] = rel_name_symbol["holo_substance"]
    rel_name_symbol["hmem"] = rel_name_symbol["holo_member"]
    rel_name_symbol["mmem"] = rel_name_symbol["mero_member"]
    rel_name_symbol["mprt"] = rel_name_symbol["mero_part"]
    rel_name_symbol["msub"] = rel_name_symbol["mero_substance"]
    rel_name_symbol["caus"] = rel_name_symbol["causes"]
    rel_name_symbol["also"] = rel_name_symbol["also"]
    rel_name_symbol["ants"] = rel_name_symbol["antonym"]
    rel_name_symbol["eq_synonym"] = rel_name_symbol["similar"]
    rel_name_symbol["sim"] = rel_name_symbol["similar"]
    rel_name_symbol["dmtc"] = rel_name_symbol["has_domain_topic"]
    rel_name_symbol["dmnc"] = rel_name_symbol["domain_topic"]
    rel_name_symbol["dmtr"] = rel_name_symbol["has_domain_region"]
    rel_name_symbol["dmnr"] = rel_name_symbol["domain_region"]
    rel_name_symbol["dmtu"] = rel_name_symbol["USAG-Domain-Mem"]
    rel_name_symbol["dmnu"] = rel_name_symbol["USAG-syn-Domain"]

    senses = {}
    synsets = {}
    synset_num = 0
    seen_words = set()
    synset_with_words = set()
    unwanted_sections = set()
    comment = []
    similar_to_rel = set()

    tree = ET.ElementTree(file=os.getcwd() + "/data/input/" + src_file)
    root = tree.getroot()

    print(" * Reading the LMF file")

    for section in root:
        if section.tag not in unwanted_sections:
            print("  **  "  + section.tag)
            if section.tag == "Lexicon":                     # The "Lexicon" section is what we need
                if comment == []:
                    for attrib in section.attrib:
                        comment.append(str(attrib) + ": " + section.attrib[attrib])
                for element in section:                      # Each Lexicon has 2 elements "LexicalEntry" and "Synset"
                    # LexicalEntry
                    if element.tag == "LexicalEntry":
                        containing_synset = []
                        valid_sense = True                   # if a sense doesn't belong to a synset it is invalid
                        this_LexicalEntry = element          # just to make the code easier to follow
                        id = this_LexicalEntry.attrib["id"]
                        #print("    Current LexicalEntry: ", id)

                        for word_info in this_LexicalEntry:  # each lexical entry has Lemma, pos, sense1..n and the belonging synset
                            if word_info.tag == "Lemma":
                                lemma = word_info.attrib["writtenForm"]
                                word_pos = word_info.attrib["partOfSpeech"]
                                seen_words.add(lemma)
                            if word_info.tag == "Sense":
                                try:
                                    syn = word_info.attrib["synset"]
                                    containing_synset.append(syn)
                                    synset_with_words.add(syn)
                                    if syn in synsets.keys():
                                        synsets[syn] += "\t" + lemma
                                    else:
                                        synsets[syn] = lemma

                                except:
                                    valid_sense = False
                                    print("    Current LexicalEntry: ", id, word_info)
                        if valid_sense:
                            senses[id] = (lemma, word_pos, containing_synset)

                    #Synset
                    elif element.tag == "Synset":
                        gloss = ""
                        rel_type = []
                        target_synset = []
                        target_synset_pos = []

                        this_synset = element               # just to make the code easier to follow
                        id = this_synset.attrib["id"]
                        synset_pos = id.split("-")[-1]

                        for synset_info in this_synset:  # each synset has SynsetRelation and gloss
                            if synset_info.tag == "Definition" or synset_info.tag == "Statement":
                                if "gloss" in synset_info.attrib.keys():
                                    gloss += synset_info.attrib["gloss"] + "; "
                                elif "example" in synset_info.attrib.keys():
                                    gloss += '"' + synset_info.attrib["example"] + ';"'
                                else:
                                    gloss += synset_info.text + ";"
                            if synset_info.tag == "Definitions":
                                for defin in synset_info:
                                    if "gloss" in defin.attrib.keys():
                                        gloss += defin.attrib["gloss"] + "; "
                                    elif "example" in defin.attrib.keys():
                                        gloss += '"' + defin.attrib["example"] + ';"'
                                    else:
                                        gloss += synset_info.text + ";"
                            elif synset_info.tag == "SynsetRelations":
                                for syn_rel in synset_info:
                                    cur_rel = syn_rel.attrib["relType"]
                                    if cur_rel in rel_name_symbol.keys():
                                        rel_type.append(rel_name_symbol[cur_rel])
                                        target = syn_rel.attrib["targets"]
                                        target_synset.append(target)
                                        target_synset_pos.append(target.split("-")[-1])

                        if gloss == "":
                            gloss = "    "

                        if id not in synsets.keys():
                            synset_words = ""
                        else:
                            synset_words = synsets[id]
                        synsets[id] = (synset_num, [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss[:gloss.rfind(";")]],[])
                        synset_num += 1

                    else:
                        print("    Unknown element in Lexicon: " + str(element.tag))
            elif section.tag == "SenseAxes":
                for element in section:  # for similar  to relations
                    if element.tag == "SenseAxis" and element.attrib["relType"] == "eq_synonym":
                        temp = []
                        for sim in element:
                            temp.append(sim.attrib["ID"])
                        if temp[0] in synsets.keys():
                            synsets[temp[0]][2].append(temp[1])
            else:
                print("    Unknown section in the input file: " + str(section.tag))
                unwanted_sections.add(section.tag)
    return senses, synsets, synset_with_words, comment

def xml_handler_general(src_file, rel_name_symbol):
    # this function reads the an xml file -Completely compatible with the LMF format- and saves the sense/synsets info
    # Synsets are saved in a dictionary as follows
    #    synsets[id] = [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss]
    # Senses are saved in a dictionary as follows
    # senses[id] = (lemma, word_pos, containing_synset)

    rel_name_symbol["instance_hyponym"] = rel_name_symbol["instance_hyponym"]
    rel_name_symbol["instance_hypernym"] = rel_name_symbol["instance_hypernym"]
    rel_name_symbol["attribute"] = rel_name_symbol["attribute"]
    rel_name_symbol["holo_part"] = rel_name_symbol["holo_part"]
    rel_name_symbol["holo_substance"] = rel_name_symbol["holo_substance"]
    rel_name_symbol["holo_member"] = rel_name_symbol["holo_member"]
    rel_name_symbol["mero_member"] = rel_name_symbol["mero_member"]
    rel_name_symbol["mero_part"] = rel_name_symbol["mero_part"]
    rel_name_symbol["mero_substance"] = rel_name_symbol["mero_substance"]
    rel_name_symbol["causes"] = rel_name_symbol["causes"]
    rel_name_symbol["also"] = rel_name_symbol["also"]
    rel_name_symbol["antonym"] = rel_name_symbol["antonym"]
    rel_name_symbol["similar"] = rel_name_symbol["similar"]
    #rel_name_symbol["eq_synonym"] = rel_name_symbol["similar"]
    #rel_name_symbol["sim"] = rel_name_symbol["similar"]
    rel_name_symbol["has_domain_topic"] = rel_name_symbol["has_domain_topic"]
    rel_name_symbol["domain_topic"] = rel_name_symbol["domain_topic"]
    rel_name_symbol["has_domain_region"] = rel_name_symbol["has_domain_region"]
    rel_name_symbol["domain_region"] = rel_name_symbol["domain_region"]


    senses = {}
    synsets = {}
    synset_num = 0
    seen_words = set()
    synset_with_words = set()
    unwanted_sections = set()
    comment = []

    tree = ET.ElementTree(file=os.getcwd() + "/data/input/" + src_file)
    root = tree.getroot()

    for section in root:
        if section.tag not in unwanted_sections:
            print("  **  "  + section.tag)
            if section.tag == "Lexicon":                     # The "Lexicon" section is what we need
                if comment == []:
                    for attrib in section.attrib:
                        comment.append(str(attrib) + ": " + section.attrib[attrib])
                for element in section:                      # Each Lexicon has 2 elements "LexicalEntry" and "Synset"
                    # LexicalEntry
                    if element.tag == "LexicalEntry":
                        containing_synset = []
                        valid_sense = True                   # if a sense doesn't belong to a synset it is invalid
                        this_LexicalEntry = element          # just to make the code easier to follow
                        id = this_LexicalEntry.attrib["id"]
                        #print("    Current LexicalEntry: ", id)

                        for word_info in this_LexicalEntry:  # each lexical entry has Lemma, pos, sense1..n and the belonging synset
                            if word_info.tag == "Lemma":
                                lemma = word_info.attrib["writtenForm"]
                                word_pos = word_info.attrib["partOfSpeech"]
                                seen_words.add(lemma)
                            if word_info.tag == "Sense":
                                try:
                                    syn = word_info.attrib["synset"]
                                    containing_synset.append(syn)
                                    synset_with_words.add(syn)
                                    if syn in synsets.keys():
                                        synsets[syn] += "\t" + lemma
                                    else:
                                        synsets[syn] = lemma

                                except:
                                    valid_sense = False
                                    print("    Current LexicalEntry: ", id, word_info)
                        if valid_sense:
                            senses[id] = (lemma, word_pos, containing_synset)

                    #Synset
                    elif element.tag == "Synset":
                        gloss = ""
                        rel_type = []
                        target_synset = []
                        target_synset_pos = []

                        this_synset = element               # just to make the code easier to follow
                        id = this_synset.attrib["id"]
                        synset_pos = id.split("-")[-1]

                        for synset_info in this_synset:  # each synset has SynsetRelation and gloss
                            if synset_info.tag == "Definition" or synset_info.tag == "Statement":
                                if "gloss" in synset_info.attrib.keys():
                                    gloss += synset_info.attrib["gloss"] + "; "
                                elif "example" in synset_info.attrib.keys():
                                    gloss += '"' + synset_info.attrib["example"] + ';"'
                                else:
                                    gloss += synset_info.text + ";"
                            if synset_info.tag == "Definitions":
                                for defin in synset_info:
                                    if "gloss" in defin.attrib.keys():
                                        gloss += defin.attrib["gloss"] + "; "
                                    elif "example" in defin.attrib.keys():
                                        gloss += '"' + defin.attrib["example"] + ';"'
                                    else:
                                        gloss += synset_info.text + ";"
                            elif synset_info.tag == "SynsetRelation":
                                for syn_rel in synset_info:
                                    cur_rel = syn_rel.attrib["relType"]
                                    if cur_rel in rel_name_symbol.keys():
                                        rel_type.append(rel_name_symbol[cur_rel])
                                        target = syn_rel.attrib["targets"]
                                        target_synset.append(target)
                                        target_synset_pos.append(target.split("-")[-1])

                        if gloss == "":
                            gloss = "    "

                        if id not in synsets.keys():
                            synset_words = ""
                        else:
                            synset_words = synsets[id]
                        synsets[id] = (synset_num, [synset_words, synset_pos, rel_type, target_synset, target_synset_pos, gloss[:gloss.rfind(";")]],[])
                        synset_num += 1

                    else:
                        print("    Unknown element in Lexicon: " + str(element.tag))
            elif section.tag == "SenseAxes":
                for element in section:  # for similar  to relations
                    if element.tag == "SenseAxis" and element.attrib["relType"] == "eq_synonym":
                        temp = []
                        for sim in element:
                            temp.append(sim.attrib["ID"])
                        if temp[0] in synsets.keys():
                            synsets[temp[0]][2].append(temp[1])
            else:
                print("    Unknown section in the input file: " + str(section.tag))
                unwanted_sections.add(section.tag)

    return senses, synsets, synset_with_words, comment
