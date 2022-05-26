""""Stores help texts shown to the user when the help-button is clicked

These dictionaries are referenced to when a request is made to the help-text
URL with the key name in that URL to get the appropriate help text. After
changes have been made to this module, uWSGI should be reloaded using:

uwsgi --reload /tmp/uwsgi-master.pid

within the Docker container

Author: Matthias van den Belt
"""

from cagecat.const import fasta_extensions, genbank_extensions

job_details = {
    'job_title': {
        'title': 'Job title',
        'module': '',
        'text': 'Enter a job title to label your analyses and enable quick identification of your executed jobs.\n\nRequired: no\n\nMaximum length: 60 characters'
    },
    'email_notification': {
        'title': 'Email notification',
        'module': '',
        'text': 'Enter your e-mail to get notified when your job has finished. Your email will be removed from our database after one notification mail.\n\nRequired: no'
    }
}

general = {
    # 'generalEnteredJobId': {
    #     'title': 'Previous job ID',
    #     'module': '',
    #     'text': 'The ID of the job which\' results are wished to be used.'
    # },
    'generalDelimiter': {
        'title': 'Output file delimiter',
        'module': '',
        'text': 'Single delimiter character that will be used when writing results to a file.\n\nResults in the summary file will be separated of each other in the by the specified character. Can be left empty, in which case the summary file is formatted in a human readable form.\n\nRequired: no\nDefault: no delimiter (human readable)'
    },
    'generalDecimals': {
        'title': 'Number of decimals',
        'module': '',
        'text': 'Number of decimal places to use when saving score values.\n\nRequired: yes'
    },
    'generalHideHeaders': {
        'title': 'Hide column headers',
        'module': '',
        'text': 'Enabling this option hides the headers (first row of file indicating the following columns: organism, scaffold, start, end, score, query_id) of the found hits when writing to this output file. when saving result output.\n\nRequired: no'
    }
}

