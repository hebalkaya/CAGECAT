"""Stores (helper) functions to execute when a submitted job will be executed

Author: Matthias van den Belt
"""
# package imports

# own project imports
import os.path

from multicblaster.workers_helpers import *
import config

# Whenever a CMD is ran from a function, all print statements within that
# same function are performed when the CMD has finished

### redis-queue functions
def forge_database_args(options):

    # TODO: handle recompute scenario
    base = ['--database']
    if options['mode'] in ('hmm', 'combi_remote'):
        base.append(os.path.join(config.CONF['MOUNTED_DB_FOLDER'], f'{options["selectedGenus"]}.fasta'))
        # TODO: should me modular

    if options['mode'] in ('remote', 'combi_remote'):
        if 'database_type' in options:
            base.append(options['database_type'])
        else:  # when recomputing it's not there
            return []

    if len(base) not in (2, 3):
        raise IOError('Incorrect database arguments length')

    return base


def cblaster_search(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)

    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)
    recompute = False

    # create the base command, with all required fields
    cmd = ["cblaster", "search",
           "--output", os.path.join(RESULTS_PATH, f"{job_id}_summary.txt"),
           "--plot", os.path.join(RESULTS_PATH, f"{job_id}_plot.html"),
           "--blast_file", os.path.join(RESULTS_PATH, f"{job_id}_blasthits.txt"),
           "--mode", options["mode"]]

    cmd.extend(forge_database_args(options))
    # add input options
    if options['mode'] in ('remote', 'combi_remote'):
        input_type = options["inputType"]

        if input_type == "fasta":
            cmd.extend(["--query_file", file_path])
            session_path = os.path.join(RESULTS_PATH, f"{job_id}_session.json")
            store_query_sequences_headers(LOG_PATH, input_type, file_path)
        elif input_type == "ncbi_entries":
            entries = options["ncbiEntriesTextArea"].split()

            cmd.append("--query_ids")
            cmd.extend(entries)

            session_path = os.path.join(RESULTS_PATH, f"{job_id}_session.json")
            store_query_sequences_headers(LOG_PATH, input_type, entries)
        elif input_type == "prev_session":
            recompute = True
            cmd.extend(["--recompute",
                        os.path.join(RESULTS_PATH, f"{job_id}_session.json")])
            session_path = file_path

        else:  # future input types and prev_session
            raise NotImplementedError(f"Input type {input_type} is not supported "
                                      f"in cblaster_search")

            # add search options
        if not recompute:
            cmd.extend([
                # "--database", options["database_type"],
                "--hitlist_size", options["hitlist_size"]])

            if options["entrez_query"]:
                cmd.extend(["--entrez_query", options["entrez_query"]])

    if options['mode'] in ('hmm', 'combi_remote'):
        session_path = os.path.join(RESULTS_PATH, f"{job_id}_session.json")

        # add HMM profiles
        cmd.append('--query_profiles')
        cmd.extend(options["hmmProfiles"].split())

        # PFAM database
        cmd.extend(['--database_pfam', config.DATABASE_FOLDER])

        # database to search in
        # cmd.extend(['--database', os.path.join(config.DATABASE_FOLDER, 'Streptomyces.fasta')])

    cmd.extend(["--session_file", session_path])



    # add filtering options
    cmd.extend(["--max_evalue", options["max_evalue"],
                "--min_identity", options["min_identity"],
                "--min_coverage", options["min_query_coverage"]])

    # add clustering options
    cmd.extend(["--gap", options["max_intergenic_gap"],
                "--unique", options["min_unique_query_hits"],
                "--min_hits", options["min_hits_in_clusters"],
                "--percentage", options["percentageQueryGenes"]])

    if options["requiredSequences"]:  # as empty string evaluates to False
        cmd.append("--require")
        for q in options["requiredSequences"].split(";"):
            cmd.append(f"{q.strip().split()[0]}")  # to prevent 1 header to be interpreted
                                    # as multiple due to spaces in header

    # add summary table
    cmd.extend(create_summary_table_commands('search', options))

    # add binary table
    cmd.extend(["--binary",
                os.path.join(RESULTS_PATH, f"{job_id}_binary.txt")])

    bin_table_delim = options["searchBinTableDelim"]
    if bin_table_delim:
        cmd.extend(["--binary_delimiter", bin_table_delim])

    cmd.extend(["--binary_decimals", options["searchBinTableDecimals"]])

    if "searchBinTableHideHeaders" in options:
        cmd.append("--binary_hide_headers")

    cmd.extend(["--binary_key", options["keyFunction"]])

    # TODO: maybe it can also be used with len as keyfunction
    if "hitAttribute" in options:  # only when keyFunction is not len
        cmd.extend(["--binary_attr", options["hitAttribute"]])

    # add additional options
    if "sortClusters" in options:
        cmd.append("--sort_clusters")

    # add intermediate genes options
    if "intermediate_genes" in options:
        cmd.extend(["--intermediate_genes",
                "--max_distance", options["intermediate_max_distance"],
                "--maximum_clusters", options["intermediate_max_clusters"],
                "--ipg_file", os.path.join(RESULTS_PATH, f"{job_id}_ipg.txt")])

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


