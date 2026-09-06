# Archive — superseded and historical manuscript files

**`../finger_millet_preprint_v2.md` is the live draft.** It is the only manuscript file
outside this directory and the only one that should be edited, cited or circulated.
Nothing in this directory is current, in any format.

---

## Contents

### The historical record — unmodified 17 April 2026 text

| File | Status |
|---|---|
| `finger_millet_preprint_ORIGINAL_17Apr2026.md` | Unmodified 17 April 2026 text of the v1 draft. |
| `finger_millet_preprint_v2_ORIGINAL_17Apr2026.md` | Unmodified 17 April 2026 text of the v2 draft. |
| `finger_millet_preprint_ORIGINAL_17Apr2026.html` | **Stale HTML rendering of the pre-correction text. Must not be circulated.** |
| `finger_millet_preprint_v2_ORIGINAL_17Apr2026.html` | **Stale HTML rendering of the pre-correction text. Must not be circulated.** |

These four files are retained **unchanged** as the historical record of what was written
before the August 2026 audit — the two markdown drafts and the pandoc HTML rendering of
each. They have never been edited and must not be. They still contain the uncorrected
claims — most conspicuously the **99.6% no-homology rate**, which was an artefact of a
broken database join and whose true value is **63.3%** — together with every other claim
later revised. They are preserved so that the corrections can be audited against the text
they corrected, not because that text is believed. See the note on the HTML files below.

Every correction applied to them is itemised in `docs/MANUSCRIPT_CORRECTIONS.md` of the
accompanying Zenodo deposit.

### The superseded corrected draft

| File | Status |
|---|---|
| `finger_millet_preprint.md` | Corrected v1 draft. **Superseded by `../finger_millet_preprint_v2.md`.** |

This is the earlier of the two drafts, corrected in place during the August 2026 audit and
again on 5 September 2026. It duplicates the live v2 draft with less detail and adds
nothing to it. It is kept **only so that no uncorrected version of the manuscript exists
on disk** — retiring it by deletion would have been fine, but retiring it by correction
means that anyone who finds a stray copy of the v1 text has a corrected counterpart to
compare against. It is not a draft under development and should not be taken forward.

---

## The two HTML renderings

**These are stale HTML renderings of the pre-correction text and must not be circulated.**

Both were produced by pandoc on 17 April 2026 and render the ORIGINAL markdown archived
here, **not** the corrected drafts. Both still state the **99.6%** figure. Neither has been
regenerated since.

Until 5 September 2026 they sat in the parent directory under the *live* file names —
`finger_millet_preprint.html` and `finger_millet_preprint_v2.html` — so that opening the
apparently-current v2 HTML gave the uncorrected paper. They were moved here and renamed to
the `_ORIGINAL_17Apr2026` convention to remove that trap. **The parent directory now
contains exactly one manuscript file, `finger_millet_preprint_v2.md`, and no HTML at all.**

If an HTML copy is needed, regenerate it from `../finger_millet_preprint_v2.md`; do not
reuse these.

---

*Directory created 5 September 2026.*