cblaster_search = {
    'genomeFile': {
        'title': 'File with query proteins',
        'module': '',
        'text': 'File containing protein/nucleotide sequences (FASTA) or a GenBank (not GenPept) file with the regions of interest (not a full genome, which will cause an error) to be searched.\n\n',
        'frame': ''.join([
          '<span>Allowed extensions:</span>'
          '<ul>',
            ''.join([f'<li>{ext[1:]}</li>' for ext in fasta_extensions + genbank_extensions]),
          '</ul>'
        ])
    },
    'ncbiEntriesTextArea': {
        'title': 'Search from NCBI identifiers',
        'module': '',
        'text': 'A collection of valid NCBI sequence identifiers to be searched.\n\nNCBI identifiers should be separated by a newline (enter).\n\nEntering invalid identifiers will not halt the analysis, but the invalid identifiers are not used in the analysis. Likewise, duplicate identifiers will be used once in your analysis.'
    },
    'entrez_query': {
        'title': 'Filter results using Entrez query',
        'module': '',
        'text': 'An NCBI Entrez term for filtering of the NCBI database during your analysis. Your search results will be restricted to the sequences in the database adhering to this Entrez term.(e.g. Aspergillus[organism])\n\nRequired: no',
        'frame': '<a target="_blank" href="https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=FAQ#Organism">Additional explanation</a>'
    },
    'database_type': {
        'title': 'Type of NCBI Database to search',
        'module': '',
        'text': 'The type of NCBI database to be searched. Click the links below for a detailed explanation of the contents of each database.\n\nRequired: yes',
        'frame': '<ul>'
                 
                 '<li>'
                 '<a target="_blank" href="https://blast.ncbi.nlm.nih.gov/getDBInfo.cgi?CMD=getDbInfo&DB_PATH=nr&IS_PROT=on&IS_COMPLETE=on">'
                 'nr'
                 '</a>'
                 '</li>'

                 '<li>'
                 '<a target="_blank" href="https://blast.ncbi.nlm.nih.gov/getDBInfo.cgi?CMD=getDbInfo&DB_PATH=refseq_protein&IS_PROT=on&IS_COMPLETE=on">'
                 'RefSeq protein'
                 '</a>'
                 '</li>'

                 '<li>'
                 '<a target="_blank" href="https://blast.ncbi.nlm.nih.gov/getDBInfo.cgi?CMD=getDbInfo&DB_PATH=swissprot&IS_PROT=on&IS_COMPLETE=on">'
                 'Swissprot'
                 '</a>'
                 '</li>'

                 '<li>'
                 '<a target="_blank" href="https://blast.ncbi.nlm.nih.gov/getDBInfo.cgi?CMD=getDbInfo&DB_PATH=pdb&IS_PROT=on&IS_COMPLETE=on">'
                 'pdbaa'
                 '</a>'
                 '</li>'
                 
                 '</ul>'
    },
    'max_hits': {
        'title': 'Maximum hits to save',
        'module': '',
        'text': 'Maximum number of hits to save from a remote BLAST search. Setting this value too low may result in missed hits/clusters.\n\nRequired: yes'
    },
    'max_evalue': {
        'title': 'Maximum e-value',
        'module': '',
        'text': 'Maximum e-value for a BLAST hit to be saved to the results.\n\nRequired: yes'
    },
    'min_identity': {
        'title': 'Minimum percent identity',
        'module': '',
        'text': 'Minimum percent identity with your input sequencess in order for a BLAST hit to be saved.\n\nRequired: yes'
    },
    'min_query_coverage': {
        'title': 'Minimum percent query coverage',
        'module': '',
        'text': 'Minimum percent query coverage in order for a BLAST hit to be saved.\n\nRequired: yes'
    },
    'max_intergenic_gap': {
        'title': 'Maximum intergenic distance between genes',
        'module': '',
        'text': 'Maximum allowed intergenic distance (bp) between conserved hits to be considered in the same cluster block.\n\nIf you are not sure which value to use, please refer to the Gene Neighbourhood Estimation documentation, as this will help you find a proper value.\n\nRequired: yes\nDefault value: 20000',
        'frame': '<a href="https://cagecat.bioinformatics.nl/tools/explanation">Gene Neighbourhood Estimation documentation</a>'
    },
    'percentageQueryGenes': {
        'title': 'Minimum percentage of query genes present in clusters',
        'module': '',
        'text': 'Minimum percentage of query genes that must be present in clusters hits.\n\nRequired: yes'
    },
    'min_unique_query_hits': {
        'title': 'Minimum unique query sequences',
        'module': '',
        'text': 'Minimum number of unique query sequences that must be present in cluster hits.\n\nRequired: yes'
    },
    'min_hits_in_clusters': {
        'title': 'Minimum number of query hits in clusters',
        'module': '',
        'text': 'Minimum number of query hits in a cluster.\n\nRequired: yes'
    },
    'requiredSequencesSelector': {
        'title': 'Required sequences in a cluster',
        'module': '',
        'text': 'Identifiers of query sequences that must be present in cluster hits.\n\nOnce you upload a query file or enter NCBI identifiers, click a sequence header to select it. Hold CTRL while clicking to select multiple sequences. To unselect a header, hold CTRL while clicking the header. A blue/gray background indicates that that sequence is selected.\n\nRequired: no\nDefault: none selected'
    },
    'sortClusters': {
        'title': 'Sort output clusters',
        'module': '',
        'text': 'Sorts the clusters of the final output on cluster score. This means that clusters of the same organism are not necessarily close together in the output.\n\nRequired: no'
    },
    'intermediate_genes': {
        'title': 'Save intermediate genes of clusters',
        'module': '',
        'text': 'Save genes that are in or near clusters but not part of the cluster.\n\nRequired: no'
    },
    'intermediate_max_distance': {
        'title': 'Maximum intermediate gene distance',
        'module': '',
        'text': 'The maximum distance (bp) between the start/end of a cluster and an intermediate gene\n\nSetting this to a higher value will allow for a broader analysis of the genome neighbourhood of each cluster.\n\nRequired: yes'
    },
    'intermediate_max_clusters': {
        'title': 'Maximum number of clusters to find intermediate genes for',
        'module': '',
        'text': 'The maximum number of clusters for which intermediate genes will be assigned. Ordered on score.\n\nRequired: yes'
    }
}

