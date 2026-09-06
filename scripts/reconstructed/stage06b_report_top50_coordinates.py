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
#   Source line range : 335-361 (heredoc body: 336-360)
#   Pipeline stage    : 6 — candidate selection
#   Purpose           : Print genomic coordinates of the top-50 transcripts from novel_genes.gtf. Diagnostic only.
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

# Load top 50 IDs
with open("results/novel_genes/top50_ids.txt") as f:
    top_ids = set(line.strip() for line in f)

# Extract from novel_genes.gtf
coords = []
with open("results/novel_genes/novel_genes.gtf") as f:
    for line in f:
        if "\ttranscript\t" not in line:
            continue
        m = re.search(r'transcript_id "([^"]+)"', line)
        if not m:
            continue
        tid = m.group(1)
        if tid not in top_ids:
            continue
        parts = line.strip().split('\t')
        chrom, start, end, strand = parts[0], int(parts[3]), int(parts[4]), parts[6]
        coords.append((tid, chrom, start, end, strand))

print(f"Found coordinates for {len(coords)} transcripts")
for c in coords[:5]:
    print(f"  {c[0]}: {c[1]}:{c[2]}-{c[3]} ({c[4]})")
