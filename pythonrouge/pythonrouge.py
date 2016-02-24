# -*- coding: utf-8 -*-
import os
import re
import glob
import tempfile
from tempfile import mkdtemp
import subprocess
import sys
import shutil

def pythonrouge(peer_sentence, model_sentence, ROUGE_path, data_path,  ngram_order=3):
    temp_dir = tempfile.mkdtemp()
    summary_dir = os.path.join(temp_dir, "model")
    reference_dir = os.path.join(temp_dir, "peer")

    os.mkdir(summary_dir)
    os.mkdir(reference_dir)
    
    model_summary = "model.txt"
    with open(summary_dir+"/" + model_summary, "w") as model:
        model.write(model_sentence)

    peer_summary = "peer.txt"
    with open(reference_dir+"/" + peer_summary, "w") as peer:
        peer.write(peer_sentence)

    abs_model_path = str(summary_dir+"/" + model_summary)
    abs_peer_path = str(reference_dir+"/" + peer_summary)

    model_sum_list = [abs_model_path]
    ref_sum_list = [[abs_peer_path]]

    options = "-a -m -n " + str(ngram_order)
    
    xml_path = "rouge.xml"
    with open(temp_dir+"/"+xml_path, "w") as xml_file:
        xml_file.write('<ROUGE-EVAL version="1.0">\n')
        for model_sum_index, model_sum_file in enumerate(model_sum_list):
            xml_file.write('<EVAL ID="' + str(model_sum_index+1) + '">\n')
            xml_file.write("<PEER-ROOT>\n")
            model_sum_dir = os.path.dirname(model_sum_file)
            xml_file.write(model_sum_dir + "\n")
            xml_file.write("</PEER-ROOT>\n")
            xml_file.write("<MODEL-ROOT>\n")
            ref_summ_dir = os.path.dirname(ref_sum_list[0][0] + "\n")
            xml_file.write(ref_summ_dir + "\n")
            xml_file.write("</MODEL-ROOT>\n")
            xml_file.write('<INPUT-FORMAT TYPE="SPL">\n')
            xml_file.write("</INPUT-FORMAT>\n")
            xml_file.write("<PEERS>\n")
            model_sum_basename = os.path.basename(model_sum_file)
            xml_file.write('<P ID="X">' + model_sum_basename + "</P>\n")
            xml_file.write("</PEERS>\n")
            xml_file.write("<MODELS>")
            letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
            ref_summ_basename = os.path.basename(ref_sum_list[0][0])
            xml_file.write('<M ID="' + letter_list[0] + '">' + ref_summ_basename + "</M>\n")
            xml_file.write("</MODELS>\n")

            xml_file.write("</EVAL>\n")
        xml_file.write("</ROUGE-EVAL>\n")
        xml_file.close()
    
    abs_xml_path = str(temp_dir+"/"+xml_path)
    output = subprocess.check_output([ROUGE_path, "-e", data_path, "-a", "-m", "-2", "-4","-n", str(ngram_order), "-x", abs_xml_path], stderr=subprocess.STDOUT)
    output = output.decode("utf-8")
    outputs = output.strip().split("\n")

    recall_list = list()
    precision_list = list()
    F_measure_list = list()

    for n in range(ngram_order+1):
        for line in outputs:
            for score in ["R", "P", "F"]:
                match = re.findall('X ROUGE-{0} Average_{1}: ([0-9.]+)'.format((n+1), score),line)
                su_match = re.findall("X ROUGE-S\* Average_{0}: ([0-9.]+)".format(score),line) #su-4
                if match:
                    if score == "R":
                        recall_list.append(float(match[0]))
                    elif score == "P":
                        precision_list.append(float(match[0]))
                    if score == "F":
                        F_measure_list.append(float(match[0]))
                if su_match and n == 3:                
                        if score == "R":
                            recall_list.append(float(su_match[0]))
                        elif score == "P":
                            precision_list.append(float(su_match[0]))
                        if score == "F":
                            F_measure_list.append(float(su_match[0]))
    
    # you can return precision and recall if you add those list to result
    result = {}
    result["rouge-1"] = F_measure_list[0]
    result["rouge-2"] = F_measure_list[1]
    result["rouge-3"] = F_measure_list[2]
    result["rouge-su4"] = F_measure_list[3]
    shutil.rmtree(temp_dir)
    return result
