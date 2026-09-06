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
#   Source line range : 1570-1640 (heredoc body: 1571-1639)
#   Pipeline stage    : 11 — comparative screen
#   Purpose           : Two-species classifier (sorghum + rice). Produced the SUPERSEDED table giving 5 Eleusine-specific candidates.
#   Writes            : results/synteny/synteny_combined.tsv
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

top10 = [
    "MSTRG.333.1", "MSTRG.4687.1", "MSTRG.6647.1",
    "MSTRG.14681.1", "MSTRG.14874.2", "MSTRG.20738.1",
    "MSTRG.31255.1", "MSTRG.36758.1", "MSTRG.45758.1",
    "MSTRG.45757.2"
]

# Parse rice BLAST results
results = {}
with open("results/synteny/vs_rice.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 6:
            continue
        m = re.search(r'(MSTRG\.\d+\.\d+)', parts[0])
        if not m:
            continue
        gene = m.group(1)
        pident = float(parts[2])
        length = int(parts[3])
        evalue = parts[4]
        bitscore = float(parts[5])
        if gene not in results or bitscore > results[gene][3]:
            results[gene] = (pident, length, evalue, bitscore)

# Load sorghum results
sorghum = {}
with open("results/synteny/synteny_summary.tsv") as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        sorghum[parts[0]] = parts[5]

print("Synteny summary — Finger millet vs Sorghum + Rice:")
print(f"{'Gene':<16} {'Sorghum':<12} {'Rice':<12} {'Classification'}")
print("-" * 65)

for gene in top10:
    in_sorghum = sorghum.get(gene, "NO")
    in_rice = "YES" if gene in results else "NO"

    if in_sorghum == "YES" and in_rice == "YES":
        classification = "Pan-grass conserved"
    elif in_sorghum == "YES" or in_rice == "YES":
        classification = "Partially conserved"
    else:
        classification = "Eleusine-specific ⭐"

    s_sym = "✅" if in_sorghum == "YES" else "❌"
    r_sym = "✅" if in_rice == "YES" else "❌"
    print(f"{gene:<16} {s_sym:<12} {r_sym:<12} {classification}")

# Save combined results
with open("results/synteny/synteny_combined.tsv", "w") as f:
    f.write("gene\tsorghum\trice\tclassification\n")
    for gene in top10:
        in_sorghum = sorghum.get(gene, "NO")
        in_rice = "YES" if gene in results else "NO"
        if in_sorghum == "YES" and in_rice == "YES":
            cls = "Pan-grass conserved"
        elif in_sorghum == "YES" or in_rice == "YES":
            cls = "Partially conserved"
        else:
            cls = "Eleusine-specific"
        f.write(f"{gene}\t{in_sorghum}\t{in_rice}\t{cls}\n")

print("\n✓ Combined synteny results saved")
