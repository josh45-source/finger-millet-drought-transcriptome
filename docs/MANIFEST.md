# MANIFEST — Finger Millet Drought Transcriptome, Deposition Package

**Regenerated:** 28 August 2026, from the package as it actually stands;
`manuscript/` added and every count and size re-derived 6 September 2026.
**Package root:** `/mnt/d/finger_millet_zenodo/`
**Contents:** **217 files** across **25 directories**, **164,152,862 B (156.5 MB)**.

Reference assembly used throughout: **GCA_032690845.1** (`Eleusine_coracana_v1.0`,
*Eleusine coracana* subsp. *coracana* cv. KNE 796-S) — chromosome-scale, 18
pseudomolecules, 532 sequences, 1,111,714,373 bp, N50 61,270,980 bp.

> ## The package contains two analyses
>
> **`results_v2/` is the corrected re-analysis and supersedes `results_v1/`.**
> `results_v1/` is the April 2026 analysis exactly as performed, retained unmodified as a
> historical record because four defects were found in it. Its numbers should not be
> quoted. Each directory carries its own `README.md` stating this.

Every file present is listed below, and every file listed is present — verified
programmatically; see `docs/VERIFICATION.md` §2 (second verification).

---

## 1. Root

| File | Size | Description |
|---|---|---|
| `.gitignore` | 96 B | Excludes OS cruft (`.DS_Store`, `Thumbs.db`) from the deposit and from any mirror repository. |
| `CITATION.cff` | 6,267 B | Citation metadata, CFF 1.2.0. `type: dataset`, version 2.0.0, dual licence `[MIT, CC-BY-4.0]`. References Hatakeyama 2018 (RNA-seq source), GCA_032690845.1 (genome) and Lloyd et al. 2019 (ITR homology-rate context). |
| `LICENSE` | 25,049 B | Dual-licence statement plus both full texts: MIT (Part 1, governs `scripts/`) and CC BY 4.0 (Part 2, governs everything else). Includes a list of third-party material covered by neither. CC BY legal code retrieved from creativecommons.org on 28 Aug 2026 and reproduced unaltered. |
| `README.md` | 26,853 B | Package overview: corrected headline results, the lead candidate, data sources, workflow, repository structure, known defects, limitations, reproducibility status, AI-use disclosure, licence and citation. |

## 2. `workflow/` — pipeline definition

| File | Size | Description |
|---|---|---|
| `LICENSE` | 1,073 B | MIT licence text, standalone copy governing `workflow/Snakefile` and `workflow/setup.sh`. `workflow/config.yaml` is configuration data and remains under CC BY 4.0. |
| `Snakefile` | 17,353 B | **MIT-licensed** (see `workflow/LICENSE`). Snakemake 9.19.0 workflow. Stages 1-5 plus Swiss-Prot annotation: reference download, HISAT2 index, read download, FastQC/MultiQC, Trimmomatic, HISAT2 alignment, StringTie assemble/merge/count, gffcompare, novel-transcript extraction, DESeq2, blastx, final report, tool-version logging. **Sanitised for deposition** - see section 6. |
| `config.yaml` | 3,011 B | **CC BY 4.0** — configuration data, not code. Sample accessions, reference URLs and local paths, trimming/alignment/StringTie/DE/BLAST parameters, resource limits. **MODIFIED IN THIS COPY** - see section 6. |
| `setup.sh` | 4,308 B | **MIT-licensed** (see `workflow/LICENSE`). Environment bootstrap: conda environment creation and directory scaffold. **Sanitised for deposition** - see section 6. |

## 3. `scripts/` — analysis scripts

Files here are maintained source. Twenty further scripts exist only as recoveries from
shell history and are held separately in `scripts/reconstructed/` — see §7.

| File | Size | Description |
|---|---|---|
| `LICENSE` | 1,073 B | MIT licence text, standalone copy governing `scripts/` and everything beneath it. |
| `analyze_structures.cxc` | 8,684 B | UCSF ChimeraX command script. **DOES NOT RUN AS WRITTEN - retained as a provenance artefact only.** Three of its four `open` statements name model files that do not exist, and the lead candidate is never opened. A 53-line header added 28 Aug 2026 states all four defects and records that the absolute paths are retained deliberately as provenance; the 5,709-byte body beneath it is byte-identical to the original. **It is not the record of the prediction settings** - `structures/*/config.json` is. |
| `de_analysis.R` | 9,218 B | **v1.** DESeq2 differential expression, called by Snakefile `rule de_analysis`. Builds its count matrix as `round(cov * 100)` from StringTie `cov` values - **this is defect 1**; design `~condition`, contrast drought-vs-control, filter `rowSums >= 10`, thresholds padj < 0.05 and log2FC >= 1.5. No `lfcShrink()`. Retained as the record of what was run. |
| `de_analysis_v2.R` | 13,692 B | **v2, primary analysis.** DESeq2 on the prepDE transcript-level matrix at read length 142 bp. Design `~ condition`, control as reference, contrast drought-vs-control, prefilter `rowSums >= 10`, thresholds padj < 0.05 and log2FC >= 1.5 applied to the unshrunk MLE to match v1. `lfcShrink(type="apeglm")` reported alongside. Emits the DE tables, diagnostics, PCA coordinates, sample distances and every figure in `figures_v2/` except `volcano_plot.png`, which is drawn by `volcano_plot_v2.R`. |
| `de_analysis_v2_paired.R` | 8,116 B | **v2.** Fits `~ plant + condition` alongside `~ condition` and compares dispersion, tested counts and per-candidate significance. The paired model was **rejected** - see §12. |
| `merge_results.py` | 3,796 B | **v1.** Called by Snakefile `rule final_report`. Joins drought-upregulated novel transcripts to Swiss-Prot blastx hits. **Contains defects 2 and 3**: the join key never matches, and `STRESS_WORDS` are tested as substrings. Retained as the record of what was run. |
| `rebuild_annotation_v2.py` | 7,530 B | **v2.** Rebuilds the annotation table with a clean join on transcript ID. Reproduces `merge_results.py`'s tier rules verbatim (including its `STRESS_WORDS` list) and emits both its 3-string scheme and the 4-string scheme used in the candidate tables. |
| `run_foldseek.sh` | 6,319 B | First Foldseek submission attempt (19 Apr 2026, 22:55). All four submissions returned `HTTP 400: selected databases are not valid`. Retained for provenance; superseded by the file below. **Sanitised** - paths now read from `$FM_STRUCTURES`. |
| `run_foldseek_webapi.sh` | 6,823 B | Corrected Foldseek client (19 Apr 2026, 23:16) that produced the retained results. Submits to `search.foldseek.com/api/ticket` with `mode=3diaa` against afdb50, afdb-swissprot, afdb-proteome, pdb100. **Sanitised** - paths now read from `$FM_STRUCTURES`. |
| `volcano_plot_v2.R` | 4,970 B | **v2.** Draws `figures_v2/volcano_plot.png` (manuscript Figure 2) from `results_v2/de/all_de_results_v2.tsv`. Plots only; it refits nothing. Reproduces the published counts exactly: 76,917 tested transcripts, 2,422 drought-upregulated novel (1,144 with control signal, 1,278 zero-in-all-controls). Style matches the ggplot panels of `de_analysis_v2.R`. Added 5 Sep 2026, after the figure legends were reconciled against the deposited figures. |

