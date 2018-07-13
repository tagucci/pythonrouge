# -*- coding: utf-8 -*-
from __future__ import print_function
from pythonrouge.pythonrouge import Pythonrouge
from pprint import pprint

if __name__ == '__main__':
    summary = './sample/summary/'
    reference = './sample/reference/'
    print('evaluate sumamry & reference in these dirs')
    print('summary:\t{}\nreference:\t{}'.format(summary, reference))
    rouge = Pythonrouge(summary_file_exist=True,
                        peer_path=summary, model_path=reference,
                        n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                        recall_only=False, f_measure_only=False,
                        stemming=True, stopwords=True,
                        word_level=True, length_limit=True, length=50,
                        use_cf=True, cf=95, scoring_formula='average',
                        resampling=True, samples=1000, favor=True, p=0.5)
    score = rouge.calc_score()
    print('ROUGE-N(1-2) & SU4 recall & f-measure with confidence interval')
    pprint(score)
    print('Evaluate ROUGE based on sentecnce lists')
    """
    ROUGE evaluates all system summaries and its corresponding reference
    a summary or summaries at onece.
    Summary should be double list, in each list has each summary.
    Reference summaries should be triple list because some of reference
    has multiple gold summaries.
    """
    summary = [["Great location, very good selection of food for\
                 breakfast buffet.",
                "Stunning food, amazing service.",
                "The food is excellent and the service great."],
               ["The keyboard, more than 90% standard size, is just\
                 large enough .",
                "Surprisingly readable screen for the size .",
                "Smaller size videos   play even smoother ."]]
    reference = [
                 [["Food was excellent with a wide range of choices and\
                   good services.", "It was a bit expensive though."],
                  ["Food can be a little bit overpriced, but is good for\
                  hotel."],
                  ["The food in the hotel was a little over priced but\
                  excellent in taste and choice.",
                  "There were also many choices to eat in the near\
                  vicinity of the hotel."]],
                 [["The size is great and allows for excellent\
                   portability.",
                   "Makes it exceptionally easy to tote around, and the\
                   keyboard is fairly big considering the size of this\
                   netbook."],
                  ["Size is small and manageable.",
                   "Perfect size and weight.",
                   "Great size for travel."],
                  ["The keyboard is a decent size, a bit smaller then\
                  average but good.",
                  "The laptop itself is small but big enough do do\
                  things on it."],
                  ["In spite of being small it is still comfortable.",
                  "The screen and keyboard are well sized for use"]]
                  ]
    rouge = Pythonrouge(summary_file_exist=False,
                        summary=summary, reference=reference,
                        n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                        recall_only=True, stemming=True, stopwords=True,
                        word_level=True, length_limit=True, length=50,
                        use_cf=True, cf=95, scoring_formula='average',
                        resampling=True, samples=1000, favor=True, p=0.5)
    score = rouge.calc_score()
    print('ROUGE-N(1-2) & SU4 recall only with confidence interval')
    pprint(score)
