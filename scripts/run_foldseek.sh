#!/bin/bash
# ============================================================
# Finger Millet Novel Genes — Foldseek Automated Search
# Author: see CITATION.cff (finger millet project)
#
# HOW TO RUN (on Linux/WSL terminal):
#   bash run_foldseek.sh
#
# To open WSL on Windows, press Win+R and type: wsl
# Your Windows Downloads folder is at:
#   $FM_STRUCTURES (originally C:\Users\<user>\Downloads\)
# ============================================================

# ---- PATHS (already configured for your machine) ----
# Directory holding the ColabFold output folders.
# In this deposit they are under  structures/  — set FM_STRUCTURES to point there:
#   export FM_STRUCTURES=/path/to/package/structures
WIN_DOWNLOADS="${FM_STRUCTURES:-./structures}"
OUT_DIR="${FM_FOLDSEEK_OUT:-./foldseek_results}"
DB_DIR="$HOME/foldseek_dbs"
TMP_DIR="/tmp/foldseek_tmp"

# ---- Your 4 PDB files ----
declare -A PROTEINS
PROTEINS["MSTRG_4687_1"]="${WIN_DOWNLOADS}/MSTRG_4687_1_finger_millet_a8fb3/MSTRG_4687_1_finger_millet_a8fb3_relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb"
PROTEINS["MSTRG_45757_2"]="${WIN_DOWNLOADS}/MSTRG_45757_2_finger_millet_24e2d/MSTRG_45757_2_finger_millet_24e2d_relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb"
PROTEINS["MSTRG_6647_1"]="${WIN_DOWNLOADS}/MSTRG_6647_1_finger_millet_27b31/MSTRG_6647_1_finger_millet_27b31_relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb"
PROTEINS["MSTRG_45758_1"]="${WIN_DOWNLOADS}/MSTRG_45758_1_finger_millet_9385e/MSTRG_45758_1_finger_millet_9385e_relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb"

# ---- Databases to search ----
DATABASES=("afdb50" "afdb-swissprot" "afdb-proteome" "pdb100")

# ============================================================
# FUNCTIONS
# ============================================================

install_foldseek() {
    echo "=== Checking Foldseek ==="
    if command -v foldseek &> /dev/null; then
        echo "✅ Foldseek found: $(foldseek version)"
        return
    fi
    echo "Installing Foldseek..."
    wget -q https://mmseqs.com/foldseek/foldseek-linux-avx2.tar.gz -O /tmp/foldseek.tar.gz
    tar xzf /tmp/foldseek.tar.gz -C /tmp/
    sudo cp /tmp/foldseek/bin/foldseek /usr/local/bin/
    echo "✅ Foldseek installed"
}

download_databases() {
    echo ""
    echo "=== Downloading Databases (only needed once, may take time) ==="
    mkdir -p "${DB_DIR}"
    for db in "${DATABASES[@]}"; do
        if [ -f "${DB_DIR}/${db}.dbtype" ]; then
            echo "  ✅ ${db} already exists"
        else
            echo "  Downloading ${db}..."
            foldseek databases ${db} "${DB_DIR}/${db}" "${TMP_DIR}"
            echo "  ✅ ${db} done"
        fi
    done
}

check_pdb_files() {
    echo ""
    echo "=== Checking PDB files exist ==="
    ALL_OK=true
    for name in "${!PROTEINS[@]}"; do
        PDB="${PROTEINS[$name]}"
        if [ -f "$PDB" ]; then
            echo "  ✅ ${name}: found"
        else
            echo "  ❌ ${name}: NOT FOUND at ${PDB}"
            echo "     → Check the filename inside the folder matches exactly"
            ALL_OK=false
        fi
    done
    if [ "$ALL_OK" = false ]; then
        echo ""
        echo "⚠️  Some PDB files missing. Listing actual files in each folder:"
        for name in "${!PROTEINS[@]}"; do
            FOLDER=$(dirname "${PROTEINS[$name]}")
            echo "  ${name}:"
            ls "${FOLDER}"/*.pdb 2>/dev/null || echo "    No PDB files found in ${FOLDER}"
        done
        echo ""
        echo "Update the PROTEINS paths in this script to match the actual filenames."
        exit 1
    fi
}

run_searches() {
    echo ""
    echo "=== Running Foldseek Searches ==="
    mkdir -p "${OUT_DIR}" "${TMP_DIR}"

    for name in "${!PROTEINS[@]}"; do
        PDB="${PROTEINS[$name]}"
        echo ""
        echo "--- ${name} ---"
        PROTEIN_OUT="${OUT_DIR}/${name}"
        mkdir -p "${PROTEIN_OUT}"

        for db in "${DATABASES[@]}"; do
            RESULT="${PROTEIN_OUT}/${name}_vs_${db}.tsv"
            if [ -f "$RESULT" ] && [ -s "$RESULT" ]; then
                echo "  ✅ ${db}: already done"
                continue
            fi
            echo "  Searching vs ${db}..."
            foldseek easy-search \
                "${PDB}" \
                "${DB_DIR}/${db}" \
                "${RESULT}" \
                "${TMP_DIR}" \
                --exhaustive-search 1 \
                --format-output "query,target,prob,evalue,seqid,qlen,tlen,alnlen,qstart,qend,tstart,tend,taxname" \
                -e 10 \
                --num-iterations 3 \
                -v 1
            echo "  ✅ ${db}: done → ${RESULT}"
        done
    done
}

summarize_results() {
    echo ""
    echo "=== Generating Summary ==="
    SUMMARY="${OUT_DIR}/SUMMARY_all_proteins.tsv"
    echo -e "Protein\tDatabase\tTop_Hit\tProbability\tE-value\tSeq_ID(%)\tOrganism" > "${SUMMARY}"

    for name in "${!PROTEINS[@]}"; do
        for db in "${DATABASES[@]}"; do
            RESULT="${OUT_DIR}/${name}/${name}_vs_${db}.tsv"
            if [ -f "$RESULT" ] && [ -s "$RESULT" ]; then
                TOP=$(head -1 "${RESULT}")
                TARGET=$(echo "$TOP" | cut -f2)
                PROB=$(echo "$TOP"   | cut -f3)
                EVAL=$(echo "$TOP"   | cut -f4)
                SEQID=$(echo "$TOP"  | cut -f5)
                TAXNAME=$(echo "$TOP"| cut -f13)
                echo -e "${name}\t${db}\t${TARGET}\t${PROB}\t${EVAL}\t${SEQID}\t${TAXNAME}" >> "${SUMMARY}"
            else
                echo -e "${name}\t${db}\tNo_hits\t-\t-\t-\t-" >> "${SUMMARY}"
            fi
        done
    done

    echo ""
    echo "=== RESULTS SUMMARY ==="
    column -t -s $'\t' "${SUMMARY}"
    echo ""
    echo "✅ Full summary saved to: ${SUMMARY}"
}

# ============================================================
# MAIN
# ============================================================
echo "============================================"
echo " Finger Millet Foldseek Pipeline"
echo " Date: $(date)"
echo "============================================"

install_foldseek
download_databases
check_pdb_files
run_searches
summarize_results

echo ""
echo "============================================"
echo " PIPELINE COMPLETE"
echo " Results: ${OUT_DIR}"
echo "============================================"
