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
#   Source line range : 1084-1154 (heredoc body: 1085-1153)
#   Pipeline stage    : 10 — co-expression
#   Purpose           : Hand-written Pearson correlation over all candidate pairs (n = 6 samples). No p-values, confidence intervals, or multiple-testing correction.
#   Writes            : results/coexpression/correlation_matrix.tsv
#
# Caveat on ordering: ~/.bash_history carries no timestamps, and because
# concurrent screen sessions flush their buffers independently, line order
# is NOT strictly chronological across sessions. Line numbers identify the
# block; they do not establish execution order relative to distant blocks.
#
# Working directory at execution was /mnt/d/finger_millet_project unless
# the relative paths in the body indicate otherwise.
# =============================================================================

import math
from collections import defaultdict

samples = [
    "DRR095904", "DRR095905", "DRR095906",
    "DRR095907", "DRR095908", "DRR095909"
]

# Load expression matrix
expression = {}
with open("results/coexpression/expression_matrix.tsv") as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split('\t')
        gene = parts[0]
        vals = [float(x) for x in parts[1:]]
        expression[gene] = vals

genes = list(expression.keys())

def pearson(x, y):
    n = len(x)
    mx = sum(x)/n
    my = sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0
    return num/(dx*dy)

# Calculate all pairwise correlations
print("Pearson correlation matrix:")
print(f"{'Gene':<15}", end="")
for g in genes:
    print(f"{g[:10]:<12}", end="")
print()
print("-" * 130)

corr_matrix = {}
for g1 in genes:
    print(f"{g1:<15}", end="")
    corr_matrix[g1] = {}
    for g2 in genes:
        r = pearson(expression[g1], expression[g2])
        corr_matrix[g1][g2] = r
        print(f"{r:<12.3f}", end="")
    print()

# Find highly correlated pairs
print("\nHighly correlated gene pairs (r > 0.95):")
print(f"{'Gene 1':<15} {'Gene 2':<15} {'Correlation':<12}")
print("-" * 45)
for i, g1 in enumerate(genes):
    for j, g2 in enumerate(genes):
        if i < j:
            r = corr_matrix[g1][g2]
            if r > 0.95:
                print(f"{g1:<15} {g2:<15} {r:<12.4f}")

# Save
with open("results/coexpression/correlation_matrix.tsv", "w") as f:
    f.write("gene_id\t" + "\t".join(genes) + "\n")
    for g1 in genes:
        row = g1 + "\t" + "\t".join(
            f"{corr_matrix[g1][g2]:.4f}" for g2 in genes)
        f.write(row + "\n")

print("\n✓ Correlation matrix saved")
