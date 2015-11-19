# pythonrouge
This is the python script to use ROUGE, summarization evaluation toolkit.
  
In this implementation, you can evaluate ROUGE-1, ROUGE-2, ROUGE-3, and ROUGE-SU4. You can evaluate your model summary with a peer summary right now. It's not necessary to make an xml file as in the general ROUGE package.

Any feedbacks or comments are welcome.

# Usage

The only things you need to evaluate ROUGE score is to specify the paths of ROUGE-1.5.5.pl and RELEASE-1.5.5/data in this package.

```
from pythonrouge import pythonrouge

ROUGE = sys.argv[1] #ROUGE-1.5.5.pl
data_path = sys.argv[2] #data folder in RELEASE-1.5.5
peer = " Tokyo is the one of the biggest city in the world."
model = "The capital of Japan, Tokyo, is the center of Japanese economy."
score = pythonrouge.pythonrouge(ROUGE, data_path, model, peer)
print(score)
```

The output will be below. For convenience, only f_score will be output.

```
{'rouge-1': 0.45455, 'rouge-2': 0.2, 'rouge-3': 0.11111, 'rouge-su4': 0.14545}
```
