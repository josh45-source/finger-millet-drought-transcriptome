# results_v1/ — ORIGINAL ANALYSIS, SUPERSEDED

**Status: historical record. Do not use these numbers.**

This directory holds the results exactly as produced by the April 2026 pipeline run.
It is retained unmodified so the published claims can be traced to the files that
generated them, and so the corrections in `results_v2/` can be checked against them.

**These results contain four confirmed defects.** They are documented in full in
`../docs/DE_COMPARISON.md` and `../docs/VERIFICATION.md`:

1. **DESeq2 was not given read counts.** `../scripts/de_analysis.R` computes
   `round(cov * 100)` from the StringTie `cov` attribute. The genuine `-e -B` count
   tables existed and were never used.
2. **The BLAST annotation join never matched.** `bedtools getfasta -name` on a GTF
   wrote the feature type (`transcript`) as the FASTA name, so every query ID read
   `transcript::<chrom>:<start>-<end>` while the DE table was keyed on `MSTRG.x.y`.
   The `how="left"` merge assigned NaN to all 2,354 rows.
3. **`STRESS_WORDS` matched substrings, not words** — `ABA` matched *tabacum*,
   `LEA` matched *nuclear*.
4. **Sequence extraction lost exon structure**, so all extracted sequences carry
   their introns.

**Use `../results_v2/` instead.**

| This directory | Superseded by |
|---|---|
| `all_de_results.tsv` | `../results_v2/de/all_de_results_v2.tsv` |
| `drought_upregulated_novel_genes.tsv` (2,354) | `../results_v2/de/drought_upregulated_novel_genes_v2.tsv` (2,422) |
| — (no working annotation table existed) | `../results_v2/annotation/candidate_genes_v2_annotated.tsv` |

`synteny_3species.tsv`, `novel_vs_known_correlation.tsv`, the InterProScan output and
the peptide FASTAs in `sequences/` are **not** superseded — no v2 equivalent was
produced. They inherit the unspliced-extraction limitation described above.
