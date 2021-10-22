#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=DIGIX_train
#SBATCH --mem-per-cpu=4G
#SBATCH -o logs/1_r.txt
#SBATCH -e logs/1_p.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=30

module load anaconda/3.6
source activate /scratch/itee/uqswan37/Reproduce_SR/envs/
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2


python3 processing_uml.py