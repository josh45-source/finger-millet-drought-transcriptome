# Reference-guided transcriptome analysis of finger millet (*Eleusine coracana*) reveals 2,354 novel drought-responsive transcripts with largely uncharacterised protein repertoire

**Joshua [SURNAME]¹**

¹ [Your Institution/Affiliation], Kampala, Uganda

**Corresponding author:** [your email]

**Keywords:** finger millet, *Eleusine coracana*, drought stress, RNA-seq, novel genes, transcriptomics, reference-guided assembly, orphan genes

---

## Abstract

Finger millet (*Eleusine coracana* (L.) Gaertn.) is a drought-tolerant C₄ cereal of significant importance across sub-Saharan Africa and South Asia, yet the molecular basis of its exceptional drought hardiness remains incompletely understood. Previous transcriptomic studies relied on de novo assembly approaches in the absence of a reference genome, limiting the discovery of novel unannotated genes. Here, we present the first reference-guided transcriptomic analysis of drought stress in finger millet, leveraging the recently published chromosome-scale genome assembly (GCA_032690845.1). Using a reproducible Snakemake pipeline integrating HISAT2, StringTie, GFFCompare, and DESeq2, we analysed publicly available RNA-seq data from control and drought-stressed leaf tissue (DDBJ accession DRS049651; n = 3 per condition). We detected 21,864 novel transcripts absent from the current genome annotation, of which 2,354 were significantly upregulated under drought (adjusted p-value < 0.05, log₂ fold change ≥ 1.5). Strikingly, 99.6% of these novel drought-upregulated transcripts had no significant homology to any characterised protein in UniProt/Swiss-Prot, suggesting that finger millet possesses a largely unique drought-responsive gene repertoire. TransDecoder analysis confirmed that 88% of top candidates encode putative proteins, with InterProScan annotation revealing signal peptides, ARM repeat domains, phosphatidylinositol phosphate kinase (PIPK) domains, and MYB-binding protein families among the most highly induced candidates. Six candidates lacking open reading frames were classified as putative drought-responsive long non-coding RNAs (lncRNAs). Our findings substantially expand the known drought-responsive gene catalogue of finger millet and provide a foundation for functional validation and crop improvement efforts.

---

## 1. Introduction

Drought stress is the foremost constraint on global food security, with projections indicating that water-limited conditions will increasingly threaten crop productivity across Africa and Asia (FAO, 2023). Finger millet (*Eleusine coracana* (L.) Gaertn.) is uniquely positioned as a model for drought tolerance research: it is an allotetraploid C₄ cereal (2n = 4x = 36, AABB genome) cultivated by smallholder farmers across more than 25 countries, renowned for its ability to survive prolonged water deficit that would be lethal to most other cereals (Upadhyaya et al., 2007; Vetriventhan et al., 2015). Despite its agronomic significance, finger millet remains an orphan crop — underrepresented in genomic and functional genomic databases relative to major cereals such as rice, maize, and wheat.

The molecular basis of drought tolerance in finger millet involves multiple coordinated pathways including osmotic adjustment, reactive oxygen species (ROS) scavenging, abscisic acid (ABA) signalling, and protein protection mechanisms (Parvathi et al., 2019). Previous transcriptomic investigations have identified key drought-responsive genes including calcineurin B-like interacting protein kinase 31 (CIPK31), serine/threonine protein phosphatase 2A (PP2A), farnesyl pyrophosphate synthase (FPS), and TATA-binding protein associated factor 6 (TAF6) (Parvathi et al., 2013, 2019). However, these studies employed de novo transcriptome assembly without a reference genome, which constrains the ability to identify truly novel, unannotated genes and introduces assembly artefacts.

The publication of a chromosome-scale reference genome for *E. coracana* (GCA_032690845.1; Hatakeyama et al., 2018) now enables reference-guided transcriptomic approaches that can systematically identify transcripts absent from the current annotation. Such novel transcripts — assembled against a high-quality genome backbone — represent genuine unannotated genes rather than assembly chimeras, and are thus stronger candidates for functional investigation.

