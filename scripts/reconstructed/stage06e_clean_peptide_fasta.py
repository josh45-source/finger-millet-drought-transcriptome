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
#   Source line range : 440-468 (heredoc body: 441-467)
#   Pipeline stage    : 6 — ORF prediction
#   Purpose           : Rewrite TransDecoder peptides with bare MSTRG headers and stop-codon asterisks stripped, for InterProScan submission. Run from results/transdecoder/.
#   Writes            : results/transdecoder/top50_clean.pep
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

with open("top50_transcripts.fa.transdecoder.pep") as f:
    content = f.read()

entries = content.strip().split('\n>')
clean = []
for entry in entries:
    if not entry.startswith('>'):
        entry = '>' + entry
    lines = entry.strip().split('\n')
    header = lines[0]
    # Extract just the MSTRG ID
    m = re.search(r'(MSTRG\.\d+\.\d+)', header)
    if m:
        tid = m.group(1)
        seq = ''.join(lines[1:])
        # Remove stop codon asterisk
        seq = seq.replace('*', '')
        clean.append(f'>{tid}\n{seq}')

with open("top50_clean.pep", 'w') as f:
    f.write('\n'.join(clean))

print(f"✓ Cleaned {len(clean)} sequences")
print("\nFirst entry preview:")
print('\n'.join(clean[0].split('\n')[:3]))
