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
#   Source line range : 411-434 (heredoc body: 412-433)
#   Pipeline stage    : 6 — ORF prediction
#   Purpose           : Compare TransDecoder peptide output against the top-50 list to identify candidates with no predicted ORF (reported as putative lncRNAs). Run from results/transdecoder/.
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

# Get IDs with ORFs
orfs = set()
with open("top50_transcripts.fa.transdecoder.pep") as f:
    for line in f:
        if line.startswith(">"):
            # Extract original transcript ID
            tid = line.split("::")[0].replace(">","").strip()
            orfs.add(tid)

# Compare with top50
with open("../novel_genes/top50_ids.txt") as f:
    top50 = [line.strip() for line in f]

print("✅ Candidates WITH protein-coding ORF:")
for tid in top50:
    if tid in orfs:
        print(f"  {tid}")

print(f"\n❌ Candidates with NO ORF (likely lncRNA):")
for tid in top50:
    if tid not in orfs:
        print(f"  {tid}")
