# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from pythonrouge import pythonrouge

if __name__ == '__main__':
    peer = " Tokyo is the one of the biggest city in the world."
    model = "The capital of Japan, Tokyo, is the center of Japanese economy."
    print("Peer summary: ", peer)
    print("Model summary: ", model)
    score = pythonrouge.pythonrouge(peer, model)
    print("ROUGE-1: {0}\nROUGE-2: {1}\nROUGE-3: {2}\nROUGE-SU4: {3}\nROUGE-L: {4}".format(
        score["ROUGE-1"], score["ROUGE-2"], score["ROUGE-3"], score["ROUGE-SU4"], score["ROUGE-L"]))

