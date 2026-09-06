# DE_COMPARISON.md — original analysis vs re-analysis with genuine counts

**Date:** 26 August 2026
**Original:** `results/de_analysis/`, `results/final_report/candidate_genes_final.tsv` (13–14 April 2026)
**Re-analysis:** `results_v2/de/` (this document)

Nothing under `results/` was modified. The original remains the historical record.

---

## 0. Summary

| | original | re-analysis |
|---|---|---|
| DESeq2 input | `round(cov × 100)` — StringTie per-base coverage × 100 | `prepDE.py` counts from the same `stringtie -e -B` GTFs, read length 142 bp |
| Transcripts tested | 88,336 | 76,917 |
| **Novel drought-up (class-u, padj < 0.05, log2FC ≥ 1.5)** | **2,354** | **2,422** |
| lfcShrink | none | `apeglm` (reported alongside, not used for thresholding) |
| Design | `~ condition` | `~ condition` (paired model tested and rejected, §8) |

**The headline count barely moves: 2,354 → 2,422, a 2.9% increase.** Effect sizes for well-measured transcripts are essentially unchanged. What the correct input destroys is precision — the extreme p-values — and it exposes a separate, more serious error in the annotation join that has nothing to do with counting (§4).

---

## 1. Why the count is stable

The relationship between the two inputs is, per transcript,

```
old_count  =  round(cov × 100)
new_count  ≈  cov × length / 142
```

so `old ≈ new × 14200/length`. That factor is **constant within a transcript**, and therefore cancels in a drought-vs-control ratio. Size factors confirm it — recomputing them on a reconstructed `cov × 100` matrix from the same GTFs gives values within 0.8% of the prepDE ones:

| Sample | size factor, cov×100 | size factor, prepDE | ratio |
|---|---|---|---|
| DRR095904 | 0.5732 | 0.5737 | 0.999 |
| DRR095905 | 0.7422 | 0.7419 | 1.000 |
| DRR095906 | 0.7364 | 0.7349 | 1.002 |
| DRR095907 | 2.0156 | 1.9988 | 1.008 |
| DRR095908 | 1.7674 | 1.7538 | 1.008 |
| DRR095909 | 1.1365 | 1.1309 | 1.005 |

Implied log2FC bias from normalisation alone: **−0.009**. Negligible.

So the coverage substitution was not a systematic distortion of fold change. Its damage is concentrated elsewhere: in the *variance* structure, which is what sets the p-values, and in transcripts with zero control counts (§7).

---

## 2. Retained, lost, gained

| | count | % of original 2,354 |
|---|---|---|
| **Retained** (in both) | **2,125** | 90.3% |
| **Lost** (original only) | **229** | 9.7% |
| **Gained** (re-analysis only) | **297** | — |

Why the 229 were lost:

| reason | n |
|---|---|
| padj ≥ 0.05 in re-analysis | 175 |
| padj became NA (independent filtering / outlier) | 40 |
| dropped by prefilter `rowSums < 10` | 6 |
| log2FC fell below 1.5 | 5 |
| failed both thresholds | 2 |
| **technical: not quantified in all six samples** | **1** (`MSTRG.24742.1`) |

`MSTRG.24742.1` is not a biological loss. It is one of the 39 transcripts StringTie `-e` failed to emit for every sample (Phase B §B2), so it was excluded from the harmonised matrix before DESeq2 ran. It should be counted as "not assessable," not "not significant."

The dominant reason — 175 of 229 — is simply that the p-value no longer clears 0.05 once the variance is estimated from real counts. That is the expected consequence of the fix, not a surprise.

---

## 3. The eight named candidates

Ranks below are **within the novel drought-up set**, which is the like-for-like comparison against the original (whose 2,354 rows were ranked among themselves). Global rank across all 83,195 tested transcripts is given separately.

