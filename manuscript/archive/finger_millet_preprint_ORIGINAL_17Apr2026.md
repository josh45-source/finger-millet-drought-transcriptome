# Reference-guided transcriptome analysis of finger millet (*Eleusine coracana*) reveals 2,354 novel drought-responsive transcripts with largely uncharacterised protein repertoire

**Joshua [SURNAME]¹**

¹ [Your Institution/Affiliation], Kampala, Uganda

**Corresponding author:** [your email]

**Keywords:** finger millet, *Eleusine coracana*, drought stress, RNA-seq, novel genes, transcriptomics, reference-guided assembly, orphan genes

---

## Abstract

Finger millet (*Eleusine coracana* (L.) Gaertn.) is a drought-tolerant C₄ cereal of significant importance across sub-Saharan Africa and South Asia, yet the molecular basis of its exceptional drought hardiness remains incompletely understood. Previous transcriptomic studies relied on de novo assembly approaches in the absence of a reference genome, limiting the discovery of novel unannotated genes. Here, we present the first reference-guided transcriptomic analysis of drought stress in finger millet, leveraging the recently published chromosome-scale genome assembly (GCA_032690845.1). Using a reproducible Snakemake pipeline integrating HISAT2, StringTie, GFFCompare, and DESeq2, we analysed publicly available RNA-seq data from control and drought-stressed leaf tissue (DDBJ accession DRS049651). We detected 21,864 novel transcripts absent from the current genome annotation, of which 2,354 were significantly upregulated under drought (adjusted p-value < 0.05, log₂ fold change ≥ 1.5). Strikingly, 99.6% of these novel drought-upregulated transcripts had no significant homology to any characterised protein in UniProt/Swiss-Prot, suggesting that finger millet possesses a largely unique drought-responsive gene repertoire. TransDecoder analysis confirmed that 88% of top candidates encode putative proteins, with InterProScan annotation revealing signal peptides, ARM repeat domains, phosphatidylinositol phosphate kinase (PIPK) domains, and MYB-binding protein families among the most highly induced candidates. Six candidates lacking open reading frames were classified as putative drought-responsive long non-coding RNAs (lncRNAs). Our findings substantially expand the known drought-responsive gene catalogue of finger millet and provide a foundation for functional validation and crop improvement efforts. All pipeline code and results are publicly available.

---

## 1. Introduction

Drought stress is the foremost constraint on global food security, with projections indicating that water-limited conditions will increasingly threaten crop productivity across Africa and Asia (FAO, 2023). Finger millet (*Eleusine coracana* (L.) Gaertn.) is uniquely positioned as a model for drought tolerance research: it is an allotetraploid C₄ cereal (2n = 4x = 36, AABB genome) cultivated by smallholder farmers across more than 25 countries, renowned for its ability to survive prolonged water deficit that would be lethal to most other cereals (Upadhyaya et al., 2007; Vetriventhan et al., 2015). Despite its agronomic significance, finger millet remains an orphan crop — underrepresented in genomic and functional genomic databases relative to major cereals such as rice, maize, and wheat.

The molecular basis of drought tolerance in finger millet involves multiple coordinated pathways including osmotic adjustment, reactive oxygen species (ROS) scavenging, abscisic acid (ABA) signalling, and protein protection mechanisms (Parvathi et al., 2019). Previous transcriptomic investigations have identified key drought-responsive genes including calcineurin B-like interacting protein kinase 31 (CIPK31), serine/threonine protein phosphatase 2A (PP2A), farnesyl pyrophosphate synthase (FPS), and TATA-binding protein associated factor 6 (TAF6) (Parvathi et al., 2013, 2019). However, these studies employed de novo transcriptome assembly without a reference genome, which constrains the ability to identify truly novel, unannotated genes and introduces assembly artefacts.

The publication of a chromosome-scale reference genome for *E. coracana* (GCA_032690845.1; Hatakeyama et al., 2018, updated 2023) now enables reference-guided transcriptomic approaches that can systematically identify transcripts absent from the current annotation. Such "novel" transcripts — assembled against a high-quality genome backbone — represent genuine unannotated genes rather than assembly chimeras, and are thus stronger candidates for functional investigation.