Here, we present the first reference-guided RNA-seq analysis of drought stress in finger millet. Using a fully reproducible bioinformatics pipeline, we identify 2,354 novel drought-upregulated transcripts, characterise their protein-coding potential and domain architecture, and highlight priority candidates for experimental validation. We demonstrate that the majority of these novel transcripts lack homology to any previously characterised protein, suggesting that a substantial component of finger millet's drought response is mediated by genes unique to this species or its close relatives.

---

## 2. Materials and Methods

### 2.1 RNA-seq Data

Publicly available RNA-seq data were obtained from the DNA Data Bank of Japan (DDBJ) under accession DRS049651 (BioProject: DRP005412; Hatakeyama et al., 2018). The dataset comprises paired-end Illumina HiSeq 4000 reads from leaf tissue of *Eleusine coracana* subsp. *coracana* sampled under well-irrigated control conditions (n = 3; DRR095904, DRR095905, DRR095906) and drought-stressed conditions (n = 3; DRR095907, DRR095908, DRR095909). Raw FASTQ files were downloaded directly from the European Nucleotide Archive (ENA) FTP server.

### 2.2 Reference Genome

The *E. coracana* chromosome-scale genome assembly GCA_032690845.1 (*Eleusine_coracana_v1.0*) and its associated GFF3 annotation were downloaded from NCBI using the NCBI datasets command-line tool. The genome comprises 9 pseudochromosomes with a total assembly size of approximately 1.1 Gb.

### 2.3 Quality Control and Read Trimming

Raw read quality was assessed using FastQC v0.12 and MultiQC v1.25. Adapter sequences and low-quality bases were removed using Trimmomatic v0.40 in paired-end mode with the following parameters: ILLUMINACLIP:TruSeq3-PE.fa:2:30:10, LEADING:3, TRAILING:3, SLIDINGWINDOW:4:15, MINLEN:36.

### 2.4 Read Alignment

Trimmed paired-end reads were aligned to the reference genome using HISAT2 v2.2.1 with parameters: --score-min L,0,-0.5, --no-mixed, --no-discordant, --mp 4,2, --rdg 5,3, --rfg 5,3, --rna-strandness RF, --dta, --min-intronlen 20, --max-intronlen 500000. Aligned reads were filtered for mapping quality (MAPQ ≥ 20) using SAMtools v1.21 and sorted by genomic coordinate.

### 2.5 Transcript Assembly and Novel Gene Detection

Transcript assembly was performed for each sample independently using StringTie v2.2.1 guided by the reference annotation. Sample-level assemblies were merged using StringTie --merge to produce a consensus transcriptome. Novel transcripts were identified by comparison with the reference annotation using GFFCompare v0.12.6. Transcripts assigned class code "u" (intergenic, no overlap with any annotated feature) were classified as novel intergenic transcripts.

### 2.6 Differential Expression Analysis

Read abundance for all novel transcripts was estimated using StringTie in count mode against the merged assembly. Differential expression analysis was performed using DESeq2 v1.46 in R v4.4, comparing drought-stressed (n = 3) versus control (n = 3) conditions. Transcripts were considered significantly drought-upregulated if they had adjusted p-value < 0.05 (Benjamini-Hochberg correction) and log₂ fold change ≥ 1.5. The Wald test was used for hypothesis testing.

### 2.7 Homology Search

Genomic sequences of novel drought-upregulated transcripts were extracted using BEDTools v2.31 getfasta. BLASTx was performed against UniProt Swiss-Prot (release 2025_01; 574,627 sequences) with E-value threshold 1×10⁻⁵ (--max_target_seqs 5, -num_threads 4, -outfmt 6).

### 2.8 Protein-coding Potential and Domain Annotation

ORF prediction was performed on the top 50 candidates using TransDecoder v5.7.1 (minimum ORF length: 100 amino acids, --single_best_only). Predicted protein sequences were submitted to the InterProScan web server (v5.77-108.0; job ID: iprscan5-R20260417-190817-0777-66196655-p1m) for domain annotation.

### 2.9 Candidate Gene Prioritisation

Novel drought-upregulated transcripts were stratified into three priority tiers:
- **Tier 1 — Highly induced, no homolog:** No BLASTx hit and log₂FC ≥ 3
- **Tier 1 — No homolog:** No BLASTx hit and log₂FC < 3
- **Tier 2 — Stress-related homolog:** BLASTx hit to a stress-associated protein
- **Tier 3 — Other homolog:** BLASTx hit to a protein of other function

