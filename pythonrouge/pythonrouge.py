# -*- coding: utf-8 -*-
import os
import re
import glob
import tempfile
from tempfile import mkdtemp
import subprocess
import sys
import shutil

class Pythonrouge:
    def __init__(self, n_gram=2, ROUGE_SU4=True, ROUGE_L=False, ROUGE_W=False, ROUGE_W_Weight=1.2, stemming=True, stopwords=False, word_level=True, length_limit=True, length=100, use_cf=False, cf=95, scoring_formula="average", resampling=True, samples=1000, favor=True, p=0.5):
        """
        n_gram: Compute ROUGE-N up to max-ngram length will be computed.
        ROUGE_SU4: Compute ROUGE-SU4 measures unigram and skip-bigram
        separated by up to four words.
        ROUGE_L: Calculate ROUGE-L.
        stemming: Stem both model and system summaries using Porter stemmer before computing various statistics.
        stopwords: Remove stopwords in model and system summaries before computing various statistics.
        word_level: Evaluate based on words. If False, rouge evaluates the system summary based on bytes.
        length_limit: If you want to limit the length of the system summary, set True.
        length: Limit first N words/bytes of the system summary.
        use_cf: If True, you can use confidence interval to compute.
        cf: Confidence interval (default is 95%)
        scoring_formula: 'average' is calculated by model average. 'best' is calculated by best model.
        resampling: Use bootstrap resampling.
        samples: pecify the number of sampling point in bootstrap resampling (default is 1000).
        favor: If True, set relative importance of ROUGE scores as blow.
        p: Relative importance of recall and precision ROUGE scores. Alpha -> 1 favors precision, Alpha -> 0 favors recall.
        """
        self.n_gram = n_gram
        self.ROUGE_SU4 = ROUGE_SU4
        self.ROUGE_L = ROUGE_L
        self.ROUGE_W = ROUGE_W
        self.ROUGE_W_Weight = ROUGE_W_Weight
        self.stemming = stemming
        self.stopwords = stopwords
        self.length_limit = length_limit
        self.length = length
        self.word_level = word_level
        self.use_cf = use_cf
        self.cf = cf
        self.scoring_formula = scoring_formula
        self.resampling = resampling
        self.samples = samples
        self.favor = favor
        self.p = p


    def setting(self, files=True, summary_path="./", reference_path="./", summary=[], reference=[], delete=True, temp_root=""):
        """
        files: If you've already saved sytem outputs and reference summaries in specific directory, choose 'True'.
               If you evaluate system outputs and summaries as lists of sentences, choose 'False'.
        summary_path & reference_path: If you set files=True, choose each directory path.
        # Directory format sample
        1 system summary and 4 reference summaries.
        - system summary
        ./summary_path/summaryA.txt
        - reference summary
        ./reference_path/summaryA.1.txt
        ./reference_path/summaryA.2.txt
        ./reference_path/summaryA.3.txt
        ./reference_path/summaryA.4.txt
        In first N strings, reference summaries should have same file name as the system output file.
        delete: If True, the rouge setting file(setting.xml) is deleted.
                If False, rouge setting file is saved in current directory.

        If you set files=False, your input format should be as below.
        # summary: double list
        summary = [[summaryA_sent1, summaryA_sent2], [summaryB_sent1, summaryB_sent2]]
        # reference: triple list
        reference = [[[summaryA_ref1_sent1, summaryA_ref1_sent2], [summaryA_ref2_sent1, summaryA_ref2_sent2]],
                     [[summaryB_ref1_sent1, summaryB_ref1_sent2], [summaryB_ref2_sent1, summaryB_ref2_sent2]]
        """
        if not temp_root:
            temp_dir = tempfile.mkdtemp()
        else:
            temp_dir = tempfile.mkdtemp(dir=temp_root)

        # save input lists in temp_dir
        if not files:
            summary_path = os.path.join(temp_dir, "system")
            reference_path = os.path.join(temp_dir, "reference")
            os.mkdir(summary_path)
            os.mkdir(reference_path)
            if len(summary) != len(reference): assert("size of summary and refernece is different.")
            for i, doc in enumerate(summary):
                path = os.path.join(summary_path, "{}.txt".format(i))
                f = open(path, "w")
                for sent in doc:
                    f.write("{}\n".format(sent))
                f.close()
            for j, ref in enumerate(reference):
                for k, doc in enumerate(ref):
                    path = os.path.join(reference_path, "{}_{}.txt".format(j, k))
                    f = open(path, "w")
                    for sent in doc:
                        f.write("{}\n".format(sent))
                    f.close()
        if delete:
            xml_path = os.path.join(temp_dir, "setting.xml")
        else:
            xml_path = "setting.xml"
        xml_file = open("{}".format(xml_path), "w")
        xml_file.write('<ROUGE-EVAL version="1.0">\n')
        for n, sys in enumerate(glob.glob("{}/*".format(summary_path))):
            file_name = os.path.splitext(os.path.basename(path))[0]
            refs  = glob.glob("{}/{}*".format(reference_path, file_name))
            xml_file.write('<EVAL ID="{}">\n'.format(n+1))
            xml_file.write("<MODEL-ROOT>{}</MODEL-ROOT>\n".format(reference_path))
            xml_file.write("<PEER-ROOT>{}</PEER-ROOT>\n".format(summary_path))
            xml_file.write('<INPUT-FORMAT TYPE="SPL">\n"</INPUT-FORMAT>\n')
            xml_file.write("<PEERS>\n")
            xml_file.write('<P ID="{}">{}</P>\n'.format('A', os.path.basename(sys)))
            xml_file.write("</PEERS>\n")
            xml_file.write("<MODELS>\n")
            for path, ids in zip(glob.glob("{}/{}*".format(reference_path, file_name)), ["A", "B", "C", "D", "E", "F", "G"]):
                xml_file.write('<M ID="{}">{}</M>\n'.format(ids, os.path.basename(path)))
            xml_file.write("</MODELS>\n")
            xml_file.write("</EVAL>\n")
        xml_file.write("</ROUGE-EVAL>\n")
        xml_file.close()
        self.temp_dir = temp_dir
        self.setting_file = xml_path
        return xml_path


    def eval_rouge(self, xml_path, recall_only=False, f_measure_only=False, ROUGE_path="./RELEASE-1.5.5/ROUGE-1.5.5.pl", data_path='./RELEASE-1.5.5/data'):
        ROUGE_path = os.path.abspath(ROUGE_path)
        data_path  = os.path.abspath(data_path)
        rouge_cmd  = ['perl', ROUGE_path, "-e", data_path, "-a"]
        if recall_only and f_measure_only:
            assert("choose True in recall_only or f_measure_only, or set both as 'False'")
        if self.n_gram == 0: assert "n-gram should not be less than 1."
        rouge_cmd += "-n {}".format(self.n_gram).split()
        if self.ROUGE_SU4:
            rouge_cmd += "-2 4 -u".split()
        if not self.ROUGE_L:
            rouge_cmd.append("-x")
        if self.ROUGE_W:
            rouge_cmd.append("-w")
            rouge_cmd.append(str(self.ROUGE_W_Weight))
        if self.length_limit:
            if self.length == 0: assert "Length limit should not be less than 1."
            if self.word_level:
                rouge_cmd += "-l {}".format(self.length).split()
            else:
                rouge_cmd += "-b {}".format(self.length).split()
        if self.stemming:
            rouge_cmd.append("-m")
        if self.stopwords:
            rouge_cmd.append("-s")
        if self.use_cf:
            rouge_cmd += "-c {}".format(self.cf).split()
        if self.scoring_formula == "average":
            rouge_cmd += "-f A".split()
        elif self.scoring_formula:
            rouge_cmd += "-f B".split()
        else:
            assert "Choose scoreing formula 'average' or 'best'"
        if self.resampling:
            rouge_cmd += "-r {}".format(self.samples).split()
        if self.favor:
            rouge_cmd += "-p {}".format(self.p).split()
        rouge_cmd.append(xml_path)
        output  = subprocess.check_output(rouge_cmd, stderr=subprocess.STDOUT)
        output  = output.decode("utf-8")
        outputs = output.strip().split("\n")
        result  = dict()
        n = 1
        for line in outputs:
            if self.ROUGE_SU4:
                su_r_match = re.findall('A ROUGE-SU4 Average_R: ([0-9.]+)', line)
                su_p_match = re.findall('A ROUGE-SU4 Average_P: ([0-9.]+)', line)
                su_f_match = re.findall('A ROUGE-SU4 Average_F: ([0-9.]+)', line)
                if su_r_match:
                    if recall_only:
                        result['ROUGE-SU4'] = float(su_r_match[0])
                    elif f_measure_only:
                        pass
                    else:
                        result['ROUGE-SU4-R'] = float(su_r_match[0])
                if not recall_only:
                    if f_measure_only and su_f_match:
                        result['ROUGE-SU4'] = float(su_f_match[0])
                    else:
                        if su_p_match and not f_measure_only:
                            result['ROUGE-SU4-P'] = float(su_p_match[0])
                        elif su_f_match and not f_measure_only:
                            result['ROUGE-SU4-F'] = float(su_f_match[0])
            if self.ROUGE_L:
                l_r_match = re.findall('A ROUGE-L Average_R: ([0-9.]+)', line)
                l_p_match = re.findall('A ROUGE-L Average_P: ([0-9.]+)', line)
                l_f_match = re.findall('A ROUGE-L Average_F: ([0-9.]+)', line)
                if l_r_match:
                    if recall_only:
                        result['ROUGE-L'] = float(l_r_match[0])
                    elif f_measure_only:
                        pass
                    else:
                        result['ROUGE-L-R'] = float(l_r_match[0])
                if not recall_only:
                    if f_measure_only and l_f_match:
                        result['ROUGE-L'] = float(l_f_match[0])
                    else:
                        if l_p_match and not f_measure_only:
                            result['ROUGE-L-P'] = float(l_p_match[0])
                        elif l_f_match and not f_measure_only:
                            result['ROUGE-L-F'] = float(l_f_match[0])
            if self.ROUGE_W:
                w_r_match = re.findall('A ROUGE-W-{} Average_R: ([0-9.]+)'.format(self.ROUGE_W_Weight), line)
                w_p_match = re.findall('A ROUGE-W-{} Average_P: ([0-9.]+)'.format(self.ROUGE_W_Weight), line)
                w_f_match = re.findall('A ROUGE-W-{} Average_F: ([0-9.]+)'.format(self.ROUGE_W_Weight), line)
                if w_r_match:
                    if recall_only:
                        result['ROUGE-W-{}'.format(self.ROUGE_W_Weight)] = float(w_r_match[0])
                    elif f_measure_only:
                        pass
                    else:
                        result['ROUGE-W-{}-R'.format(self.ROUGE_W_Weight)] = float(w_r_match[0])
                if not recall_only:
                    if f_measure_only and w_f_match:
                        result['ROUGE-W-{}'.format(self.ROUGE_W_Weight)] = float(w_f_match[0])
                    else:
                        if w_p_match and not f_measure_only:
                            result['ROUGE-W-{}-P'.format(self.ROUGE_W_Weight)] = float(w_p_match[0])
                        elif w_f_match and not f_measure_only:
                            result['ROUGE-W-{}-F'.format(self.ROUGE_W_Weight)] = float(w_f_match[0])
            r_match = re.findall('A ROUGE-{} Average_R: ([0-9.]+)'.format(n), line)
            p_match = re.findall('A ROUGE-{} Average_P: ([0-9.]+)'.format(n), line)
            f_match = re.findall('A ROUGE-{} Average_F: ([0-9.]+)'.format(n), line)
            if r_match:
                if recall_only:
                    result['ROUGE-{}'.format(n)] = float(r_match[0])
                elif f_measure_only:
                    pass
                else:
                    result['ROUGE-{}-R'.format(n)] = float(r_match[0])
            if not recall_only:
                if f_measure_only and f_match:
                    result['ROUGE-{}'.format(n)] = float(f_match[0])
                else:
                    if p_match and not f_measure_only:
                        result['ROUGE-{}-P'.format(n)] = float(p_match[0])
                    elif f_match and not f_measure_only:
                        result['ROUGE-{}-F'.format(n)] = float(f_match[0])
            if f_match: n += 1
        shutil.rmtree(self.temp_dir)
        return result
