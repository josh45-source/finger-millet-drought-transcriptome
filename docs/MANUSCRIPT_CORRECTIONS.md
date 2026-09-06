# MANUSCRIPT_CORRECTIONS.md

**Subject:** the 17 April 2026 manuscript text, 3,452 words, now archived as
`archive/finger_millet_preprint_v2_ORIGINAL_17Apr2026.md` in the manuscript directory
**Compiled:** 28 August 2026
**Basis:** `results_v2/` re-analysis — genuine `prepDE.py` counts, re-run BLASTx with correct query IDs, `results_v2/DE_COMPARISON.md`

**When this document was compiled, no edits had been made to either preprint;** it lists
what had to change and why. The corrections were subsequently applied. The live draft is
`finger_millet_preprint_v2.md`; the corrected v1 draft and both unmodified 17 April texts
are in `archive/` alongside it, described by `archive/README.md`.

Every quotation below is verbatim from v2. Section numbers are v2's.

---

## Correction notice — 28 August 2026

Two figures describing the MSTRG.31255.1 multiple sequence alignment were **wrong in the
first version of this document** (26 August 2026) and have been corrected throughout.
They are recorded here rather than silently overwritten, because they were also carried
into `README.md` and reported verbally, and anyone working from the earlier text needs to
know.

| Stated 26 Aug | Correct value | What went wrong |
|---|---|---|
| "32 homologs" | **27 distinct homologs** (32 aligned rows, 5 exact duplicates) | Alignment *rows* were counted as distinct sequences. The `.a3m` holds five pairs whose sequences are byte-identical: `K4A2R8`/`UniRef100_A0A368Q1M5`, `A0A0D9XDT2`/`UniRef100_A0A0D9XDT2`, `A0A0E0ES30`/`UniRef100_A0A0E0ES30`, `A0A0E0M128`/`UniRef100_A0A0E0M128`, and `9712\|scaffold142863_1`/`MGYP001059640954`. Each pair is one sequence indexed under two accessions. |
| "nine grass genera" | **seven genera, twelve species** | Miscount. The genera are *Arundo*, *Dichanthelium*, *Leersia*, *Oryza*, *Setaria*, *Sorghum* and *Zea*. Six of the twelve species are *Oryza*, which is where the overcount came from. |
| "30 of 32 are Uncharacterized protein" | **23 rows** are "Uncharacterized protein"; 2 carry a functional name; 2 are obsolete entries with no retrievable name; 5 are unannotated metagenomic/environmental sequences | The original figure conflated "no functional name" with the TrEMBL "Uncharacterized protein" label, and counted metagenomic rows as UniProt entries. |

**Unchanged and still correct:** three subfamilies (Oryzoideae, Panicoideae,
Arundinoideae); no *Eleusine* and no Chloridoideae sequence in the alignment; every
UniProt-derived row unreviewed TrEMBL and absent from Swiss-Prot; MSA depth 34 as
reported by ColabFold (= 32 aligned rows + 2 copies of the query); best E = 7.3e-31.

All three figures are now recomputed directly from the deposited
`structures/MSTRG_31255_1/MSTRG_31255_1_finger_millet_932c3.a3m`, and the full per-row
table — accession, source database, organism, subfamily, product name, identity, E-value
and duplicate grouping — is deposited alongside it as `MSA_composition.tsv` so every
number here can be checked without re-querying UniProt.

---

## How this is organised

| Class | Meaning | Count |
|---|---|---|
| **A** | Numerical correction — swap the value, the sentence still stands | 14 |
| **B** | Argument must be rewritten — the claim's substance changes | 4 |
| **C** | **Conclusion changes, not just the number** | 3 |
| **D** | Checked and confirmed correct — do not touch | 12 |
| **E** | Not fixable by re-analysis — belongs in Limitations | 5 |

Read Class C first. Those three are the ones a reviewer will use to reject the paper.

---

# CLASS C — corrections that change the conclusion

## C1. The 99.6% no-homology claim is a software bug

**Where:** Abstract; §3.4 (twice, plus the tier table); §4.2 (first sentence and the whole three-explanation argument); §5 Conclusions.

**Exact sentences:**

> "Strikingly, 99.6% of these novel drought-upregulated transcripts had no significant homology to any characterised protein in UniProt/Swiss-Prot, suggesting that finger millet possesses a largely unique drought-responsive gene repertoire." *(Abstract)*

