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
DATA_DIR = "collection/boc_ncbo/"
api_key = ["2de1074c-0b33-4cf1-94a7-bea779490d64", "1f606b90-38aa-4fc6-8c49-ccd97764d16d", "6a431880-d7c4-4d03-8553-9fa5f22fa09f", "2e0d6468-e6c6-42da-a814-f4cf83252a2e", "30962d18-5b9a-46f0-aec8-ddcb521777d0", "adb9d8b2-9631-4153-8fd8-0a94dd20a3aa", "69c6a479-13bc-47ed-bc30-8edd789c5bc5", "b785f44e-6a40-484f-9a81-969633d23691"]
api_len = len(api_key)

def request(urls):
    id = urls[0]
    dic = urls[1]
    lets_continue = True
    while lets_continue:
        try:
            r = requests.post(url, data = dic)
            lets_continue = False
        except:
            time.sleep(0.5)

    worker = mp.current_process().name
    output = open(DATA_DIR + str(worker) + '.jsonl', 'a+')

    required = r.content.decode("utf-8")
    if required[0:13] != "You have made":

        new_dict = {
            'id': id,
            'content': required
        }
        json.dump(new_dict, output)
        output.write('\n')

    time.sleep(0.07)


def getdict(input_collection, id_set):
    doc_dic = {}
    id_list  = set()
    with open(input_collection) as jsonfile:
        for line_index, line in tqdm(enumerate(jsonfile)):
            data_list = json.loads(line)
            id = str(data_list["id"])
            if id == "null" or id is None or id in id_set:
                continue
            #print(id)
            id_list.add(id)
            # id = data_list["pmid"]
            # if id=="null" or id is None or id in id_set:
            #     continue
            # id_list.add(id)
            # title = data_list["title"]
            # content = data_list["abstract"]

            # new_content = ""
            # if title != "":
            #     new_content += title + " " + content
            # else:
            #     new_content = content
            new_content = '+'.join(data_list["contents"])
            new_dict = {
                'text': new_content,
                'apikey':api_key[line_index % api_len],
                'ontologies':'AI-RHEUM,COSTART,CRISP,FMA,GO,GO-EXT,HCPCS,ICD10,ICD10CM,ICD10PCS,ICD9CM,ICPC2P,LOINC,MDDB,MEDDRA,MESH,MEDLINEPLUS,NCIT,NCBITAXON,NDDF,NDFRT,NIC,OMIM,PDQ,RCD,RXNORM,SNOMEDCT,VANDF,WHO-ART',
                'exclude_numbers': True,
                'whole_word_only':True,
                'exclude_synonyms': True,
                'format':'json',
                'longest_only':True
            }
            #url = "https://data.bioontology.org/annotator?text=" + new_content + "&apikey=" + api_key[line_index % api_len] + "&ontologies=AI-RHEUM,COSTART,CRISP,FMA,GO,GO-EXT,HCPCS,ICD10,ICD10CM,ICD10PCS,ICD9CM,ICPC2P,LOINC,MDDB,MEDDRA,MESH,MEDLINEPLUS,NCIT,NCBITAXON,NDDF,NDFRT,NIC,OMIM,PDQ,RCD,RXNORM,SNOMEDCT,VANDF,WHO-ART&exclude_numbers=true&whole_word_only=true&exclude_synonyms=true&format=json&longest_only=true"
            doc_dic[id] = new_dict
    return doc_dic, id_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_collection", type=str, default="collection/weighted1_bow.jsonl")
    parser.add_argument("--num_workers", type=int, default=10)
    parser.add_argument('--generated_collection', type=str, default="non_setting")
    args = parser.parse_args()
    input = args.input_collection
    num_of_workers = args.num_workers

    id_list = set()
    output_files = glob.glob(DATA_DIR+'*')
    if args.generated_collection == "non_setting":
        for output_file in tqdm(output_files):
            with open(output_file, 'r') as f:
                for line in f:
                    try:
                        data_list = json.loads(line)
                        id_now = data_list["id"]
                        id_list.add(id_now)
                    except:
                        pass
    else:
        output_file =args.generated_collection
        with open(output_file, 'r') as f:
            for line in f:
                data_list = json.loads(line)
                id_now = str(data_list["id"])
                id_list.add(id_now)
    print(len(id_list))
    doc_dict, id_removed = getdict(input_collection=input, id_set=id_list)
    print(id_removed)
    p = Pool(num_of_workers)
    count = int(math.ceil(len(id_removed)/num_of_workers))

    with p:
        doc_content_list = [[id, doc_dict[id]] for id in
                            id_removed]
        p.map(request, doc_content_list)