## 4. `scripts/reconstructed/` — scripts recovered from shell history

**These twenty scripts were never saved to disk during the analysis.** They were typed
directly into an interactive shell as `python3 << 'EOF' … EOF` heredocs and survive only
as text inside `~/.bash_history`. They are reproduced here **verbatim** — nothing
corrected, reformatted, improved or sanitised. Only a provenance header was prepended.

**They must not be cited as original source code.** See
`scripts/reconstructed/README.md` for status, prerequisites and the note on the
placeholder email address.

### 4.1 Extracted scripts

| File | Stage | History lines | Size | Purpose / output |
|---|---|---|---|---|
| `heroGene01_cysteine_comparison_MSTRG31255.py` | hero | 650-670 | 2,459 B | Prints the 104 aa MSTRG.31255.1 peptide beside *Leersia perrieri* A0A0D9XDT2 with cysteines highlighted. Informal — **not a family assignment** |
| `heroGene02_ncbi_blastp_web_submit.py` | hero | 673-712 | 2,895 B | Submits the 76 aa mature peptide to the NCBI BLAST URL API. **Results printed to terminal only; not retained** |
| `heroGene03_ncbi_blastp_web_submit_v2.py` | hero | 714-785 | 3,775 B | Second NCBI blastp attempt with EBI REST fallback. **Results not retained.** Contains the placeholder contact address `joshua@research.com` required by the EBI API |
| `stage06a_select_top50_by_padj.py` | 6 | 312-330 | 2,091 B | Sorts `candidate_genes_final.tsv` by padj ascending, takes the first 50. **Defines the entire downstream candidate set.** → `top50_ids.txt` |
| `stage06b_report_top50_coordinates.py` | 6 | 335-361 | 2,289 B | Prints top-50 genomic coordinates. Diagnostic only |
| `stage06c_build_top50_bed.py` | 6 | 365-393 | 2,444 B | Builds `top50.bed` from transcript start/end. **No exon records exist in `novel_genes.gtf`, so extraction is unspliced genomic** → `top50.bed` |
| `stage06d_identify_candidates_without_orf.py` | 6 | 411-434 | 2,191 B | Identifies the 6 candidates with no TransDecoder ORF. Diagnostic only |
| `stage06e_clean_peptide_fasta.py` | 6 | 440-468 | 2,295 B | Rewrites peptides with bare MSTRG headers, strips stop asterisks → `top50_clean.pep` (the InterProScan input) |
| `stage08a_report_top10_coordinates.py` | 8 | 877-907 | 2,340 B | Prints top-10 coordinates, used to hand-build the table in `stage08b`. Diagnostic only |
| `stage08b_build_promoter_bed.py` | 8 | 909-946 | 2,841 B | Strand-aware **1,000 bp** upstream windows from hard-coded coordinates → `promoters.bed` |
| `stage08c_scan_promoter_motifs.py` | 8 | 949-1013 | 3,697 B | **The promoter/ABRE scanner.** Exact-substring count of six hard-coded motifs. `has_ABRE` is true if **any** of the six matched, including W-box and MYB → `abre_results.tsv` |
| `stage09a_extract_uniprot_ids_for_gprofiler.py` | 9 | 1163-1233 | 3,775 B | Parses `sp|ACC|` accessions from blastx hits for manual g:Profiler submission. 29 written; only 9 mapped |
| `stage10a_build_expression_matrix.py` | 10 | 1021-1082 | 3,353 B | Extracts raw StringTie `cov` per candidate per sample → `expression_matrix.tsv` |
| `stage10b_pearson_correlation_candidates.py` | 10 | 1084-1154 | 3,436 B | Hand-written Pearson across candidate pairs, n = 6. No p-values or correction |
| `stage10c_locate_known_genes_and_extract_expression.py` | 10 | 1252-1343 | 4,610 B | Locates the 5 marker genes by best blastn hit; takes max coverage of any overlapping transcript |
| `stage10d_pearson_correlation_vs_known_genes.py` | 10 | 1345-1429 | 4,544 B | **The co-expression script behind the reported r values.** Expression matrices are embedded as hard-coded literals; its only `open()` is the output write. All 10 candidate vectors were independently verified against `results/counts/*.gtf` — 10/10 exact → `novel_vs_known_correlation.tsv` |
| `stage11a_report_top10_coordinates_for_synteny.py` | 11 | 1434-1464 | 2,350 B | Prints top-10 coordinates before the BLAST searches. Diagnostic only |
| `stage11b_parse_sorghum_blast.py` | 11 | 1487-1564 | 3,989 B | Best hit per gene by bitscore from `vs_sorghum.txt` → `synteny_summary.tsv` |
| `stage11c_classify_two_species.py` | 11 | 1570-1640 | 3,786 B | Two-species classifier. Produced the **superseded** 5-Eleusine-specific table |
| `stage11d_classify_three_species.py` | 11 | 1646-1726 | 4,225 B | **The definitive synteny classifier** (sorghum + rice + foxtail). Produced the 4/1/1/4 classification. Top-10 list is hard-coded → `synteny_3species.tsv` |

