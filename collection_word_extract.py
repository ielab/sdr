import json
import argparse
from tqdm import tqdm
from gensim.utils import tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
cachedStopwords = set(stopwords.words("english"))

import os
size = 1000

parser = argparse.ArgumentParser()
parser.add_argument("--input_collection", type=str, default="collection/all.jsonl")
parser.add_argument("--output_collection", type=str, default="collection/word")
parser.add_argument("--weight", type=int, default=1)
args = parser.parse_args()

input = args.input_collection
output = args.output_collection
weight = args.weight

doc_dic = {}
already_got_id = set()

word_set = set()
with open(output+str(weight)+".tsv", 'w') as file:
    with open(input) as jsonfile:
        for line_index, line in tqdm(enumerate(jsonfile)):
            data_list = json.loads(line)
            id = data_list["pmid"]
            if id in already_got_id or id=="null" or id is None:
                continue
            else:
                already_got_id.add(id)
                title = data_list["title"].lower()
                content = data_list["abstract"].lower()

                new_content = ""
                if title!="":
                    new_content += title*weight+" " + content
                else:
                    new_content = content

                tokenised_list = new_content.split()
                tokenised_removed = [tok for tok in tokenised_list if tok not in cachedStopwords]

                word_set.update(tokenised_removed)
    for element in word_set:
        file.write(element)
        file.write('\n')