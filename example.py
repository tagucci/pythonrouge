# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from pythonrouge import pythonrouge

if __name__ == '__main__':
    ROUGE = sys.argv[1]
    data_path = sys.argv[2]
    peer = " Tokyo is the one of the biggest city in the world."
    model = "The capital of Japan, Tokyo, is the center of Japanese economy."
    print("Peer summary: ", peer)
    print("Model summary: ", model)
    score = pythonrouge.pythonrouge(ROUGE, data_path, model, peer)
    print(score)
    print("ROUGE-1: {0}\nROUGE-2: {1}\nROUGE-3: {2}\nROUGE-SU4: {3}".format(
        score["rouge-1"], score["rouge-2"], score["rouge-3"], score["rouge-su4"]))