**Total: 20 scripts + README, 66 KB.**

Extraction was verified, not asserted: each file's body was compared byte-for-byte against
the corresponding `~/.bash_history` line range — **all 20 match exactly**, re-confirmed
on 28 August 2026 after sanitisation of the other scripts. All 20 parse as valid Python 3
(`ast.parse`), which is a syntax check only.

### 4.2 Non-`python3` heredocs — not extracted

| Line | Heredoc | Content | Included? |
|---|---|---|---|
| 632 | `cat > /tmp/defensins.fasta << 'EOF'` | Two-record FASTA — **data, not code** | Yes, as `results_v1/sequences/defensins.fasta` |
| 519, 791, 832 | `cat > main.tex << 'ENDOFFILE'` | LaTeX manuscript skeleton revisions | No — not analysis code |

## 5. `results_v1/` — ORIGINAL ANALYSIS, SUPERSEDED

**Do not quote these numbers.** Retained so published claims can be traced to the files
that produced them, and so the corrections can be checked against them.

| File | Size | Description |
|---|---|---|
| `README.md` | 26,853 B | Status marker: original analysis, superseded, do not quote these numbers. Lists the four defects and the v2 files that supersede each table. |
| `all_de_results.tsv` | 11,303,880 B | **v1, superseded.** Complete DESeq2 output for all 88,336 tested transcripts. Produced from the `round(cov * 100)` input. |
| `drought_upregulated_novel_genes.tsv` | 300,440 B | **v1, superseded.** The original headline result: 2,354 novel class-`u` drought-upregulated transcripts at padj < 0.05 and log2FC >= 1.5, sorted by padj. |
| `iprscan5-R20260417-190817-0777-66196655-p1m.tsv` | 382,359 B | InterProScan 5 output from the EBI REST service, job submitted 17 Apr 2026 19:08:17. 37 of 44 proteins annotated across 18 member databases. InterProScan version is not recorded in the file. |
| `novel_vs_known_correlation.tsv` | 658 B | Pearson correlation of 10 candidates against five characterised finger millet drought genes (CIPK31, TAF6, PP2A, SRPRa, FPS), computed on raw StringTie coverage across 6 samples. MSTRG.31255.1: r = 0.9925 (FPS), 0.9896 (PP2A). Not superseded. |
| `synteny_3species.tsv` | 491 B | Conservation classification of 10 candidates by presence/absence of a blastn hit (E <= 1e-5) in *Sorghum bicolor*, *Oryza sativa* and *Setaria italica*. 4 Eleusine-specific, 1 Panicoideae-specific, 1 partially conserved, 4 pan-grass. **Underpowered - see the limitation in README.md.** Not superseded; no v2 equivalent was produced. |
| `top50_transcripts.fa.transdecoder.pep` | 22,438 B | TransDecoder 5.7.1 predicted peptides for the top-50 candidates (`-m 100`, `--single_best_only`). 44 of 50 yielded an ORF >= 100 aa. |

### 5.1 `results_v1/novel_genes/`

| File | Size | Description |
|---|---|---|
| `blast_results.txt` | 10,345,726 B | Raw v1 blastx output against Swiss-Prot, 51,468 hit lines. Query IDs read `transcript::<chrom>:<start>-<end>` - **this is defect 2**. Added 28 Aug 2026. |
| `novel_genes.gtf` | 3,584,456 B | The 21,864 gffcompare class-`u` transcript records. **Contains transcript records only, no exon records** - this is defect 4, the cause of the unspliced extraction. Added 28 Aug 2026 to close reproducibility gaps. |

### 5.2 `results_v1/synteny/`

| File | Size | Description |
|---|---|---|
| `vs_foxtail.txt` | 9,060 B | blastn of the top-50 transcripts against *Setaria italica*. Added 28 Aug 2026. |
| `vs_rice.txt` | 4,593 B | blastn of the top-50 transcripts against *Oryza sativa*. Added 28 Aug 2026. |
| `vs_sorghum.txt` | 7,402 B | blastn of the top-50 transcripts against *Sorghum bicolor*, E <= 1e-5, `-max_target_seqs 1`. Added 28 Aug 2026. |

### 5.3 `results_v1/transdecoder/`

| File | Size | Description |
|---|---|---|
| `top50_transcripts.fa` | 267,855 B | The 50 extracted top-candidate sequences that TransDecoder consumed. **Headers carry correct transcript IDs** - this extraction used a BED with the ID in column 4, so defect 2 did not affect it. Added 28 Aug 2026. |

### 5.4 `results_v1/final_report/`

| File | Size | Description |
|---|---|---|
| `candidate_genes_final.tsv` | 408,273 B | The 2,354-row candidate table from which the top-50 were selected. **PROVENANCE UNKNOWN - see section 8.1.** Added 28 Aug 2026. |

### 5.5 `results_v1/sequences/`

| File | Size | Description |
|---|---|---|
| `defensins.fasta` | 301 B | **Recovered from shell history** (lines 632-637). Two records: MSTRG.31255.1 (104 aa) and *Leersia perrieri* A0A0D9XDT2 (133 aa). The MSTRG.31255.1 sequence is verified byte-identical to the copy in `top50_clean.pep`. **The filename is a working hypothesis, not an annotation** - no defensin family assignment was ever made. |
| `defensins.fasta.provenance.txt` | 3,715 B | Provenance sidecar for the file above. |
| `top50_clean.pep` | 11,704 B | Byte-identical copy of a genuine project file: the exact 44-peptide input submitted to InterProScan. Produced by `stage06e_clean_peptide_fasta.py`. |
| `top50_clean.pep.provenance.txt` | 3,431 B | Provenance sidecar for the file above. |

