# Nextstrain updates

Repository with temporary files related to ongoing phylogenetic analyses at Grubaugh Lab.

## Getting Started

The `ncov-pipeline` directory contains scripts for running pre-analyses to prepare sequence and metadata files for running `augur` and `auspice`.

### Dependencies

To be able to run the pipeline described in the `Snakefile`, one will need to set up an extended `conda` nextstrain environment, which will deploy all dependencies (modules and packages) required by the python scripts located at the `scripts` directory.

### Setting up a new conda environment

Follow the steps below to set up a conda environment for running the `ncov-pipeline`

Access a directory or choice in your local machine:
```
cd 'your/directory/of/choice'
```

Clone the present repository `ns-temp`
```
git clone https://github.com/andersonbrito/ns-temp.git
```

Rename the directory `ns-temp` as you wish. Access the newly generated directory in your local machine, change directory to `config`, and update your existing nextstrain environment as shown below:
```
cd 'your/directory/of/choice/ns-temp/config'
conda env update --file nextstrain.yaml
```

This command will install all necessary dependencies to run the pipeline.


### Preparing the working directory

This minimal set of files and directories are expected in the working directory.

```
ns-temp/
│
├── config/
│ ├── auspice_config.json
│ ├── cache_coordinates.tsv → TSV file with preexisting latitudes and longitudes
│ ├── clades.tsv
│ ├── colour_grid.html → HTML file with HEX colour matrices
│ ├── dropped_strains.txt
│ ├── geoscheme.xml → XML file with geographic scheme
│ ├── keep.txt → TXT file with accession number of genomes to be included in the analysis
│ ├── nextstrain.yaml → YAML file used to install dependencies
│ ├── reference.gb
│ └── remove.txt → TXT file with IDs of genomes to be removed
│
├── pre-analyses/
│ ├── gisaid_cov2020_sequences.fasta → FASTA file with latest genomes from GISAID
│ ├── new_genomes.fasta → FASTA file with newly sequenced genomes
│ └── COVID-19_sequencing.xlsx → Custom lab metadata file
│
└── README.md
```


### Preparing the input data

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Anderson Brito** - [WebPage](https://andersonbrito.github.io/) - andersonfbrito@gmail.com

## License

This project is licensed under the MIT License.

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

<!---
--->
