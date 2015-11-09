# -*- coding: utf-8 -*-
import os
import re
import glob
import tempfile
from tempfile import mkdtemp
import subprocess
import sys



def pythonrouge(ROUGE_path, data_path, guess_sentence, ref_sentence, ngram_order=3):
    temp_dir = tempfile.mkdtemp()
    summary_dir = os.path.join(temp_dir, 'peers')
    reference_dir = os.path.join(temp_dir, 'models')

    os.mkdir(summary_dir)
    os.mkdir(reference_dir)
    
    guess_summary = "guess.txt"
    with open(summary_dir+"/"+guess_summary, "w") as guess:
        guess.write(guess_sentence)

    ref_summary = "ref.txt"
    with open(reference_dir+"/"+ref_summary, "w") as ref:
        ref.write(ref_sentence)

    abs_guess_path = str(summary_dir+"/"+guess_summary)
    abs_ref_path = str(reference_dir+"/"+ref_summary)

    guess_sum_list = [abs_guess_path]
    ref_sum_list = [[abs_ref_path]]

    options = '-a -m -n ' + str(ngram_order)
    
    xml_path = 'rouge.xml'
    with open(temp_dir+"/"+xml_path, "w") as xml_file:
        xml_file.write('<ROUGE-EVAL version="1.0">\n')
        for guess_summ_index,guess_summ_file in enumerate(guess_sum_list):
            xml_file.write('<EVAL ID="' + str(guess_summ_index+1) + '">\n')
            xml_file.write('<PEER-ROOT>\n')
            guess_summ_dir = os.path.dirname(guess_summ_file)
            xml_file.write(guess_summ_dir + '\n')
            xml_file.write('</PEER-ROOT>\n')
            xml_file.write('<MODEL-ROOT>\n')
            ref_summ_dir = os.path.dirname(ref_sum_list[0][0] + '\n')
            xml_file.write(ref_summ_dir + '\n')
            xml_file.write('</MODEL-ROOT>\n')
            xml_file.write('<INPUT-FORMAT TYPE="SPL">\n')
            xml_file.write('</INPUT-FORMAT>\n')
            xml_file.write('<PEERS>\n')
            guess_summ_basename = os.path.basename(guess_summ_file)
            xml_file.write('<P ID="X">' + guess_summ_basename + '</P>\n')
            xml_file.write('</PEERS>\n')
            xml_file.write('<MODELS>')
            letter_list = ['A','B','C','D','E','F','G','H','I','J']
            ref_summ_basename = os.path.basename(ref_sum_list[0][0])
            xml_file.write('<M ID="' + letter_list[0] + '">' + ref_summ_basename + '</M>\n')
            xml_file.write('</MODELS>\n')

            xml_file.write('</EVAL>\n')
        xml_file.write('</ROUGE-EVAL>\n')
        xml_file.close()
    
    abs_xml_path = str(temp_dir+"/"+xml_path)
    output = subprocess.check_output([ROUGE_path, "-e", data_path, "-a", "-m", "-2", "-4","-n", str(ngram_order), "-x", abs_xml_path])
    output = output.decode("utf-8")
    outputs = output.strip().split("\n")

    recall_list = list()
    precision_list = list()
    F_measure_list = list()

    for n in range(ngram_order+1): # SUも測るから+1
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
    result = {}
    result["rouge-1"] = F_measure_list[0]
    result["rouge-2"] = F_measure_list[1]
    result["rouge-3"] = F_measure_list[2]
    result["rouge-su4"] = F_measure_list[3]
    return result

if __name__ == '__main__':
    ROUGE = sys.argv[1]
    data_path = sys.argv[2]
    ref = "Kyoto is a nice place"
    guess = "Tokyo is a nice place"
    print("correct:", ref)
    print("guess A: ",guess)
    score = pythonrouge(ROUGE, data_path, guess, ref)
    print(score)
    print(ref)
    print(guess)

    print("ROUGE-1:", score["rouge-1"])
    print("ROUGE-2:", score["rouge-2"])
    print("ROUGE-3:", score["rouge-3"])
    print("ROUGE-SU4:", score["rouge-su4"])
    




