import argparse
import os
import json
from tqdm import tqdm
import glob
import math
import scipy.stats
from statsmodels.sandbox.stats.multicomp import multipletests
import numpy

parser = argparse.ArgumentParser()
parser.add_argument("--DATA_DIR", type=str, default="2017/all/")
parser.add_argument("--year", type=int, default=2017)

args = parser.parse_args()
DATA_DIR = args.DATA_DIR
data_eval_dir = os.path.join(DATA_DIR, "eval")

files = os.listdir(data_eval_dir+'/')
result_dict = {}
p_dict = {}
result_dict["recall_10"] = {}
result_dict["recall_100"] ={}
result_dict["recall_1000"] ={}
result_dict["P_10"] ={}
result_dict["P_100"] ={}
result_dict["P_1000"] ={}
result_dict["map"] ={}
result_dict["last_rel"] ={}
result_dict["wss"] ={}
result_dict['ndcg_cut_10'] = {}
result_dict['ndcg_cut_100'] = {}
result_dict['ndcg_cut_1000'] = {}
METHOD_SET = set()
for key in tqdm(result_dict):
    new_dict = {}
    for METHOD in files:
        new_dict[METHOD] = []
        METHOD_SET.add(METHOD)
        METHOD_DIR = os.path.join(data_eval_dir, METHOD)
        eval_file= METHOD_DIR + '/' + key + ".res"
        with open(eval_file,'r') as eval:
            for line in eval:
                items = line.split()
                topic = items[0]
                score = float(items[-1])
                new_dict[METHOD].append(score)

    result_dict[key] =new_dict
Originial_method = "SDR_BOC_AES_P"

for key in tqdm(result_dict):
    pvalues = []
    method_list = []
    new_dict = {}

    method_dict = result_dict[key]
    Original_method_data = method_dict[Originial_method]
    for method in method_dict:
        if method == Originial_method:
            continue
        else:
            method_list.append(method)
            current_method_data = method_dict[method]
            pvalue = scipy.stats.ttest_rel(Original_method_data, current_method_data).pvalue
            #p_dict[key].append([method,pvalue])
            pvalues.append(pvalue)
    pvalues = numpy.array(pvalues)
    bonferroni_result = multipletests(pvalues, method='bonferroni', alpha=0.05)[0]
    for index in range(0,len(method_list)):
        method = method_list[index]
        result = bonferroni_result[index]
        new_dict[method] = result
    p_dict[key] = new_dict

keys = ["map", "P_10","P_100","P_1000", "recall_10","recall_100","recall_1000",'ndcg_cut_10','ndcg_cut_100','ndcg_cut_1000',  "last_rel","wss"]
if args.year == 2017:
    # method_set = ["BM25_BOW", "BM25_BOW_LEE", "QLM_BOW", "QLM_BOW_LEE","SDR_BOW_FULL", "SDR_BOW_FULL_LEE",
    #               "BM25_BOC_WORD", "QLM_BOC_WORD", "SDR_BOC_FULL_WORD", "AES_BOW_P", "AES_BOW",
    #               "SDR_BOW_AES_P", "SDR_BOC_AES_P", "SDR_BOW_AES", "SDR_BOC_AES", "SDR_BOW_FULL_LEE_AES", "SDR_BOW_FULL_LEE_AES_P"]
    method_set = ["QLM_BOC_WORD", "SDR_BOC_FULL_WORD", "SDR_BOC_AES_P"]
else:
    # method_set = ["BM25_BOW", "QLM_BOW","SDR_BOW_FULL",
    #               "BM25_BOC_WORD", "QLM_BOC_WORD", "SDR_BOC_FULL_WORD", "AES_BOW_P", "AES_BOW",
    #               "SDR_BOW_AES_P", "SDR_BOC_AES_P", "SDR_BOW_AES", "SDR_BOC_AES"]
    method_set = ["QLM_BOC_WORD", "SDR_BOC_FULL_WORD", "SDR_BOC_AES_P"]


max_dict = {}
for key in keys:
    current_dict = result_dict[key]
    value_dict = {}
    for method in method_set:
        ave = sum(current_dict[method])/len(current_dict[method])
        value_dict[method] = ave
    max_key = max(value_dict, key=value_dict.get)
    max_dict[key] = max_key

for method in method_set:
    final_list = []
    if method ==Originial_method:
        for key in keys:
            current_list = result_dict[key][method]
            average_num = round(sum(current_list)/len(current_list), 4)
            if method == max_dict[key]:
                final_list.append('\\textbf{' + f'{average_num: .4f}' + '}')
            else:
                final_list.append(f'{average_num: .4f}')

        print( method + "&" + "& ".join(final_list) + '\\\\')
    else:
        for key in keys:
            current_list = result_dict[key][method]
            average_num = round(sum(current_list)/len(current_list), 4)
            if p_dict[key][method]==True:
                if method == max_dict[key]:
                    final_list.append('\\textbf{' +f'{average_num: .4f}' + '}' + "$^\dagger$")
                else:
                    final_list.append(f'{average_num: .4f}' + "$^\dagger$")

            else:
                if method == max_dict[key]:
                    final_list.append('\\textbf{' +f'{average_num: .4f}' + '}')
                else:
                    final_list.append(str(f'{average_num: .4f}'))

        print( method + "&" + "& ".join(final_list)+ '\\\\')





