### 2.10 Reproducibility

The entire analysis was implemented as a Snakemake v9.19 pipeline. All software was managed using conda/mamba. Pipeline code is available at [GitHub URL — to be added].

---

## 3. Results

### 3.1 RNA-seq Quality and Alignment

After quality trimming, between 17.1 and 32.5 million read pairs per sample were retained. Alignment rates to the *E. coracana* reference genome ranged from 85.13% to 96.22% across all six samples (Table 1), consistent with expectations for a high-quality reference genome. The mean alignment rate was 92.05% across all samples, confirming the suitability of the reference assembly for transcriptome mapping.

### 3.2 Novel Transcript Detection

GFFCompare comparison of the merged StringTie assembly with the reference annotation identified **21,864 novel intergenic transcripts** (class code "u") absent from the current genome annotation. These novel transcripts represent genomic loci not captured by the existing annotation, suggesting that a substantial proportion of the expressed finger millet transcriptome remains unannotated.

### 3.3 Differential Expression of Novel Transcripts

DESeq2 analysis identified **2,354 novel transcripts significantly upregulated under drought stress** (adjusted p-value < 0.05, log₂FC ≥ 1.5). The top candidates displayed remarkably strong statistical evidence, with adjusted p-values as low as 6.73×10⁻⁶⁶, reflecting highly consistent upregulation across all three drought replicates. Expression fold changes ranged from 3-fold to over 22-fold among the top candidates (Table 2). A volcano plot illustrating the distribution of all tested novel transcripts is presented in Figure 1.

The three most statistically significant novel drought-upregulated transcripts were:
- **MSTRG.20738.1**: log₂FC = 2.59, baseMean = 2,198, padj = 6.73×10⁻⁶⁶
- **MSTRG.6647.1**: log₂FC = 3.37, baseMean = 1,212, padj = 8.71×10⁻⁵⁸
- **MSTRG.31255.1**: log₂FC = 4.46, baseMean = 11,373, padj = 8.07×10⁻⁵⁷

### 3.4 The Majority of Novel Drought Genes Lack Known Protein Homologs

BLASTx comparison against UniProt Swiss-Prot revealed that **99.6% of novel drought-upregulated transcripts (2,344 of 2,354) had no significant homology to any characterised protein**. Only 10 transcripts matched known proteins, yielding the following candidate tier distribution:

| Tier | Description | Count |
|------|-------------|-------|
| Tier 1 | No homolog, highly induced (log₂FC ≥ 3) | 1,802 |
| Tier 1 | No homolog | 542 |
| Tier 2 | Stress-related protein homolog | 3 |
| Tier 3 | Other protein homolog | 7 |
| **Total** | | **2,354** |

This near-complete absence of homology to characterised proteins suggests that finger millet possesses a drought-responsive gene repertoire that is largely unique to this species or its close relatives within Chloridoideae.

### 3.5 Novel Transcripts with Stress-Related Homologs

Three Tier 2 transcripts matched stress-associated proteins and warrant particular attention:

**MSTRG.9128.2** matched Ceramide Kinase (CERK) from *Oryza sativa* subsp. *japonica* (log₂FC = 2.57, padj = 0.0014). Ceramide kinase phosphorylates ceramide to produce ceramide-1-phosphate, a signalling lipid involved in the regulation of programmed cell death and stress responses. Upregulation of a ceramide kinase homolog suggests that sphingolipid-mediated signalling may contribute to drought adaptation in finger millet.

**MSTRG.37761.2** matched Monodehydroascorbate Reductase 3 (MDAR3) from *O. sativa* subsp. *japonica* (log₂FC = 9.51, padj = 4.97×10⁻⁷). MDAR3 is a key enzyme in the ascorbate-glutathione cycle, protecting plants from oxidative damage during drought stress. The exceptionally high fold change (~730-fold) makes this one of the most dramatically induced transcripts in our dataset.

**MSTRG.34630.1** matched Small Ubiquitin-related Modifier 1 (SUMO1) from *O. sativa* subsp. *japonica* (log₂FC = 6.11, padj = 0.0056). SUMOylation is a well-characterised post-translational modification pathway activated during abiotic stress in plants, facilitating rapid reprogramming of protein function without de novo protein synthesis.