> **Deviation from the header treatment used in `scripts/reconstructed/`.** FASTA has no
> comment syntax that modern parsers accept — a `#` or `;` preamble is read as sequence,
> or errors, in Biopython, samtools, HMMER and BLAST. Both sequence files are therefore
> held **byte-verbatim** with provenance in a same-basename `.provenance.txt` sidecar.

## 6. `results_v2/` — CORRECTED RE-ANALYSIS

| File | Size | Description |
|---|---|---|
| `README.md` | 26,853 B | Status marker: corrected re-analysis, current. v1-vs-v2 comparison table, contents, and the read-length rationale. |

### 6.1 `results_v2/de/` — differential expression

| File | Size | Description |
|---|---|---|
| `all_de_results_v2.tsv` | 15,517,049 B | **Primary DE output.** All 83,195 transcripts surviving the prefilter, with baseMean, unshrunk MLE log2FC and SE, Wald statistic, p, padj, apeglm-shrunk log2FC and SE, class-`u` flag, zero-in-all-controls flag, per-condition raw sums, and rank by padj. |
| `all_de_results_v2_paired.tsv` | 12,661,288 B | Full output of the rejected `~ plant + condition` model, retained as the record of the test. |
| `diagnostics.txt` | 1,449 B | Library sizes, detection counts, PCA coordinates, correlations between depth/detection/PC1, within- and between-group vst distances, dispersion summaries, and the detection-sensitivity audit of the drought-up novel set. |
| `drought_upregulated_all_v2.tsv` | 2,181,387 B | All 11,592 drought-upregulated transcripts (novel and reference) at padj < 0.05, log2FC >= 1.5. |
| `drought_upregulated_novel_genes_v2.tsv` | 438,752 B | **The corrected headline result: 2,422 novel class-`u` drought-upregulated transcripts.** |
| `drought_upregulated_novel_genes_v2_apeglm_threshold.tsv` | 401,734 B | The same set with the log2FC threshold applied to the apeglm-shrunk estimate instead of the MLE: 2,218 transcripts. For comparison only; not the headline figure. |
| `drought_upregulated_novel_genes_v2_paired.tsv` | 381,031 B | Drought-upregulated novel set under the rejected paired model: 2,552 transcripts, only 1,758 shared with the primary set. |
| `log2fc_old_vs_new.tsv` | 4,144,573 B | Per-transcript old and new log2FC for all 83,195 shared transcripts, with membership flags for the v1 2,354 and v2 2,422 sets. Source of the scatter in `figures_v2/`. |
| `paired_vs_unpaired.txt` | 1,342 B | Side-by-side model comparison: dispersion, tested counts, set overlap and per-candidate log2FC/padj/rank. |
| `pca_coordinates.tsv` | 915 B | PC1/PC2 per sample with library size and detected-transcript count. |
| `sample_distance_matrix.tsv` | 638 B | 6x6 Euclidean distances on vst-transformed counts. |
| `sessionInfo.txt` | 2,125 B | R session info for the primary run. |
| `sessionInfo_paired.txt` | 2,125 B | R session info for the paired-model run. |

### 6.2 `results_v2/counts/` — count matrices

| File | Size | Description |
|---|---|---|
| `featurecounts_gene.txt` | 19,613,466 B | Independent gene-level quantification: `featureCounts -p --countReadPairs -B -C -s 2 -T 4` against `merged_assembly.gtf`. Spearman rho 0.985-0.995 against the prepDE gene matrix across all six samples. |
| `featurecounts_gene.txt.summary` | 793 B | featureCounts assignment summary. 93.5-96.4% assigned per sample. |
| `gene_count_matrix_l142.csv` | 2,155,870 B | prepDE.py gene-level counts, 64,266 genes x 6 samples, 142 bp. |
| `gene_count_matrix_l151.csv` | 2,149,222 B | Gene-level equivalent of the above. |
| `novel_class_u_ids.txt` | 301,786 B | The 21,864 gffcompare class-`u` transcript IDs. |
| `sample_list.txt` | 276 B | prepDE.py input list. |
| `sample_sheet.csv` | 356 B | Sample to condition mapping with the ENA library names that corroborate it and their source. |
| `transcript_count_matrix_l142.csv` | 3,896,305 B | **The DESeq2 input.** prepDE.py transcript-level counts, 101,639 transcripts x 6 samples, at the measured mean aligned read length of 142 bp. |
| `transcript_count_matrix_l151.csv` | 3,886,140 B | Sensitivity check at 151 bp (modal untrimmed read length). Rescales all counts by a uniform 0.9405. |
| `transcripts_dropped.txt` | 804 B | The 39 transcripts StringTie `-e` failed to emit for at least one sample and which were therefore excluded. One of them, `MSTRG.24742.1`, is in the v1 2,354 set and is a technical rather than biological loss. |
| `transcripts_in_all6.txt` | 2,045,679 B | The 101,639 transcripts quantified in all six samples - the harmonised set prepDE.py was run on. |

### 6.3 `results_v2/annotation/` — corrected Swiss-Prot annotation

| File | Size | Description |
|---|---|---|
| `candidate_genes_original_reannotated.tsv` | 840,589 B | The original 2,354 set re-annotated with the same corrected join, for like-for-like comparison against the 99.6% claim. |
| `candidate_genes_v2_annotated.tsv` | 783,534 B | **The corrected annotation table.** The 2,422 novel drought-up transcripts joined to their Swiss-Prot best hits on transcript ID, with both tier schemes. |
| `novel_transcripts_best_hit.tsv` | 1,394,704 B | Best Swiss-Prot hit for every one of the 21,864 novel transcripts. 6,106 (27.9%) have a hit at E <= 1e-5. |
| `summary.json` | 987 B | Machine-readable counts and tier distributions for both sets. |

### 6.4 `results_v2/blast/` — re-run BLASTx

