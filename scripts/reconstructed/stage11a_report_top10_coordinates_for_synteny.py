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
#   Source line range : 1434-1464 (heredoc body: 1435-1463)
#   Pipeline stage    : 11 — comparative screen
#   Purpose           : Print top-10 coordinates ahead of the comparative BLAST searches. Diagnostic only.
#   Writes            : (nothing — stdout only)
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

print("Coordinates for synteny analysis:")
print(f"{'Gene':<16} {'Chromosome':<15} {'Start':<12} {'End':<12} {'Strand'}")
print("-" * 65)

with open("results/novel_genes/novel_genes.gtf") as f:
    for line in f:
        if "\ttranscript\t" not in line:
            continue
        m = re.search(r'transcript_id "([^"]+)"', line)
        if not m:
            continue
        tid = m.group(1)
        if tid not in top10:
            continue
        parts = line.strip().split('\t')
        chrom = parts[0]
        start = parts[3]
        end = parts[4]
        strand = parts[6]
        print(f"{tid:<16} {chrom:<15} {start:<12} {end:<12} {strand}")
