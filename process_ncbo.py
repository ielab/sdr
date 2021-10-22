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
DATA_DIR = "collection/processed_umls/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_ncbo_collection", type=str, default="collection/boc_ncbo/adding_ncbo.jsonl")
    parser.add_argument("--output_collection", type=str, default="collection/boc_ncbo/adding_ncbo_processed.jsonl")
    args = parser.parse_args()

    input_ncbo = args.input_ncbo_collection
    output = args.output_collection
    already_got = set()
    if os.path.exists(output):
        with open(output, 'r') as file:
            for line_index, line in tqdm(enumerate(file)):
                data_list = json.loads(line)
                id = data_list["id"]
                already_got.add(id)

    with open(output, 'a+') as file:
        with open(input_ncbo) as jsonfile:
            for line_index, line in tqdm(enumerate(jsonfile)):
                try:
                    data_list = json.loads(line)
                    id = data_list["id"]
                    #if id in already_got:
                       # continue
                    clinical_set = []
                    clinical_ranges = set()
                    content = data_list["content"]
                    content_list = json.loads(content)
                    for c in content_list:
                        an = c["annotations"]
                        #clinical_set.append(an[0]["text"].lower())
                        for a in an:
                            range = (a["from"], a["to"])
                            if range in clinical_ranges:
                                continue
                            else:
                                word = a["text"].lower()
                                clinical_ranges.add(range)
                                clinical_set.append(word)
                    print(len(clinical_set))
                    new_dic = {
                        'id': int(id),
                        'contents': clinical_set
                    }

                    #print(id, clinical_set)
                    json.dump(new_dic, file)
                    file.write('\n')
                except:
                    continue




