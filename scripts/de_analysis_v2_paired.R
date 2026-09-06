#!/usr/bin/env Rscript
# =============================================================================
#  de_analysis_v2_paired.R  --  paired (~ plant + condition) vs unpaired
#                               (~ condition) model comparison
#
#  NEW FILE. Does not modify scripts/de_analysis.R or scripts/de_analysis_v2.R.
#
#  RATIONALE
#  ---------
#  Hatakeyama et al. 2018 section 2.2 states that leaf tissue was taken from the
#  SAME plants before and after 7 days of withheld water. That makes this a
#  repeated-measures design, and ~ condition alone is misspecified: it treats
#  six independent samples where there are three plants measured twice.
#
#  The pairing is inferred from the ENA library-name suffixes:
#      Illumina_RNA_ctl_1 <-> Illumina_RNA_dry_1  = plant 1
#      Illumina_RNA_ctl_2 <-> Illumina_RNA_dry_2  = plant 2
#      Illumina_RNA_ctl_3 <-> Illumina_RNA_dry_3  = plant 3
#  mapped onto run accessions in order:
#      DRR095904 <-> DRR095907   plant 1
#      DRR095905 <-> DRR095908   plant 2
#      DRR095906 <-> DRR095909   plant 3
#
#  This is an INFERENCE, not archive-confirmed. The test of whether it is right
#  is empirical: if the suffixes really encode plant identity, blocking on plant
#  should absorb a substantial share of the between-replicate variance and drop
#  the dispersion. If dispersion is unchanged, the suffixes are just numbering
#  and the pairing is spurious.
#
#  CONFOUND, unavoidable under either model: controls were sampled 7 days before
#  the drought samples, so treatment is perfectly confounded with plant age and
#  with any batch effect associated with the two collection dates. Blocking on
#  plant does not remove this; nothing in this dataset can.
# =============================================================================

suppressPackageStartupMessages({
  library(DESeq2); library(apeglm); library(ggplot2)
  library(pheatmap); library(RColorBrewer)
})
set.seed(1)

# Package root. Override with:  export FM_ROOT=/path/to/package
PROJ      <- Sys.getenv("FM_ROOT", unset = ".")
COUNTS    <- file.path(PROJ, "results_v2/counts/transcript_count_matrix_l142.csv")
SAMPLES   <- file.path(PROJ, "results_v2/counts/sample_sheet.csv")
NOVEL_IDS <- file.path(PROJ, "results_v2/counts/novel_class_u_ids.txt")
OUT_DE    <- file.path(PROJ, "results_v2/de")
OUT_FIG   <- file.path(PROJ, "results_v2/figures")

PADJ_CUTOFF <- 0.05
LOG2FC_CUTOFF <- 1.5
MIN_ROWSUM <- 10

CANDIDATES <- c("MSTRG.31255.1","MSTRG.20738.1","MSTRG.21998.1","MSTRG.6647.1",
                "MSTRG.37761.2","MSTRG.4687.1","MSTRG.45758.1","MSTRG.45757.2")

log_msg <- function(...) cat(sprintf("[%s] ", format(Sys.time(), "%H:%M:%S")), ..., "\n", sep = "")

cts <- as.matrix(read.csv(COUNTS, row.names = 1, check.names = FALSE))
mode(cts) <- "integer"
coldata <- read.csv(SAMPLES, row.names = 1, stringsAsFactors = FALSE)
coldata <- coldata[colnames(cts), , drop = FALSE]
coldata$condition <- factor(coldata$condition, levels = c("control", "drought"))

# pairing inferred from library-name suffix
pair_map <- c(DRR095904 = "1", DRR095907 = "1",
              DRR095905 = "2", DRR095908 = "2",
              DRR095906 = "3", DRR095909 = "3")
coldata$plant <- factor(pair_map[rownames(coldata)])

log_msg("Sample sheet:")
print(coldata[, c("condition", "plant", "library_name")])

novel_ids <- readLines(NOVEL_IDS)

run_model <- function(design, tag) {
  log_msg("=== model ", tag, " : ", deparse(design))
  dds <- DESeqDataSetFromMatrix(cts, coldata, design = design)
  dds <- dds[rowSums(counts(dds)) >= MIN_ROWSUM, ]
  dds <- DESeq(dds, quiet = TRUE)

  res_mle <- results(dds, contrast = c("condition", "drought", "control"),
                     alpha = PADJ_CUTOFF)
  res_ape <- lfcShrink(dds, coef = "condition_drought_vs_control",
                       type = "apeglm", quiet = TRUE)

  out <- data.frame(
    transcript_id = rownames(res_mle),
    baseMean = res_mle$baseMean,
    log2FoldChange_MLE = res_mle$log2FoldChange,
    lfcSE_MLE = res_mle$lfcSE,
    pvalue = res_mle$pvalue,
    padj = res_mle$padj,
    log2FoldChange_apeglm = res_ape$log2FoldChange[match(rownames(res_mle), rownames(res_ape))],
    lfcSE_apeglm = res_ape$lfcSE[match(rownames(res_mle), rownames(res_ape))],
    stringsAsFactors = FALSE
  )
  out$is_novel_class_u <- out$transcript_id %in% novel_ids
  out <- out[order(out$padj, na.last = TRUE), ]
  out$rank_by_padj <- seq_len(nrow(out))

  sig_up   <- subset(out, !is.na(padj) & padj < PADJ_CUTOFF & log2FoldChange_MLE >= LOG2FC_CUTOFF)
  novel_up <- subset(sig_up, is_novel_class_u)

  list(dds = dds, res = out, sig_up = sig_up, novel_up = novel_up, tag = tag,
       asymptDisp = attr(dispersionFunction(dds), "coefficients")[["asymptDisp"]],
       extraPois  = attr(dispersionFunction(dds), "coefficients")[["extraPois"]],
       med_gene_disp = median(mcols(dds)$dispGeneEst, na.rm = TRUE),
       med_final_disp = median(dispersions(dds), na.rm = TRUE),
       n_tested = sum(!is.na(out$padj)))
}

