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
#   Source line range : 365-393 (heredoc body: 366-392)
#   Pipeline stage    : 6 — ORF prediction
#   Purpose           : Build a BED file of top-50 transcript intervals for bedtools getfasta. NOTE: uses transcript start/end only; novel_genes.gtf contains no exon records, so the extracted sequence is unspliced genomic (introns included).
#   Writes            : results/transdecoder/top50.bed
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
    top_ids = set(line.strip() for line in f)

bed_lines = []
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
        chrom = parts[0]
        start = int(parts[3]) - 1
        end = int(parts[4])
        strand = parts[6]
        bed_lines.append(f"{chrom}\t{start}\t{end}\t{tid}\t0\t{strand}")

with open("results/transdecoder/top50.bed", "w") as f:
    f.write("\n".join(bed_lines) + "\n")

print(f"✓ Created BED file with {len(bed_lines)} transcripts")
