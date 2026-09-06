# VERIFICATION.md — pre-publication check of the deposition package

**Date:** 28 August 2026
**Scope:** every file in `/mnt/d/finger_millet_zenodo/`
**Method:** read-only. No file was modified, moved or deleted. This document is the only addition.

---

## Verdict

The package is **internally sound but not publication-ready.** File integrity is perfect: 142 files, none empty, none corrupt, every copy byte-identical to its source, and every structural metric recomputes exactly. What blocks publication is a set of **documentation defects** — chiefly a README that flatly contradicts the package contents, and the fact that the deposited result tables are the ones produced by the defective analysis, with no corrected versions included.

**Nine issues would embarrass you if a reviewer found them.** They are listed first.

---

# PART 1 — Issues that would embarrass you

## 1.1 README states the structures were deleted. They are in the package. ⛔ BLOCKING

`README.md` lines 112–113:

> **No protein structures are retained.** All ColabFold outputs were deleted before this package was assembled. No PDB, MSA, or confidence-score files exist for any candidate.

`structures/` contains **95 files** — 5 relaxed PDBs, 25 unrelaxed PDBs, 25 score JSONs, 5 PAE JSONs, 5 `.a3m` MSAs, 5 `config.json`, 5 `log.txt`, 5 `cite.bibtex`, 15 PNGs. `docs/MANIFEST.md` §4a and §8.3 correctly document them and explicitly retract the deletion claim. **The README was never updated.**

A reviewer reads the README first. This is the single most damaging item in the package.

Related: the README's "Repository structure" block (lines 78–85) lists five directories and **omits `structures/` entirely**, as well as `README.md` and `CITATION.cff`.

## 1.2 "Nine grass genera" — it is seven ⛔

`README.md` lines 24–25:

> multiple sequence alignment identifies 32 homologs across nine grass
> genera (Oryzoideae, Panicoideae, Arundinoideae)

Recomputed from `structures/MSTRG_31255_1/…932c3.a3m`, with organisms resolved against UniProt:

**7 genera** — *Arundo*, *Dichanthelium*, *Leersia*, *Oryza*, *Setaria*, *Sorghum*, *Zea*
**12 species** — including six *Oryza* (*barthii*, *brachyantha*, *glaberrima*, *meridionalis*, *punctata*, *rufipogon*)

The three named subfamilies are correct. **This is my error, carried into the README and into `results_v2/MANUSCRIPT_CORRECTIONS.md`. Both need correcting to "seven grass genera (12 species)".**

## 1.3 "32 homologs" counts alignment rows, not distinct sequences ⛔

The `.a3m` holds 34 records: 2 copies of the query and 32 aligned sequences. Of those 32, **five are exact duplicates of another row**:

```
K4A2R8      == UniRef100_A0A368Q1M5
A0A0D9XDT2  == UniRef100_A0A0D9XDT2
A0A0E0ES30  == UniRef100_A0A0E0ES30
A0A0E0M128  == UniRef100_A0A0E0M128
9712|scaffold142863_1|+2|11 == MGYP001059640954
```

**27 distinct sequences, not 32.** Say "32 alignment rows representing 27 distinct sequences" or simply "27 homologs". The same overcount is in `MANUSCRIPT_CORRECTIONS.md`.

## 1.4 `analyze_structures.cxc` cannot have produced the deposited figures ⛔

The script opens four PDBs, all named `..._relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb`. The actual rank_001 model differs per candidate:

| Candidate | script expects | actually exists |
|---|---|---|
| MSTRG_4687_1 | `model_1` | **`model_5`** |
| MSTRG_45757_2 | `model_1` | `model_1` ✓ |
| MSTRG_6647_1 | `model_1` | **`model_3`** |
| MSTRG_45758_1 | `model_1` | **`model_3`** |

**Three of the four `open` statements reference files that do not exist.** The script as deposited would fail on load. Either an earlier ColabFold run with different rankings existed, or the working version was hand-edited and not retained. Either way, `figures/image1`–`image6.png` have **no verifiable generating script**.

This also **falsifies a MANIFEST claim.** `docs/MANIFEST.md` §2 says the `.cxc` "Documents the ColabFold model filenames … which are the only surviving record of the prediction settings." They are not the record, they are wrong, and `structures/*/config.json` is now the actual record. MANIFEST §4a already warns "do not assume `model_1`" — §2 contradicts it.

Note also that **MSTRG.31255.1 is not among the four structures the script opens**, so none of the six figures can depict the lead candidate.

## 1.5 The package deposits the defective results and none of the corrections ⛔ BLOCKING

Nothing from the `results_v2/` re-analysis is in the package. Searched: no occurrence of `63.5`, `2,422`, `2422` anywhere in `README.md`, `docs/MANIFEST.md` or `CITATION.cff`.

The deposit therefore presents as its headline result:

- `results/drought_upregulated_novel_genes.tsv` — 2,354 transcripts, produced by DESeq2 fed `round(cov * 100)`
- `results/all_de_results.tsv` — the same
- no annotation table at all, so the corrected **63.5% no-homology** figure appears nowhere

The README's limitations section (lines 151–156) does document the `cov * 100` defect honestly — but it documents it as a caveat on tables that are still presented as the result. A reader has no corrected numbers to use. **The BLASTx key-mismatch bug and the substring `STRESS_WORDS` bug are not mentioned at all.**

