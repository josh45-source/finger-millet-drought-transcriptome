# ============================================================
#  de_analysis.R — finger millet
#  Maintainer: see CITATION.cff
# ============================================================

suppressPackageStartupMessages({
  library(DESeq2)
  library(ggplot2)
  library(pheatmap)
  library(dplyr)
  library(RColorBrewer)
  library(ggrepel)
})

# ── Read Snakemake parameters ─────────────────────────────────
count_files  <- snakemake@input[["count_gtfs"]]
novel_gtf    <- snakemake@input[["novel_gtf"]]
out_all_de   <- snakemake@output[["all_de"]]
out_novel_up <- snakemake@output[["novel_up"]]
out_volcano  <- snakemake@output[["volcano"]]
out_heatmap  <- snakemake@output[["heatmap"]]
padj_cutoff  <- as.numeric(snakemake@params[["padj_cutoff"]])
lfc_cutoff   <- as.numeric(snakemake@params[["lfc_cutoff"]])
min_count    <- as.numeric(snakemake@params[["min_count"]])
controls     <- strsplit(snakemake@params[["controls"]], ",")[[1]]
droughts     <- strsplit(snakemake@params[["droughts"]], ",")[[1]]

log_file <- snakemake@log[[1]]
con <- file(log_file, open = "wt")
sink(con, type = "message")
sink(con, type = "output")

cat("=== DE Analysis Started:", format(Sys.time()), "===\n")
cat("\n")

dir.create("results/de_analysis", showWarnings = FALSE, recursive = TRUE)

# ── Parse novel gene IDs ──────────────────────────────────────
cat("Reading novel gene GTF...\n")
novel_lines <- readLines(novel_gtf)
novel_lines <- novel_lines[!grepl("^#", novel_lines)]

extract_attr <- function(lines, attr) {
  pattern <- paste0(attr, ' "([^"]+)"')
  sapply(regmatches(lines, regexpr(pattern, lines)),
         function(x) if(length(x)==0) NA else
           sub(paste0('.*', attr, ' "([^"]+)".*'), '\\1', x))
}

tx_lines <- novel_lines[grepl("\ttranscript\t", novel_lines)]
novel_transcript_ids <- extract_attr(tx_lines, "transcript_id")
novel_transcript_ids <- novel_transcript_ids[!is.na(novel_transcript_ids)]
cat("  Novel transcripts:", length(novel_transcript_ids), "\n")

# ── Build count matrix — FIXED approach ──────────────────────
cat("\nBuilding count matrix...\n")
all_samples <- c(controls, droughts)

parse_counts <- function(gtf_file, sample_name) {
  tryCatch({
    lines <- readLines(gtf_file)
    lines <- lines[!grepl("^#", lines) & grepl("\ttranscript\t", lines)]
    if (length(lines) == 0) return(NULL)
    
    # Extract transcript_id
    ids <- gsub('.*transcript_id "([^"]+)".*', '\\1', lines)
    
    # Extract coverage as count proxy
    cov_str <- gsub('.*cov "([^"]+)".*', '\\1', lines)
    cov <- suppressWarnings(as.numeric(cov_str))
    cov[is.na(cov)] <- 0
    counts <- round(cov * 100)
    
    df <- data.frame(
      transcript_id = ids,
      count = counts,
      stringsAsFactors = FALSE
    )
    colnames(df)[2] <- sample_name
    df <- df[!duplicated(df$transcript_id), ]
    return(df)
  }, error = function(e) {
    cat("  Warning: Could not parse", gtf_file, "\n")
    return(NULL)
  })
}

# Parse all samples
count_list <- list()
for (i in seq_along(count_files)) {
  s <- all_samples[i]
  cat("  Parsing:", s, "\n")
  df <- parse_counts(count_files[i], s)
  if (!is.null(df)) count_list[[s]] <- df
}

# Get union of all transcript IDs
all_ids <- unique(unlist(lapply(count_list, function(x) x$transcript_id)))
cat("  Total transcripts:", length(all_ids), "\n")

# Build matrix efficiently
count_matrix <- matrix(0L, nrow=length(all_ids), ncol=length(count_list),
                       dimnames=list(all_ids, names(count_list)))

for (s in names(count_list)) {
  df <- count_list[[s]]
  idx <- match(df$transcript_id, all_ids)
  valid <- !is.na(idx)
  count_matrix[idx[valid], s] <- as.integer(df[[s]][valid])
}

cat("  Matrix dimensions:", nrow(count_matrix), "x", ncol(count_matrix), "\n")

# Filter low counts
keep <- rowSums(count_matrix) >= min_count
count_matrix <- count_matrix[keep, ]
cat("  After filtering (min count", min_count, "):", nrow(count_matrix), "\n")

if (nrow(count_matrix) < 10) {
  cat("WARNING: Very few transcripts after filtering — lowering threshold\n")
  count_matrix <- matrix[rowSums(count_matrix) >= 1, ]
}

# ── DESeq2 ────────────────────────────────────────────────────
cat("\nRunning DESeq2...\n")

col_data <- data.frame(
  condition = factor(
    ifelse(colnames(count_matrix) %in% controls, "control", "drought"),
    levels = c("control", "drought")
  ),
  row.names = colnames(count_matrix)
)
cat("Sample conditions:\n")
print(col_data)