> "BLASTx comparison against UniProt Swiss-Prot revealed that **99.6% of novel drought-upregulated transcripts (2,344 of 2,354) had no significant homology to any characterised protein**. Only 10 transcripts matched known proteins, yielding the following candidate tier distribution:" *(§3.4)*

> "The finding that 99.6% of novel drought-upregulated transcripts lack homology to characterised proteins is remarkable." *(§4.2)*

> "The near-complete absence of homology to characterised proteins suggests that finger millet's exceptional drought tolerance is underpinned in part by a unique molecular repertoire previously inaccessible to researchers." *(§5)*

**Corrected value: 63.5% (1,494 of 2,354). 860 transcripts matched known proteins, not 10.**

**Evidence.** `bedtools getfasta -name` was given a GTF and wrote the feature type — the literal string `transcript` — as the FASTA name, so all 21,864 query IDs read `transcript::<chrom>:<start>-<end>`. `merge_results.py` joins that to a DE table keyed on `MSTRG.x.y`. The key spaces are disjoint; the `how="left"` merge assigned `NaN` to every row. `results/final_report/candidate_genes_annotated.tsv` — the actual Snakemake output, 14 Apr 21:31 — contains **zero** annotated rows. The 10 in `candidate_genes_final.tsv` were hand-added between 21:31 and 22:27.

BLASTx was re-run 27–28 Aug with identical parameters against the identical database, from a re-extraction whose sequences are byte-identical (`d2d9c6e535fa1395af38d1ef11f08e88` for both sequence streams). Output: **51,468 hit lines in both runs, with columns 2–7 byte-identical (`715cfd1610884697656649b5d487270e`)**. The original BLASTx was correct. Its entire result was discarded by the join.

**Why this changes the conclusion, not the number.** §4.2 offers three explanations for the 99.6% — Chloridoideae under-representation in databases, sequence divergence below detection, and genuine orphan genes. At 63.5% that argument does not merely weaken; its premise is gone. A no-homology rate of 63.5% for *unannotated intergenic transcripts assembled from a single tissue* is unremarkable — it is roughly what any RNA-seq study recovers from novel loci, most of which are lowly expressed, repeat-adjacent, or fragmentary. **The "largely unique drought-responsive gene repertoire" framing, which is the paper's central claim and appears in the title's spirit, the abstract, §4.2 and the Conclusions, is not supported by the corrected data.**

**Required action:** rewrite the Abstract's fourth sentence, all of §3.4, all of §4.2, and the Conclusions' second sentence. The tier table in §3.4 must be replaced (see C2). Reframe the paper around what the data do support: a catalogue of 2,422 drought-responsive transcripts absent from the current annotation, of which a substantial minority have no Swiss-Prot homolog.

---

## C2. The tier table is wrong by one to two orders of magnitude in two rows

**Where:** §3.4 table; §2.9 (tier definitions); Abstract; Table 2's Tier column.

**Exact table as printed:**

> | Tier | Description | Count |
> |------|-------------|-------|
> | Tier 1 | No homolog, highly induced (log₂FC ≥ 3) | 1,802 |
> | Tier 1 | No homolog | 542 |
> | Tier 2 | Stress-related protein homolog | 3 |
> | Tier 3 | Other protein homolog | 7 |
> | **Total** | | **2,354 |

**Corrected** (original 2,354 set, clean join, word-boundary keyword matching):

| Tier | Description | as printed | **corrected** |
|---|---|---|---|
| Tier 1 | No homolog, highly induced | 1,802 | **1,168** |
| Tier 1 | No homolog | 542 | **326** |
| Tier 2 | Stress-related homolog | 3 | **56** |
| Tier 3 | Other homolog | 7 | **804** |

Tier 2 is understated **19-fold**, Tier 3 **115-fold**.

**A second, independent bug.** `merge_results.py` tests `w.lower() in ann.lower()` — substring, not word. Two of its `STRESS_WORDS` are three-letter strings that occur inside common words:

- **`ABA` matches `tabacum`** — every *Nicotiana tabacum* hit is scored stress-related (36 transcripts).
- **`LEA` matches `nuclear` and `nuclease`** (30 transcripts).

**58% of Tier 2 (69 of 119) has no word-boundary match at all.** The most frequent Tier 2 annotation is `sp|P10978|POLX_TOBAC Retrovirus-related Pol polyprotein from transposon TNT 1-94` — a tobacco retrotransposon, classified stress-related because *tab**aba**cum*.

