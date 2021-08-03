#!/usr/bin/bash

# TODO: remove previous databases, create them all over again to include new genomes

fn_non_unique="non_unique_genera.txt"
fn_unique="unique_genera.txt"

echo "If you try to rerun this script, make sure to remove any unmoved files.."
echo ".. from the default RefSeq GBKS storage folder to prevent missing a file"

echo " Fetching all genera from NCBI"
esearch -db assembly -query '(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter])))' | efetch -format docsum | xtract -pattern DocumentSummary -element Organism > "$fn_non_unique"

echo " Creating list of unique genera"
total_genera=$(python get_unique_genera.py "${fn_non_unique}" "${fn_unique}")

i=0
echo " Downloading genomes"
for genus in $(cat "$fn_unique")
do
  i=$((i+1))

  echo " Processing ${genus} (${i} of ${total_genera})"
  echo "   -> Fetching FTP paths"
  esearch -db assembly -query '(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter]))) AND '${genus}'[Organism]' | efetch -format docsum | xtract -pattern DocumentSummary -element FtpPath_RefSeq SpeciesName > "${genus}_ftp_paths.txt"

  echo "   -> Downloading files"
  python download_files.py "${genus}_ftp_paths.txt"
done

echo "Creating file to stop creating databases"
python download_files.py 'everything_has_been_downloaded'

echo "Removing ftp paths files"
rm *_ftp_paths.txt

# TODO: maybe add compression for all refseqs
# TODO: remove too_few_species.txt
echo "Done!"