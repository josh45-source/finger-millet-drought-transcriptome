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
#   Source line range : 909-946 (heredoc body: 910-945)
#   Pipeline stage    : 8 — promoter analysis
#   Purpose           : Build strand-aware 1000 bp upstream promoter intervals from hard-coded coordinates. + strand: (start-1001, start-1); - strand: (end, end+1000).
#   Writes            : results/promoter_analysis/promoters.bed
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

coords = [
    ("MSTRG.333.1",   "CM064417.1", 3454517,  3463191,  "+"),
    ("MSTRG.4687.1",  "CM064418.1", 51077356, 51083641, "-"),
    ("MSTRG.6647.1",  "CM064419.1", 1567016,  1574258,  "+"),
    ("MSTRG.14681.1", "CM064421.1", 10423119, 10424833, "+"),
    ("MSTRG.14874.2", "CM064421.1", 15314031, 15318107, "+"),
    ("MSTRG.20738.1", "CM064423.1", 6958270,  6963730,  "-"),
    ("MSTRG.31255.1", "CM064427.1", 16937315, 16938027, "-"),
    ("MSTRG.36758.1", "CM064429.1", 9770807,  9773064,  "+"),
    ("MSTRG.45758.1", "CM064434.1", 47998519, 48003901, "+"),
    ("MSTRG.45757.2", "CM064434.1", 47980126, 47983062, "-"),
]

# Create BED file for promoter regions
# For + strand: promoter = (start-1000) to start
# For - strand: promoter = end to (end+1000)
bed_lines = []
for tid, chrom, start, end, strand in coords:
    if strand == "+":
        prom_start = max(0, start - 1001)
        prom_end   = start - 1
    else:
        prom_start = end
        prom_end   = end + 1000
    bed_lines.append(
        f"{chrom}\t{prom_start}\t{prom_end}\t{tid}\t0\t{strand}"
    )

with open("results/promoter_analysis/promoters.bed", "w") as f:
    f.write("\n".join(bed_lines) + "\n")

print("Promoter BED file created:")
for line in bed_lines:
    print(f"  {line}")
