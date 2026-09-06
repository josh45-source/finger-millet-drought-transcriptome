#!/usr/bin/env bash
# ============================================================
#  setup.sh — One-time environment setup
#  Maintainer: see CITATION.cff
#  Project root: taken from $FM_PROJECT, else the directory containing this script
#
#  Run this ONCE after copying pipeline files:
#    bash setup.sh
# ============================================================

set -euo pipefail

echo "============================================"
echo "  Finger Millet Pipeline — Setup"
echo "  $(date)"
echo "============================================"
echo ""

# Project root. Override with:  export FM_PROJECT=/path/to/project
PROJECT="${FM_PROJECT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"

# ── 1. Confirm we're in the right place ──────────────────────
cd "$PROJECT"
echo "✓ Working directory: $(pwd)"

# ── 2. Confirm conda environment ─────────────────────────────
# Locate conda. Override with:  export CONDA_SH=/path/to/conda.sh
source "${CONDA_SH:-$(conda info --base 2>/dev/null)/etc/profile.d/conda.sh}"
conda activate finger_millet
echo "✓ Conda environment: $(conda info --envs | grep '*' | awk '{print $1}')"

# ── 3. Verify all tools ──────────────────────────────────────
echo ""
echo ">>> Verifying tools..."
printf "  %-20s %s\n" "hisat2:"       "$(hisat2 --version | head -1)"
printf "  %-20s %s\n" "samtools:"     "$(samtools --version | head -1)"
printf "  %-20s %s\n" "stringtie:"    "$(stringtie --version)"
printf "  %-20s %s\n" "fastqc:"       "$(fastqc --version)"
printf "  %-20s %s\n" "fasterq-dump:" "$(fasterq-dump --version 2>&1 | head -1)"
printf "  %-20s %s\n" "gffcompare:"   "$(gffcompare --version 2>&1 | head -1)"
printf "  %-20s %s\n" "bedtools:"     "$(bedtools --version | head -1)"
printf "  %-20s %s\n" "blastx:"       "$(blastx -version 2>&1 | head -1)"
printf "  %-20s %s\n" "snakemake:"    "$(conda run -n snakemake snakemake --version)"

# ── 4. Verify project structure ───────────────────────────────
echo ""
echo ">>> Checking project structure..."
REQUIRED=(
    "Snakefile"
    "config.yaml"
    "scripts/de_analysis.R"
    "scripts/merge_results.py"
    "data/raw"
    "data/ref"
    "results/qc"
    "results/trimmed"
    "results/aligned"
    "results/assembled"
    "results/counts"
    "results/novel_genes"
    "results/de_analysis"
    "results/final_report"
    "logs"
)

ALL_OK=true
for ITEM in "${REQUIRED[@]}"; do
    if [[ -e "$ITEM" ]]; then
        echo "  ✓ $ITEM"
    else
        echo "  ✗ MISSING: $ITEM"
        ALL_OK=false
    fi
done

# ── 5. Check disk space ───────────────────────────────────────
echo ""
echo ">>> Disk space:"
printf "  WSL filesystem: "
df -h / | tail -1 | awk '{print $4 " available (" $5 " used)"}'
printf "  D: drive:       "
df -h /mnt/d | tail -1 | awk '{print $4 " available (" $5 " used)"}'

# ── 6. Run dry run ────────────────────────────────────────────
echo ""
echo ">>> Running Snakemake dry run..."
echo "    (This shows what will run — no data downloaded yet)"
echo ""

if conda run -n snakemake snakemake -n --configfile config.yaml 2>&1 | head -40; then
    echo ""
    echo "✓ Dry run passed — pipeline is ready!"
else
    echo ""
    echo "⚠ Dry run found issues — check config.yaml"
    echo "  Most likely: SRR accession numbers not filled in yet"
fi

echo ""
echo "============================================"
echo "  Setup Complete!"
echo ""
echo "  Next steps:"
echo "  1. Search SRA for finger millet datasets:"
echo "     esearch -db sra -query '\"Eleusine coracana\"[Organism]"
echo "     AND \"RNA-Seq\"[Strategy] AND \"drought\"'"
echo ""
echo "  2. Edit config.yaml — fill in real SRR accessions"
echo "     nano config.yaml"
echo ""
echo "  3. Run the pipeline inside screen:"
echo "     screen -S finger_millet"
echo "     snakemake --configfile config.yaml --cores 4"
echo "============================================"
