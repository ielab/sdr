import json
import argparse
from tqdm import tqdm
import requests
from multiprocessing import Process, Pool
import multiprocessing as mp
import os
import math
import glob
import time
import sys



def get_collection_word(collection_file):
    word_set = set()
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            new_content = datalist['contents']
            for word in new_content:
                if '-' in word:
                    word_set.add(word)
                    print(word)
    return word_set

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="collection/weighted1_bow_cased_lee.jsonl")
    parser.add_argument("--num_workers", type=int, default=20)
    parser.add_argument('--generated_collection', type=str, default="non_setting")
    args = parser.parse_args()
    input = args.input_collection
    num_of_workers = args.num_workers
    word_set = get_collection_word(input)
    #output_files = glob.glob(DATA_DIR+'*')
    print(len(word_set))
