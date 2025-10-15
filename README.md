# sRNA
<img src="https://github.com/labcbb/sRNA/blob/main/figure.jpg?raw=true" width="800" />

##  About sRNA

This software provides a streamlined solution for small non-conding RNA quantification. By simply inputting a fastq.gz file, users can efficiently process and analyze small non-conding RNA data, allowing for easy extraction of quantitative insights. Designed to handle the complexity of small non-conding RNA sequencing data, it simplifies the workflow, making it accessible for researchers in the field of genomics and bioinformatics. This tool offers a user-friendly approach to the quantification of small non-conding RNAs, facilitating further studies in areas like gene regulation, disease mechanisms, and biomarker discovery.

## Declaration

Our software relys on snakemake for pipeline management which requires snakemake config file (here we use config.yaml). To perform sRNA quantification from a different directory (not in sRNA folder), you must first verify the settings in the `config.yaml` file. It is critical to ensure that the `input path`, `output path`, `reference sequence and index path`, and `tools path` are all accurately configured. 

The `config.yaml` has been provided along with this GitHub repository.

## Installation

To use the sRNA software, you'll need to download and install its dependencies, including findadapt snakemake

## Download and Install sRNA

Download this GitHub repository to an appropriate location.

```bash
wget https://github.com/labcbb/sRNA/archive/refs/heads/main.zip
unzip main.zip
```

## Configure the conda environment

```bash
cd sRNA-main
conda env create -f environment.yml
conda activate sRNA
```
## Before running the software for the first time

Suppose you have alreay activated the sRNA environment. The sRNA also relys on findadapt. Before running sRNA for the first time, you are required to install findadapt using below commands.

```
wget https://github.com/chc-code/findadapt/archive/refs/heads/master.zip
unzip master.zip  
mv findadapt-master $CONDA_PREFIX
chmod +x ${CONDA_PREFIX}/findadapt-master/findadapt 
ln -s ${CONDA_PREFIX}/findadapt-master/findadapt ${CONDA_PREFIX}/bin
findadapt -h
```

## Attention
If you want to run the script with the sample, please delete the results folder first

```bash
rm -r results
```

## Familiarize config.yaml

config.yaml includes multiple parameter, e.g., sample_list (sample information txt path), outdir (output directory), and et al. User should understand the paramter and adjust as needed. Most of the cases, user can use default parameter. In case of use have multiple project and directory, config.yaml can be copied into diffierent location and use user specific parameter setting. 

<img src="https://github.com/labcbb/sRNA/blob/main/Parameter.png?raw=true" />

## Running the Workflow

Once the environment is set up, you can run the sRNA analysis workflow with the following Snakemake command:
```bash
snakemake -s /pathy/to/sRNA-main/sRNA --configfile /pathy/to/sRNA-main/config.yaml --config cutadapt_enabled=true merge_variants=yes --cores 4 --rerun-incomplete
```
Here is an explanation of the parameters:

- `-s sRNA`: Specifies the Snakefile path to use. In this case, test4 is your main workflow file. Replace this with your actual Snakefile name if different.

- `--configfile config.yaml`: Specifies the configuration file for the analysis. You should ensure that config.yaml is correctly set up to specify the input data and parameters for the analysis.

- `--cores 4`: Specifies the number of CPU cores to use for the workflow. Adjust this number based on the available resources. You can change 4 to any number of cores you want to allocate.

- `--rerun-incomplete`: This option ensures that Snakemake will rerun any incomplete jobs in case of failure or partial execution.

- `cutadapt_enabled=true`: Enables the cutadapt tool to remove adapter sequences from the `fastq.gz` file.
- `cutadapt_enabled=false`: Retains the original `fastq.gz` file data without removing adapter sequences.

