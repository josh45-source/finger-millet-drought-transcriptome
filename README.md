# Finger Millet Drought Transcriptome — Reference-Guided Reanalysis

Reference-guided reanalysis of published drought-response RNA-seq in finger millet
(*Eleusine coracana* (L.) Gaertn.) against the chromosome-scale KNE 796-S genome
assembly, cataloguing transcripts absent from the current annotation.

<!-- Add the Zenodo badge here after minting the DOI -->
<!-- [![DOI](https://zenodo.org/badge/DOI/XX.XXXX/zenodo.XXXXXXX.svg)](https://doi.org/XX.XXXX/zenodo.XXXXXXX) -->

---

> ## ⚠ Read this first: the package contains two analyses
>
> **`results_v2/` is the corrected re-analysis and supersedes everything in
> `results_v1/`.** Use v2 numbers.
>
> `results_v1/` is the April 2026 analysis exactly as performed. It is retained
> unmodified so published claims can be traced to the files that produced them — and
> because four defects were found in it that a reader needs to be able to verify.
> **Its numbers should not be quoted.**
>
> The full reconciliation is in `docs/DE_COMPARISON.md`; the consequences for the
> manuscript drafts are in `docs/MANUSCRIPT_CORRECTIONS.md`; the pre-publication audit
> of this package is in `docs/VERIFICATION.md`.

---

## Overview

Published drought RNA-seq for finger millet was originally analysed without a
chromosome-scale reference. This project reanalyses those data against the KNE 796-S
assembly (GCA_032690845.1, 2023), which resolves both subgenomes of the allotetraploid
(2n = 4x = 36, AABB) into 18 pseudomolecules.

**Headline result (corrected analysis):**

| | |
|---|---|
| Novel intergenic transcripts detected (gffcompare class `u`) | **21,864** |
| Significantly drought-upregulated (padj < 0.05, log₂FC ≥ 1.5) | **2,422** |
| Of those, no Swiss-Prot homolog at E ≤ 1e-5 | **1,532 (63.3%)** |
| Mobile-element derived | **203 (8.4%)** |
| Novel transcripts with a Swiss-Prot hit, across all 21,864 | **6,106 (27.9%)** |

Tier distribution of the 2,422, from the corrected BLASTx join with word-boundary
keyword matching:

| Tier | Count |
|---|---|
| Tier 1 — no homolog, highly induced (log₂FC ≥ 3) | 1,184 |
| Tier 1 — no homolog | 348 |
| Tier 2 — stress-related homolog | 50 |
| Tier 3 — other homolog | 840 |

For like-for-like comparison, the *original* 2,354-transcript set re-annotated with the
same corrected join gives 63.5% with no homology (1,494 of 2,354) and tiers
1,168 / 326 / 56 / 804.

### The no-homology rate is unremarkable, and that matters

The first version of this analysis reported **99.6%** of drought-upregulated novel
transcripts as having no Swiss-Prot homolog, and built an argument on it. That figure
was a software defect, not a finding — the annotation join never matched (see
*Known defects* below). The true rate is **≈63%**.

**≈63% is consistent with published expectations for intergenic transcribed regions in
the grasses.** Lloyd *et al.* (2019) found that only **16–23% of intergenic transcribed
regions (ITRs)** in their survey had detectable protein-level similarity, i.e. roughly
77–84% did not — so a novel-transcript set that is ~63% homology-free is, if anything,
*better* annotated than the ITR background. No claim of an unusually novel gene
repertoire is supportable from this rate.

> Lloyd JP, Bowman MJ, Azodi CB, Sowers RP, Moghe GD, Childs KL, Shiu S-H (2019).
> Evolutionary characteristics of intergenic transcribed regions indicate rare
> novel genes and widespread noisy transcription in the Poaceae.
> *Scientific Reports* **9**:12122.
> doi:[10.1038/s41598-019-47797-y](https://doi.org/10.1038/s41598-019-47797-y)

The interesting question this dataset can support is not *"why is so much unknown?"* but
*"which specific loci are worth following up?"*

---

## The lead candidate: MSTRG.31255.1

One candidate survives systematic re-examination. Every statement below is traceable to
a deposited file.

**Locus.** `CM064427.1` (chromosome **6A**) : 16,937,315–16,938,027, minus strand, 713 bp.
**Single-exon**, so it is unaffected by the unspliced-extraction defect described below.

**Expression.** baseMean 575.6, **log₂FC 4.434** (apeglm-shrunk 4.382),
**padj 1.56 × 10⁻³²**. Rank 4 of 2,422 by padj. Stable across the unpaired model, the
paired model and apeglm shrinkage — the shrunk and unshrunk estimates differ by 1.2%,
which indicates a well-measured transcript rather than a low-count artefact.

**Protein.** 104 aa, cysteine-rich. Complete ORF with a genuine start and stop codon at
nt 108–422 of the extracted interval. Signal peptide predicted at residues
**1–28 (SignalP-EUK)** and **1–32 (Phobius)**; Phobius annotates residues **33–104 as
extracellular** (`NON_CYTOPLASMIC_DOMAIN`).

> **It is secreted, not membrane-associated.** SignalP-EUK's own verdict is
> `SignalP-noTM` — it explicitly calls no transmembrane region. TMHMM's "TMhelix 7–29"
> lies inside the signal peptide (Phobius H-region 12–23, cleavage at 28) and is the
> standard TMHMM/signal-peptide confusion. The only TM-positive call comes from
> `SignalP_GRAM_POSITIVE`, a bacterial model.

**Homology.** **No Swiss-Prot hit at E ≤ 1e-5**, confirmed with the corrected join. But
the ColabFold MSA finds **27 distinct homologs** (32 aligned rows, 5 exact duplicates)
across **seven grass genera and twelve species in three subfamilies**:

| Subfamily | Genera |
|---|---|
| Oryzoideae | *Oryza* (6 species), *Leersia* |
| Panicoideae | *Setaria*, *Dichanthelium*, *Sorghum*, *Zea* |
| Arundinoideae | *Arundo* |

Best E = 7.3 × 10⁻³¹ at 30.0% identity. **Twenty-three rows are annotated only as
"uncharacterized protein"; every UniProt-derived row is unreviewed TrEMBL and none is in
Swiss-Prot** — which is precisely why BLASTx against Swiss-Prot returns nothing. All
share an invariant C-terminal cysteine module. The per-row table is deposited at
`structures/MSTRG_31255_1/MSA_composition.tsv`.

**Gene family.** tblastn of the 104 aa peptide against the assembly recovers a small
family: a 100%-identity self-match at 6A:16,937,920–16,937,609, a **tandem paralog on 6A**
at 16,932,988–16,933,233 (79.3% identity, 4.4 kb upstream, same strand), and a
**homoeologous copy on 6B** at 17,668,818–17,669,132 (88.6%), plus two more diverged 6B
copies. The 6A/6B pair is exactly what an AABB allotetraploid predicts. **None of the
family members is annotated in the reference.**

**Structure — low confidence.** ColabFold 1.6.1 / AlphaFold2-ptm: **mean pLDDT 59.95,
pTM 0.390, MSA depth 34**. Only residues **~66–104 exceed pLDDT 70**; 41 of 104 residues
fall below 50. **The model supports a disulfide-stabilised C-terminal cysteine module and
nothing more.** It is far too weak to assign a fold or a repeat architecture, and any
description of confident flanking helices is unsupported.

**What this does and does not support.** The evidence supports *a small secreted
cysteine-rich protein family conserved across the grasses and uncharacterised throughout*.
It does **not** support "finger millet-specific". No Chloridoideae sequence appears in the
alignment, so conservation within *Eleusine*'s own subfamily has never been tested —
a targeted tblastn against *E. indica* and *Oropetium thomaeum* would settle it.

---

## Data sources

Both inputs are public and were used under their respective terms.

| Resource | Accession | Source |
|---|---|---|
| RNA-seq, control | DRR095904, DRR095905, DRR095906 | DDBJ Sequence Read Archive |
| RNA-seq, drought | DRR095907, DRR095908, DRR095909 | DDBJ Sequence Read Archive |
| Sample / BioProject | DRS049651 / PRJDB5606 | Hatakeyama *et al.* (2018) |
| Reference genome | GCA_032690845.1 (*Eleusine_coracana_v1.0*, cv. KNE 796-S) | NCBI GenBank / Phytozome |
| Protein database | UniProt Swiss-Prot, 574,627 sequences / 208,482,574 residues | UniProt Consortium |

Assembly as used: **532 sequences** (18 pseudomolecules + 514 unplaced scaffolds),
**1,111,714,373 bp**, N50 **61,270,980 bp**.

> **The reference is not the Hatakeyama assembly.** GCA_032690845.1 is a 2023
> chromosome-scale assembly of Kenyan cultivar KNE 796-S (WGS project JASSVF, Phytozome
> locus prefix `ELECO.r07`). Hatakeyama *et al.* 2018 describes a different, short-read
> assembly of a different accession. The 2018 paper is the correct citation for the
> **RNA-seq data**, not for the genome.

---

## Workflow

Stages 1–5 and the Swiss-Prot annotation step are defined in the Snakemake workflow.
Stages 6 onward were executed interactively — see *Reproducibility*.

| Stage | Tool | Version |
|---|---|---|
| Quality control | FastQC / MultiQC | 0.12.1 / 1.33 |
| Trimming | Trimmomatic | 0.40 |
| Alignment | HISAT2 | 2.2.2 |
| Assembly, quantification | StringTie | 3.0.0 |
| Transcript comparison | gffcompare | 0.12.10 |
| Count matrices | `prepDE.py` (StringTie 3.0.0) | — |
| Independent count check | featureCounts (subread) | 2.1.1 |
| Differential expression | DESeq2 / apeglm, R 4.5.3 | 1.50.2 / 1.32.0 |
| ORF prediction | TransDecoder | 5.7.1 |
| Domain annotation | InterProScan 5 | EBI REST service |
| Homology search | BLAST+ | 2.17.0 |
| Structure prediction | ColabFold / AlphaFold2-ptm | 1.6.1, web service |
| Structural homology | Foldseek | web API |
| Workflow engine | Snakemake | 9.19.0 |

Full parameters are in the deposited scripts and in `docs/MANIFEST.md`.

**Read length was measured, not assumed.** `prepDE.py` was run at the mean aligned read
length of **142 bp**, sampled across four 4 Mb windows on chromosomes 1A, 3B, 6A and 9A in
every BAM. Modal length is 151 bp, but reads are Trimmomatic-trimmed. Matrices at both
lengths are deposited; the 151 bp version rescales all counts by a uniform 0.9405, which
DESeq2's size factors absorb entirely, so the choice affects no result.

---

## Repository structure

```
workflow/            Snakefile, config.yaml, setup.sh                            3 files
scripts/             maintained analysis scripts (v1 and v2)                     8 files
  reconstructed/     20 scripts recovered verbatim from shell history + README  21 files
results_v1/          ORIGINAL analysis — superseded, retained as record         18 files
  novel_genes/       novel_genes.gtf, blast_results.txt
  synteny/           vs_sorghum.txt, vs_rice.txt, vs_foxtail.txt
  transdecoder/      top50_transcripts.fa
  final_report/      candidate_genes_final.tsv (provenance unknown — see below)
  sequences/         peptide FASTAs + provenance sidecars
results_v2/          CORRECTED re-analysis — use these                          32 files
  de/                DESeq2 output, both models, diagnostics
  counts/            prepDE + featureCounts matrices, sample sheet
  annotation/        corrected BLASTx join, all three annotation tables
  blast/             raw BLASTx output, query BED, run script
structures/          ColabFold models, MSAs, scores, query CSVs                101 files
figures_v2/          10 plots, all reproducible from deposited inputs           10 files
logs/                run logs                                                    5 files
docs/                MANIFEST, DE_COMPARISON, MANUSCRIPT_CORRECTIONS, VERIFICATION
LICENSE, CITATION.cff, README.md
```

**204 files, ~155 MB.**

To run any deposited script, first make `results_v1` visible under the name the scripts
expect:

```bash
ln -s results_v1 results     # or: mv results_v1 results
export FM_ROOT="$PWD"        # v2 scripts read this; default is "."
```

---

## Known defects in the original analysis

All four were found by audit, are fixed or quantified in `results_v2/`, and are
documented in full in `docs/DE_COMPARISON.md`.

1. **DESeq2 was not given read counts.** `scripts/de_analysis.R` parses the `cov`
   attribute from the StringTie GTFs and computes `round(cov * 100)` — per-base coverage
   scaled by an arbitrary constant. StringTie *was* run with `-e -B` and did produce
   genuine count tables; they were never used. `lfcShrink()` was never called.
   *Consequence:* the negative-binomial variance assumption was violated, p-values were
   far too extreme (6.7 × 10⁻⁶⁶ became 1.4 × 10⁻³⁷), and fold changes for transcripts with
   zero control counts were inflated by ~3 log₂ units. **Fold changes for transcripts with
   any control signal were essentially unaffected** (median shift −0.02, r = 0.974).

2. **The BLASTx annotation join never matched.** `bedtools getfasta -name` was given a
   GTF, so it wrote the *feature type* — the literal string `transcript` — as the FASTA
   name. All 21,864 query IDs read `transcript::<chrom>:<start>-<end>` while the DE table
   was keyed on `MSTRG.x.y`. The `how="left"` merge assigned NaN to every row.
   *Consequence:* the pipeline reported **zero** annotations; the "99.6% no homology"
   claim is an artefact. The re-run confirms the original BLASTx itself was correct —
   51,468 hit lines in both runs, columns 2–7 byte-identical. **This affected only the
   whole-set extraction; the top-50 extraction used a BED with correct IDs.**

3. **`STRESS_WORDS` matched substrings, not words.** `ABA` matched *tab**aba**cum*;
   `LEA` matched *nuc**lea**r* and *nuc**lea**se*. 58% of Tier 2 had no word-boundary
   match. The most frequent "stress-related" annotation was a tobacco retrotransposon.
   *Consequence:* Tier 2 is 50, not 119 — and even those 50 are 46 × `kinase`,
   2 × `stress`, 2 × `peroxidase`. **"Stress-related" operationally means "contains a
   kinase" and should be rebuilt by curation.**

4. **Sequence extraction lost exon structure.** `novel_genes.gtf` retains transcript
   records but no exon records, so `bedtools getfasta -split` had nothing to split on and
   returned whole genomic intervals. The top-50 extraction ran without `-split` at all.
   *Consequence:* **all extracted sequences include introns.** 47 of the top 50 candidates
   are multi-exon, so any ORF called on them may be a chimera of exonic and intronic
   sequence — confirmed for MSTRG.45757.2, whose 197 aa prediction is 42.4% intronic and
   antisense to the annotated transcript. **The DE analysis is unaffected** (it uses
   `merged_assembly.gtf`, which retains exons). Single-exon candidates, including
   MSTRG.31255.1, are unaffected.

---

## Limitations

These constrain interpretation and cannot be fixed by re-analysis.

### Experimental design

- **Treatment is confounded with plant age — this is the largest single constraint on the
  central claim.** **No time-matched well-watered control was sampled at day seven:** the
  control libraries were taken at the start of the experiment and the drought libraries
  after seven days of withheld water. Every transcript called drought-responsive is
  equally consistent with being development-responsive over a seven-day window in a young
  plant. Nothing in this dataset can separate the two. Detailed environmental information
  for the growth period — watering amount and timing, temperature — was not retained, so
  the size of the developmental component cannot be bounded from the record either.
- **The six libraries are treated as independent samples.** Whether the control and
  drought libraries derive from the **same individual plants cannot be established**, from
  either the data or the surviving experimental records; the original laboratory notes no
  longer exist. A surviving sample-name table pairs matched replicate numbers with a `_D`
  suffix for the drought samples, which suggests that a correspondence was intended, but
  there is no documentation confirming that the same individuals were sampled twice. The
  pairing is therefore not sufficiently documented to justify treating the design as
  confirmed repeated measures. The data agree: a paired model (`~ plant + condition`) was
  fitted using the ENA library-name suffixes and **rejected** — it *increased* dispersion
  (asymptDisp 0.786 → 0.880; median 0.913 → 1.497) and cost 8,239 transcripts their
  testability, and all six possible control↔drought pairings absorb 49.1–51.0% of
  within-condition variance, statistically indistinguishable, with the suffix-inferred
  pairing not even the best. The suffixes do not encode plant identity, and no pairing is
  recoverable from the counts. **Treating the libraries as independent, as `~ condition`
  does, is the appropriate choice.**
- **Replication is biological, but is not declared in the archive.** Within each sampling
  group the three libraries were prepared from **separate plants**, so the replication is
  biological rather than technical. This is not recorded in the archive metadata: all 18
  runs of PRJDB5606 sit under a single BioSample, `SAMD00076255`.
- **The plants derive from highly inbred seed** obtained from GKVK Bangalore and
  originally from ICRISAT, so the sampled individuals should be genetically very similar.
- **The libraries were not generated for this experiment.** They were produced primarily
  to support genome annotation rather than as a designed differential-expression
  experiment. Study title: *"Finger millet genome assembly."* No growth protocol, drought
  severity or timepoint is recorded.
- **Condition assignment rests on library names** (`Illumina_RNA_ctl_1-3` /
  `dry_1-3`), which corroborate `config.yaml` but assume the run accessions map in order.

### Statistical

- **Dispersion is extreme. `asymptDisp = 0.786`** implies ~89% coefficient of variation
  between replicates at high expression — 20–80× typical for controlled plant RNA-seq.
  The replicates are biological, not technical, so this is genuine between-plant variation
  in material that was not collected under a controlled experimental protocol. Genetic
  heterogeneity is largely excluded as an explanation, because the plants derive from
  highly inbred seed, which makes the magnitude of the dispersion more notable rather than
  less. **Do not quote p-values to more than an order of magnitude.**
- **Sequencing depth is confounded with condition** (drought libraries 21.0–36.4 M
  assigned fragments vs control 18.5–22.0 M). Depth itself is excluded as an explanation
  for the detection asymmetry: a depth-matched pair (DRR095905 at 21,011,330 vs DRR095909
  at 20,994,628, 0.08% apart) still differs by 31.8% in transcripts detected, and 96.4%
  of the 1,278 zero-in-all-controls transcripts are detected in DRR095909 alone with a
  median 231 fragments. Whether this reflects genuine transcriptional activation or a
  library-preparation difference between the two collection dates cannot be determined.

### Content and annotation

- **8.4% of the drought-upregulated set (203 of 2,422) is mobile-element derived.** No
  repeat-masking was performed before novelty assessment. The figure is reproducible from
  `results_v2/annotation/candidate_genes_v2_annotated.tsv` by case-insensitive match of the
  `annotation` field against
  `transposon|retrovirus|pol polyprotein|gag-pol|reverse transcriptase|integrase|LINE-1|retrotransposon`
  (the `LINE-1` term is required: 28 rows hit `LINE-1 retrotransposable element ORF2
  protein`, which none of the other terms match). It is a lower bound — it counts only
  transcripts whose best Swiss-Prot hit is explicitly a mobile-element protein. The most frequent Swiss-Prot
  subjects across the whole annotated set are mobile-element proteins. **Two of the ten
  top-ranked candidates are Ty3/Gypsy retrotransposons** (MSTRG.4687.1, E = 2.0 × 10⁻¹⁰⁶;
  MSTRG.45758.1, E = 4.5 × 10⁻⁷²), confirmed independently by BLASTx, InterProScan and
  Foldseek. Transposon insertions are lineage-specific by nature and will score as
  species-specific for reasons unrelated to novel gene content.
- **The cross-species screen was underpowered and its "species-specific" calls are
  unreliable.** It used `blastn` (nucleotide) at E ≤ 1e-5 against three genomes. For
  MSTRG.31255.1 this returned no hits, yet the MSA for the same protein finds 27 distinct
  homologs across seven genera at 22–34% amino acid identity — a divergence at which
  nucleotide alignment fails regardless of threshold. **Protein-level search (`tblastn`)
  is the appropriate method.** Every lineage-specificity call inherits this limitation.
- The screen is homology detection, not synteny: no collinearity or orthology assignment
  was performed, and `-max_target_seqs 1` was used, which does not reliably return the
  best hit.
- **No Chloridoideae genome was included.** The three comparison genomes (*Sorghum
  bicolor*, *Oryza sativa*, *Setaria italica*) are Panicoideae and Oryzoideae, so
  conservation among *Eleusine*'s close relatives was never tested.
- Absence of a BLAST hit is not evidence of gene absence.
- Only 10 of 50 candidates were classified, and the list is hard-coded in the scripts.
- **The candidate set has an untraced origin.** `results_v1/final_report/candidate_genes_final.tsv`,
  from which the top-50 were selected, has **no recorded creating script or command** — no
  Snakefile rule and no shell-history line produces it, and it contains four tier strings
  where `merge_results.py` can emit only three. This is a break in the chain of custody
  affecting all downstream candidate selection. The file is deposited; its provenance is
  not recoverable.
- A MAPQ ≥ 20 filter discards reads mapping ambiguously between the A and B subgenomes.
- GO enrichment was attempted and is **excluded**: wrong organism (*A. thaliana*),
  9 of 29 accessions mapped, and no drought-, ABA-, ROS- or osmotic-stress term among the
  28 returned.
- Co-expression values are not re-derived at run time — `stage10d` hard-codes its
  expression matrices as literals. They were independently verified against the StringTie
  count files (10/10 exact), but re-running the script replays rather than recomputes.
- **Computational analysis only. No experimental validation has been performed, and this
  work has not been peer reviewed.**

---

## Reproducibility

- **`results_v2/` is fully reproducible from deposited files.** `de_analysis_v2.R`,
  `de_analysis_v2_paired.R` and `rebuild_annotation_v2.py` each have all their inputs in
  the package.
- **`results_v1/` DE tables are not.** They need `results/counts/*_counts.gtf` (~600 MB),
  which is too large to deposit. The Snakefile rule that produces it is included and its
  inputs are the public reads and the public genome.
- **Twenty analysis scripts were never saved as files.** Stages 6, 8, 9, 10 and 11 were
  executed as shell heredocs and survive only in shell history. They are recovered
  verbatim in `scripts/reconstructed/`, unmodified — including hard-coded values, absolute
  paths and internal inconsistencies. See `scripts/reconstructed/README.md`.
- **`config.yaml` has been corrected in this copy.** The original reference URLs pointed at
  GCA_002477235.1, a different assembly from the one used. The original file is unmodified
  in the source project. See `docs/MANIFEST.md` §6.
- **`novel_transcripts_named.fa` (72 MB) is omitted** and regenerable — see
  `results_v2/blast/run_blastx_v2.sh` for the `bedtools getfasta` command and
  `results_v2/blast/novel_transcripts.bed` for the intervals.
- **Six ChimeraX renders were withdrawn.** `analyze_structures.cxc` cannot run as written
  (three of four `open` paths name non-existent model files) and never opens the lead
  candidate, so the images' subjects could not be established. The script is retained as a
  provenance artefact with a header stating the defect. See `docs/VERIFICATION.md` §1.4.
- **Some result tables are not deposited**: promoter-scan output, co-expression matrices,
  the g:Profiler CSV, and Foldseek result directories. Reasons are in `docs/MANIFEST.md` §8.

---

## Use of AI assistance

Anthropic's Claude was used at several stages of this project and its use is disclosed
here in full.

**Original analysis (April 2026).** Claude (via claude.ai) was used to plan the pipeline,
draft the Snakemake workflow and R scripts, troubleshoot software installation, and
interpret intermediate results. All commands were executed by the author.

**Audit and re-analysis (August 2026).** Claude Code was used to audit the completed
workflow against the filesystem, recover analysis scripts from shell history, re-run the
differential expression analysis using proper count matrices, re-run BLASTx with corrected
sequence identifiers, and compile the corrections document. The scripts
`de_analysis_v2.R`, `de_analysis_v2_paired.R` and `rebuild_annotation_v2.py` were written
with Claude Code and reviewed by the author.

**Author responsibility.** All analytical decisions, all interpretation, and all claims in
this deposit are the author's. AI output was reviewed rather than accepted; several
AI-generated conclusions were found to be incorrect during the audit and are documented as
corrections in `docs/DE_COMPARISON.md` and `docs/MANUSCRIPT_CORRECTIONS.md`.

---

## Licence

This package is **dual-licensed**:

| Contents | Licence |
|---|---|
| Everything in `scripts/` — including `scripts/reconstructed/` | **MIT** (see `scripts/LICENSE`) |
| `workflow/Snakefile` and `workflow/setup.sh` — executable code | **MIT** (see `workflow/LICENSE`) |
| Everything else — data tables, structures, figures, documentation, and `workflow/config.yaml` | **CC BY 4.0** |

The two `workflow/` scripts are MIT so they can be reused and modified without the
ambiguity a Creative Commons licence introduces for software. `workflow/config.yaml` is
configuration data, not code, and stays under CC BY 4.0.

Full texts of both licences, and the statement of which applies to what, are in
[`LICENSE`](LICENSE).

Third-party inputs (the RNA-seq reads, the reference assembly, Swiss-Prot) are **not**
covered by these licences and remain under their original terms.

---

## Citation

If you use this work, cite the Zenodo record — see [`CITATION.cff`](CITATION.cff).

Please also cite the underlying data and reference genome:

- Hatakeyama M, *et al.* (2018). Multiple hybrid de novo genome assembly of finger millet,
  an orphan allotetraploid crop. *DNA Research* **25**(1), 39–47.
  *(Source of the RNA-seq data, DRS049651 — not of the reference genome.)*
- *Eleusine coracana* subsp. *coracana* cv. KNE 796-S genome assembly
  (GCA_032690845.1). NCBI GenBank / Phytozome.

---

## Contact

Joash Joshua Ayo — Independent Researcher, Kampala, Uganda
[ORCID 0009-0007-1642-0172](https://orcid.org/0009-0007-1642-0172) — joashjoshua789@gmail.com

Feedback and correction are welcome. **This work has not been peer reviewed and no
experimental validation has been performed.**