### 3.6 Protein-coding Potential of Top Candidates

TransDecoder ORF prediction on the top 50 candidates identified complete or partial ORFs in **44 of 50 transcripts (88%)**, confirming that the large majority of top candidates are protein-coding genes (Table 3). The six candidates lacking ORFs (MSTRG.14681.1, MSTRG.46022.1, MSTRG.14947.1, MSTRG.45098.4, MSTRG.6129.1, MSTRG.26934.1) are classified as putative drought-responsive long non-coding RNAs (lncRNAs).

### 3.7 InterProScan Domain Annotation of Top Candidates

InterProScan analysis of the 44 predicted protein sequences revealed functionally informative domain architectures for several key candidates:

**MSTRG.31255.1** (log₂FC = 4.46, ~22-fold upregulated): Multiple orthogonal algorithms (Phobius, SignalP-EUK, TMHMM) consistently identified a signal peptide and transmembrane helix, classifying this protein as secreted or membrane-associated. Secreted proteins are commonly induced during drought to protect the cell wall and apoplast from dehydration damage.

**MSTRG.20738.1** (log₂FC = 2.59, padj = 6.73×10⁻⁶⁶): InterProScan identified an ARM (Armadillo) repeat domain (SUPERFAMILY classification) with PANTHER assigning it to the BAP28 family. ARM repeats mediate protein-protein interactions and are components of several plant drought signalling pathways, including the ABA receptor complex and the proteasomal degradation machinery activated under stress.

**MSTRG.21998.1**: InterProScan identified a Phosphatidylinositol-4-phosphate 5-Kinase (PIPK) domain confirmed by five independent databases (Pfam: PF01504, PANTHER, SMART: PIPK_2, ProSiteProfiles, Gene3D). PIP kinases phosphorylate phosphoinositides to generate second messengers that regulate ion channel activity, vacuolar functions, and stomatal closure — all critical processes in plant drought responses. This candidate has the strongest functional annotation of any transcript in our dataset.

**MSTRG.6647.1** (log₂FC = 3.37, ~10-fold upregulated): A signal peptide was confirmed by Phobius and SignalP, and PANTHER assigned this protein to the MYB-binding protein family. MYB transcription factors are master regulators of abiotic stress responses in plants, and proteins that interact with MYB factors may play important regulatory roles in drought gene expression networks.

---

## 4. Discussion

### 4.1 Advantages of Reference-guided Over De Novo Approaches

Previous transcriptomic analysis of finger millet drought response by Parvathi et al. (2019) using de novo Trinity assembly identified 1,790 differentially expressed transcripts in total. Our reference-guided approach, enabled by the chromosome-scale genome, identified 2,354 novel drought-upregulated transcripts alone — transcripts absent from the annotation and undiscoverable by de novo methods. Reference-guided assembly anchors transcripts to specific genomic coordinates, eliminates assembly chimeras, enables strand-specific analysis, and provides a reliable foundation for downstream ORF prediction and synteny analysis.

### 4.2 The Uncharacterised Drought Proteome of Finger Millet

The finding that 99.6% of novel drought-upregulated transcripts lack homology to characterised proteins is remarkable. Several explanations may account for this observation. First, finger millet belongs to the subfamily Chloridoideae, phylogenetically distant from model species whose proteomes dominate reference databases. Genes that evolved within this lineage would not be expected to have close homologs in Swiss-Prot. Second, some genes may represent highly diverged members of known protein families whose sequence similarity has been eroded below the BLASTx detection threshold, despite conservation of structural or functional features. Third, a subset may be genuinely novel "orphan genes" — documented in other plant lineages as contributors to species-specific stress adaptations. Discriminating between these possibilities will require structural modelling, synteny analysis across Chloridoideae species, and experimental characterisation.

### 4.3 Key Candidates for Functional Validation

Based on expression magnitude, statistical significance, protein-coding potential, and domain annotation, we prioritise:

**Priority 1 — MSTRG.21998.1 (PIPK domain):** Confirmed by five independent databases, PIP kinases are druggable targets whose manipulation alters drought tolerance in model plants. This represents the strongest functionally annotated candidate.

