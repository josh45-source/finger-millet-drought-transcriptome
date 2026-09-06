#!/usr/bin/env Rscript
# =============================================================================
#  de_analysis_v2.R  --  Differential expression, re-run with genuine counts
#
#  NEW FILE. Does not modify or replace scripts/de_analysis.R, which is kept
#  verbatim as the historical record of what was actually run in April 2026.
#
#  WHY THIS EXISTS
#  ---------------
#  The original scripts/de_analysis.R parsed the `cov` attribute out of the
#  StringTie -e GTFs and fed DESeq2:
#
#        counts <- round(cov * 100)
#
#  That is per-base coverage rescaled by an arbitrary constant, not read counts.
#  It breaks the negative-binomial mean-variance relationship DESeq2 assumes,
#  and the rescaling factor is transcript-length dependent, so it distorts
#  transcripts unequally. The genuine count data produced by `stringtie -e -B`
#  existed on disk the whole time and was never used.
#
#  This script uses the prepDE.py transcript-level count matrix derived from
#  those same GTFs at the measured mean aligned read length of 142 bp.
#
#  INPUT   results_v2/counts/transcript_count_matrix_l142.csv
#  OUTPUT  results_v2/de/*, results_v2/figures/*
#
#  Everything under results/ is read-only to this script.
# =============================================================================

suppressPackageStartupMessages({
  library(DESeq2)
  library(apeglm)
  library(ggplot2)
  library(pheatmap)
  library(RColorBrewer)
})

set.seed(1)

# Package root. Override with:  export FM_ROOT=/path/to/package
PROJ      <- Sys.getenv("FM_ROOT", unset = ".")
COUNTS    <- file.path(PROJ, "results_v2/counts/transcript_count_matrix_l142.csv")
SAMPLES   <- file.path(PROJ, "results_v2/counts/sample_sheet.csv")
NOVEL_IDS <- file.path(PROJ, "results_v2/counts/novel_class_u_ids.txt")
OUT_DE    <- file.path(PROJ, "results_v2/de")
OUT_FIG   <- file.path(PROJ, "results_v2/figures")

PADJ_CUTOFF   <- 0.05   # same as config.yaml de_analysis.padj_cutoff
LOG2FC_CUTOFF <- 1.5    # same as config.yaml de_analysis.log2fc_cutoff
MIN_ROWSUM    <- 10     # prefilter

dir.create(OUT_DE,  recursive = TRUE, showWarnings = FALSE)
dir.create(OUT_FIG, recursive = TRUE, showWarnings = FALSE)

log_msg <- function(...) cat(sprintf("[%s] ", format(Sys.time(), "%H:%M:%S")), ..., "\n", sep = "")

# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------
cts <- read.csv(COUNTS, row.names = 1, check.names = FALSE)
cts <- as.matrix(cts)
mode(cts) <- "integer"

coldata <- read.csv(SAMPLES, row.names = 1, stringsAsFactors = FALSE)
coldata <- coldata[colnames(cts), , drop = FALSE]

# control is the reference level, so the contrast is drought vs control
coldata$condition <- factor(coldata$condition, levels = c("control", "drought"))

stopifnot(identical(rownames(coldata), colnames(cts)))
log_msg("Count matrix: ", nrow(cts), " transcripts x ", ncol(cts), " samples")
log_msg("Conditions:   ", paste(sprintf("%s=%s", rownames(coldata), coldata$condition), collapse = ", "))

novel_ids <- readLines(NOVEL_IDS)
log_msg("Novel (class_code u) transcript IDs: ", length(novel_ids))

# raw library sizes and detection, before any filtering
lib_size  <- colSums(cts)
detected  <- colSums(cts > 0)

# ---------------------------------------------------------------------------
# 2. DESeq2
# ---------------------------------------------------------------------------
dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design = ~ condition)

keep <- rowSums(counts(dds)) >= MIN_ROWSUM
log_msg("Prefilter rowSums >= ", MIN_ROWSUM, ": keeping ", sum(keep), " of ", length(keep),
        " (", sprintf("%.1f%%", 100 * sum(keep) / length(keep)), ")")