Here, we present the first reference-guided RNA-seq analysis of drought stress in finger millet. Using a fully reproducible bioinformatics pipeline, we identify 2,354 novel drought-upregulated transcripts, characterise their protein-coding potential and domain architecture, and highlight priority candidates for experimental validation. We demonstrate that the majority of these novel transcripts lack homology to any previously characterised protein, suggesting that a substantial component of finger millet's drought response is mediated by genes unique to this species or its close relatives.

---

## 2. Materials and Methods

### 2.1 RNA-seq Data

Publicly available RNA-seq data were obtained from the DNA Data Bank of Japan (DDBJ) under accession DRS049651 (BioProject: DRP005412; Hatakeyama et al., 2018). The dataset comprises paired-end Illumina HiSeq 4000 reads from leaf tissue of *Eleusine coracana* subsp. *coracana* sampled under well-irrigated control (n = 3; DRR095904, DRR095905, DRR095906) and drought-stressed (n = 3; DRR095907, DRR095908, DRR095909) conditions. Raw FASTQ files were downloaded directly from the European Nucleotide Archive (ENA) FTP server.

### 2.2 Reference Genome

The *E. coracana* chromosome-scale genome assembly GCA_032690845.1 (*Eleusine_coracana_v1.0*) and its associated GFF3 annotation were downloaded from NCBI using the NCBI datasets command-line tool. The genome comprises 9 pseudochromosomes with a total assembly size of approximately 1.1 Gb.

### 2.3 Quality Control and Read Trimming

Raw read quality was assessed using FastQC v0.12 and MultiQC v1.25. Adapter sequences and low-quality bases were removed using Trimmomatic v0.40 in paired-end mode with the following parameters: ILLUMINACLIP:TruSeq3-PE.fa:2:30:10, LEADING:3, TRAILING:3, SLIDINGWINDOW:4:15, MINLEN:36. All trimmed files were verified for integrity using gzip integrity checking.

### 2.4 Read Alignment

Trimmed paired-end reads were aligned to the reference genome using HISAT2 v2.2.1. A genome index was constructed from the reference FASTA using hisat2-build. Alignment was performed with the following parameters: --score-min L,0,-0.5, --no-mixed, --no-discordant, --mp 4,2, --rdg 5,3, --rfg 5,3, --rna-strandness RF, --dta, --min-intronlen 20, --max-intronlen 500000. Aligned reads were filtered for mapping quality (MAPQ ≥ 20) using SAMtools v1.21 and sorted by genomic coordinate.

### 2.5 Transcript Assembly and Novel Gene Detection

Transcript assembly was performed for each sample independently using StringTie v2.2.1, guided by the reference annotation. Sample-level assemblies were merged using StringTie --merge to produce a consensus transcriptome. Novel transcripts were identified by comparison with the reference annotation using GFFCompare v0.12.6. Transcripts assigned GFFCompare class code "u" (intergenic, no overlap with any annotated feature) were classified as novel intergenic transcripts and retained for downstream analysis.

### 2.6 Differential Expression Analysis

Read abundance for all novel transcripts was estimated using StringTie in count mode (--e flag) against the merged assembly. Count matrices were constructed from per-sample GTF output files. Differential expression analysis was performed using DESeq2 v1.46 in R v4.4, comparing drought-stressed (n = 3) versus control (n = 3) conditions. Transcripts were considered significantly drought-upregulated if they met the following criteria: adjusted p-value < 0.05 (Benjamini-Hochberg correction) and log₂ fold change ≥ 1.5. The Wald test was used for hypothesis testing, and library sizes were normalised using DESeq2's median-of-ratios method.

### 2.7 Sequence Extraction and Homology Search

