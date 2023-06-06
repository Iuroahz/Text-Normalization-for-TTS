#!/bin/bash -l
#SBATCH -A uppmax2023-2-2 
#SBATCH -p core -n 4
#SBATCH -t 3-00:00:00
#SBATCH -M snowy
#SBATCH -J align_6
## SBATCH --gres=gpu:1
## SBATCH --gpus-per-node=1

CUDA_VISIBLE_DEVICES=0

export PYTHONPATH=/proj/uppmax2023-2-2/zhaorui/mt/lib/python3.7/site-packages/:$PYTHONPATH.
pip install pandas

python3 align_6.py
