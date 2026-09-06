# Reference-guided transcriptome analysis of finger millet (*Eleusine coracana*) identifies 2,422 drought-associated transcripts absent from the current annotation

**Joash Joshua Ayo¹**

¹ Independent Researcher, Kampala, Uganda

**Corresponding author:** joashjoshua789@gmail.com

**ORCID:** [0009-0007-1642-0172](https://orcid.org/0009-0007-1642-0172)

**Keywords:** finger millet, *Eleusine coracana*, drought stress, RNA-seq, reference-guided assembly, intergenic transcribed regions, transcriptome annotation

---

> **Revision note — 28 August 2026, retired 5 September 2026.** This is the earlier of two
> drafts, corrected in place. The 17 April 2026 text is retained unchanged as
> `finger_millet_preprint_ORIGINAL_17Apr2026.md` in this directory.
>
> **This draft is RETIRED. `../finger_millet_preprint_v2.md` is the live draft and is the
> one to take forward.** This file has been corrected so that no uncorrected version of
> the manuscript remains on disk, but it duplicates v2 with less detail and is not under
> development. See `README.md` in this directory.
>
> An audit of the underlying workflow found four software defects and the analysis was
> re-run. Every quantitative claim has been recomputed. The previously reported figure of
> **99.6% of transcripts lacking a characterised homolog was an artefact of a broken
> database join**; the true figure is **63.3%**. Corrections are itemised in
> `docs/MANUSCRIPT_CORRECTIONS.md` of the accompanying deposit.

---

## Abstract

Finger millet (*Eleusine coracana* (L.) Gaertn.) is a drought-tolerant C₄ cereal of significant importance across sub-Saharan Africa and South Asia. Previous transcriptomic studies relied on de novo assembly in the absence of a chromosome-scale reference, limiting the discovery of unannotated genes. Here we present a reference-guided reanalysis of drought-response RNA-seq against the chromosome-scale KNE 796-S assembly (GCA_032690845.1). Using a Snakemake pipeline integrating HISAT2, StringTie, GFFCompare and DESeq2, we analysed publicly available RNA-seq from control and drought-sampled leaf tissue (DDBJ accession DRS049651). We detected 21,864 transcripts absent from the current annotation, of which 2,422 were significantly upregulated in drought-sampled tissue (adjusted p < 0.05, log₂FC ≥ 1.5). Of these, 1,532 (63.3%) had no significant homology to any characterised protein in UniProt/Swiss-Prot — a rate consistent with published expectations for intergenic transcribed regions in the grasses, and therefore not evidence of an unusual gene repertoire. The annotated remainder is dominated by mobile elements (203 transcripts, 8.4% of the set) and by conserved nucleolar ribosome-biogenesis factors that the reference annotation has missed. One candidate withstands re-examination: MSTRG.31255.1, a single-exon locus on chromosome 6A encoding a 104-amino-acid secreted cysteine-rich peptide, with a tandem paralog and a 6B homoeologue, no Swiss-Prot homolog, and 27 uncharacterised homologs across seven grass genera. Because the control and drought tissue were sampled seven days apart with no time-matched well-watered control, treatment is confounded with plant age; these results are hypothesis-generating.

---

## 1. Introduction

Drought stress is a foremost constraint on global food security (FAO, 2023). Finger millet (*Eleusine coracana* (L.) Gaertn.) is an allotetraploid C₄ cereal (2n = 4x = 36, AABB genome) cultivated by smallholder farmers across more than 25 countries and valued for its tolerance of water deficit (Upadhyaya et al., 2007; Vetriventhan et al., 2015). It remains underrepresented in genomic databases relative to major cereals.

The molecular basis of drought tolerance in finger millet involves osmotic adjustment, ROS scavenging, ABA signalling and protein protection (Parvathi et al., 2019). Earlier transcriptomic work identified CIPK31, PP2A, FPS and TAF6 as drought-responsive (Parvathi et al., 2013, 2019), but employed de novo assembly without a reference genome, which constrains identification of unannotated genes and introduces assembly artefacts.

A chromosome-scale assembly for *E. coracana* (GCA_032690845.1, cultivar KNE 796-S, 2023) now enables reference-guided approaches. Here we catalogue transcripts absent from the current annotation that are upregulated in drought-sampled tissue, and **distinguish genuinely uncharacterised loci from two categories that superficially resemble them: mobile elements, and conserved genes the annotation has missed.**

---

## 2. Materials and Methods

### 2.1 RNA-seq Data

RNA-seq data were obtained from DDBJ under accession DRS049651 (BioProject PRJDB5606; Hatakeyama et al., 2018): paired-end Illumina reads from leaf tissue of *E. coracana* subsp. *coracana* sampled under well-watered conditions (n = 3; DRR095904–906) and after seven days of withheld water (n = 3; DRR095907–909). FASTQ files were downloaded from ENA.

Condition assignment follows the ENA library names (`Illumina_RNA_ctl_1-3`, `Illumina_RNA_dry_1-3`), assuming run accessions map in order.

The plants were grown from a highly inbred seed stock obtained from GKVK Bangalore and originally sourced from ICRISAT, so the sampled individuals are expected to be genetically very similar. Within each sampling group the three libraries were prepared from **separate plants**, so the replication is biological rather than technical; this is not recorded in the archive metadata, where all 18 runs of PRJDB5606 share a single BioSample (SAMD00076255). The libraries were generated primarily to support genome annotation rather than as a designed differential-expression experiment — the study is titled "Finger millet genome assembly" — and no growth protocol, drought severity or timepoint is recorded, nor was detailed environmental information for the growth period, including watering amount and timing and temperature, retained (§4.6).

### 2.2 Reference Genome

GCA_032690845.1 (*Eleusine_coracana_v1.0*, cv. KNE 796-S) and its GFF3 annotation were downloaded from NCBI. The assembly comprises **532 sequences: 18 pseudomolecules** (1A/1B–9A/9B, resolving both subgenomes) plus 514 unplaced scaffolds, **1,111,714,373 bp**, N50 61,270,980 bp.

> This is **not** the assembly described by Hatakeyama et al. (2018), which is a short-read
> assembly of a different accession. That paper is the correct citation for the RNA-seq
> data, not for the genome.

### 2.3 Quality Control and Read Trimming

FastQC v0.12.1 and MultiQC v1.33. Trimmomatic v0.40, paired-end: ILLUMINACLIP:TruSeq3-PE.fa:2:30:10, LEADING:3, TRAILING:3, SLIDINGWINDOW:4:15, MINLEN:36.

### 2.4 Read Alignment

HISAT2 v2.2.2: --score-min L,0,-0.5, --no-mixed, --no-discordant, --mp 4,2, --rdg 5,3, --rfg 5,3, --rna-strandness RF, --dta, --min-intronlen 20, --max-intronlen 500000. Filtered at MAPQ ≥ 20 with SAMtools v1.23.1 and coordinate-sorted. The MAPQ filter discards reads mapping ambiguously between the A and B subgenomes.

### 2.5 Transcript Assembly and Detection of Unannotated Transcripts

StringTie v3.0.0 per sample, guided by the reference annotation, merged with `--merge`. GFFCompare v0.12.10 identified transcripts absent from the annotation; class code "u" (intergenic, no overlap with any annotated feature) was retained.

> **Terminology.** These are *transcripts absent from the current annotation*, not "novel
> genes". Class code "u" records absence from an annotation file, not novelty.

### 2.6 Differential Expression Analysis

Counts were generated with `prepDE.py` (StringTie 3.0.0) from the per-sample `stringtie -e -B` output at the **measured mean aligned read length of 142 bp**, and validated against `featureCounts` (subread v2.1.1; `-p --countReadPairs -B -C -s 2`) at **Spearman ρ = 0.985–0.995** across all six samples.

DESeq2 v1.50.2 under R v4.5.3, design `~ condition`, contrast drought versus control, prefilter `rowSums(counts) ≥ 10`. Significance at adjusted p < 0.05 (Benjamini–Hochberg) and log₂FC ≥ 1.5 on the unshrunk MLE; `lfcShrink(type="apeglm")` (apeglm v1.32.0) reported alongside.

A paired design (`~ plant + condition`) was fitted and **rejected**: it increased dispersion (asymptotic dispersion 0.786 → 0.880) and cost 8,239 transcripts their testability. All six possible pairings absorb 49.1–51.0% of within-condition variance, so the library-name suffixes do not encode plant identity; nor can the pairing be established from the surviving experimental records, so the six libraries are treated as independent samples (§4.6).

### 2.7 Sequence Extraction and Homology Search

Genomic sequences were extracted with BEDTools v2.31.1 `getfasta` and searched with BLASTx (BLAST+ v2.17.0) against UniProt Swiss-Prot (574,627 sequences; 208,482,574 residues) at E ≤ 1×10⁻⁵, `-max_target_seqs 5`, `-outfmt 6`. Best hit per transcript by ascending E-value then descending bit score.

> **Extraction caveat.** The GTF used for extraction retained transcript records but no exon
> records, so extracted sequences are whole genomic intervals **including introns**. 47 of
> the top 50 candidates are multi-exon. Single-exon candidates, including MSTRG.31255.1,
> are unaffected (§4.6).

### 2.8 Protein-coding Potential and Domain Annotation

TransDecoder v5.7.1 on the top 50 candidates by adjusted p-value (`-m 100`, `--single_best_only`). Peptides were submitted to the InterProScan 5 web service at EBI (job `iprscan5-R20260417-190817-0777-66196655-p1m`); the service version is not recorded in the output.

### 2.9 Candidate Stratification

- **Tier 1 — no Swiss-Prot homolog**, subdivided at log₂FC ≥ 3
- **Tier 2 — homolog matching a stress-associated keyword**
- **Tier 3 — homolog of other function**

> **A coarse triage, not a functional classification.** Tier 2 is a word-boundary keyword
> match; 46 of the 50 Tier 2 assignments arise from the single word "kinase". It should be
> rebuilt by curation before being used to prioritise experiments.

### 2.10 Reproducibility and Code Availability

Implemented as a Snakemake v9.19.0 pipeline with conda-managed environments. Code, count matrices, result tables, structural models and a full record of corrections are deposited [Zenodo DOI — to be added].

---

## 3. Results

### 3.1 RNA-seq Quality and Alignment

After trimming, between 17.1 and 32.5 million read pairs per sample were retained. Alignment rates ranged from 85.13% to 96.22%, mean 92.05% (Table 1). Assigned fragment counts differ between groups (control 18.5–22.0 M; drought 21.0–36.4 M), so depth is partially confounded with condition (§3.6).

### 3.2 Transcripts Absent from the Current Annotation

GFFCompare identified **21,864 transcripts** with class code "u". BLASTx returns a significant Swiss-Prot hit for **6,106 of these (27.9%)**.

### 3.3 Differential Expression

DESeq2 identified **2,422 transcripts significantly upregulated in drought-sampled tissue** (adjusted p < 0.05, log₂FC ≥ 1.5). The smallest adjusted p-value is **1.37 × 10⁻³⁷**. Applying the threshold to apeglm-shrunk estimates gives 2,218.

The three most significant are MSTRG.45758.1 (log₂FC 3.14, padj 9.25 × 10⁻³⁸), MSTRG.6647.1 (3.36, 1.04 × 10⁻³⁷) and MSTRG.20738.1 (2.59, 1.37 × 10⁻³⁷). **The first is a retrotransposon and the third a nucleolar rRNA-processing factor** (§3.5, §3.8).

### 3.4 Homology: 63.3% Without a Characterised Homolog

**1,532 of 2,422 (63.3%) had no significant Swiss-Prot homology**; 890 (36.7%) did.

| Tier | Description | Count |
|------|-------------|-------|
| Tier 1 | No homolog, highly induced (log₂FC ≥ 3) | 1,184 |
| Tier 1 | No homolog | 348 |
| Tier 2 | Stress-keyword homolog | 50 |
| Tier 3 | Other homolog | 840 |
| **Total** | | **2,422** |

**This rate is unremarkable.** Lloyd et al. (2019) found only 16–23% of intergenic transcribed regions had detectable protein similarity — i.e. 77–84% did not. Our set is better annotated than that background. **No claim of an unusual or lineage-specific gene repertoire is supportable.**

> **An earlier version reported 99.6% (2,344 of 2,354).** That was a software defect.
> Sequence extraction wrote the GTF feature type — the literal string `transcript` — as the
> FASTA header, so BLASTx query identifiers could never match the expression table's
> transcript IDs, and the left join assigned a null annotation to every row. Re-running
> BLASTx with correct identifiers produced output byte-identical to the original in every
> field except the query name.

### 3.5 A Substantial Fraction Is Mobile-Element Derived

**203 of 2,422 (8.4%)** have a best hit to a transposon, retrovirus-related polyprotein, integrase, reverse transcriptase or LINE-1 element; **eight of the top 50** fall in this class. MSTRG.45758.1, the most significant transcript in the dataset, matches Transposon Tf1-107 polyprotein (E = 4.5 × 10⁻⁷²); MSTRG.4687.1 matches Transposon Tf2-6 polyprotein (E = 2.0 × 10⁻¹⁰⁶). Both are corroborated independently by InterProScan (Pfam integrase core PF00665, integrase zinc-binding PF17921, RNase H-like RT PF17917, CDD `RNase_HI_RT_Ty3`) and by Foldseek.

No repeat-masking was performed prior to assessment. **Comparable studies should mask repeats before interpreting unannotated transcripts as candidate genes.**

### 3.6 Detection Asymmetry Is Not a Depth Artefact

Drought libraries detect 74,000–79,000 transcripts versus 56,000–62,000 in control, and 1,278 of the 2,422 (52.8%) have zero counts in all three control libraries. Tested directly: DRR095905 (control) and DRR095909 (drought) differ in library size by 0.08% yet differ by 31.8% in transcripts detected, and 1,232 of the 1,278 (96.4%) are detected in DRR095909 alone with a median 231 fragments. **Depth is excluded.** Whether the asymmetry is biological or a library-preparation difference between collection dates cannot be determined.

**Fold changes for transcripts with zero control counts are not identifiable** and are reported as lower bounds only.

### 3.7 Protein-coding Potential

TransDecoder identified ORFs ≥ 100 aa in **44 of the top 50 (88%)**. The six without (MSTRG.14681.1, MSTRG.46022.1, MSTRG.14947.1, MSTRG.45098.4, MSTRG.6129.1, MSTRG.26934.1) were previously described as long non-coding RNAs. **That classification does not survive: five of the six have Swiss-Prot protein homologs** — Dormancy-associated protein homolog 1, small ribosomal subunit protein uS14, mitochondrial import receptor TOM6, histone deacetylase HDT2, and hydrophobic protein LTI6B respectively. The absence of a predicted ORF reflects ORF-calling on unspliced genomic sequence (§2.7). **No lncRNA claim is made.**

### 3.8 Domain Annotation of Selected Candidates

**MSTRG.31255.1** (log₂FC 4.43, padj 1.56 × 10⁻³²): signal peptide predicted at residues 1–28 (SignalP-EUK) and 1–32 (Phobius), with residues 33–104 annotated extracellular. **Secreted, not membrane-associated** — SignalP-EUK returns `SignalP-noTM`, and the TMHMM helix at 7–29 lies inside the signal peptide.

**MSTRG.20738.1** (log₂FC 2.59): ARM/Armadillo repeat confirmed (SUPERFAMILY SSF48371, E = 1.5 × 10⁻⁹). **Not a no-homolog transcript** — BLASTx matches *Arabidopsis* At3g06530 at E = 2.2 × 10⁻⁸⁴, and PANTHER assigns BAP28 / UTP10. **It is a nucleolar rRNA-processing factor.** The earlier interpretation invoking the ABA receptor complex and proteasomal degradation was unsupported and is withdrawn.

**MSTRG.6647.1** (log₂FC 3.36): no Swiss-Prot hit; PANTHER assigns MYB-binding protein 1A (PTHR13213, E = 4.0 × 10⁻⁹⁷). **MYBBP1A is a nucleolar ribosome-biogenesis protein, not a partner of plant drought MYB transcription factors.** With MSTRG.20738.1, MSTRG.4655.1 (UTP20) and MSTRG.18418.1 (NOC3), **four of the top ten encode nucleolar machinery** — consistent with a change in growth rate rather than a drought-protective programme.

**MSTRG.21998.1** (log₂FC 2.98): PIP-kinase domain confirmed by five databases (Pfam PF01504, PANTHER PTHR45748, SMART SM00330, ProSiteProfiles PS51455, Gene3D). **The enzyme is FAB1D, a PI3P 5-kinase** (BLASTx E = 5.3 × 10⁻⁹⁹), governing vacuolar and endosomal trafficking — **not the PI(4,5)P₂-generating PIP5Ks that regulate stomatal closure**, as previously stated. It has blastn hits in all three comparison species and is therefore not lineage-specific, and its 420 aa ORF requires re-derivation from a spliced transcript.

**MSTRG.37761.2**, previously described as "~730-fold induced", is **~87-fold** (log₂FC 6.45, down from 9.51; padj 2.49 × 10⁻⁴), with baseMean 11.9, zero counts in all three controls, and rank 1,191.

---

## 4. Discussion

### 4.1 Advantages and Limits of the Reference-Guided Approach

Reference-guided assembly anchors transcripts to genomic coordinates, eliminates many chimeras, enables strand-specific analysis and permits homoeolog-aware interpretation in a polyploid. The 21,864 class-"u" transcripts show the *E. coracana* annotation is incomplete, as expected for a recently released assembly of an orphan crop. What the approach does **not** establish is that these are novel genes.

### 4.2 The Uncharacterised Fraction Requires No Special Explanation

An earlier version treated a 99.6% no-homology rate as a finding and offered three explanations: phylogenetic distance of Chloridoideae from model species, divergence below the detection threshold, and de novo gene birth. **At 63.3% there is no phenomenon to explain.** The composition of the annotated 36.7% is more informative than the size of the unannotated fraction: it is dominated by mobile elements and by conserved housekeeping machinery the annotation has missed.

### 4.3 Candidates for Functional Validation

The corrections remove most previously prioritised candidates: MSTRG.45758.1 and MSTRG.4687.1 are retrotransposons; MSTRG.20738.1 and MSTRG.6647.1 are nucleolar factors; MSTRG.21998.1 is a conserved FAB1 homolog needing ORF re-derivation; MSTRG.37761.2 is a low-count transcript at ~87-fold.

**One candidate survives: MSTRG.31255.1.** Single-exon on chromosome 6A (16,937,315–16,938,027, minus strand); complete 104 aa ORF with genuine start and stop; predicted signal peptide and extracellular mature region; log₂FC 4.43, padj 1.56 × 10⁻³², rank 4 of 2,422, stable across the unpaired model, the paired model and apeglm shrinkage; counts 26/33/46 in control versus 2,785/1,662/1,086 in drought, a real ratio rather than a division by zero; no Swiss-Prot homolog under the corrected join.

Its ColabFold MSA contains **27 distinct homologs** (32 alignment rows, 5 exact duplicates) across **seven grass genera and twelve species in three subfamilies** — *Oryza* (six species), *Leersia*, *Setaria*, *Dichanthelium*, *Sorghum*, *Zea*, *Arundo* — 23 annotated only as "uncharacterized protein", every UniProt-derived row an unreviewed TrEMBL entry absent from Swiss-Prot. All share an invariant C-terminal cysteine module. tblastn recovers a tandem paralog 4.4 kb upstream on 6A (79.3% identity) and a homoeologous copy on 6B (88.6%), consistent with the AABB structure; none of the family is annotated.

This supports **a small secreted cysteine-rich protein family conserved across the grasses and uncharacterised throughout** — not a finger millet-specific protein. No Chloridoideae sequence appears in the alignment, so subfamily-level conservation is untested.

The AlphaFold2 model is **low confidence** (mean pLDDT 59.95, pTM 0.390, MSA depth 34; only residues ~66–104 above pLDDT 70, 41 of 104 below 50) and supports a disulfide-stabilised C-terminal module and nothing more.

### 4.4 The Cross-species Screen Is Underpowered

The screen used blastn at E ≤ 1e-5 against three genomes with `-max_target_seqs 1`, which does not reliably return the best hit. For MSTRG.31255.1 it returned no hits, yet protein-level alignment recovers 27 homologs at 22–34% identity — a divergence at which nucleotide alignment fails regardless of threshold. **Every lineage-specificity call inherits this limitation.** No collinearity or orthology assignment was performed; the three comparison genomes are Panicoideae and Oryzoideae, with no Chloridoideae included. Absence of a BLAST hit is not evidence of gene absence.

### 4.5 What Would Make This Conclusive

1. tblastn against Chloridoideae genomes (*E. indica*, *O. thomaeum*)
2. RT-PCR across the exon structure and 5′/3′ RACE, then ORF re-derivation from a spliced sequence
3. qRT-PCR in a designed drought experiment **with a time-matched well-watered control**
4. Repeat-masked reanalysis
5. Peptide-level confirmation of secretion

### 4.6 Limitations

**Treatment is confounded with plant age.** No time-matched well-watered control was sampled at day seven: controls were taken at the start of the experiment and the drought samples after seven days of withheld water. Every transcript reported here as drought-responsive is equally consistent with being development-responsive. Detailed environmental information for the growth period — watering amount and timing, temperature — was not retained. This is the largest single constraint on the interpretation.

**The six libraries are treated as independent samples.** Whether the control and drought libraries derive from the same individual plants cannot be established, from either the data or the surviving experimental records; the original laboratory notes no longer exist. A surviving sample-name table pairs matched replicate numbers with a `_D` suffix for the drought samples, which suggests an intended correspondence, but no documentation confirms that the same individuals were sampled twice. The pairing is not sufficiently documented to treat the design as confirmed repeated measures, and all six possible pairings absorb an indistinguishable 49.1–51.0% of within-condition variance, so none is recoverable from the counts either. Treating the libraries as independent, as `~ condition` does, is the appropriate choice.

**Replication is biological, and dispersion is extreme** (asymptotic dispersion 0.786, ~89% CV at high expression, 20–80× typical). The three libraries per condition come from separate plants, though this is not recorded in the archive metadata (one BioSample for 18 runs). The dispersion reflects genuine between-plant variation in material not collected under a controlled experimental protocol; genetic heterogeneity is largely excluded, since the plants derive from highly inbred seed (§2.1), which makes the magnitude more notable rather than less. **P-values should not be quoted to better than an order of magnitude.**

**The libraries were not generated for this experiment** — they were produced primarily to support genome annotation.

**All extracted sequences are unspliced**, affecting ORF prediction, domain annotation and the cross-species screen, but not the differential expression analysis, which used the exon-aware merged assembly.

**The candidate list has an untraced step**: the table from which the top 50 were selected has no recorded generating script. This is disclosed, and the file is deposited.

**Computational analysis only.** No experimental validation; not peer reviewed.

---

## 5. Conclusions

Reference-guided reanalysis identifies 2,422 transcripts absent from the current finger millet annotation and upregulated in drought-sampled tissue. Of these, 63.3% have no characterised homolog — a rate consistent with published expectations for intergenic transcribed regions, not evidence of an unusual gene repertoire. The annotated remainder is dominated by mobile elements (8.4% of the whole set) and conserved nucleolar machinery missed by the annotation; both are readily mistaken for novel drought genes.

After filtering, one locus withstands scrutiny: MSTRG.31255.1, a single-exon gene on chromosome 6A encoding a secreted cysteine-rich peptide, with a tandem paralog and a 6B homoeologue and 27 uncharacterised homologs across seven grass genera.

Because the design confounds drought treatment with plant age, these results are hypothesis-generating. The contributions of this work are a catalogue of unannotated drought-associated transcripts anchored to a chromosome-scale assembly, one specific candidate for characterisation, and a documented account of four analytical defects — coverage substituted for counts, a broken annotation join, a substring keyword match, and an exon-less sequence extraction — each of which produced a plausible but incorrect result.

---

## Data Availability

Raw RNA-seq data: DDBJ accession DRS049651 (BioProject PRJDB5606). Reference genome: NCBI GenBank GCA_032690845.1. The complete analysis — workflow, scripts, original and corrected result sets, count matrices, corrected BLASTx output and annotation tables, structural models, figures and full documentation of corrections — is deposited at [Zenodo DOI — to be added]. InterProScan job: `iprscan5-R20260417-190817-0777-66196655-p1m`.

## Author Contributions

J. J. Ayo conceived the study, developed and executed the bioinformatics pipeline, analysed the results, and wrote the manuscript.

## Use of AI Assistance

Anthropic's Claude was used to plan the pipeline, draft the workflow and scripts, and interpret intermediate results (April 2026); and subsequently to audit the completed workflow, recover analysis scripts from shell history, re-run the differential expression and homology analyses, and compile the corrections (August 2026). All commands were executed by the author. All analytical decisions, interpretation and claims are the author's. AI output was reviewed rather than accepted; several AI-generated conclusions were found to be incorrect during the audit and are documented as corrections in the deposit.

## Acknowledgements

The author thanks the developers of HISAT2, StringTie, GFFCompare, DESeq2, TransDecoder, BLAST+, InterProScan, ColabFold and Foldseek. The RNA-seq data were generated and made public by Hatakeyama et al.; the assembly GCA_032690845.1 was generated by its submitters and made available through NCBI GenBank and Phytozome.

## Competing Interests

The author declares no competing interests.

---

## References

1. FAO (2023). The State of Food and Agriculture 2023. Rome: Food and Agriculture Organization of the United Nations.
2. Hatakeyama M, et al. (2018). Multiple hybrid de novo genome assembly of finger millet, an orphan allotetraploid crop. *DNA Research*, 25(1), 39–47. doi:10.1093/dnares/dsx036 — *source of the RNA-seq data, not of the reference genome.*
3. Lloyd JP, Bowman MJ, Azodi CB, Sowers RP, Moghe GD, Childs KL, Shiu S-H (2019). Evolutionary characteristics of intergenic transcribed regions indicate rare novel genes and widespread noisy transcription in the Poaceae. *Scientific Reports*, 9, 12122. doi:10.1038/s41598-019-47797-y
4. Parvathi MS, et al. (2019). Transcriptome analysis of finger millet (*Eleusine coracana* (L.) Gaertn.) reveals unique drought responsive genes. *Journal of Genetics*, 98, 46.
5. Parvathi MS, et al. (2013). Expression analysis of stress responsive pathway genes linked to drought hardiness in an adapted crop, finger millet (*Eleusine coracana*). *Journal of Plant Biochemistry and Biotechnology*, 22, 192–201.
6. Pertea M, et al. (2015). StringTie enables improved reconstruction of a transcriptome from RNA-seq reads. *Nature Biotechnology*, 33, 290–295.
7. Kim D, et al. (2019). Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype. *Nature Biotechnology*, 37, 907–915.
8. Love MI, Huber W, Anders S (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15, 550.
9. Zhu A, Ibrahim JG, Love MI (2019). Heavy-tailed prior distributions for sequence count data: removing the noise and preserving large differences. *Bioinformatics*, 35, 2084–2092.
10. Liao Y, Smyth GK, Shi W (2014). featureCounts: an efficient general purpose program for assigning sequence reads to genomic features. *Bioinformatics*, 30, 923–930.
11. Camacho C, et al. (2009). BLAST+: architecture and applications. *BMC Bioinformatics*, 10, 421.
12. Haas BJ, et al. (2013). De novo transcript sequence reconstruction from RNA-seq using the Trinity platform. *Nature Protocols*, 8, 1494–1512.
13. Jones P, et al. (2014). InterProScan 5: genome-scale protein function classification. *Bioinformatics*, 30, 1236–1240.
14. Mirdita M, et al. (2022). ColabFold: making protein folding accessible to all. *Nature Methods*, 19, 679–682.
15. van Kempen M, et al. (2024). Fast and accurate protein structure search with Foldseek. *Nature Biotechnology*, 42, 243–246.
16. Quinlan AR, Hall IM (2010). BEDTools: a flexible suite of utilities for comparing genomic features. *Bioinformatics*, 26, 841–842.
17. Köster J, Rahmann S (2012). Snakemake — a scalable bioinformatics workflow engine. *Bioinformatics*, 28, 2520–2522.
18. Upadhyaya HD, Gowda CLL, Reddy VG (2007). Morphological diversity in finger millet germplasm introduced from southern and Eastern Africa. *Journal of SAT Agricultural Research*, 3, 1–3.
19. Vetriventhan M, et al. (2015). Finger and foxtail millets. In: *Genetic and Genomic Resources for Grain Cereals Improvement* (eds. Singh M, Upadhyaya HD), pp. 291–319. Academic Press.

---

## Tables

**Table 1.** Summary of RNA-seq alignment statistics for all six samples.

| Sample | Condition | Total Read Pairs | Alignment Rate |
|--------|-----------|-----------------|----------------|
| DRR095904 | Control | 17,137,569 | 85.13% |
| DRR095905 | Control | 17,377,076 | 91.08% |
| DRR095906 | Control | 18,174,857 | 96.22% |
| DRR095907 | Drought | 32,473,303 | 91.50% |
| DRR095908 | Drought | 27,174,371 | 94.24% |
| DRR095909 | Drought | 17,094,814 | 94.11% |
| **Mean** | | **21,571,998** | **92.05%** |

**Table 2.** The ten most significant drought-upregulated transcripts absent from the current annotation, with corrected annotations.

| Transcript ID | log₂FC | baseMean | padj | Tier | Best Swiss-Prot hit |
|---------------|--------|----------|------|------|---------------------|
| MSTRG.45758.1 | 3.14 | 536 | 9.25×10⁻³⁸ | Tier 3 | **Transposon Tf1-107 polyprotein** |
| MSTRG.6647.1 | 3.36 | 357 | 1.04×10⁻³⁷ | Tier 1 | none; PANTHER: MYB-binding protein 1A (nucleolar) |
| MSTRG.20738.1 | 2.59 | 546 | 1.37×10⁻³⁷ | Tier 3 | At3g06530; PANTHER: BAP28 / UTP10, **nucleolar** |
| **MSTRG.31255.1** | **4.43** | **576** | **1.56×10⁻³²** | **Tier 1** | **none — secreted cysteine-rich peptide** |
| MSTRG.8267.6 | 14.88 | 4,076 | 1.54×10⁻²⁹ | Tier 3 | **Retrovirus-related Pol polyprotein, transposon 17.6** |
| MSTRG.4687.1 | 3.50 | 1,797 | 2.04×10⁻²⁸ | Tier 3 | **Transposon Tf2-6 polyprotein** |
| MSTRG.14874.2 | 3.01 | 435 | 1.72×10⁻²⁷ | Tier 3 | Geranylgeranyl transferase type-2 subunit alpha 1 |
| MSTRG.4655.1 | 2.02 | 764 | 3.88×10⁻²⁷ | Tier 3 | Small subunit processome component 20 (UTP20), **nucleolar** |
| MSTRG.14681.1 | 2.48 | 6,335 | 5.57×10⁻²⁶ | Tier 3 | Dormancy-associated protein homolog 1 |
| MSTRG.18418.1 | 3.17 | 244 | 8.02×10⁻²⁵ | Tier 3 | Nucleolar complex-associated protein 3 (NOC3), **nucleolar** |

Three of the top ten are mobile elements; four encode nucleolar or ribosome-biogenesis factors.

**Table 3.** TransDecoder ORF prediction for the top 50 candidates.

| Category | Count | Percentage |
|----------|-------|------------|
| ORF ≥ 100 aa predicted | 44 | 88% |
| No ORF predicted from unspliced sequence | 6 | 12% |
| **Total** | **50** | |

The six without a predicted ORF are **not** classified as non-coding; five have Swiss-Prot protein homologs (§3.7).

---

## Figure Legends

Each figure corresponds to one file in `figures_v2/` of the accompanying deposit; the file name is given after the legend.

**Figure 1.** DESeq2 dispersion estimates against mean normalised count, showing gene-wise estimates, fitted trend and shrunken final values. (`dispersion_plot.png`)

**Figure 2.** Volcano plot of differential expression, drought-sampled versus control, on the unshrunk MLE estimate for all 76,917 tested transcripts. Dashed lines mark log₂FC = ±1.5 and adjusted p = 0.05. The 2,422 significant novel transcripts are highlighted, split into the 1,144 with control signal and the 1,278 with zero counts in all three control libraries, whose fold changes are lower bounds. (`volcano_plot.png`)

**Figure 3.** Principal component analysis of variance-stabilised counts; PC1 accounts for 74% of variance and separates the two groups. (`pca.png`)

**Figure 4.** PC1 against library size, showing the separation is not depth-driven. (`pc1_vs_library_size.png`)

**Figure 5.** Sample-to-sample distance heatmap on variance-stabilised counts. (`sample_distance_heatmap.png`)

**Figure 6.** Old versus corrected log₂ fold change for all 83,195 shared transcripts, showing that transcripts with control signal lie on the identity line while zero-control transcripts fall below it. (`log2fc_old_vs_new.png`)

**Additional diagnostic figures** are deposited in `figures_v2/` but not reproduced here: `ma_plot_unshrunk.png`, `ma_plot_apeglm.png`, `detection_vs_depth.png`, and the panels from the rejected paired model, `dispersion_plot_paired.png` and `pca_paired.png`.
