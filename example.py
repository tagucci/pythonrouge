# -*- coding: utf-8 -*-

import sys
from pythonrouge import pythonrouge

if __name__ == '__main__':
    ROUGE = sys.argv[1]
    data_path = sys.argv[2]
    ref = "Kyoto is a nice place"
    guess = "Tokyo is a nice place"
    print("correct:", ref)
    print("guess A: ",guess)
    score = pythonrouge.pythonrouge(ROUGE, data_path, guess, ref)
    print(score)
    print(ref)
    print(guess)

    print("ROUGE-1:", score["rouge-1"])
    print("ROUGE-2:", score["rouge-2"])
    print("ROUGE-3:", score["rouge-3"])
    print("ROUGE-SU4:", score["rouge-su4"])
    




