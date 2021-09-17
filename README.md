# ncbi-datadownload

## Setting up 
git clone https://github.com/WEHI-ResearchComputing/ncbi-datadownload.git
cd ncbi-datadownload
module load anaconda3
conda init
conda create --name ncbi --file requirements.txt

## Test env is set up correctly
conda activate ncbi
python -c 'import ncbi.datasets.openapi; print(ncbi.datasets.openapi.__version__)'

'''
11.32.1
'''

