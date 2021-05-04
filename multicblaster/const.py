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

HELP_TEXTS = {"max_intergenic_gap": {"title": "Maximum intergenic gap",
                                     "text": "This is the explanation"},
              "entrez_query": {"title": "Huize Wunderlich",
                               "text": "HAHA HALLO DAAR ROSAN"}}