def cblaster_gne(job_id, options=None, file_path=None):
    """

    :param job_id:
    :param options:
    :param file_path: session file path
    :return:
    """
    pre_job_formalities(job_id)

    _, log_path, results_path = generate_paths(job_id)

    session_path = file_path

    cmd = ["cblaster", "gne", session_path,
           "--max_gap", options["max_intergenic_distance"],
           "--samples", options["sample_number"],
           "--scale", options["sampling_space"],
           "--plot", os.path.join(results_path, f"{job_id}_plot.html"),
           "--output", os.path.join(results_path, f"{job_id}_summary.txt")]

    cmd.extend(create_summary_table_commands('gne', options))

    return_code = run_command(cmd, log_path, job_id)

    post_job_formalities(job_id, return_code)


def cblaster_extract_sequences(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    extension = "txt"
    if "downloadSeqs" in options:
        extension = "fasta"

    cmd = ["cblaster", "extract", file_path,
           "--output", os.path.join(RESULTS_PATH, f"{job_id}_sequences.{extension}")]

    cmd.extend(create_filtering_command(options, False))

    if "outputDelimiter" in options and options["outputDelimiter"]:
        cmd.extend(["--delimiter", options["outputDelimiter"]])

    if "nameOnly" in options:
        cmd.append("--name_only")

    if "downloadSeqs" in options:
        cmd.append("--extract_sequences")

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


def cblaster_extract_clusters(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    # cluster_dir = os.path.join(RESULTS_PATH, "clusters")
    # os.mkdir(cluster_dir)

    cmd = ["cblaster", "extract_clusters", file_path,
           "--output", RESULTS_PATH]

    cmd.extend(create_filtering_command(options, True))

    if options["prefix"]:
        cmd.extend(["--prefix", options["prefix"]])

    cmd.extend(["--format", options["format"]])

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


def clinker_full(job_id, options=None, file_path=None):
    """

    :param job_id:
    :param options:
    :param file_path: is path with following structure: multicblaster/jobs/prev_job_id/results/*.gbk to select all gbk files

    :return:
    """
    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    cmd = ["clinker", file_path,
           "--jobs", "1",
           "--session", os.path.join(RESULTS_PATH, f"{job_id}_session.json"),
           "--output", os.path.join(RESULTS_PATH, "alignments.txt"),
           "--plot", os.path.join(RESULTS_PATH, f"{job_id}_plot.html")]
    # TODO: implement ranges

    if "noAlign" in options:
        cmd.append("--no_align")

    cmd.extend(["--identity", options["identity"]])

    if options["clinkerDelim"]:  # empty string evaluates to false
        cmd.extend(["--delimiter", options["clinkerDelim"]])

    cmd.extend(["--decimals", options["clinkerDecimals"]])

    if "hideLinkHeaders" in options:
        cmd.append("--hide_link_headers")

    if "hideAlignHeaders" in options:
        cmd.append("--hide_aln_headers")

    if "useFileOrder" in options:
        cmd.append("--use_file_order")

    return_code = run_command(cmd, LOG_PATH, job_id)

    post_job_formalities(job_id, return_code)


def clinker_query(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)
    # print("We are in clinker_query")
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    cmd = ["cblaster", "plot_clusters", file_path,
           "--output", os.path.join(RESULTS_PATH, f"{job_id}_plot.html")]

    cmd.extend(create_filtering_command(options, True))

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


def corason(job_id, options=None, file_path=None):

    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    cmd = ["echo", "we should execute corason here"]
    # TODO: implement CORASON

    cmd.extend(["queryfile", "tmpQUERYFILEPATH",
                "special_org", "tmpREFERENCECLUSTERPATH",
                "e_value", options["evalue"],
                "e_core", options["ecore"]])

    if "bitscore" in options:
        cmd.append("bitscore") # TODO: check if this is really the way, or an integer should be provided (true/false)

    cmd.extend(["cluster_radio", options["clusterRadio"],
                "e_cluster", options["ecluster"]])

    # list functionality intentionally left out, as clusters to search in
    # are already selected and therefore all clusters in the GENOME directory
    # should be searched

    cmd.extend(["rescale", options["rescale"]])

    if "antismashFile" in options:
        cmd.extend(["antismash", options["antismashFile"]])

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)
