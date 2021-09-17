# ncbi-datadownload

This is a python script to download data from ncbi using [ncbi Python APIs](https://www.ncbi.nlm.nih.gov/datasets/docs/languages/python/api/)

## Setting up env in [vc7-shared/interactive slurm session](https://rc.wehi.edu.au/Documentation/getting-started/interactive-work)
```
git clone https://github.com/WEHI-ResearchComputing/ncbi-datadownload.git
cd ncbi-datadownload
module load anaconda3
conda init
conda create --name ncbi --file requirements.txt
```

## Test env is set up correctly
```
conda activate ncbi
python -c 'import ncbi.datasets.openapi; print(ncbi.datasets.openapi.__version__)'

```
The result should be similar to 
```
11.32.1
```

## Configure Download/Output directories
You can use any text editor to open `config.json` that or through Open Ondemand File Menu
```
nano config.json
```
```
{"taxname": "Pseudomonas aeruginosa", 
"assembly_level": ["complete_genome"], 
"ret_content": "ASSM_ACC", 
"other_species": ["Pseudomonas putida", "Pseudomonas fluorescens", "Pseudomonas stutzeri", "Pseudomonas syringae", "Pseudomonas viridiflava", "Pseudomonas chlororaphis"], 
"download_dir": "/vast/scratch/users/iskander.j/download", 
"output_dir": "/vast/scratch/users/iskander.j/ncbi_output"}
```
Change the paths values for download_dir and output_dir to your directories on vast or HPCScratch.
You can also change the inclusion genome name `taxname` or add/remove items from the exclusion group `other_species`

## Modify slurm job submission script
Open `job.slurm` add your email after `--mail-user`
```
nano job.slurm
```
```
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

```

## Running

```
sbatch job.slurm
```
# Output Folder structure
* Master
* Nontarget
* Pool
* Results


Pool will contain all inclusion genomes. Nontarget will contain all exclusion group genomes

# [Montiring the job](https://rc.wehi.edu.au/Documentation/getting-started/batch-system/getting-started)

`squeue -u <userid>` will show a list of your jobs running in the queue, `R` means running and `PD` means pending
A text file will be created in the folder called ncbi_dl_<jobid>.out to where the output of the running processes will be redirected.
When the job ends, you will get an email and to check that all files have been downloaded check the last line in ncbi_dl_<jobid>.out

```
Found 654,398 and Moved 654,398
```
The numbers of files found for inclusion group (654) and exclusion group (398) should be equal to number of files moved for inclusion group (654) and exclusion group (398).