After removing substring false positives, the surviving 56 are 46 × `kinase`, 2 × `stress`, 2 × `peroxidase` and a handful of others. **"Stress-related" operationally means "contains a kinase."**

**Why this changes the conclusion.** §2.9's prioritisation scheme is presented as a functional triage, and §4.3's four priority candidates are drawn from it. Neither is defensible as constructed. Tier 2 must be rebuilt by manual curation of the 860 annotated transcripts, not keyword matching, and §2.9 must state the method honestly.

**Note for the record:** `MSTRG.37761.2` (MDAR3) is Tier 3 under both keyword schemes — "Monodehydroascorbate reductase" contains no keyword. `candidate_genes_final.tsv` files it as Tier 2, which no version of `tier()` can produce. Confirms the filed annotations were hand-entered.

---

## C3. 8.4% of the catalogue is transposon-derived, and two of the ten headline candidates are retrotransposons

**Where:** Table 2 rows 4 and 8; §3.4; §4.2; §5.

**Exact sentences:**

> `| MSTRG.45758.1 | 3.14 | 2,035 | 2.83×10⁻⁵² | Tier 1 | No homolog |` *(Table 2)*
> `| MSTRG.4687.1 | 3.50 | 4,032 | 7.38×10⁻³⁶ | Tier 1 | No homolog |` *(Table 2)*

**Corrected:**

| Transcript | Best Swiss-Prot hit | E-value | Tier |
|---|---|---|---|
| MSTRG.45758.1 | Transposon Tf1-107 polyprotein (*S. pombe*) | **4.46e-72** | **Tier 3** |
| MSTRG.4687.1 | Transposon Tf2-6 polyprotein (*S. pombe*) | **2.03e-106** | **Tier 3** |

**Evidence — three independent methods agree:**

1. **BLASTx** (this re-run): the hits above.
2. **InterProScan** `iprscan5-R20260417-190817-0777-66196655-p1m`: both carry Pfam `PF00665` Integrase core, `PF17921` Integrase zinc-binding, `PF17917` RNase H-like RT; MSTRG.4687.1 additionally CDD `cd09274 RNase_HI_RT_Ty3`; MSTRG.45758.1 additionally `PF24626` Tf2-1-like SH3.
3. **Foldseek**: Transposon Tf2-7 polyprotein at probability 1.0, E = 3.1e-36 and 2.5e-50.

Across the whole set, **203 of 2,422 (8.4%)** hit a transposon, retrovirus-related polyprotein, integrase or reverse transcriptase. The most frequent Swiss-Prot subjects among all 890 annotated transcripts are mobile-element proteins: `POLX_TOBAC` (35), `YG31B_YEAST` (26), `TF107_SCHPM` (23), `POLR1_ARATH` (22), `LIN1_NYCCO` (19).

**Why this changes the conclusion.** These are not novel genes. They are unannotated copies of mobile elements, and their drought "induction" is at least as consistent with stress-induced retrotransposon activation — a well-documented phenomenon — as with a protective function. Two of the ten transcripts in Table 2 are in this category. The paper must state the mobile-element fraction explicitly and exclude these from the candidate list, or defend keeping them.

**v1 was right and v2 made this worse.** v1's Table 2 annotated MSTRG.45758.1 as "Transposable element"; v2 replaced that with "No homolog". Restore and extend it.

---

# CLASS B — corrections requiring rewritten argument

## B1. MSTRG.20738.1 is not a Tier 1 no-homolog transcript

**Where:** Table 2 row 1; §3.7; §4.3 Priority 4.

**Exact sentences:**

> `| MSTRG.20738.1 | 2.59 | 2,198 | 6.73×10⁻⁶⁶ | Tier 1 | ARM repeat domain |` *(Table 2)*

> "**MSTRG.20738.1** (log₂FC = 2.59, padj = 6.73×10⁻⁶⁶): InterProScan identified an ARM (Armadillo) repeat domain (SUPERFAMILY classification) with PANTHER assigning it to the BAP28 family. ARM repeats mediate protein-protein interactions and are components of several plant drought signalling pathways, including the ABA receptor complex and the proteasomal degradation machinery activated under stress." *(§3.7)*

