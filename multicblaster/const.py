""" TODO: module docstring

"""

EXTRACT_CLUSTERS_OPTIONS = {"selectedOrganisms": "",
                            "selectedScaffolds": "",  # empty strings as
                            "clusterNumbers": "",  # if nothing was
                            "clusterScoreThreshold": "",  # filled in in the
                            "prefix": "",  # submission form
                            "format": "genbank",
                            "maxclusters": "99999"}  # indicates no maximum

# values can also be tuples
DOWNSTREAM_MODULES_OPTIONS = {"search": ["recompute", "gne",
                                         "extract_sequences",
                                         "extract_clusters",
                                         "corason", "clinker_full",
                                         "clinker_query"],
                              "recompute": ["gne", "extract_sequences",
                                            "extract_clusters",
                                            "corason", "clinker_full",
                                            "clinker_query"],
                              "corason": [],
                              "gne": [],
                              "extract_sequences": [],
                              "extract_clusters": ["clinker_full"],
                              # TODO: possible corason and clinker_query. Get query headers from .csv file
                              "clinker_full": [],
                              "clinker_query": ["extract_clusters"] # TODO: possibly also corason?
                              }

# TODO: create all help texts per module using script
GENERAL_HELPS = {'generalEnteredJobId': {'title': 'Previous job ID', 'module': '', 'text': 'The ID of the job which\' results are wished to be used.'},
                 'generalDelimiter': {'title': 'Output file delimiter', 'module': '', 'text': 'Single delimiter character to use when writing results to a file.\n\nResults will be separated of each other in the output file by the specified character.\n\nRequired: no\nDefault: no delimiter (human readable)'},
                 'generalDecimals': {'title': 'Number of decimals', 'module': '', 'text': 'Total decimal places to use when saving score values.\n\nRequired: no'},
                 'generalHideHeaders': {'title': 'Hide headers', 'module': '', 'text': 'Hide headers when saving result output.\n\nRequired: no'}}
SEARCH_HELPS = {'genomeFile': {'title': 'Query file', 'module': '', 'text': 'FASTA file containing protein sequences to be searched.'},
                'ncbiEntriesTextArea': {'title': 'Search from NCBI entries', 'module': '', 'text': 'A collection of valid NCBI sequence identifiers to be searched.\n\nEntering the same identifier twice will prevent you from continuing.'},
                'entrez_query': {'title': 'Filter using Entrez query', 'module': '', 'text': 'An NCBI Entrez search term for pre-search filtering of an NCBI database when using command line BLASTp (e.g. Aspergillus[organism]\n\nRequired: no'},
                'database_type': {'title': 'Database to search in', 'module': '', 'text': 'Database to be searched: NCBI database name.\n\nRequired: yes'},
                'max_hits': {'title': 'Maximum hits to show', 'module': '', 'text': 'Maximum total hits to save from a remote BLAST search. Setting this value too low may result in missed hits/clusters.\n\nRequired: yes'},
                'max_evalue': {'title': 'Maximum e-value', 'module': '', 'text': 'Maximum e-value for a BLAST hit to be saved.\n\nRequired: yes'},
                'min_identity': {'title': 'Minimum percent identity', 'module': '', 'text': 'Minimum percent identity for a BLAST hit to be saved.\n\nRequired: yes'},
                'min_query_coverage': {'title': 'Minimum query coverage', 'module': '', 'text': 'Minimum percent query coverage for a BLAST hit to be saved.\n\nRequired: yes'},
                'max_intergenic_gap': {'title': 'Maximum intergenic distance between genes', 'module': '', 'text': 'Maximum allowed intergenic distance (bp) between conserved hits to be considered in the same block.\n\nIf you are not sure which value to use, please refer to the Gene Neighbourhood Estimation documentation, as this will help you find a proper value.\n\nRequired: yes\nDefault value: 20000'},
                'percentageQueryGenes': {'title': 'Percentage of query genes', 'module': '', 'text': 'Filter on %% of query genes needed to be present in cluster\n\nRequired: yes'},
                'min_unique_query_hits': {'title': 'Minimum unique query sequences', 'module': '', 'text': 'Minimum number of unique query sequences that must be conservedin a hit cluster.\n\nRequired: yes'},
                'min_hits_in_clusters': {'title': 'Minimum hit number in clusters', 'module': '', 'text': 'Minimum number of hits in a cluster.\n\nRequired: yes'},
                'requiredSequencesSelector': {'title': 'Required sequences in a cluster', 'module': '', 'text': 'Names of query sequences that must be represented in a hit cluster.\n\nOnce you upload a query file or enter NCBI entries, click a sequence header to select it. Hold CTRL while clicking to select multiple sequences. To unselect a header, hold CTRL while clicking the header.\n\nRequired: no\nDefault: none selected'},
                'sortClusters': {'title': 'Sort output clusters', 'module': '', 'text': 'Sorts the clusters of the final output on score. This means that clusters of the same organism are not neccesairily close together in the output.\n\nRequired: no'},
                'intermediate_genes': {'title': 'Show intermediate genes', 'module': '', 'text': 'Show genes that in or near clusters but not part of the cluster.\n\nRequired: no'},
                'intermediate_max_distance': {'title': 'Maximum intermediate gene distance', 'module': '', 'text': 'The maximum distance between the start/end of a cluster and an intermediate gene\n\nSetting this to a higher value will allow for a broader analysis of the genome neighbourhood of each cluster.\n\nRequired: yes'},
                'intermediate_max_clusters': {'title': 'Maximum number of clusters to find intermediate genes for', 'module': '', 'text': 'The maximum amount of clusters will get intermediate genes assigned. Ordered on score.\n\nRequired: yes'}}
