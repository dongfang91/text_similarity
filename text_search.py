"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from sentence_transformers import SentenceTransformer
import scipy.spatial
import argparse
import read_files as read
import os


def main(model, sentence_corpus, query):

    embedder = SentenceTransformer(model)
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

    parser.add_argument('-embeddings',
                        help='the direcotory of the sentence embeddings',required=True)

    parser.add_argument('-query',
                        help='output path for the sentence embeddings',required=True)

    args = parser.parse_args()
    model_path = args.model
    corpus_embedding = args.embeddings
    query = args.query

    main(model_path,corpus_embedding,query)