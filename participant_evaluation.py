import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT

parser = argparse.ArgumentParser()
parser.add_argument("--year", type=str, default="2017")
parser.add_argument("--trec_eval", type = str, default="trec_eval/trec_eval")
parser.add_argument("--tar_eval", type = str, default="python3 tar/scripts/tar_eval.py")

args = parser.parse_args()
trec_eval = args.trec_eval
tar_eval = args.tar_eval
if args.year =="2017":
    participant_run_file = os.path.join("participant_runs",args.year,'Test_Data_Sheffield-run-2.txt' )
    our_dir = os.path.join("participant_runs",args.year,"qrel_content_all.txt")
elif args.year =="2018":
    participant_run_file = os.path.join("participant_runs", args.year, 'sheffield-general_terms.task2.txt')
    our_dir = os.path.join("participant_runs",args.year,"qrels_content_test.txt")
output_file = os.path.join("participant_runs", args.year, "run.txt")

eval_files = open(our_dir, 'r').readlines()
relevance_dict = {}
for line in eval_files:
    items = line.split()
    topic = items[0]
    pid = items[2]
    relevance = items[-1]
    if int(relevance)==1:
        if topic not in relevance_dict:
            relevance_dict[topic] = [pid]
        else:
            relevance_dict[topic].append(pid)
topic_list = []
for topic in relevance_dict:
    if len(relevance_dict[topic])<=1:
        print(topic)
    else:
        topic_list.append(topic)

run = open(participant_run_file, 'r').readlines()

output = open(output_file, 'w')
for line in run:
    items = line.split()
    topic = items[0]
    if topic in topic_list:
        output.write(line)
output.close()

command = trec_eval+" -m recall.10,100,1000 -m P.10,100,1000 -m map -m ndcg_cut.10,100,1000 " + ' ' + our_dir + " " + participant_run_file
results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
list_r = []
for result in results:
    items = result.split()
    if items[1]=="all":
        list_r.append(items[2])



command = tar_eval + " " +  our_dir + " " + participant_run_file
results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
for result in results:
    items = result.split('\t')
    if len(items) == 3 and items[0] == "ALL":
        if items[1] == "min_req":
            list_r.append(items[2].strip())
        elif items[1] == 'wss_100':
            list_r.append(items[2].strip())
print("&".join(list_r) + '\\\\')





