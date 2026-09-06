#!/usr/bin/env python3
"""
rebuild_annotation_v2.py -- rebuild the candidate annotation table with a clean
join on transcript ID.

WHY THIS EXISTS
---------------
The original scripts/merge_results.py joined the DE table (keyed on MSTRG.x.y)
to results/novel_genes/blast_results.txt, whose query IDs were the literal
string "transcript" plus coordinates -- because `bedtools getfasta -name` was
given a GTF and wrote the feature type as the name. The two key spaces are
disjoint, so the how="left" merge assigned NaN to every row and the pipeline
reported 0 annotations for all 2,354 candidates.

This script consumes results_v2/blast/blast_results_v2.txt, produced from a
re-extraction whose headers carry the transcript ID (sequences byte-identical
to the original, md5 d2d9c6e535fa1395af38d1ef11f08e88), and joins on the real
transcript ID.

The tier rules are reproduced verbatim from merge_results.py, including its
STRESS_WORDS list. Two tier schemes are emitted:

  tier3  -- exactly merge_results.py's function, which can only ever return
            three strings. Kept so the original logic is auditable.
  tier4  -- the four-string scheme actually present in
            results/final_report/candidate_genes_final.tsv, which splits
            merge_results.py's collapsed "Tier 3 -- other/no homolog" bucket
            into "Tier 1 -- no homolog" and "Tier 3 -- other homolog".
            This is what the lost hand-edited script must have done, and it is
            the scheme the preprint tables use.

Writes to results_v2/ only. Nothing under results/ is modified.
"""
import csv, sys, os, json
from collections import defaultdict

# Package root. Override with:  export FM_ROOT=/path/to/package
P = os.environ.get("FM_ROOT", ".")
BLAST   = f"{P}/results_v2/blast/blast_results_v2.txt"
NEW_UP  = f"{P}/results_v2/de/drought_upregulated_novel_genes_v2.tsv"
OLD_UP  = f"{P}/results/final_report/candidate_genes_final.tsv"
NOVEL   = f"{P}/results_v2/counts/novel_class_u_ids.txt"
OUTDIR  = f"{P}/results_v2/annotation"
os.makedirs(OUTDIR, exist_ok=True)

# ---- verbatim from scripts/merge_results.py -------------------------------
STRESS_WORDS = [
    "drought","stress","dehydration","osmotic","ABA",
    "abscisic","desiccation","water deficit","LEA",
    "late embryogenesis","aquaporin","peroxidase","kinase"
]

def tier3(has_hit, ann, lfc):
    """merge_results.py's tier() exactly as written. Emits 3 strings."""
    is_stress = has_hit and any(w.lower() in ann.lower() for w in STRESS_WORDS)
    if not has_hit and lfc >= 3:
        return "Tier 1 — Novel, no homolog, highly induced"
    elif is_stress:
        return "Tier 2 — Novel, stress-related homolog"
    else:
        return "Tier 3 — Novel, other/no homolog"

def tier4(has_hit, ann, lfc):
    """The 4-string scheme used in candidate_genes_final.tsv."""
    is_stress = has_hit and any(w.lower() in ann.lower() for w in STRESS_WORDS)
    if is_stress: return "Tier 2 — Novel, stress-related homolog"
    if has_hit:   return "Tier 3 — Novel, other homolog"
    if lfc >= 3:  return "Tier 1 — Novel, no homolog, highly induced"
    return "Tier 1 — Novel, no homolog"

# ---- best BLAST hit per transcript ---------------------------------------
# outfmt: qseqid sseqid pident length evalue bitscore stitle
best = {}
n_lines = 0
with open(BLAST) as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 7:
            continue
        n_lines += 1
        qid = p[0].split("::", 1)[0]          # MSTRG.x.y::chrom:start-end -> MSTRG.x.y
        try:
            ev, bs = float(p[4]), float(p[5])
        except ValueError:
            continue
        cur = best.get(qid)
        # same ordering as merge_results.py: evalue ascending, bitscore descending
        if cur is None or (ev, -bs) < (cur["evalue"], -cur["bitscore"]):
            best[qid] = {"subject_id": p[1], "pident": p[2], "length": p[3],
                         "evalue": ev, "bitscore": bs, "annotation": p[6]}

