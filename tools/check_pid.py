import json
import argparse
from tqdm import tqdm

import os
size = 1000

parser = argparse.ArgumentParser()
parser.add_argument("--input_collection", type=str, default="collection/all.jsonl")
parser.add_argument("--input_id", type=str, default="collection/pid_dir/all.txt")
args = parser.parse_args()

input = args.input_collection
input_filename = args.input_id
doc_id_list = set()


with open(input_filename, 'r') as f:
    lines = f.readlines()
    for line in lines:
        doc_id_list.add(line.strip('\n'))
print(len(doc_id_list))

doc_dict_list = set()

with open(input) as jsonfile:
    for line in jsonfile:
        data_list = json.loads(line)
        id = data_list["pmid"]
        doc_dict_list.add(id)

for i in doc_dict_list:
    if i not in doc_id_list:
        print(i)
    else:
        doc_id_list.remove(i)


