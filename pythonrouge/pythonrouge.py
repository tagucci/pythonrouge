# -*- coding: utf-8 -*-
import os
import re
import glob
import tempfile
from tempfile import mkdtemp
import subprocess
import sys
import shutil

def pythonrouge(peer_sentence, model_sentence, ROUGE_path='./pythonrouge/RELEASE-1.5.5/ROUGE-1.5.5.pl', data_path='./pythonrouge/RELEASE-1.5.5/data'):
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
    ROUGE_path   = os.path.abspath(ROUGE_path)
    data_path    = os.path.abspath(data_path)
    output = subprocess.check_output([ROUGE_path, "-e", data_path, "-a", "-m", "-2", "4","-n", "3", abs_xml_path], stderr=subprocess.STDOUT)
    output = output.decode("utf-8")
    outputs = output.strip().split("\n")
    F_measure_list = []
    result = dict()
    n = 1
    for line in outputs:
        rouge = 'ROUGE-{}'.format(n)
        match    = re.findall('X ROUGE-{} Average_F: ([0-9.]+)'.format(n), line)
        l_match  = re.findall('X ROUGE-L Average_F: ([0-9.]+)', line)  #ROUGE-L
        su_match = re.findall('X ROUGE-S4 Average_F: ([0-9.]+)', line)   #ROUGE-SU4
        if match:
            F_measure_list.append(float(match[0]))
            result[rouge] = float(match[0])
            n += 1
        elif l_match:
            F_measure_list.append(float(l_match[0]))    
            result['ROUGE-L'] = float(l_match[0])
        elif su_match:                
            F_measure_list.append(float(su_match[0]))
            result['ROUGE-SU4'] = float(su_match[0])
    shutil.rmtree(temp_dir)
    return result
