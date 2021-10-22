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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_umls_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_umls.jsonl")
    parser.add_argument("--output_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_umls_split2.jsonl")
    args = parser.parse_args()

    input_umls = args.input_umls_collection
    output = args.output_collection
    already_got = set()
    if os.path.exists(output):
        with open(output, 'r') as file:
            for line_index, line in tqdm(enumerate(file)):
                data_list = json.loads(line)
                id = data_list["id"]
                already_got.add(id)

    with open(output, 'a+') as file:
        with open(input_umls) as jsonfile:
            for line_index, line in tqdm(enumerate(jsonfile)):
                data_list = json.loads(line)
                id = data_list["id"]
                if id in already_got:
                    continue
                clinical_terms= []
                content = data_list["contents"]
                clinical_terms.extend(content)
                for term in content:
                    new_terms = term.split()
                    clinical_terms.extend(new_terms)
                new_dic = {
                    'id': id,
                    'contents': clinical_terms
                }
                json.dump(new_dic, file)
                file.write('\n')