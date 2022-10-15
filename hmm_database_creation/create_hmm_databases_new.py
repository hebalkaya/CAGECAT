import copy
import subprocess
import json
from copy import deepcopy
from pathlib import Path

cmd = [
    'ncbi-genome-download',
    '--section', 'refseq',
    '--refseq-categories', 'reference,representative',
    '--output-folder', '/hmm_databases/',
    '--formats', 'genbank',
    '--verbose',
    '--no-cache',
    '--retries', '1',
    '--parallel', '5'
]

# end result:
# <genus>.txt
# gf1
# gff2
min_genomes_number = {
    'fungi': 10,
    'bacteria': 50,
}


def main():
    for kingdom, min_genomes in min_genomes_number.items():
        genus_dict = list_genera(kingdom)
        write_genus_filepaths(kingdom, genus_dict, min_genomes)

        # write file to be used as input for ncbi-genome-download
        download_genome_files(kingdom, genus_dict)

        # TODO: create databases. shall we do it here?


def download_genome_files(kingdom, genus_dict):
    print('Writing genera_to_download.txt')
    fp = base / 'genera_to_download.txt'
    with open(fp, 'w') as outf:
        for genus in genus_dict:
            outf.write(f'{genus}\n')

    command = deepcopy(cmd)
    command.extend(['--genera', fp.as_posix()])
    command.append(kingdom)

    print('Downloading genome files')
    subprocess.run(command)


def write_genus_filepaths(kingdom, genus_dict, min_genomes):
    """Writes paths of genus GenBank files to a file

    To be used as input for cblaster makedb. Also, genera with too few genome
    file are removed from the dictionary
    """
    print('Writing all filepaths per genus')
    for genus in deepcopy(list(genus_dict.keys())):
        file_paths = genus_dict.get(genus)

        if len(file_paths) < min_genomes:
            print(f'\tSkipped genus {genus} (too few genome files)')
            genus_dict.pop(genus)
            continue

        fp = base / 'ftp-paths' / kingdom
        if not fp.exists():
            fp.mkdir(parents=True, exist_ok=True)

        fp = fp / f'{genus}_cblaster_makedb_files.txt'

        with open(fp, 'w') as outf:
            for genus_fp in file_paths:
                # genus_fp: Path
                outf.write(f'{genus_fp}\n')


def list_genera(kingdom):
    print(f'Listing all genera genome files of the {kingdom} kingdom')
    genus_dict = {}
    fp = base / f'{kingdom}_all_genera'
    fp = fp.with_suffix('.txt')

    command = deepcopy(cmd)
    command.append('--dry-run')
    command.append(kingdom)

    with open(fp, 'w') as outf:
        subprocess.run(command, stderr=outf, stdout=outf, text=True)
    with open(fp) as inf:
        for line in inf:
            if line.startswith('INFO') or line.startswith('Considering'):
                continue

            splitted = line.strip().split('\t')
            genus = splitted[1].split()[0]  # example of splitted[1]: 'Schizosaccharomyces pombe'

            fn = Path(base / splitted[0]).as_posix()  # splitted[0] is the filename of genbank file
            if genus not in genus_dict:
                genus_dict[genus] = [fn]
            else:
                genus_dict[genus].append(fn)

    return genus_dict


if __name__ == '__main__':
    base = Path('/hmm_db_downloads')
    main()