GNE_HELPS = {'max_intergenic_distance': {'title': 'Maximum intergenic distance', 'module': '', 'text': 'Maximum distance in bp between genes.\n\nRequired: yes'},
             'sample_number': {'title': 'Number of samples', 'module': '', 'text': 'Total samples taken from Maximum intergenic distance.\n\nRequired: yes'},
             'sampling_space': {'title': 'Sampling space', 'module': '', 'text': 'Draw sampling values from a linear or log scale.\n\nRequired: yes'}}
CLINKER_FULL_HELPS = {'noAlign': {'title': 'Do not align clusters', 'module': '', 'text': 'Do not align clusters.\n\nRequired: no'},
                      'identity': {'title': 'Minimum alignment sequence identity', 'module': '', 'text': 'Minimum alignment sequence identity.\n\nRequired: yes'},
                      'hideLinkHeaders': {'title': 'Hide alignment column headers', 'module': '', 'text': 'Hide alignment column headers.\n\nRequired: no'},
                      'hideAlignHeaders': {'title': 'Hide alignment cluster name headers', 'module': '', 'text': 'Hide alignment cluster name headers.\n\nRequired: no'},
                      'useFileOrder': {'title': 'Maintain order of input files', 'module': '', 'text': 'Display clusters in order of input files.\n\nRequired: no'}}
BINARY_TABLE_HELPS = {'keyFunction': {'title': 'Key function', 'module': '', 'text': 'Key function used when generating binary table cell values.\n\nRequired: yes'},
                      'hitAttribute': {'title': 'Hit attribute', 'module': '', 'text': 'Hit attribute used when generating binary table cell values.\n\nRequired: yes'}}
FILTERING_HELPS = {'selectedOrganisms': {'title': 'Organisms to filter fot', 'module': '', 'text': 'Organism names to filter hits for. When entering multiple organisms, separate by a space.\n\nRequired: no'},
                   'selectedScaffolds': {'title': 'TODO', 'module': '', 'text': 'TODO'},  # TODO: check if we still use it
                   'clusterNumbers': {'title': 'Cluster numbers', 'module': '', 'text': 'Cluster numbers/ranges provided by the summary file of the \'search\' command or selected online. If no numbers are entered, no filtering takes place.\n\nRequired: no'},
                   'clusterScoreThreshold': {'title': 'Cluster score threshold', 'module': '', 'text': 'Minimum score of a cluster in order to be included. If no score is entered, no filtering takes place.\n\nRequired: no'},
                   'selectedQueries': {'title': 'Query filtering', 'module': '', 'text': 'IDs of query sequences to filter for.\n\nRequired: no'}}
CLINKER_QUERY_HELPS = {'maxclusters': {'title': 'Maximum number of clusters to plot', 'module': '', 'text': 'The maximum amount of clusters that will be plotted. Ordered on score.\n\nRequired: yes'}}
EXTR_SEQS_HELPS = {'downloadSeqs': {'title': 'Download sequences', 'module': '', 'text': 'Download protein sequences for the selected proteins. The resulting summary will have a FASTA format.\n\nRequired: no'},
                   'nameOnly': {'title': 'Name only', 'module': '', 'text': 'Do not save sequence descriptions (i.e. no genomic coordinates).\n\nRequired: no'}}
