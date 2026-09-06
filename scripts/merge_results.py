#!/usr/bin/env python3
"""
merge_results.py — Merge DE results with BLAST annotations
Maintainer: see CITATION.cff
"""

import pandas as pd
import os
import logging

# ── Snakemake inputs ──────────────────────────────────────────
novel_up_file = snakemake.input["novel_up"]
blast_file    = snakemake.input["blast"]
out_report    = snakemake.output["report"]
log_file      = snakemake.log[0]

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)
log = logging.getLogger()
log.info("=== Final Report Started ===")

# ── Load DE results ───────────────────────────────────────────
log.info(f"Reading DE results: {novel_up_file}")
try:
    de = pd.read_csv(novel_up_file, sep="\t")
    log.info(f"  Loaded {len(de)} novel drought-upregulated transcripts")
except Exception as e:
    log.error(f"Could not read DE results: {e}")
    de = pd.DataFrame(columns=["transcript_id","log2FoldChange","padj"])

# ── Load BLAST results ────────────────────────────────────────
blast_cols = ["transcript_id","subject_id","pident","length",
              "evalue","bitscore","annotation"]
log.info(f"Reading BLAST results: {blast_file}")
try:
    blast = pd.read_csv(blast_file, sep="\t",
                        names=blast_cols, header=None)
    blast = (blast.sort_values(["transcript_id","evalue","bitscore"],
                                ascending=[True,True,False])
                  .drop_duplicates("transcript_id", keep="first"))
    log.info(f"  Best BLAST hits: {len(blast)}")
except Exception as e:
    log.warning(f"Could not read BLAST results: {e}")
    blast = pd.DataFrame(columns=blast_cols)

# ── Merge ─────────────────────────────────────────────────────
merged = pd.merge(
    de,
    blast[["transcript_id","evalue","bitscore","annotation"]],
    on="transcript_id", how="left"
)

# ── Tier candidates ───────────────────────────────────────────
STRESS_WORDS = [
    "drought","stress","dehydration","osmotic","ABA",
    "abscisic","desiccation","water deficit","LEA",
    "late embryogenesis","aquaporin","peroxidase","kinase"
]

def tier(row):
    has_hit  = pd.notna(row.get("annotation"))
    ann      = str(row.get("annotation","")).lower()
    is_stress = has_hit and any(w.lower() in ann for w in STRESS_WORDS)
    lfc      = row.get("log2FoldChange", 0)

    if not has_hit and lfc >= 3:
        return "Tier 1 — Novel, no homolog, highly induced"
    elif is_stress:
        return "Tier 2 — Novel, stress-related homolog"
    else:
        return "Tier 3 — Novel, other/no homolog"

merged["candidate_tier"] = merged.apply(tier, axis=1)
merged = merged.sort_values(["candidate_tier","padj"])

# ── Save ──────────────────────────────────────────────────────
os.makedirs(os.path.dirname(out_report), exist_ok=True)
merged.to_csv(out_report, sep="\t", index=False)

log.info(f"\nFinal report saved: {out_report}")
log.info(f"Total candidates: {len(merged)}")
if "candidate_tier" in merged.columns:
    for tier_name, count in merged["candidate_tier"].value_counts().items():
        log.info(f"  {tier_name}: {count}")

log.info("=== Final Report Done ===")
print(f"✓ Candidate genes saved: {out_report}")
print(f"  Total: {len(merged)}")
