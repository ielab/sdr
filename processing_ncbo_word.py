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


parser = argparse.ArgumentParser()

parser.add_argument("--input_ncbo_collection", type=str, default="collection/boc_ncbo_word_2/word.jsonl")
parser.add_argument("--output_ncbo_collection", type=str, default="collection/boc_ncbo_word_2/word.tsv")
args = parser.parse_args()
input_ncbo = args.input_ncbo_collection
output_ncbo = args.output_ncbo_collection
with open(output_ncbo, 'w') as file:
    with open(input_ncbo, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            try:
                data_list = json.loads(line)
                word = data_list["word"]
                content = data_list["content"]
                if content == '[]':
                    continue
                content_data = json.loads(content)
                clinical_set = []
                clinical_ranges = set()
                for c in content_data:
                    an = c["annotations"]
                    for a in an:
                        term = a['text']
                        range = (a["from"], a["to"])
                        if range not in clinical_ranges:
                            clinical_ranges.add(range)
                            file.write(word + '\t' + term + '\n')
            except:
                continue