EXTR_CLUST_HELPS = {'prefix': {'title': 'File prefix', 'module': '', 'text': 'Start of the name for each created cluster file, e.g. <prefix>_cluster1.\n\nRequired: no'},
                    'format': {'title': 'File format', 'module': '', 'text': 'Format of the resulting files.\n\nRequired: no'}}
CORASON_HELPS = {'selectedQuery': {'title': 'Selected query', 'module': '', 'text': 'Query to be analyzed\n\nRequired: yes'},
                 'selectedReferenceCluster': {'title': 'Selected reference cluster', 'module': '', 'text': 'TODO'},
                 'selectedClustersToSearch': {'title': 'Selected clusters to search in', 'module': '', 'text': 'TODO'}, # is this list parameter?
                 'evalue': {'title': 'Minimal e-value', 'module': '', 'text': 'Minimal e-value for a gene to be considered a hit.\n\nRequired: yes'},
                 'bitscore': {'title': 'Bitscore', 'module': '', 'text': 'TODO'},
                 'clusterRadio': {'title': 'Number of genes to analyze', 'module': '', 'text': 'Number of genes in the neighbourhood to analyze\n\nRequired: yes'},
                 'ecluster': {'title': 'e-value of genes from reference cluster', 'module': '', 'text': 'e-value for sequences from reference cluster\n\nRequired: yes'},
                 'ecore': {'title': 'TODO', 'module': '', 'text': 'e-value for Best Bidirectional Hits used to construct genomic core from clusters.\n\nRequired: yes'},
                 'rescale': {'title': 'Rescale', 'module': '', 'text': 'Increasing this number will show a bigger cluster region with smaller genes.\n\nRequired: no?'}}
# TODO: missing antismash file
HMM_HELPS  = {'selectedGenus': {'title': 'Selected genus', 'module': '', 'text': 'Genus-specific database to search in. The database is constructed of all representative or reference genomes of the selected genus.\n\nRequired: yes'},
              'hmmProfiles': {'title': 'HMM profiles', 'module': '', 'text': 'HMM profile identifiers to use when searching the selected genus database.\n\nRequired: yes'}}

# BLANC: {'input_help': {'title': 'TODO', 'module': '', 'text': 'TODO'}}

HELP_OVERVIEW = [('multiple', GENERAL_HELPS), ('search', SEARCH_HELPS),
                 ('neighbourhood', GNE_HELPS), ('clinker visualisation', CLINKER_FULL_HELPS),
                 ('search', BINARY_TABLE_HELPS), ('multiple', FILTERING_HELPS),
                 ('clinker visualisation with query', CLINKER_QUERY_HELPS), ('extract sequences',
                 EXTR_SEQS_HELPS), ('extract clusters', EXTR_CLUST_HELPS),
                 ('corason', CORASON_HELPS), ('HMM', HMM_HELPS)]

HELP_TEXTS = {}

for label, d in HELP_OVERVIEW:
    for key in d:
        d[key]['module'] = label

    HELP_TEXTS.update(d)

### Post-analysis explanation section