## 1.6 Personal email address in a deposited script ⚠

`scripts/reconstructed/heroGene03_ncbi_blastp_web_submit_v2.py`:

```python
'email': 'joshua@research.com'
```

Supplied to the EBI REST API, which requires a contact address. The domain looks like a placeholder rather than a real mailbox, but it is the only email in the package and it will be indexed. It sits inside a **verbatim recovery**, so removing it breaks the verbatim guarantee — see §5 for options.

## 1.7 Username and machine name in five files ⚠

`joshua @ Joash-Joshua` appears in:

```
workflow/Snakefile        (header comment, and echoed into tool_versions.txt at run time)
workflow/config.yaml      (header comment)
workflow/setup.sh         (header comment)
scripts/de_analysis.R     (header comment, and cat() to stdout at run time)
scripts/merge_results.py  (docstring, and log.info() at run time)
```

`Joash-Joshua` is a machine hostname. Two of these are not merely comments — they are printed into logs at run time.

## 1.8 Absolute paths that will not resolve on any other machine ⚠

| File | Path |
|---|---|
| `workflow/Snakefile` | `/home/joshua/miniconda3/envs/finger_millet/bin`, `/home/joshua/miniconda3/envs/snakemake/bin` (prepended to `PATH`); `/mnt/d/finger_millet_project` |
| `workflow/setup.sh` | `source /home/joshua/miniconda3/etc/profile.d/conda.sh`; `PROJECT="/mnt/d/finger_millet_project"` |
| `scripts/run_foldseek.sh` | `WIN_DOWNLOADS="/mnt/c/Users/Joshua/Downloads"`, `OUT_DIR="/mnt/c/Users/Joshua/Desktop/foldseek_results"` |
| `scripts/run_foldseek_webapi.sh` | same two |
| `scripts/analyze_structures.cxc` | **14 hard-coded `C:\Users\Joshua\…` paths** — 4 `open`, 9 `save`, 4 `movie encode` |
| `scripts/reconstructed/*.py` (20 files) | `/mnt/d/finger_millet_project` in the provenance header only |

The Snakefile's `PATH` manipulation is the most consequential: it silently prepends a non-existent directory on any other machine.

MANIFEST §4a documents the Foldseek/ChimeraX path staleness and the relocation to `D:\Downloads D\`. The Snakefile and setup.sh paths are **not** documented anywhere.

## 1.9 `defensins.fasta` size is misstated ⚠

`docs/MANIFEST.md` §3.1 claims **355 B**. The file is **301 B**. Record count (2) and both sequence lengths (104 aa, 133 aa) are correct, and the MSTRG.31255.1 sequence is byte-identical to the copy in `top50_clean.pep` as claimed.

---

# PART 2 — File integrity

## 2.1 Basic checks — all pass

| Check | Result |
|---|---|
| Files on disk | **142** (MANIFEST claims 142 ✓) |
| Empty files | **0** |
| Unreadable files | **0** |
| Total size | 63,389,152 B = **60.5 MB** (MANIFEST claims 61 MB — acceptable) |
| Directories | **13** excluding root (MANIFEST §9 claims 12 — off by one) |

## 2.2 Format validation — all pass

Every file was parsed as the format its extension claims.

| Type | n | Check applied | Result |
|---|---|---|---|
| `.json` | 35 | `json.load()` | all parse |
| `.pdb` | 30 | ATOM records present + `END` terminator | all valid |
| `.png` | 21 | PNG magic + `IEND` chunk present | none truncated |
| `.py` | 21 | `ast.parse()` | all parse |
| `.tsv` | 5 | consistent column count across all rows | none ragged |
| `.a3m` | 5 | `#`-header + ≥1 record | all valid |
| `.pep` / `.fasta` | 3 | ≥1 record, no consecutive headers | all valid |
| `.sh` | 3 | `bash -n` | all pass |
| `.R` | 1 | `parse()` | passes |
| `.yaml` | 1 | `yaml.safe_load()` | valid |

`workflow/Snakefile` does not parse as plain Python — expected, it is Snakemake DSL.

## 2.3 Byte-identity against sources — all pass

`cmp` against every claimed source:

```
workflow/Snakefile ......................... identical
workflow/setup.sh .......................... identical
workflow/config.yaml ....................... DIFFERS (3,013 vs 2,078 B) — INTENDED, see MANIFEST §6
scripts/de_analysis.R ...................... identical
scripts/merge_results.py ................... identical (to both project and Downloads D copies)
scripts/run_foldseek.sh .................... identical
scripts/run_foldseek_webapi.sh ............. identical
scripts/analyze_structures.cxc ............. identical
results/all_de_results.tsv ................. identical
results/drought_upregulated_novel_genes.tsv  identical
results/synteny_3species.tsv ............... identical
results/novel_vs_known_correlation.tsv ..... identical
results/top50_transcripts.fa.transdecoder.pep identical
results/iprscan5-…-p1m.tsv ................. identical (to both Desktop and project copies)
results/sequences/top50_clean.pep .......... identical
figures/image1–6.png ....................... identical (6/6)
structures/  95 files across 5 candidates .. identical (0 mismatches)
```

**One deliberate difference only.** `workflow/config.yaml` is the modified copy documented in MANIFEST §6. The original at `/mnt/d/finger_millet_project/config.yaml` remains 2,078 B, MD5 `ecbd2fb66cd066214aa0b0598c652a00` — re-verified.