dds <- dds[keep, ]

dds <- DESeq(dds)

log_msg("Size factors: ", paste(sprintf("%s=%.4f", names(sizeFactors(dds)), sizeFactors(dds)), collapse = ", "))

# ---------------------------------------------------------------------------
# 3. Results, unshrunk (MLE) and shrunk (apeglm)
# ---------------------------------------------------------------------------
res_mle <- results(dds,
                   contrast = c("condition", "drought", "control"),
                   alpha    = PADJ_CUTOFF)

log_msg("Coefficient used for shrinkage: ", resultsNames(dds)[2])
res_ape <- lfcShrink(dds, coef = "condition_drought_vs_control", type = "apeglm")

res <- data.frame(
  transcript_id      = rownames(res_mle),
  baseMean           = res_mle$baseMean,
  log2FoldChange_MLE = res_mle$log2FoldChange,
  lfcSE_MLE          = res_mle$lfcSE,
  stat               = res_mle$stat,
  pvalue             = res_mle$pvalue,
  padj               = res_mle$padj,
  log2FoldChange_apeglm = res_ape$log2FoldChange[match(rownames(res_mle), rownames(res_ape))],
  lfcSE_apeglm          = res_ape$lfcSE[match(rownames(res_mle), rownames(res_ape))],
  stringsAsFactors   = FALSE
)
res$is_novel_class_u <- res$transcript_id %in% novel_ids

# per-sample normalised and raw counts, useful downstream
norm_counts <- counts(dds, normalized = TRUE)
raw_counts  <- counts(dds, normalized = FALSE)
ctrl_cols   <- rownames(coldata)[coldata$condition == "control"]
drt_cols    <- rownames(coldata)[coldata$condition == "drought"]

res$zero_in_all_controls <- rowSums(raw_counts[res$transcript_id, ctrl_cols, drop = FALSE]) == 0
res$ctrl_raw_sum <- rowSums(raw_counts[res$transcript_id, ctrl_cols, drop = FALSE])
res$drt_raw_sum  <- rowSums(raw_counts[res$transcript_id, drt_cols,  drop = FALSE])
res$ctrl_n_nonzero <- rowSums(raw_counts[res$transcript_id, ctrl_cols, drop = FALSE] > 0)

res <- res[order(res$padj, na.last = TRUE), ]
res$rank_by_padj <- seq_len(nrow(res))

