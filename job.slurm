#!/bin/bash

#SBATCH --time=8:00:00
#SBATCH --job-name=ncbi_dl
#SBATCH --mail-type=ALL
#SBATCH --mail-user=iskander.j@wehi.edu.au
#SBATCH --output %x_%j.out
#SBATCH --cpus-per-task=10
#SBATCH --mem=500MB

source /stornext/System/data/apps/anaconda3/anaconda3-4.3.1/etc/profile.d/conda.sh
conda activate ncbi

python run.py

