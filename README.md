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
snakemake -s sRNA --configfile config.yaml --config cutadapt_enabled=true --cores 4 --rerun-incomplete
```
Here is an explanation of the parameters:

- `-s sRNA`: Specifies the Snakefile to use. In this case, test4 is your main workflow file. Replace this with your actual Snakefile name if different.

- `--configfile config.yaml`: Specifies the configuration file for the analysis. You should ensure that config.yaml is correctly set up to specify the input data and parameters for the analysis.

- `--cores 4`: Specifies the number of CPU cores to use for the workflow. Adjust this number based on the available resources. You can change 4 to any number of cores you want to allocate.

- `--rerun-incomplete`: This option ensures that Snakemake will rerun any incomplete jobs in case of failure or partial execution.

- `cutadapt_enabled=true`: Enables the cutadapt tool to remove adapter sequences from the `fastq.gz` file.
- `cutadapt_enabled=false`: Retains the original `fastq.gz` file data without removing adapter sequences.

For more information about additional parameters and options available in Snakemake, you can use the command snakemake -h to view the full help documentation.

## Input File Format
Before running the analysis, you must provide a sample.txt file that includes the necessary sample information. The file should be formatted as follows:
- First column: Sample names (e.g., sample1, sample2, etc.)
- Second column: The full file path to the corresponding FASTQ file.
  The structure of the sample.txt file should look like this:
```plaintext
sample1    /path/to/sample1.fastq.gz
sample2    /path/to/sample2.fastq.gz
sample3    /path/to/sample3.fastq.gz
```

## Output Format
After running the workflow, two main output folders will be generated:
### 1. multiqc
This folder contains the multiQC report, which provides an overview of the analysis, including a summary of the quality control results for each FASTQ file processed.  Specifically, the `multiqc_report.html` file can be used to assess whether adapter sequences have been properly removed from the FASTQ files.  This report provides visual insights into the quality of the sequencing data, highlighting any potential issues with adapter contamination.
### 2. total
This folder contains the main results of the small RNA quantification analysis. The `results.txt` file will have the following columns:
- `Column 1: sncRNAs` – The unique identifier for each small RNA detected in the analysis.
- `Column 2: length` – The length of the small RNA in nucleotides.
- `Column 3: count` – The raw count of reads mapped to this small RNA across all samples.
- `Column 4: CPM` (Counts Per Million) – A normalized measure of the small RNA count, adjusting for library size, allowing for comparison across different samples.
- `Column 5: sample` – The identifier for the sample from which the small RNA data was derived.

Example of the `results.txt` file format:
```bash
sncRNAs    length    count    CPM    sample
smallRNA_1    22    1500    5000    SRRXXX
smallRNA_2    21    1200    4000    SRRXXX
smallRNA_3    23    2000    6700    SRRXXX
```