> "**Priority 4 — MSTRG.20738.1 (ARM repeat, most significant p-value):** With the smallest adjusted p-value in the dataset (6.73×10⁻⁶⁶), this transcript shows exceptional consistency across replicates. ARM repeat proteins are scaffolding components of signalling complexes and may represent a novel component of finger millet's drought network." *(§4.3)*

**Corrections:**

- **Tier 1 → Tier 3.** It hits `sp|Q9C8Z4|HEAT1_ARATH` (*A. thaliana* At3g06530) at **E = 2.19e-84**. It has a strong, characterised homolog.
- **The domain call is correct** — SUPERFAMILY `SSF48371` ARM repeat (E = 1.49e-9), Gene3D `G3DSA:1.25.10.10` Armadillo-like helical, PANTHER `PTHR13457` BAP28. BLASTx independently confirms it via a HEAT-repeat protein. Keep this.
- **The functional interpretation is unsupported.** PANTHER `PTHR13457 BAP28` maps to `IPR040191` — **U3 small nucleolar RNA-associated protein 10 (UTP10)**, a nucleolar rRNA-processing factor. Nothing in the output points to ABA receptors or the proteasome. Delete the ABA-receptor and proteasome sentence.
- **padj 6.73×10⁻⁶⁶ → 1.37×10⁻³⁷**, and it is no longer the most significant transcript in the dataset. Under the re-analysis it ranks 3rd within the novel set (`MSTRG.45758.1` is 1st — a retrotransposon).

**Why the argument changes:** Priority 4 rests entirely on "smallest adjusted p-value in the dataset" plus a drought-signalling interpretation. Neither survives. The same problem affects **MSTRG.6647.1**, whose PANTHER assignment `PTHR13213 MYB-BINDING PROTEIN 1A` is MYBBP1A — also a nucleolar ribosome-biogenesis protein, not a partner of plant drought MYB transcription factors. **Two of the four highlighted candidates are ribosome-biogenesis machinery.** §3.7 and §4.3 need rewriting on that basis.

---

## B2. MSTRG.21998.1 is FAB1D — a PI**3**P 5-kinase, not a PI**4**P 5-kinase

**Where:** §3.7; §4.3 Priority 1; Abstract; §5.

**Exact sentences:**

> "**MSTRG.21998.1**: InterProScan identified a Phosphatidylinositol-4-phosphate 5-Kinase (PIPK) domain confirmed by five independent databases (Pfam: PF01504, PANTHER, SMART: PIPK_2, ProSiteProfiles, Gene3D). PIP kinases phosphorylate phosphoinositides to generate second messengers that regulate ion channel activity, vacuolar functions, and stomatal closure — all critical processes in plant drought responses. This candidate has the strongest functional annotation of any transcript in our dataset." *(§3.7)*

> "**Priority 1 — MSTRG.21998.1 (PIPK domain):** Confirmed by five independent databases, PIP kinases are druggable targets whose manipulation alters drought tolerance in model plants. This represents the strongest functionally annotated candidate." *(§4.3)*

**Corrections:**

- **The five-database claim is accurate.** All five signatures are present: `PF01504`, `PTHR45748`, `SM00330 PIPK_2`, `PS51455`, `G3DSA:3.30.800.10`. Keep it.
- **The enzyme is misidentified.** BLASTx best hit is `sp|Q9XID0|FAB1D_ARATH` — *Putative 1-phosphatidylinositol-**3**-phosphate 5-kinase FAB1D* — at **E = 5.25e-99**. PANTHER independently says `PTHR45748 1-PHOSPHATIDYLINOSITOL 3-PHOSPHATE 5-KINASE-RELATED`. Both name the FAB1/PIKfyve family, which phosphorylates PI3P to make PI(3,5)P₂ and governs vacuolar and endosomal trafficking. **Pfam `PF01504` is the shared PIPK catalytic core, not evidence of PI4P 5-kinase activity.**
- The stomatal-closure / ion-channel narrative belongs to PI(4,5)P₂-generating PIP5Ks, a different enzyme. It does not apply.
- **This transcript is not lineage-specific.** It has blastn hits in all three comparison species (2 sorghum, 2 rice, 4 foxtail) and never appears in either synteny classification table. It looks like an annotation gap over a conserved FAB1 gene.
- **Its Tier 2 status is an artefact** of the `kinase` keyword (C2).
- **The ORF was predicted from unspliced genomic sequence.** `novel_genes.gtf` has no exon records and the top-50 extraction ran without `-split`, so the 420 aa peptide may read through introns. This transcript is multi-exon. **Re-derive the ORF from a spliced transcript before making any domain claim.**

