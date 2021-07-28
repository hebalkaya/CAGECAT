"""Module to store functions currently not used for possible future usage

Author: Matthias van den Belt
"""

import typing as t


def parse_selected_scaffolds(selected_clusters: str) -> t.Union[str, None]:
    """Returns scaffolds of the selected clusters

    Input:
        - selected_clusters: user-selected clusters. These clusters are
            separated by "\r\n"

    Output:
        - selected_scaffolds: parsed scaffolds. Is None when no clusters have
            been selected for downstream processing

    """
    if selected_clusters != "No clusters selected":
        selected_scaffolds = []

        for cluster in selected_clusters.split("\n"):
            # TODO: optimization: use regex here
            sep_index = cluster.find(")") + 1  # due to excluding last index
            # organism = cluster[:sep_index].split("(")[0].strip()
            selected_scaffolds.append(
                cluster[sep_index + 1:].strip())  # due to separation
            # character between organism and scaffold

        selected_scaffolds = "\n".join(selected_scaffolds)
    else:
        selected_scaffolds = None

    return selected_scaffolds