Genomic sequences of novel drought-upregulated transcripts were extracted from the reference genome using BEDTools v2.31 getfasta. Translated protein sequences were predicted using BLASTx v2.15 against the UniProt Swiss-Prot database (release 2025_01; 574,627 sequences) using an E-value threshold of 1×10⁻⁵, retaining up to 5 hits per query (--max_target_seqs 5, -num_threads 4, -outfmt 6). Transcripts with no significant BLASTx hit were classified as encoding proteins with no known homolog.

### 2.8 Protein-coding Potential and Domain Annotation

Open reading frame (ORF) prediction was performed on the top 50 candidate transcripts (ranked by adjusted p-value) using TransDecoder v5.7.1 with a minimum ORF length of 100 amino acids (--single_best_only flag). Predicted protein sequences were submitted to the InterProScan web server (version 5.77-108.0) for domain annotation against all available databases including Pfam, PANTHER, SUPERFAMILY, Gene3D, Phobius, SignalP, and TMHMM.

### 2.9 Candidate Gene Prioritisation

Novel drought-upregulated transcripts were stratified into three priority tiers based on BLASTx results and expression magnitude:

- **Tier 1 — Highly induced, no homolog:** No BLASTx hit and log₂FC ≥ 3 (≥8-fold upregulated)
- **Tier 1 — No homolog:** No BLASTx hit and log₂FC < 3
- **Tier 2 — Stress-related homolog:** BLASTx hit to a protein with known involvement in stress response, signalling, or protection
- **Tier 3 — Other homolog:** BLASTx hit to a protein of other function

### 2.10 Reproducibility and Code Availability

The entire analysis was implemented as a Snakemake v9.19 pipeline to ensure full reproducibility. All software was managed using conda/mamba environments. The pipeline code, configuration files, and result summaries are available at [GitHub repository — to be added upon submission].

---

## 3. Results

### 3.1 RNA-seq Quality and Alignment

After quality trimming, an average of [X] million read pairs per sample were retained (range: [X]–[X] million). Alignment rates to the *E. coracana* reference genome ranged from [X]% to [X]%, consistent with expectations for a well-assembled reference genome (Table 1). The highest alignment rate was observed for DRR095906 (96.22%), confirming the high quality of both the sequencing data and the reference genome assembly.

### 3.2 Novel Transcript Detection

StringTie assembled transcripts from all six samples were merged into a consensus transcriptome comprising [X] total transcripts. Comparison with the reference annotation using GFFCompare identified **21,864 novel intergenic transcripts** (class code "u") absent from the current genome annotation (Figure 1). These novel transcripts represent genomic loci not captured by the existing annotation, suggesting that a substantial proportion of the finger millet transcriptome remains unannotated.

### 3.3 Differential Expression of Novel Transcripts

DESeq2 analysis identified **2,354 novel transcripts significantly upregulated under drought stress** (adjusted p-value < 0.05, log₂FC ≥ 1.5) (Figure 2, volcano plot). The top candidates displayed remarkably strong statistical evidence, with adjusted p-values as low as 6.73×10⁻⁶⁶ (MSTRG.20738.1), reflecting highly consistent upregulation across all three drought replicates. Expression fold changes among the top candidates ranged from 3-fold to over 22-fold (Table 2).

The three most significant novel drought-upregulated transcripts were:

- **MSTRG.20738.1**: log₂FC = 2.59, baseMean = 2,198, padj = 6.73×10⁻⁶⁶
- **MSTRG.6647.1**: log₂FC = 3.37, baseMean = 1,212, padj = 8.71×10⁻⁵⁸
- **MSTRG.31255.1**: log₂FC = 4.46, baseMean = 11,373, padj = 8.07×10⁻⁵⁷

### 3.4 The Majority of Novel Drought Genes Lack Known Protein Homologs

BLASTx comparison against UniProt Swiss-Prot revealed that **99.6% of novel drought-upregulated transcripts (2,344 of 2,354) had no significant homology to any characterised protein** (E-value < 1×10⁻⁵). Only 10 transcripts matched known proteins, yielding the following candidate tiers:

