#!/usr/bin/env bash
# =============================================================================
#  run_blastx_v2.sh -- re-run BLASTx with correct transcript IDs in the headers
#
#  The original run (Snakefile rule blast_novel, 14 Apr 2026) used a FASTA whose
#  headers were written by `bedtools getfasta -name` on a GTF. bedtools wrote the
#  GTF feature type -- the literal string "transcript" -- as the name, so every
#  one of the 21,864 records was called `transcript::<chrom>:<start>-<end>`.
#  merge_results.py then joined those query IDs to a DE table keyed on MSTRG.x.y.
#  The key spaces are disjoint, the how="left" merge assigned NaN to every row,
#  and the pipeline reported 0 annotations. See results_v2/DE_COMPARISON.md section 4.
#
#  This run is IDENTICAL to the original except that the query FASTA headers
#  carry the transcript ID. The sequences are byte-identical -- verified by md5
#  of the sequence-only stream (d2d9c6e535fa1395af38d1ef11f08e88 for both).
#
#  Parameters are taken from config.yaml verbatim:
#      evalue 1e-5, num_threads 4, max_target_seqs 5,
#      outfmt "6 qseqid sseqid pident length evalue bitscore stitle"
# =============================================================================
set -euo pipefail
source "${CONDA_SH:-$(conda info --base 2>/dev/null)/etc/profile.d/conda.sh}"
conda activate "${FM_ENV:-finger_millet}"
cd "${FM_ROOT:-.}"

OUT=results_v2/blast/blast_results_v2.txt
LOG=results_v2/logs/blastx_v2.log

echo "START $(date -Is)"            | tee -a "$LOG"
echo "blastx $(blastx -version | head -1)" | tee -a "$LOG"
echo "query: results_v2/blast/novel_transcripts_named.fa ($(grep -c '>' results_v2/blast/novel_transcripts_named.fa) records)" | tee -a "$LOG"

/usr/bin/time -v blastx \
    -query results_v2/blast/novel_transcripts_named.fa \
    -db data/ref/uniprot_db \
    -out "$OUT" \
    -outfmt "6 qseqid sseqid pident length evalue bitscore stitle" \
    -evalue 1e-5 \
    -num_threads 4 \
    -max_target_seqs 5 \
    2>> "$LOG"

echo "END $(date -Is)"              | tee -a "$LOG"
echo "hits: $(wc -l < "$OUT")"      | tee -a "$LOG"
echo "queries with >=1 hit: $(cut -f1 "$OUT" | sort -u | wc -l)" | tee -a "$LOG"
touch results_v2/blast/BLASTX_DONE
