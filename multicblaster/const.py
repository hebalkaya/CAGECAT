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
                              "extract_clusters": ["corason", "clinker_full",
                                                   "clinker_query"],
                              "clinker_full": [],
                              "clinker_query": ["extract_clusters"] # TODO: possibly also corason?
                              }

# TODO: create all help texts per module using script
GENERAL_HELPS = {'generalEnteredJobId': {'title': 'Previous job ID', 'module': 'TODO', 'text': 'TODO'}, 'generalDelimiter': {'title': 'Output file delimiter', 'module': 'TODO', 'text': 'TODO'}, 'generalDecimals': {'title': 'Number of decimals', 'module': 'TODO', 'text': 'TODO'}, 'generalHideHeaders': {'title': 'Hide headers', 'module': 'TODO', 'text': 'TODO'}}
SEARCH_HELPS = {'genomeFile': {'title': 'Query file', 'module': 'TODO', 'text': 'TODO'}, 'ncbiEntriesTextArea': {'title': 'Search from NCBI entries', 'module': 'TODO', 'text': 'TODO'}, 'entrez_query': {'title': 'Filter using Entrez query', 'module': 'TODO', 'text': 'TODO'}, 'database_type': {'title': 'Database to search in', 'module': 'TODO', 'text': 'TODO'}, 'max_hits': {'title': 'Maximum hits to show', 'module': 'TODO', 'text': 'TODO'}, 'max_evalue': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'min_identity': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'min_query_coverage': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'max_intergenic_gap': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'percentageQueryGenes': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'min_unique_query_hits': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'min_hits_in_clusters': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'requiredSequencesSelector': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'sortClusters': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'intermediate_genes': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'intermediate_max_distance': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'intermediate_max_clusters': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
GNE_HELPS = {'max_intergenic_distance': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'sample_number': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'sampling_space': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
CLINKER_FULL_HELPS = {'noAlign': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'identity': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'hideLinkHeaders': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'hideAlignHeaders': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'useFileOrder': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
BINARY_TABLE_HELPS = {'keyFunction': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'hitAttribu te': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
FILTERING_HELPS = {'selectedOrganisms': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'selectedScaffolds': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'clusterNumbers': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'clusterScoreThreshold': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'selectedQueries': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
CLINKER_QUERY_HELPS = {'maxclusters': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
EXTR_SEQS_HELPS = {'downloadSeqs': {'title': 'Download sequences', 'module': 'TODO', 'text': 'TODO'}, 'nameOnly': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
EXTR_CLUST_HELPS = {'prefix': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'format': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}
CORASON_HELPS = {'selectedQuery': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'selectedReferenceCluster': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'selectedClustersToSearch': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'evalue': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'bitscore': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'clusterRadio': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'ecluster': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'ecore': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}, 'rescale': {'title': 'TODO', 'module': 'TODO', 'text': 'TODO'}}

HELP_OVERVIEW = [('multiple', GENERAL_HELPS), ('search', SEARCH_HELPS),
                 ('gne', GNE_HELPS), ('clinker_full', CLINKER_FULL_HELPS),
                 ('search', BINARY_TABLE_HELPS), ('multiple', FILTERING_HELPS),
                 ('clinker_query', CLINKER_QUERY_HELPS), ('extract_sequences',
                 EXTR_SEQS_HELPS), ('extract_clusters', EXTR_CLUST_HELPS),
                 ('corason', CORASON_HELPS)]
HELP_TEXTS = {}

for label, d in HELP_OVERVIEW:
    for key in d:
        d[key]['module'] = label

    HELP_TEXTS.update(d)