**Why the argument changes:** Priority 1 is the paper's strongest functional claim. FAB1D is a plausible and interesting drought candidate — vacuolar trafficking matters under osmotic stress — but it is a *different* claim from the one written, it rests on a peptide of uncertain validity, and the gene is conserved rather than novel.

---

## B3. Fold changes for transcripts with zero control counts are not identifiable

**Where:** §3.5 (twice); §4.3 Priority 2.

**Exact sentences:**

> "**MSTRG.37761.2** matched Monodehydroascorbate Reductase 3 (MDAR3) from *O. sativa* subsp. *japonica* (log₂FC = 9.51, padj = 4.97×10⁻⁷). … The exceptionally high fold change (~730-fold) makes this one of the most dramatically induced transcripts in our dataset." *(§3.5)*

> "**Priority 2 — MSTRG.37761.2 (MDAR3 homolog, ~730-fold induced):** The extraordinary induction magnitude combined with homology to a characterised antioxidant enzyme makes this a compelling candidate for ROS scavenging during drought." *(§4.3)*

**Corrected: log₂FC = 6.45, ~87-fold, padj = 2.49×10⁻⁴.** The "730-fold" figure is wrong by a factor of **eight**.

**Evidence.** baseMean 11.9. Raw counts: **0, 0, 0** in control and 109 fragments total across drought. With a zero denominator, DESeq2's log2FC is determined by the magnitude of the numerator, not by a ratio — and the original input (`cov × 100`) inflated counts several-fold, inflating the pseudo-infinite fold change correspondingly.

This is systematic, not isolated. Among the 2,125 transcripts significant in both analyses:

| subset | n | median log2FC shift | Pearson r |
|---|---|---|---|
| detected in ≥1 control library | 854 | **−0.02** | **0.974** |
| zero in all three controls | 1,271 | **−3.03** | 0.616 |

**Transcripts with control signal are unaffected. The entire discrepancy is in transcripts where log2FC is undefined.** Worst case, `MSTRG.24586.8`: counts `0,0,0,8105,7324,0`, old log2FC 27.35, new 13.31. Neither means anything.

**Why the argument changes:** Priority 2 rests entirely on "extraordinary induction magnitude." At 87-fold from 109 fragments with one drought replicate contributing nothing, it is an ordinary low-count transcript. Every fold change quoted for a zero-control transcript must be recomputed or replaced with a lower bound.

---

## B4. Methods §2.6 describes a count workflow that was not the one used

**Where:** §2.6.

**Exact sentence:**

> "Read abundance for all novel transcripts was estimated using StringTie in count mode against the merged assembly. Differential expression analysis was performed using DESeq2 v1.46 in R v4.4, comparing drought-stressed (n = 3) versus control (n = 3) conditions."

**Correction.** Sentence one is true — `stringtie -e -B` ran and produced genuine count tables. What it omits is that those tables were never used. `scripts/de_analysis.R` parsed the `cov` attribute from the GTFs and computed:

```r
counts <- round(cov * 100)
```

DESeq2 was supplied **per-base coverage × 100**, not read counts. This violates the negative-binomial mean–variance assumption the method rests on.

**Also:** `lfcShrink()` was never called — neither `apeglm` nor `ashr` was installed — so no shrinkage may be claimed.

**Required action:** the re-analysis (`scripts/de_analysis_v2.R`) uses `prepDE.py` counts at the measured mean aligned read length of 142 bp, validated against `featureCounts` at Spearman ρ = 0.985–0.995 across all six samples. Methods must describe *that*, and every downstream number must come from it.

**Mitigating fact worth stating plainly:** the substitution did **not** systematically distort fold changes. Because `old ≈ new × 14200/length` is constant within a transcript, it cancels in a ratio; size factors recomputed on a reconstructed `cov × 100` matrix agree with prepDE's to within 0.8%, implying a normalisation bias of −0.009. The damage was to the *variance* structure, hence the p-values, and to zero-control transcripts (B3).

---

# CLASS A — numerical corrections

Drop-in value swaps. The surrounding sentence stands.

