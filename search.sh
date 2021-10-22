#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=SR
#SBATCH --mem-per-cpu=10G
#SBATCH -o logs/4_print.txt
#SBATCH -e logs/4_error.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=10

module load anaconda/3.6
source activate /scratch/itee/uqswan37/Reproduce_SR/envs/
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2


method=$1

python3 search.py \
--METHOD $method \
--format all

