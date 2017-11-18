# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
from pythonrouge.pythonrouge import Pythonrouge
from pprint import pprint


def word2ids(summary, reference):
    id_dict = defaultdict(lambda: len(id_dict))
    summary = [[' '.join([str(id_dict[w]) for w in sent.split()])
                for sent in doc] for doc in summary]
    reference = [[[' '.join([str(id_dict[w]) for w in sent.split()])
                   for sent in doc] for doc in refs] for refs in reference]
    return summary, reference


if __name__ == '__main__':
    # prediction
    summary = [  # 1st summary
               ["現在　の　東京　の　天気　は　曇り　です　。",
                "明日　の　予報　は　晴れ　のち　曇り　です　。"],
                 # 2nd summary
               ["奈良　の　観光　名所　は　奈良公園　。",
                "奈良　の　鹿　は　凶暴　で　ある　。"]]
    # gold summary
    reference = [  # 1st gold summary (there are 2 gold summaries)
                 [["今日　の　東京　は　曇り　で 、 明日　は　晴れる　でしょ　う　。"],
                  ["現在　の　東京　の　気候　は　雨　です　。",
                   "明日　の　天気　は　晴れ　のち　曇り　です　。"]],
                   # 2nd gold summary (there are 1 gold summaries)
                 [["奈良　と　いえば　奈良公園　。",
                   "奈良　の　鹿　は　本当に　穏やか　。"]]
                 ]
    summary, reference = word2ids(summary, reference)
    rouge = Pythonrouge(summary_file_exist=False,
                        summary=summary, reference=reference,
                        n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                        recall_only=True)
    score = rouge.calc_score()
    print('ROUGE-N(1-2) & SU4 recall only')
    pprint(score)
