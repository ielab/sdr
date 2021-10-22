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
def count_num(l, minnum, maxnum):
    count = 0
    for i in l:
        if i<=maxnum and i>minnum:
            count+=1
    return count

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

    output_dir = 'graph/' + input_bow_collection.split('/')[-1].split('.')[0] + '_' + \
                 input_bow_original_collection.split('/')[-1].split('.')[0] + '_' + \
                 input_boc_collection.split('/')[-1].split('.')[0] + '.pdf'
    ql_file = os.path.join(DATA_DIR, "qrel_content_all.txt")

    bow_dict = {}

    with open(input_bow_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = data_list["id"]
            contents = data_list["contents"]
            new_contents = []
            new_contents.extend(contents)
            bow_dict[id] = new_contents
    bow_original_dict = {}

    with open(input_bow_original_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = data_list["id"]
            contents = data_list["contents"]
            new_contents = []
            new_contents.extend(contents)
            bow_original_dict[id] = new_contents

    boc_dict = {}

    with open(input_boc_collection, 'r') as jsonfile:
        for line in tqdm(jsonfile):
            data_list = json.loads(line)
            id = data_list["id"]
            contents = data_list["contents"]
            new_contents = []
            new_contents.extend(contents)
            boc_dict[id] = new_contents

    ql_positives = {}
    ql_negatives = {}

    lines = open(ql_file, 'r').readlines()
    for line in lines:
        items = line.split()
        topic = items[0]
        pid = int(items[2])
        relevance = int(items[-1])
        if relevance == 1:
            if topic in ql_positives:
                ql_positives[topic].append(pid)
            else:
                ql_positives[topic] = [pid]
        else:
            if topic in ql_negatives:
                ql_negatives[topic].append(pid)
            else:
                ql_negatives[topic] = [pid]
    overall_ratio_boc = []
    overall_ratio_bow = []
    overall_ratio_original_bow = []
    for id in tqdm(ql_positives):
        pid_positives = ql_positives[id]
        # pid_negatives = ql_negatives[id]
        boc_word_dict = {}
        bow_original_word_dict = {}
        bow_word_dict = {}
        for pid_positive in pid_positives:
            boc_p = boc_dict[pid_positive]
            for term in set(boc_p):
                if term not in boc_word_dict:
                    boc_word_dict[term] = 1
                else:
                    boc_word_dict[term] += 1

        for pid_positive in pid_positives:
            bow_p = bow_original_dict[pid_positive]
            for term in set(bow_p):
                if term not in bow_original_word_dict:
                    bow_original_word_dict[term] = 1
                else:
                    bow_original_word_dict[term] += 1

        for pid_positive in pid_positives:
            bow_p = bow_dict[pid_positive]
            for term in set(bow_p):
                if term not in bow_word_dict:
                    bow_word_dict[term] = 1
                else:
                    bow_word_dict[term] += 1

        ratio_list = []
        for term in boc_word_dict:
            ratio = boc_word_dict[term] / len(pid_positives)
            ratio_list.append(ratio)
        overall_ratio_boc.extend(ratio_list)

        ratio_list = []
        for term in bow_original_word_dict:
            ratio = bow_original_word_dict[term] / len(pid_positives)
            ratio_list.append(ratio)
        overall_ratio_original_bow.extend(ratio_list)

        ratio_list = []
        for term in bow_word_dict:
            ratio = bow_word_dict[term] / len(pid_positives)
            ratio_list.append(ratio)
            overall_ratio_bow.extend(ratio_list)

    overall_ratio = [overall_ratio_boc, overall_ratio_original_bow, overall_ratio_bow]

    # overall_ratio_boc = numpy.random.random(100)
    # overall_ratio_bow = numpy.random.random(100)

    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    counting_ranges = [[0, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1.0]]

    boc = numpy.histogram(overall_ratio_boc, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                          weights=numpy.ones(len(overall_ratio_boc)) / len(overall_ratio_boc))

    boc_times = [count_num(overall_ratio_boc, r[0], r[1]) for r in counting_ranges]
    print("boc:", boc_times, sum(boc_times))
    bow_original = numpy.histogram(overall_ratio_original_bow, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                                   weights=numpy.ones(len(overall_ratio_original_bow)) / len(
                                       overall_ratio_original_bow))

    bow_original_times = [count_num(overall_ratio_original_bow, r[0], r[1]) for r in counting_ranges]
    print("bow_original:", bow_original_times, sum(bow_original_times))


    bow = numpy.histogram(overall_ratio_bow, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                          weights=numpy.ones(len(overall_ratio_bow)) / len(overall_ratio_bow))

    bow_times = [count_num(overall_ratio_bow, r[0], r[1]) for r in counting_ranges]
    print("bow:", bow_times, sum(bow_times))


    overall = [list(x) for x in list(zip(boc[0], bow_original[0], bow[0]))]


    width = 0.5

    labels = ['BOC', 'BOW(Lee&Sun)', 'BOW(Our)']

    #fig, ax = plt.subplots()
    b = [0,0,0]
    plt.figure(figsize=[8, 4])
    plt.tick_params(labelsize=16)
    for line_index, o in enumerate(overall):
        if line_index!=0:
            b = [a+overall[line_index-1][aindex] for aindex, a in enumerate(b)]
        plt.barh(labels, o, width ,b, label=bins[line_index])
    plt.legend(loc='lower center', fontsize= 16, bbox_to_anchor=(0.4, 1.01),
              fancybox=False, shadow=False, ncol=3, labels=["(0.0, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]", "(0.8, 1.0]"])
    #plt.hist(overall_ratio_boc, bins, color =["green", "red"], label=['boc', 'bow'], density=True)
    plt.tight_layout()
    plt.savefig(output_dir)

