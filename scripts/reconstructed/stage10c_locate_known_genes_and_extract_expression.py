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
#   Source line range : 1252-1343 (heredoc body: 1253-1342)
#   Pipeline stage    : 10 — co-expression
#   Purpose           : Take best blastn hit per known drought gene (CIPK31, TAF6, PP2A, SRPRa, FPS) to locate it in the assembly, then take the maximum StringTie coverage of any overlapping transcript as that gene's expression per sample.
#   Writes            : results/known_drought_genes/known_gene_expression.tsv
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
from collections import defaultdict

# Known gene names
gene_names = {
    "KT288194.1": "CIPK31",
    "KT824872.1": "TAF6",
    "KT824869.1": "PP2A",
    "KT824870.1": "SRPRa",
    "KT824871.1": "FPS"
}

# Get best BLAST hit (highest bitscore) for each known gene
print("Finding best genome locations...")
best_hits = {}
with open("results/known_drought_genes/known_vs_genome.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 10:
            continue
        qid = parts[0]
        chrom = parts[1]
        sstart = int(parts[6])
        send = int(parts[7])
        bitscore = float(parts[9])
        start = min(sstart, send)
        end = max(sstart, send)
        if qid not in best_hits or bitscore > best_hits[qid][3]:
            best_hits[qid] = (chrom, start, end, bitscore)

print("\nBest genome locations:")
for qid, (chrom, start, end, score) in best_hits.items():
    name = gene_names.get(qid, qid)
    print(f"  {name}: {chrom}:{start}-{end} (score={score:.0f})")

# Now search StringTie count files for transcripts overlapping these regions
print("\nSearching for expression in count files...")
samples = [
    "DRR095904", "DRR095905", "DRR095906",
    "DRR095907", "DRR095908", "DRR095909"
]

known_expression = {name: {} for name in gene_names.values()}

for sample in samples:
    gtf_file = f"results/counts/{sample}_counts.gtf"
    with open(gtf_file) as f:
        for line in f:
            if "\ttranscript\t" not in line:
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            t_start = int(parts[3])
            t_end = int(parts[4])
            cov_m = re.search(r'cov "([^"]+)"', line)
            if not cov_m:
                continue
            cov = float(cov_m.group(1))

            # Check overlap with each known gene
            for qid, (g_chrom, g_start, g_end, _) in best_hits.items():
                name = gene_names[qid]
                if chrom == g_chrom and t_start <= g_end and t_end >= g_start:
                    # Take highest coverage overlapping transcript
                    if sample not in known_expression[name] or \
                       cov > known_expression[name][sample]:
                        known_expression[name][sample] = cov

# Print results
print(f"\n{'Gene':<10}", end="")
for s in samples:
    print(f"{s:<12}", end="")
print()
print("-" * 85)

for name in gene_names.values():
    print(f"{name:<10}", end="")
    for s in samples:
        val = known_expression[name].get(s, 0.0)
        print(f"{val:<12.1f}", end="")
    print()

# Save
with open("results/known_drought_genes/known_gene_expression.tsv", "w") as f:
    f.write("gene\t" + "\t".join(samples) + "\n")
    for name in gene_names.values():
        vals = [str(known_expression[name].get(s, 0.0)) for s in samples]
        f.write(name + "\t" + "\t".join(vals) + "\n")

print("\n✓ Saved expression values")
