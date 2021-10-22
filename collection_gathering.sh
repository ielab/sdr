#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=DIGIX_train
#SBATCH --mem-per-cpu=10G
#SBATCH -o logs/2.txt
#SBATCH -e logs/2.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=5

module load anaconda/3.6
source activate /scratch/itee/uqswan37/Reproduce_SR/envs/
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2


num=$1

python3 collection_gathering.py \
--filename collection/pid_dir/$num.txt \
--email aaa \
--output collection/$num.jsonl

python3 collection_gathering.py \
--filename collection/pid_dir/3.txt \
--email aaa \
--output collection/3.jsonl

