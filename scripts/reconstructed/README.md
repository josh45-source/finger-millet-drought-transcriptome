# `scripts/reconstructed/` — recovered artefacts, not maintained source

**These twenty scripts were never saved to disk during the analysis.** They were typed
directly into an interactive shell as `python3 << 'EOF' … EOF` heredocs and survive only
as text inside the author's `~/.bash_history`. They were extracted on 19 August 2026 and
are reproduced here **byte-for-byte verbatim** — nothing corrected, reformatted, improved
or sanitised. Indentation, comments, spelling, hard-coded values and any bugs are exactly
as executed. Only a provenance header has been prepended to each file, recording its
source line range and the pipeline stage it belongs to.

Verbatim status is verified, not asserted: each file's body has been compared byte-for-byte
against the recorded `~/.bash_history` line range, and **all twenty match exactly**. The
check was repeated on 28 August 2026 with the same result.

## They are not sanitised, and this is deliberate

Unlike the maintained source files in `../` — where machine-specific paths were replaced
with documented environment variables for deposition — **these files retain everything
that was in them at execution time**:

- **Absolute paths specific to the author's machine**, including `/mnt/d/finger_millet_project`
  in every provenance header and relative paths that assume a particular working directory.
- **The author's username**, in paths and comments.
- **The email address `joshua@research.com`.** This appears in
  `heroGene03_ncbi_blastp_web_submit_v2.py` and is a **placeholder** supplied to satisfy
  the required contact field of the EBI REST API, which rejects submissions without one.
  It is not a working mailbox and was never used to receive correspondence.

Sanitising these files would destroy the only thing that makes them worth depositing.
Their evidentiary value lies entirely in being an exact record of what was run — a
corrected version would be a reconstruction of a reconstruction, and no reader could
tell which lines were original. **They are retained unmodified for provenance and are
not intended to run elsewhere without adaptation.**

## Before running any of them

1. **Paths.** Scripts reference `results/…`; this package stores those files under
   `results_v1/…`. Rename or symlink `results_v1` → `results` at the package root first.
2. **Working directory.** `stage06d` and `stage06e` were run from inside
   `results/transdecoder/`, not the project root. Others assume the project root.
3. **Chain order.** Several read files that other scripts in this directory produce.
   `stage06a` must run before `stage06b`/`06c`/`06d`/`08a` (it creates `top50_ids.txt`);
   `stage11b` before `stage11c`.
4. **Missing inputs.** `stage10a`, `stage10b` and `stage10c` require
   `results/counts/*_counts.gtf` (~600 MB), which is not deposited. They cannot run from
   this package alone.
5. **Hard-coded values.** The ten-candidate list is hard-coded in `stage08b`, `stage10a`,
   `stage10d` and `stage11a`–`11d` rather than read from `top50_ids.txt`.
   `stage08b` additionally hard-codes genomic coordinates, and **`stage10d` hard-codes its
   entire expression matrix as Python literals** — re-running it replays the published
   correlations but does not re-derive them from count data. Those literals were
   independently checked against `results/counts/*.gtf` during the audit; all ten
   candidate vectors matched exactly.

## Citing

**These must not be cited as original source code.** They are recovered artefacts. If you
need to refer to the analysis they performed, cite the deposition record (see
`../../CITATION.cff`) and identify the stage.

Full per-script detail — source line ranges, stage, purpose and outputs — is in
`../../docs/MANIFEST.md` §7.
