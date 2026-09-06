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
#   Source line range : 673-712 (heredoc body: 674-711)
#   Pipeline stage    : hero-gene characterisation (MSTRG.31255.1)
#   Purpose           : Submit the 76 aa mature peptide to the NCBI BLAST URL API (blastp vs nr) and poll for results. First attempt; RID printed to terminal only, no output retained.
#   Writes            : (nothing — stdout only; results not retained)
#
# Caveat on ordering: ~/.bash_history carries no timestamps, and because
# concurrent screen sessions flush their buffers independently, line order
# is NOT strictly chronological across sessions. Line numbers identify the
# block; they do not establish execution order relative to distant blocks.
#
# Working directory at execution was /mnt/d/finger_millet_project unless
# the relative paths in the body indicate otherwise.
# =============================================================================

import urllib.request, urllib.parse, time

# Submit BLAST
params = urllib.parse.urlencode({
    'CMD': 'Put',
    'PROGRAM': 'blastp',
    'DATABASE': 'nr',
    'QUERY': 'AVHARETPEKEQQVLLQMPLAQELADVLSQLIPKNGGVEDCATEACKSCYSTCRVWCRFVPSCYPRCAELFECDSK',
    'HITLIST_SIZE': 20,
    'FORMAT_TYPE': 'Text'
}).encode()

req = urllib.request.Request('https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi', data=params)
response = urllib.request.urlopen(req).read().decode()

# Extract RID
rid = [l.split('=')[1].strip() for l in response.split('\n') if 'RID' in l and '=' in l]
if rid:
    print(f"RID = {rid[0]}")
    print(f"Check results at: https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID={rid[0]}&FORMAT_TYPE=Text")
    print("Waiting 30 seconds then fetching results...")
    time.sleep(30)
    result_url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID={rid[0]}&FORMAT_TYPE=Text"
    result = urllib.request.urlopen(result_url).read().decode()
    # Print top hits
    in_hits = False
    count = 0
    for line in result.split('\n'):
        if 'Sequences producing' in line:
            in_hits = True
        if in_hits:
            print(line)
            count += 1
        if count > 30:
            break
else:
    print("Could not get RID")
    print(response[:500])
