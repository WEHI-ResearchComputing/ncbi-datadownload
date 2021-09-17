import logging
import os
import json
from pathlib import Path
import sys
import zipfile,glob,shutil
import numpy as np


from ncbi.datasets.openapi import ApiClient as DatasetsApiClient
from ncbi.datasets.openapi import ApiException as DatasetsApiException
from ncbi.datasets.openapi import GenomeApi as DatasetsGenomeApi
from ncbi.datasets.metadata.genome import get_assembly_metadata_by_taxon
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def downloads_and_process(accessions, dest_dir,output_dir):
    
    n = str(random.random())
    name=f'{n}'.replace(".","")
    zipfile_name=f'{name}.zip'
    
    download_link(accessions, zipfile_name, dest_dir)
    print(os.path.join(dest_dir,zipfile_name))
    with zipfile.ZipFile(os.path.join(dest_dir,zipfile_name), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(dest_dir,name))
        files=os.listdir(os.path.join(dest_dir,name,"ncbi_dataset/data"))
    numfiles=0
    try:
        for file in files:
            if os.path.isdir(os.path.join(dest_dir,name,"ncbi_dataset/data",file)):
                filetomove=glob.glob(os.path.join(dest_dir,name,"ncbi_dataset/data",file,f"{file}*"))
                if len(filetomove)>0:
                    numfiles=numfiles+1
                    shutil.move(filetomove[0], output_dir)
                    logging.info('Moved %s',filetomove[0])
    except OSError as e:
            sys.exit(f'Error in moving {filetomove[0]}\n')
   
    #logging.info('Moved %d files',numfiles)
    
    
def write_accessions(filename, accession):
    with open(filename, 'w') as filehandle:
        for link in accession:
            filehandle.write('%s\n' % link)

def read_accessions(filename):
    accessions = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            l = line[:-1]
            accessions.append(l)
    return accessions

def get_accessions(taxname,assembly_level,ret_content):
    accessions: List[str] = [
        asm_rec.assembly.assembly_accession 
        for asm_rec in get_assembly_metadata_by_taxon(taxname,
                                              filters_assembly_level=assembly_level,
                                              returned_content=ret_content)]
    if not accessions:
        sys.exit()

    logging.info(f'found {len(accessions)} genomes for {taxname}')
    return accessions

def download_link(accessions, zipfile_name, dest_dir):
    if type(accessions) is np.ndarray:
        accessions=accessions.tolist()
    if not isinstance(accessions, list):
        accessions=[accessions]
    with DatasetsApiClient() as api_client:
        genome_api = DatasetsGenomeApi(api_client)
        try:
            genome_ds_download = genome_api.download_assembly_package(
                accessions,
                include_annotation_type=['RNA_FASTA'],
                _preload_content=False)

            with open(os.path.join(dest_dir,zipfile_name), 'wb') as f:
                f.write(genome_ds_download.data)
            print(f'Download completed -- see {zipfile_name}')
        except DatasetsApiException as e:
            sys.exit(f'Exception when calling download_assembly_package: {e}\n')
    
def setup_output_dir(op_dir):
    dirs=[op_dir,
    os.path.join(op_dir,"Pool"),os.path.join(op_dir,"Master"),
    os.path.join(op_dir,"Nontarget"),
    os.path.join(op_dir,"Results")]
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)
    logging.info("Output Directory Tree Created.")
    
def setup_download_dir(directory):
    download_dir = Path(directory)
    if download_dir.exists():
        shutil.rmtree(download_dir)
    download_dir.mkdir()
    logging.info("Download Directory Tree Created.")