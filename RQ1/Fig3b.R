library(readxl)
library(dplyr)
library(ggplot2)
library(ScottKnottESD)
if (!requireNamespace("here", quietly = TRUE)) install.packages("here")
library(here)
library(rstudioapi)


get_script_dir <- function() {
  # 1. RStudio
  if (interactive() && requireNamespace("rstudioapi", quietly = TRUE)) {
    tryCatch({
      script_path <- rstudioapi::getActiveDocumentContext()$path
      if (length(script_path) > 0) {
        return(dirname(script_path))
      }
    }, error = function(e) NULL)
  }
  
  # 2.source
  args <- commandArgs(trailingOnly = FALSE)
  script_path <- sub("--file=", "", args[grep("--file=", args)])
  if (length(script_path) > 0) {
    return(dirname(normalizePath(script_path)))
  }
  
  # wd
  warning("Unable to automatically obtain script path, defaults to returning the current working directory. Please manually specify the relevant path", getwd())
  return(getwd())
}

script_dir <- get_script_dir()
cat("The directory where the current script is located：", script_dir, "\n")


colname1<-"CountLineCodeExe"
colname2<-"CountLineCode"

# read data from Excel
valueCD <- read_excel(paste0(script_dir,"/metrics/Csmith_stat.xlsx"),col_types = "numeric")
valueCE <- read_excel(paste0(script_dir,"/metrics/CsmithEdge_stat.xlsx"),col_types = "numeric")
valueCH <- read_excel(paste0(script_dir,"/metrics/Hicond_stat.xlsx"),col_types = "numeric")
valueY1F <- read_excel(paste0(script_dir,"/metrics/Yarpgen_v1_func_stat.xlsx"),col_types = "numeric")
valueY1D <- read_excel(paste0(script_dir,"/metrics/Yarpgen_v1_driver_stat.xlsx"),col_types = "numeric")
valueY2F <- read_excel(paste0(script_dir,"/metrics/Yarpgen_v2_func_stat.xlsx"),col_types = "numeric")
valueY2D <- read_excel(paste0(script_dir,"/metrics/Yarpgen_v2_driver_stat.xlsx"),col_types = "numeric")

CD <- data.frame(ratio = valueCD[[colname1]] / valueCD[[colname2]], technique = "Csmith")
CE <- data.frame(ratio = valueCE[[colname1]] / valueCE[[colname2]], technique = "CsmithEdge")
CH <- data.frame(ratio = valueCH[[colname1]] / valueCH[[colname2]], technique = "Csmith-HiCOND")
Y1F <- data.frame(ratio = valueY1F[[colname1]] / valueY1F[[colname2]], technique = "Y-func")
Y1D <- data.frame(ratio = valueY1D[[colname1]] / valueY1D[[colname2]], technique = "Y-driver")
Y2F <- data.frame(ratio = valueY2F[[colname1]] / valueY2F[[colname2]], technique = "Y2-func")
Y2D <- data.frame(ratio = valueY2D[[colname1]] / valueY2D[[colname2]], technique = "Y2-driver")
Y1 <- data.frame(ratio = (valueY1F[[colname1]]+valueY1D[[colname1]]) / (valueY1F[[colname2]]+valueY1D[[colname2]]), technique = "YARPGen")
Y2 <- data.frame(ratio = (valueY2F[[colname1]]+valueY2D[[colname1]]) / (valueY2F[[colname2]]+valueY2D[[colname2]]), technique = "YARPGen v.2")


all <- rbind(CD, CE, CH, Y1F, Y1D, Y2F, Y2D, Y1, Y2)



#rank
result <- data.frame(
  CD = CD$ratio,
  CE = CE$ratio,
  CH = CH$ratio,
  Y1F = Y1F$ratio,
  Y1D = Y1D$ratio,
  Y2F = Y2F$ratio,
  Y2D = Y2D$ratio,
  Y1 = Y1$ratio,
  Y2 = Y2$ratio
)
sk <- sk_esd(result, version="np")


all$rank = 0
all[all$technique == "Csmith", ]$rank = sk$groups[["CD"]]
all[all$technique == "CsmithEdge", ]$rank = sk$groups[["CE"]]
all[all$technique == "Csmith-HiCOND", ]$rank = sk$groups[["CH"]]
all[all$technique == "Y-func", ]$rank = sk$groups[["Y1F"]]
all[all$technique == "Y-driver", ]$rank = sk$groups[["Y1D"]]
all[all$technique == "Y2-func", ]$rank = sk$groups[["Y2F"]]
all[all$technique == "Y2-driver", ]$rank = sk$groups[["Y2D"]]
all[all$technique == "YARPGen", ]$rank = sk$groups[["Y1"]]
all[all$technique == "YARPGen v.2", ]$rank = sk$groups[["Y2"]]

#plot
ggplot(all, aes(x = reorder(technique, -ratio, FUN = median), y = ratio)) +
  geom_boxplot(outlier.shape = NA) +  
  facet_grid(~rank, drop = TRUE, scales = "free", space = "free") +
  scale_y_continuous(limits = c(0, 1),expand = c(0, 0))+
  ylab("") +
  xlab("") +
  theme(
    axis.text.x = element_text(
      angle = -40,          
      hjust = 0.5,          
      #family = "Times New Roman",
      size = 24             
    ),
    axis.text.y = element_text(
      size = 24             
    )
  )
ggsave(paste0(script_dir,"/Fig3b.pdf"), width = 16,height = 8)