| # | §  | Exact text | Correct value | Evidence |
|---|---|---|---|---|
| A1 | 2.2 | "The genome comprises **9 pseudochromosomes** with a total assembly size of approximately 1.1 Gb." | **18** | `genome.fa.fai`: CM064417.1–CM064434.1, named 1A/1B…9A/9B. 1.1 Gb is correct (1,111,714,373 bp). v2 contradicts itself — §1 states "2n = 4x = 36", which requires 18. |
| A2 | 2.3 | "MultiQC v1.25" | **1.33** | conda env |
| A3 | 2.4 | "HISAT2 v2.2.1" | **2.2.2** | conda env |
| A4 | 2.4 | "SAMtools v1.21" | **1.23.1** | conda env |
| A5 | 2.5 | "StringTie v2.2.1" | **3.0.0** | GTF headers. Major-version error. |
| A6 | 2.5 | "GFFCompare v0.12.6" | **0.12.10** | conda env |
| A7 | 2.6 | "DESeq2 v1.46 in R v4.4" | **1.50.2**, R **4.5.3** | `sessionInfo()` |
| A8 | 2.7 | "BLASTx" (version given in v1 as 2.15) | **2.17.0+** | `blastx -version` |
| A9 | Abstract, 3.3, 5 | "2,354" novel drought-upregulated | **2,422** | `results_v2/de/drought_upregulated_novel_genes_v2.tsv`. 2,125 retained, 229 lost, 297 gained. |
| A10 | 3.3 | "adjusted p-values as low as 6.73×10⁻⁶⁶" | **1.37×10⁻³⁷** | The original's precision was an artefact of inflated counts. |
| A11 | 3.3, 3.7 | Table 2 padj column, all rows | see `results_v2/de/` | All padj values change by 15–30 orders of magnitude. |
| A12 | 3.4 | "Only 10 transcripts matched known proteins" | **860** | C1 |
| A13 | Table 1 | "Mean | | **21,572,065**" | **21,571,998** | The six values sum to 129,431,990. Trivial, but it will not reproduce. |
| A14 | 3.3 | "Expression fold changes ranged from 3-fold to over 22-fold among the top candidates" | upper bound correct (2^4.46 = 22.0); lower bound unsupported — smallest in Table 2 is log₂FC 2.06 = **4.2-fold** | `candidate_genes_final.tsv` |

**Table 2 must be regenerated in full** from `results_v2/annotation/candidate_genes_v2_annotated.tsv`. Beyond the tier and annotation corrections in C3/B1, the membership changes: **only 33 of the top 50 by padj are shared** between analyses. `MSTRG.36758.1` — the transcript whose reclassification resolved the Eleusine-specific candidate count — is no longer top-50 at all.

---

# CLASS D — checked and confirmed correct

Do not change these. Several were previously flagged as uncertain and are now settled.

| # | § | Claim | Status |
|---|---|---|---|
| D1 | Abstract, 3.2 | 21,864 novel intergenic transcripts, class code "u" | **Confirmed** — `novel_genes.gtf`, 21,864 records |
| D2 | Abstract, 2.6 | Thresholds padj < 0.05, log₂FC ≥ 1.5, BH, Wald | **Confirmed** — min observed log2FC 1.50092 |
| D3 | 2.2 | GCA_032690845.1, *Eleusine_coracana_v1.0*, ~1.1 Gb | **Confirmed** — `annotation.gff3` header. (Note `config.yaml` still points at ML365 — fix before code deposition.) |
| D4 | 2.3 | Trimmomatic 0.40 and all five parameters | **Confirmed** — Snakefile |
| D5 | 2.4 | Every HISAT2 flag; MAPQ ≥ 20 | **Confirmed** — Snakefile |
| D6 | 2.7 | "release 2025_01; **574,627 sequences**" | **Confirmed** — `blastdbcmd -info`: 574,627 sequences, 208,482,574 residues. (Release label itself still unverified.) |
| D7 | 2.8 | TransDecoder 5.7.1, min ORF 100 aa, `--single_best_only`, top 50 by padj | **Confirmed** — history lines 399, 403 |
| D8 | 2.10 | Snakemake v9.19 | **Confirmed** — 9.19.0 |
| D9 | **Table 1, all 14 values** | read pairs and alignment rates | **Confirmed** — every value matches the HISAT2 summaries exactly; mean rate 92.05% ✓ |
| D10 | 3.6, Table 3 | 44 of 50 (88%) yielded ORFs; the six named no-ORF transcripts | **Confirmed** — `top50_clean.pep` has 44 records; the six absent IDs match |
| D11 | 3.7 | MSTRG.31255.1 signal peptide | **Confirmed** — Phobius 1–32, SignalP_EUK 1–28 |
| D12 | Data Availability | InterProScan job ID | **Confirmed** — MD5-matched |