| Tier | Description | Count |
|------|-------------|-------|
| Tier 1 | No homolog, highly induced (log₂FC ≥ 3) | 1,802 |
| Tier 1 | No homolog | 542 |
| Tier 2 | Stress-related protein homolog | 3 |
| Tier 3 | Other protein homolog | 7 |
| **Total** | | **2,354** |

This near-complete absence of homology to characterised proteins suggests that a large fraction of finger millet's drought response is mediated by genes that are either unique to *E. coracana*, unique to the Chloridoideae subfamily, or represent highly diverged members of known protein families that are undetectable by sequence similarity alone.

### 3.5 Novel Transcripts with Stress-Related Homologs

Three Tier 2 transcripts — those matching stress-associated proteins — warrant particular attention:

**MSTRG.9128.2** matched Ceramide Kinase (CERK) from *Oryza sativa* subsp. *japonica* (log₂FC = 2.57, padj = 0.0014). Ceramide kinase phosphorylates ceramide to produce ceramide-1-phosphate, a signalling lipid involved in the regulation of programmed cell death and stress responses. Upregulation of a ceramide kinase homolog suggests that sphingolipid-mediated cell death regulation may contribute to drought adaptation in finger millet.

**MSTRG.37761.2** matched Monodehydroascorbate Reductase 3 (MDAR3) from *O. sativa* subsp. *japonica* (log₂FC = 9.51, padj = 4.97×10⁻⁷). MDAR3 is a key enzyme in the ascorbate-glutathione cycle, which protects plants from oxidative damage generated during drought stress. The exceptionally high fold change (approximately 730-fold) highlights this as one of the most dramatically induced transcripts in our dataset.

**MSTRG.34630.1** matched Small Ubiquitin-related Modifier 1 (SUMO1) from *O. sativa* subsp. *japonica* (log₂FC = 6.11, padj = 0.0056). SUMOylation is a well-characterised post-translational modification pathway activated during abiotic stress in plants, facilitating rapid reprogramming of protein function and gene expression without de novo protein synthesis.

### 3.6 Protein-coding Potential of Top Candidates

TransDecoder ORF prediction on the top 50 candidates (by adjusted p-value) identified complete or partial ORFs in **44 of 50 transcripts (88%)**, confirming that the large majority of top candidates are protein-coding genes rather than non-coding RNAs (Table 3). The six candidates lacking ORFs (MSTRG.14681.1, MSTRG.46022.1, MSTRG.14947.1, MSTRG.45098.4, MSTRG.6129.1, MSTRG.26934.1) are classified as putative drought-responsive long non-coding RNAs (lncRNAs) — an emerging class of stress regulators in plants.

### 3.7 InterProScan Domain Annotation of Top Candidates

InterProScan analysis of the 44 predicted protein sequences revealed functionally informative domain architectures for several key candidates:

**MSTRG.31255.1** (log₂FC = 4.46, 22-fold upregulated): Multiple orthogonal algorithms (Phobius, SignalP-EUK, TMHMM) consistently identified a signal peptide and transmembrane helix, classifying this protein as secreted or membrane-associated. Secreted proteins are commonly induced during drought to protect the cell wall and apoplast from dehydration damage.

**MSTRG.20738.1** (log₂FC = 2.59, the most statistically significant candidate): InterProScan identified an ARM (Armadillo) repeat domain (SUPERFAMILY classification). ARM repeats mediate protein-protein interactions and are components of several plant drought signalling pathways, including the ABA receptor complex and the proteasomal degradation machinery activated under stress.

**MSTRG.21998.1**: InterProScan identified a Phosphatidylinositol-4-phosphate 5-Kinase (PIPK) domain confirmed by multiple databases (Pfam: PF01504, PANTHER, SMART: PIPK_2, ProSiteProfiles). PIP kinases phosphorylate phosphoinositides to generate second messengers that regulate ion channel activity, vacuolar functions, and stomatal closure — all critical processes in plant drought responses. This represents a particularly strong functional candidate for drought adaptation.

