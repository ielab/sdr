import argparse
import os
import json
from tqdm import tqdm
import glob
import math
import scipy.stats
from statsmodels.sandbox.stats.multicomp import multipletests
import numpy
from subprocess import Popen, PIPE, STDOUT

trec_eval = "trec_eval/trec_eval"
tar_eval = "python3 tar/scripts/tar_eval.py"

METHOD_trec_KEYS = ["map", "P_10","P_100","P_1000", "recall_10","recall_100","recall_1000", 'ndcg_cut_10','ndcg_cut_100','ndcg_cut_1000']
METHOD_tar_KEYS = ["min_req","wss_100"]
METHOD_KEYS = ["map", "P_10","P_100","P_1000", "recall_10","recall_100","recall_1000", 'ndcg_cut_10','ndcg_cut_100','ndcg_cut_1000', "min_req","wss_100"]
measurements = ["SDR_BOC_AES_P", "SDR_BOW_AES_P"]

years = ['2017', "2018", "2019"]
data_dirs = ['all','multiple']
#measurements = ["SDR_BOC_AES_P"]
p_dict = {}
result_dict = {}
for year in years:
    p_dict[year] = {}
    result_dict[year] = {}
    for measurement in tqdm(measurements):
        result_dict[year][measurement] = {}
        p_dict[year][measurement] = {}
        data_dict = {}
        output_runs_dir = os.path.join(year, "multiple", "output", measurement) + '/'
        output_list= glob.glob(output_runs_dir+"*.trec")
        for output_file in tqdm(output_list):
            output_file_qid = output_file.split('/')[-1].split('.')[0]

            tem_result_dict_a = {}
            tem_result_dict_m = {}
            for data_dir in data_dirs:
                result_dict[year][measurement][data_dir] = {}
                output_file = os.path.join(year, data_dir, "output", measurement) + '/'+output_file_qid+'.trec'
                input_d = os.path.join(year, data_dir, "input")
                command = trec_eval + " -q -m recall.10,100,1000 -m P.10,100,1000 -m map -m ndcg_cut.10,100,1000" + ' ' + input_d + '/' + output_file_qid + '.qrel' + " " + output_file
                results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True,
                                shell=True).stdout.readlines()

                for result in results:
                    items = result.split()
                    for k in METHOD_trec_KEYS:
                        if k not in tem_result_dict_a:
                            tem_result_dict_a[k] = {}
                        if k not in tem_result_dict_m:
                            tem_result_dict_m[k] = {}

                        if len(items) == 3 and items[0] == k and items[1]!='all':
                            query_id = items[1]
                            if data_dir =="all":
                                actual_id = query_id.split('_')[1]
                                score = float(items[-1])
                                tem_result_dict_a[k][actual_id] = score
                            else:
                                actual_id = '_'.join(query_id.split('_')[1:])
                                score = float(items[-1])
                                tem_result_dict_m[k][actual_id] = score

                command2 = tar_eval + " " +  input_d +'/' +output_file_qid+'.qrel' + " " + output_file
                results = Popen(command2, stdout=PIPE, stderr=PIPE, universal_newlines=True,
                                shell=True).stdout.readlines()
                for result in results:
                    items = result.split()
                    for k in METHOD_tar_KEYS:
                        if k not in tem_result_dict_a:
                            tem_result_dict_a[k] = {}
                        if k not in tem_result_dict_m:
                            tem_result_dict_m[k] = {}
                        if len(items) == 3 and items[1] == k and items[0] != 'ALL':
                            query_id = items[0]
                            if data_dir == "all":
                                actual_id = query_id.split('_')[1]
                                score = float(items[-1])
                                tem_result_dict_a[k][actual_id] = score
                            else:
                                actual_id = '_'.join(query_id.split('_')[1:])
                                score = float(items[-1])
                                tem_result_dict_m[k][actual_id] = score
            #print(output_file_qid,tem_result_dict_m)
            reference_dict = tem_result_dict_m["map"]

            refering_dict = {}
            for pid_com in reference_dict:
                pids = pid_com.split('_')
                max_dict = {}
                for pid in pids:
                    if pid in tem_result_dict_a["map"]:
                        max_dict[pid] = tem_result_dict_a["map"][pid]
                if len(max_dict)>0:
                    max_key = max(max_dict, key=max_dict.get)
                    refering_dict[pid_com] = max_key

            for eval_type in tem_result_dict_m:
                if eval_type not in result_dict[year][measurement]:
                    result_dict[year][measurement][eval_type] = {}
                all_list = []
                multiple_list = []
                data_di = tem_result_dict_m[eval_type]
                for actual in data_di:
                    m_value = data_di[actual]
                    if actual not in refering_dict:
                        continue
                    a_value = tem_result_dict_a[eval_type][refering_dict[actual]]
                    all_list.append(a_value)
                    multiple_list.append(m_value)
                if len(all_list)==0 or len(multiple_list) ==0:
                    continue
                all_average = sum(all_list)/len(all_list)
                multiple_average = sum(multiple_list)/len(multiple_list)
                if "all" not in result_dict[year][measurement][eval_type]:
                    result_dict[year][measurement][eval_type]["all"] = [all_average]
                else:
                    result_dict[year][measurement][eval_type]["all"].append(all_average)
                if "multiple" not in result_dict[year][measurement][eval_type]:
                    result_dict[year][measurement][eval_type]["multiple"] = [multiple_average]
                else:
                    result_dict[year][measurement][eval_type]["multiple"].append(multiple_average)

for year in years:
    increase_dict = {}
    for measurement in measurements:
        measure_list_all = []
        measure_list_multiple = []
        for key in METHOD_KEYS:

            all_list = result_dict[year][measurement][key]["all"]
            multiple_list = result_dict[year][measurement][key]["multiple"]
            average_all = sum(all_list)/len(all_list)
            average_multiple = sum(multiple_list)/len(multiple_list)
            p_value = scipy.stats.ttest_rel(all_list, multiple_list).pvalue
            if p_value<0.05:
                measure_list_multiple.append(str(f'{average_multiple: .4f}')+"$^\dagger$")
            else:
                measure_list_multiple.append(str(f'{average_multiple: .4f}'))
            measure_list_all.append(str(f'{average_all: .4f}'))
            if key not in increase_dict:
                increase_dict[key] = [((average_multiple-average_all)/average_all)*100]
            else:
                increase_dict[key].append(((average_multiple - average_all) / average_all) * 100)

        print(str(year) + ' single ' + measurement + "&" + '& '.join(measure_list_all) + '\\\\')
        print(str(year) + ' multiple ' + measurement + "&"+ '& '.join(measure_list_multiple) + '\\\\')
    average_increase = []
    for key in METHOD_KEYS:
        increased_average = sum(increase_dict[key])/len(increase_dict[key])
        average_increase.append(f'{increased_average: .4f}')
    print(str(year) + ' %increased ' + "&" + '& '.join(average_increase) + '\\\\')