| Transcript | old log2FC | old padj | old rank | new log2FC | apeglm | new padj | **new rank** | global rank |
|---|---|---|---|---|---|---|---|---|
| **MSTRG.31255.1** | 4.456 | 8.07e-57 | 3 | **4.434** | 4.382 | **1.56e-32** | **4** | 312 |
| MSTRG.20738.1 | 2.587 | 6.73e-66 | 1 | 2.587 | 2.565 | 1.37e-37 | 3 | 211 |
| MSTRG.6647.1 | 3.374 | 8.71e-58 | 2 | 3.355 | 3.324 | 1.04e-37 | 2 | 209 |
| MSTRG.45758.1 | 3.143 | 2.83e-52 | 4 | 3.143 | 3.114 | 9.25e-38 | **1** | 208 |
| MSTRG.4687.1 | 3.496 | 7.38e-36 | 8 | 3.499 | 3.455 | 2.04e-28 | 6 | 411 |
| MSTRG.45757.2 | 2.110 | 3.83e-41 | 7 | 2.118 | 2.091 | 6.66e-23 | 11 | 636 |
| MSTRG.21998.1 | 2.979 | 1.62e-23 | 38 | 2.981 | 2.927 | 3.60e-19 | 19 | 896 |
| MSTRG.37761.2 | 9.509 | 4.97e-07 | 1124 | **6.448** | 6.507 | **2.49e-04** | 1191 | 11301 |

**All eight remain significant. Seven of the eight have log2FC unchanged to within 0.6%, and their ordering is nearly preserved** — the top four are still the top four, merely reshuffled. `MSTRG.31255.1` moves 3 → 4. apeglm shrinkage barely touches them (largest shift 1.2%), which confirms they are high-count, well-estimated transcripts rather than low-count artefacts.

**One candidate changes materially: `MSTRG.37761.2`.** log2FC falls from 9.509 to 6.448, so the preprints' *"approximately 730-fold"* becomes **~87-fold** — wrong by a factor of eight. padj moves from 4.97e-07 to 2.49e-04. Its baseMean is 11.9, it has zero counts in all three control libraries, and it is supported by 109 fragments in total. This is the drafts' **Priority 2** candidate; it is still significant but should not carry that weight.

### The six "lncRNA" candidates

| Transcript | old rank | new rank |
|---|---|---|
| MSTRG.14681.1 | 6 | 9 |
| MSTRG.46022.1 | 15 | 17 |
| MSTRG.14947.1 | 18 | 13 |
| MSTRG.45098.4 | 29 | 51 |
| MSTRG.6129.1 | 37 | 96 |
| MSTRG.26934.1 | 41 | 204 |

All six remain significant. The last three fall well outside the top 50, so the claim that the no-ORF set sits among the very top candidates weakens.

---

## 4. Tier distribution — the annotation join was broken

**The tier assignment can be reproduced, and doing so uncovers an error larger than the counting one.**

`merge_results.py` joins the DE table to `results/novel_genes/blast_results.txt` on a column both call `transcript_id`. But the BLAST query IDs are not transcript IDs:

```
transcript::CM064417.1:327051-329510	sp|Q9FNJ9|CA1P_ARATH	55.000	40	8.92e-17	47.8	...
```

`bedtools getfasta -name` was given a GTF, so it wrote the **feature type** (`transcript`) plus coordinates as the FASTA header, for all 21,864 records. The DE table is keyed on `MSTRG.x.y`. **The two key spaces are disjoint — the merge could never match anything.** Because it is a `how="left"` merge, every row silently received `annotation = NaN`, and `tier()` returned "no homolog" for all of them.

This is confirmed on disk by the three surviving report versions:

| File | mtime | annotated rows |
|---|---|---|
| `candidate_genes_annotated.tsv` (Snakemake output) | 14 Apr 21:31 | **0** |
| `candidate_genes_annotated_v2.tsv` | 14 Apr 22:06 | 10 |
| `candidate_genes_final.tsv` | 14 Apr 22:27 | 10 |

The pipeline produced **zero** annotations. The 10 in the final table were added by the manually-modified script between 21:31 and 22:27 — the script the audit could not recover.

BLASTx was re-run (28 Aug 2026) against the same database with the same parameters, from a re-extraction whose headers carry the transcript ID. **The BLAST output is provably identical to the original** — 51,468 hit lines in both, and columns 2–7 are byte-identical (md5 `715cfd1610884697656649b5d487270e` for both files). Only the query names differ. This proves the original BLASTx ran correctly and its entire result was discarded by the key mismatch.

**6,106 of the 21,864 novel transcripts (27.9%) have a Swiss-Prot hit at E ≤ 1e-5.**

