DATASET=$1
format = $2

python3 search.py \
--METHOD BM25_BOW \
--format $format \
--DATA_DIR $DATA_DIR
--collection

python3 search.py \
--METHOD QLM_BOW \
--format $format \
--DATA_DIR $DATA_DIR

python3 search.py \
--METHOD _BOW \
--format $format \
--DATA_DIR $DATA_DIR

python3 search.py \
--METHOD BM25_BOW \
--format $format \
--DATA_DIR $DATA_DIR

python3 search.py \
--METHOD BM25_BOW \
--format $format \
--DATA_DIR $DATA_DIR


