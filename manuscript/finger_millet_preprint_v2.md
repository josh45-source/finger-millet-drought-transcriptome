# Reference-guided transcriptome analysis of finger millet (*Eleusine coracana*) identifies 2,422 drought-associated transcripts absent from the current annotation

**Joash Joshua Ayo¹**

¹ Independent Researcher, Kampala, Uganda

**Corresponding author:** joashjoshua789@gmail.com

**ORCID:** [0009-0007-1642-0172](https://orcid.org/0009-0007-1642-0172)

**Keywords:** finger millet, *Eleusine coracana*, drought stress, RNA-seq, reference-guided assembly, intergenic transcribed regions, transcriptome annotation

---

> **Revision note — 28 August 2026.** This draft supersedes the version of 17 April 2026,
> which is retained unchanged as `archive/finger_millet_preprint_v2_ORIGINAL_17Apr2026.md`. An
> audit of the underlying workflow found four software defects, and the analysis was
> re-run. Every quantitative claim below has been recomputed. The most consequential
> change is that the previously reported figure of **99.6% of novel transcripts lacking a
> characterised homolog was an artefact of a broken database join**; the true figure is
> **63.3%**, which is unremarkable. Corrections are itemised in `docs/MANUSCRIPT_CORRECTIONS.md`
> of the accompanying deposit.

---

## Abstract

Finger millet (*Eleusine coracana* (L.) Gaertn.) is a drought-tolerant C₄ cereal of significant importance across sub-Saharan Africa and South Asia, yet the molecular basis of its drought hardiness remains incompletely understood. Previous transcriptomic studies relied on de novo assembly in the absence of a chromosome-scale reference, limiting the discovery of unannotated genes. Here we present a reference-guided reanalysis of drought-response RNA-seq in finger millet against the chromosome-scale KNE 796-S assembly (GCA_032690845.1). Using a Snakemake pipeline integrating HISAT2, StringTie, GFFCompare and DESeq2, we analysed publicly available RNA-seq from control and drought-sampled leaf tissue (DDBJ accession DRS049651; n = 3 per condition). We detected 21,864 transcripts absent from the current genome annotation, of which 2,422 were significantly upregulated in the drought samples (adjusted p < 0.05, log₂ fold change ≥ 1.5). Of these, 1,532 (63.3%) had no significant homology to any characterised protein in UniProt/Swiss-Prot — a rate consistent with published expectations for intergenic transcribed regions in the grasses, and therefore not evidence of an unusual gene repertoire. Annotation of the remainder is dominated by two classes that are easily mistaken for novel drought genes: **203 transcripts (8.4%) are mobile-element derived**, and several of the most statistically significant candidates encode nucleolar ribosome-biogenesis factors. One candidate withstands systematic re-examination: MSTRG.31255.1, a single-exon locus on chromosome 6A encoding a 104-amino-acid cysteine-rich peptide with a predicted signal peptide and extracellular localisation, with homoeologous copies on 6A and 6B, no Swiss-Prot homolog, and 27 uncharacterised homologs across seven grass genera. Because the control and drought tissue were sampled seven days apart with no time-matched well-watered control, treatment is confounded with plant age; these results are hypothesis-generating and require experimental validation.

---

## 1. Introduction

Drought stress is a foremost constraint on global food security, with projections indicating that water-limited conditions will increasingly threaten crop productivity across Africa and Asia (FAO, 2023). Finger millet (*Eleusine coracana* (L.) Gaertn.) is an allotetraploid C₄ cereal (2n = 4x = 36, AABB genome) cultivated by smallholder farmers across more than 25 countries and valued for its tolerance of water deficit (Upadhyaya et al., 2007; Vetriventhan et al., 2015). Despite its agronomic significance, finger millet remains underrepresented in genomic and functional genomic databases relative to rice, maize and wheat.

The molecular basis of drought tolerance in finger millet involves osmotic adjustment, reactive oxygen species (ROS) scavenging, abscisic acid (ABA) signalling and protein protection mechanisms (Parvathi et al., 2019). Previous transcriptomic investigations identified drought-responsive genes including CIPK31, PP2A, FPS and TAF6 (Parvathi et al., 2013, 2019). Those studies employed de novo transcriptome assembly without a reference genome, which constrains the identification of unannotated genes and introduces assembly artefacts.

A chromosome-scale reference assembly for *E. coracana* (GCA_032690845.1, cultivar KNE 796-S, released 2023) now enables reference-guided approaches that can systematically identify transcripts absent from the current annotation. Such transcripts — assembled against a high-quality genome backbone — are anchored to specific genomic coordinates rather than reconstructed de novo.

Here we catalogue transcripts absent from the current annotation that are upregulated in drought-sampled tissue, characterise their protein-coding potential and homology, and identify which are plausible candidates for follow-up. **A central purpose of this paper is to distinguish genuinely uncharacterised loci from two categories that superficially resemble them: mobile elements, and conserved genes that the reference annotation has simply missed.**

---

## 2. Materials and Methods

### 2.1 RNA-seq Data

Publicly available RNA-seq data were obtained from the DNA Data Bank of Japan (DDBJ) under accession DRS049651 (BioProject: PRJDB5606; Hatakeyama et al., 2018). The dataset comprises paired-end Illumina reads from leaf tissue of *Eleusine coracana* subsp. *coracana* sampled under well-watered conditions (n = 3; DRR095904, DRR095905, DRR095906) and after seven days of withheld water (n = 3; DRR095907, DRR095908, DRR095909). Raw FASTQ files were downloaded from the European Nucleotide Archive (ENA).

**Condition assignment** follows the ENA library names (`Illumina_RNA_ctl_1-3`, `Illumina_RNA_dry_1-3`), assuming run accessions map to library names in order.

**Plant material and replicate structure.** The plants were grown from a highly inbred seed stock obtained from GKVK Bangalore and originally sourced from ICRISAT, so the sampled individuals are expected to be genetically very similar. Within each sampling group the three libraries were prepared from **separate plants**, so the replication is biological rather than technical. This is not recorded in the archive metadata: all 18 runs of PRJDB5606 are registered under a single BioSample (SAMD00076255), so no replicate structure is declared there. The libraries were generated primarily to support genome annotation rather than as a designed differential-expression experiment — the study is titled "Finger millet genome assembly" — and no growth protocol, drought severity or timepoint is recorded. Detailed environmental information for the growth period, including watering amount and timing and temperature, was not retained. **See §4.6.**

### 2.2 Reference Genome

The *E. coracana* chromosome-scale assembly GCA_032690845.1 (*Eleusine_coracana_v1.0*, cultivar KNE 796-S) and its GFF3 annotation were downloaded from NCBI. The assembly comprises **532 sequences: 18 pseudomolecules** (1A/1B through 9A/9B, resolving both subgenomes of the allotetraploid) plus 514 unplaced scaffolds, totalling **1,111,714,373 bp** with an N50 of 61,270,980 bp.

> This assembly is **not** the one described by Hatakeyama et al. (2018), which is a
> short-read assembly of a different accession. Hatakeyama et al. (2018) is the correct
> citation for the RNA-seq data used here, not for the reference genome.

### 2.3 Quality Control and Read Trimming

Read quality was assessed using FastQC v0.12.1 and MultiQC v1.33. Adapters and low-quality bases were removed using Trimmomatic v0.40 in paired-end mode: ILLUMINACLIP:TruSeq3-PE.fa:2:30:10, LEADING:3, TRAILING:3, SLIDINGWINDOW:4:15, MINLEN:36.

### 2.4 Read Alignment

Trimmed reads were aligned with HISAT2 v2.2.2 using: --score-min L,0,-0.5, --no-mixed, --no-discordant, --mp 4,2, --rdg 5,3, --rfg 5,3, --rna-strandness RF, --dta, --min-intronlen 20, --max-intronlen 500000. Alignments were filtered at MAPQ ≥ 20 with SAMtools v1.23.1 and coordinate-sorted. The MAPQ filter discards reads mapping ambiguously between the A and B subgenomes.

### 2.5 Transcript Assembly and Detection of Unannotated Transcripts

Transcripts were assembled per sample with StringTie v3.0.0 guided by the reference annotation, then merged with `stringtie --merge`. Transcripts absent from the reference annotation were identified by comparison with GFFCompare v0.12.10; those assigned class code "u" (intergenic, no overlap with any annotated feature) were retained.

> **Terminology.** We refer to these as *transcripts absent from the current annotation*
> rather than "novel genes". Class code "u" records absence from an annotation file; it is
> not evidence of novelty. As §3.4 shows, a substantial fraction are mobile elements or
> conserved genes the annotation has missed.

### 2.6 Differential Expression Analysis

Read counts were generated with `prepDE.py` (bundled with StringTie 3.0.0) from the per-sample `stringtie -e -B` output, at the **measured mean aligned read length of 142 bp** (sampled across four 4 Mb windows on chromosomes 1A, 3B, 6A and 9A in every alignment; the modal untrimmed length is 151 bp). Counts were independently validated against `featureCounts` (subread v2.1.1; `-p --countReadPairs -B -C -s 2`), which agreed at **Spearman ρ = 0.985–0.995 across all six samples**.

Differential expression used DESeq2 v1.50.2 under R v4.5.3, design `~ condition`, contrast drought versus control, with transcripts prefiltered at `rowSums(counts) ≥ 10`. Transcripts were called significantly upregulated at adjusted p < 0.05 (Benjamini–Hochberg) and log₂ fold change ≥ 1.5, applied to the unshrunk maximum-likelihood estimate. Shrunken estimates from `lfcShrink(type="apeglm")` (apeglm v1.32.0) are reported alongside; for the candidates discussed below the two differ by less than 1.5%.

A paired design (`~ plant + condition`), with pairing inferred from the ENA library-name suffixes, was fitted and **rejected**: it increased dispersion (asymptotic dispersion 0.786 → 0.880) and cost 8,239 transcripts their testability. All six possible control-to-drought pairings absorb 49.1–51.0% of within-condition variance, which is indistinguishable, so the suffixes do not encode plant identity. Nor can the pairing be established from the surviving experimental records (§4.6). The six libraries are therefore treated as independent samples. See §4.6.

### 2.7 Homology Search

Genomic sequences were extracted with BEDTools v2.31.1 `getfasta` and searched with BLASTx (BLAST+ v2.17.0) against UniProt Swiss-Prot (574,627 sequences; 208,482,574 residues) at E ≤ 1×10⁻⁵, `-max_target_seqs 5`, `-outfmt 6`. The best hit per transcript was taken by ascending E-value then descending bit score.

> **Extraction caveat.** The GTF used for extraction retained transcript records but no
> exon records, so extracted sequences are whole genomic intervals **including introns**.
> 47 of the top 50 candidates are multi-exon; any ORF called on them may be a chimera of
> exonic and intronic sequence. Single-exon candidates, including MSTRG.31255.1, are
> unaffected. See §4.6.

### 2.8 Protein-coding Potential and Domain Annotation

ORF prediction used TransDecoder v5.7.1 on the top 50 candidates by adjusted p-value (`-m 100`, `--single_best_only`). Predicted peptides were submitted to the InterProScan 5 web service at EBI (job `iprscan5-R20260417-190817-0777-66196655-p1m`); the service version is not recorded in the output.

### 2.9 Candidate Stratification

Transcripts were stratified by homology and induction magnitude:

- **Tier 1 — no Swiss-Prot homolog**, subdivided at log₂FC ≥ 3
- **Tier 2 — homolog matching a stress-associated keyword**
- **Tier 3 — homolog of other function**

> **This scheme is a coarse triage, not a functional classification.** Tier 2 membership is
> a keyword match against a fixed word list, applied at word boundaries. In practice
> 46 of the 50 Tier 2 assignments arise from the single word "kinase". Tier 2 should be
> rebuilt by manual curation before it is used to prioritise experiments.

### 2.10 Reproducibility

The analysis was implemented as a Snakemake v9.19.0 pipeline with conda-managed environments. All code, count matrices, result tables, structural models and a full record of corrections are deposited [Zenodo DOI — to be added].

---

## 3. Results

### 3.1 RNA-seq Quality and Alignment

After trimming, between 17.1 and 32.5 million read pairs per sample were retained. Alignment rates ranged from 85.13% to 96.22%, mean 92.05% (Table 1). Assigned fragment counts differ systematically between groups (control 18.5–22.0 M; drought 21.0–36.4 M), so sequencing depth is partially confounded with condition; this is addressed in §3.6.

### 3.2 Transcripts Absent from the Current Annotation

GFFCompare identified **21,864 transcripts** assigned class code "u". BLASTx against Swiss-Prot returns a significant hit for **6,106 of these (27.9%)**.

### 3.3 Differential Expression

DESeq2 identified **2,422 transcripts significantly upregulated in the drought samples** (adjusted p < 0.05, log₂FC ≥ 1.5). The smallest adjusted p-value is **1.37 × 10⁻³⁷**. Applying the log₂FC threshold to apeglm-shrunk estimates instead of the MLE gives 2,218 transcripts.

The most statistically significant transcripts are listed in Table 2. **Three of the top ten are mobile elements** and a further three encode nucleolar or ribosome-biogenesis factors.

### 3.4 Homology: 63.3% Without a Characterised Homolog, Which Is Unremarkable

BLASTx revealed that **1,532 of 2,422 (63.3%) had no significant homology** to any characterised protein in Swiss-Prot; 890 (36.7%) did.

| Tier | Description | Count |
|------|-------------|-------|
| Tier 1 | No homolog, highly induced (log₂FC ≥ 3) | 1,184 |
| Tier 1 | No homolog | 348 |
| Tier 2 | Stress-keyword homolog | 50 |
| Tier 3 | Other homolog | 840 |
| **Total** | | **2,422** |

**This rate is what should be expected.** Lloyd et al. (2019) found that only 16–23% of intergenic transcribed regions in their survey had detectable protein-level similarity — i.e. roughly 77–84% did not. A set of unannotated transcripts that is 63.3% homology-free is, if anything, better annotated than the intergenic background. **No claim of an unusual or lineage-specific gene repertoire is supportable from this figure.**

> **An earlier version of this manuscript reported 99.6% (2,344 of 2,354).** That figure
> was a software defect, not a result. Sequence extraction wrote the GTF feature type —
> the literal string `transcript` — as the FASTA header, so every BLASTx query identifier
> was `transcript::<chrom>:<start>-<end>` while the expression table was keyed on
> transcript ID. The left join silently assigned a null annotation to every row. Re-running
> BLASTx with correct identifiers produced output byte-identical to the original in every
> field except the query name, confirming the search itself was always correct and only
> the join was broken.

### 3.5 A Substantial Fraction Is Mobile-Element Derived

**203 of the 2,422 transcripts (8.4%)** have a best Swiss-Prot hit to a transposon, retrovirus-related polyprotein, integrase, reverse transcriptase or LINE-1 element. Among the annotated subset the most frequent subjects are all mobile-element proteins. **Eight of the top 50 by adjusted p-value fall in this class.**

Two examples illustrate the problem for candidate selection. MSTRG.45758.1, the most statistically significant transcript in the dataset (log₂FC 3.14, padj 9.25 × 10⁻³⁸), matches Transposon Tf1-107 polyprotein at E = 4.5 × 10⁻⁷². MSTRG.4687.1 (log₂FC 3.50, padj 2.04 × 10⁻²⁸) matches Transposon Tf2-6 polyprotein at E = 2.0 × 10⁻¹⁰⁶. Both assignments are independently corroborated by InterProScan — Pfam integrase core (PF00665), integrase zinc-binding (PF17921), RNase H-like reverse transcriptase (PF17917), and CDD `RNase_HI_RT_Ty3` — and by Foldseek structural search returning transposon Tf2-7 polyprotein at probability 1.0.

No repeat-masking was performed prior to assessment. Because transposon insertions are lineage-specific by nature, they will score as species-specific for reasons unrelated to gene novelty. **We recommend that comparable studies mask repeats before interpreting unannotated transcripts as candidate genes.**

### 3.6 Detection Asymmetry Is Not a Depth Artefact

Drought libraries detect 74,000–79,000 transcripts versus 56,000–62,000 in control, and 1,278 of the 2,422 (52.8%) have zero counts in all three control libraries. This pattern is what insufficient sequencing depth would produce, so it was tested directly.

DRR095905 (control) and DRR095909 (drought) differ in library size by 0.08% (21,011,330 vs 20,994,628 assigned counts) yet differ by 31.8% in transcripts detected. Of the 1,278 zero-in-all-controls transcripts, **1,232 (96.4%) are detected in DRR095909 alone**, with a median of 231 fragments across the drought libraries and none below 20. **Sequencing depth is therefore excluded as the explanation.** Whether the asymmetry reflects genuine transcriptional activation or a library-preparation difference between the two collection dates cannot be determined from these data.

**Fold changes for transcripts with zero control counts are not identifiable** and are reported here only as lower bounds; with a zero denominator the estimate is driven by the magnitude of the numerator rather than by a ratio.

### 3.7 Protein-coding Potential

TransDecoder identified ORFs of ≥ 100 aa in **44 of the top 50 transcripts (88%)**. The six without a predicted ORF (MSTRG.14681.1, MSTRG.46022.1, MSTRG.14947.1, MSTRG.45098.4, MSTRG.6129.1, MSTRG.26934.1) were provisionally described as long non-coding RNAs in an earlier version of this manuscript. **That classification does not survive the corrected annotation: five of the six have Swiss-Prot protein homologs**, including Dormancy-associated protein homolog 1 (MSTRG.14681.1), small ribosomal subunit protein uS14 (MSTRG.46022.1), mitochondrial import receptor subunit TOM6 (MSTRG.14947.1), histone deacetylase HDT2 (MSTRG.6129.1) and hydrophobic protein LTI6B (MSTRG.26934.1).

The absence of a predicted ORF reflects the extraction defect described in §2.7 — ORFs were called on unspliced genomic sequence — not an absence of coding potential. **No lncRNA claim is made in this manuscript.**

### 3.8 Domain Annotation of Selected Candidates

**MSTRG.31255.1** (log₂FC 4.43, padj 1.56 × 10⁻³², rank 4): Phobius and SignalP-EUK both predict a signal peptide (residues 1–32 and 1–28 respectively), and Phobius annotates residues 33–104 as extracellular. **This protein is predicted to be secreted, not membrane-associated.** SignalP-EUK's own verdict is `SignalP-noTM`; the transmembrane helix reported by TMHMM at residues 7–29 lies inside the signal peptide and is the well-documented confusion between a signal-peptide h-region and a transmembrane segment.

**MSTRG.20738.1** (log₂FC 2.59, padj 1.37 × 10⁻³⁷, rank 3): InterProScan identifies an ARM/Armadillo repeat (SUPERFAMILY SSF48371, E = 1.5 × 10⁻⁹) and an Armadillo-like helical fold (Gene3D). **This transcript is not without a homolog**: BLASTx matches *Arabidopsis* At3g06530 at E = 2.2 × 10⁻⁸⁴, and PANTHER assigns it to BAP28, which maps to U3 small nucleolar RNA-associated protein 10 (UTP10). **It is a nucleolar rRNA-processing factor, not a component of ABA signalling.** An earlier version of this manuscript interpreted the ARM repeat as evidence of involvement in the ABA receptor complex and proteasomal degradation; that interpretation was unsupported and is withdrawn.

**MSTRG.6647.1** (log₂FC 3.36, padj 1.04 × 10⁻³⁷, rank 2): no Swiss-Prot hit, but PANTHER assigns it to the MYB-binding protein 1A family (PTHR13213, E = 4.0 × 10⁻⁹⁷) and Pfam to DNA polymerase V / Myb-binding protein 1A (PF04931). **MYBBP1A is a nucleolar ribosome-biogenesis protein, not a partner of plant drought MYB transcription factors.** Together with MSTRG.20738.1, MSTRG.4655.1 (UTP20) and MSTRG.18418.1 (NOC3), **four of the top ten transcripts encode nucleolar or ribosome-biogenesis machinery** — a coherent signal, but one consistent with a general change in growth rate rather than a specific drought-protective programme.

**MSTRG.21998.1** (log₂FC 2.98, padj 3.60 × 10⁻¹⁹, rank 19): a phosphatidylinositol phosphate kinase domain is confirmed by five independent databases (Pfam PF01504, PANTHER PTHR45748, SMART SM00330, ProSiteProfiles PS51455, Gene3D G3DSA:3.30.800.10). **The enzyme is FAB1D**, a putative 1-phosphatidylinositol-**3**-phosphate 5-kinase (BLASTx to *Arabidopsis* FAB1D, E = 5.3 × 10⁻⁹⁹; PANTHER independently names the PI3P 5-kinase family). FAB1/PIKfyve enzymes phosphorylate PI3P to generate PI(3,5)P₂ and govern vacuolar and endosomal trafficking. **This is a different enzyme from the PI(4,5)P₂-generating PIP5Ks that regulate stomatal closure**, and an earlier version of this manuscript misattributed that function to it. Two further caveats apply: this transcript has blastn hits in all three comparison species and is therefore not lineage-specific, and its 420 aa ORF was predicted from unspliced genomic sequence and requires re-derivation from a spliced transcript before the domain assignment can be relied upon.

---

## 4. Discussion

### 4.1 What a Reference-Guided Approach Adds

Reference-guided assembly anchors transcripts to genomic coordinates, eliminates many assembly chimeras, enables strand-specific analysis and permits homoeolog-aware interpretation in a polyploid. The 21,864 transcripts absent from the current annotation demonstrate that the *E. coracana* annotation is incomplete, which is expected for a recently released assembly of an orphan crop.

What the approach does **not** do is establish that those transcripts are novel genes. Class code "u" is a statement about an annotation file.

### 4.2 The Uncharacterised Fraction Requires No Special Explanation

An earlier version of this manuscript treated a 99.6% no-homology rate as a finding and offered three explanations for it: phylogenetic distance of Chloridoideae from model species, sequence divergence below the BLASTx detection threshold, and de novo gene birth. **With the corrected figure of 63.3%, that argument has no phenomenon to explain.** Lloyd et al. (2019) report 16–23% of intergenic transcribed regions with detectable protein similarity; our set is better annotated than that background, not worse.

The composition of the annotated 36.7% is more informative than the size of the unannotated fraction. It is dominated by mobile elements (§3.5) and by conserved housekeeping machinery that the reference annotation has missed — nucleolar ribosome-biogenesis factors in particular. Both categories are recovered as class code "u" for reasons that have nothing to do with lineage-specific gene content.

### 4.3 Candidates for Follow-up

Applying the corrections above removes most of the candidates prioritised in the earlier version of this manuscript. Specifically: MSTRG.45758.1 and MSTRG.4687.1 are retrotransposons; MSTRG.20738.1 and MSTRG.6647.1 are nucleolar ribosome-biogenesis factors; MSTRG.21998.1 is a conserved FAB1 homolog whose ORF requires re-derivation; and MSTRG.37761.2, previously described as "~730-fold induced", is in fact ~87-fold (log₂FC 6.45, down from 9.51), has a baseMean of 11.9, has zero counts in all three control libraries and ranks 1,191st.

**One candidate survives: MSTRG.31255.1.**

- Single-exon, so unaffected by the unspliced-extraction defect
- Complete ORF with genuine start and stop codons; 104 aa, cysteine-rich
- Predicted signal peptide (1–28 / 1–32) and extracellular mature region (33–104)
- log₂FC 4.43, padj 1.56 × 10⁻³², rank 4 of 2,422; stable across the unpaired model, the paired model and apeglm shrinkage (estimates differ by 1.2%)
- Detected at 26/33/46 counts in control versus 2,785/1,662/1,086 in drought — a real ratio, not a division by zero
- No Swiss-Prot homolog under the corrected join
- 27 distinct homologs (32 alignment rows, 5 exact duplicates) across **seven grass genera and twelve species in three subfamilies** — *Oryza* (six species), *Leersia*, *Setaria*, *Dichanthelium*, *Sorghum*, *Zea*, *Arundo* — of which 23 are annotated only as "uncharacterized protein". Every UniProt-derived homolog is an unreviewed TrEMBL entry and none is in Swiss-Prot, which is exactly why the Swiss-Prot search returns nothing
- All homologs share an invariant C-terminal cysteine module
- A small gene family: tblastn recovers a tandem paralog 4.4 kb upstream on 6A (79.3% identity) and a homoeologous copy on 6B (88.6%), consistent with the AABB structure. **None of the family members is annotated in the reference**

This supports description as **a small secreted cysteine-rich protein family conserved across the grasses and uncharacterised throughout** — not as a finger millet-specific protein. No Chloridoideae sequence appears in the alignment, so conservation within *Eleusine*'s own subfamily has never been tested; a targeted tblastn against *Eleusine indica* and *Oropetium thomaeum* would settle it and should precede any functional work.

Its AlphaFold2 model (ColabFold 1.6.1) is **low confidence**: mean pLDDT 59.95, pTM 0.390, MSA depth 34, with only residues ~66–104 exceeding pLDDT 70 and 41 of 104 residues below 50. It supports a disulfide-stabilised C-terminal module and nothing more; no fold or repeat architecture can be assigned.

### 4.4 The Cross-species Screen Is Underpowered

Cross-species comparison used blastn (nucleotide) at E ≤ 1e-5 against three genomes with `-max_target_seqs 1`, which does not reliably return the best hit. For MSTRG.31255.1 this returned no hits in any species, yet the protein-level alignment for the same locus recovers 27 homologs at 22–34% amino acid identity — a divergence at which nucleotide alignment fails regardless of threshold. **Every lineage-specificity call in this work inherits this limitation and should be regarded as provisional.** The screen is homology detection, not synteny: no collinearity or orthology assignment was performed. The three comparison genomes (*Sorghum bicolor*, *Oryza sativa*, *Setaria italica*) are Panicoideae and Oryzoideae; no Chloridoideae genome was included. Absence of a BLAST hit is not evidence of gene absence.

### 4.5 What Would Make This Conclusive

1. tblastn of the MSTRG.31255.1 peptide against Chloridoideae genomes (*E. indica*, *O. thomaeum*) to test subfamily-level conservation
2. RT-PCR across the exon structure and 5′/3′ RACE to confirm the transcript model, followed by re-derivation of the ORF from a spliced sequence
3. qRT-PCR in a properly designed drought experiment with a time-matched well-watered control, to separate drought response from developmental change
4. Repeat-masked reanalysis, so that mobile elements do not enter the candidate set
5. Peptide-level confirmation of secretion (apoplastic fluid proteomics or a fluorescent fusion)

### 4.6 Limitations

**Treatment is confounded with plant age.** No time-matched well-watered control was sampled at day seven: the control libraries were taken at the start of the experiment and the drought libraries after seven days of withheld water. Every transcript reported here as drought-responsive is therefore equally consistent with being development-responsive over a seven-day window in a young plant. Detailed environmental information for the growth period — watering amount and timing, temperature — was not retained, so the size of the developmental component cannot be bounded from the record either. Nothing in this dataset can separate the two, and this is the largest single constraint on the interpretation offered above.

**The six libraries are treated as independent samples.** Whether the control and drought libraries derive from the same individual plants cannot be established, from either the data or the surviving experimental records; the original laboratory notes no longer exist. A surviving sample-name table pairs matched replicate numbers with a `_D` suffix for the drought samples, which suggests that a correspondence was intended, but there is no documentation confirming that the same individuals were sampled twice. The pairing is therefore not sufficiently documented to justify treating the design as confirmed repeated measures. The data agree: all six possible control-to-drought pairings absorb an indistinguishable 49.1–51.0% of within-condition variance (§2.6), so no pairing is recoverable from the counts either. Treating the six libraries as independent, as `~ condition` does, is the appropriate choice.

**Replication is biological, and between-replicate dispersion is extreme.** The three libraries per condition were prepared from separate plants, so the replication is biological rather than technical, although this is not recorded in the archive metadata (all 18 runs of PRJDB5606 share one BioSample). The asymptotic dispersion of 0.786 implies a coefficient of variation near 89% at high expression, 20–80× typical for controlled plant RNA-seq. It reflects genuine between-plant variation in material that was not collected under a controlled experimental protocol. Genetic heterogeneity is largely excluded as an explanation, since the plants derive from a highly inbred seed stock obtained from GKVK Bangalore and originally from ICRISAT and should be genetically very similar (§2.1), which makes the magnitude of the dispersion more notable rather than less. **P-values should not be quoted to better than an order of magnitude.**

**The libraries were not generated for this experiment.** They were produced primarily to support genome annotation rather than as a designed differential-expression experiment.

**All extracted sequences are unspliced** (§2.7), affecting ORF prediction, domain annotation and the cross-species screen, though not the differential expression analysis, which was computed from the exon-aware merged assembly.

**The candidate list has an untraced step.** The table from which the top 50 were selected has no recorded generating script; its provenance could not be reconstructed. This is disclosed rather than concealed, and the file is deposited.

**Computational analysis only.** No experimental validation has been performed and this manuscript has not been peer reviewed.

---

## 5. Conclusions

Reference-guided reanalysis of drought-response RNA-seq against the chromosome-scale finger millet assembly identifies 2,422 transcripts that are absent from the current annotation and upregulated in drought-sampled tissue. Of these, 63.3% have no characterised homolog — a rate consistent with published expectations for intergenic transcribed regions and therefore not evidence of an unusual gene repertoire. The annotated remainder is dominated by mobile elements (8.4% of the whole set) and by conserved nucleolar machinery that the reference annotation has missed; both classes are readily mistaken for novel drought genes and should be excluded before candidates are selected.

After applying these filters, one locus withstands scrutiny: MSTRG.31255.1, a single-exon gene on chromosome 6A encoding a secreted cysteine-rich peptide, with a tandem paralog and a 6B homoeologue, no Swiss-Prot homolog, and 27 uncharacterised homologs spanning seven grass genera. It appears to belong to a small secreted protein family conserved across the grasses and uncharacterised throughout.

Because the underlying design confounds drought treatment with plant age, these results are hypothesis-generating. The principal contributions of this work are a catalogue of unannotated drought-associated transcripts anchored to a chromosome-scale assembly, a specific candidate for functional characterisation, and a documented account of four analytical defects — a coverage-for-counts substitution, a broken annotation join, a substring keyword match, and an exon-less sequence extraction — each of which produced a plausible-looking but incorrect result.

---

## Data Availability

Raw RNA-seq data are available from DDBJ under accession DRS049651 (BioProject PRJDB5606). The reference genome is NCBI GenBank accession GCA_032690845.1. The complete analysis — Snakemake workflow, analysis scripts, both the original and corrected result sets, count matrices, corrected BLASTx output and annotation tables, ColabFold structural models with confidence scores, diagnostic figures, and full documentation of provenance and corrections — is deposited at [Zenodo DOI — to be added]. The InterProScan job identifier is `iprscan5-R20260417-190817-0777-66196655-p1m`.

## Author Contributions

J. J. Ayo conceived the study, developed and executed the bioinformatics pipeline, analysed the results, and wrote the manuscript.

## Use of AI Assistance

Anthropic's Claude was used to plan the pipeline, draft the workflow and scripts, and interpret intermediate results (April 2026); and subsequently to audit the completed workflow, recover analysis scripts from shell history, re-run the differential expression and homology analyses, and compile the corrections (August 2026). All commands were executed by the author. All analytical decisions, interpretation and claims are the author's. AI output was reviewed rather than accepted; several AI-generated conclusions were found to be incorrect during the audit and are documented as corrections in the deposit.

## Acknowledgements

The author thanks the developers of HISAT2, StringTie, GFFCompare, DESeq2, TransDecoder, BLAST+, InterProScan, ColabFold and Foldseek. The RNA-seq data were generated and made public by Hatakeyama et al.; the chromosome-scale assembly GCA_032690845.1 was generated by its submitters and made available through NCBI GenBank and Phytozome.

## Competing Interests

The author declares no competing interests.

---

## References

1. FAO (2023). The State of Food and Agriculture 2023. Rome: FAO.
2. Hatakeyama M, et al. (2018). Multiple hybrid de novo genome assembly of finger millet, an orphan allotetraploid crop. *DNA Research*, 25(1), 39–47. doi:10.1093/dnares/dsx036 — *source of the RNA-seq data reanalysed here, not of the reference genome.*
3. Lloyd JP, Bowman MJ, Azodi CB, Sowers RP, Moghe GD, Childs KL, Shiu S-H (2019). Evolutionary characteristics of intergenic transcribed regions indicate rare novel genes and widespread noisy transcription in the Poaceae. *Scientific Reports*, 9, 12122. doi:10.1038/s41598-019-47797-y
4. Parvathi MS, et al. (2019). Transcriptome analysis of finger millet reveals unique drought responsive genes. *Journal of Genetics*, 98, 46.
5. Parvathi MS, et al. (2013). Expression analysis of stress responsive pathway genes in finger millet. *Journal of Plant Biochemistry and Biotechnology*, 22, 192–201.
6. Kim D, et al. (2019). Graph-based genome alignment with HISAT2. *Nature Biotechnology*, 37, 907–915.
7. Pertea M, et al. (2015). StringTie enables improved reconstruction of a transcriptome from RNA-seq reads. *Nature Biotechnology*, 33, 290–295.
8. Love MI, Huber W, Anders S (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15, 550.
9. Zhu A, Ibrahim JG, Love MI (2019). Heavy-tailed prior distributions for sequence count data. *Bioinformatics*, 35, 2084–2092.
10. Liao Y, Smyth GK, Shi W (2014). featureCounts: an efficient general purpose program for assigning sequence reads to genomic features. *Bioinformatics*, 30, 923–930.
11. Camacho C, et al. (2009). BLAST+: architecture and applications. *BMC Bioinformatics*, 10, 421.
12. Jones P, et al. (2014). InterProScan 5: genome-scale protein function classification. *Bioinformatics*, 30, 1236–1240.
13. Mirdita M, et al. (2022). ColabFold: making protein folding accessible to all. *Nature Methods*, 19, 679–682.
14. van Kempen M, et al. (2024). Fast and accurate protein structure search with Foldseek. *Nature Biotechnology*, 42, 243–246.
15. Quinlan AR, Hall IM (2010). BEDTools: a flexible suite of utilities for comparing genomic features. *Bioinformatics*, 26, 841–842.
16. Köster J, Rahmann S (2012). Snakemake — a scalable bioinformatics workflow engine. *Bioinformatics*, 28, 2520–2522.
17. Upadhyaya HD, et al. (2007). Morphological diversity in finger millet germplasm. *Journal of SAT Agricultural Research*, 3, 1–3.
18. Vetriventhan M, et al. (2015). Finger and foxtail millets. In: *Genetic and Genomic Resources for Grain Cereals Improvement*, pp. 291–319.

---

## Tables

**Table 1.** RNA-seq alignment statistics.

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
| MSTRG.45758.1 | 3.14 | 536 | 9.25×10⁻³⁸ | Tier 3 | **Transposon Tf1-107 polyprotein** (E = 4.5×10⁻⁷²) |
| MSTRG.6647.1 | 3.36 | 357 | 1.04×10⁻³⁷ | Tier 1 | none; PANTHER: MYB-binding protein 1A family (nucleolar) |
| MSTRG.20738.1 | 2.59 | 546 | 1.37×10⁻³⁷ | Tier 3 | At3g06530 (E = 2.2×10⁻⁸⁴); PANTHER: BAP28 / UTP10, **nucleolar** |
| **MSTRG.31255.1** | **4.43** | **576** | **1.56×10⁻³²** | **Tier 1** | **none — secreted cysteine-rich peptide, see §4.3** |
| MSTRG.8267.6 | 14.88 | 4,076 | 1.54×10⁻²⁹ | Tier 3 | **Retrovirus-related Pol polyprotein, transposon 17.6** |
| MSTRG.4687.1 | 3.50 | 1,797 | 2.04×10⁻²⁸ | Tier 3 | **Transposon Tf2-6 polyprotein** (E = 2.0×10⁻¹⁰⁶) |
| MSTRG.14874.2 | 3.01 | 435 | 1.72×10⁻²⁷ | Tier 3 | Geranylgeranyl transferase type-2 subunit alpha 1 |
| MSTRG.4655.1 | 2.02 | 764 | 3.88×10⁻²⁷ | Tier 3 | Small subunit processome component 20 (UTP20), **nucleolar** |
| MSTRG.14681.1 | 2.48 | 6,335 | 5.57×10⁻²⁶ | Tier 3 | Dormancy-associated protein homolog 1 |
| MSTRG.18418.1 | 3.17 | 244 | 8.02×10⁻²⁵ | Tier 3 | Nucleolar complex-associated protein 3 (NOC3), **nucleolar** |

Bold entries mark the two classes discussed in §3.5 and §3.8. Of the top ten, three are mobile elements and four encode nucleolar or ribosome-biogenesis factors.

**Table 3.** ORF prediction for the top 50 candidates.

| Category | Count | Percentage |
|----------|-------|------------|
| ORF ≥ 100 aa predicted | 44 | 88% |
| No ORF predicted from unspliced sequence | 6 | 12% |
| **Total** | **50** | |

Note: the six without a predicted ORF are **not** classified as non-coding; five of the six have Swiss-Prot protein homologs (§3.7).

---

## Figure Legends

Each figure corresponds to one file in `figures_v2/` of the accompanying deposit; the file name is given after the legend.

**Figure 1.** DESeq2 dispersion estimates against mean normalised count, showing gene-wise estimates, the fitted trend and shrunken final values. The asymptotic dispersion of 0.786 is the basis for the caution in §4.6. (`dispersion_plot.png`)

**Figure 2.** Volcano plot of differential expression, drought-sampled versus control, on the unshrunk MLE fold-change estimate for all 76,917 tested transcripts. Dashed lines mark log₂FC = ±1.5 and adjusted p = 0.05. The 2,422 significantly upregulated transcripts absent from the current annotation are highlighted, split into the 1,144 with control signal and the 1,278 with zero counts in all three control libraries, whose fold changes are lower bounds rather than identifiable ratios (§3.6) and which form the diagonal band running to the right-hand limit. Points outside the plotting window are drawn as open triangles at the boundary. (`volcano_plot.png`)

**Figure 3.** Principal component analysis of variance-stabilised counts. PC1 (74% of variance) separates the two groups. (`pca.png`)

**Figure 4.** PC1 against library size, demonstrating that the group separation on PC1 is not driven by sequencing depth (§3.6). (`pc1_vs_library_size.png`)

**Figure 5.** Sample-to-sample distance heatmap on variance-stabilised counts. Drought samples cluster tightly (mean distance 282); control samples are markedly more heterogeneous (mean 496). (`sample_distance_heatmap.png`)

**Figure 6.** Old versus corrected log₂ fold change for all 83,195 shared transcripts. Transcripts with control signal lie on the identity line (r = 0.974); those with zero control counts fall below it, showing where the earlier analysis inflated fold changes (§3.6). (`log2fc_old_vs_new.png`)

**Additional diagnostic figures** are deposited in `figures_v2/` but not reproduced here: MA plots on the unshrunk and apeglm-shrunk estimates (`ma_plot_unshrunk.png`, `ma_plot_apeglm.png`), transcripts detected against library size (`detection_vs_depth.png`), and the dispersion and PCA panels from the rejected paired model of §2.6 (`dispersion_plot_paired.png`, `pca_paired.png`).
