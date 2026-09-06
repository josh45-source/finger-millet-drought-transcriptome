#!/bin/bash
# ============================================================
# Finger Millet — Foldseek Web API (FIXED database format)
# Press Ctrl+C to stop at any time
# ============================================================

# Directory holding the ColabFold output folders.
# In this deposit they are under  structures/  — set FM_STRUCTURES to point there:
#   export FM_STRUCTURES=/path/to/package/structures
WIN_DOWNLOADS="${FM_STRUCTURES:-./structures}"
OUT_DIR="${FM_FOLDSEEK_OUT:-./foldseek_results}"
mkdir -p "${OUT_DIR}"

API="https://search.foldseek.com/api"

# Auto-find relaxed_rank_001 PDB in a folder
find_pdb() {
    find "$1" -name "*relaxed_rank_001*.pdb" | head -1
}

# ---- Your 4 protein folders ----
declare -A FOLDERS
FOLDERS["MSTRG_4687_1"]="${WIN_DOWNLOADS}/MSTRG_4687_1_finger_millet_a8fb3"
FOLDERS["MSTRG_45757_2"]="${WIN_DOWNLOADS}/MSTRG_45757_2_finger_millet_24e2d"
FOLDERS["MSTRG_6647_1"]="${WIN_DOWNLOADS}/MSTRG_6647_1_finger_millet_27b31"
FOLDERS["MSTRG_45758_1"]="${WIN_DOWNLOADS}/MSTRG_45758_1_finger_millet_9385e"

# ============================================================
# SUBMIT one job at a time, wait, download, repeat
# ============================================================
process_protein() {
    local NAME="$1"
    local PDB="$2"
    local PROTEIN_OUT="${OUT_DIR}/${NAME}"
    mkdir -p "${PROTEIN_OUT}"

    echo ""
    echo "=========================================="
    echo " Processing: ${NAME}"
    echo " PDB: $(basename $PDB)"
    echo "=========================================="

    # ---- Submit ----
    echo "  Submitting to Foldseek..."
    RESPONSE=$(curl -s -X POST "${API}/ticket" \
        -F "q=@${PDB}" \
        -F "mode=3diaa" \
        -F "database[]=afdb50" \
        -F "database[]=afdb-swissprot" \
        -F "database[]=afdb-proteome" \
        -F "database[]=pdb100" \
        2>/dev/null)

    echo "  Server response: ${RESPONSE}"

    # Extract ticket ID
    TICKET=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('id', ''))
except:
    print('')
" 2>/dev/null)

    if [ -z "$TICKET" ]; then
        echo "  ❌ Submission failed. Response: ${RESPONSE}"
        echo "  Trying with fewer databases..."

        # Fallback: try with just swissprot
        RESPONSE=$(curl -s -X POST "${API}/ticket" \
            -F "q=@${PDB}" \
            -F "mode=3diaa" \
            -F "database[]=afdb-swissprot" \
            2>/dev/null)

        TICKET=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('id', ''))
except:
    print('')
" 2>/dev/null)

        if [ -z "$TICKET" ]; then
            echo "  ❌ Fallback also failed: ${RESPONSE}"
            return 1
        fi
    fi

    echo "  ✅ Ticket ID: ${TICKET}"
    echo "${TICKET}" > "${PROTEIN_OUT}/${NAME}.ticket"

    # ---- Wait for completion ----
    echo "  Waiting for results..."
    ATTEMPTS=0
    while true; do
        STATUS_RESP=$(curl -s "${API}/ticket/${TICKET}" 2>/dev/null)
        STATUS=$(echo "$STATUS_RESP" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('status', 'UNKNOWN'))
except:
    print('UNKNOWN')
" 2>/dev/null)

        ATTEMPTS=$((ATTEMPTS + 1))
        echo "  [Attempt ${ATTEMPTS}] Status: ${STATUS}"

        if [ "$STATUS" = "COMPLETE" ]; then
            echo "  ✅ Job complete!"
            break
        elif [ "$STATUS" = "ERROR" ]; then
            echo "  ❌ Job failed on server"
            return 1
        elif [ $ATTEMPTS -gt 60 ]; then
            echo "  ⚠️  Timeout after 30 minutes"
            return 1
        fi
        sleep 30
    done

    # ---- Download results ----
    echo "  Downloading results..."
    curl -s "${API}/result/download/${TICKET}" \
        -o "${PROTEIN_OUT}/${NAME}_results.tar.gz" 2>/dev/null

    if [ -f "${PROTEIN_OUT}/${NAME}_results.tar.gz" ] && \
       [ -s "${PROTEIN_OUT}/${NAME}_results.tar.gz" ]; then
        tar xzf "${PROTEIN_OUT}/${NAME}_results.tar.gz" \
            -C "${PROTEIN_OUT}/" 2>/dev/null
        echo "  ✅ Results extracted to ${PROTEIN_OUT}/"
    fi

    # ---- Get top hits as TSV ----
    curl -s "${API}/result/${TICKET}/0" \
        -o "${PROTEIN_OUT}/${NAME}_hits_raw.json" 2>/dev/null

    # Parse to readable TSV
    python3 << PYEOF
import json, os

json_file = "${PROTEIN_OUT}/${NAME}_hits_raw.json"
tsv_file  = "${PROTEIN_OUT}/${NAME}_top_hits.tsv"

if not os.path.exists(json_file):
    print("  No JSON found")
    exit()

with open(json_file) as f:
    try:
        data = json.load(f)
    except Exception as e:
        print(f"  JSON parse error: {e}")
        exit()

with open(tsv_file, "w") as out:
    out.write("Database\tTarget\tProbability\tE-value\tSeqID\tOrganism\tDescription\n")
    results = data.get("results", [])
    for db_block in results:
        db = db_block.get("db", "unknown")
        alignments = db_block.get("alignments", [[]])[0]  # top query
        for hit in alignments[:5]:  # top 5 hits per db
            out.write("\t".join([
                db,
                str(hit.get("target", "")),
                str(hit.get("prob", "")),
                str(hit.get("eval", "")),
                str(hit.get("seqId", "")),
                str(hit.get("taxName", "")),
                str(hit.get("tDescription", ""))
            ]) + "\n")

print(f"  Top hits saved to: {tsv_file}")
PYEOF

    # Print top hits to terminal
    echo ""
    echo "  --- Top hits for ${NAME} ---"
    if [ -f "${PROTEIN_OUT}/${NAME}_top_hits.tsv" ]; then
        column -t -s $'\t' "${PROTEIN_OUT}/${NAME}_top_hits.tsv" | head -20
    fi
}

# ============================================================
# MAIN
# ============================================================
echo "============================================"
echo " Finger Millet Foldseek Web API Pipeline"
echo " Date: $(date)"
echo "============================================"

# First check what databases are actually available
echo ""
echo "=== Checking available databases ==="
curl -s "${API}/databases" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Available databases:')
    for db in data:
        print(f'  - {db}')
except Exception as e:
    print(f'Could not fetch database list: {e}')
    print(sys.stdin.read()[:200])
" 2>/dev/null

echo ""

# Process each protein one at a time
for name in "${!FOLDERS[@]}"; do
    PDB=$(find_pdb "${FOLDERS[$name]}")
    if [ -z "$PDB" ]; then
        echo "❌ ${name}: PDB not found, skipping"
        continue
    fi
    process_protein "$name" "$PDB"
done

echo ""
echo "============================================"
echo " ALL DONE!"
echo " Results in: ${OUT_DIR}"
echo "============================================"
