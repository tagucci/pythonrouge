# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import basename
from re import findall
from glob import glob
from tempfile import mkdtemp
import subprocess
import shutil
ROUGE_path = os.path.join("/".join(os.path.abspath(__file__).split("/")[:-1]) +
                          "/RELEASE-1.5.5/ROUGE-1.5.5.pl")
data_path = os.path.join("/".join(os.path.abspath(__file__).split("/")[:-1]) +
                         "/RELEASE-1.5.5/data")


class Pythonrouge:
    def __init__(self, summary_file_exist=True, summary=None, reference=None,
                 delete_xml=True, xml_dir='/tmp/',
                 recall_only=False, f_measure_only=False,
                 peer_path='/tmp/', model_path='/tmp/',
                 n_gram=2, ROUGE_SU4=True, ROUGE_L=False, ROUGE_W=False,
                 ROUGE_W_Weight=1.2, stemming=True, stopwords=False,
                 word_level=True, length_limit=True, length=100, use_cf=False,
                 cf=95, scoring_formula="average", resampling=True,
                 samples=1000, favor=True, p=0.5):
        """
        n_gram: Compute ROUGE-N up to max-ngram length will be computed.
        ROUGE_SU4: Compute ROUGE-SU4 measures unigram and skip-bigram
        separated by up to four words.
        ROUGE_L: Calculate ROUGE-L.
        stemming: Stem both model and system summaries using Porter stemmer
                  before computing various statistics.
        stopwords: Remove stopwords in model and system summaries before
                   computing various statistics.
        word_level: Evaluate based on words. If False, rouge evaluates the
                    system summary based on bytes.
        length_limit: If you want to limit the length of the system summary,
                      set True.
        length: Limit first N words/bytes of the system summary.
        use_cf: If True, you can use confidence interval to compute.
        cf: Confidence interval (default is 95%)
        scoring_formula: 'average' is calculated by model average. 'best' is
                         calculated by best model.
        resampling: Use bootstrap resampling.
        samples: pecify the number of sampling point in bootstrap resampling
                 (default is 1000).
        favor: If True, set relative importance of ROUGE scores as blow.
        p: Relative importance of recall and precision ROUGE scores.
           Alpha -> 1 favors precision, Alpha -> 0 favors recall.

        ### Summary Files ###
        peer_path & model_path: If summary_file_exist=True,
                                choose each directory path.
        files: If you've already saved sytem outputs and reference summaries
               in specific directory, choose 'True'.
               If you evaluate system outputs and summaries as lists of
               sentences, choose 'False'.
        # Directory format sample
        1 system summary and 4 reference summaries.
        - system summary(peer_path)
        ./summary_path/summaryA.txt
        - reference summary(model_path)
        ./reference_path/summaryA.1.txt
        ./reference_path/summaryA.2.txt
        ./reference_path/summaryA.3.txt
        ./reference_path/summaryA.4.txt
        In first N strings, reference summaries should have same file name
        as the system output file.
        delete: If True, the rouge setting file(setting.xml) is deleted.
                If False, rouge setting file is saved in current directory.

        If summary_file_exist=False, your input format should be as below.
        # summary: double list
        summary = [[summaryA_sent1, summaryA_sent2],
                   [summaryB_sent1, summaryB_sent2]]
        # reference: triple list
        reference = [[[summaryA_ref1_sent1, summaryA_ref1_sent2],
                     [summaryA_ref2_sent1, summaryA_ref2_sent2]],
                     [[summaryB_ref1_sent1, summaryB_ref1_sent2],
                     [summaryB_ref2_sent1, summaryB_ref2_sent2]]
        """
        # system output summary and reference summary
        self.summary = summary
        self.reference = reference
        # ROUGE path
        self.ROUGE_path = ROUGE_path
        self.data_path = data_path
        # peer/model path
        self.peer_path = peer_path
        self.model_path = model_path
        self.summary_file_exist = summary_file_exist
        self.delete_xml = delete_xml
        self.xml_dir = xml_dir
        # evaluation parameter - you can check details of below in ROUGE
        # directory pythonrouge/RELEASE-1.5.5/README.txt
        self.n_gram = n_gram
        self.ROUGE_SU4 = ROUGE_SU4
        self.ROUGE_L = ROUGE_L
        self.ROUGE_W = ROUGE_W
        self.W_Weight = ROUGE_W_Weight
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
        # evaluation outputs
        self.recall_only = recall_only
        self.f_measure_only = f_measure_only
        # check size of system/reference summary length
        if not summary_file_exist and len(self.summary) != len(self.reference):
            assert('size of summary and refernece is different.')

        # check output ROUGE types
        if self.recall_only and self.f_measure_only:
            assert("choose True in recall_only or f_measure_only,\
                    or set both as 'False'")

        # check n-gram of ROUGE
        if self.n_gram == 0:
            assert 'n-gram should not be less than 1.'

        # check the length of lenght limit
        if self.length_limit and self.length == 0:
            assert 'Length limit should not be less than 1.'

        # check scoreing formula: best/average
        if self.scoring_formula != 'best' or self.scoring_formula == 'average':
            assert 'Choose scoreing formula "average" or "best"'

    def make_xml(self):
        if not self.xml_dir:
            tmp_dir = mkdtemp()
        else:
            tmp_dir = mkdtemp(dir=self.xml_dir)

        # save summaries in tmp_dir
        if not self.summary_file_exist:
            self.peer_path = os.path.join(tmp_dir, 'system')
            self.model_path = os.path.join(tmp_dir, 'reference')
            os.mkdir(self.peer_path)
            os.mkdir(self.model_path)

            # save system summaries in tmp_dir
            for i, doc in enumerate(self.summary):
                path = os.path.join(self.peer_path, '{}.txt'.format(i))
                with open(path, 'w') as f:
                    for sent in doc:
                        f.write('{}\n'.format(sent))

            # save reference summaries in tmp_dir
            for j, ref in enumerate(self.reference):
                for k, doc in enumerate(ref):
                    path = os.path.join(self.model_path,
                                        '{}.{}.txt'.format(j, k))
                    with open(path, 'w') as f:
                        for sent in doc:
                            f.write("{}\n".format(sent))

        # set xml setting file path
        xml_path = os.path.join(tmp_dir, 'setting.xml')
        if not self.delete_xml:
            print('setting file is saved at {}'.format(xml_path))

        # write system/summary path to xml
        xml = open('{}'.format(xml_path), 'w')
        xml.write('<ROUGE-EVAL version="1.0">\n')
        for n, peer in enumerate(glob("{}/*".format(self.peer_path))):
            file_name = os.path.splitext(os.path.basename(peer))[0]
            xml.write('<EVAL ID="{}">\n'.format(n + 1))
            xml.write('<MODEL-ROOT>{}</MODEL-ROOT>\n'.format(self.model_path))
            xml.write('<PEER-ROOT>{}</PEER-ROOT>\n'.format(self.peer_path))
            xml.write('<INPUT-FORMAT TYPE="SPL">\n"</INPUT-FORMAT>\n')
            xml.write('<PEERS>\n')
            xml.write('<P ID="{}">{}</P>\n'.format('A', basename(peer)))
            xml.write('</PEERS>\n')
            xml.write('<MODELS>\n')
            model_paths = glob('{}/{}.*'.format(self.model_path, file_name))
            for path, ids in zip(model_paths,
                                 [i for i in range(len(model_paths))]):
                xml.write('<M ID="{}">{}</M>\n'.format(ids, basename(path)))
            xml.write('</MODELS>\n')
            xml.write('</EVAL>\n')
        xml.write('</ROUGE-EVAL>\n')
        xml.close()
        self.tmp_dir = tmp_dir
        self.setting_file = xml_path

    def set_command(self):
        self.make_xml()
        rouge_cmd = ['perl', self.ROUGE_path, "-e", self.data_path, "-a"]
        rouge_cmd += '-n {}'.format(self.n_gram).split()
        # ROUGE-SU4
        if self.ROUGE_SU4:
            rouge_cmd += '-2 4 -u'.split()

        # ROUGE-L
        if not self.ROUGE_L:
            rouge_cmd.append('-x')

        # ROUGE-W
        if self.ROUGE_W:
            rouge_cmd.append('-w')
            rouge_cmd.append(str(self.W_Weight))

        # set length limit
        if self.length_limit:
            # word level length limit
            if self.word_level:
                rouge_cmd += '-l {}'.format(self.length).split()

            # bytes level length limit
            else:
                rouge_cmd += '-b {}'.format(self.length).split()

        # stemming
        if self.stemming:
            rouge_cmd.append('-m')

        # stopwords
        if self.stopwords:
            rouge_cmd.append('-s')

        # confidence interval
        if self.use_cf:
            rouge_cmd += '-c {}'.format(self.cf).split()

        # scoring based on averaging scores
        if self.scoring_formula == 'average':
            rouge_cmd += '-f A'.split()

        # scoring based on best scores
        elif self.scoring_formula:
            rouge_cmd += '-f B'.split()

        # the number of sampling point in bootstrap resampling
        if self.resampling:
            rouge_cmd += '-r {}'.format(self.samples).split()

        # relative importance of recall and precision ROUGE scores
        if self.favor:
            rouge_cmd += '-p {}'.format(self.p).split()

        rouge_cmd.append(self.setting_file)
        return rouge_cmd

    def parse_output(self, lines):
        result = dict()
        n = 1
        for l in lines:
            # find ROUGE-N
            r_match = findall('A ROUGE-{} Average_R: ([0-9.]+)'.format(n), l)
            f_match = findall('A ROUGE-{} Average_F: ([0-9.]+)'.format(n), l)

            # ROUGE-N recall
            if self.recall_only and r_match:
                result['ROUGE-{}'.format(n)] = float(r_match[0])
            elif r_match and not self.f_measure_only:
                result['ROUGE-{}-R'.format(n)] = float(r_match[0])

            # ROUGE-N F-measure
            if self.f_measure_only and f_match:
                result['ROUGE-{}'.format(n)] = float(f_match[0])
            elif f_match and not self.recall_only:
                result['ROUGE-{}-F'.format(n)] = float(f_match[0])

            # count up ROUGE-N
            if f_match:
                n += 1

            # find ROUGE-SU4
            su_r_match = findall('A ROUGE-SU4 Average_R: ([0-9.]+)', l)
            su_f_match = findall('A ROUGE-SU4 Average_F: ([0-9.]+)', l)

            # ROUGE-SU4 Recall
            if self.recall_only and su_r_match:
                result['ROUGE-SU4'] = float(su_r_match[0])
            elif su_r_match and not self.f_measure_only:
                result['ROUGE-SU4-R'] = float(su_r_match[0])

            # ROUGE-SU4 F-measure
            if self.f_measure_only and su_f_match:
                result['ROUGE-SU4'] = float(su_f_match[0])
            elif su_f_match and not self.recall_only:
                result['ROUGE-SU4-F'] = float(su_f_match[0])

            # find ROUGE-L
            l_r_match = findall('A ROUGE-L Average_R: ([0-9.]+)', l)
            l_f_match = findall('A ROUGE-L Average_F: ([0-9.]+)', l)

            # ROUGE-L Recall
            if self.recall_only and l_r_match:
                result['ROUGE-L'] = float(l_r_match[0])
            elif l_r_match and not self.f_measure_only:
                result['ROUGE-L-R'] = float(l_r_match[0])

            # ROUGE-L F-measure
            if self.f_measure_only and l_f_match:
                result['ROUGE-L'] = float(l_f_match[0])
            elif l_f_match and not self.recall_only:
                result['ROUGE-L-F'] = float(l_f_match[0])

            # find ROUGE-W
            w_r_match = findall(
                'A ROUGE-W-{} Average_R: ([0-9.]+)'.format(self.W_Weight), l)
            w_f_match = findall(
                'A ROUGE-W-{} Average_F: ([0-9.]+)'.format(self.W_Weight), l)

            # ROUGE-W recall
            if self.recall_only and w_r_match:
                result['ROUGE-W-{}'.format(self.W_Weight)
                       ] = float(w_r_match[0])
            elif w_r_match and not self.f_measure_only:
                result['ROUGE-W-{}-R'.format(self.W_Weight)
                       ] = float(w_r_match[0])

            # ROUGE-W F-measure
            if self.f_measure_only and w_f_match:
                result['ROUGE-W-{}'.format(self.W_Weight)
                       ] = float(w_f_match[0])
            elif w_f_match and not self.recall_only:
                result['ROUGE-W-{}-F'.format(self.W_Weight)
                       ] = float(w_f_match[0])
        return result

    def calc_score(self):
        rouge_cmd = self.set_command()
        output = subprocess.check_output(rouge_cmd, stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        output = output.strip().split('\n')
        result = self.parse_output(output)
        if self.delete_xml:
            shutil.rmtree(self.tmp_dir)
        return result
