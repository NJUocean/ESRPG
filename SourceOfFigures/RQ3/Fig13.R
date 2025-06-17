library(ggplot2)
library(dplyr)
library(stringr)
library(RColorBrewer)

# obtain current path of script
get_script_dir <- function() {
  if (interactive() && requireNamespace("rstudioapi", quietly = TRUE)) {
    tryCatch({
      script_path <- rstudioapi::getActiveDocumentContext()$path
      if (length(script_path) > 0) {
        return(dirname(script_path))
      }
    }, error = function(e) NULL)
  }
  
  args <- commandArgs(trailingOnly = FALSE)
  script_path <- sub("--file=", "", args[grep("--file=", args)])
  if (length(script_path) > 0) {
    return(dirname(normalizePath(script_path)))
  }
  
  warning("Unable to automatically obtain script path, defaults to returning the current working directory. Please manually specify the relevant path", getwd())
  return(getwd())
}

script_dir <- get_script_dir()
cat("The directory where the current script is located：", script_dir, "\n")

categories <- c("NDRC=-1", "NDRC=1", "0<NDRC<0.5", "NDRC=0.5", "0.5<NDRC<1", "-1<NDRC<-0.5", "NDRC=-0.5", "-0.5<NDRC<0")
fixed_colors <- RColorBrewer::brewer.pal(8, "Set1")


sizes_list <- list(
  c(126, 96, 2, 93, 1, 1, 3, 4),
  c(26, 20, 0, 12, 0, 0, 0, 0),
  c(124, 71, 0, 73, 0, 0, 3, 0),
  c(1, 0, 0, 1161, 14, 0, 0, 0),
  c(0, 0, 0, 9, 0, 0, 0, 0)
)
suffix=c("a","b","c","d","e")


for (i in seq_along(sizes_list)) {
  sizes <- sizes_list[[i]]
  df <- data.frame(
    Category = categories,
    size = sizes
  )

  filtered_df <- df %>%
    filter(size > 0)
  if (nrow(filtered_df) == 0) {
    cat(paste0("No data for group ", i, "\n"))
    next
  }
  

  sorted_df <- arrange(filtered_df, -size)
  sorted_categories <- sorted_df$Category
  sorted_df$Category <- factor(sorted_df$Category, levels = sorted_df$Category)
  matched_colors <- fixed_colors[match(sorted_categories, categories)]
  

  ggplot(sorted_df, aes(x = "", y = size, fill = Category)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y") +
    theme_void() +
    scale_fill_manual(
      values = matched_colors,
      labels = paste0(sorted_df$Category, "  (", sorted_df$size, ")")
    ) +
    theme(
      legend.position = "right",
      legend.text = element_text(size = 40),
      legend.title = element_text(size = 50),
    )
  
  filename <- paste0(script_dir, "/Fig13", suffix[i], ".pdf")
  ggsave(filename, width = 16, height = 8)

}