| | annotated | no hit | % no hit |
|---|---|---|---|
| Original 2,354, **as filed** | 10 | 2,344 | **99.6%** |
| Original 2,354, **clean join** | **860** | 1,494 | **63.5%** |
| Re-analysis 2,422, clean join | **890** | 1,532 | **63.3%** |

**The "99.6% of novel drought-upregulated transcripts had no significant homology" claim is not a finding. It is a bug.** The true figure is **63.5%**. Both preprint drafts build their central argument on 99.6%, in the abstract, §3.4, §4.2 and the Conclusions. That argument does not survive.

### Tier distributions

Using `merge_results.py`'s own substring matching:

| Tier | original, as filed | original, clean join | re-analysis |
|---|---|---|---|
| Tier 1 — no homolog, highly induced | 1,802 | 1,168 | 1,184 |
| Tier 1 — no homolog | 542 | 326 | 348 |
| Tier 2 — stress-related homolog | **3** | **121** | **119** |
| Tier 3 — other homolog | **7** | **739** | **771** |
| **Total** | 2,354 | 2,354 | 2,422 |

### A second bug: STRESS_WORDS matches substrings, not words

`merge_results.py` tests `w.lower() in ann.lower()`. Two of its keywords are three-letter strings that occur inside common words:

- **`ABA` matches `tabacum`** — every *Nicotiana tabacum* hit is scored stress-related. 36 transcripts.
- **`LEA` matches `nuclear` and `nuclease`** — 30 transcripts.

**58% of Tier 2 (69 of 119) has no word-boundary match at all.** The single most frequent Tier 2 annotation is `sp|P10978|POLX_TOBAC Retrovirus-related Pol polyprotein from transposon TNT 1-94` — a tobacco retrotransposon, classified "stress-related" because *tabacum* contains *aba*.

With word-boundary matching:

| Tier | original 2,354 | re-analysis 2,422 |
|---|---|---|
| Tier 1 — no homolog, highly induced | 1,168 | 1,184 |
| Tier 1 — no homolog | 326 | 348 |
| **Tier 2 — stress-related homolog** | **56** | **50** |
| Tier 3 — other homolog | 804 | 840 |

Even those 50 are 46 × `kinase`, 2 × `stress`, 2 × `peroxidase`. "Stress-related" is, in practice, "contains a kinase." **Tier 2 should be rebuilt by curation, not keyword matching, before publication.**

Note `MSTRG.37761.2` (MDAR3) is Tier 3 under both keyword schemes — "Monodehydroascorbate reductase" contains no keyword. `candidate_genes_final.tsv` files it as Tier 2, which no version of `tier()` produces. Further evidence the 10 filed annotations were hand-curated.

### Mobile elements

**203 of the 2,422 (8.4%) hit a transposon, retrovirus-related polyprotein, integrase or reverse transcriptase.** The most frequent Swiss-Prot subjects across the whole annotated set are mobile-element proteins: `POLX_TOBAC` (35), `YG31B_YEAST` (26), `TF107_SCHPM` (23), `POLR1_ARATH` (22), `LIN1_NYCCO` (19). This independently confirms, by a third method, that a substantial slice of the "novel drought-responsive gene catalogue" is repeat-derived.

`MSTRG.4687.1` → Transposon Tf2-6 polyprotein, E = 2.03e-106. `MSTRG.45758.1` → Transposon Tf1-107 polyprotein, E = 4.46e-72. Both were filed as "Tier 1 — no homolog."

### Correction to the coordinate-join estimate

The Phase D figure of 71.5% no-homology, obtained by joining on genomic coordinates, was **too high by 8 percentage points** — it found 672 hits where the clean join finds 860. Coordinate collisions (21,864 transcripts on 19,590 intervals) lost assignments. **The clean transcript-ID join supersedes it.** The direction and magnitude of the original error were right; the exact figure was not.

---

## 5. Top 50 by padj

**33 of 50 shared (66%). 17 dropped out, 17 entered.**

