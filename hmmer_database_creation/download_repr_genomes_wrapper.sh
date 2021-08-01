#!/usr/bin/bash

fn_unordered="all_genera_unordered.txt"
fn="all_genera.txt"

echo "Fetching genera from NCBI"
esearch -db assembly -query '(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter])))' | efetch -format docsum | xtract -pattern DocumentSummary -element Organism > "$fn_unordered"

echo "Creating list of unique genera"
python get_unique_genera.py "$fn_unordered" "$fn"
rm "$fn_unordered"

echo "Downloading genomes"
lines=$(cat "$fn")
for line in $lines
do
  python download_refseqs.py "$line"
done

echo "Removing $fn"
rm "$fn"

echo "Finished!"
touch