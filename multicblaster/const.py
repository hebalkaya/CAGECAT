EXTRACT_CLUSTERS_OPTIONS = {"selectedScaffolds": "",  # empty strings as
                            "clusterNumbers": "",  # if nothing was
                            "clusterScoreThreshold": "",  # filled in in the
                            "prefix": "",  # submission form
                            "format": "genbank",
                            "maxclusters": "99999"}  # indicates no maximum


# # TODO: add organism filtering
#
# if options["selectedScaffolds"]:
#     cmd.append("--scaffolds")
#     cmd.extend(options["selectedScaffolds"].split())
#
# if options["clusterNumbers"]:
#     cmd.append("--clusters")
#     cmd.extend(options["clusterNumbers"].strip().split())
#
# if options["clusterScoreThreshold"]:
#     cmd.extend(["--score_threshold", options["clusterScoreThreshold"]])
#
# if options["prefix"]:
#     cmd.extend(["--prefix", options["prefix"]])
#
# cmd.extend(["--format", options["format"]])
# cmd.extend(["--maximum_clusters", options["maxclusters"]])