import json
import argparse
import math
import itertools
from tqdm import tqdm
import os
size = 1000
import random

parser = argparse.ArgumentParser()
parser.add_argument("--input_qrel", type=str, default ="qrel_eval/2019/qrels_content_all.txt")
parser.add_argument("--input_test_eval", type=str, default = "qrel_eval/2019/qrels_content_test.txt")
parser.add_argument("--DATA_DIR", type=str, default="2019/multiple")
parser.add_argument("--percentage", type=float, default=0.2)
parser.add_argument("--random_seed", type=int, default=2)
args = parser.parse_args()

input_qrel_file = args.input_qrel
input_eval_file = args.input_eval
input_test_eval_file = args.input_test_eval
output_queries_file = os.path.join(args.DATA_DIR, "input", "queries.tsv")
output_run_fie = os.path.join(args.DATA_DIR, "input", "run.jsonl")
output_eval_file_run = os.path.join(args.DATA_DIR, "input", "eval_id.tsv")
percentage = args.percentage
random_seed = args.random_seed

output_test_eval_file_run = os.path.join(args.DATA_DIR, "input", "eval_test_topic_id.tsv")


input_qrel = open(input_qrel_file, 'r')
input_eval = open(input_eval_file, 'r')
input_test_eval = open(input_test_eval_file, 'r')
output_quries = open(output_queries_file, 'w')
output_test_eval_run = open(output_test_eval_file_run, 'w')
output_eval_for_run = open(output_eval_file_run, 'w')
output_run = open(output_run_fie, 'w')


doc_dict = {}
qid_list = []

doc_positive_dict = {}

lines = input_qrel.readlines()
for line in tqdm(lines):
    items = line.split()
    id = items[0]
    pid = int(items[2])
    if int(items[-1]) ==1:
        #printa(id+'\t'+query+'\n')
        #output_quries.write(id+'\n')
        if id not in qid_list:
            qid_list.append(id)
        if id in doc_positive_dict:
            doc_positive_dict[id].append(pid)
        else:
            doc_positive_dict[id] = [pid]
    if id in doc_dict:
        doc_dict[id].append(pid)
    else:
        doc_dict[id] = [pid]
input_qrel.close()


output_eval_set = set()
total_num = 0
for qid in tqdm(qid_list):
    data_positive_list = sorted(list(set(doc_positive_dict[qid])))

    data_list = doc_dict[qid]
    number = math.ceil(len(data_positive_list)*percentage)
    output_eval_file = os.path.join(args.DATA_DIR, "input", str(qid) + ".qrel")
    output_eval = open(output_eval_file, 'w')

    subsets = []
    random.Random(random_seed).shuffle(data_positive_list)

    if number>1:
        for i in range(0, len(data_positive_list)-1):
            subsets.append(data_positive_list[i:i+number])

        for positive_ids in subsets:
            id = qid + '_' + '_'.join([str(x) for x in positive_ids])
            output_eval_set.add(id)
            output_quries.write(str(id) + '\n')
            removed_list = [str(x) for x in data_list if x != positive_ids]
            removed_positive_list = [str(x) for x in data_positive_list if x != positive_ids]
            for ppid in removed_positive_list:
                output_eval.write(str(id)+'\t' +'Q0\t' + str(ppid) + '\t' + '1' + '\n')

            removed_list = set(removed_list)
            removed_list = list(removed_list)
            new_dict = {
                'qid': id,
                'pid': removed_list
            }

            json.dump(new_dict, output_run)
            output_run.write('\n')
    output_eval.close()
output_run.close()
output_quries.close()

for id in output_eval_set:
    output_eval_for_run.write(id + '\n')
output_eval_for_run.close()

test_eval_set = set()
lines = input_test_eval.readlines()
for line in tqdm(lines):
    items = line.split()
    #if int(items[-1]) ==1:
    qid = items[0]
        #pid = items[2]
    test_eval_set.add(qid)
#
for item in test_eval_set:
    output_test_eval_run.write(item+'\n')