write.table(res, file.path(OUT_DE, "all_de_results_v2.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

# significance defined on the unshrunk MLE, to match the original analysis
sig_up <- subset(res, !is.na(padj) & padj < PADJ_CUTOFF & log2FoldChange_MLE >= LOG2FC_CUTOFF)
write.table(sig_up, file.path(OUT_DE, "drought_upregulated_all_v2.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

novel_up <- subset(sig_up, is_novel_class_u)
write.table(novel_up, file.path(OUT_DE, "drought_upregulated_novel_genes_v2.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

# same thresholds but applied to the shrunk estimate, for comparison only
novel_up_ape <- subset(res, !is.na(padj) & padj < PADJ_CUTOFF &
                            log2FoldChange_apeglm >= LOG2FC_CUTOFF & is_novel_class_u)
write.table(novel_up_ape, file.path(OUT_DE, "drought_upregulated_novel_genes_v2_apeglm_threshold.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

log_msg("Tested (non-NA padj):            ", sum(!is.na(res$padj)))
log_msg("Drought-up, all transcripts:     ", nrow(sig_up))
log_msg("Drought-up, novel class-u (MLE): ", nrow(novel_up))
log_msg("Drought-up, novel class-u (ape): ", nrow(novel_up_ape))

# ---------------------------------------------------------------------------
# 4. Diagnostics
# ---------------------------------------------------------------------------
vsd <- vst(dds, blind = TRUE)

pcadata <- plotPCA(vsd, intgroup = "condition", returnData = TRUE)
pcavar  <- round(100 * attr(pcadata, "percentVar"))
pcadata$sample    <- rownames(pcadata)
pcadata$lib_size  <- lib_size[rownames(pcadata)]
pcadata$detected  <- detected[rownames(pcadata)]
write.table(pcadata, file.path(OUT_DE, "pca_coordinates.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

sampleDists    <- dist(t(assay(vsd)))
sdm            <- as.matrix(sampleDists)
write.table(sdm, file.path(OUT_DE, "sample_distance_matrix.tsv"), sep = "\t", quote = FALSE)

diag_lines <- c(
  "== library size vs detection ==",
  sprintf("%-12s %12s %12s %10s %10s", "sample", "lib_size", "detected", "PC1", "PC2"),
  sprintf("%-12s %12d %12d %10.2f %10.2f",
          pcadata$sample, pcadata$lib_size, pcadata$detected, pcadata$PC1, pcadata$PC2),
  "",
  sprintf("Pearson  r(lib_size, detected) = %.4f", cor(lib_size, detected)),
  sprintf("Spearman r(lib_size, detected) = %.4f", cor(lib_size, detected, method = "spearman")),
  sprintf("Pearson  r(lib_size, PC1)      = %.4f", cor(pcadata$lib_size, pcadata$PC1)),
  sprintf("Spearman r(lib_size, PC1)      = %.4f", cor(pcadata$lib_size, pcadata$PC1, method = "spearman")),
  sprintf("Pearson  r(detected, PC1)      = %.4f", cor(pcadata$detected, pcadata$PC1)),
  "",
  sprintf("PC1 variance explained = %d%%   PC2 = %d%%", pcavar[1], pcavar[2]),
  "",
  "== within-group vst distances ==",
  sprintf("control  mean=%.2f  range=%.2f-%.2f",
          mean(sdm[ctrl_cols, ctrl_cols][upper.tri(sdm[ctrl_cols, ctrl_cols])]),
          min(sdm[ctrl_cols, ctrl_cols][upper.tri(sdm[ctrl_cols, ctrl_cols])]),
          max(sdm[ctrl_cols, ctrl_cols][upper.tri(sdm[ctrl_cols, ctrl_cols])])),
  sprintf("drought  mean=%.2f  range=%.2f-%.2f",
          mean(sdm[drt_cols, drt_cols][upper.tri(sdm[drt_cols, drt_cols])]),
          min(sdm[drt_cols, drt_cols][upper.tri(sdm[drt_cols, drt_cols])]),
          max(sdm[drt_cols, drt_cols][upper.tri(sdm[drt_cols, drt_cols])])),
  sprintf("between  mean=%.2f  range=%.2f-%.2f",
          mean(sdm[ctrl_cols, drt_cols]), min(sdm[ctrl_cols, drt_cols]), max(sdm[ctrl_cols, drt_cols])),
  "",
  "== dispersion ==",
  sprintf("gene-wise dispersion  median=%.4f  IQR=%.4f-%.4f",
          median(mcols(dds)$dispGeneEst, na.rm = TRUE),
          quantile(mcols(dds)$dispGeneEst, .25, na.rm = TRUE),
          quantile(mcols(dds)$dispGeneEst, .75, na.rm = TRUE)),
  sprintf("final dispersion      median=%.4f  IQR=%.4f-%.4f",
          median(dispersions(dds), na.rm = TRUE),
          quantile(dispersions(dds), .25, na.rm = TRUE),
          quantile(dispersions(dds), .75, na.rm = TRUE)),
  sprintf("dispersionFunction: %s", paste(deparse(attr(dispersionFunction(dds), "coefficients")), collapse = " ")),
  "",
  "== detection-sensitivity audit of drought-up novel set ==",
  sprintf("novel drought-up total                       : %d", nrow(novel_up)),
  sprintf("  zero in ALL three control libraries        : %d (%.1f%%)",
          sum(novel_up$zero_in_all_controls),
          100 * sum(novel_up$zero_in_all_controls) / nrow(novel_up)),
  sprintf("  nonzero in 1 control library only          : %d", sum(novel_up$ctrl_n_nonzero == 1)),
  sprintf("  nonzero in 2 control libraries             : %d", sum(novel_up$ctrl_n_nonzero == 2)),
  sprintf("  nonzero in all 3 control libraries         : %d", sum(novel_up$ctrl_n_nonzero == 3)),
  sprintf("  control raw sum < 10 (low-but-nonzero)     : %d",
          sum(novel_up$ctrl_raw_sum > 0 & novel_up$ctrl_raw_sum < 10))
)
writeLines(diag_lines, file.path(OUT_DE, "diagnostics.txt"))
cat(paste(diag_lines, collapse = "\n"), "\n")

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
png(file.path(OUT_FIG, "dispersion_plot.png"), width = 1400, height = 1100, res = 150)
plotDispEsts(dds, main = "DESeq2 dispersion estimates (prepDE counts, l=142)")
dev.off()

png(file.path(OUT_FIG, "ma_plot_unshrunk.png"), width = 1400, height = 1100, res = 150)
DESeq2::plotMA(res_mle, ylim = c(-10, 10), main = "MA plot - unshrunk (MLE)")
abline(h = c(-LOG2FC_CUTOFF, LOG2FC_CUTOFF), col = "blue", lty = 2)
dev.off()

png(file.path(OUT_FIG, "ma_plot_apeglm.png"), width = 1400, height = 1100, res = 150)
DESeq2::plotMA(res_ape, ylim = c(-10, 10), main = "MA plot - apeglm shrunk")
abline(h = c(-LOG2FC_CUTOFF, LOG2FC_CUTOFF), col = "blue", lty = 2)
dev.off()

p <- ggplot(pcadata, aes(PC1, PC2, colour = condition, label = sample)) +
  geom_point(size = 5) +
  geom_text(vjust = -1.2, size = 3.2, show.legend = FALSE) +
  xlab(sprintf("PC1: %d%% variance", pcavar[1])) +
  ylab(sprintf("PC2: %d%% variance", pcavar[2])) +
  coord_fixed() + theme_bw() +
  ggtitle("PCA of vst-transformed counts")
ggsave(file.path(OUT_FIG, "pca.png"), p, width = 8, height = 6, dpi = 150)

p2 <- ggplot(pcadata, aes(lib_size / 1e6, PC1, colour = condition, label = sample)) +
  geom_point(size = 5) + geom_text(vjust = -1.2, size = 3.2, show.legend = FALSE) +
  xlab("library size (millions)") + ylab(sprintf("PC1 (%d%% var)", pcavar[1])) +
  theme_bw() + ggtitle(sprintf("PC1 vs library size  (Pearson r = %.3f)",
                               cor(pcadata$lib_size, pcadata$PC1)))
ggsave(file.path(OUT_FIG, "pc1_vs_library_size.png"), p2, width = 8, height = 6, dpi = 150)

p3 <- ggplot(pcadata, aes(lib_size / 1e6, detected / 1e3, colour = condition, label = sample)) +
  geom_point(size = 5) + geom_text(vjust = -1.2, size = 3.2, show.legend = FALSE) +
  xlab("library size (millions)") + ylab("transcripts detected (thousands)") +
  theme_bw() + ggtitle(sprintf("Detection vs depth  (Pearson r = %.3f)",
                               cor(lib_size, detected)))
ggsave(file.path(OUT_FIG, "detection_vs_depth.png"), p3, width = 8, height = 6, dpi = 150)

colours <- colorRampPalette(rev(brewer.pal(9, "Blues")))(255)
rownames(sdm) <- paste(rownames(sdm), coldata$condition, sep = " - ")
colnames(sdm) <- NULL
png(file.path(OUT_FIG, "sample_distance_heatmap.png"), width = 1200, height = 1000, res = 150)
pheatmap(sdm, clustering_distance_rows = sampleDists,
         clustering_distance_cols = sampleDists, col = colours,
         main = "Sample-to-sample distances (vst)")
dev.off()

# ---------------------------------------------------------------------------
# 6. Session info
# ---------------------------------------------------------------------------
writeLines(capture.output(sessionInfo()), file.path(OUT_DE, "sessionInfo.txt"))
log_msg("Done.")