**MSTRG.31255.1 is the claim that survives everything.** log₂FC 4.434 (was 4.456 — a 0.5% change), padj 1.56×10⁻³², rank 4 within the novel set (was 3), apeglm shifts it by 1.2%. Stable under the unpaired model, the paired model and apeglm. **No Swiss-Prot hit even with the corrected join** — genuinely no homolog at E ≤ 1e-5, consistent with its ColabFold MSA, in which every UniProt-derived row is an unreviewed TrEMBL entry absent from Swiss-Prot. Single-exon, so unaffected by the unspliced-extraction defect; ORF verified complete with a real start and stop; the same 104 aa string appears in the peptide FASTA, the InterProScan submission and the MSA. If the paper needs one candidate to carry it, this is the one.

---

## One claim that must be **corrected in the opposite direction**

**§3.7 on MSTRG.31255.1:**

> "Multiple orthogonal algorithms (Phobius, SignalP-EUK, TMHMM) consistently identified a signal peptide and transmembrane helix, classifying this protein as secreted or membrane-associated."

The algorithms are not orthogonal here and do not agree. SignalP-EUK's own verdict is `SignalP-noTM` — it explicitly calls *no* transmembrane region. Phobius annotates residues 33–104 `NON_CYTOPLASMIC_DOMAIN` — the entire mature protein extracellular, no TM. TMHMM's "TMhelix 7–29" lies inside the signal peptide (Phobius H-region 12–23, SignalP cleavage at 28) — the standard TMHMM/signal-peptide confusion. The only TM-positive call is `SignalP_GRAM_POSITIVE → SignalP-TM`, a **bacterial** model applied to a plant protein.

**"Secreted" is supported. "or membrane-associated" must be deleted.** Doing so strengthens the claim rather than weakening it.

**Additional evidence now available and not in the manuscript:** the ColabFold MSA holds 32 aligned rows representing **27 distinct sequences** (5 rows are exact duplicates of another row). 27 rows carry UniProt/UniRef accessions spanning **seven grass genera and twelve species in three subfamilies** — *Oryza* (6 species), *Leersia*, *Setaria*, *Dichanthelium*, *Sorghum*, *Zea*, *Arundo*; the remaining 5 rows are metagenomic or environmental with no taxonomy. Best E = 7.3e-31, all sharing a conserved C-terminal cysteine-rich module. **None is *Eleusine*; none is Chloridoideae. Only 2 of the 32 rows carry any functional product name** (both "RBR-type E3 ubiquitin transferase", *O. meridionalis*, and both are spurious segment matches within long multidomain proteins); 23 are "Uncharacterized protein", 2 are obsolete entries whose product name is no longer retrievable, and 5 are unannotated metagenomic sequences. **Every UniProt-derived row is unreviewed TrEMBL and none is in Swiss-Prot** — which is exactly why Swiss-Prot BLASTx finds nothing. The full per-row table is deposited at `structures/MSTRG_31255_1/MSA_composition.tsv`. This supports "**a small secreted cysteine-rich protein family conserved across the grasses and uncharacterised in all of them**" — a defensible and interesting claim. It does **not** support §4.3's "finger millet-specific secreted drought-protective protein". The AlphaFold model is low-confidence (mean pLDDT 59.95, pTM 0.395, MSA depth 34, only residues ~66–104 above 70) and should be described as evidence for a disulfide-stabilised C-terminal module and nothing more.

---

# CLASS E — not fixable by re-analysis; belongs in Limitations

