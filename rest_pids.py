import json
import argparse
from tqdm import tqdm
from quickumls import QuickUMLS
import spacy
import time
import glob
from multiprocessing import Process, Pool
from search import get_collection
import multiprocessing as mp
from ncbo_request import getdict
import os
import math
size = 1000
input_umls = "umls_data/"
matcher = QuickUMLS(input_umls)
DATA_DIR = "collection/processed_umls/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all_collection", type=str, default="collection/all.jsonl")
    parser.add_argument("--input_weighted", type=str, default="collection/weighted1_bow.jsonl")
    parser.add_argument("--input_ncbo_collection", type=str, default="collection/boc_ncbo/ncbo_v2_processed.jsonl")
    parser.add_argument("--output", type=str, default="collection/boc_ncbo/rest_pid.jsonl")
    args = parser.parse_args()
    input_collection = args.input_weighted
    input_ncbo = args.input_ncbo_collection
    output = args.output
    all_dict, all_list = getdict(args.all_collection)

    #pid_dict = get_collection(input_collection)
    pid_set = set(all_list)
    print(len(pid_set))
    #with open(output, 'w') as o:
    with open(input_ncbo, 'r') as file:
        for line_index, line in tqdm(enumerate(file)):
            data_list = json.loads(line)
            id = str(data_list["id"])
            pid_set.remove(id)
    print(pid_set)




