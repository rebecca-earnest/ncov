#!/bin/bash

# set max wallclock time
#SBATCH --time=80:00:00

# node information
#SBATCH -A covid -p covid

# memory requirement
#SBATCH --mem=50g

# number of nodes
#SBATCH --nodes=1

# CPUs allocated to each task
#SBATCH --cpus-per-task=20

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=BEGIN,END --mail-user=rebecca.earnest@yale.edu

module load miniconda
source activate nextstrain

export AUGUR_RECURSION_LIMIT=10000
snakemake export
