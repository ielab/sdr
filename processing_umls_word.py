import json
import argparse
from tqdm import tqdm
from quickumls import QuickUMLS
import spacy
import time
import glob
from multiprocessing import Process, Pool
import multiprocessing as mp
import os
import math
size = 1000
input_umls = "umls_data/"
matcher = QuickUMLS(input_umls)
DATA_DIR = "collection/processed_umls_word_2/"

def get_collection_word(collection_file):
    word_set = set()
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            new_content = datalist['contents']
            for word in new_content:
                if '-' in word:
                    word_set.add(word)
    return word_set



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="collection/weighted1_bow_cased_lower_lee.jsonl")
    parser.add_argument("--input_umls_dir", type=str, default="umls_data/")
    parser.add_argument("--output_file", type=str, default="collection/processed_umls_word_2/word.tsv")
    args = parser.parse_args()

    input_umls = args.input_umls_dir
    input_collection = args.input_collection
    output = open(args.output_file, 'w')
    #nlp  = spacy.load('en_core_web_sm')
    word_set = get_collection_word(input_collection)
    for word in tqdm(word_set):
        umls_match = matcher.match(word)
        if len(umls_match)!=0:
            for a in umls_match[0]:
                term = a['term']
                output.write(word + '\t' + term + '\n')








