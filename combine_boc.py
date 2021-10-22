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
    parser.add_argument("--input_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_bow.jsonl")
    parser.add_argument("--input_ncbo_collection", type=str, default="collection/boc_ncbo/ncbo_processed.jsonl")
    parser.add_argument("--input_umls_collection", type=str, default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_boc_term_umls.jsonl")
    parser.add_argument("--output_collection", type=str, default="collection/weighted1_boc_v17.jsonl")
    args = parser.parse_args()

    input_collection = args.input_collection
    input_ncbo = args.input_ncbo_collection
    input_umls = args.input_umls_collection
    output = args.output_collection

    id_set = set()
    with open(input_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            id_set.add(id)

    if os.path.exists(output):
        with open(output, 'r') as file:
            for line_index, line in tqdm(enumerate(file)):
                data_list = json.loads(line)
                id = int(data_list["id"])
                id_set.remove(id)
    umls_dict = {}

    with open(input_umls, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            #contents = ' '.join([d.lower() for d in data_list["contents"]])
            #new_contents = tokenize(contents)
            new_contents = [d.lower() for d in data_list["contents"]]
            # new_contents = list(itertools.chain.from_iterable(new_contents))
            new_contents = [tok for tok in new_contents if tok not in cachedStopwords]
            umls_dict[id] = new_contents

    ncbo_dict = {}

    with open(input_ncbo, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            # contents = ' '.join([d.lower() for d in data_list["contents"]])
            # new_contents = tokenize(contents)
            new_contents = [d.lower() for d in data_list["contents"]]
            # new_contents = list(itertools.chain.from_iterable(new_contents))
            new_contents = [tok for tok in new_contents if tok not in cachedStopwords]
            ncbo_dict[id] = new_contents

    with open(output, 'a+') as file:
        for id in tqdm(id_set):
            clinical_set = []
            ncbo_set = set()
            if id in ncbo_dict:
                clinical_set.extend(ncbo_dict[id])
                ncbo_set = set(ncbo_dict[id])

            if id in umls_dict:
                umls_data = umls_dict[id]
                for word in umls_data:
                    if word not in ncbo_set:
                        clinical_set.append(word)
            new_dic = {
                'id': id,
                'contents': clinical_set
            }
            #print(id, clinical_set)
            json.dump(new_dic, file)
            file.write('\n')