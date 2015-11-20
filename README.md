# pythonrouge
This is the python script to use ROUGE, summarization evaluation toolkit.
  
In this implementation, you can evaluate ROUGE-1, ROUGE-2, ROUGE-3, and ROUGE-SU4. You can evaluate your model summary with a peer summary right now. It's not necessary to make an xml file as in the general ROUGE package.

Any feedbacks or comments are welcome.

# Install
```
python setup.py install
```
Then, you can use pythonrouge.

# Usage

```
from pythonrouge import pythonrouge

peer = " Tokyo is the one of the biggest city in the world."
model = "The capital of Japan, Tokyo, is the center of Japanese economy."
score = pythonrouge.pythonrouge(peer, model)
print(score)
```

The output will be below. For convenience, only f_score will be output.

```
{'rouge-1': 0.45455, 'rouge-2': 0.2, 'rouge-3': 0.11111, 'rouge-su4': 0.14545}
```