## 2.4 Reconstructed scripts still match shell history

All 20 files in `scripts/reconstructed/` were re-checked against the byte ranges named in their own headers:

**20/20 byte-identical.** `~/.bash_history` has since grown to 1,840 lines (the extraction used ranges up to 1730), but lines 1–1730 are unchanged, so every recorded range still resolves correctly.

## 2.5 MANIFEST completeness — both directions

**Files present but not named in MANIFEST: 102.**

Of these, **100 are structure files** that MANIFEST §4a describes by composition ("19 files each: 1 relaxed rank_001 PDB · 5 unrelaxed PDBs · …") rather than by name. That is a defensible choice for 95 machine-named files, and the composition statement is accurate. The remaining two are **`README.md` and `CITATION.cff`, which appear nowhere in the MANIFEST at all** — MANIFEST §5 lists `docs/` as containing only `MANIFEST.md`.

**Files MANIFEST names that are absent: 0 genuine.** Twelve apparent hits were checked individually; all are either glob patterns (`scores_rank_*.json`), extension fragments, or deliberate references to files documented as *not* included (`interproscan_results.tsv` = the project's copy, `synteny_combined.tsv` = superseded, `MSTRG_4687_1_pLDDT.png` etc. = lost ChimeraX outputs).

---

# PART 3 — Quantitative claims recomputed

Every figure below was recomputed from the deposited files.

## 3.1 Reproduce exactly

| Claim | Source | Claimed | Recomputed |
|---|---|---|---|
| `all_de_results.tsv` lines | MANIFEST §3 | 88,337 | **88,337** ✓ |
| `drought_upregulated_novel_genes.tsv` lines | §3 | 2,355 | **2,355** ✓ |
| Novel drought-up transcripts | §3, README | 2,354 | **2,354** ✓ |
| `synteny_3species.tsv` lines | §3 | 11 | **11** ✓ |
| `novel_vs_known_correlation.tsv` lines | §3 | 11 | **11** ✓ |
| InterProScan TSV lines | §3 | 254 | **254** ✓ |
| InterProScan MD5 | §3 | `4170ff44…` | **`4170ff449f6a5db3645ff6cfa295efaa`** ✓ |
| Proteins annotated / member DBs | §3 | 37 / 18 | **37 / 18** ✓ |
| TransDecoder peptide records | §3 | 44 | **44** ✓ |
| `top50_clean.pep` records | §3.1 | 44 | **44** ✓ |
| `defensins.fasta` records | §3.1 | 2 | **2** ✓ |
| Snakefile / config.yaml / setup.sh lines | §1 | 468 / 87 / 112 | **468 / 87 / 112** ✓ |
| de_analysis.R / merge_results.py lines | §2 | 253 / 92 | **253 / 92** ✓ |
| run_foldseek(.sh/_webapi.sh) / .cxc lines | §2 | 172 / 223 / 190 | **172 / 223 / 190** ✓ |
| Reconstructed script count | §7.1 | 20 | **20** ✓ |
| Reconstructed total size | §7.1 | 92 KB | **92 KB** ✓ |
| Minimum log2FC in the 2,354 | §6.2 | 1.5009 | **1.50092** ✓ |
| Count at log2FC > 2 | §6.2 | 2,081 | **2,081** ✓ |
| MSTRG.31255.1 correlation | §3 | r = 0.9925 (FPS), 0.9896 (PP2A) | **0.9925 / 0.9896** ✓ |
| Synteny classification | §3 | 4 / 1 / 1 / 4 | **4 Eleusine-specific, 1 Panicoideae, 1 partial, 4 pan-grass** ✓ |
| Assembly: sequences / bp / N50 | README | 532 / 1,111,714,373 / 61,270,980 | **532 / 1,111,714,373 / 61,270,980** ✓ |
| 18 pseudomolecules + 514 scaffolds | README | 18 / 514 | **18 / 514** ✓ |
| MSTRG.31255.1 in deposited table | — | — | **log2FC 4.4558, padj 8.07e-57, baseMean 11,372.9, rank 3** ✓ matches Table 2 of the preprints |
| Structure metrics, all 5 candidates | §4a | see below | **all exact** ✓ |

Structure metrics recomputed from the deposited `scores_rank_001*.json` and `.a3m`:

| Candidate | Length | Mean pLDDT | pTM | MSA depth |
|---|---|---|---|---|
| MSTRG_31255_1 | 104 ✓ | **59.95** ✓ | 0.390 ✓ | **34** ✓ |
| MSTRG_4687_1 | 342 ✓ | 86.20 ✓ | 0.440 ✓ | 14,714 ✓ |
| MSTRG_45757_2 | 197 ✓ | 46.51 ✓ | 0.220 ✓ | **2** ✓ |
| MSTRG_45758_1 | 526 ✓ | 83.82 ✓ | 0.590 ✓ | 17,808 ✓ |
| MSTRG_6647_1 | 421 ✓ | 76.59 ✓ | 0.770 ✓ | 334 ✓ |

Per-candidate directory sizes (1.6 / 13 / 3.0 / 23 / 8.6 MB), `structures/` total (47.8 MB vs 49 claimed) and core-only total (38.9 MB vs 38.8 claimed) all agree within rounding.

## 3.2 Do not reproduce

| Claim | Location | Claimed | Actual |
|---|---|---|---|
| `defensins.fasta` size | MANIFEST §3.1 | 355 B | **301 B** |
| Grass genera in the MSA | README | nine | **seven** (12 species) |
| Homologs in the MSA | README | 32 | **32 rows, 27 distinct sequences** |
| Directory count | MANIFEST §9 | 12 | **13** excluding root |

## 3.3 Cannot be checked — the figure is not in the package

**The 63.5% no-homology figure, the corrected tier distribution, and the 2,422-transcript re-analysis do not appear anywhere in the package.** See §1.5.

---

# PART 4 — Scripts

## 4.1 Syntax — all pass

21 Python files (`ast.parse`), 1 R file (`parse()`), 3 shell scripts (`bash -n`), 1 YAML (`safe_load`): **all parse without error.** Syntax validity only; it is not a claim that any of them runs correctly outside its original working directory.

## 4.2 Hard-coded values

| Script | Hard-coded |
|---|---|
| `stage08b_build_promoter_bed.py` | 10 transcript IDs **and their genomic coordinates** |
| `stage10a`, `stage10d`, `stage11a`, `stage11b`, `stage11c`, `stage11d` | the 10-candidate list |
| `stage10d_pearson_correlation_vs_known_genes.py` | **complete expression matrices as Python literals** (`novel = {…}`, `known = {…}`) — its only `open()` is the output write |
| `stage08c_scan_promoter_motifs.py` | six motif strings; 1,000 bp window |
| `heroGene01/02/03` | the MSTRG.31255.1 peptide sequence |

**MANIFEST §7.2's statement that `stage10d` reads no input files is correct** — verified directly. Re-running it reproduces the published correlations but does not re-derive them from count data.

The 10-candidate list should be read from `top50_ids.txt` and the coordinates from `novel_genes.gtf`. It is not, in any of the seven scripts.

## 4.3 References to files not in the package

Every reconstructed script and `de_analysis.R` reads inputs that are **not deposited**:

```
candidate_genes_final.tsv                  results/novel_genes/novel_genes.gtf
results/novel_genes/novel_transcripts.fa   results/novel_genes/blast_results.txt
results/novel_genes/top50_ids.txt          results/transdecoder/top50.bed
results/transdecoder/top50_transcripts.fa  results/assembled/merged_assembly.gtf
results/counts/*.gtf                       results/synteny/vs_{sorghum,rice,foxtail}.txt
results/synteny/synteny_summary.tsv        results/promoter_analysis/{promoters.bed,promoters.fa,abre_results.tsv}
results/coexpression/{expression_matrix,correlation_matrix}.tsv
results/known_drought_genes/known_gene_expression.tsv
```

MANIFEST §8.1 acknowledges the omissions. The practical consequence is quantified in Part 6.

---

# PART 5 — Privacy

## 5.1 Clean

- **No API keys, tokens, passwords or credentials.** Scanned for `api_key`, `secret`, `token`, `password`, `Bearer`, `Authorization:`, `ghp_`, `sk-…`, `AKIA…` across all text files. Zero hits.
- **No IP addresses.** All 19 URLs point at legitimate public services: NCBI BLAST, EBI, Foldseek, ORCID, NCBI FTP, UniProt FTP, Zenodo, MMseqs, ColabFold API, DOI, Creative Commons.
- **No unrelated shell-history content.** All 20 reconstructed scripts match their declared history ranges byte-for-byte; nothing outside those ranges leaked in. The scan of `/mnt/d/Downloads D/` shows unrelated material (coursework, other projects, personal files) — **none of it is in the package.**

## 5.2 To decide

| Item | Where | Note |
|---|---|---|
| `joshua@research.com` | `scripts/reconstructed/heroGene03_…_v2.py` | Only email in the package. Inside a verbatim recovery. |
| `joshua @ Joash-Joshua` | Snakefile, config.yaml, setup.sh, de_analysis.R, merge_results.py | Username + hostname. Printed to logs at run time in two of them. |
| `/home/joshua/…`, `/mnt/d/…`, `C:\Users\Joshua\…` | 6 files + 20 headers | See §1.8 |

**Recommendation, for your decision — I have changed nothing.** The genuine source files (`Snakefile`, `config.yaml`, `setup.sh`, `de_analysis.R`, `merge_results.py`) can be sanitised freely; they are yours and the change would be documented in the MANIFEST. The `reconstructed/` scripts should **not** be edited — their entire evidentiary value is that they are verbatim. If the email must go, the honest options are (a) leave it and note it in the MANIFEST as an artefact of the original execution, or (b) redact it in place with a visible marker such as `'email': '[REDACTED]'` and record the redaction in the header, which breaks byte-verbatim status and must be stated. Option (a) is defensible; the domain is a placeholder, not a mailbox.

---

# PART 6 — Reproducibility gaps

For each deposited result, whether a deposited script can regenerate it.

| Deposited result | Producing script | In package? | Inputs present? | Regenerable? |
|---|---|---|---|---|
| `results/all_de_results.tsv` | `scripts/de_analysis.R` | ✅ | ❌ needs `results/counts/*.gtf`, `novel_genes.gtf` | **No** |
| `results/drought_upregulated_novel_genes.tsv` | `scripts/de_analysis.R` | ✅ | ❌ same | **No** |
| `results/synteny_3species.tsv` | `stage11d_classify_three_species.py` | ✅ | ❌ needs `vs_{sorghum,rice,foxtail}.txt` | **No** |
| `results/novel_vs_known_correlation.tsv` | `stage10d_pearson_correlation_vs_known_genes.py` | ✅ | ✅ (hard-coded literals) | **Yes — but it replays values, it does not re-derive them** |
| `results/sequences/top50_clean.pep` | `stage06e_clean_peptide_fasta.py` | ✅ | ✅ `top50_transcripts.fa.transdecoder.pep` is deposited | **Yes** (script expects to run from `results/transdecoder/`) |
| `results/top50_transcripts.fa.transdecoder.pep` | TransDecoder CLI one-liner | ❌ not a script | ❌ `top50_transcripts.fa` absent | **No** |
| `results/iprscan5-…-p1m.tsv` | EBI REST web service | ❌ | ✅ query sequences deposited | **No** — external service, version unrecorded |
| `results/sequences/defensins.fasta` | data heredoc | — | — | **N/A** — it is the artefact |
| `figures/image1–6.png` | `scripts/analyze_structures.cxc` | ✅ | ❌ **3 of 4 `open` paths reference non-existent models** (§1.4) | **No** |
| `structures/*/` | ColabFold web service | ❌ | ❌ query `.csv` not deposited | **No** — but `config.json` records every parameter |

**Two of ten deposited results can be regenerated from deposited code, and one of those only replays hard-coded numbers.**

Not deposited but needed to close most of these: `results/counts/*.gtf` (~600 MB), `results/novel_genes/novel_genes.gtf` (3.6 MB), `results/novel_genes/blast_results.txt` (10.3 MB), `results/synteny/vs_*.txt` (small), `results/transdecoder/top50_transcripts.fa`, `results/final_report/candidate_genes_final.tsv`. **All except the count GTFs are small enough to include and would close six of the eight gaps.**

The ColabFold query `.csv` exists in each source folder at `/mnt/d/Downloads D/` and was not deposited; adding it (a few hundred bytes each) would make the structure predictions re-submittable.

---

# PART 7 — Recommended actions, in order

Nothing below has been done. All require your approval.

**Blocking**

1. **Rewrite `README.md` lines 112–113.** The structures exist and are deposited. Add `structures/` to the repository-structure block.
2. **Decide what the deposit is.** Either add the `results_v2/` corrected tables and state the 63.5% figure, or state prominently in the README that these are the original uncorrected results and point to where the corrections live. As it stands the package silently presents superseded numbers.

**Factual corrections**

3. README: "nine grass genera" → **"seven grass genera (12 species)"**; "32 homologs" → **"32 alignment rows representing 27 distinct sequences"**.
4. MANIFEST §3.1: `defensins.fasta` **301 B**, not 355 B.
5. MANIFEST §2: remove the claim that `analyze_structures.cxc` documents the prediction settings; it names `model_1` for all four candidates and is wrong for three. Point to `structures/*/config.json` instead.
6. MANIFEST §9: **13 directories**, not 12.
7. MANIFEST §5: list `README.md` and `CITATION.cff`.

**Documentation**

8. Add a MANIFEST note that `figures/image1–6.png` have no working generating script, and that none of them can depict MSTRG.31255.1 (the `.cxc` never opens it).
9. Document the `Snakefile` and `setup.sh` absolute paths, which §4a currently covers only for the Foldseek and ChimeraX scripts.
10. Bump `CITATION.cff` `version` and `date-released`. It currently reads 1.0.0 / 2026-08-19. Note also that its abstract advertises "promoter motif scanning, co-expression analysis" whose result tables are not deposited.

**Optional but cheap**

11. Deposit `novel_genes.gtf`, `blast_results.txt`, `vs_*.txt`, `top50_transcripts.fa`, `candidate_genes_final.tsv` and the five ColabFold query `.csv` files — under 20 MB total, closes six of eight reproducibility gaps.
12. Decide on §5.2 (email, username, hostname).

---

## Method note

Checks were performed with `cmp` (byte-identity), `file` (MIME type), `json.load`, `ast.parse`, `bash -n`, `R parse()`, `yaml.safe_load`, PNG magic/`IEND` inspection, PDB `ATOM`/`END` inspection, and direct recomputation from the deposited tables and JSON. Organism assignments for the MSA were resolved against the UniProt REST API; two deleted accessions (`A0A368Q1M5`, `A0A0A9C887`) were recovered from UniSave entry-name history as `_SETIT` and `_ARUDO`.

No file in `/mnt/d/finger_millet_zenodo/` or `/mnt/d/finger_millet_project/` was modified, moved or deleted during this verification. This document is the only file added.

---
---

# SECOND VERIFICATION — 28 August 2026, after rectification

The twelve issues listed in Part 1 and Part 7 above have been addressed. This section
re-runs **every check in this document** against the rectified package and reports the
result of each. It is appended rather than replacing the first pass: the original audit is
the reason the rectification happened, and deleting it would erase that record.

**Result: 24 checks pass, 0 fail, 4 notes.** All four notes are deliberate retentions or
false positives, itemised in §2.6.

## 2.0 What changed

| Issue (first pass) | Status |
|---|---|
| **1.1** README said structures were deleted | **FIXED** — README rewritten; `structures/` documented, 101 files |
| **1.2** "nine grass genera" | **FIXED** — seven genera, twelve species, recomputed from the `.a3m` |
| **1.3** "32 homologs" | **FIXED** — 32 aligned rows, **27 distinct** sequences, 5 duplicate pairs named |
| **1.4** `analyze_structures.cxc` cannot produce the figures | **FIXED** — six figures withdrawn; script retained with a 50-line defect header |
| **1.5** Corrected analysis absent | **FIXED** — `results_v2/` added (32 files), `figures_v2/`, `logs/`, three v2 scripts, two docs |
| **1.6** Email in a deposited script | **RETAINED, DOCUMENTED** — verbatim artefact; see §2.6 |
| **1.7** Username in five files | **FIXED** for all genuine source files; retained only in `analyze_structures.cxc` |
| **1.8** Absolute paths | **FIXED** — eleven files now use documented environment variables |
| **1.9** `defensins.fasta` size misstated | **FIXED** — MANIFEST regenerated from the filesystem, so all sizes are derived |
| **7.10** CITATION.cff stale | **FIXED** — v2.0.0, dual licence, three references, abstract rewritten |
| **7.11** Reproducibility gaps | **PARTLY FIXED** — see §2.5 |
| **7.12** Licence | **FIXED** — dual MIT / CC BY 4.0, both full texts |

Also added since the first pass: `LICENSE`, `scripts/LICENSE`,
`scripts/reconstructed/README.md`, `results_v1/README.md`, `results_v2/README.md`,
`structures/MSTRG_31255_1/MSA_composition.tsv`, and the six reproducibility-gap files.
`figures/` was removed.

## 2.1 File integrity — PASS

| Check | Result |
|---|---|
| Files / directories | **206 files, 23 directories** |
| Empty files | **0** |
| Unreadable files | **0** |
| Format validation | **118 files parsed against their extension, 0 problems** |

Formats checked as before: JSON via `json.load`, PDB for ATOM records and an `END`
terminator, PNG for magic bytes and an `IEND` chunk, Python via `ast.parse`, TSV for
consistent column width, `.a3m` for header and records, FASTA for well-formed records.

> **One first-pass false alarm resolved.** `results_v2/de/sample_distance_matrix.tsv` was
> initially flagged as ragged: header 6 fields, data rows 7. This is R's `write.table`
> row-name convention, not corruption. The check now accepts a header exactly one field
> narrower than the data rows, and the file passes.

## 2.2 Byte-identity — PASS

**159 deposited copies compared against their sources: 0 differ, 0 sources missing.**

Three files are deliberately not byte-identical, each documented in MANIFEST §11:

1. `workflow/config.yaml` — reference URLs corrected (§11.1)
2. `scripts/analyze_structures.cxc` — 50-line defect header prepended (§11.2). **The
   5,709-byte body beneath the header was verified byte-identical to the original.**
3. Eleven files sanitised for deposition (§11.3)

`/mnt/d/finger_millet_project/` remains untouched — `results/` still holds 240 files.

## 2.3 MANIFEST completeness, both directions — PASS

The MANIFEST was **regenerated programmatically from the package**, so every size and
count is derived rather than typed, and it is iterated to a fixed point so its own size
and the package total are self-consistent.

| Check | Result |
|---|---|
| Filenames in MANIFEST inventory tables | **117** |
| Distinct basenames present | 190 |
| Present but not listed | **0** (88 machine-named structure files are described by composition in §9, a documented convention) |
| Listed but absent | **0** |
| MANIFEST self-count vs actual | **206 / 23 / byte total — exact match** |

## 2.4 Numbers — PASS

**19 of 19 quantitative claims in `README.md` and `CITATION.cff` recompute from deposited
files.** Nothing was carried over.

| Claim | Recomputed from |
|---|---|
| 21,864 novel transcripts | `results_v2/counts/novel_class_u_ids.txt` |
| **2,422** drought-upregulated | `results_v2/de/drought_upregulated_novel_genes_v2.tsv` |
| **1,532 (63.3%)** no homology | `results_v2/annotation/candidate_genes_v2_annotated.tsv` |
| Tiers **1,184 / 348 / 50 / 840** | same, word-boundary keyword matching |
| **203 (8.4%)** mobile-element | same, documented match pattern |
| **6,106 (27.9%)** of 21,864 with a hit | `results_v2/annotation/novel_transcripts_best_hit.tsv` |
| MSTRG.31255.1 log2FC **4.434**, padj **1.56e-32** | `drought_upregulated_novel_genes_v2.tsv` |
| pLDDT **59.95**, pTM **0.390**, MSA depth **34** | `structures/MSTRG_31255_1/*scores_rank_001*.json`, `.a3m` |
| **27 distinct** homologs, **seven** genera, **twelve** species | `.a3m` + `MSA_composition.tsv` |
| v1 table still 2,354 rows | `results_v1/drought_upregulated_novel_genes.tsv` |

> **One figure needed care.** The mobile-element count is 203 only when `LINE-1` is
> included in the match pattern: 28 rows hit `LINE-1 retrotransposable element ORF2
> protein`, which no other term matches ("retrotransposable" does not contain
> "transposon"). The pattern is now recorded in `README.md` beside the claim, and the
> figure is flagged as a lower bound.

> **A precision note on 63.5% vs 63.3%.** Both are correct and they attach to different
> denominators. The **2,422** corrected set is **63.3%** (1,532). The original **2,354**
> set, re-annotated with the same corrected join for like-for-like comparison against the
> 99.6% claim, is **63.5%** (1,494). `README.md` leads with 63.3% because that is the set
> it reports, and states 63.5% immediately below.

## 2.5 Scripts and reproducibility — PASS

| Check | Result |
|---|---|
| Python `ast.parse` | **22 files, 0 errors** |
| Shell `bash -n` | **4 files, 0 errors** |
| R `parse()` | **3 files, 0 errors** |
| YAML `safe_load` | `workflow/config.yaml`, `CITATION.cff` — both valid |
| Reconstructed scripts vs `~/.bash_history` | **20/20 byte-identical** — re-confirmed after the sanitisation of all other scripts |

**Reproducibility improved from 2 of 10 to 10 of 16 fully regenerable**, plus 2 partial.
All three v2 scripts report every input present. Newly closed: `synteny_3species.tsv`,
`top50_transcripts.fa.transdecoder.pep`, `blast_results.txt`, and the `stage06a` →
`stage06b/c/d`/`stage08a` and `stage11b` → `stage11c` chains.

**Still open, with reasons stated rather than worked around:**

- `results/counts/*_counts.gtf` (~600 MB) blocks the v1 DE tables, `results_v2/counts/*`,
  and `stage10a`/`10b`/`10c`. Too large to deposit.
- `iprscan5-…-p1m.tsv` — EBI web service, no local script, version not recorded.
- **`candidate_genes_final.tsv` provenance remains unknown.** The file is now deposited,
  but no Snakefile rule and no history line creates it, and it contains four tier strings
  where `merge_results.py` can emit only three. This is a **known break in the chain of
  custody, not an oversight**, and it is stated as such in `README.md` and MANIFEST §12.

## 2.6 Privacy — PASS with four documented notes

**Zero occurrences of the username, hostname, home directory or the original project path
in any genuine (non-reconstructed) source file.** Eleven files were sanitised and all
re-verified to parse.

Four notes, all deliberate or benign:

1. **`scripts/analyze_structures.cxc` retains 22 lines containing the username** in
   `C:\Users\Joshua\…` paths. **Deliberate**, documented in MANIFEST §11.3: those paths
   are the documentary evidence for the 5 August 2026 relocation described in §9.4, and
   the file is now explicitly a provenance artefact that does not run. What it discloses
   is a Windows account named "Joshua", where the deposit is authored under
   *Joash Joshua Ayo* with a public ORCID.
2. **One email address in the package: `joshua@research.com`**, in
   `scripts/reconstructed/heroGene03_ncbi_blastp_web_submit_v2.py`. **Deliberate** — a
   placeholder satisfying the EBI REST API's required contact field, never a working
   mailbox, inside a verbatim recovery. Explained in `scripts/reconstructed/README.md`.
3. **Three "credential pattern" hits are false positives**: `README.md` and
   `MANUSCRIPT_CORRECTIONS.md` match on *"**secret**ed"*; `VERIFICATION.md` matches on its
   own description of the scan pattern. **No API keys, tokens, passwords or credentials
   exist in the package.**
4. No IP addresses. All external URLs point to public services: NCBI, EBI, Foldseek,
   UniProt, ORCID, Zenodo, ColabFold, MMseqs, DOI, Creative Commons.

## 2.7 Cross-file consistency — PASS

Every contradiction found in the first pass was re-tested and none survives:

| Claim | Result |
|---|---|
| "No protein structures are retained" in README | **absent** |
| "nine grass genera" in README | **absent** |
| "32 homologs" in README | **absent** |
| "only surviving record of the prediction settings" in MANIFEST | **absent** |
| `figures/` directory | **absent**, withdrawal documented in MANIFEST §7 and §13.4 |
| `results_v1/README.md`, `results_v2/README.md` status markers | **present** |
| `LICENSE` contains both full texts | **yes** |
| README AI-use disclosure present, no placeholder | **yes** |

`docs/MANUSCRIPT_CORRECTIONS.md` still contains the strings "nine grass genera" and
"32 homologs" — **only inside its dated correction notice**, where they are quoted as the
figures that were wrong. That is intentional. The check distinguishes table rows (the
correction notice) from prose, and passes.

## 2.8 Remaining decisions for the author

Neither blocks deposition; both are noted so they are conscious choices.

1. **`workflow/` is under CC BY 4.0**, per the specified split. `Snakefile` and `setup.sh`
   are executable code, and Creative Commons advises against CC licences for software —
   they do not address source-vs-binary distribution, patent grants or linking. Moving
   `workflow/` (or just those two files) to MIT is a one-line change.
2. **`analyze_structures.cxc` username retention** — see §2.6 note 1. Alternatives are
   redacting to `<user>` with a note in its header, or dropping the file and relying on
   `structures/*/config.json` for the settings record.

## 2.9 Method

`cmp` and full-content comparison for byte-identity; `json.load`, `ast.parse`, `bash -n`,
`R parse()`, `yaml.safe_load`; PNG magic and `IEND` inspection; PDB `ATOM`/`END`
inspection; direct recomputation from deposited tables, JSON and the `.a3m`; regex scans
for usernames, emails and credential patterns; and byte comparison of all twenty
reconstructed scripts against `~/.bash_history`.

**No file in `/mnt/d/finger_millet_project/` was created, modified, moved or deleted at
any point.** All changes were confined to `/mnt/d/finger_millet_zenodo/`.

---
---

# THIRD VERIFICATION — 28 August 2026, after the licence split and final hygiene

Two author decisions were applied and two repository-hygiene items added. Every check from
the second verification was re-run, plus **nine new checks** covering the changes.

**Result: 33 checks pass, 0 fail, 4 notes.** The notes are unchanged from the second pass
and remain deliberate retentions or false positives (§2.6).

## 3.1 Decision 1 — licence split refined

`workflow/Snakefile` and `workflow/setup.sh` moved from CC BY 4.0 to **MIT**, on the
grounds that they are executable code and Creative Commons advises against CC licences for
software. **`workflow/config.yaml` remains under CC BY 4.0** — it is configuration data,
not code.

| Change | Verified |
|---|---|
| `LICENSE` MIT clause now names `workflow/Snakefile` and `workflow/setup.sh` | **PASS** |
| `LICENSE` CC BY clause now names `workflow/config.yaml` only, with a cross-reference | **PASS** |
| `workflow/LICENSE` created | **PASS** |
| `workflow/LICENSE` byte-identical to `scripts/LICENSE` | **PASS** |
| `README.md` licence table shows all three rows | **PASS** |
| `CITATION.cff` `message` states the split | **PASS** |
| `CITATION.cff` `license: [MIT, CC-BY-4.0]` | unchanged — still correct, both licences still apply |

The final split:

```
MIT        scripts/**  (incl. scripts/reconstructed/)
           workflow/Snakefile
           workflow/setup.sh
CC BY 4.0  everything else, incl. workflow/config.yaml
```

## 3.2 Decision 2 — `analyze_structures.cxc` left unredacted

The absolute `C:\Users\Joshua\…` paths are retained. Three lines were added to its header
recording that this is deliberate:

> These absolute paths are retained deliberately as provenance — they are the
> documentary evidence for the relocation recorded in docs/MANIFEST.md section 9.4 —
> and the account name they contain is the author's own.

| Check | Result |
|---|---|
| Header states deliberate retention and account ownership | **PASS** |
| Header length | 50 → **53 lines** |
| **Original body still byte-identical** | **PASS — 5,709 B, found by byte-exact offset search rather than a hard-coded line number** |

The verification now locates the body offset by searching for the position at which the
remainder of the file equals the original byte-for-byte, so the check cannot silently rot
if the header is edited again.

## 3.3 Repository hygiene

| Check | Result |
|---|---|
| `.gitignore` present, containing `.DS_Store` and `Thumbs.db` | **PASS** |
| **No file exceeds 100 MB** (GitHub hard limit) | **PASS — 0 over; largest is 18.7 MB** (`results_v2/counts/featurecounts_gene.txt`) |
| Files over GitHub's 50 MB warning threshold | **0** |
| Total vs Zenodo's 50 GB per-record limit | 0.15 GB |
| Symlinks / non-regular files | 0 |
| Filenames with spaces or non-ASCII characters | 0 |
| Longest path | 115 characters |

## 3.4 Everything else — re-run and unchanged

| Check | Result |
|---|---|
| Files / directories | **208 files, 23 directories** (+2: `workflow/LICENSE`, `.gitignore`) |
| Empty / unreadable files | 0 / 0 |
| Format validation | 118 files, **0 problems** |
| Byte-identity of deposited copies | **159 checked, 0 differ, 0 sources missing** |
| MANIFEST completeness, both directions | **0 unlisted, 0 absent** |
| MANIFEST self-count | **208 / 23 / 162,507,091 B — exact** |
| README + CITATION numbers recomputed | **19 / 19** |
| Python / shell / R / YAML syntax | 22 / 4 / 3 / 2 files, **0 errors** |
| Reconstructed scripts vs `~/.bash_history` | **20 / 20 byte-identical** |
| Username or hostname in genuine source files | **0** |
| Stale or contradicted claims | **0** |
| `/mnt/d/finger_millet_project/` | **untouched — 240 files, `config.yaml` md5 `ecbd2fb66cd066214aa0b0598c652a00`** |

## 3.5 Reference URLs — caveat discharged

MANIFEST §11.1 previously warned that the corrected reference URLs had never been fetched.
All three now return **HTTP 200**:

| Resource | Status | Size |
|---|---|---|
| `GCA_032690845.1_..._genomic.fna.gz` | 200 | 331.1 MB |
| `GCA_032690845.1_..._genomic.gff.gz` | 200 | 9.1 MB |
| `uniprot_sprot.fasta.gz` | 200 | 89.4 MB |

The `config.yaml` correction — repointing from GCA_002477235.1, which was never the
assembly used — is confirmed to resolve, not merely to look right.

## 3.6 One cosmetic characteristic, documented rather than changed

Four TSVs use CRLF line endings: `results_v1/final_report/candidate_genes_final.tsv`
(inherited from its unknown origin) and the three tables in `results_v2/annotation/`,
because Python's `csv` module writes `\r\n` by default. This is RFC 4180-compliant and
parses correctly in R, pandas and `awk`. **They were deliberately not normalised**, because
that would break byte-identity with their sources — a guarantee worth more than cosmetic
consistency. Recorded in MANIFEST §14 with the `tr -d '\r'` workaround.

## 3.7 Status

**No open items remain.** All twelve issues from the first verification are closed, both
author decisions are applied and verified, and the package passes 33 of 33 checks.
