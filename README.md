# CX-5461 Immunogenomics Workflow

![Home Screenshot](https://raw.githubusercontent.com/aidbiolab/immunogenomics/main/Home.png)

## Project Overview

This repository contains a comprehensive computational pipeline for **neoantigen prediction** and **immune biomarker discovery** in the context of **CX-5461 (Pidnarulex)** treatment — a selective G-quadruplex stabilizer currently under investigation in multiple cancer types.

The workflow is primarily optimized for **High-Homologous Recombination Deficiency (HRD) Breast Cancer** subsets, where tumors with impaired DNA repair pathways show heightened sensitivity to CX-5461-induced replication stress and potential immunogenicity enhancement.

The architecture is modular and designed to be scalable to other solid tumors, particularly **Colorectal Cancer (CRC)**, by simply swapping data sources (e.g., TCGA-COAD/READ instead of TCGA-BRCA) and adjusting mutational signature parameters.

This project builds upon and extends previous genomic characterizations of breast cancer in underrepresented populations. For foundational context on gene mutational profiles and expression alterations in ductal luminal breast cancer from Southwest Colombia, see:

> Cortes-Urrea, C.; Bueno-Gutiérrez, F.; Solarte, M.; Guevara-Burbano, M.; Tobar-Tosse, F.; Vélez-Varela, P.E.; Bonilla, J.C.; Barreto, G.; Velasco-Medina, J.; Moreno, P.A.; De Las Rivas, J. **Exomes of Ductal Luminal Breast Cancer Patients from Southwest Colombia: Gene Mutational Profile and Related Expression Alterations**. *Biomolecules* 2020, **10**(5), 698.  
> DOI: [10.3390/biom10050698](https://doi.org/10.3390/biom10050698)

That study identified recurrent alterations in key drivers (TP53, PIK3CA, ESR1) and pathways (PI3K-AKT, TGF-β), providing critical biological rationale for the neoantigen simulation and prioritization strategies implemented here.

## Background & Scientific Rationale

CX-5461 induces replication fork stalling at G-quadruplex structures, leading to synthetic lethality in HRD-deficient cells and the generation of novel somatic mutations. These treatment-induced variants can give rise to neoantigens potentially recognizable by the adaptive immune system.

This pipeline simulates CX-5461-like mutational signatures, predicts MHC class I binding affinities, integrates multi-omics data, and applies deep learning to rank high-confidence neoepitopes — paving the way for personalized immunotherapy combinations in HRD-enriched cancers.

## The 4-Step Workflow

### 1. Data Acquisition  
[`scripts/step1_download_data.py`](scripts/step1_download_data.py)

- Programmatic access to **GDC API** (Genomic Data Commons) for TCGA-BRCA metadata, somatic mutations, RNA-seq, and clinical data  
- HRD-high cohort selection using LST/TAI/LOH scores, BRCA1/2 status, and demographic filters  
- Output: clean, harmonized datasets saved in `/data/`

### 2. Neoantigen Prediction  
[`scripts/step2_neoantigen_prediction.py`](scripts/step2_neoantigen_prediction.py)

- Simulation of **CX-5461-induced SBS mutational signatures** based on COSMIC reference patterns  
- Variant-to-peptide translation and MHC binding affinity prediction using **NetMHCpan-4.1** (pan-allele) and **MHCflurry**  
- Filtering: IC50 < 500 nM (strong binders), percentile rank < 2%  
- Output: ranked neoepitope candidates in `/data/neoantigens.csv`

### 3. Multi-Omics Integration  
[`scripts/step3_integration.R`](scripts/step3_integration.R)

- Integration of predicted neoantigens with RNA-seq expression (DESeq2 differential analysis)  
- Correlation with experimental signatures from CX-5461-treated cell lines (GEO GSE series)  
- Prioritization based on expression level (>1 TPM), fold-change, and immune-related pathway enrichment  
- Output: integrated multi-omics tables and visualizations in `/data/` and `/assets/`

### 4. Machine Learning Architecture  
[`models/step4_ml_model.py`](models/step4_ml_model.py)

- **NeoPredictor**: PyTorch-based multi-modal neural network  
- Inputs: peptide sequence embeddings (ESM/ProtBERT), HRD scores, gene expression levels  
- Task: binary classification (immunogenic vs. non-immunogenic) or regression of immunogenicity score  
- Training with cross-validation, GPU support, and evaluation using AUC-ROC, PR-AUC, F1  
- Output: trained models (`/models/neo_predictor.pth`) and final predictions (`/data/predictions.csv`)

## Key Technical Skills Demonstrated

- Cancer genomics & large-scale data mining (TCGA, GDC API, ICGC)  
- Immunoinformatics (MHC binding prediction, neoantigen prioritization)  
- Multi-omics integration (R: TCGAbiolinks, DESeq2; Python: pandas, biopython)  
- Deep learning for biomarker discovery (PyTorch, custom architectures)  
- Reproducible workflows with modular scripts and clear documentation

## Scalability to Colorectal Cancer (CRC)

The pipeline is intentionally designed for extension to CRC:

- Replace TCGA-BRCA queries with TCGA-COAD/READ in Step 1  
- Adjust mutational signature weights to reflect CRC-specific CX-5461 responses  
- Incorporate MSI status and tumor microenvironment features (CIBERSORT, xCell)  
- Potential application: prediction of neoantigens targetable by CIK cells or checkpoint inhibitors post-CX-5461

## Installation & Quick Start

```bash
# Clone repository
git clone https://github.com/aidbiolab/immunogenomics.git
cd immunogenomics

# Install Python dependencies
pip install -r requirements.txt   # (create this file if needed)

# Install R packages (run in R)
install.packages(c("TCGAbiolinks", "DESeq2", "edgeR"))

# Install external tools manually:
# - NetMHCpan-4.1 → http://www.cbs.dtu.dk/services/NetMHCpan/
# - MHCflurry    → pip install mhcflurry

Then run the steps sequentially:
python scripts/step1_download_data.py
python scripts/step2_neoantigen_prediction.py
Rscript scripts/step3_integration.R
python models/step4_ml_model.py
