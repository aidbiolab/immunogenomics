# CX-5461 Immunogenomics Workflow

![Project Showcase](index.html) <!-- Note: In GitHub, this would be a URL to the hosted page -->
![Home Screenshot](https://raw.githubusercontent.com/aidbiolab/immunogenomics/main/Home.png)

## Project Overview
This repository showcases a comprehensive computational framework for predicting neoantigens and identifying immune biomarkers in the context of **CX-5461 (Pidnarulex)** treatment. While optimized for **High-HRD Breast Cancer** subsets, the pipeline is architected to be systemically scalable to **Colorectal Cancer (CRC)** and other solid tumors sensitive to G-quadruplex stabilization.

## The 4-Step Workflow

### [1] Data Acquisition ([scripts/step1_download_data.py](scripts/step1_download_data.py))
*   Programmatic integration with **GDC API** for TCGA-BRCA metadata retrieval.
*   Filtering strategies for HRD-high cohorts and BRCA-mutant demographics.

### [2] Neoantigen Prediction ([scripts/step2_neoantigen_prediction.py](scripts/step2_neoantigen_prediction.py))
*   Simulation of **SBS-CX-5461** mutational signatures using COSMIC data.
*   Integration with **NetMHCpan-4.1** and **MHCflurry** for binding affinity modeling.

### [3] Multi-Omics Integration ([scripts/step3_integration.R](scripts/step3_integration.R))
*   Correlation of predicted variants with experimental RNA-seq signatures (GSE series).
*   Prioritization of high-affinity, upregulated epitopes.

### [4] Machine Learning Architecture ([models/step4_ml_model.py](models/step4_ml_model.py))
*   **NeoPredictor**: A PyTorch-based neural network that fusion-integrates peptide sequences with clinical HRD scores and expression levels.

## Key Technical Skills Demonstrated
*   **Cancer Genomics**: TCGA/ICGC data mining and API interaction.
*   **Immunoinformatics**: MHC binding prediction and epitope prioritization.
*   **Bioinformatics (R/Python)**: DESeq2, TCGAbiolinks, pandas, and data visualization.
*   **Machine Learning**: Deep learning for biomarker discovery with PyTorch.

## Scalability to CRC
This framework serves as a proof-of-concept for the future development of CRC-specific models. By swapping the primary data loaders from `TCGA-BRCA` to `TCGA-COAD/READ`, researchers can apply the same systematic modeling to predict CIK recognition in colorectal cancer models following CX-5461 induced stress.
