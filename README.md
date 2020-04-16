# Nextstrain updates

Repository with files related to ongoing SARS-CoV-2 phylogenetic analyses at [Grubaugh Lab](grubaughlab.com).


## Getting Started

The `ncov-pipeline` directory contains scripts for running pre-analyses to prepare sequence and metadata files for running `augur` and `auspice`, and run the `nextstrain` pipeline itself.


### Dependencies

To be able to run the pipeline determined by the `Snakefile`, one needs to set up an extended `conda` nextstrain environment, which will deploy all dependencies (modules and packages) required by the python scripts located at the `scripts` directory. Check each individual script in that directory to know what each of them do along the workflow.


### Setting up a new conda environment

Follow the steps below to set up a conda environment for running the `ncov-pipeline`

Access a directory or choice in your local machine:
```
cd 'your/directory/of/choice'
```

Clone the present repository `ncov`
```
git clone https://github.com/andersonbrito/ncov.git
```

Rename the directory `ncov` as you wish. Access the newly generated directory in your local machine, change directory to `config`, and update your existing nextstrain environment as shown below:
```
cd 'your/directory/of/choice/ncov/config'
conda env update --file nextstrain.yaml
```

This command will install all necessary dependencies to run the pipeline.


## Preparing the working directory

This minimal set of files and directories are expected in the working directory.

```
ncov/
│
├── config/
│ ├── auspice_config.json
│ ├── cache_coordinates.tsv 	→ TSV file with preexisting latitudes and longitudes
│ ├── clades.tsv 			→ TSV file with clade-defining mutations
│ ├── colour_grid.html 		→ HTML file with HEX colour matrices
│ ├── dropped_strains.txt	→ TXT file with IDs of sequences to be dropped along the run
│ ├── geoscheme.xml 		→ XML file with geographic scheme
│ ├── keep.txt 			→ TXT file with accession number of genomes to be included in the analysis
│ ├── nextstrain.yaml 		→ YAML file used to install dependencies
│ ├── reference.gb 		→ GenBank file with the reference genome
│ └── remove.txt 		→ TXT file with IDs of genomes to be removed prior to the run
│
├── pre-analyses/
│ ├── gisaid_cov2020_sequences.fasta 	→ FASTA file with latest genomes from GISAID
│ ├── new_genomes.fasta 		→ FASTA file with newly sequenced genomes
│ └── COVID-19_sequencing.xlsx 		→ Custom lab metadata file
│
└── README.md
```


### Preparing the input data

Files in the `pre-analyses` directory need to be downloaded from distinct sources, as shown below.
|              File              |                                              Source                                             |
|:------------------------------:|:-----------------------------------------------------------------------------------------------:|
| gisaid_cov2020_sequences.fasta |         Downloaded from GISAID (all complete genomes submitted after 01-12-2019)        |
|        new_genomes.fasta       | Newly sequenced genomes, with headers formatted as ">Yale-00X", downloaded from the Lab's Dropbox |
|    COVID-19_sequencing.xlsx    |                     Metadata spreadsheet downloaded from Google Spreadsheets                    |


## Running the pipeline

### Generating nextstrain metadata

By running the command below, the appropriate files `sequences.fasta`, and `metadata.tsv` will be created inside a `data` directory, and the TSV files `colors.tsv` and `latlongs.tsv` will be created inside the `config` directory.

```
snakemake preanalyses
```

### Running augur

By running the command below, the rest of the pipeline will executed
```
snakemake export
```

### Removing previous results

By running the command below files related to previous analyses in the working directory will be removed.
```
snakemake clean
```

Such command will remove the following files and directories:
```
results
auspice
data
config/colors.tsv
config/latlongs.tsv
```

### Deleting input files after a successful run

This command will delete the directory `pre-analyses`:
```
snakemake delete
```


## New versions

The scripts in this pipeline will be updated as needed. Re-download this repository (`git clone...`) whenever a new analysis has to be done, to ensure the latest scripts are being used.

---
## Author

* **Anderson Brito** - [WebPage](https://andersonbrito.github.io/) - andersonfbrito@gmail.com
