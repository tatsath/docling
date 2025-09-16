#!/usr/bin/env python3
"""Ultra-fast GPU PDF parser - minimal code, maximum speed"""

import os, sys, json
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Setup offline GPU processing
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")

# Create GPU-optimized converter
pipeline = PdfPipelineOptions(
    artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
    enable_remote_services=False,
    do_table_structure=True,
    do_ocr=True,
    do_chunking=True,
)
pipeline.ocr_options = EasyOcrOptions(use_gpu=True, lang=['en'])

converter = DocumentConverter({
    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)
})

# Process PDF
print("🚀 GPU Processing companies_house_document_2.pdf...")
result = converter.convert("companies_house_document_2.pdf")
doc = result.document

# Extract and save
text = doc.export_to_text()
markdown = doc.export_to_markdown()

os.makedirs("output", exist_ok=True)
with open("output/companies_house_document_2_text.txt", "w") as f: f.write(text)
with open("output/companies_house_document_2_content.md", "w") as f: f.write(markdown)

print(f"✅ Done! {len(text)} chars, {len(doc.tables)} tables, {len(doc.pictures)} images")