- `merge_variants=yes`:  Variants of quantitative tDR
- `merge_variants=no`: Variants of non-quantitative tDR

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
This folder contains the main results of the small non-conding RNA quantification analysis. The `results.txt` file will have the following columns:
- `Column 1: sncRNAs` – The unique identifier for each small non-conding RNA detected in the analysis.
- `Column 2: length` – The length of the small non-conding RNA in nucleotides.
- `Column 3: count` – The raw count of reads mapped to this small non-conding RNA across all samples.
- `Column 4: CPM` (Counts Per Million) – A normalized measure of the small non-conding RNA count, adjusting for library size, allowing for comparison across different samples.
- `Column 5: sample` – The identifier for the sample from which the small non-conding RNA data was derived.

Example of the `results.txt` file format:
```bash
sncRNAs    length    count    CPM    sample
smallRNA_1    22    1500    5000    sample1
smallRNA_2    21    1200    4000    sample1
smallRNA_3    23    2000    6700    sample1
```

# Case study

## Backgroud

Recently, a tDR study was published in *Science* (Li et al., A hypoxia-responsive tRNA-derived small non-conding RNA confers renal protection through RNA autophagy, 2025, *Science*, https://www.science.org/doi/10.1126/science.adp5384). Li et al. identified two top significant tDR (tDR-1:32-Asp-GTC-2 (tRNA-Asp-GTC-5′tDR) and tDR-39:72-Asp-GTC-2-M2 (tRNA-Asp-GTC-3′tDR)) by comparing hypoxia kidney cells with normoxia cells (below Figure A). Here we show how to use sRNA tool to reproduce the results step by step.

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

Before running, please set up tool environment following the above description (Installation section). 

Then run our tool.

**Input file:** `sample.txt`

```
SRR14416473  ./GSE173806/SRR14416473_1.fastq.gz
SRR14416474  ./GSE173806/SRR14416474_1.fastq.gz
SRR14416475  ./GSE173806/SRR14416475_1.fastq.gz
SRR14416479  ./GSE173806/SRR14416479_1.fastq.gz
SRR14416480  ./GSE173806/SRR14416480_1.fastq.gz
SRR14416481  ./GSE173806/SRR14416481_1.fastq.gz
```

**Run**

User can copy config.yaml to working directory or directly use /pathy/to/sRNA-main/config.yaml. Make sure  `input path`, `output path`, `reference sequence and index path`, and `tools path` are set correctly in config.yaml. 

```
cd /path/to/sRNA-main
snakemake -s /pathy/to/sRNA-main/sRNA --configfile /pathy/to/config.yaml --config cutadapt_enabled=true merge_variants=yes --cores 4 --rerun-incomplete
```

User can refer the output description in this page. By using the `results.txt` file, you can explore the small non-conding RNA data across multiple samples and gain insights into the abundance and distribution of specific small non-conding RNAs in your dataset. 


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

Please also set up a group_info.txt in CaseStudy file. **You should need to use `Tab` to separate `sample` from `group`**

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

## Please note that this is the grouping information. If your grouping is not in this place, it needs to be modified

group_df <- readr::read_tsv("./CaseStudy/group_info.txt")
group <- group_df$group
names(group) <- group_df$sample

# read sRNA output
## Please note that this is quantitative data. If your data is not in this place, it needs to be modified

data = readr::read_tsv("./results/total/result.txt")
data$sample <- gsub("_1", "", data$sample)
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

tdr.diff$Gene = NA
tdr.diff[c( "tDR-1:32-Asp-GTC-2", "tDR-39:72-Asp-GTC-2-M2"), ]$Gene = c( "tDR-1:32-Asp-GTC-2", "tDR-39:72-Asp-GTC-2-M2")
tdr.diff = tdr.diff %>% arrange(desc(logFC))
tdr.diff$rank = 1:nrow(tdr.diff)

p <- ggpubr::ggscatter(tdr.diff, x= "rank", y = "logFC", ylab = "logFC", repel = T, label = "Gene", color = "gray", font.label = c(14, "bold", "black"))

# Save the picture
ggsave("tdr_analysis_plot.png", p, width = 10, height = 8, dpi = 300)
cat("Plot saved as: tdr_analysis_plot.png\n")

cat("Analysis completed successfully!\n")

```

## Please feel free to contact us if you have any question