| File | Size | Description |
|---|---|---|
| `blast_results_v2.txt` | 10,489,491 B | Re-run blastx output, 51,468 hit lines, query IDs carrying real transcript IDs. Columns 2-7 are byte-identical to the v1 output (md5 `715cfd1610884697656649b5d487270e` for both), proving the original search was correct and only the join was broken. |
| `novel_transcripts.bed` | 1,011,914 B | The 21,864 intervals with transcript IDs in column 4, used to re-extract sequences with correct FASTA headers. |
| `run_blastx_v2.sh` | 2,233 B | The re-run script, documenting the defect it corrects and carrying the exact blastx parameters (taken verbatim from `config.yaml`). |

> **`novel_transcripts_named.fa` (72 MB) is deliberately omitted** and is regenerable.
> Rebuild it with the command recorded in `run_blastx_v2.sh`:
> ```
> bedtools getfasta -fi <genome.fa> -bed results_v2/blast/novel_transcripts.bed \
>     -fo novel_transcripts_named.fa -split -name
> ```
> using `results_v1/novel_genes/novel_genes.gtf` as the source of the intervals (already
> converted in the deposited BED) and GCA_032690845.1 as the reference. The sequences are
> byte-identical to the v1 extraction; only the FASTA headers differ.

## 7. `figures_v2/` — diagnostic figures

All ten are produced by `scripts/de_analysis_v2.R` and `scripts/de_analysis_v2_paired.R`
and are **reproducible from deposited inputs**.

| File | Size | |
|---|---|---|
| `detection_vs_depth.png` | 53,580 B | Transcripts detected against library size. Not a manuscript figure. |
| `dispersion_plot.png` | 182,355 B | **Manuscript Figure 1.** DESeq2 dispersion estimates, unpaired `~ condition` model. |
| `dispersion_plot_paired.png` | 189,366 B | Dispersion estimates from the rejected paired model. Not a manuscript figure. |
| `log2fc_old_vs_new.png` | 185,549 B | **Manuscript Figure 6.** Old versus corrected log2FC, 83,195 shared transcripts. |
| `ma_plot_apeglm.png` | 99,483 B | MA plot on apeglm-shrunk estimates. Not a manuscript figure. |
| `ma_plot_unshrunk.png` | 122,595 B | MA plot on the unshrunk MLE. Not a manuscript figure. |
| `pc1_vs_library_size.png` | 47,624 B | **Manuscript Figure 4.** PC1 against library size. |
| `pca.png` | 47,666 B | **Manuscript Figure 3.** PCA of vst counts, unpaired model. |
| `pca_paired.png` | 47,230 B | PCA from the rejected paired model. Not a manuscript figure. |
| `sample_distance_heatmap.png` | 44,140 B | **Manuscript Figure 5.** Sample-to-sample vst distances. |
| `volcano_plot.png` | 175,638 B | **Manuscript Figure 2.** Volcano plot, unshrunk MLE, 76,917 tested transcripts, with the 2,422 drought-upregulated novel transcripts highlighted and the 1,278 zero-control (lower-bound) subset shown separately. Written by `scripts/volcano_plot_v2.R`. |

> **`figures/` was WITHDRAWN on 28 August 2026.** It held six ChimeraX renders
> (`image1`–`image6.png`) whose subject could not be established and which no deposited
> script can regenerate: `analyze_structures.cxc` cannot run as written, and it never
> opens the lead candidate. Publishing six unattributable images alongside a corrected
> analysis would have been worse than publishing none. The originals are unaffected and
> remain outside this package. See `docs/VERIFICATION.md` §1.4.

## 8. `logs/`

| File | Size | |
|---|---|---|
| `blastx_v2.log` | 1,171 B |  |
| `de_analysis_v2.log` | 2,977 B |  |
| `de_analysis_v2_paired.log` | 2,041 B |  |
| `featurecounts.log` | 7,012 B |  |
| `rebuild_annotation_v2.log` | 1,461 B |  |

The 0-byte `extract_sequences_v2.log` was omitted rather than deposited empty — bedtools
emitted no stderr during the re-extraction.

## 9. `structures/` — ColabFold / AlphaFold2 models

Recovered from `/mnt/d/Downloads D/`. All files are byte-identical copies of the ColabFold
output. One subdirectory per candidate.

| Directory | Files | Length | Mean pLDDT | pTM | MSA depth | rank_001 model | Size |
|---|---|---|---|---|---|---|---|
| `MSTRG_31255_1/` | 21 | 104 aa | **59.95** | 0.390 | **34** | `model_4` | 1.5 MB |
| `MSTRG_45757_2/` | 20 | 197 aa | **46.51** | 0.220 | **2** | `model_1` | 2.9 MB |
| `MSTRG_45758_1/` | 20 | 526 aa | **83.82** | 0.590 | **17,808** | `model_3` | 22.7 MB |
| `MSTRG_4687_1/` | 20 | 342 aa | **86.20** | 0.440 | **14,714** | `model_5` | 12.2 MB |
| `MSTRG_6647_1/` | 20 | 421 aa | **76.59** | 0.770 | **334** | `model_3` | 8.5 MB |

All metrics above are **recomputed from the deposited `scores_rank_001*.json` and `.a3m`**,
not carried over.

Each directory holds: 1 relaxed rank_001 PDB · 5 unrelaxed PDBs · 5 `scores_rank_*.json` ·
1 `predicted_aligned_error_v1.json` · 1 `.a3m` MSA · 1 query `.csv` · `config.json` ·
`log.txt` · `cite.bibtex` · 3 PNGs. `MSTRG_31255_1/` additionally holds
`MSA_composition.tsv`.

**The query `.csv` files were added on 28 August 2026.** Each holds the exact `id,sequence`
pair submitted to ColabFold, so every prediction is re-submittable with identical
parameters.

### 9.1 Run parameters (`config.json`, identical across all five)

