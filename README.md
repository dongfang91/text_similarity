# text_similarity
Text similarity using BERT sentence embeddings.


This repository is based on the [Sentence Transformers](https://github.com/UKPLab/sentence-transformers), a repository fine-tunes BERT / RoBERTa / DistilBERT / ALBERT / XLNet with a siamese or triplet network structure to produce semantically meaningful sentence embeddings that can be used in unsupervised scenarios: Semantic textual similarity via cosine-similarity, clustering, semantic search. There are multiple different others [sentence-BERT models](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/).


## Setup
We recommend Python 3.6 or higher. The model is implemented with PyTorch (at least 1.0.1) using [transformers v2.3.0](https://github.com/huggingface/transformers).
The code does **not** work with Python 2.7.

**With pip**

Install the model with `pip`:
```
pip install -U sentence-transformers
```


## Getting Started

### Dataset
First, the sentence corpus should be downloaded and saved in the directory "data/sentence_corpus/". Please look at the format of the example file "data/sentence_corpus/input.tsv", each row of this tsv file is one sentence. 

### Model
Second, the model should be downloaded ([sentence-BERT models](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/)) and saved in the directory "./model/". In this repository, we use the "roberta-base-nli-mean-tokens" as one example.

### Generate sentence embeddings for every sentence in the corpus
Generate sentence embeddings and save them as pickle files.

```
python process_sentence_corpus.py -model model/roberta-base-nli-mean-tokens -model_type sentence_bert -sentences data/sentence_corpus/example.tsv -output data/output/
```

### Search most similar sentences in the corpus for the query 
Find the 5 most similar sentence for the query

```
python text_search.py -model model/roberta-base-nli-mean-tokens -model_type sentence_bert -embeddings data/output/ -query "I like eatting apples."
```

## Customize the sentence-BERT models
Further train the sentence-BERT models on extra datasets. **GPU resources are required.**

### Collect domain-specific dataset
Collec the extra dataset and save them into "data/extra_dataset/train.tsv" and "data/extra_dataset/train.tsv". Each row of the train.tsv file is one training example with the format of "$sentence1, $most_similar_sentence_for sentence1, $irrelevant_sentence_for_sentence1".

### Hyper-parameters tunning
Currently, the default hyper-parameters are fixed and saved in "continue_training.conf"

### Continue training the sentence-BERT model on domain-specific dataset

```
python continue_training_models.py -model model/roberta-base-nli-mean-tokens -extra_dataset data/extra_dataset
```