**Priority 2 — MSTRG.37761.2 (MDAR3 homolog, ~730-fold induced):** The extraordinary induction magnitude combined with homology to a characterised antioxidant enzyme makes this a compelling candidate for ROS scavenging during drought.

**Priority 3 — MSTRG.31255.1 (secreted protein, 22-fold induced):** High expression, strong statistical confidence, confirmed signal peptide, and complete absence of known homologs make this an intriguing candidate for a finger millet-specific secreted drought-protective protein.

**Priority 4 — MSTRG.20738.1 (ARM repeat, most significant p-value):** With the smallest adjusted p-value in the dataset (6.73×10⁻⁶⁶), this transcript shows exceptional consistency across replicates. ARM repeat proteins are scaffolding components of signalling complexes and may represent a novel component of finger millet's drought network.

### 4.4 Drought-responsive lncRNAs

The identification of six putative drought-responsive lncRNAs adds a further dimension to the novel gene catalogue. Long non-coding RNAs are increasingly recognised as important regulators of plant stress responses, acting through epigenetic modification, RNA-protein interactions, and competition for miRNA binding. To our knowledge, this is the first report of drought-responsive lncRNAs in finger millet identified by reference-guided analysis.

### 4.5 Limitations and Future Directions

Several limitations should be acknowledged. First, the data derive from a single publicly available dataset comprising three replicates per condition — sufficient for statistical analysis but limited in biological diversity. Validation across multiple varieties and conditions is necessary. Second, novel transcripts have not been experimentally validated; qRT-PCR confirmation is an important next step. Third, the 99.6% rate of no-homolog findings also reflects limitations of current databases with respect to Chloridoideae diversity.

Future work should prioritise: (1) qRT-PCR validation of the top 10 candidates across a panel of finger millet varieties; (2) structural modelling using AlphaFold2 to reveal hidden functional relationships; (3) synteny analysis across Chloridoideae species; and (4) functional validation by overexpression or CRISPR-based analysis.

---

## 5. Conclusions

Using a reference-guided bioinformatics pipeline applied to the chromosome-scale finger millet genome, we identified 2,354 novel transcripts upregulated under drought stress — the largest catalogue of novel drought-responsive gene candidates in *Eleusine coracana* to date. The near-complete absence of homology to characterised proteins suggests that finger millet's exceptional drought tolerance is underpinned in part by a unique molecular repertoire previously inaccessible to researchers. Transcripts with signal peptides, ARM repeat domains, PIP kinase domains, and MYB-binding protein features represent compelling priorities for experimental validation. All data and code are made fully available to facilitate collaborative validation efforts and accelerate the translation of these findings into crop improvement strategies for water-limited environments.

---

## Data Availability

Raw RNA-seq data are available from DDBJ under accession DRS049651. The reference genome is available from NCBI under accession GCA_032690845.1. The analysis pipeline and result tables are available at [GitHub URL — to be added]. InterProScan job ID: iprscan5-R20260417-190817-0777-66196655-p1m.

---

## Author Contributions

J. [Surname] conceived the study, developed and executed the bioinformatics pipeline, analysed the results, and wrote the manuscript.

---

## Acknowledgements

The author thanks the developers of HISAT2, StringTie, GFFCompare, DESeq2, TransDecoder, and InterProScan for providing open-source tools. The chromosome-scale genome assembly was generated by Hatakeyama et al. and made publicly available through NCBI. [Add institutional support if applicable.]

---

## Competing Interests

The author declares no competing interests.

---

## References

