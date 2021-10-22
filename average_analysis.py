import json
import argparse
from tqdm import tqdm
import os
import math
size = 1000

parser = argparse.ArgumentParser()
parser.add_argument("--input_eval", type=str, default = "qrel_eval/2017/qrel_content_all.txt")
parser.add_argument("--percentage", type=float, default = 0.2)
parser.add_argument("--DATA_DIR", type=str, default="2017/all")
args = parser.parse_args()

input_eval_file = args.input_eval



input_eval = open(input_eval_file, 'r')


doc_dict = {}
qid_list = []

doc_positive_dict = {}

lines = input_eval.readlines()
for line in tqdm(lines):
    items = line.split()
    id = items[0] + '_' + items[2]
    if int(items[-1]) ==1:
        #printa(id+'\t'+query+'\n')
        if items[0] not in qid_list:
            qid_list.append(items[0])
        if items[0] in doc_positive_dict:
            doc_positive_dict[items[0]].append(items[2])
        else:
            doc_positive_dict[items[0]] = [items[2]]

list_len = []
for i in doc_positive_dict:
    current_len = len(doc_positive_dict[i])
    if current_len>1:
        calculation = math.ceil(current_len*args.percentage)
        list_len.append(calculation)

print(list_len)
print(sum(list_len)/len(list_len))