| # | Issue | Detail |
|---|---|---|
| **E1** | **Treatment is confounded with plant age** | **No time-matched well-watered control was sampled at day seven**; controls were taken at the start and drought samples after 7 days of withheld water. Every "drought-responsive" transcript is equally consistent with being development-responsive over a 7-day window. Detailed environmental information for the growth period — watering amount and timing, temperature — was not retained. **This is the single largest constraint on the paper's central claim and should shape the framing, not sit in a limitations list.** |
| **E2** | **Pairing not established; libraries treated as independent** | Whether control and drought libraries derive from the same individual plants cannot be determined from either the data or the surviving experimental records — the original laboratory notes no longer exist, and a surviving sample-name table using matched replicate numbers with a `_D` suffix suggests an intended correspondence but confirms nothing. Library-name suffixes do not encode plant identity: all six possible control↔drought pairings absorb 49.1–51.0% of within-condition variance, indistinguishable, and the suffix-inferred pairing is not the best. The pairing is not sufficiently documented to treat the design as confirmed repeated measures, so `~ condition`, which treats the six libraries as independent samples, is the appropriate choice. Replication within each condition is biological — the three libraries per group come from separate plants — though the archive metadata does not record this. |
| **E3** | **Biological replication, undeclared in the archive** | The three libraries per condition were prepared from separate plants, so the replication is biological rather than technical, but the archive does not record this: all 18 runs of PRJDB5606 sit under one BioSample, `SAMD00076255`. Study title: *"Finger millet genome assembly."* The libraries were generated primarily to support genome annotation, not as a designed drought experiment; no growth protocol, severity, or timepoint is recorded, and detailed environmental information was not retained. The plants derive from highly inbred seed (GKVK Bangalore, originally ICRISAT). |
| **E4** | **Extreme dispersion** | asymptDisp = 0.786 ⇒ ~89% CV between replicates at high expression, 20–80× typical for controlled plant RNA-seq. The replicates are biological, not technical, so this is genuine between-plant variation in material not collected under a controlled experimental protocol. Genetic heterogeneity is largely excluded, since the plants derive from highly inbred seed — which makes the magnitude more notable rather than less. **Do not quote p-values to more than an order of magnitude.** |
| **E5** | **All extracted sequences are unspliced** | `novel_genes.gtf` has zero exon records and the top-50 extraction ran without `-split`, so every downstream sequence carries its introns. 47 of the top 50 candidates are multi-exon. Affects ORF prediction, domain annotation and the synteny screen. **Does not affect the DE analysis**, which was computed from `merged_assembly.gtf` and is exon-aware. MSTRG.31255.1 and MSTRG.20738.1 are single-exon and unaffected. |

**One favourable finding for E-class concerns.** The detection asymmetry — drought libraries detect 74k–79k transcripts vs 56k–62k in control — is **not** a sequencing-depth artefact. A depth-matched pair (DRR095905 at 21,011,330 vs DRR095909 at 20,994,628, 0.08% apart) differs by 31.8% in detection, and 96.4% of the 1,278 zero-in-all-controls transcripts are detected in DRR095909 alone, with a median 231 fragments and none below 20. Whether it reflects genuine transcriptional activation or a library-preparation difference between the two collection dates cannot be determined — but depth is excluded.

---

# Suggested order of work

1. **C1** — rewrite Abstract, §3.4, §4.2, §5 around 63.5%. Everything else is downstream of this.
2. **C3 + B1** — regenerate Table 2 from the corrected annotation; remove or defend the two retrotransposons; drop the ABA-receptor interpretation.
3. **C2** — rebuild Tier 2 by curation; rewrite §2.9 to describe what was actually done.
4. **B2** — FAB1D. Re-derive the ORF from a spliced transcript first; the domain claim is provisional until then.
5. **B3** — recompute or bound every fold change for zero-control transcripts, starting with the 730-fold figure.
6. **B4 + Class A** — Methods rewrite and the 14 numeric swaps.
7. **E1** — decide how to frame the age confound. This is an editorial decision, not a computational one.

---

## Source files

```
results_v2/DE_COMPARISON.md                                     full reconciliation
results_v2/de/all_de_results_v2.tsv                             83,195 transcripts
results_v2/de/drought_upregulated_novel_genes_v2.tsv            2,422
results_v2/de/paired_vs_unpaired.txt                            E2
results_v2/annotation/candidate_genes_v2_annotated.tsv          2,422, clean join
results_v2/annotation/candidate_genes_original_reannotated.tsv  2,354, clean join
results_v2/annotation/novel_transcripts_best_hit.tsv            all 21,864
results_v2/blast/blast_results_v2.txt                           51,468 hits
results_v2/figures/                                             dispersion, PCA, MA, distances, log2FC scatter
scripts/de_analysis_v2.R, de_analysis_v2_paired.R, rebuild_annotation_v2.py
```

Nothing under `results/` was modified at any point. Neither preprint has been edited.
