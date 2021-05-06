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
                              "clinker_query": ["extract_clusters"] # TODO: possibly also corason?
                              }

# TODO: create all help texts per module using script

HELP_OVERVIEW = []
HELP_TEXTS = {}

for d in HELP_OVERVIEW:
    HELP_TEXTS.update(HELP_OVERVIEW)