# ECIR Reproducibility Paper: Seed-driven Document Ranking for Systematic Reviews: A Reproducibility Study

This code corresponds to the reproducibility paper: "Seed-driven Document Ranking for Systematic Reviews: A Reproducibility Study" and every results gathered from the paper is generated using the code.

### Environment setup:
- This project is implemented and tested only for python version 3.6.12, other python versions are not tested and can not ensure the full run of the results.

First please install the required packages:
```
pip3 install -r requirements.txt
```

### Query&Eval generation:
First please clone the TAR repository using the command
```
git clone https://github.com/CLEF-TAR/tar.git
```
The data that's been used include the following files:
```
For 2017:
tar/tree/master/2017-TAR/training/qrels/qrel_content_train
tar/tree/master/2017-TAR/testing/qrels/qrel_content_test.txt
Please cat these two files together to make 2017_full.txt

For 2018:
tar/tree/master/2018-TAR/Task2/Training/qrels/full.train.content.2018.qrels
tar/tree/master/2018-TAR/Task2/Testing/qrels/full.test.content.2018.qrels
Please cat these two files together to make 2018_full.txt

For 2019:
tar/tree/master/2019-TAR/Task2/Training/Intervention/qrels/full.train.int.content.2019.qrels
tar/tree/master/2019-TAR/Task2/Testing/Intervention/qrels/full.test.int.content.2019.qrels
Please cat thee two files together to make 2019_full.txt, and also 2019_test.txt (note for 2019 these two will be same)

```
Then you can generate query and evaluation the file by:
```
For snigle:
python3 topic_query_generation.py --input_qrel qrel_file_for_training+testing --input_test_qrel qrel_file_for_testing --DATA_DIR output_dir

For multiple:
python3 topic_query_generation_multiple.py --input_qrel qrel_file_for_training+testing --input_test_qrel qrel_file_for_testing --DATA_DIR output_dir

```
Please note: you need to generate for each year and put it in a seperate folder, not the overall one.


### Collection generation:

For BOW collection generation, the following command is needed
```
python3 gather_all_pids.py --filenames 2017_full.txt+2018_full.txt+2019_full.txt --output_dir collection/pid_dir --chunks n
python3 collection_gathering.py --filename yourpidsfile --email xxx@email.com --output output_collection
python3 collection_processing.py --input_collection acquired_collection_file --output_collection processed_file(default is weighted1_bow.jsonl)
```

Then for BOC collection generation, first ensure to check [Quickumls](https://github.com/Georgetown-IR-Lab/QuickUMLS) to gather umls data first.
For BOC collection then, run the following command to generation boc_collection:
```
python3 ncbo_request_word.py --input_collection your_generated_bow_collection --num_workers for_multi_procesing --generated_collection output_dir_ncbo
cat output_dir/* > ncbo.tsv
python3 processing_uml.py --input_collection your_bow_collection --input_umls_dir your_output_umls_dir --num_workers for_multi_procesing
python3 processing_umls_word.py --input_collection your_generated_bow_collection --input_umls_dir your_output_umls_dir_from_last_step --output_file umls.tsv
python3 boc_extraction.py --input_collection bow_collection --input_ncbo_collection ncbo.tsv --input_umls_collection umls.tsv --output_collection processed_file(default is weighted1_boc.jsonl)
```

### RQ1: Does the effectiveness of SDR generalise beyond the CLEF TAR 2017 dataset?

For RQ1, single seed driven results are aquired for clef tar 2017, 2018, 2019, for this please run the following command.
```
bash search.sh 2017_single_data_dir all
bash search.sh 2018_single_data_dir test
bash search.sh 2019_single_data_dir test
```
to get the run_file of all three years single seed run_file with all method.

Then evaluation by:
```
bash evaluation_full.sh 2017_single_data_dir all
bash evaluation_full.sh 2018_single_data_dir test
bash evaluation_full.sh 2019_single_data_dir test
```
to print out evaluation measures and also save evaluation measurement files in the corresponding eval folder


### RQ2: What is the impact of using multiple seed studies collectively on the effectiveness of SDR?
For RQ2, multiple seed driven results are acquired for clef tar 2017, 2018, 2019, for this please run the following command.
```
bash search_multiple.sh 2017_multiple_data_dir all
bash search_multiple.sh 2018_multiple_data_dir test
bash search_multiple.sh 2019_multiple_data_dir test
```
to get the run_file of all three years multiple seed run_file with all methods.

Then evaluation by:
```
bash evaluation_full.sh 2017_multiple_data_dir all
bash evaluation_full.sh 2018_multiple_data_dir test
bash evaluation_full.sh 2019_multiple_data_dir test
```
to print out evaluation measures and also save evaluation measurement files in the corresponding eval folder

### RQ3: To what extent do seed studies impact the ranking stability of single- and multi-SDR?

For this question, we need to use the results acquired from the last two steps, in which we can generate variability graphs by using the following command:
```
python3 graph_maaking.distribution_graph.py --year 2017 --type oracle 
python3 graph_maaking.distribution_graph.py --year 2018 --type oracle 
python3 graph_maaking.distribution_graph.py --year 2019 --type oracle 
```
to get distribution graphs of the three years.

