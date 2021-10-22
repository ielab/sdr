import json
import argparse
from tqdm import tqdm
import time
import glob
from multiprocessing import Process, Pool
import multiprocessing as mp
import os
import math


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_ncbo_collection", type=str, default="ncbo_v2.jsonl")
    parser.add_argument("--output_collection", type=str, default="ncbo_v2_filtered.jsonl")
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
                    content = data_list["content"]
                    #content_list = json.loads(content)
                    new_dic = {
                        'id': id,
                        'contents': content
                    }
                    #print(id, clinical_set)
                    json.dump(new_dic, file)
                    file.write('\n')
                except:
                    continue