Dropped out: `MSTRG.36758.1`, `MSTRG.43537.1`, `MSTRG.45098.4`, `MSTRG.42967.1`, `MSTRG.35163.1`, `MSTRG.42966.1`, `MSTRG.6129.1`, `MSTRG.11862.1`, `MSTRG.25101.1`, `MSTRG.26934.1`, `MSTRG.38836.1`, `MSTRG.40256.1`, `MSTRG.9649.1`, `MSTRG.21211.2`, `MSTRG.5080.1`, `MSTRG.16826.3`, `MSTRG.44482.2`

Entered: `MSTRG.31491.1`, `MSTRG.34757.1`, `MSTRG.1457.1`, `MSTRG.38687.3`, `MSTRG.16254.1`, `MSTRG.9600.1`, `MSTRG.15372.6`, `MSTRG.25195.1`, `MSTRG.12928.4`, `MSTRG.37296.1`, `MSTRG.23748.1`, `MSTRG.41023.3`, `MSTRG.45630.4`, `MSTRG.28976.3`, `MSTRG.24033.4`, `MSTRG.37504.6`, `MSTRG.31435.1`

`MSTRG.36758.1` matters beyond the list: it is the transcript whose reclassification from Eleusine-specific to Panicoideae-specific resolved the 5-vs-4 candidate-count discrepancy (audit D1). It is no longer a top-50 candidate at all.

The 17 that left were selected on inflated precision; the 17 that entered were previously masked by it. Any downstream work keyed to "the top 50" — the TransDecoder run, the InterProScan submission, the three-species synteny screen — was performed on a list that is now one-third different.

---

## 6. log2FC correlation, old vs new

Across all **83,195** shared transcripts:

- **Pearson r = 0.8884**
- **Spearman rho = 0.9986**

Restricted to the 2,125 retained novel drought-up transcripts:

- Pearson r = 0.9241, Spearman rho = 0.8862

Scatter: `results_v2/figures/log2fc_old_vs_new.png`

The near-perfect rank correlation with a lower Pearson is the signature of a monotone but non-linear relationship: the *ordering* of transcripts is almost completely preserved, while the *magnitudes* are compressed at the extremes.

---

## 7. Where the magnitudes moved, and why

Median shift (new − old) across all 83,195 shared transcripts: **+0.01** — essentially zero, as §1 predicts.

Among the 2,125 retained candidates it is **−2.04**. Splitting on control detection resolves the apparent contradiction completely:

| subset | n | median shift | Pearson r |
|---|---|---|---|
| **detected in ≥1 control library** | 854 | **−0.02** | **0.9744** |
| **zero in all three control libraries** | 1,271 | **−3.03** | 0.6162 |

For transcripts with any control signal, the old and new fold changes agree almost exactly. **The entire discrepancy lives in transcripts with zero control counts — where log2FC is not identifiable at all.** With a zero denominator DESeq2 returns a value driven by the magnitude of the numerator, and since `cov × 100` inflates counts several-fold, the original analysis produced correspondingly inflated pseudo-infinite fold changes.

Worked example, `MSTRG.24586.8` (the largest shift, −14.05):

```
prepDE counts : 0, 0, 0, 8105, 7324, 0
cov × 100     : 0, 0, 0, 15210, 13746, 0
old log2FC = 27.35        new log2FC = 13.31
```

Neither number means anything. It is not a 174-million-fold induction; it is a division by zero, and the transcript is absent from one of the three drought libraries as well.

**Consequence for the manuscript:** every fold change quoted for a transcript with no control expression is an artefact of count magnitude. The drafts' *"Expression fold changes among the top candidates ranged from 3-fold to over 22-fold"* is safe — those candidates all have control signal. *"approximately 730-fold"* for MSTRG.37761.2 is not, and neither is any figure drawn from the tail of the distribution.

---

## 8. Model specification

A paired design `~ plant + condition` was fitted and rejected. Pairing inferred from ENA library-name suffixes (`Illumina_RNA_ctl_1` ↔ `Illumina_RNA_dry_1` = plant 1, etc.) **increased** dispersion — asymptDisp 0.7858 → 0.8804, median final dispersion 0.9129 → 1.4972 — and cost 8,239 transcripts their testability. Testing all six possible control↔drought pairings showed each absorbs 49.1–51.0% of within-condition variance, statistically indistinguishable, with the suffix-inferred pairing not even the best. **The suffixes do not encode plant identity.**