# format is: {module: [(paragraph_title, text), ...]}
# empty paragraph title means that no header should be generated
POST_ANALYSIS_EXPLANATIONS = {'multicblaster_search':
                                  [('', 'Query sequences are searched against the NCBI’s BLAST API in remote mode. BLAST hits are filtered according to user defined quality thresholds. In remote mode, each hit is then queried against the NCBI’s Identical Protein Groups (IPG) resource, which, as its name suggests, groups proteins sharing identical amino acid sequence as an anti-redundancy measure. The resulting IPG table contains source genomic coordinates for each hit protein sequence, which cblaster uses to group them by their corresponding organism, scaffold and subject sequences. Query sequences are searched against the NCBI’s BLAST API in remote mode. BLAST hits are filtered according to user defined quality thresholds. In remote mode, each hit is then queried against the NCBI’s Identical Protein Groups (IPG) resource, which, as its name suggests, groups proteins sharing identical amino acid sequence as an anti-redundancy measure. The resulting IPG table contains source genomic coordinates for each hit protein sequence, which cblaster uses to group them by their corresponding organism, scaffold and subject sequences.'),
                                   ('', 'In order to run a cblaster search, you will need to point the module to a collection of sequences to be used as queries. These can be provided in two ways:\n1. A FASTA format file containing amino acid sequences\n2. A list of valid NCBI sequence identifiers (e.g. accession, GI number)'),
                                   ('HMMER searches', 'To run a domain search, you need to specify the search mode as HMM, provide an array of query Pfam domain profile names and select a database (consisting of all representative/reference genomes of the selected genus stored at NCBI) to search in. This will extract the specified domain profiles (PF00001 and PF00002) from the Pfam database and search the sequences in the selected genus database for any domain hits.'),
                                   ('Result filtering', 'The default values for each filter are pretty generous, and may need changing based on your data. The search thresholds should be fairly self explanatory; any hit not meeting them are discarded from the BLAST search results.'),
                                   ('', 'The clustering thresholds, however, are a bit more interesting. These determine what conditions a candidate hit cluster must satisfy in order to be detected by cblaster. The most important parameter here is Maximum Intergenic Gap, which determines how far (in base pairs) any two hits in a cluster can be from one another. This parameter could vary wildly based on your data set. For example, in bacterial or fungal secondary metabolite gene clusters where genes are typically found very close together, a low value could be used. Conversely, plant clusters, which may involve a collection of key genes spread out over the entire chromosome, would require a much higher value. The Neighbourhood module can used to calibrate this parameter based on your results'),
                                   ('Output', 'By default, a complete summary is generated and saved to a file after the search has finished. This reports all clusters, as well as the scores and positions of each gene hit, found during the search, organized by the organisms and genomic scaffolds they belong to.'),
                                   ('Binary table', 'An easier way to digest all of the information that cblaster will produce is by using the binary table output. This generates a matrix which shows the absence/presence of query sequence (columns) hits in each result cluster (rows). By default, the binary table will only report the total number of hits per query sequence in each cluster. However, you can instead change this to some value calculated from the actual scores of hits in the clusters.'),
                                   ('', 'This is controlled by two additional parameters: Hit attribute, which determines which score attribute (‘identity’, ‘coverage’, ‘bitscore’ or ‘evalue’) to use when calculating cell values, and Key function, which determines the function (‘len’, ‘max’, ‘sum’) applied to the score attribute.'),
                                   ('', 'Each cell in the matrix refers to multiple hit sequences within each cluster. For every cell, the chosen score attribute is extracted from each hit corresponding to that cell. Then, the key function is applied to the extracted scores. The ‘len’ function calculates the length of each score list - essentially just counting the number of hits in that cell. The ‘max’ and ‘sum’ functions calculate the maximum and sum of each score list, respectively.'),
                                   ('Search sessions are saved', 'Given that searches can take a significant time to run (i.e. as long as any normal batch BLAST job will take), cblaster is capable of saving a search session to file, and loading it back later for further filtering and visualization. Once the session is saved, any subsequent runs with that session specified will make cblaster try to load it instead of performing a new search.'),
                                   ('Finding intermediate genes between hits', 'The default output for cblaster is the cluster heatmap, which shows the absence or presence of your query sequences. While we find this is generally the easiest way to pick up on patterns of cluster conservation, we also like to be able to visualize our results in their own genomic contexts so we can see the differences in gene order, orientation, size and so on.'),
                                   ('', 'For this reason, we added integration to the clinker tool (https://github.com/gamcil/clinker), which can generate highly interactive gene cluster comparison plots. However, in a regular cblaster search, we do not have access to any information about the genes between the BLAST hits shown in the heatmap. This means that if you were to run the Visualize with query clusters module on a previous job, you would produce a figure where most of the clusters are missing genes!'),
                                   ('', 'To get around this, you can use the Find intermediate genes parameter when performing a cblaster search. After the search has completed, genomic regions corresponding to the detected gene clusters are retrieved from the NCBI, and used to fill in the missing genes.')
                                   ],
                              'cblaster_query_visualization':
                                  [('', 'By default, the visualisation offered by cblaster shows only a heatmap of query hits per result cluster. While this is very useful for quickly identifying patterns in large datasets, we generally still want to see how these clusters compare in a more biologically relevant way.'),
                                   ('', 'The Visualize with query clusters module allows you to do precisely this. Given a previous job and some selected clusters, this module will automatically extract the clusters, then generate an interactive visualisation showing each cluster to-scale using clinker (doi: 10.1093/bioinformatics/btab007, https://github.com/gamcil/clinker).'),
                                   ]}