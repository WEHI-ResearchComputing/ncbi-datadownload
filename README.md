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

## Running