Nor can the pairing be established from the surviving experimental records. Whether the control and drought libraries derive from the same individual plants cannot be determined: the original laboratory notes no longer exist, and although a surviving sample-name table pairs matched replicate numbers with a `_D` suffix for the drought samples — suggesting an intended correspondence — no documentation confirms that the same individuals were sampled twice. The pairing is therefore not sufficiently documented to justify treating the design as confirmed repeated measures, and the six libraries should be treated as independent samples. **This is what the permutation over all six pairings already showed, and what the unpaired model assumes, so no analysis changes.** `~ condition` is the appropriate choice.

---

## 9. Limitations that no re-analysis can fix

1. **Treatment is confounded with plant age.** Controls were sampled seven days before the drought samples and no time-matched well-watered control was sampled at day seven. Every "drought-responsive" transcript is equally consistent with being development-responsive over a seven-day window. Detailed environmental information for the growth period — watering amount and timing, temperature — was not retained. This is the single largest constraint on the study's central claim.
2. **Replication is biological, but is not declared in the archive.** Within each sampling group the three libraries were prepared from separate plants, so the replication is biological rather than technical. The archive metadata does not record this: all 18 runs of PRJDB5606 sit under one BioSample, `SAMD00076255`.
3. **The libraries were not generated for this experiment.** They were produced primarily to support genome annotation rather than as a designed differential-expression experiment. Study title: *"Finger millet genome assembly."* No growth protocol, drought severity, or timepoint is recorded. The plants derive from a highly inbred seed stock obtained from GKVK Bangalore and originally from ICRISAT, so the sampled individuals should be genetically very similar.
4. **Dispersion is extreme.** asymptDisp = 0.786 implies ~89% CV between replicates at high expression, 20–80× typical for controlled plant RNA-seq. The replicates are biological, not technical, so this is genuine between-plant variation in material that was not collected under a controlled experimental protocol. Genetic heterogeneity is largely excluded as an explanation, since the plants derive from highly inbred seed, which makes the magnitude more notable rather than less.
5. **Condition assignment rests on library names.** `Illumina_RNA_ctl_1-3` / `dry_1-3` corroborate `config.yaml`, but the run-accession → library-name correspondence is assumed to be in order.
6. **The 2,354/2,422 sequences are unspliced.** `novel_genes.gtf` has no exon records and the top-50 extraction ran without `-split`, so every downstream sequence carries its introns. 47 of the top 50 candidates are multi-exon. This affects the ORF predictions, the domain annotations and the synteny screen — not the DE analysis, which was computed from `merged_assembly.gtf` and is exon-aware.
7. **Detection asymmetry is real but unexplained.** Drought libraries detect 74k–79k transcripts vs 56k–62k in control. A depth-matched pair (DRR095905 at 21,011,330 vs DRR095909 at 20,994,628 — 0.08% apart) differs by 31.8% in detection, so this is *not* a sequencing-depth artefact. Whether it reflects genuine transcriptional activation under stress or a library-preparation difference between the two collection dates cannot be determined from the data.

---

## 10. Verdict

**The biology largely survives; the statistics do not.**

Survives: the novel-transcript count (21,864), the drought-up count (2,354 → 2,422, +2.9%), the effect sizes for well-measured transcripts (r = 0.97 for anything with control signal), all eight named candidates, and `MSTRG.31255.1` specifically — log2FC 4.434 vs 4.456, rank 4 vs 3 within the novel set, and confirmed by the depth-matched detection test.

Does not survive:
- **the 99.6% no-homolog claim** — a broken join; the real figure is **63.5%**, and Tier 2 is 56 transcripts (word-boundary matching), not 3;
- **8.4% of the catalogue is mobile-element derived**, confirmed by BLASTx, InterProScan and Foldseek independently;
- **the extreme p-values** — 6.73e-66 becomes 1.37e-37, and this is the honest number;
- **"approximately 730-fold"** for MSTRG.37761.2 — really ~87-fold;
- **one-third of the top-50 list**, on which every downstream analysis was built.

Priority for correction, in order: the annotation join (§4), the fold changes of zero-control transcripts (§7), the top-50-dependent downstream work (§5), and the age confound (§9.1) — which is the one that should change how the study is framed rather than which numbers it reports.
