DATASET=$1
format = $2


python3 search_multiple.py \
--METHOD SDR_BOW_FULL \
--format $format \
--DATA_DIR $DATA_DIR

python3 search_multiple.py \
--METHOD SDR_BOC_FULL_WORD \
--format $format \
--DATA_DIR $DATA_DIR

python3 search_multiple.py \
--METHOD AES_BOW \
--format $format \
--DATA_DIR $DATA_DIR

python3 search_multiple.py \
--METHOD AES_BOW_P \
--format $format \
--DATA_DIR $DATA_DIR

python3 aes_sdr_combine.py --DATA_DIR $DATA_DIR \
--AES_METHOD AES_BOW \
--SDR_METHOD SDR_BOW_FULL \
--COM_METHOD AES_BOW_AES

python3 aes_sdr_combine.py --DATA_DIR $DATA_DIR \
--AES_METHOD AES_BOW_P \
--SDR_METHOD SDR_BOW_FULL \
--COM_METHOD AES_BOW_AES_P

python3 aes_sdr_combine.py --DATA_DIR $DATA_DIR \
--AES_METHOD AES_BOW \
--SDR_METHOD SDR_BOC_FULL_WORD \
--COM_METHOD AES_BOC_AES

python3 aes_sdr_combine.py --DATA_DIR $DATA_DIR \
--AES_METHOD AES_BOW_P \
--SDR_METHOD SDR_BOC_FULL_WORD \
--COM_METHOD AES_BOC_AES_P