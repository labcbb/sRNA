# sRNA
##  About sRNA
This software provides a streamlined solution for small RNA quantification. By simply inputting a fastq.gz file, users can efficiently process and analyze small RNA data, allowing for easy extraction of quantitative insights. Designed to handle the complexity of small RNA sequencing data, it simplifies the workflow, making it accessible for researchers in the field of genomics and bioinformatics. This tool offers a user-friendly approach to the quantification of small RNAs, facilitating further studies in areas like gene regulation, disease mechanisms, and biomarker discovery.

## Installation
To use the sRNA software, you'll need to download and install its dependencies, including findadapt snakemake
### 1. Download and Install sRNA
```bash
wget https://github.com/labcbb/sRNA/archive/refs/heads/main.zip
unzip main.zip
```
### 2. Download and Install FindAdapt
```bash
wget https://github.com/chc-code/findadapt/archive/refs/heads/master.zip
unzip master.zip  # The output folder will be findadapt-master
```

## Configure the conda environment
```bash
conda env create -f environment.yml
conda activate sRNA
```

## Running the Workflow
Once the environment is set up, you can run the sRNA analysis workflow with the following Snakemake command:
```bash
snakemake -s sRNA --configfile config.yaml --cores 4 --rerun-incomplete
```
Here is an explanation of the parameters:

-s sRNA: Specifies the Snakefile to use. In this case, test4 is your main workflow file. Replace this with your actual Snakefile name if different.

--configfile config.yaml: Specifies the configuration file for the analysis. You should ensure that config.yaml is correctly set up to specify the input data and parameters for the analysis.

--cores 4: Specifies the number of CPU cores to use for the workflow. Adjust this number based on the available resources. You can change 4 to any number of cores you want to allocate.

--rerun-incomplete: This option ensures that Snakemake will rerun any incomplete jobs in case of failure or partial execution.

For more information about additional parameters and options available in Snakemake, you can use the command snakemake -h to view the full help documentation.
