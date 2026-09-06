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
#   Source line range : 312-330 (heredoc body: 313-329)
#   Pipeline stage    : 6 — candidate selection
#   Purpose           : Sort candidate_genes_final.tsv by padj ascending; take the first 50. Defines the entire downstream candidate set; the 'top 10' are simply rows 1-10 of this list.
#   Writes            : results/novel_genes/top50_ids.txt
#
# Caveat on ordering: ~/.bash_history carries no timestamps, and because
# concurrent screen sessions flush their buffers independently, line order
# is NOT strictly chronological across sessions. Line numbers identify the
# block; they do not establish execution order relative to distant blocks.
#
# Working directory at execution was /mnt/d/finger_millet_project unless
# the relative paths in the body indicate otherwise.
# =============================================================================

import csv

top_ids = []
with open("results/final_report/candidate_genes_final.tsv") as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = sorted(reader, key=lambda x: float(x.get('padj', 1)))
    for row in rows[:50]:
        top_ids.append(row['transcript_id'])

print("Top 10 candidates:")
for tid in top_ids[:10]:
    print(f"  {tid}")

with open("results/novel_genes/top50_ids.txt", "w") as f:
    for tid in top_ids:
        f.write(tid + "\n")
print(f"\n✓ Saved {len(top_ids)} IDs to top50_ids.txt")
