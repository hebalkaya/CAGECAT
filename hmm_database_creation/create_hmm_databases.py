import subprocess
from copy import deepcopy
from pathlib import Path

base = Path('/hmm_db_downloads')
db_path = Path('/hmm_databases')
log_base = base / 'logs'
log_base.mkdir(parents=True, exist_ok=True)

cmd = [
    'ncbi-genome-download',
    '--section', 'refseq',
    '--refseq-categories', 'reference,representative',
    '--output-folder', base,
    '--formats', 'genbank',
    '--verbose',
    '--no-cache',
    '--retries', '1',
    '--parallel', '10'
]


min_genomes_number = {
    'fungi': 10,
    'bacteria': 50,
}

def create_cblaster_databases(kingdom, genus_file_dict):
    print(f'Creating databases for the {kingdom} kingdom')
    for genus, genus_genomes_file in genus_file_dict.items():
        print(f'\tCreating database for the {genus} genus (input file: {genus_genomes_file})')
        # genus_genome_file is a .txt with all file paths to be used when constructing the db
        out_dir = db_path / kingdom
        out_dir.mkdir(parents=True, exist_ok=True)

        out_file = out_dir / genus

        cmd = [
            "cblaster", "makedb",
            "--name", out_file.as_posix(),
            "--cpus", '10',
            "--batch", '30',
            genus_genomes_file
        ]

        db_creation_dir = log_base / 'db-creation' / kingdom
        db_creation_dir.mkdir(parents=True, exist_ok=True)
        fp = db_creation_dir / genus
        fp = fp.with_suffix('.log')

        with open(fp, 'w') as outf:
            subprocess.run(cmd, stderr=outf, stdout=outf, text=True)


def main():
    for kingdom, min_genomes in min_genomes_number.items():
        genus_dict = list_genera(kingdom)

        # write file to be used as input for ncbi-genome-download
        genus_dict = filter_invalid_genera(genus_dict, min_genomes)
        download_genome_files(kingdom, genus_dict)

        genus_file_dict = write_genus_filepaths(kingdom, genus_dict)
        create_cblaster_databases(kingdom, genus_file_dict)


def download_genome_files(kingdom, genus_dict):
    print('Writing genera_to_download.txt')
    fp = base / 'genera_to_download.txt'

    with open(fp, 'w') as outf:
        for genus in genus_dict:
            outf.write(f'{genus}\n')

    command = deepcopy(cmd)
    command.extend(['--genera', fp.as_posix()])
    command.append(kingdom)

    print(f'Downloading genome files for kingdom {kingdom}')
    genome_download_log_dir = log_base / 'genome-file-download'
    genome_download_log_dir.mkdir(parents=True, exist_ok=True)
    fp = genome_download_log_dir / kingdom
    fp = fp.with_suffix('.log')

    with open(fp, 'w') as outf:
        ret = subprocess.run(command, stderr=outf, stdout=outf, text=True)

    assert ret.returncode == 0


def filter_invalid_genera(genus_dict, min_genomes):
    print('Filtering genera with too few genome files')

    for genus in deepcopy(list(genus_dict.keys())):
        file_paths = genus_dict.get(genus)

        if len(file_paths) < min_genomes:
            print(f'\tRemoved {genus} (too few genome files)')
            genus_dict.pop(genus)

    return genus_dict


def write_genus_filepaths(kingdom, genus_dict):
    """Writes paths of genus GenBank files to a file

    To be used as input for cblaster makedb. Also, genera with too few genome
    file are removed from the dictionary
    """
    genus_file_dict = {}

    for genus in genus_dict:
        print(f'Writing genome filepaths for genus {genus}')
        file_paths = genus_dict.get(genus)

        fp = base / 'genome-files' / kingdom
        if not fp.exists():
            fp.mkdir(parents=True, exist_ok=True)

        fp = fp / f'{genus}_cblaster_makedb_files.txt'
        genus_file_dict[genus] = fp.as_posix()

        with open(fp, 'w') as outf:
            for genome_entry in file_paths:
                # genus_fp: Path
                genome_file_folder = base / 'refseq' / kingdom / genome_entry

                assert len(list(genome_file_folder.iterdir())) == 2
                for file in genome_file_folder.iterdir():
                    if file.suffix == '':  # file with MD5checksums does not have suffix
                        continue

                    outf.write(f'{file.as_posix()}\n')

    return genus_file_dict


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

            # fn = Path(base / splitted[0]).as_posix()  # splitted[0] is the filename of genbank file
            # splitted[0] is the entry name
            if genus not in genus_dict:
                genus_dict[genus] = [splitted[0]]
            else:
                genus_dict[genus].append(splitted[0])

    # TODO: implement json dump?
    return genus_dict


if __name__ == '__main__':
    main()
