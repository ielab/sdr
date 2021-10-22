#ECIR Reproducibility Paper: Seed-driven Document Ranking for Systematic Reviews: A Reproducibility Study

This code corresponds to the reproducibility paper: "Seed-driven Document Ranking for Systematic Reviews: A Reproducibility Study" and every results gathered from paper are generated using the code.

###Enviroment setup:
- This project is implemented and tested only for python version 3.6.12, other python versions are not tested and can not ensure the full run of the results.

First please install the required packages:
```
pip3 install -r requirements.txt
```

###Query&Eval generation:
First please clone TAR repository using command
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
Then you can generate query and evaluation file by:
```
python3 topic_query_generation.py --input_qrel qrel_file_for_training+testing --input_test_qrel qrel_file_for_testing --DATA_DIR output_dir
```

For collection generation, we need to first acquire all pmids used in the collection usinng:
```
python3 gather_all_pids.py --filenames 2017_full.txt+2018_full.txt+2019_full.txt --output_dir collection/pid_dir --chunks n
```

Then to acquire all pubmed title+abstract using
```
python3 collection_gathering.py --filename yourpidsfile --email xxx@email.com --output output_collection
```

Then you can process the col










