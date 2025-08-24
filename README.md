# sRNA
<img src="https://github.com/labcbb/sRNA/blob/main/figure.jpg?raw=true" width="800" />

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
cd sRNA-main
conda env create -f environment.yml
conda activate sRNA
```
## Attention
If you want to run the script with the sample, please delete the results folder first
```bash
rm -r results
```
## Running the Workflow
To run the workflow correctly, you need to ensure that the path to the `findadapt-master` directory is specified correctly. In the command below:
```bash
export PATH=$PATH:/data/home/huangrende/mrna/sRNA/sRNA-main/test/findadapt-master
```
Replace `/data/home/huangrende/mrna/sRNA/sRNA-main/test/findadapt-master` with the absolute path to your own findadapt-master directory.

For example, if the `findadapt-master` folder is located at `/home/username/findadapt`, you should use:
```bash
export PATH=$PATH:/home/username/findadapt-master
```
This ensures that the `findadapt` tool is correctly added to the system path and can be executed by the workflow.

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
smallRNA_1    22    1500    5000    sample1
smallRNA_2    21    1200    4000    sample1
smallRNA_3    23    2000    6700    sample1
```
In this example:

- smallRNA_1: A small RNA with a length of 22 nucleotides, appearing 1500 times in sample1 with a CPM of 5000.
- Each row represents a small RNA detected in a specific sample.

# Case study

## Backgroud

Recently, a tDR study was published in *Science* (Li et al., A hypoxia-responsive tRNA-derived small RNA confers renal protection through RNA autophagy, 2025, *Science*, https://www.science.org/doi/10.1126/science.adp5384). Li et al. identified two top significant tDR (tDR-1:32-Asp-GTC-2 (tRNA-Asp-GTC-5′tDR) and tDR-39:72-Asp-GTC-2-M2 (tRNA-Asp-GTC-3′tDR)) by comparing hypoxia kidney cells with normoxia cells (below Figure A). Here we show how to use sRNA tool to reproduce the results step by step.

<img src="https://github.com/labcbb/sRNA/blob/main/GSE17380volcano.png?raw=true" />

## Download dataset GSE173806

```
mkdir GSE173806 && cd GSE173806
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/073/SRR14416473/SRR14416473_1.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/074/SRR14416474/SRR14416474_1.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/075/SRR14416475/SRR14416475_1.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/079/SRR14416479/SRR14416479_1.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/080/SRR14416480/SRR14416480_1.fastq.gz
wget -nc ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR144/081/SRR14416481/SRR14416481_1.fastq.gz
```

## Run sRNA

Please set up tool environment following the above description and run our tool.

**Input file:** input.tsv

```
SRR14416473  SRR14416473_1.fastq.gz
SRR14416474  SRR14416474_1.fastq.gz
SRR14416475  SRR14416475_1.fastq.gz
SRR14416479  SRR14416479_1.fastq.gz
SRR14416480  SRR14416480_1.fastq.gz
SRR14416481  SRR14416481_1.fastq.gz
```

**Run**

```
cp /path/to/sRNA/config.yaml ./
snakemake -s sRNA --configfile config.yaml --config cutadapt_enabled=true --cores 4 --rerun-incomplete
```
User can refer the output description in this page. By using the `results.txt` file, you can explore the small RNA data across multiple samples and gain insights into the abundance and distribution of specific small RNAs in your dataset. 


## Analysis

**Set up R packages**

```{r}
# install_and_load_packages.R
options(repos = c(CRAN = "https://cloud.r-project.org/"))
required_packages <- c("dplyr", "readr", "tidyr", "tibble", "stringr", "ggplot2", "ggpubr")

# check package
check_and_install <- function(package_name) {
  if (!require(package_name, character.only = TRUE, quietly = TRUE)) {
    cat(paste("Installing package:", package_name, "\n"))
    install.packages(package_name, dependencies = TRUE, quiet = TRUE)
    library(package_name, character.only = TRUE)
    cat(paste("Successfully installed and loaded:", package_name, "\n"))
  } else {
    cat(paste("Package", package_name, "already installed, loading...\n"))
  }
}

cat("Checking and installing CRAN packages...\n")
for (pkg in required_packages) {
  check_and_install(pkg)
}

# install loonR package
cat("Checking loonR package...\n")
if (!require("loonR", quietly = TRUE)) {
  cat("Installing loonR from GitHub...\n")
  if (!require("devtools", quietly = TRUE)) {
    cat("Installing devtools...\n")
    install.packages("devtools", quiet = TRUE)
    library(devtools)
  }
  devtools::install_github("ProfessionalFarmer/loonR", quiet = TRUE)
  library(loonR)
  cat("Successfully installed and loaded: loonR\n")
} else {
  cat("Package loonR already installed, loading...\n")
  library(loonR)
}

cat("All packages loaded successfully!\n")
```

Please also set up a group_info.txt as below.

```
sample  group
SRR14416473  CTRL
SRR14416474  CTRL
SRR14416475  CTRL
SRR14416479  Treat
SRR14416480  Treat
SRR14416481  Treat
```

**Now start analysis**, you can reproduce the Figure B

```
cat("Starting analysis...\n\n")

group_df <- readr::read_tsv("./group_info.txt")
group <- group_df$group
names(group) <- group_df$sample

# read sRNA output
data = readr::read_tsv("./results/total/result.txt")
# data$sample <- gsub("_1", "", data$sample)
data <- data[,-(2:3)]
data = tidyr::pivot_wider(data, names_from = sample, values_from = CPM)
data = data %>% tibble::column_to_rownames("sncRNAs")
data = data[,names(group)]

tdr.data = data[stringr::str_detect(rownames(data), "^tDR"),]
tdr.data[is.na(tdr.data)] = 0
tdr.data = log2( tdr.data[rowMeans(tdr.data) > 1,] + 1)

tdr.diff = loonR::limma_differential(tdr.data, group)
loonR::volcano_plot_V2(tdr.diff$logFC, tdr.diff$adj.P.Val, tdr.diff$REF, p.cutoff = 0.01, logFC.cutoff = 1, 
                       show.top.n = 0, sig.genes = c( "tDR-1:32-Asp-GTC-2", "tDR-39:72-Asp-GTC-2-M2")  ) + xlim(c(-5,5))

```

# Please feel free to contact us if you have any question.






