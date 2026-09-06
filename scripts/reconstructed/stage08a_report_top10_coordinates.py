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
#   Source line range : 877-907 (heredoc body: 878-906)
#   Pipeline stage    : 8 — promoter analysis
#   Purpose           : Print genomic coordinates of the top-10 candidates from novel_genes.gtf, used to hand-build the promoter coordinate table in stage08b.
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

with open("results/novel_genes/top50_ids.txt") as f:
    top_ids = [line.strip() for line in f]

# Get top 10 only
top10 = top_ids[:10]

print("Top 10 candidates:")
coords = []
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
        start = int(parts[3])
        end = int(parts[4])
        strand = parts[6]
        print(f"  {tid}: {chrom}:{start}-{end} ({strand})")
        coords.append((tid, chrom, start, end, strand))

print(f"\nFound {len(coords)} coordinates")
