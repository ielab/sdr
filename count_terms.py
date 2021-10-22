import json
import argparse
from tqdm import tqdm
import spacy
import time
import glob
from multiprocessing import Process, Pool
import multiprocessing as mp
import os
import math
from matplotlib import pyplot as plt
import numpy

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_bow_collection", type=str,
                        default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_bow.jsonl")
    parser.add_argument("--input_bow_collection_original", type=str,
                        default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_bow_cased_lee.jsonl")
    parser.add_argument("--input_boc_collection", type=str,
                        default="/scratch/itee/uqswan37/Reproduce_SR/collection/weighted1_boc_word.jsonl")
    parser.add_argument("--DATA_DIR", type=str, default="qrel_eval/2017")

    args = parser.parse_args()

    input_bow_collection = args.input_bow_collection
    input_bow_original_collection = args.input_bow_collection_original
    input_boc_collection = args.input_boc_collection

    DATA_DIR = args.DATA_DIR

    bow_set = set()
    bow_num_dict = {}
    with open(input_bow_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            contents = data_list["contents"]
            bow_set.update(contents)
            bow_num_dict[id] = contents

    bow_original_set = set()
    bow_original_num_dict = {}

    with open(input_bow_original_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            contents = data_list["contents"]
            bow_original_set.update(contents)
            bow_original_num_dict[id] = contents

    boc_set = set()
    boc_num_dict = {}

    with open(input_boc_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = int(data_list["id"])
            contents = data_list["contents"]
            boc_set.update(contents)
            boc_num_dict[id] = contents

    print("bow distinct words", len(bow_set))
    print("bowlee distinct words",len(bow_original_set))
    print("boc distinct words",len(boc_set))
    percentage_theirs = []
    percentage_ours = []
    overall_boc = 0
    overall_bow = 0
    overall_bow_o = 0
    for id in tqdm(bow_num_dict):
        bow_num = len(bow_num_dict[id])
        bow_original_num = len(bow_original_num_dict[id])
        boc_num = len(boc_num_dict[id])
        print(str(id))
        print(bow_num_dict[id])
        print(bow_original_num_dict[id])
        print(boc_num_dict[id])
        break
        if bow_original_num!=0:
            percentage_theirs.append(boc_num/bow_original_num)
        if bow_num != 0:
            percentage_ours.append(boc_num/bow_num)
        overall_boc += boc_num
        overall_bow += bow_num
        overall_bow_o += bow_original_num
    # print("our percentage", str(sum(percentage_ours)/len(percentage_ours)))
    # print("their percentage", str(sum(percentage_theirs) / len(percentage_theirs)))
    #
    # print("our o percentage", str(overall_boc/overall_bow))
    # print("their o percentage", str(overall_boc / overall_bow_o))