**MSTRG.6647.1** (log₂FC = 3.37): A signal peptide was confirmed by Phobius and SignalP, and PANTHER assigned this protein to the MYB-binding protein family. MYB transcription factors are master regulators of abiotic stress responses in plants, and proteins that interact with MYB factors may play important regulatory roles in drought gene expression networks.

---

## 4. Discussion

### 4.1 Advantages of Reference-guided Over De Novo Approaches

Previous transcriptomic analysis of finger millet drought response by Parvathi et al. (2019) using de novo Trinity assembly identified 1,790 differentially expressed transcripts. Our reference-guided approach, enabled by the availability of the chromosome-scale genome, identified 2,354 novel drought-upregulated transcripts alone — transcripts that are absent from the current annotation and would not have been discoverable by de novo assembly. Reference-guided assembly anchors transcripts to specific genomic coordinates, eliminates many assembly chimeras, enables strand-specific analysis, and provides a more reliable foundation for downstream analyses including ORF prediction and synteny analysis.

### 4.2 The Uncharacterised Drought Proteome of Finger Millet

The finding that 99.6% of novel drought-upregulated transcripts lack homology to characterised proteins is remarkable and warrants discussion. Several non-exclusive explanations may account for this observation. First, finger millet belongs to the subfamily Chloridoideae, which is phylogenetically distant from the model species and major crops whose proteomes dominate reference databases. Genes that evolved specifically within this lineage would not be expected to have close homologs in Swiss-Prot. Second, some genes may represent highly diverged members of known protein families whose sequence similarity has been eroded to below the BLASTx detection threshold, despite conservation of structural or functional features. Third, a subset may be genuinely novel genes with no evolutionary precedent — sometimes called "orphan genes" or "de novo evolved genes" — which have been documented in other plant lineages as contributors to species-specific stress adaptations. Discriminating between these possibilities will require structural modelling, synteny analysis, and ultimately experimental characterisation.

### 4.3 Key Candidates for Functional Validation

Based on the combined evidence from expression magnitude, statistical significance, protein-coding potential, and domain annotation, we prioritise the following candidates for experimental follow-up:

**Priority 1 — MSTRG.21998.1 (PIPK domain):** The confirmation of a phosphatidylinositol phosphate kinase domain by five independent databases provides the strongest functional annotation of any candidate in our dataset. PIP kinases are druggable targets and their manipulation has been shown to alter drought tolerance in model plants. qRT-PCR validation followed by overexpression or CRISPR-based functional analysis in a tractable plant system would be highly informative.

**Priority 2 — MSTRG.37761.2 (MDAR3 homolog, 730-fold induced):** The extraordinary induction magnitude of this transcript under drought, combined with its homology to a well-characterised antioxidant enzyme, makes it a compelling candidate for contributing to ROS scavenging during water deficit.

**Priority 3 — MSTRG.31255.1 (secreted protein, 22-fold induced):** The high expression level, strong statistical significance, confirmed signal peptide, and lack of any known homolog make this an intriguing candidate for a finger millet-specific secreted drought-protective protein.

**Priority 4 — MSTRG.20738.1 (ARM repeat, most significant p-value):** With the smallest adjusted p-value in the entire dataset (6.73×10⁻⁶⁶), this transcript shows exceptional consistency across replicates. ARM repeat proteins are scaffolding proteins in signalling complexes, and this candidate may represent a novel component of the drought signalling network in finger millet.

### 4.4 Drought-responsive lncRNAs in Finger Millet

The identification of six putative drought-responsive lncRNAs adds a further dimension to the novel gene catalogue. Long non-coding RNAs are increasingly recognised as important regulators of plant stress responses, acting through mechanisms including epigenetic modification, RNA-protein interactions, and competition for miRNA binding. To our knowledge, this represents the first report of drought-responsive lncRNAs in finger millet identified by reference-guided analysis.

### 4.5 Limitations and Future Directions

