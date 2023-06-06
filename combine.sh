#!/bin/bash -l
#SBATCH -A uppmax2023-2-2 
#SBATCH -p core -n 4
#SBATCH -t 3-00:00:00
#SBATCH -M snowy
#SBATCH -J date_1
##SBATCH --gres=gpu:1
##SBATCH -q gpu

CUDA_VISIBLE_DEVICES=0

conda activate /proj/uppmax2023-2-2/zhaorui/mt
export PYTHONPATH=/proj/uppmax2023-2-2/zhaorui/mt/lib/python3.10/site-packages/:$PYTHONPATH.

python3 combine.py
~