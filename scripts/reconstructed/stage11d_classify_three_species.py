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
#   Source line range : 1646-1726 (heredoc body: 1647-1725)
#   Pipeline stage    : 11 — comparative screen
#   Purpose           : THE DEFINITIVE SYNTENY CLASSIFIER (sorghum + rice + foxtail millet). Produced the authoritative table: 4 Eleusine-specific, 1 Panicoideae-specific, 1 partially conserved, 4 pan-grass conserved. Classification rests on presence/absence of a blastn hit at E <= 1e-5; the top-10 list is hard-coded.
#   Writes            : results/synteny/synteny_3species.tsv
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

def parse_blast(filename):
    results = {}
    with open(filename) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 6:
                continue
            m = re.search(r'(MSTRG\.\d+\.\d+)', parts[0])
            if not m:
                continue
            gene = m.group(1)
            bitscore = float(parts[5])
            pident = float(parts[2])
            if gene not in results or bitscore > results[gene][1]:
                results[gene] = (pident, bitscore)
    return results

sorghum = parse_blast("results/synteny/vs_sorghum.txt")
rice    = parse_blast("results/synteny/vs_rice.txt")
foxtail = parse_blast("results/synteny/vs_foxtail.txt")

print("Complete synteny analysis — 3 species comparison:")
print(f"{'Gene':<16} {'Sorghum':<10} {'Rice':<10} {'Foxtail':<10} {'Classification'}")
print("-" * 75)

rows = []
for gene in top10:
    in_s = gene in sorghum
    in_r = gene in rice
    in_f = gene in foxtail

    if in_s and in_r and in_f:
        cls = "Pan-grass conserved"
    elif in_s and in_r:
        cls = "Sorghum+Rice conserved"
    elif in_f and (in_s or in_r):
        cls = "Partially conserved"
    elif in_f:
        cls = "Panicoideae-specific"
    elif in_s or in_r:
        cls = "Partially conserved"
    else:
        cls = "Eleusine-specific ⭐"

    s = "✅" if in_s else "❌"
    r = "✅" if in_r else "❌"
    f = "✅" if in_f else "❌"
    print(f"{gene:<16} {s:<10} {r:<10} {f:<10} {cls}")
    rows.append((gene, in_s, in_r, in_f, cls))

# Summary
eleusine = sum(1 for r in rows if "Eleusine" in r[4])
pan = sum(1 for r in rows if "Pan-grass" in r[4])
partial = sum(1 for r in rows if "Partial" in r[4] or
              "Sorghum" in r[4])

print(f"\nSummary:")
print(f"  Pan-grass conserved:    {pan}/10")
print(f"  Partially conserved:    {partial}/10")
print(f"  Eleusine-specific:      {eleusine}/10")

# Save
with open("results/synteny/synteny_3species.tsv", "w") as f:
    f.write("gene\tsorghum\trice\tfoxtail\tclassification\n")
    for gene, in_s, in_r, in_f, cls in rows:
        f.write(f"{gene}\t{'YES' if in_s else 'NO'}\t"
                f"{'YES' if in_r else 'NO'}\t"
                f"{'YES' if in_f else 'NO'}\t{cls}\n")

print("\n✓ Saved results/synteny/synteny_3species.tsv")