**ColabFold 1.6.1**, commit `9712f2ff262d3977d571919317e06cc96c29cd95` · `alphafold2_ptm` ·
MSA mode `mmseqs2_uniref_env` · **no templates** · 5 models, **3 recycles**, 1 seed
(`random_seed 0`) · ranked by pLDDT · 1 × Amber relaxation (200 iterations, tolerance 2.39,
stiffness 10.0) · `max_seq` 512 / `max_extra_seq` 5120 · `pair_mode: unpaired_paired` ·
host `https://api.colabfold.com`.

**The rank_001 model number differs per candidate** — do not assume `model_1`. This is
what `analyze_structures.cxc` got wrong.

### 9.2 `MSTRG_31255_1/MSA_composition.tsv`

| File | Size | Description |
|---|---|---|
| `MSA_composition.tsv` | 4,442 B | Per-row composition of the MSTRG.31255.1 MSA: accession, source database, organism, subfamily, product name, target length, identity, E-value, duplicate grouping. Added 28 Aug 2026 so the MSA claims in README.md are checkable without re-querying UniProt. |

Added 28 August 2026. One row per alignment row: accession, source database, organism,
subfamily, product name, target length, sequence identity, E-value and duplicate grouping.
It exists so the MSA claims in `README.md` can be checked without re-querying UniProt.

Recomputed from the deposited `.a3m`: **32 aligned rows representing 27 distinct
sequences** (5 exact-duplicate pairs). 27 rows carry UniProt/UniRef accessions spanning
**seven genera and twelve species in three subfamilies**; 5 are metagenomic or
environmental with no taxonomy. Only 2 rows carry a functional product name; 23 are
"Uncharacterized protein"; 2 are obsolete entries. **Every UniProt-derived row is
unreviewed TrEMBL and none is in Swiss-Prot** — which is why Swiss-Prot BLASTx returns
nothing for this transcript.

Two species assignments (`A0A368Q1M5` → *Setaria italica*, `A0A0A9C887` → *Arundo donax*)
were recovered from UniSave entry-name history because those accessions have since been
deleted from UniProt; their product names are not retrievable.

### 9.3 Reading the confidence numbers

- **MSTRG.31255.1** (lead candidate): mean pLDDT **59.95**, pTM **0.390**, **MSA depth 34**.
  Per-residue: signal peptide 1–28 mean 48.5; residues 29–65 in the 36–52 band; **only
  residues 66–104 are confident (~80–87)**. 37/104 residues ≥ 70, **41/104 below 50**. Far
  too weak to assign a fold or repeat architecture. It supports a disulfide-stabilised
  C-terminal cysteine module and nothing more.
- **MSTRG.45757.2**: mean pLDDT **46.51**, pTM **0.22**, **MSA of just 2 sequences** —
  effectively single-sequence prediction, unreliable throughout. Consistent with its lack
  of any Foldseek hit and with 42.4% of its ORF deriving from intronic sequence.
- The two retrotransposon candidates have **MSA depths of 14,714 and 17,808** and
  correspondingly high pLDDT (86.2, 83.8). Deep MSAs are expected for mobile elements,
  which are present in thousands of genomic copies — this independently corroborates the
  retrotransposon assignment made by InterProScan, Foldseek and BLASTx.

### 9.4 Relocation history — why the scripts' paths do not resolve

