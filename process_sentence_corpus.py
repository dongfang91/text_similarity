from sentence_transformers import SentenceTransformer, models
import argparse
import read_files as read
import os

def main(model_path, model_type, sentence_corpus, output_path):

    #### Read sentence courpus.  output: list of sentences ####
    sentences = read.read_from_tsv(os.path.join(sentence_corpus , "input.tsv"))
    sentences = [item for row in sentences for item in row]
    print(sentences[:10])

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

    sentences_embedding = embedder.encode(sentences)

    read.save_in_pickle(os.path.join(output_path,"embeddings.pkl"),sentences_embedding)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sentence embedding for each sentence in the sentence corpus ')

    parser.add_argument('-model',
                        help='the direcotory of the model',required= True)

    parser.add_argument('-model_type',
                        help='the type of the model, sentence_bert or just bert',required= True)

    parser.add_argument('-sentences',
                        help='the direcotory of the sentence corpus',required=True)

    parser.add_argument('-output',
                        help='the direcotory of the sentence corpus',required=True)

    args = parser.parse_args()
    model_path = args.model
    model_type = args.model_type
    sentence_corpus = args.sentences
    output_path = args.output

    main(model_path, model_type, sentence_corpus, output_path)