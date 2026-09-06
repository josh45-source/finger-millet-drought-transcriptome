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
#   Source line range : 1345-1429 (heredoc body: 1346-1428)
#   Pipeline stage    : 10 — co-expression
#   Purpose           : THE CO-EXPRESSION SCRIPT that produced the reported r values. NOTE: the expression matrices for both novel and known genes are embedded as hard-coded Python literals rather than read from file. The audit verified all 10 candidate vectors against results/counts/*.gtf — 10/10 match exactly.
#   Writes            : results/known_drought_genes/novel_vs_known_correlation.tsv
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

samples = [
    "DRR095904", "DRR095905", "DRR095906",
    "DRR095907", "DRR095908", "DRR095909"
]

# Novel gene expression
novel = {
    "MSTRG.333.1":  [4.5,  5.3,  5.6,  63.3,  49.2,  39.0],
    "MSTRG.4687.1": [2.6,  5.9,  5.2,  152.0, 128.1, 84.5],
    "MSTRG.6647.1": [1.1,  1.6,  1.7,  40.8,  37.7,  28.1],
    "MSTRG.14681.1":[132.4,214.4,200.9,2493.6,2793.6,1787.9],
    "MSTRG.14874.2":[3.6,  3.1,  4.4,  96.0,  74.6,  49.3],
    "MSTRG.20738.1":[3.4,  5.0,  4.5,  70.6,  65.3,  46.7],
    "MSTRG.31255.1":[5.0,  6.5,  9.0,  554.6, 330.9, 216.2],
    "MSTRG.36758.1":[0.5,  0.7,  0.7,  14.1,  12.7,  7.8],
    "MSTRG.45758.1":[2.3,  3.6,  2.6,  78.1,  60.1,  42.0],
    "MSTRG.45757.2":[19.0, 25.9, 19.8, 273.4, 249.8, 151.6],
}

# Known drought gene expression
known = {
    "CIPK31": [138.8, 150.1, 188.6, 308.1, 292.8, 112.7],
    "TAF6":   [8.7,   14.4,  12.3,  39.2,  34.3,  24.1],
    "PP2A":   [31.9,  14.4,  30.6,  254.1, 185.2, 97.2],
    "SRPRa":  [91.3,  163.3, 162.9, 506.0, 322.2, 200.4],
    "FPS":    [40.7,  26.1,  32.6,  142.8, 99.0,  68.3],
}

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

# Calculate correlations
print("Correlation of novel genes with known drought genes:")
print(f"{'Novel Gene':<16}", end="")
for k in known:
    print(f"{k:<10}", end="")
print(f"{'Best_r':<10} {'Best_known'}")
print("-" * 80)

results = []
for ng, nvals in novel.items():
    print(f"{ng:<16}", end="")
    best_r = 0
    best_k = ""
    for kg, kvals in known.items():
        r = pearson(nvals, kvals)
        print(f"{r:<10.3f}", end="")
        if abs(r) > abs(best_r):
            best_r = r
            best_k = kg
    print(f"{best_r:<10.3f} {best_k}")
    results.append((ng, best_r, best_k))

# Save results
with open("results/known_drought_genes/novel_vs_known_correlation.tsv","w") as f:
    f.write("novel_gene\tCIPK31\tTAF6\tPP2A\tSRPRa\tFPS\tbest_r\tbest_known\n")
    for ng, nvals in novel.items():
        cors = [str(round(pearson(nvals, known[k]), 4)) for k in known]
        best_r = max(pearson(nvals, known[k]) for k in known)
        best_k = max(known.keys(), key=lambda k: pearson(nvals, known[k]))
        f.write(ng + "\t" + "\t".join(cors) + f"\t{best_r:.4f}\t{best_k}\n")

print("\n✓ Results saved")

# Summary
print("\nHighly correlated pairs (r > 0.85):")
print(f"{'Novel gene':<16} {'Known gene':<10} {'r'}")
print("-" * 40)
for ng, nvals in novel.items():
    for kg, kvals in known.items():
        r = pearson(nvals, kvals)
        if r > 0.85:
            print(f"{ng:<16} {kg:<10} {r:.4f}")
