# pythonrouge
This is the python wrapper to use ROUGE, summarization evaluation toolkit.

In this implementation, you can evaluate various types of ROUGE metrics. You can evaluate your system summaries with reference summaries right now. It's not necessary to make an xml file as in the general ROUGE package. However, you can evaluate ROUGE scores in a standard way if you saved system summaries and reference summaries in specific directories. In the document summarization research, recall or F-measure of ROUGE metrics is used in most cases. So you can choose either recall or F-measure or both of these of ROUGE evaluation result for convenience.

Any feedbacks or comments are welcome.

# Install
You can install pythonrouge in both ways

```
# not using pip
git clone https://github.com/tagucci/pythonrouge.git
python setup.py install

# using pip
pip install git+https://github.com/tagucci/pythonrouge.git
```
Then, you can use pythonrouge.

# Usage

The only things you need to evaluate ROUGE score is to specify the paths of ROUGE-1.5.5.pl and RELEASE-1.5.5/data in this package.

```
from pythonrouge.pythonrouge import Pythonrouge

# system summary(predict) & reference summary
summary = [[" Tokyo is the one of the biggest city in the world."]]
reference = [[["The capital of Japan, Tokyo, is the center of Japanese economy."]]]

# initialize setting of ROUGE to eval ROUGE-1, 2, SU4
# if you evaluate ROUGE by sentence list as above, set summary_file_exist=False
# if recall_only=True, you can get recall scores of ROUGE
rouge = Pythonrouge(summary_file_exist=False,
                    summary=summary, reference=reference,
                    n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                    recall_only=True, stemming=True, stopwords=True,
                    word_level=True, length_limit=True, length=50,
                    use_cf=False, cf=95, scoring_formula='average',
                    resampling=True, samples=1000, favor=True, p=0.5)
score = rouge.calc_score()
print(score)
```

The output will be below. In this case, only recall metrics of ROUGE is printed.

```
{'ROUGE-1': 0.16667, 'ROUGE-2': 0.0, 'ROUGE-SU4': 0.05}
```

You can also evaluate ROUGE scripts in a standard way.
In this case, your directory format of system/reference summary directory should be as below.

```
# Directory format sample
1 system summary and 4 reference summaries.
- system summary
./summary_path/summaryA.txt

- reference summary
./reference_path/summaryA.1.txt
./reference_path/summaryA.2.txt
./reference_path/summaryA.3.txt
./reference_path/summaryA.4.txt

File name of reference summaries should be same as the system summary.
In this case, system file is "summaryA.txt" and reference files should have "summaryA" in file names.

# Name Rule
- system summary
{NAME}.txt

- reference summary
{NAME}.{SUMMARY_ID}.txt

In system and reference summary, {NAME} should be same as an above sample.
If there are 4 gold summaries, {SUMMARY_ID} is [1, 2, 3, 4].
```

After putting system/reference files as above, you can evaluate ROUGE metrics as blow.

```
from pythonrouge.pythonrouge import Pythonrouge

# initialize setting of ROUGE, eval ROUGE-1, 2, SU4
# if summary_file_exis=True, you should specify system summary(peer_path) and reference summary(model_path) paths
rouge = Pythonrouge(summary_file_exist=True,
                    peer_path=summary, model_path=reference,
                    n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                    recall_only=True,
                    stemming=True, stopwords=True,
                    word_level=True, length_limit=True, length=50,
                    use_cf=False, cf=95, scoring_formula='average',
                    resampling=True, samples=1000, favor=True, p=0.5)
```


# Error Handling
If you encounter following error message when you use pythonrouge

```
Cannot open exception db file for reading: /home/pythonrouge/pythonrouge/RELEASE-1.5.5/data/WordNet-2.0.exc.db
```

you can run pythonrouge by doing following.

```
# move to pythonrouge dir you've installed
cd pythonrouge/RELEASE-1.5.5/data/
rm WordNet-2.0.exc.db # only if exist
cd WordNet-2.0-Exceptions
rm WordNet-2.0.exc.db # only if exist
./buildExeptionDB.pl . exc WordNet-2.0.exc.db
cd ../
ln -s WordNet-2.0-Exceptions/WordNet-2.0.exc.db WordNet-2.0.exc.db
```