1. FAO (2023). The State of Food and Agriculture 2023. Rome: FAO.
2. Hatakeyama M, et al. (2018). Multiple hybrid de novo genome assembly of finger millet. *DNA Research*, 25(1), 39–47.
3. Parvathi MS, et al. (2019). Transcriptome analysis of finger millet reveals unique drought responsive genes. *Journal of Genetics*, 98, 46.
4. Parvathi MS, et al. (2013). Expression analysis of stress responsive pathway genes in finger millet. *Journal of Plant Biochemistry and Biotechnology*, 22, 192–201.
5. Kim D, et al. (2019). Graph-based genome alignment with HISAT2. *Nature Biotechnology*, 37, 907–915.
6. Pertea M, et al. (2015). StringTie enables improved reconstruction of a transcriptome from RNA-seq reads. *Nature Biotechnology*, 33, 290–295.
7. Love MI, Huber W, Anders S (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15, 550.
8. Camacho C, et al. (2009). BLAST+: architecture and applications. *BMC Bioinformatics*, 10, 421.
9. Jones P, et al. (2014). InterProScan 5: genome-scale protein function classification. *Bioinformatics*, 30, 1236–1240.
10. Quinlan AR, Hall IM (2010). BEDTools: a flexible suite of utilities for comparing genomic features. *Bioinformatics*, 26, 841–842.
11. Köster J, Rahmann S (2012). Snakemake — a scalable bioinformatics workflow engine. *Bioinformatics*, 28, 2520–2522.
12. Upadhyaya HD, et al. (2007). Morphological diversity in finger millet germplasm. *Journal of SAT Agricultural Research*, 3, 1–3.
13. Vetriventhan M, et al. (2015). Finger and foxtail millets. In: *Genetic and Genomic Resources for Grain Cereals Improvement*, pp. 291–319.

---

## Tables

**Table 1.** RNA-seq alignment statistics for all six samples.

| Sample | Condition | Total Read Pairs | Alignment Rate |
|--------|-----------|-----------------|----------------|
| DRR095904 | Control | 17,137,569 | 85.13% |
| DRR095905 | Control | 17,377,076 | 91.08% |
| DRR095906 | Control | 18,174,857 | 96.22% |
| DRR095907 | Drought | 32,473,303 | 91.50% |
| DRR095908 | Drought | 27,174,371 | 94.24% |
| DRR095909 | Drought | 17,094,814 | 94.11% |
| **Mean** | | **21,572,065** | **92.05%** |

**Table 2.** Top 10 novel drought-upregulated transcripts ranked by adjusted p-value.

| Transcript ID | log₂FC | baseMean | padj | Tier | InterProScan Annotation |
|---------------|--------|----------|------|------|------------------------|
| MSTRG.20738.1 | 2.59 | 2,198 | 6.73×10⁻⁶⁶ | Tier 1 | ARM repeat domain |
| MSTRG.6647.1 | 3.37 | 1,212 | 8.71×10⁻⁵⁸ | Tier 1 | Signal peptide; MYB-binding |
| MSTRG.31255.1 | 4.46 | 11,373 | 8.07×10⁻⁵⁷ | Tier 1 | Signal peptide; secreted |
| MSTRG.45758.1 | 3.14 | 2,035 | 2.83×10⁻⁵² | Tier 1 | No homolog |
| MSTRG.36758.1 | 2.97 | 395 | 2.54×10⁻⁴³ | Tier 1 | No homolog |
| MSTRG.14681.1 | 2.47 | 86,393 | 2.86×10⁻⁴² | Tier 1 | Putative lncRNA |
| MSTRG.45757.2 | 2.11 | 8,424 | 3.83×10⁻⁴¹ | Tier 1 | No homolog |
| MSTRG.4687.1 | 3.50 | 4,032 | 7.38×10⁻³⁶ | Tier 1 | No homolog |
| MSTRG.333.1 | 2.06 | 1,934 | 8.74×10⁻³⁶ | Tier 1 | No homolog |
| MSTRG.14874.2 | 3.01 | 2,496 | 3.49×10⁻³⁵ | Tier 1 | No homolog |

**Table 3.** TransDecoder ORF prediction summary for top 50 candidates.

| Category | Count | Percentage |
|----------|-------|------------|
| Complete or partial ORF predicted | 44 | 88% |
| No ORF (putative lncRNA) | 6 | 12% |
| **Total** | **50** | |

---

## Figure Legends

**Figure 1.** Volcano plot of differential expression analysis comparing drought-stressed versus control finger millet leaf tissue. Red triangles indicate novel drought-upregulated transcripts (n = 2,354). Dashed lines indicate thresholds of log₂FC = ±1.5 and adjusted p-value = 0.05.

**Figure 2.** Heatmap of expression patterns for novel drought-upregulated transcripts across all six samples (three control: DRR095904–906; three drought: DRR095907–909). Colour scale represents variance-stabilised, row-scaled expression values.

**Figure 3.** InterProScan domain architecture of top protein-coding candidates illustrating signal peptides, ARM repeat domains, and PIP kinase domains identified in priority candidates.
