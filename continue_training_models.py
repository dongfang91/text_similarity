from torch.utils.data import DataLoader
import math
from sentence_transformers import SentenceTransformer,  SentencesDataset, LoggingHandler, losses
from sentence_transformers.evaluation import TripletEvaluator
from sentence_transformers.readers import TripletReader
import logging
from datetime import datetime


#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout
import argparse
import configparser
import warnings
import os


config = configparser.ConfigParser()
config.read('continue_training.conf')
num_epochs = config['Parameters']['Epoch']
train_batch_size = config['Parameters']['Batch']
triplet_margin = config['Parameters']['Triplet_margin']

def main(model_path,extra_dataset):
    # Read the dataset
    train_batch_size = 64
    num_epochs = 20
    model_save_path = model_path+'_continue_training_'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    n2c2_reader = TripletReader(extra_dataset)

    # Load a pre-trained sentence transformer model
    model = SentenceTransformer(model_path)

    # Convert the dataset to a DataLoader ready for training
    logging.info("Read extra training dataset")
    train_data = SentencesDataset(n2c2_reader.get_examples('train.tsv'), model)
    train_dataloader = DataLoader(train_data, shuffle=True, batch_size=train_batch_size)
    train_loss = losses.TripletLoss(model=model,triplet_margin=triplet_margin)


    logging.info("Read development dataset")
    dev_data = SentencesDataset(examples=n2c2_reader.get_examples('dev.tsv'), model=model)
    dev_dataloader = DataLoader(dev_data, shuffle=False, batch_size=train_batch_size)
    evaluator = TripletEvaluator(dev_dataloader)


    # Configure the training. We skip evaluation in this example
    warmup_steps = math.ceil(len(train_data)*num_epochs/train_batch_size*0.1) #10% of train data for warm-up
    logging.info("Warmup-steps: {}".format(warmup_steps))


    # Train the model
    model.fit(train_objectives=[(train_dataloader, train_loss)],
              evaluator=evaluator,
              epochs=num_epochs,
              evaluation_steps=math.ceil(len(train_data)/train_batch_size),
              warmup_steps=warmup_steps,
              output_path=model_save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sentence embedding for each sentence in the sentence corpus ')

    parser.add_argument('-model',
                        help='the direcotory of the model',required= True)

    parser.add_argument('-extra_dataset',
                        help='the direcotory of the extra dataset',required=True)


    args = parser.parse_args()
    model_path = args.model
    dataset = args.extra_dataset

    main(model_path,dataset)

