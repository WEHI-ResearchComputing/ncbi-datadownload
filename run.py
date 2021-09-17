from download_ncbi import *
import json
from functools import partial
from time import time
from multiprocessing.pool import Pool
import numpy as np


def main(argv):
    with open('config.json') as f:
        config = json.load(f)

    taxname=config['taxname'] #'Pseudomonas aeruginosa'
    assembly_level=config['assembly_level'] #['complete_genome']
    ret_content=config['ret_content'] #'ASSM_ACC'
    accessions=get_accessions(taxname,assembly_level,ret_content)
    filename=f'accessions_{taxname}.txt'
    write_accessions(filename, accessions)
    main_acc=len(accessions)
    dest_dir=config['download_dir']
    op_dir=config['output_dir']
    
    setup_output_dir(op_dir)
    setup_download_dir(dest_dir)

    ts = time()
    numfiles=50
    exc_acc=0
    ts = time()
    with Pool(20) as p:
        download_main = partial(downloads_and_process,dest_dir=dest_dir,output_dir=os.path.join(op_dir,"Pool"))
        ln=len(accessions)
        acc=np.array_split(accessions, (ln/numfiles)+1)
        p.map(download_main, acc)
        download_exc = partial(downloads_and_process,dest_dir=dest_dir,output_dir=os.path.join(op_dir,"Nontarget"))
        for species in config['other_species']:
            taxname=species
            accessions=get_accessions(taxname,assembly_level,ret_content)
            ln=len(accessions)
            acc=np.array_split(accessions, (ln/numfiles)+1)
            filename=f'accessions_{taxname}.txt'
            write_accessions(filename, accessions)
            exc_acc=exc_acc+len(accessions)
            p.map(download_exc, acc)
    logging.info('Took %s seconds to download other species', time() - ts)

    main_moved=len(os.listdir(os.path.join(op_dir,"Pool")))
    exc_moved=len(os.listdir(os.path.join(op_dir,"Nontarget")))
    logging.info("Found %d,%d and Moved %d,%d",main_acc,exc_acc,main_moved,exc_moved)
    
if __name__ == '__main__':
    main(sys.argv[1:])