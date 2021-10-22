import json
import argparse
from tqdm import tqdm
import spacy
import time
import glob
from multiprocessing import Process, Pool
from gensim.utils import tokenize
import multiprocessing as mp
import itertools
import os
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
cachedStopwords = set(stopwords.words("english"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_bow_cased_lower_lee.jsonl")
    parser.add_argument("--input_umls_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/processed_umls_word/word.tsv")
    parser.add_argument("--input_umls_collection2", type=str,
                        default="/scratch/itee/uqswan37/Reproduce_SR/collection/processed_umls_word_2/word.tsv")
    parser.add_argument("--output_collection", type=str, default="collection/weighted1_boc_terms_umls_connected.jsonl")
    args = parser.parse_args()

    input_collection = args.input_collection
    input_umls = args.input_umls_collection
    input_umls_2 = args.input_umls_collection2
    output = args.output_collection

    umls_dict = {}
    with open(input_umls, 'r') as file:
        for line in tqdm(file):
            items = line.split('\t')
            word = items[0]
            term = items[1].strip()
            if word in umls_dict:
                umls_dict[word].append(term.lower())
            else:
                umls_dict[word] = [term.lower()]
    with open(input_umls_2, 'r') as file:
        for line in tqdm(file):
            items = line.split('\t')
            word = items[0]
            term = items[1].strip()
            if word in umls_dict:
                umls_dict[word].append(term.lower())
            else:
                umls_dict[word] = [term.lower()]
    umls_set = umls_dict.keys()
    with open(output, 'w') as file:
        with open(input_collection, 'r') as jsonfile:
            for line in tqdm(jsonfile):
                data_list = json.loads(line)
                id = int(data_list["id"])
                content = data_list["contents"]
                clinical_set = []
                for word in content:
                    if word in umls_set:
                        term_list = umls_dict[word]
                        #for t in term_list:
                        clinical_set.append(term_list[0])
                new_dic = {
                    'id': id,
                    'contents': clinical_set
                }
                json.dump(new_dic, file)
                file.write('\n')
