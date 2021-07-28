"""Module to hold all parsing and formatting functions

Author: Matthias van den Belt
"""

# package imports
import re
from more_itertools import consecutive_groups

# own project imports
import cagecat.utils as ut

# typing imports
import typing as t

### Function definitions
def parse_selected_cluster_names(selected_clusters: str) \
        -> t.Union[str, None]:
    """Extracts and formats selected clusters in a readable manner

    Input:
        - selected_clusters: user-selected clusters. These clusters are
            separated by "\r\n"

    Output:
        - cluster_names: parsed cluster names. Returns None when no clusters
            were selected. For CORASON, this should never happen, as
            it always needs clusters to search in
    """
    if selected_clusters != "No clusters selected":
        cluster_names = []

        for cluster in selected_clusters.split("\r\n"):
            sep_index = cluster.find(")") + 1
            organism = cluster[:sep_index].split("(")[0].strip()
            clust_num = int(re.findall(ut.CLUST_NUMBER_PATTERN_W_SCORE, cluster)[0])

            cluster_names.append(f"{organism} (Cluster {clust_num})")

        cluster_names = "\n".join(cluster_names)
    else:
        cluster_names = None

    return cluster_names


def format_cluster_numbers(cluster_numbers: t.List[int]) -> t.List[str]:
    """Pretty formats the selected cluster numbers in a sorted way

    Input:
        - cluster_numbers: parsed user-selected cluster numbers

    Output:
        - pretty formatted cluster numbers. Consecutive cluster numbers are
            shown in the following way: [3, 2, 1, 8] becomes ["1-3", "8"]
    """
    cluster_numbers.sort()
    groups = [list(g) for g in consecutive_groups(cluster_numbers)]
    return [f"{g[0]}-{g[-1]}" if len(g) != 1 else str(g[0]) for g in groups]


def parse_selected_cluster_numbers(selected_clusters: str,
                                   pattern: str,
                                   format_nicely: bool = True) -> str:
    """Parses the cluster numbers of the user-selected clusters

    Input:
        - selected_clusters: user-selected clusters. These clusters are
            separated by "\r\n"
        - pattern: appropriate pattern to use to parse selected cluster
            numbers. This changes as some modules use a different format
            to show their clusters
        - format_nicely: create nicely formatted (e.g. 1 & 2 & 3 & 5
            becomes 1-3 5) or create a functional format (e.g. 1,2,3,5).
            What is desired is dependent on what code is called after this
            function.

    Output:
        - cluster_numbers: extracted cluster numbers separated by a space.
            Consecutive numbers are merged by the format_cluster_numbers
            function. Example: [1, 8, 3, 2] becomes ["1-3", "8"]. Is an
            empty string when no clusters have been selected. Not None, as
            this value is used to set the value of the input area of
            cluster numbers in HTML.
    """
    if selected_clusters:  # empty string evaluates to False
        cluster_numbers = []

        for cluster in selected_clusters.split("\r\n"):
            cluster_numbers.append(int(re.findall(pattern,
                                                  cluster)[0]))

        if format_nicely:
            cluster_numbers = " ".join(format_cluster_numbers(cluster_numbers))
        else:
            cluster_numbers = ",".join([str(n) for n in cluster_numbers])
    else:
        cluster_numbers = ""

    return cluster_numbers
