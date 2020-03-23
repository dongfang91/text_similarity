from sentence_transformers import SentenceTransformer
import argparse
import read_files as read
import os

def main(model_path, sentence_corpus):

    #### Read sentence courpus.  output: list of sentences ####
    sentences = read.read_from_tsv(os.path.join(sentence_corpus , "input.tsv"))
    sentences = [item for row in sentences for item in row]
    print(sentences[:10])

    #### load sentence BERT models and generate sentence embeddings ####
    embedder = SentenceTransformer(model_path)
    sentences_embedding = embedder.encode(sentences)

    read.save_in_pickle(os.path.join(sentence_corpus,"embeddings.pkl"),sentences_embedding)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sentence embedding for each sentence in the sentence corpus ')

    parser.add_argument('-model',
                        help='the direcotory of the model',required= True)

    parser.add_argument('-sentences',
                        help='the direcotory of the sentence corpus',required=True)

    args = parser.parse_args()
    model_path = args.model
    sentence_corpus = args.sentences

    main(model_path,sentence_corpus)