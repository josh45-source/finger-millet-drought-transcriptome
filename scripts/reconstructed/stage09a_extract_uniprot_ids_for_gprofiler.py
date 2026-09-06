# =============================================================================
# RECONSTRUCTED FROM SHELL HISTORY — NOT A MAINTAINED SOURCE FILE
# =============================================================================
#
# This script was never saved to disk during the analysis. It was typed
# directly into an interactive shell as a heredoc:
#
#     python3 << 'EOF'
#     ... body ...
#     EOF
#
# The body below was recovered VERBATIM from ~/.bash_history on
# 19 August 2026. Nothing has been corrected, reformatted, or improved:
# indentation, comments, spelling, hard-coded values and any bugs are
# exactly as executed. Only this header has been added.
#
#   Source            : ~/.bash_history
#   Source line range : 1163-1233 (heredoc body: 1164-1232)
#   Pipeline stage    : 9 — GO enrichment
#   Purpose           : Parse UniProt accessions (sp|ACC| regex) from the Swiss-Prot blastx hits of drought-upregulated transcripts, for manual paste into the g:Profiler web server. 29 accessions were written; g:Profiler mapped only 9.
#   Writes            : results/coexpression/uniprot_ids_for_goprofiler.txt
#
# Caveat on ordering: ~/.bash_history carries no timestamps, and because
# concurrent screen sessions flush their buffers independently, line order
# is NOT strictly chronological across sessions. Line numbers identify the
# block; they do not establish execution order relative to distant blocks.
#
# Working directory at execution was /mnt/d/finger_millet_project unless
# the relative paths in the body indicate otherwise.
# =============================================================================

import re

# Load mapping: coord_id -> MSTRG_id
print("Building ID mapping...")
mstrg_to_coord = {}
with open("results/novel_genes/novel_genes.gtf") as f:
    for line in f:
        if "\ttranscript\t" not in line:
            continue
        m_id = re.search(r'transcript_id "([^"]+)"', line)
        if not m_id:
            continue
        tid = m_id.group(1)
        parts = line.strip().split('\t')
        chrom, start, end = parts[0], parts[3], parts[4]
        coord = f"transcript::{chrom}:{start}-{end}"
        mstrg_to_coord[tid] = coord

# Reverse mapping
coord_to_mstrg = {v: k for k, v in mstrg_to_coord.items()}

# Load drought upregulated genes
drought_genes = set()
with open("results/de_analysis/drought_upregulated_novel_genes.tsv") as f:
    next(f)  # skip header
    for line in f:
        tid = line.strip().split('\t')[6]
        drought_genes.add(tid)

print(f"Drought upregulated genes: {len(drought_genes)}")

# Extract UniProt IDs for drought genes from BLAST
print("Extracting UniProt IDs...")
uniprot_ids = set()
gene_to_uniprot = {}

with open("results/novel_genes/blast_results.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue
        coord_id = parts[0]
        uniprot_raw = parts[1]

        # Get MSTRG id
        mstrg = coord_to_mstrg.get(coord_id)
        if not mstrg or mstrg not in drought_genes:
            continue

        # Extract UniProt accession e.g. sp|Q9FNJ9|CA1P_ARATH
        m = re.search(r'sp\|([A-Z0-9]+)\|', uniprot_raw)
        if m:
            uid = m.group(1)
            uniprot_ids.add(uid)
            if mstrg not in gene_to_uniprot:
                gene_to_uniprot[mstrg] = uid

print(f"Unique UniProt IDs found: {len(uniprot_ids)}")

# Save UniProt IDs for g:Profiler
with open("results/coexpression/uniprot_ids_for_goprofiler.txt", "w") as f:
    for uid in sorted(uniprot_ids):
        f.write(uid + "\n")

print("\nUniProt IDs (paste these into g:Profiler):")
for uid in sorted(uniprot_ids):
    print(f"  {uid}")

print("\n✓ Saved to results/coexpression/uniprot_ids_for_goprofiler.txt")
