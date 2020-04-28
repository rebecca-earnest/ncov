# Nextstrain updates

Repository with files related to ongoing SARS-CoV-2 phylogenetic analyses at [Grubaugh Lab](grubaughlab.com).


## Getting Started

This repository contains scripts for running pre-analyses to prepare sequence and metadata files for running `augur` and `auspice`, and for running the `nextstrain` pipeline itself.


### Dependencies

To be able to run the pipeline determined by the `Snakefile`, one needs to set up an extended `conda` nextstrain environment, which will deploy all dependencies (modules and packages) required by the python scripts located at the `scripts` directory. Check each individual script in that directory to know what they do along the workflow.


### Setting up a new conda environment

Follow the steps below to set up a conda environment for running the pipeline.

Access a directory or choice in your local machine:
```
cd 'your/directory/of/choice'
```

Clone this repository `ncov`
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
├── auspice/ 			→ directory where the input for auspice will be stored
│
├── config/
│ ├── auspice_config.json	→ JSON file used to create the file used by auspice
│ ├── cache_coordinates.tsv 	→ TSV file with preexisting latitudes and longitudes
│ ├── clades.tsv 		→ TSV file with clade-defining mutations
│ ├── colour_grid.html 		→ HTML file with HEX colour matrices
│ ├── dropped_strains.txt	→ TXT file with IDs of sequences to be dropped along the run
│ ├── geoscheme.xml 		→ XML file with geographic scheme
│ ├── keep.txt 			→ TXT file with accession number of genomes to be included in the analysis
│ ├── nextstrain.yaml 		→ YAML file used to install dependencies
│ ├── reference.gb 		→ GenBank file of a reference genome
│ └── remove.txt 		→ TXT file with IDs of genomes to be removed prior to the run
│
├── pre-analyses/
│ ├── gisaid_cov2020_sequences.fasta 	→ FASTA file with the latest genomes from GISAID
│ ├── new_genomes.fasta 		→ FASTA file with the lab's newly sequenced genomes
│ └── COVID-19_sequencing.xlsx 		→ Custom lab metadata file
│
└── README.md
```


### Preparing the input data

Files in the `pre-analyses` directory need to be downloaded from distinct sources, as shown below.
|              File              |                                              Source                                             |
|:------------------------------:|:-----------------------------------------------------------------------------------------------:|
| gisaid_cov2020_sequences.fasta |         Downloaded from GISAID (all complete genomes submitted from 2019-Dec-01)        |
|        new_genomes.fasta¹       | Newly sequenced genomes, with headers formatted as ">Yale-XXX", downloaded from the Lab's Dropbox |
|    COVID-19_sequencing.xlsx²    |                     Metadata spreadsheet downloaded from an internal Google Sheet                    |



Notes:< /br>
¹ FASTA file containing all genomes sequenced by the lab, including newly sequenced genomes< /br>
² This Excel spreadsheet must have the following columns, named as shown below:< /br>

- Sample-ID *→ lab samples unique identifier, as described below*
- Collection-date
- Country
- State *→ state acronym*
- Division  *→ state full name*
- City
- Host
- Source *→ lab source of the viral samples*
- Update

#### Adapting the Python scripts
A few lines in the scripts `add_newgenomes.py` ans `filter_metadata.py` need to be changed to match your lab's sample naming and origin.

Lines to be changed in `add_newgenomes.py`:
- Lines 45, 56 and 81: **"Yale-"** must match the unique identifier, only found in your lab's genome IDs. Ours is set (in bold) as follows: hCoV-19/USA/**CT-Yale-001**/2020


Lines to be changed in `filter_metadata.py`:
- Line 77: `sheet_name` must be changed to match your Excel sheet name

- Lines 91 and 142: Same as described above, **"Yale-"** must match the unique identifier, only found in your lab's genome IDs. Ours is set (in bold) as follows: hCoV-19/USA/**CT-Yale-001**/2020

- Lines 156 and 179: change these lines to match the country of origin (alpha-3 ISO code)

- Lines 153 and 169: change these lines to match the name and acronym of the most likely state of origin of the samples, if the 'State' field is unknown

- Line 187: change this line to match you lab's name

- Line 188: change this line to match you lab's main author's name

## Running the pipeline

### Generating augur input data

By running the command below, the appropriate files `sequences.fasta` and `metadata.tsv` will be created inside the `data` directory, and the TSV files `colors.tsv` and `latlongs.tsv` will be created inside the `config` directory:

```
snakemake preanalyses
```

### Running augur

By running the command below, the rest of the pipeline will be executed:
```
snakemake export
```

### Removing previous results

By running the command below files related to previous analyses in the working directory will be removed:
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

### Deleting temporary input files after a successful run

This command will delete the directory `pre-analyses` and its large files:
```
snakemake delete
```


## New versions

The code in `scripts` will be updated as needed. Re-download this repository (`git clone...`) whenever a new analysis has to be done, to ensure the latest scripts are being used.

---
## Author

* **Anderson Brito** - [WebPage](https://andersonbrito.github.io/) - anderson.brito@yale.edu
