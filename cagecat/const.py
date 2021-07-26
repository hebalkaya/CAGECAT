"""Module to store constants such as help texts

Author: Matthias van den Belt

"""
import config
from cagecat import app
from cagecat.help_texts import HELP_OVERVIEW, HELP_TEXTS

with open(app.config['PRESENT_DATABASES_LOCATION']) as inf:
    PRESENT_DATABASES = inf.read().strip().split(',')
    PRESENT_DATABASES.sort()

CLINKER_MODULES = ('clinker_query', 'clinker_full')

FAILURE_REASONS = {'ERROR - No valid profiles could be selected': # module search, hmm/hmm+remote mode, incorrect HMM profiles
                       'No valid HMM profiles have been entered. Check your HMM profiles for potential spelling errors.',
                   'ValueError: Search completed, but found no hits':  # module search, no hits found
                       'Your search with the specified parameters did not return any hits. Check your input, and try to loosen your search parameters to get results.',
                   'Too many selected clusters':
                       'You have selected too many clusters to use in your downstream analysis. Check the maximum number of clusters for the analysis you were trying to execute, and try again.',  # clinker_full, extract_clusters
                   'Too many samples':
                       'You set the value for the number of samples parameter too high. Change it to the maximum value and try again.'
                   }

MODULE_TO_PROGRAM = {'search': 'cblaster',
                     'gne': 'cblaster',
                     'recompute': 'cblaster',
                     'extract': 'cblaster',
                     'extract_clusters': 'cblaster',
                     'clinker_query': 'cblaster',
                     'clinker_full': 'clinker'
                     }

EXTRACT_CLUSTERS_OPTIONS = {"selectedOrganisms": "",
                            "selectedScaffolds": "",  # empty strings as
                            "clusterNumbers": "",  # if nothing was
                            "clusterScoreThreshold": "",  # filled in in the
                            "prefix": "",  # submission form
                            "format": "genbank",
                            "maxclusters": str(config.THRESHOLDS['maximum_clusters_to_extract'])}  # indicates no maximum

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
                              # TODO: would: possible corason and clinker_query. Get query headers from .csv file
                              "clinker_full": [],
                              "clinker_query": ["extract_clusters"] # TODO: would: possibly also corason?
                              }

### Post-analysis explanation section

# format is: {module: [(paragraph_title, text), ...]}
# {module: [('list', ('point1', 'point2', ...))]} results in an ordered list being generated
# empty paragraph title means that no header should be generated
POST_ANALYSIS_EXPLANATIONS = {'multicblaster_search':
                                  [('', 'Query sequences are searched against the NCBI’s BLAST API in remote mode. BLAST hits are filtered according to user defined quality thresholds. In remote mode, each hit is then queried against the NCBI’s Identical Protein Groups (IPG) resource, which, as its name suggests, groups proteins sharing identical amino acid sequence as an anti-redundancy measure. The resulting IPG table contains source genomic coordinates for each hit protein sequence, which cblaster uses to group them by their corresponding organism, scaffold and subject sequences.'),
                                   ('', 'In order to run a cblaster search, you will need to point the module to a collection of sequences to be used as queries. These can be provided in two ways:'),
                                   ('list', ('A FASTA format file containing amino acid sequences',
                                             'A list of valid NCBI sequence identifiers (e.g. accession, GI number)')),
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
                                   ],
                              'clinker_full_visualization': [('', 'clinker: generating publication-quality gene cluster comparison figures.'),
                                                             ('', 'Given a job, corresponding GenBank files will be downloaded and clinker will automatically extract protein translations, perform global alignments between sequences in each cluster, determine the optimal display order based on cluster similarity, and generate an interactive visualisation that can be extensively tweaked before being exported as an SVG file.'),
                                                             ('', 'An overview of usage, as well as all changeable options, is provided in the visualisation sidebar. Briefly:'),
                                                             ('list', ('Clusters can be rearranged vertically by dragging cluster names',
                                                                       'Loci can be moved or resized by hovering over them and dragging the box',
                                                                       'The visualisation can be anchored around a specific gene by clicking on it',
                                                                       'Clusters and similarity groups can be renamed by clicking on their text',
                                                                       'Similarity group colours can be changed by clicking on the circles in the legend',
                                                                       'Groups can be removed by right-clicking their label in the legend',
                                                                       'The scale bar can be resized by clicking its text and entering a new value (bp)'))
                                                             ],
                              'neighbourhood_estimation': [('', 'In cblaster, the most important parameter when detecting hit clusters is the maximum inter-hit gap parameter. This determines how far cblaster will look between any two hits before terminating a given cluster. By default, this parameter is set to 20,000 bp; if no new hit is found within 20,000 bp of the previous hit in a cluster, cblaster will terminate extension of that cluster. Though the 20 kb cutoff has worked quite well for us when looking at fungi or bacteria, where gene density within clusters is quite high, it may not work for all datasets. For example, plant gene clusters may have key biosynthetic genes spread out over large stretches of the chromosome, with many genes in between; this is where the gne module comes in.'),
                                                           ('', 'The Neighbourhood estimation module lets you robustly detect an appropriate value to use for this parameter by continually re-running cluster detection on a saved search session at different gap values over some interval. It then generates plots of the mean and median cluster sizes (bp), as well as the total number of predicted clusters, at each value.'),
                                                           ('', 'The Neighbourhood estimation module generates a list of gap values (total number determined by the samples parameter) from 0 to some upper limit (determined by the Max. intergenic distance parameter). These numbers can be chosen in two ways. By default, Neighbourhood estimation will take evenly spaced (i.e. linear) values over the range 0-100,000 bp. Alternatively, you can choose to generate these values via a log scale, which will result in more samples at lower values than at higher ones. This can be specified using the sampling space parameter. As these plots typically resemble logarithmic growth (i.e. rise steeply, then level off), it can make sense to sample more heavily in the more unstable region of the curve')
                                                            ],
                              'extract_sequences': [('', 'After a search has been performed, it can be useful to retrieve sequences matching a certain query for further analyses (e.g. sequence comparisons for phylogenies). This is easily accomplished using the Extract sequences module.'),
                                                    ('', 'A preceding job is used as input, and extracts sequences matching any filters you have specified. If no filters are specified, ALL hit sequences will be extracted. By default, only sequence names are extracted. This is because cblaster stores no actual sequence data for hit sequences during it’s normal search workflow, only their coordinates. However, sequences can automatically be retrieved from the NCBI by specifying the Download sequences parameter. cblaster will then write them, in FASTA format to a file.'),
                                                    ('', 'The Extract sequences can also filter based on the organism that each hit sequence is on. The organism filter uses regular expression patterns based on organism names, but it is not obligatory to use regular expressions.  Multiple patterns can be provided, and are additive (i.e. any organism matching any of the patterns will be saved). ')
                                                    ],
                              'extract_clusters': [('', 'A common next step after a cblaster search is to retrieve the identified gene clusters so we can perform additional analysis. cblaster provides the Extract clusters module precisely for this purpose, allowing you to generate GenBank files of specific gene clusters directly from a previous job. Extract all clusters from a job could take a long time for searches with many results.'),
                                                   ],
                              'recompute': [('', 'You can recompute a previous job using new filter thresholds to filter previous results.')]
                              }

SUBMIT_URL = "/submit_job"
MODULES_WHICH_HAVE_PLOTS = ["search", "recompute", "gne",
                             "clinker_full", "clinker_query"]