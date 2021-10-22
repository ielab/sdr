

data=$1
python3 evaluation.py --METHOD AES_BOW --DATA_DIR $data
python3 evaluation.py --METHOD AES_BOW_P --DATA_DIR $data
python3 evaluation.py --METHOD BM25_BOC_WORD --DATA_DIR $data
python3 evaluation.py --METHOD BM25_BOW --DATA_DIR $data
python3 evaluation.py --METHOD QLM_BOC_WORD --DATA_DIR $data
python3 evaluation.py --METHOD QLM_BOW --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOC_AES --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOC_AES_P --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOC_FULL_WORD --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOW_AES --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOW_AES_P --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOW_FULL --DATA_DIR $data

python3 evaluation.py --METHOD BM25_BOW_LEE --DATA_DIR $data
python3 evaluation.py --METHOD QLM_BOW_LEE --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOW_FULL_LEE --DATA_DIR $data

python3 evaluation.py --METHOD SDR_BOW_FULL_LEE_AES --DATA_DIR $data
python3 evaluation.py --METHOD SDR_BOW_FULL_LEE_AES_P --DATA_DIR $data





