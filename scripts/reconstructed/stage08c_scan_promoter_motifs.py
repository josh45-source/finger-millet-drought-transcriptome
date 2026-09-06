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
#   Source line range : 949-1013 (heredoc body: 950-1012)
#   Pipeline stage    : 8 — promoter analysis
#   Purpose           : THE PROMOTER MOTIF SCANNER. Exact-substring count of six hard-coded motifs (ABRE_core ACGTGG, ABRE_variant ACGTGT, ABRE_G_box CACGTG, DRE, MYB, W_box) in the extracted 1000 bp promoters. NOTE: has_ABRE is set true if ANY of the six matched, including W-box and MYB which are not ABREs.
#   Writes            : results/promoter_analysis/abre_results.tsv
#
# Caveat on ordering: ~/.bash_history carries no timestamps, and because
# concurrent screen sessions flush their buffers independently, line order
# is NOT strictly chronological across sessions. Line numbers identify the
# block; they do not establish execution order relative to distant blocks.
#
# Working directory at execution was /mnt/d/finger_millet_project unless
# the relative paths in the body indicate otherwise.
# =============================================================================

# Search for ABRE motifs in promoter sequences

# ABRE core motifs
ABRE_MOTIFS = {
    "ABRE_core":    "ACGTGG",
    "ABRE_variant": "ACGTGT",
    "ABRE_G_box":   "CACGTG",
    "DRE_motif":    "TACCGACAT",
    "MYB_motif":    "CAACTG",
    "W_box":        "TTGACT",
}

results = {}

# Read promoter sequences
with open("results/promoter_analysis/promoters.fa") as f:
    current_id = None
    current_seq = []
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if current_id:
                results[current_id] = "".join(current_seq).upper()
            current_id = line[1:].split("::")[0].split("(")[0]
            current_seq = []
        else:
            current_seq.append(line)
    if current_id:
        results[current_id] = "".join(current_seq).upper()

print(f"{'Gene':<15} {'Seq_len':<10} ", end="")
for motif in ABRE_MOTIFS:
    print(f"{motif:<12}", end="")
print()
print("-" * 100)

summary = []
for tid, seq in results.items():
    print(f"{tid:<15} {len(seq):<10} ", end="")
    motif_counts = {}
    for motif_name, motif_seq in ABRE_MOTIFS.items():
        count = seq.count(motif_seq)
        motif_counts[motif_name] = count
        print(f"{count:<12}", end="")
    print()
    summary.append((tid, seq, motif_counts))

# Save results
with open("results/promoter_analysis/abre_results.tsv", "w") as f:
    header = "transcript_id\t" + "\t".join(ABRE_MOTIFS.keys()) + "\thas_ABRE"
    f.write(header + "\n")
    for tid, seq, counts in summary:
        has_abre = "YES" if any(counts.values()) else "NO"
        row = tid + "\t" + "\t".join(str(counts[m]) for m in ABRE_MOTIFS) + f"\t{has_abre}"
        f.write(row + "\n")

print("\n✓ Results saved to results/promoter_analysis/abre_results.tsv")

# Summary
has_abre = sum(1 for _, _, c in summary if any(c.values()))
print(f"\nSummary:")
print(f"  Candidates with at least one ABRE motif: {has_abre}/10")
print(f"  Candidates with no motifs:               {10-has_abre}/10")
