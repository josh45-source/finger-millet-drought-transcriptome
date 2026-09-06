# results_v2/ — CORRECTED RE-ANALYSIS

**Status: current. These are the results to use.**

Produced 26–28 August 2026. Supersedes `../results_v1/`. Full old-vs-new
reconciliation in `../docs/DE_COMPARISON.md`; manuscript-level consequences in
`../docs/MANUSCRIPT_CORRECTIONS.md`.

## What changed

| | v1 | v2 |
|---|---|---|
| DESeq2 input | `round(cov * 100)` | `prepDE.py` counts, read length 142 bp |
| Count validation | none | `featureCounts`, Spearman rho 0.985–0.995 |
| Shrinkage | none | `lfcShrink(type="apeglm")`, reported alongside MLE |
| BLAST join key | broken (`transcript::coords` vs `MSTRG.x.y`) | transcript ID |
| Novel drought-up | 2,354 | **2,422** |
| No Swiss-Prot homology | 99.6% (an artefact) | **63.5%** |

## Contents

- `de/` — DESeq2 output for both the unpaired (`~ condition`, primary) and paired
  (`~ plant + condition`, tested and rejected) models, diagnostics, PCA coordinates,
  sample distances, session info, and the old-vs-new log2FC table.
- `counts/` — `prepDE.py` transcript- and gene-level matrices at read lengths 142 and
  151 bp, the `featureCounts` cross-check, the sample sheet, the class-code-u ID list,
  and the 39 transcripts StringTie `-e` failed to emit for every sample.
- `annotation/` — the re-run BLASTx joined on transcript ID: the 2,422 set, the
  original 2,354 set re-annotated for like-for-like comparison, and best hits for all
  21,864 novel transcripts.
- `blast/` — raw BLASTx output, the BED used for extraction, and the run script.

Figures are in `../figures_v2/`; run logs in `../logs/`.

## Read length

`prepDE.py` was run at the measured mean aligned read length of **142 bp** (sampled
across four 4 Mb windows on chromosomes 1A, 3B, 6A and 9A in every BAM; modal length
is 151 bp but the reads are Trimmomatic-trimmed). The 151 bp matrices are included as
a sensitivity check: they rescale every count by a uniform 0.9405, which DESeq2's size
factors absorb entirely. **Read-length choice does not affect any differential
expression result.**