dds <- DESeqDataSetFromMatrix(count_matrix, col_data, ~condition)
dds <- DESeq(dds, quiet=TRUE)

res <- as.data.frame(results(
  dds,
  contrast = c("condition", "drought", "control"),
  alpha = padj_cutoff
))
res$transcript_id <- rownames(res)
res$drought_up <- !is.na(res$padj) &
                  res$padj < padj_cutoff &
                  res$log2FoldChange >= lfc_cutoff

cat("\nDE Summary:\n")
cat("  Total tested:           ", nrow(res), "\n")
cat("  Drought upregulated:    ", sum(res$drought_up, na.rm=TRUE), "\n")
cat("  Drought downregulated:  ",
    sum(!is.na(res$padj) & res$padj < padj_cutoff &
        res$log2FoldChange <= -lfc_cutoff, na.rm=TRUE), "\n")

write.table(res, out_all_de, sep="\t", quote=FALSE, row.names=FALSE)
cat("\nAll DE results saved:", out_all_de, "\n")

# ── Intersect with novel genes ────────────────────────────────
cat("\nFinding novel drought-upregulated genes...\n")

novel_up <- res[res$drought_up & res$transcript_id %in% novel_transcript_ids, ]
novel_up <- novel_up[order(novel_up$padj), ]

cat("  Novel drought-upregulated candidates:", nrow(novel_up), "\n")
write.table(novel_up, out_novel_up, sep="\t", quote=FALSE, row.names=FALSE)

# ── Volcano Plot ──────────────────────────────────────────────
cat("\nGenerating volcano plot...\n")

plot_df <- res %>%
  filter(!is.na(padj), !is.na(log2FoldChange)) %>%
  mutate(
    is_novel = transcript_id %in% novel_transcript_ids,
    group = case_when(
      is_novel & drought_up ~ "Novel + Drought UP",
      drought_up ~ "Drought UP",
      !is.na(padj) & padj < padj_cutoff &
        log2FoldChange <= -lfc_cutoff ~ "Drought DOWN",
      TRUE ~ "NS"
    ),
    nlp = pmin(-log10(padj + 1e-300), 50),
    label = ifelse(is_novel & drought_up, transcript_id, NA_character_)
  )

color_map <- c(
  "Novel + Drought UP" = "#E41A1C",
  "Drought UP"         = "#FF7F00",
  "Drought DOWN"       = "#377EB8",
  "NS"                 = "grey70"
)

p <- ggplot(plot_df, aes(log2FoldChange, nlp, color=group, label=label)) +
  geom_point(alpha=0.5, size=1.2) +
  geom_point(data=filter(plot_df, group=="Novel + Drought UP"),
             size=3, shape=17) +
  geom_text_repel(size=2.5, max.overlaps=15, na.rm=TRUE) +
  scale_color_manual(values=color_map, name="Category") +
  geom_vline(xintercept=c(-lfc_cutoff, lfc_cutoff),
             linetype="dashed", color="grey40") +
  geom_hline(yintercept=-log10(padj_cutoff),
             linetype="dashed", color="grey40") +
  labs(
    title = "Drought vs Control — Finger Millet (Eleusine coracana)",
    subtitle = paste0("Red triangles = novel drought-upregulated (n=",
                      nrow(novel_up), ")"),
    x = "log2 Fold Change (Drought/Control)",
    y = "-log10(adjusted p-value)"
  ) +
  theme_bw(base_size=12)

pdf(out_volcano, width=10, height=7)
print(p)
dev.off()
cat("Volcano plot saved:", out_volcano, "\n")

# ── Heatmap ───────────────────────────────────────────────────
cat("\nGenerating heatmap...\n")

if (nrow(novel_up) >= 2) {
  vst_data <- tryCatch(vst(dds, blind=FALSE),
                       error=function(e) rlog(dds, blind=FALSE))
  nm <- assay(vst_data)
  hm_genes <- novel_up$transcript_id[novel_up$transcript_id %in% rownames(nm)]

  if (length(hm_genes) >= 2) {
    hm_mat <- t(scale(t(nm[hm_genes, ])))
    ann_col <- data.frame(Condition=col_data$condition,
                          row.names=rownames(col_data))
    ann_colors <- list(Condition=c(control="#4DAF4A", drought="#E41A1C"))

    pdf(out_heatmap, width=9, height=max(6, length(hm_genes)*0.3+3))
    pheatmap(hm_mat, annotation_col=ann_col,
             annotation_colors=ann_colors,
             cluster_rows=TRUE, cluster_cols=TRUE,
             show_rownames=length(hm_genes)<=50,
             color=colorRampPalette(rev(brewer.pal(9,"RdBu")))(100),
             main="Novel Drought-Upregulated Genes (VST, row-scaled)",
             fontsize=9)
    dev.off()
  }
} else {
  pdf(out_heatmap)
  plot.new()
  text(0.5, 0.5, paste("Novel drought-upregulated candidates:", nrow(novel_up)))
  dev.off()
}

cat("\n=== DE Analysis Complete:", format(Sys.time()), "===\n")
cat("Novel drought-upregulated candidates:", nrow(novel_up), "\n")
sink(); sink(type="message")
