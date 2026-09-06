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
#   Source line range : 1021-1082 (heredoc body: 1022-1081)
#   Pipeline stage    : 10 — co-expression
#   Purpose           : Extract StringTie per-transcript 'cov' values for the 10 candidates across all 6 samples. Raw coverage, not normalised or log-transformed.
#   Writes            : results/coexpression/expression_matrix.tsv
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
import csv
from collections import defaultdict

# Our top 10 novel candidates
novel_genes = [
    "MSTRG.333.1", "MSTRG.4687.1", "MSTRG.6647.1",
    "MSTRG.14681.1", "MSTRG.14874.2", "MSTRG.20738.1",
    "MSTRG.31255.1", "MSTRG.36758.1", "MSTRG.45758.1",
    "MSTRG.45757.2"
]

samples = [
    "DRR095904", "DRR095905", "DRR095906",  # control
    "DRR095907", "DRR095908", "DRR095909"   # drought
]

# Extract coverage values from count GTF files
print("Extracting expression values...")
expression = defaultdict(dict)

for sample in samples:
    gtf_file = f"results/counts/{sample}_counts.gtf"
    with open(gtf_file) as f:
        for line in f:
            if "\ttranscript\t" not in line:
                continue
            m = re.search(r'transcript_id "([^"]+)"', line)
            cov = re.search(r'cov "([^"]+)"', line)
            if m and cov:
                tid = m.group(1)
                if tid in novel_genes:
                    try:
                        expression[tid][sample] = float(cov.group(1))
                    except:
                        expression[tid][sample] = 0.0

# Print expression matrix
print("\nExpression matrix (coverage values):")
print(f"{'Gene':<15}", end="")
for s in samples:
    print(f"{s:<12}", end="")
print()
print("-" * 90)

for gene in novel_genes:
    print(f"{gene:<15}", end="")
    for s in samples:
        val = expression[gene].get(s, 0.0)
        print(f"{val:<12.1f}", end="")
    print()

# Save matrix
with open("results/coexpression/expression_matrix.tsv", "w") as f:
    f.write("gene_id\t" + "\t".join(samples) + "\n")
    for gene in novel_genes:
        vals = [str(expression[gene].get(s, 0.0)) for s in samples]
        f.write(gene + "\t" + "\t".join(vals) + "\n")

print("\n✓ Expression matrix saved")
