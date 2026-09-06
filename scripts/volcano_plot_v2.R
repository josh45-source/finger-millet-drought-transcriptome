#!/usr/bin/env Rscript
# volcano_plot_v2.R
#
# Draws figures_v2/volcano_plot.png (manuscript Figure 2) from the v2 DESeq2
# table written by de_analysis_v2.R. Read-only with respect to the DE results:
# it recomputes nothing and refits nothing, it only plots what is already in
# results_v2/de/all_de_results_v2.tsv.
#
# Style follows the ggplot panels emitted by de_analysis_v2.R (theme_bw,
# ggsave at 8 x 6 in, 150 dpi) so the figure sits alongside pca.png,
# pc1_vs_library_size.png and detection_vs_depth.png without restyling.
#
# Fold changes are the unshrunk MLE, which is the estimate the significance
# thresholds were applied to in de_analysis_v2.R.
#
# Usage:  Rscript scripts/volcano_plot_v2.R
#         FM_ROOT=/path/to/deposit Rscript scripts/volcano_plot_v2.R

suppressPackageStartupMessages(library(ggplot2))

ROOT     <- Sys.getenv("FM_ROOT", ".")
DE_FILE  <- file.path(ROOT, "results_v2", "de", "all_de_results_v2.tsv")
OUT_FIG  <- file.path(ROOT, "figures_v2")

PADJ_CUTOFF    <- 0.05
LOG2FC_CUTOFF  <- 1.5
X_CAP          <- 10    # matches the ylim of the MA plots in de_analysis_v2.R
Y_CAP          <- 50    # -log10(padj); above this the axis is uninformative

res <- read.delim(DE_FILE, stringsAsFactors = FALSE)

# Transcripts DESeq2 did not test (independent filtering / all-zero) carry
# padj = NA and are not plottable on a volcano.
res <- res[!is.na(res$padj) & !is.na(res$log2FoldChange_MLE), ]

# One transcript underflows to padj = 0. Set it to the smallest representable
# non-zero padj in the table so -log10 stays finite; it is capped anyway.
min_nonzero <- min(res$padj[res$padj > 0])
res$padj[res$padj == 0] <- min_nonzero

res$neglog10padj <- -log10(res$padj)

sig_up_novel <- res$is_novel_class_u == "TRUE" &
                res$padj < PADJ_CUTOFF &
                res$log2FoldChange_MLE >= LOG2FC_CUTOFF

res$category <- "all other transcripts"
res$category[sig_up_novel & res$zero_in_all_controls == "FALSE"] <-
  "drought-up, absent from annotation"
res$category[sig_up_novel & res$zero_in_all_controls == "TRUE"]  <-
  "drought-up, zero control counts (lower bound)"

res$category <- factor(res$category, levels = c(
  "all other transcripts",
  "drought-up, absent from annotation",
  "drought-up, zero control counts (lower bound)"))

# Clip to the plotting window; clipped points are drawn as open triangles so
# the axis limits never hide that a point lies outside them.
res$x <- pmax(pmin(res$log2FoldChange_MLE, X_CAP), -X_CAP)
res$y <- pmin(res$neglog10padj, Y_CAP)
res$clipped <- abs(res$log2FoldChange_MLE) > X_CAP | res$neglog10padj > Y_CAP

n_tested  <- nrow(res)
n_clipped <- sum(res$clipped)
n_blue    <- sum(res$category == "drought-up, absent from annotation")
n_orange  <- sum(res$category == "drought-up, zero control counts (lower bound)")

cat(sprintf("tested transcripts plotted : %d\n", n_tested))
cat(sprintf("  drought-up, novel        : %d\n", n_blue))
cat(sprintf("  drought-up, zero control : %d\n", n_orange))
cat(sprintf("  total significant novel  : %d\n", n_blue + n_orange))
cat(sprintf("  clipped to plot window   : %d\n", n_clipped))

# Draw the grey background first, then the highlighted sets on top.
res <- res[order(res$category), ]

p <- ggplot(res, aes(x, y, colour = category, shape = clipped)) +
  geom_hline(yintercept = -log10(PADJ_CUTOFF), linetype = "dashed",
             colour = "grey30", linewidth = 0.4) +
  geom_vline(xintercept = c(-LOG2FC_CUTOFF, LOG2FC_CUTOFF), linetype = "dashed",
             colour = "grey30", linewidth = 0.4) +
  geom_point(size = 0.7, alpha = 0.5) +
  scale_colour_manual(values = c(
    "all other transcripts"                         = "grey70",
    "drought-up, absent from annotation"            = "#2c7fb8",
    "drought-up, zero control counts (lower bound)" = "#d95f02"),
    name = NULL) +
  scale_shape_manual(values = c(`FALSE` = 16, `TRUE` = 2), guide = "none") +
  scale_x_continuous(limits = c(-X_CAP, X_CAP)) +
  scale_y_continuous(limits = c(0, Y_CAP)) +
  xlab(expression(log[2]~fold~change~(drought~vs~control))) +
  ylab(expression(-log[10]~adjusted~p)) +
  theme_bw() +
  theme(legend.position = "bottom",
        legend.text = element_text(size = 8),
        legend.margin = margin(t = 0, b = 0),
        legend.box.spacing = unit(4, "pt"),
        legend.key.height = unit(10, "pt"),
        plot.subtitle = element_text(size = 8)) +
  guides(colour = guide_legend(nrow = 3, byrow = TRUE,
                               override.aes = list(size = 2.5, alpha = 1))) +
  ggtitle("Volcano plot - drought vs control (unshrunk MLE)",
          subtitle = sprintf(
            "%s transcripts tested; open triangles clipped at |log2FC| = %d or -log10(padj) = %d (n = %s)",
            format(n_tested, big.mark = ","), X_CAP, Y_CAP,
            format(n_clipped, big.mark = ",")))

ggsave(file.path(OUT_FIG, "volcano_plot.png"), p, width = 8, height = 6, dpi = 150)
cat(sprintf("wrote %s\n", file.path(OUT_FIG, "volcano_plot.png")))
