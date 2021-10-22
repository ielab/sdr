import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT

parser = argparse.ArgumentParser()
parser.add_argument("--DATA_DIR", type=str, default="2017")
parser.add_argument("--METHOD", type=str, required=True)
args = parser.parse_args()

input_single = os.path.join(args.DATA_DIR, "all", "output", args.METHOD)
input_multiple = os.path.join(args.DATA_DIR, "multiple", "output", args.METHOD)

output_list_single = glob.glob(input_single+"/*.trec")
output_list_multiple = glob.glob(input_multiple+"/*.trec")

OUTPUT_LIST = []
for output_file in output_list_single:
    output_file_qid = output_file.split('/')[-1].split('.')[0]
    corresponding_multiple = os.path.join(args.DATA_DIR, "multiple", "output", args.METHOD,output_file_qid+'.trec' )
    if not os.path.exists(corresponding_multiple):
        OUTPUT_LIST.append(output_file_qid)
print(', '.join(OUTPUT_LIST))