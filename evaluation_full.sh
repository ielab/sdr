

data=$1
format=$2
python3 evaluation.py --METHOD AES_BOW --DATA_DIR $data --format $format
python3 evaluation.py --METHOD AES_BOW_P --DATA_DIR $data --format $format
python3 evaluation.py --METHOD BM25_BOC_WORD --DATA_DIR $data --format $format
python3 evaluation.py --METHOD BM25_BOW --DATA_DIR $data --format $format
python3 evaluation.py --METHOD QLM_BOC_WORD --DATA_DIR $data --format $format
python3 evaluation.py --METHOD QLM_BOW --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOC_AES --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOC_AES_P --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOC_FULL_WORD --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOW_AES --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOW_AES_P --DATA_DIR $data --format $format
python3 evaluation.py --METHOD SDR_BOW_FULL --DATA_DIR $data --format $format