Several limitations of the present study should be acknowledged. First, the RNA-seq data analysed here derive from a single publicly available dataset (Hatakeyama et al., 2018), comprising three replicates per condition — sufficient for statistical analysis but limited in terms of biological diversity. Validation across multiple finger millet varieties and growth conditions will be necessary to establish the generality of our findings. Second, the novel transcripts identified here have not yet been experimentally validated; confirmation by qRT-PCR, northern blotting, or ribosome profiling remains an important next step. Third, the annotation of 99.6% of novel candidates as having no known homolog, while biologically significant, also reflects the limitations of current protein databases with respect to Chloridoideae diversity. Structural characterisation using AlphaFold2 or related tools may reveal hidden functional relationships not apparent from sequence alone.

Future work should prioritise: (1) qRT-PCR validation of the top 10 candidates across a panel of finger millet varieties under controlled drought conditions; (2) structural modelling of the uncharacterised proteins using AlphaFold2; (3) synteny analysis to determine whether novel loci are conserved in related species such as *Eleusine indica* or *Dactyloctenium aegyptium*; and (4) development of a finger millet transformation system to enable functional validation by overexpression or gene silencing.

---

## 5. Conclusions

Using a reference-guided bioinformatics pipeline applied to the newly available chromosome-scale finger millet genome, we have identified 2,354 novel transcripts upregulated under drought stress — the largest catalogue of novel drought-responsive gene candidates in *Eleusine coracana* to date. The near-complete absence of homology to characterised proteins suggests that finger millet's exceptional drought tolerance is underpinned in part by a unique molecular repertoire that has not previously been accessible to researchers. Transcripts with signal peptides, ARM repeat domains, PIP kinase domains, and MYB-binding protein features represent compelling priorities for experimental validation. We make all data and code fully available to facilitate collaborative validation efforts and to accelerate the translation of these findings into crop improvement strategies for water-limited environments.

---

## Data Availability

Raw RNA-seq data are available from DDBJ under accession DRS049651. The reference genome is available from NCBI under accession GCA_032690845.1. The analysis pipeline (Snakemake), configuration files, and result tables are available at [GitHub URL — to be added]. The InterProScan job ID for this analysis is: iprscan5-R20260417-190817-0777-66196655-p1m.

---

## Author Contributions

J.[Surname] conceived the study, developed and executed the bioinformatics pipeline, analysed the results, and wrote the manuscript.

---

## Acknowledgements

The author thanks the developers of HISAT2, StringTie, GFFCompare, DESeq2, TransDecoder, and InterProScan for providing open-source tools that made this analysis possible. The chromosome-scale genome assembly was generated by Hatakeyama et al. and made publicly available through NCBI. [Add any institutional support here.]

---

## Competing Interests

The author declares no competing interests.

---

## References

1. FAO (2023). The State of Food and Agriculture 2023. Rome: Food and Agriculture Organization of the United Nations.

2. Hatakeyama M, et al. (2018). Multiple hybrid de novo genome assembly of finger millet, an orphan allotetraploid crop. *DNA Research*, 25(1), 39–47.

3. Parvathi MS, et al. (2019). Transcriptome analysis of finger millet (*Eleusine coracana* (L.) Gaertn.) reveals unique drought responsive genes. *Journal of Genetics*, 98, 46.

4. Parvathi MS, et al. (2013). Expression analysis of stress responsive pathway genes linked to drought hardiness in an adapted crop, finger millet (*Eleusine coracana*). *Journal of Plant Biochemistry and Biotechnology*, 22, 192–201.

5. Pertea M, et al. (2015). StringTie enables improved reconstruction of a transcriptome from RNA-seq reads. *Nature Biotechnology*, 33, 290–295.

6. Kim D, et al. (2019). Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype. *Nature Biotechnology*, 37, 907–915.

