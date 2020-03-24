"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from sentence_transformers import SentenceTransformer, models
import scipy.spatial
import argparse
import read_files as read
import os


def main(model_path, model_type,sentence_corpus, query):
    if model_type.lower() in ["bert"]:
        word_embedding_model = models.BERT(model_path)

        # Apply mean pooling to get one fixed sized sentence vector
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True,
                                       pooling_mode_cls_token=False,
                                       pooling_mode_max_tokens=False)

        embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        #### load sentence BERT models and generate sentence embeddings ####
    else:
        #### load sentence BERT models and generate sentence embeddings ####
        embedder = SentenceTransformer(model_path)
    corpus_embeddings = read.read_from_pickle(os.path.join(sentence_corpus, "embeddings.pkl"))
    corpus = read.read_from_tsv(os.path.join(sentence_corpus , "input.tsv"))
    sentences = [item for row in corpus for item in row]

    query_embedding = embedder.encode([query])

    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    closest_n = 5

    distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]


    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for idx, distance in results[0:closest_n]:
        print(sentences[idx].strip(), "(Score: %.4f)" % (1 - distance))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sentence embedding for each sentence in the sentence corpus ')

    parser.add_argument('-model',
                        help='the direcotory of the model',required= True)

    parser.add_argument('-model_type',
                        help='the type of the model, sentence_bert or just bert',required= True)

    parser.add_argument('-embeddings',
                        help='the direcotory of the sentence embeddings',required=True)

    parser.add_argument('-query',
                        help='output path for the sentence embeddings',required=True)

    args = parser.parse_args()
    model_path = args.model
    model_type = args.model_type
    corpus_embedding = args.embeddings
    query = args.query

    main(model_path, model_type, corpus_embedding,query)