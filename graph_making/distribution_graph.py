import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm
import statistics
import scipy.stats
import math
import random
random.seed(100)
parser = argparse.ArgumentParser()
parser.add_argument("--year", type=str, default="2017")
parser.add_argument("--type", type=str, default="single")
parser.add_argument("--METHOD", type=str, default="SDR_BOW_AES_P")
parser.add_argument("--trec_eval", type = str, default="trec_eval/trec_eval")
args = parser.parse_args()

if args.type =="single" or args.type =="oracle":
    DATA_DIR_run = args.year + '/all'
else:
    DATA_DIR_run = args.year + '/multiple'
output_dir = "graph/distribution_" + args.year + '_' + args.type + '.pdf'
DATA_DIR_Multi = args.year + '/multiple'


input_d = os.path.join(DATA_DIR_run, "input")
data_eval_file = os.path.join(DATA_DIR_run, "input", "eval.qrel")
data_test_eval_file = os.path.join(DATA_DIR_Multi, "input", "eval_test_topic_id.tsv")

data_output_dir = os.path.join(DATA_DIR_run, "output", args.METHOD)
data_eval_dir = os.path.join(DATA_DIR_run, "eval")
trec_eval = args.trec_eval



test_eval_list = []
data_test_eval = open(data_test_eval_file, 'r')
lines = data_test_eval.readlines()
for line in lines:
    test_eval_list.append(line.strip('\n'))

if not os.path.exists(data_eval_dir):
    os.mkdir(data_eval_dir)


result_dict = {}
average_dict = []
if args.type!="oracle":
    output_list= glob.glob(data_output_dir+"/*.trec")
    qrel_list = glob.glob(input_d+"/*.qrel")
    test_list = []
    for q in qrel_list:
        output_qid = q.split('/')[-1].split('.')[0]
        if output_qid in test_eval_list:
            test_list.append(output_qid)
    for output_file in output_list:
        output_file_qid = output_file.split('/')[-1].split('.')[0]
        if not os.path.exists(os.path.join(DATA_DIR_Multi, "output",args.METHOD, output_file_qid + ".trec")):
            continue
        command = trec_eval+" -q -m map" + ' ' + input_d +'/' +output_file_qid+'.qrel' + " " + output_file
        results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
        for result in results:
            items = result.split()
            if len(items)== 3 and items[0]=="map":
                if items[1]!="all":
                    if output_file_qid not in result_dict:
                        result_dict[output_file_qid] = [float(items[-1])]
                    else:
                        result_dict[output_file_qid].append(float(items[-1]))
    sorted_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: sum(item[1]) / len(item[1]))}
    overall_list = [sum(result_dict[k]) / len(result_dict[k]) for k in result_dict]
    overall_value = sum(overall_list) / len(overall_list)
    print(sorted_dict.values())

    # fig,ax = plt.subplots()
    plt.boxplot(sorted_dict.values(), meanline=True)
    plt.xticks([])
    plt.ylim(0, 1)
    plt.yticks(fontsize=14)
    # plt.axhline(y=overall_value, color='black', linestyle='dashed', label="average")
    plt.ylabel("MAP", fontsize=16)
    plt.xlabel("Systematic reviews", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_dir)
    variance_list = []
    for topic in result_dict:

        variance_a = statistics.variance(result_dict[topic])
        variance_list.append(variance_a)
        #print(topic, variance_a)
    print(args.type, sum(variance_list)/len(variance_list))
else:
    data_dirs = ['all', 'multiple']
    output_runs_dir = os.path.join(DATA_DIR_Multi, "output", args.METHOD) + '/'
    output_list = glob.glob(output_runs_dir + "*.trec")
    for data_dir in data_dirs:
        if data_dir not in result_dict:
            result_dict[data_dir] = {}
    for output_file in tqdm(output_list):
        output_file_qid = output_file.split('/')[-1].split('.')[0]
        tem_result_dict_a = {}
        tem_result_dict_m = {}
        for data_dir in data_dirs:
            output_file = os.path.join(args.year, data_dir, "output", args.METHOD) + '/' + output_file_qid + '.trec'
            input_d = os.path.join(args.year, data_dir, "input")
            command = trec_eval + " -q -m map" + ' ' + input_d + '/' + output_file_qid + '.qrel' + " " + output_file
            results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True,
                            shell=True).stdout.readlines()
            for result in results:
                items = result.split()
                if len(items) == 3 and items[0] == "map" and items[1] != 'all':
                    query_id = items[1]
                    if data_dir == "all":
                        actual_id = query_id.split('_')[1]
                        score = float(items[-1])
                        tem_result_dict_a[actual_id] = score
                    else:
                        actual_id = '_'.join(query_id.split('_')[1:])
                        score = float(items[-1])
                        tem_result_dict_m[actual_id] = score
        reference_dict = tem_result_dict_m
        refering_dict = {}
        for pid_com in reference_dict:
            pids = pid_com.split('_')
            max_dict = {}
            for pid in pids:
                if pid in tem_result_dict_a:
                    max_dict[pid] = tem_result_dict_a[pid]

            if len(max_dict) > 0:

                max_key = random.choice(list(max_dict.keys()))
                refering_dict[pid_com] = max_key
        all_list = []
        multiple_list = []
        data_di = tem_result_dict_m
        for actual in data_di:
            m_value = data_di[actual]
            if actual not in refering_dict:
                continue
            a_value = tem_result_dict_a[refering_dict[actual]]
            all_list.append(a_value)
            multiple_list.append(m_value)
        if len(all_list) == 0 or len(multiple_list) == 0:
            continue
        result_dict["all"][output_file_qid] = all_list
        result_dict["multiple"][output_file_qid] = multiple_list


    for data_dir in data_dirs:

        current_dict = result_dict[data_dir]
        #print(data_dir, variance)
        plt.figure(figsize=[7, 4])
        output_dir = "graph/distribution_" + args.year + '_' + args.type + data_dir +  '.pdf'
        sorted_dict = {k: v for k, v in sorted(current_dict.items(), key=lambda item: sum(item[1]) / len(item[1]))}
        print(sorted_dict)
        plt.boxplot(sorted_dict.values(), meanline=True)

        plt.xticks([])
        plt.ylim(0, 1)
        plt.yticks(fontsize=18)
        # plt.axhline(y=overall_value, color='black', linestyle='dashed', label="average")
        plt.ylabel("MAP", fontsize=18)
        plt.xlabel("Systematic review topics", fontsize=18)
        plt.tight_layout()
        plt.savefig(output_dir)
        plt.close()

    v_a_list = []
    v_m_list = []

    for topic in result_dict["all"]:
        variance_a = statistics.variance(result_dict["all"][topic])
        v_a_list.append(variance_a)
        variance_m = statistics.variance(result_dict["multiple"][topic])
        v_m_list.append(variance_m)
    p_value = scipy.stats.ttest_rel(v_a_list, v_m_list).pvalue
    print("p_value",  p_value)
    if p_value<0.05:
        print("it's significant")
    print(sum(v_a_list)/len(v_m_list), sum(v_m_list)/len(v_m_list))