The Foldseek scripts and `analyze_structures.cxc` referenced these folders under
`C:\Users\Joshua\Downloads\`. **Those paths are correct for April 2026 and stale
today.** The folders were **moved** to `D:\Downloads D\` on **5 August 2026**; nothing was
deleted, and no project file appears in either Windows Recycle Bin. The Foldseek scripts
have been sanitised to read `$FM_STRUCTURES` and now default to `./structures`.

---

## 10. `docs/` — documentation

| File | Size | Description |
|---|---|---|
| `DE_COMPARISON.md` | 19,983 B | Full reconciliation of the original analysis against the corrected re-analysis: counts, retained/lost/gained, tier distributions, per-candidate comparison, top-50 membership, log2FC correlation, model specification, limitations. |
| `MANIFEST.md` | 44,924 B | This file. Regenerated from the package as it stands; every size and count is derived, not typed. |
| `MANUSCRIPT_CORRECTIONS.md` | 33,153 B | Every claim in the manuscript draft affected by the re-analysis, classified A (numeric swap), B (rewritten argument), C (conclusion changes), D (confirmed correct), E (not fixable). Carries a dated correction notice for three MSA figures that were wrong in its first version. |
| `VERIFICATION.md` | 40,170 B | Pre-publication audit of this package (first pass 28 Aug 2026) plus the second verification appended after rectification. File integrity, format validation, byte-identity, number recomputation, script review, privacy scan, reproducibility gaps. |

---

## 10a. `manuscript/` — the preprint and its archive

Added 6 September 2026, after the rest of this package had been numbered. It is
sectioned `10a` rather than `11` **so that no existing section number moves**: the
cross-references to §11–§14 in `docs/VERIFICATION.md` and elsewhere were written against
the numbering below and remain valid.

All seven files were copied in from the working manuscript directory and are
**byte-identical to their sources** — verified by `cmp` at the time of the copy. The
package copy is now the canonical one; the outside working copy is a duplicate and will
drift if it is edited.

| File | Size | Description |
|---|---|---|
| `finger_millet_preprint_v2.md` | 41,782 B | **The live draft, and the only current manuscript file in this package.** Reports the corrected re-analysis: 21,864 class-`u` transcripts, 2,422 drought-upregulated, 1,532 (63.3%) with no Swiss-Prot homolog, 1,278 zero in all three controls. Carries a dated revision note retracting the 99.6% figure as a software defect (§3.4, §4.2), a limitations section (§4.6) stating the plant-age confound, the treatment of the six libraries as independent samples, and the biological—not technical—nature of the replication. Six numbered figure legends, each naming a file in `figures_v2/`. |

### 10a.1 `manuscript/archive/`

**Nothing in this directory is current, in any format.** It holds the two unmodified 17
April 2026 drafts, the pandoc HTML rendering of each, and the corrected v1 draft that the
live v2 draft supersedes. The four 17 April files still state the withdrawn **99.6%**
figure and are retained only so the corrections can be audited against the text they
corrected.

| File | Size | Description |
|---|---|---|
| `README.md` | 26,853 B | States that `../finger_millet_preprint_v2.md` is the live draft, tabulates what each archived file is, and records that the two HTML renderings were moved out of the live directory on 5 Sep 2026 because they sat there under the live file names while containing the uncorrected text. Its reference to "the accompanying Zenodo deposit" now means the package it sits in; `docs/MANUSCRIPT_CORRECTIONS.md` resolves from here as `../../docs/`. |
| `finger_millet_preprint.md` | 33,426 B | The v1 draft, corrected in place during the August 2026 audit and again on 5 Sep 2026. **Superseded** by the live v2 draft, which it duplicates with less detail. Retained so that no uncorrected version of the manuscript exists on disk outside the four dated originals below. Not a draft under development. |
| `finger_millet_preprint_ORIGINAL_17Apr2026.md` | 28,951 B | Unmodified 17 April 2026 text of the v1 draft. **Never edited.** Retains its April 2026 mtime and is byte-identical to the pre-audit copy. Contains the 99.6% claim and every other subsequently revised statement. |
| `finger_millet_preprint_ORIGINAL_17Apr2026.html` | 659,111 B | Pandoc rendering of the file above, produced 17 April 2026 and never regenerated. **Stale; must not be circulated.** Until 5 Sep 2026 it sat under the live name `finger_millet_preprint.html`. |
| `finger_millet_preprint_v2_ORIGINAL_17Apr2026.md` | 25,714 B | Unmodified 17 April 2026 text of the v2 draft. **Never edited.** Retains its April 2026 mtime and is byte-identical to the pre-audit copy. |
| `finger_millet_preprint_v2_ORIGINAL_17Apr2026.html` | 655,596 B | Pandoc rendering of the file above, produced 17 April 2026 and never regenerated. **Stale; must not be circulated.** Until 5 Sep 2026 it sat under the live name `finger_millet_preprint_v2.html`, so opening the apparently-current HTML gave the uncorrected paper. |

Every correction applied to the 17 April text is itemised in
`docs/MANUSCRIPT_CORRECTIONS.md`; the underlying numeric reconciliation is in
`docs/DE_COMPARISON.md`.

---

## 11. Modifications made to deposited copies

Every other file in this package is a byte-identical copy of its source. **Three files are
not**, and each is documented here.

**11.1 `workflow/config.yaml` — reference URLs corrected.** Both `genome_url` and
`annotation_url` pointed at `GCA_002477235.1_Ecoracana_ML365_v1.0`, which was **not** the
assembly used. They now point at `GCA_032690845.1_Eleusine_coracana_v1.0`. Without this,
anyone re-running the workflow would silently download the wrong genome. Evidence, from
`data/ref/annotation.gff3` lines 4–5:
```
#!genome-build Eleusine_coracana_v1.0
#!genome-build-accession NCBI_Assembly:GCA_032690845.1
```
A comment was also added at `log2fc_cutoff` recording that the applied threshold is **1.5,
not 2.0**, that `de_analysis.R` filters one-sided on `log2FoldChange >= lfc_cutoff`, that
the minimum log2FoldChange among the 2,354 v1 transcripts is 1.5009, and that at
log2FC > 2 the v1 count would be 2,081. The value itself is unchanged.

> **The corrected URLs have not been fetched or validated** — confirm both resolve on the
> NCBI FTP server before deposition.

**11.2 `scripts/analyze_structures.cxc` — 53-line deposition header prepended**
(28 Aug 2026) stating that the script does not run as written and is not the record of the
prediction settings. **The 5,709-byte body beneath the header is byte-identical to the
original** — verified.

**11.3 Sanitisation for deposition** (28 Aug 2026). Machine-specific values were removed
from maintained source files and replaced with documented environment variables:

| File | Change |
|---|---|
| `workflow/Snakefile` | Hard-coded `PATH` prepend under the author's home directory replaced with opt-in `$FM_ENV_BIN`; adapter search now uses `$CONDA_PREFIX`; username removed from `tool_versions.txt` output (now `hostname`) |
| `workflow/setup.sh` | `PROJECT` now `${FM_PROJECT:-<script dir>}`; conda located via `${CONDA_SH:-$(conda info --base)/...}` |
| `workflow/config.yaml` | Header and two machine-specific comments |
| `scripts/de_analysis.R`, `scripts/merge_results.py` | Username removed from headers and from run-time log output |
| `scripts/run_foldseek*.sh` | Absolute Windows paths replaced with `$FM_STRUCTURES` / `$FM_FOLDSEEK_OUT` |
| `scripts/de_analysis_v2*.R`, `scripts/rebuild_annotation_v2.py`, `results_v2/blast/run_blastx_v2.sh` | Project root now read from `$FM_ROOT`, default `.` |

All were re-verified to parse after editing. **`scripts/reconstructed/` was deliberately
NOT sanitised** — see §4 and `scripts/reconstructed/README.md`.

`scripts/analyze_structures.cxc` retains its absolute `C:\Users\Joshua\` paths in the
body. They are the documentary evidence for §8.4's relocation note, and the prepended
header explains them. This is a deliberate retention.

---
## 12. Reproducibility status

**Fully regenerable from deposited files:**

| Output | Producing script |
|---|---|
| `results_v2/de/*` | `scripts/de_analysis_v2.R` |
| `results_v2/de/*_paired*` | `scripts/de_analysis_v2_paired.R` |
| `results_v2/annotation/*` | `scripts/rebuild_annotation_v2.py` |
| `figures_v2/*` | the two v2 R scripts, except `volcano_plot.png` |
| `figures_v2/volcano_plot.png` | `scripts/volcano_plot_v2.R` |
| `results_v1/synteny_3species.tsv` | `stage11d_classify_three_species.py` |
| `results_v1/sequences/top50_clean.pep` | `stage06e_clean_peptide_fasta.py` |
| `top50_ids.txt` → unblocks `stage06b/c/d`, `stage08a` | `stage06a_select_top50_by_padj.py` |
| `synteny_summary.tsv` → unblocks `stage11c` | `stage11b_parse_sorghum_blast.py` |

**Reproduces but does not re-derive:** `results_v1/novel_vs_known_correlation.tsv` —
`stage10d` hard-codes its expression matrices as literals.

**Cannot be regenerated from this package:**

- `results_v1/all_de_results.tsv` and `drought_upregulated_novel_genes.tsv`,
  `results_v2/counts/*`, and `stage10a`/`10b`/`10c` — all need
  `results/counts/*_counts.gtf` (~600 MB), too large to deposit. The Snakefile rule that
  produces it is included and its inputs are the public reads and the public genome.
- `results_v1/iprscan5-*.tsv` — EBI web service, no local script, version not recorded.
- `structures/*` — ColabFold web service, but with the query `.csv` files now deposited
  alongside `config.json`, every prediction is re-submittable with identical parameters.
- **`results_v1/final_report/candidate_genes_final.tsv` — provenance unknown.** No
  Snakefile rule and no shell-history line creates it, and it contains four tier strings
  where `merge_results.py` can emit only three. **This is a known break in the chain of
  custody, not an oversight**, and it affects all downstream candidate selection. The file
  is deposited; its generating code is not recoverable.

**The paired model was tested and rejected.** `~ plant + condition`, with pairing inferred
from the ENA library-name suffixes, *increased* dispersion (asymptDisp 0.786 → 0.880;
median 0.913 → 1.497) and cost 8,239 transcripts their testability. All six possible
control↔drought pairings absorb 49.1–51.0% of within-condition variance —
indistinguishable — and the suffix-inferred pairing is not even the best. The suffixes do
not encode plant identity.

Nor can the pairing be established from the surviving experimental records. Whether the
control and drought libraries derive from the same individual plants cannot be
determined: the original laboratory notes no longer exist, and although a surviving
sample-name table pairs matched replicate numbers with a `_D` suffix for the drought
samples — suggesting that a correspondence was intended — no documentation confirms that
the same individuals were sampled twice. The pairing is therefore not sufficiently
documented to justify treating the design as confirmed repeated measures. `~ condition`,
which treats the six libraries as independent samples, is the appropriate choice and
remains the primary analysis.

Replication within each condition **is** biological: the three libraries per group were
prepared from separate plants, though the archive metadata does not record this (all 18
runs share one BioSample). The plants derive from a highly inbred seed stock obtained from
GKVK Bangalore and originally from ICRISAT, so they should be genetically very similar,
which makes the extreme between-replicate dispersion (asymptDisp 0.786) more notable
rather than less: it reflects genuine between-plant variation in material that was not
collected under a controlled experimental protocol. No time-matched well-watered control
was sampled at day seven, and detailed environmental information for the growth period —
watering amount and timing, temperature — was not retained, so treatment remains
confounded with plant age.

### 12.1 To run any deposited script

```bash
ln -s results_v1 results     # scripts reference results/…; the package stores results_v1/…
export FM_ROOT="$PWD"        # v2 scripts read this; default is "."
```

`stage06d` and `stage06e` were run from inside `results/transdecoder/`, not the project
root.

---

## 13. Items deliberately omitted, with reasons

**13.1 Not deposited.** `results/coexpression/correlation_matrix.tsv` and
`expression_matrix.tsv`, `results/promoter_analysis/abre_results.tsv`,
`results/novel_genes/gffcmp.stats`, the Foldseek result directories, and
`results/counts/*_counts.gtf` (size). The promoter and co-expression outputs are
regenerable from the deposited scripts given the count GTFs and the reference.

**13.2 No GO enrichment output.** `gProfiler_athaliana_4-18-2026_10-49-33 PM__intersections.csv`
is excluded because it does not support a drought-enrichment claim: organism
*Arabidopsis thaliana*, 9 genes mapped of 29 submitted, and **no drought-, ABA-, ROS- or
osmotic-stress-related term among the 28 returned**.

**13.3 No LaTeX source or bibliography.** The manuscript itself **is** deposited, as
markdown, in `manuscript/` — see §10a. What is missing is its typesetting source:
`paper/main.tex` is an empty LaTeX skeleton and no `references.bib` exists anywhere. The source project is **not a git repository**, so no
commit history accompanies this deposit. The manuscript-level consequences of the
re-analysis are in `docs/MANUSCRIPT_CORRECTIONS.md`.

**13.4 `figures/` withdrawn** — see §7.

**13.5 `novel_transcripts_named.fa`** — 72 MB, regenerable; see §6.4.

---

## 14. Integrity

- Every file in this package is a byte-identical copy of its source **except** the three
  documented in §9.
- **No file in `/mnt/d/finger_millet_project/` was created, modified, moved or deleted**
  at any point during the audit, the re-analysis or the rectification.
- Structure metrics, MSA composition, tier distributions, row counts and all headline
  figures in `README.md` and `CITATION.cff` are **recomputed from deposited files**, not
  carried over. See `docs/VERIFICATION.md` §2 for the full second verification.

**Line endings.** Four TSVs use CRLF rather than LF:
`results_v1/final_report/candidate_genes_final.tsv` (inherited from its unknown origin)
and the three tables in `results_v2/annotation/`, because Python's `csv` module writes
`
` by default. This is RFC 4180-compliant and parses correctly in R's `read.delim`,
pandas, `awk` and `cut -f` on any field but the last. **They have deliberately not been
normalised**, because doing so would break byte-identity with their sources, which is
worth more than cosmetic consistency. On Linux, strip with `tr -d '
'` if the trailing
carriage return in the final column is inconvenient.

**Reference URLs validated 28 August 2026.** All three URLs in `workflow/config.yaml`
return HTTP 200: the genome (331.1 MB), the annotation (9.1 MB) and Swiss-Prot (89.4 MB).
The caveat in §11.1 that they had never been fetched is now discharged.

**Total: 217 files across 25 directories, 164,152,862 B (156.5 MB).**