m_un <- run_model(~ condition,         "unpaired")
m_pa <- run_model(~ plant + condition, "paired")

write.table(m_pa$res, file.path(OUT_DE, "all_de_results_v2_paired.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
write.table(m_pa$novel_up, file.path(OUT_DE, "drought_upregulated_novel_genes_v2_paired.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

# ---------------------------------------------------------------------------
fmt <- function(m) sprintf(
  "%-10s asymptDisp=%.4f  extraPois=%.2f  med_geneEst=%.4f  med_final=%.4f  tested=%d  novel_up=%d  all_up=%d",
  m$tag, m$asymptDisp, m$extraPois, m$med_gene_disp, m$med_final_disp,
  m$n_tested, nrow(m$novel_up), nrow(m$sig_up))

lines <- c("=========== MODEL COMPARISON ===========", fmt(m_un), fmt(m_pa), "",
  sprintf("asymptDisp change   : %.4f -> %.4f  (%+.1f%%)",
          m_un$asymptDisp, m_pa$asymptDisp,
          100*(m_pa$asymptDisp - m_un$asymptDisp)/m_un$asymptDisp),
  sprintf("median final disp   : %.4f -> %.4f  (%+.1f%%)",
          m_un$med_final_disp, m_pa$med_final_disp,
          100*(m_pa$med_final_disp - m_un$med_final_disp)/m_un$med_final_disp),
  sprintf("novel drought-up    : %d -> %d  (%+d)",
          nrow(m_un$novel_up), nrow(m_pa$novel_up),
          nrow(m_pa$novel_up) - nrow(m_un$novel_up)),
  "")

ovl <- length(intersect(m_un$novel_up$transcript_id, m_pa$novel_up$transcript_id))
lines <- c(lines,
  sprintf("novel set overlap   : %d shared; %d unpaired-only; %d paired-only",
          ovl, nrow(m_un$novel_up)-ovl, nrow(m_pa$novel_up)-ovl), "",
  "=========== CANDIDATES ===========",
  sprintf("%-16s %-34s %-34s", "", "--------- UNPAIRED ---------", "---------- PAIRED ----------"),
  sprintf("%-16s %10s %11s %6s   %10s %11s %6s",
          "transcript","log2FC","padj","rank","log2FC","padj","rank"))

for (t in CANDIDATES) {
  a <- m_un$res[m_un$res$transcript_id == t, ]
  b <- m_pa$res[m_pa$res$transcript_id == t, ]
  lines <- c(lines, sprintf("%-16s %10.3f %11.3g %6d   %10.3f %11.3g %6d",
    t, a$log2FoldChange_MLE, a$padj, a$rank_by_padj,
       b$log2FoldChange_MLE, b$padj, b$rank_by_padj))
}

writeLines(lines, file.path(OUT_DE, "paired_vs_unpaired.txt"))
cat(paste(lines, collapse = "\n"), "\n")

png(file.path(OUT_FIG, "dispersion_plot_paired.png"), width = 1400, height = 1100, res = 150)
plotDispEsts(m_pa$dds, main = "Dispersion estimates -- paired model (~ plant + condition)")
dev.off()

vsd <- vst(m_pa$dds, blind = FALSE)
pd <- plotPCA(vsd, intgroup = c("condition","plant"), returnData = TRUE)
pv <- round(100*attr(pd,"percentVar"))
pd$sample <- rownames(pd)
p <- ggplot(pd, aes(PC1, PC2, colour = condition, shape = plant, label = sample)) +
  geom_point(size = 5) + geom_text(vjust = -1.2, size = 3, show.legend = FALSE) +
  xlab(sprintf("PC1: %d%% variance", pv[1])) + ylab(sprintf("PC2: %d%% variance", pv[2])) +
  theme_bw() + ggtitle("PCA, vst (blind=FALSE, paired design)")
ggsave(file.path(OUT_FIG, "pca_paired.png"), p, width = 8, height = 6, dpi = 150)

writeLines(capture.output(sessionInfo()), file.path(OUT_DE, "sessionInfo_paired.txt"))
log_msg("Done.")
