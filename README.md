# pythonrouge
This is the python script to use ROUGE, summarization evaluation toolkit.

In this implementation, you can evaluate various types of ROUGE metrics. You can evaluate your system summaries with reference summaries right now. It's not necessary to make an xml file as in the general ROUGE package. However, you can evaluate ROUGE scores in a standard way if you saved system summaries and reference summaries in specific directories. In document summarization research, recall or F-measure of ROUGE metrics is used in most cases. So you can choose only recall or F-measure of ROUGE evaluation result for convenience.

Any feedbacks or comments are welcome.

# Install
You can install pythonrouge in both ways

```
# not using pip
python setup.py install

# using pip
pip install git+https://github.com/tagucci/pythonrouge.git
```
Then, you can use pythonrouge. If you don't have ROUGE package, I recommend you clone this repository to your local, and do "python setup.py install".

# Usage

The only things you need to evaluate ROUGE score is to specify the paths of ROUGE-1.5.5.pl and RELEASE-1.5.5/data in this package.

```
from pythonrouge.pythonrouge import Pythonrouge

ROUGE = sys.argv[1] #ROUGE-1.5.5.pl
data_path = sys.argv[2] #data folder in RELEASE-1.5.5

# initialize setting of ROUGE, eval ROUGE-1, 2, SU4, L
rouge = Pythonrouge(n_gram=2, ROUGE_SU4=True, ROUGE_L=True, stemming=True, stopwords=True, word_level=True, length_limit=True, length=50, use_cf=False, cf=95, scoring_formula="average", resampling=True, samples=1000, favor=True, p=0.5)

# system summary & reference summary
summary = [[" Tokyo is the one of the biggest city in the world."]]
reference = [[["The capital of Japan, Tokyo, is the center of Japanese economy."]]]

# If you evaluate ROUGE by sentence list as above, set files=False
setting_file = rouge.setting(files=False, summary=summary, reference=reference)

# If you need only recall of ROUGE metrics, set recall_only=True
result = rouge.eval_rouge(setting_file, recall_only=True, ROUGE_path=ROUGE_path, data_path=data_path)
print(result)
```

The output will be below. In this case, only recall metrics of ROUGE is printed.

```
{'ROUGE-1': 0.16667, 'ROUGE-2': 0.0, 'ROUGE-L': 0.16667, 'ROUGE-SU4': 0.05}
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
```

After putting system/reference files as above, you can evaluate ROUGE metrics as blow.

```
from pythonrouge.pythonrouge import Pythonrouge

ROUGE = sys.argv[1] #ROUGE-1.5.5.pl
data_path = sys.argv[2] #data folder in RELEASE-1.5.5

# initialize setting of ROUGE, eval ROUGE-1~4, SU4
rouge = Pythonrouge(n_gram=4, ROUGE_SU4=True, ROUGE_L=True, stemming=True, stopwords=True, word_level=True, length_limit=True, length=50, use_cf=False, cf=95, scoring_formula="average", resampling=True, samples=1000, favor=True, p=0.5)

# make a setting file, set files=True because you've already save files in specific directories
setting_file = rouge.setting(files=True, summary_path=summary_dir, reference_path=reference_dir)

# If you need only F-measure of ROUGE metrics, set f_measure_only=True
result = rouge.eval_rouge(setting_file, ROUGE_path=ROUGE_path, data_path=data_path)
print(result)
> {ROUGE-1': 0.29836, 'ROUGE-2': 0.07059, 'ROUGE-3': 0.03896, ', 'ROUGE-4': 0.02899, 'ROUGE-SU4': 0.12444}
```



# Error Handling
If you encounter following error message when you use pythonrouge

```
Cannot open exception db file for reading: /home/pythonrouge/pythonrouge/RELEASE-1.5.5/data/WordNet-2.0.exc.db
```

you can run pythonrouge by doing following.

```
cd pythonrouge/RELEASE-1.5.5/data/
rm WordNet-2.0.exc.db
./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db
```
