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
#   Source line range : 1487-1564 (heredoc body: 1488-1563)
#   Pipeline stage    : 11 — comparative screen
#   Purpose           : Parse vs_sorghum.txt, keep the best hit per gene by bitscore, and record conserved YES/NO for the hard-coded top-10 list.
#   Writes            : results/synteny/synteny_summary.tsv
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

# Gene name mapping
gene_names = {}
current_gene = None
with open("results/transdecoder/top50_transcripts.fa") as f:
    for line in f:
        if line.startswith(">"):
            m = re.search(r'(MSTRG\.\d+\.\d+)', line)
            if m:
                current_gene = m.group(1)
        elif current_gene:
            gene_names[current_gene] = current_gene

# Parse BLAST results
print("Synteny results — Finger millet vs Sorghum bicolor:")
print(f"{'Gene':<16} {'Sorghum_chr':<20} {'Identity%':<12} {'Length':<10} {'E-value':<12} {'Conserved?'}")
print("-" * 85)

results = {}
with open("results/synteny/vs_sorghum.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 6:
            continue
        qid = parts[0]
        # Extract MSTRG id
        m = re.search(r'(MSTRG\.\d+\.\d+)', qid)
        if not m:
            continue
        gene = m.group(1)
        sorghum_chr = parts[1]
        pident = float(parts[2])
        length = int(parts[3])
        evalue = parts[4]
        bitscore = float(parts[5])

        # Keep best hit per gene
        if gene not in results or bitscore > results[gene][4]:
            results[gene] = (sorghum_chr, pident, length, evalue,
                           bitscore)

# Top 10 candidates
top10 = [
    "MSTRG.333.1", "MSTRG.4687.1", "MSTRG.6647.1",
    "MSTRG.14681.1", "MSTRG.14874.2", "MSTRG.20738.1",
    "MSTRG.31255.1", "MSTRG.36758.1", "MSTRG.45758.1",
    "MSTRG.45757.2"
]

conserved = 0
for gene in top10:
    if gene in results:
        chrom, pident, length, evalue, bitscore = results[gene]
        conserved += 1
        status = "✅ CONSERVED"
        print(f"{gene:<16} {chrom:<20} {pident:<12.1f} "
              f"{length:<10} {evalue:<12} {status}")
    else:
        print(f"{gene:<16} {'No hit':<20} {'—':<12} "
              f"{'—':<10} {'—':<12} ❌ Not found")

print(f"\nSummary: {conserved}/10 candidates conserved in Sorghum")

# Save
with open("results/synteny/synteny_summary.tsv", "w") as f:
    f.write("gene\tsorghum_chr\tpident\tlength\tevalue\tconserved\n")
    for gene in top10:
        if gene in results:
            chrom, pident, length, evalue, _ = results[gene]
            f.write(f"{gene}\t{chrom}\t{pident:.1f}\t{length}\t"
                   f"{evalue}\tYES\n")
        else:
            f.write(f"{gene}\t—\t—\t—\t—\tNO\n")

print("✓ Saved to results/synteny/synteny_summary.tsv")
