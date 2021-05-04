EXTRACT_CLUSTERS_OPTIONS = {"selectedScaffolds": "",  # empty strings as
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
                              "clinker_full": ["extract_clusters"],
                              "clinker_query": ["extract_clusters"]}

# TODO: maybe we can add module to which it belongs as well
HELP_TEXTS = { # general
              'generalDelimiter': {'title': 'TODO',
                                   'text': 'TODO'},
              'generalDecimals': {'title': 'TODO',
                                     'text': 'TODO'},
              'generalHideHeaders': {'title': 'TODO',
                                        'text': 'TODO'},
                 # search module
              'genomeFile': {'title': 'TODO',
                             'text': 'TODO'},
              'database_type': {'title': 'TODO',
                                'text': 'TODO'},
              'entrez_query': {'title': 'Entrez query',
                   'text': 'TODO'},
              'max_hits': {'title': "Maximum hits",
                           'text': "TODO"},
              'max_evalue': {'title': "Maximum e-value",
                             'text': "TODO"},
              'min_identity': {'title': "Minimum identity",
                               'text': "TODO"},
              'min_query_coverage': {'title': "Minimum query coverage",
                                     'text': "TODO"},
              'max_intergenic_gap': {'title': 'Maximum intergenic gap',
                                     'text': 'This is the explanation'},
              'percentageQueryGenes': {'title': "Percentage query genes",
                                       'text': "TODO"},
              'min_unique_query_hits': {'title': "Minimum unique query hits",
                                        'text': "TODO"},
              'min_hits_in_clusters': {'title': "Minimum hits in clusters",
                                       'text': "TODO"},
              'requiredSequencesSelector': {'title': 'TODO',
                                            'text': 'TODO'},
              'intermediate_max_distance': {'title': "Maximum distance of intermediate genes",
                                            'text': "TODO"},
              'intermediate_max_clusters': {'title': "Maximum number of clusters to get intermediate genes assigned",
                                            'text': "TODO"},
                # gne module
              'max_intergenic_distance': {'title': "Maximum intergenic distance",
                                          'text': "TODO"},
              'sample_number': {'title': "Sample number",
                                'text': "TODO"},
                # clinker full
              'identity': {'title': "Minimum alignment sequence identity",
                           'text': "TODO"},
,  , , 'keyFunction': {'title': 'TODO', 'text': 'TODO'}, 'hitAttribute': {'title': 'TODO', 'text': 'TODO'}, 'sortClusters': {'title': 'TODO', 'text': 'TODO'}, 'intermediate_genes': {'title': 'TODO', 'text': 'TODO'}, 'ncbiEntriesTextArea': {'title': 'TODO', 'text': 'TODO'}, 'generalEnteredJobId': {'title': 'TODO', 'text': 'TODO'}, 'sampling_space': {'title': 'TODO', 'text': 'TODO'}, 'hideLinkHeaders': {'title': 'TODO', 'text': 'TODO'}, 'hideAlignHeaders': {'title': 'TODO', 'text': 'TODO'}, 'useFileOrder': {'title': 'TODO', 'text': 'TODO'}}