cblaster_gne = {
    'max_intergenic_distance': {
        'title': 'Maximum intergenic distance',
        'module': '',
        'text': 'Maximum distance (bp) between genes when classifying the combination of these genes in to a cluster.\n\nRequired: yes'
    },
    'sample_number': {
        'title': 'Number of samples',
        'module': '',
        'text': 'Total samples taken from Maximum intergenic distance.\n\nRequired: yes\n\nExample (linear scale):\nMax. intergenic distance: 100000\nNumber of samples: 100\n\nExecuted with: distance=0, distance=1000, distance=2000, ... distance=100000.'
    },
    'sampling_space': {
        'title': 'Sampling space',
        'module': '',
        'text': 'Draw sampling values from a linear or log scale (also see help of "Number of samples").\n\nRequired: yes'
    }
}

clinker = {
    'noAlign': {
        'title': 'Don\t align clusters',
        'module': '',
        'text': 'Checking this will result in non-aligned clusters in your output plot.\n\nRequired: no'
    },
    'identity': {
        'title': 'Minimum alignment sequence identity',
        'module': '',
        'text': 'Minimum alignment sequence identity to colour a link between two genes.Can be changed afterwards\n\nRequired: yes'
    },

    # TODO: do these even matter? no difference observed
    'hideLinkHeaders': {
        'title': 'Hide alignment column headers',
        'module': '',
        'text': 'Hide alignment column headers.\n\nRequired: no'
    },
    'hideAlignHeaders': {
        'title': 'Hide alignment cluster name headers',
        'module': '',
        'text': 'Hide alignment cluster name headers.\n\nRequired: no'
    },
    # --- do these even matter? no difference observed

    'useFileOrder': {
        'title': 'Maintain order of input files',
        'module': '',
        'text': 'Display clusters in order of input files.\n\nRequired: no'
    },
    'fileUploadClinker': {
        'title': 'Genome file(s)',
        'module': '',
        'text': 'One or more GenBank file(s) which should be visualized. Whole genome files are not supported, so restrict your input to the proteins of interest\n\nRequired: yes',
        'frame': ''.join([
            '<span>Allowed extensions:</span>'
            '<ul>',
            ''.join([f'<li>{ext[1:]}</li>' for ext in genbank_extensions]),
            '</ul>'
        ])
    }
}

cblaster_search_binary_table = {
    'keyFunction': {
        'title': 'Key function',
        'module': '',
        'text': 'Used function to calculate statistics per query per cluster hit. To select the attribute to be used, select at the "Hit attribute" input.\n\nRequired: yes',
        'frame':
            'Additional explanation:'
            '<ul>'
            
            '<li>'
            'Length: write the query count presence in cluster hits'
            '</li>'
            
            '<li>'
            'Sum: write the sum per query of the selected attribute'
            '</li>'
            
            '<li>'
            'Max: write the maximum value per query of the selected attribute'
            '</li>'
            
            '</ul>'
    },
    'hitAttribute': {
        'title': 'Hit attribute',
        'module': '',
        'text': 'The hit attribute used when generating the binary binary table cell values of hits per querycblast. Is available when the Binary "Key function" is not "length"\n\nRequired: yes',

    }
}

cblaster_search_filtering = {
    # 'selectedScaffolds': {'title': '',
    # 'module': '', 'text': ''},
    'clusterNumbers': {
        'title': 'Cluster numbers',
        'module': '',
        'text': 'Cluster numbers/ranges as noted in the summary file, which should be selected on the previous page. If no numbers are entered, no filtering takes place.\n\nThese numbers are pre-filled (dependent on the clusters you selected in the previous window), and can not be changed on this page. To change these clusters, return to the previous page and select the clusters of interest.\n\nRequired: no'
    },
    'clusterScoreThreshold': {
        'title': 'Cluster score threshold',
        'module': '',
        'text': 'Minimum score of a cluster in order to be included in your results. If no score is entered, no filtering takes place. Scores of clusters can be inspected in the plot or summary table.\n\nRequired: no'
    },
    'selectedQueries': {
        'title': 'Result filtering by queries',
        'module': '',
        'text': 'IDs of query sequences to filter for. Only cluster hits that contain these queries are present in your output. Can be selected on the previous page.\n\nRequired: no'
    }
}

