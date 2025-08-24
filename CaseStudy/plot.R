# install_and_load_packages.R
# 自动检查和安装所需的R包

# 设置CRAN镜像
options(repos = c(CRAN = "https://cloud.r-project.org/"))

# 定义需要的包
required_packages <- c("dplyr", "readr", "tidyr", "tibble", "stringr", "ggplot2", "ggpubr")

# 检查并安装CRAN包的函数
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

# 安装CRAN包
cat("Checking and installing CRAN packages...\n")
for (pkg in required_packages) {
  check_and_install(pkg)
}

# 检查并安装loonR包
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
cat("Starting analysis...\n\n")

# 您的分析代码
group_df <- readr::read_tsv("./CaseStudy/group_info.txt")
group <- group_df$group
names(group) <- group_df$sample

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

# 保存图片
ggsave("tdr_analysis_plot.png", p, width = 10, height = 8, dpi = 300)
cat("Plot saved as: tdr_analysis_plot.png\n")

cat("Analysis completed successfully!\n")
