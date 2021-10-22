import json
import argparse
from tqdm import tqdm
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

size = 1000
import scipy
parser = argparse.ArgumentParser()
parser.add_argument("--input_qrel", type=str, default ="qrel_eval/2017/qrel_content_all.txt")
parser.add_argument("--input_eval", type=str, default = "qrel_eval/2017/qrel_content_all.txt")
parser.add_argument("--input_test_eval", type=str, default = "qrel_eval/2017/qrel_content_test.txt")
parser.add_argument("--collection", type=str, default = "collection/all.jsonl")
args = parser.parse_args()

input_qrel_file = args.input_qrel
input_eval_file = args.input_eval
input_test_eval_file = args.input_test_eval
collection_file = args.collection

input_qrel = open(input_qrel_file, 'r')
input_eval = open(input_eval_file, 'r')
input_test_eval = open(input_test_eval_file, 'r')


doc_dict = {}
with open(collection_file) as f:
    for line in tqdm(f):
        data_list = json.loads(line)
        id = data_list["pmid"]
        if id == "null" or id is None:
            continue
        else:
            title = data_list["title"]
            content = data_list["abstract"]

            new_content = ""
            if title != "":
                new_content += title + " " + content
            else:
                new_content = content
            doc_dict[int(id)] = new_content
doc_negative_dict = {}
qid_list = []

doc_positive_dict = {}
lines = input_qrel.readlines()
for line in tqdm(lines):
    items = line.split()
    id = items[0] + '_' + items[2]
    if int(items[-1]) ==1:
        if items[0] in doc_positive_dict:
            doc_positive_dict[items[0]].append(items[2])
        else:
            doc_positive_dict[items[0]] = [items[2]]
    else:
        if items[0] in doc_negative_dict:
            doc_negative_dict[items[0]].append(items[2])
        else:
            doc_negative_dict[items[0]] = [items[2]]

positive_intra_sim_dic = {}
negative_intra_sim_dic = {}
for i in tqdm(doc_negative_dict):
    if doc_positive_dict.get(i) is None:
        continue

    positives = doc_positive_dict[i]

    len_po = len(positives)

    if len_po<=1:
        continue
    positive_docs = [doc_dict[int(p)] for p in positives if int(p) in doc_dict]
    tf_idf_numpy = TfidfVectorizer().fit_transform(positive_docs).toarray()
    current_topic_sims = []
    for vector in tf_idf_numpy:
        original_vector = [vector]
        positive_values = scipy.spatial.distance.cdist(original_vector, tf_idf_numpy, 'cosine')[0]
        positive_values = [p for p in positive_values if p!=0]
        positive_value = 1 - ((sum(positive_values)) / (len(positive_values)))
        current_topic_sims.append(positive_value)
    positive_intra_sim_dic[i] = sum(current_topic_sims)/len(current_topic_sims)
    negatives = doc_negative_dict[i]

    negative_intra_sim_dic[i] = []
    #print(len_po)

    for num in range(0, 10):
        negative_samples = random.sample(negatives, len_po)
        negative_docs = [doc_dict[int(p)] for p in negative_samples if int(p) in doc_dict]
        tf_idf_numpy = TfidfVectorizer().fit_transform(negative_docs).toarray()
        current_topic_sims = []
        for vector in tf_idf_numpy:
            original_vector = [vector]
            negative_values = scipy.spatial.distance.cdist(original_vector, tf_idf_numpy, 'cosine')[0]
            negative_values = [p for p in negative_values if p != 0]
            negative_value = 1 - ((sum(negative_values)) / (len(negative_values)))
            current_topic_sims.append(negative_value)
        negative_intra_sim_dic[i].append(sum(current_topic_sims) / len(current_topic_sims))

corresponds =  []
for topic in positive_intra_sim_dic:
    positive_value = positive_intra_sim_dic[topic]
    negative_value = sum(negative_intra_sim_dic[topic])/len(negative_intra_sim_dic[topic])
    corresponds.append([positive_value,negative_value])
corresponds = sorted(corresponds,key=lambda x: (x[0],x[1]))

p = [x[0] for x in corresponds]
n = [x[1] for x in corresponds]
p_ave = sum(p)/len(p)
n_ave = sum(n)/len(n)

_X = np.arange(len(p))
plt.figure(figsize=[7,4])
plt.tick_params(labelsize=16)
plt.axhline(y=p_ave, color='b', linestyle='dashed', label="Avg of relevant docs")
plt.axhline(y=n_ave, color='b', linestyle='dotted', label="Avg of irrelevant docs")
plt.bar(_X-0.2, n, width=0.4, color='red', align='center',label="Irrelevant docs")
plt.bar(_X+0.2, p, width=0.4, color='b', align='center', label="Relevant docs" )

ax = plt.gca()
custom_ticks = np.linspace(0, 44, 45, dtype=int)
ax.set_xticks(custom_ticks)

plt.legend(fontsize= 16,bbox_to_anchor=(0.45, 1.01), fancybox=False, shadow=False, ncol=2, loc='lower center')
plt.ylabel("Intra-similarity", fontsize=16)
plt.tight_layout()
ax.axes.xaxis.set_ticklabels([])
plt.savefig("graph/intra_sim.pdf")










