import json
import argparse
from tqdm import tqdm
import os

parser = argparse.ArgumentParser()
parser.add_argument("--filenames", nargs='+', type=str, required=True)
parser.add_argument("--output_dir", type=str, default="collection/pid_dir/")
parser.add_argument("--chunks", type=int, default=1)
args = parser.parse_args()


input_filenames = args.filenames
output_path = args.output_dir
chunks = args.chunks

doc_id_set = set()

for input_file in tqdm(input_filenames):
    print(input_file)
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            doc_id_set.add(line.split()[2])
    print(len(doc_id_set))

if not os.path.exists(output_path):
    os.mkdir(output_path)
doc_id_list = list(doc_id_set)
num = int(len(doc_id_list)/chunks)+1

for i in range(0,chunks):
    output = open(output_path+str(i)+'.txt', 'w')
    current_list = doc_id_list[i*num: i*num+num]
    if i==chunks-1:
        current_list = doc_id_list[i * num: len(doc_id_list)]
    for item in current_list:
        output.write(item+'\n')










