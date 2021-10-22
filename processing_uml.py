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
DATA_DIR = "collection/processed_umls_gensim/"

def get_collection(collection_file):
    doc_dict = {}
    id_list = set()
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            id = int(datalist["id"])
            content = datalist["abstract"]
            doc_dict[id] = content
            id_list.add(id)
    return doc_dict, id_list

def get_collection_all(collection_file):
    doc_dict = {}
    id_list = set()
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            try:
                # id = int(datalist["pmid"])
                # id_list.add(id)
                # title = datalist["title"]
                # content = datalist["abstract"]
                #
                # new_content = ""
                # if title != "":
                #     new_content += title + " " + content
                # else:
                #     new_content = content
                id = int(datalist["id"])
                new_content = ' '.join(datalist['contents'])
                doc_dict[id] = new_content
                id_list.add(id)
            except:
                continue
    return doc_dict, id_list

def process(id):
    id_num = id[0]
    original_data = id[1]
    worker = mp.current_process().name
    output = open( DATA_DIR + str(worker) + '.jsonl', 'a+')

    clinical_set = []
    umls_match = matcher.match(original_data)
    ranges = set()
    for c in umls_match:
        #a = c[0]
        #term = a['ngram']
        #clinical_set.append(term)
        for a in c:
            term = a['term']
            range = (int(a['start']), int(a['end']))
            if range in ranges:
                if term not in clinical_set:
                    clinical_set.append(term)
            else:
                clinical_set.append(term)
    new_dict = {
        'id': id_num,
        'contents': clinical_set
    }
    json.dump(new_dict, output)
    output.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="collection/weighted1_bow.jsonl")
    parser.add_argument("--input_umls_dir", type=str, default="umls_data/")
    parser.add_argument("--output_collection", type=str, default="collection/processed_umls_gensim/")
    args = parser.parse_args()

    input_umls = args.input_umls_dir
    input_collection = args.input_collection
    output = args.output_collection
    output_files = glob.glob(output + '*')

    #nlp  = spacy.load('en_core_web_sm')

    original_doc, id_list = get_collection_all(args.input_collection)

    for output_file in tqdm(output_files):
        with open(output_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                id = data['id']
                id_list.remove(id)
        print(len(id_list))

    id_list = list(id_list)
    num_of_workers=30
    p = Pool(num_of_workers)
    with p:
        doc_content_list = [[id, original_doc[id]] for id in
                            id_list]
        p.map(process, doc_content_list)








