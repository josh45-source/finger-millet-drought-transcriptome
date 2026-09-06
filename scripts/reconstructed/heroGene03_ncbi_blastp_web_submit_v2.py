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
#   Source line range : 714-785 (heredoc body: 715-784)
#   Pipeline stage    : hero-gene characterisation (MSTRG.31255.1)
#   Purpose           : Second NCBI blastp submission with improved RID extraction and a fallback to the EBI NCBI-BLAST REST service against UniProtKB. Results printed to terminal only; no output retained.
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

import urllib.request, urllib.parse, time, json

QUERY = "AVHARETPEKEQQVLLQMPLAQELADVLSQLIPKNGGVEDCATEACKSCYSTCRVWCRFVPSCYPRCAELFECDSK"

# Use NCBI blastp via E-utilities
params = urllib.parse.urlencode({
    'CMD': 'Put',
    'PROGRAM': 'blastp',
    'DATABASE': 'nr',
    'QUERY': QUERY,
    'HITLIST_SIZE': 20,
    'FORMAT_TYPE': 'Text',
    'tool': 'bioinformatics_pipeline',
    'email': 'joshua@research.com'
}).encode()

headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(
    'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi',
    data=params,
    headers=headers
)
response = urllib.request.urlopen(req).read().decode()

# Better RID extraction
import re
rid_match = re.search(r'RID = ([A-Z0-9]+)', response)
if rid_match:
    rid = rid_match.group(1)
    print(f"✅ RID = {rid}")
    print("Waiting 45 seconds for BLAST to complete...")
    time.sleep(45)

    result_url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID={rid}&FORMAT_TYPE=Text"
    req2 = urllib.request.Request(result_url, headers=headers)
    result = urllib.request.urlopen(req2).read().decode()

    # Print hits section
    in_hits = False
    count = 0
    for line in result.split('\n'):
        if 'Sequences producing' in line:
            in_hits = True
        if in_hits:
            print(line)
            count += 1
        if count > 35:
            break
else:
    print("❌ Could not get RID")
    # Try UniProt BLAST instead
    print("Trying UniProt BLAST...")
    params2 = urllib.parse.urlencode({
        'sequence': QUERY,
        'program': 'blastp',
        'database': 'uniprotkb',
        'threshold': '10',
        'matrix': 'BLOSUM62',
        'filter': 'false',
        'gapped': 'true',
        'hits': '20'
    }).encode()
    req3 = urllib.request.Request(
        'https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/run',
        data=params2,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    resp3 = urllib.request.urlopen(req3).read().decode()
    print(f"UniProt job ID: {resp3}")
    print(f"Check at: https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/status/{resp3}")
