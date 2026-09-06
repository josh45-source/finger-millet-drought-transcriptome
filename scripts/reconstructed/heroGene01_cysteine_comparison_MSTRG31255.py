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
#   Source line range : 650-670 (heredoc body: 651-669)
#   Pipeline stage    : hero-gene characterisation (MSTRG.31255.1)
#   Purpose           : Print the 104 aa MSTRG.31255.1 peptide alongside the Leersia perrieri homolog A0A0D9XDT2 with cysteines highlighted, and split each at residue 28/29 into signal peptide and mature regions. Informal comparison — not a formal family assignment.
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

# Simple pairwise alignment to show conserved cysteines visually
eleusine = "MASSSAAALKMVVICALVLCVVVGPQLAAVHARETPEKEQQVLLQMPLAQELADVLSQLIPKNGGVEDCATEACKSCYSTCRVWCRFVPSCYPRCAELFECDSK"
leersia  = "MASAVALKIAALCMLILCSIGSQVMIVRASSTAKLVENVVGSSPRSSASPAPATVATSATPARQNCLILCAIKCLMDHELAAELRLAGDDSVGDVCSPACQTCLIVCAIKCVLKPNPTACYADCIVTDKCFTL"

# Highlight cysteines
def highlight_C(seq):
    return ''.join(f'[{aa}]' if aa=='C' else aa for aa in seq)

print("Eleusine (your gene):")
print(highlight_C(eleusine))
print()
print("Leersia (wild rice relative):")
print(highlight_C(leersia))
print()

# Signal peptide vs mature
print("=== Mature protein only (after signal peptide) ===")
print("Eleusine mature (29-104):", highlight_C(eleusine[28:]))
print("Leersia  mature (30-133):", highlight_C(leersia[29:]))
