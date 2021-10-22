import json
import argparse
from tqdm import tqdm
import requests
from multiprocessing import Process, Pool
import multiprocessing as mp
import os
import math
import glob
import time
url = 'https://data.bioontology.org/annotator?'
DATA_DIR = "collection/boc_ncbo_connected_word/"
api_key = ["2de1074c-0b33-4cf1-94a7-bea779490d64", "1f606b90-38aa-4fc6-8c49-ccd97764d16d", "6a431880-d7c4-4d03-8553-9fa5f22fa09f", "2e0d6468-e6c6-42da-a814-f4cf83252a2e", "30962d18-5b9a-46f0-aec8-ddcb521777d0", "adb9d8b2-9631-4153-8fd8-0a94dd20a3aa", "69c6a479-13bc-47ed-bc30-8edd789c5bc5", "b785f44e-6a40-484f-9a81-969633d23691"]
api_len = len(api_key)

def request(urls):
    word = urls[0]
    url_current = urls[1]
    lets_continue = True
    while lets_continue:
        try:
            r = requests.get(url_current)
        except:
            lets_continue = True
            time.sleep(0.5)
        if r.ok:
            lets_continue = False
        else:
            time.sleep(0.5)

    worker = mp.current_process().name
    output = open(DATA_DIR + str(worker) + '.jsonl', 'a+')
    required = r.content.decode("utf-8")
    if required[0:13] != "You have made" and r.ok:
        new_dict = {
            'word': word,
            'content': required
        }
        if required!='[]':
            print(word)
        json.dump(new_dict, output)
        output.write('\n')
    time.sleep(0.1)

def get_collection_word(collection_file):
    word_set = set()
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            new_content = datalist['contents']
            for word in new_content:
                if '-' in word:
                    word_set.add(word)
    return word_set

def getdict(word_set):
    word_dic = {}
    word_list = []
    for word_index, word in tqdm(enumerate(word_set)):
        url_new = url + "text=" + word + '&longest_only=true&exclude_numbers=false&whole_word_only=true&exclude_synonyms=true&apikey=' + api_key[word_index % api_len]
        word_list.append(word)
        word_dic[word] = url_new

    return word_dic, word_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="collection/weighted1_bow_cased_lower_lee.jsonl")
    parser.add_argument("--num_workers", type=int, default=20)
    parser.add_argument('--generated_collection', type=str, default="non_setting")
    args = parser.parse_args()
    DATA_DIR = args.generated_collection
    input = args.input_collection
    num_of_workers = args.num_workers
    word_set = get_collection_word(input)
    output_files = glob.glob(DATA_DIR+'*')
    print(len(word_set))
    if args.generated_collection == "non_setting":
        for output_file in tqdm(output_files):
            with open(output_file, 'r') as f:
                for line in f:
                    data_list = json.loads(line)
                    word = data_list['word']
                    word_set.remove(word)
    else:
        output_file =args.generated_collection
        with open(output_file, 'r') as f:
            for line in f:
                data_list = json.loads(line)
                word = data_list['word']
                word_set.remove(word)

    print(len(word_set))

    w_d, w_l = getdict(word_set)


    p = Pool(num_of_workers)
    count = int(math.ceil(len(w_l)/num_of_workers))

    with p:
        doc_content_list = [[word, w_d[word]] for word in
                            w_l]
        p.map(request, doc_content_list)