cblaster_plot_clusters = {
    'maxclusters': {
        'title': 'Maximum number of clusters to plot',
        'module': '',
        'text': 'The maximum amount of clusters that will be plotted. The clusters with the highest score will plotted.\n\nRequired: yes'
    }
}

cblaster_extract_sequences = {
    'downloadSeqs': {
        'title': 'Download sequences',
        'module': '',
        'text': 'Download protein sequences for the selected proteins. The resulting summary will have a FASTA format.\n\nRequired: no'
    },
    'nameOnly': {
        'title': 'Name only',
        'module': '',
        'text': 'Do not save sequence descriptions (i.e. no genomic coordinates).\n\nRequired: no'
    },
    'selectedOrganisms': {
        'title': 'Organisms to filter fot',
        'module': '',
        'text': 'Organism names to filter hits for (inclusive). When entering multiple organisms, separate by a space.\n\nRequired: no'
    },
}

cblaster_extract_clusters = {
    'prefix': {
        'title': 'File prefix',
        'module': '',
        'text': 'Start of the name for each created cluster file, e.g. <prefix>cluster1.\n\nRequired: no'
    },
    'format': {
        'title': 'File format',
        'module': '',
        'text': 'Format of the resulting files.\n\nRequired: no'
    }
}

# CORASON_HELPS = {'selectedQuery': {'title': 'Selected query',
# 'module': '', 'text': 'Query to be analyzed\n\nRequired: yes'},
#                  'selectedReferenceCluster': {'title': 'Selected reference cluster',
#                  'module': '', 'text': 'The cluster number of which cluster should act as the reference cluster. The cluster numbers correspond with the cluster numbers of the preceding job. Note that the reference cluster must include the query gene, or Corason will fail to execute.\n\nRequired: yes'},
#                  'selectedClustersToSearch': {'title': 'Selected clusters to search in',
#                  'module': '', 'text': 'TODO'}, # is this list parameter?
#                  'evalue': {'title': 'Minimal e-value',
#                  'module': '', 'text': 'Minimal e-value for a gene to be considered a hit.\n\nRequired: yes'},
#                  'bitscore': {'title': 'Bitscore',
#                  'module': '', 'text': 'TODO'},
#                  'clusterRadio': {'title': 'Number of genes to analyze',
#                  'module': '', 'text': 'Number of genes in the neighbourhood to analyze\n\nRequired: yes'},
#                  'ecluster': {'title': 'e-value of genes from reference cluster',
#                  'module': '', 'text': 'e-value for sequences from reference cluster\n\nRequired: yes'},
#                  'ecore': {'title': 'TODO',
#                   'module': '', 'text': 'e-value for Best Bidirectional Hits used to construct genomic core from clusters.\n\nRequired: yes'},
#                  'rescale': {'title': 'Rescale',
#                  'module': '', 'text': 'Increasing this number will show a bigger cluster region with smaller genes.\n\nRequired: no?'}}

cblaster_search_hmm_mode = {
    'selectedGenus': {
        'title': 'Selected genus',
        'module': '',
        'text': 'Genus-specific database to search in. The database is constructed of all representative or reference genomes of the selected genus.\n\nRequired: yes'
    },
    'hmmProfiles': {
        'title': 'HMM profiles',
        'module': '',
        'text': 'Valid HMM profile identifiers from Pfam (e.g. "PF00452") to use when searching the selected genus database.\n\nRequired: yes',
        'frame':
            '<a target="_blank" href="https://pfam.xfam.org/">Link to Pfam</a>'
    }
}

all_helps = [('multiple', job_details), ('multiple', general), ('search', cblaster_search), ('neighbourhood', cblaster_gne),
             ('clinker visualisation', clinker), ('search', cblaster_search_binary_table), ('multiple', cblaster_search_filtering),
             ('clinker visualisation with query', cblaster_plot_clusters), ('extract sequences', cblaster_extract_sequences),
             ('extract clusters', cblaster_extract_clusters), ('HMM', cblaster_search_hmm_mode),  # ('corason', CORASON_HELPS)
             ]
help_texts = {}

# BLANC: {'input_help': {'title': 'blanc',
# 'module': '', 'text': 'blanc'}}

for label, d in all_helps:
    for key in d:
        d[key]['module'] = label

    help_texts.update(d)