7. Love MI, Huber W, Anders S (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15, 550.

8. Camacho C, et al. (2009). BLAST+: architecture and applications. *BMC Bioinformatics*, 10, 421.

9. Haas BJ, et al. (2013). De novo transcript sequence reconstruction from RNA-seq using the Trinity platform for reference generation and analysis. *Nature Protocols*, 8, 1494–1512.

10. Jones P, et al. (2014). InterProScan 5: genome-scale protein function classification. *Bioinformatics*, 30, 1236–1240.

11. Upadhyaya HD, Gowda CLL, Reddy VG (2007). Morphological diversity in finger millet germplasm introduced from southern and Eastern Africa. *Journal of SAT Agricultural Research*, 3, 1–3.

12. Vetriventhan M, et al. (2015). Finger and foxtail millets. In: *Genetic and Genomic Resources for Grain Cereals Improvement* (eds. Singh M, Upadhyaya HD), pp. 291–319. Academic Press.

13. Köster J, Rahmann S (2012). Snakemake — a scalable bioinformatics workflow engine. *Bioinformatics*, 28, 2520–2522.

14. Quinlan AR, Hall IM (2010). BEDTools: a flexible suite of utilities for comparing genomic features. *Bioinformatics*, 26, 841–842.

---

## Tables

**Table 1.** Summary of RNA-seq alignment statistics for all six samples.

| Sample | Condition | Total Reads | Alignment Rate |
|--------|-----------|-------------|----------------|
| DRR095904 | Control | [X] | [X]% |
| DRR095905 | Control | [X] | [X]% |
| DRR095906 | Control | [X] | 96.22% |
| DRR095907 | Drought | [X] | [X]% |
| DRR095908 | Drought | [X] | [X]% |
| DRR095909 | Drought | [X] | [X]% |

**Table 2.** Top 10 novel drought-upregulated transcripts ranked by adjusted p-value.

| Transcript ID | log₂FC | baseMean | padj | Tier | Annotation |
|---------------|--------|----------|------|------|------------|
| MSTRG.20738.1 | 2.59 | 2,198 | 6.73e-66 | Tier 1 | ARM repeat domain |
| MSTRG.6647.1 | 3.37 | 1,212 | 8.71e-58 | Tier 1 | Signal peptide; MYB-binding |
| MSTRG.31255.1 | 4.46 | 11,373 | 8.07e-57 | Tier 1 | Signal peptide; secreted |
| MSTRG.45758.1 | 3.50 | 2,035 | 2.83e-52 | Tier 3 | Transposable element |
| MSTRG.36758.1 | 2.97 | 395 | 2.54e-43 | Tier 1 | No homolog |
| MSTRG.14681.1 | 2.47 | 86,393 | 2.86e-42 | Tier 1 | lncRNA (no ORF) |
| MSTRG.45757.2 | 3.50 | [X] | [X] | Tier 1 | No homolog |
| MSTRG.4687.1 | [X] | [X] | [X] | Tier 1 | No homolog |
| MSTRG.333.1 | [X] | [X] | [X] | Tier 1 | No homolog |
| MSTRG.14874.2 | [X] | [X] | [X] | Tier 1 | No homolog |

**Table 3.** TransDecoder ORF prediction summary for top 50 candidates.

| Category | Count | Percentage |
|----------|-------|------------|
| Complete ORF predicted | 44 | 88% |
| No ORF (putative lncRNA) | 6 | 12% |
| **Total** | **50** | |

---

## Figure Legends

**Figure 1.** Volcano plot of differential expression analysis comparing drought-stressed versus control finger millet leaf tissue. Red triangles indicate novel drought-upregulated transcripts (n = 2,354). Dashed lines indicate thresholds of log₂FC = ±1.5 and adjusted p-value = 0.05.

**Figure 2.** Heatmap of expression patterns for novel drought-upregulated transcripts across all six samples (three control: DRR095904–906; three drought: DRR095907–909). Colour scale represents variance-stabilised, row-scaled expression values.

**Figure 3.** Schematic of the bioinformatics pipeline used in this study, from raw reads to candidate gene prioritisation.

**Figure 4.** InterProScan domain architecture of top protein-coding candidates, illustrating signal peptides, ARM repeat domains, and kinase domains identified in priority candidates.
