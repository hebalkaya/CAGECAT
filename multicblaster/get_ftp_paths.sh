#!/usr/bin/bash

esearch -db assembly -query '(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter]))) AND '$1'[Organism]' | efetch -format docsum | xtract -pattern DocumentSummary -element FtpPath_RefSeq SpeciesName > $2