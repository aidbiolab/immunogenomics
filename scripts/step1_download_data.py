import requests
import json
import pandas as pd
import os

"""
Step 1: Gather and Download Public Data (TCGA-BRCA)

This script demonstrates how to interact with the GDC API to retrieve 
metadata and files for the TCGA-BRCA project, focusing on HRD-high cohorts.
"""

GDC_API_URL = "https://api.gdc.cancer.gov/"

def fetch_project_counts(project_id="TCGA-BRCA"):
    """Fetch file counts for a specific project."""
    fields = [
        "summary.data_categories.data_category",
        "summary.data_categories.file_count"
    ]
    params = {
        "fields": ",".join(fields),
        "filters": json.dumps({
            "op": "and",
            "content": [
                {"op": "=", "content": {"field": "project_id", "value": project_id}}
            ]
        })
    }
    
    response = requests.get(f"{GDC_API_URL}projects", params=params)
    data = response.json()
    return data['data']['hits'][0]['summary']['data_categories']

def create_manifest_query(project_id="TCGA-BRCA", data_type="Gene Expression Quantification"):
    """
    Generate a query to fetch files for specific clinical backgrounds (e.g., HRD/BRCA status).
    In a real scenario, this would be combined with clinical donor information.
    """
    filters = {
        "op": "and",
        "content": [
            {"op": "=", "content": {"field": "cases.project.project_id", "value": project_id}},
            {"op": "=", "content": {"field": "files.data_type", "value": data_type}},
            {"op": "=", "content": {"field": "files.access", "value": "open"}}
        ]
    }
    
    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name,cases.submitter_id,cases.samples.sample_type",
        "format": "TSV",
        "size": "100"
    }
    
    response = requests.get(f"{GDC_API_URL}files", params=params)
    return response.text

if __name__ == "__main__":
    print(f"--- Step 1: Initializing Data Gathering for TCGA-BRCA ---")
    
    # 1. Check availability
    try:
        counts = fetch_project_counts()
        print(f"Data categories available in TCGA-BRCA:")
        for cat in counts:
            print(f"- {cat['data_category']}: {cat['file_count']} files")
            
        # 2. Mocking the download manifest for HRD-high subsets
        # Note: Actual HRD status is typically derived from Somatic Mutations and Clinical datasets.
        manifest = create_manifest_query()
        os.makedirs("data/raw", exist_ok=True)
        with open("data/raw/brca_manifest.tsv", "w") as f:
            f.write(manifest)
            
        print("\n[SUCCESS] Manifest created at data/raw/brca_manifest.tsv")
        print("Run 'gdc-client download -m brca_manifest.tsv' to fetch raw data.")
        
    except Exception as e:
        print(f"[ERROR] Could not connect to GDC API: {e}")