novel_ids = set(open(NOVEL).read().split())
print(f"BLAST lines parsed          : {n_lines:,}")
print(f"transcripts with >=1 hit    : {len(best):,}")
print(f"  of which class-code u     : {len(set(best) & novel_ids):,} of {len(novel_ids):,} "
      f"({100*len(set(best) & novel_ids)/len(novel_ids):.1f}%)")

def annotate(rows, lfc_key, out_path, label):
    counts3, counts4 = defaultdict(int), defaultdict(int)
    hits = 0
    fields = list(rows[0].keys()) + ["subject_id","pident","aln_length","evalue",
                                     "bitscore","annotation","candidate_tier",
                                     "candidate_tier_merge_results_py"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            t = r["transcript_id"]
            b = best.get(t)
            has = b is not None
            hits += has
            ann = b["annotation"] if has else ""
            lfc = float(r[lfc_key])
            t4 = tier4(has, ann, lfc); t3 = tier3(has, ann, lfc)
            counts4[t4] += 1; counts3[t3] += 1
            r = dict(r)
            r.update({"subject_id": b["subject_id"] if has else "",
                      "pident": b["pident"] if has else "",
                      "aln_length": b["length"] if has else "",
                      "evalue": b["evalue"] if has else "",
                      "bitscore": b["bitscore"] if has else "",
                      "annotation": ann,
                      "candidate_tier": t4,
                      "candidate_tier_merge_results_py": t3})
            w.writerow(r)
    n = len(rows)
    print(f"\n=== {label}: {n:,} transcripts ===")
    print(f"  with BLAST hit : {hits:,} ({100*hits/n:.1f}%)")
    print(f"  NO homology    : {n-hits:,} ({100*(n-hits)/n:.1f}%)   <-- the headline number")
    print("  tier distribution (4-tier, as in candidate_genes_final.tsv):")
    for k in sorted(counts4, key=lambda k: -counts4[k]):
        print(f"    {counts4[k]:6,}  {k}")
    print("  tier distribution (merge_results.py's own 3-tier function):")
    for k in sorted(counts3, key=lambda k: -counts3[k]):
        print(f"    {counts3[k]:6,}  {k}")
    return {"n": n, "hits": hits, "no_hit": n-hits,
            "tier4": dict(counts4), "tier3": dict(counts3)}

summary = {}
with open(NEW_UP) as f:
    new_rows = list(csv.DictReader(f, delimiter="\t"))
summary["reanalysis"] = annotate(new_rows, "log2FoldChange_MLE",
    f"{OUTDIR}/candidate_genes_v2_annotated.tsv",
    "RE-ANALYSIS novel drought-up (2,422)")

with open(OLD_UP) as f:
    old_rows = list(csv.DictReader(f, delimiter="\t"))
summary["original"] = annotate(old_rows, "log2FoldChange",
    f"{OUTDIR}/candidate_genes_original_reannotated.tsv",
    "ORIGINAL novel drought-up (2,354), re-annotated")

# all 21,864 novel transcripts, annotation only
with open(f"{OUTDIR}/novel_transcripts_best_hit.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["transcript_id","subject_id","pident","aln_length","evalue","bitscore","annotation"])
    for t in sorted(novel_ids):
        b = best.get(t)
        w.writerow([t] + ([b["subject_id"], b["pident"], b["length"], b["evalue"],
                           b["bitscore"], b["annotation"]] if b else [""]*6))

summary["all_novel"] = {"n": len(novel_ids), "hits": len(set(best) & novel_ids)}
json.dump(summary, open(f"{OUTDIR}/summary.json","w"), indent=1)
print(f"\nWrote {OUTDIR}/")
