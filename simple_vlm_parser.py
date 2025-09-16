#!/usr/bin/env python3
"""
Simple VLM SmolDocling Parser - Direct implementation
"""

import os
from docling.datamodel import vlm_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

# Setup offline mode
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# PDF file to process
pdf_file = "companies_house_document_2.pdf"

print("🧠 VLM SmolDocling Processing...")
print(f"📄 File: {pdf_file}")
print("🔒 Offline mode enabled")

# Method 1: Simple default values using transformers framework
print("\n🔄 Method 1: Default Transformers Framework")
try:
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline,
            ),
        }
    )
    
    doc = converter.convert(source=pdf_file).document
    markdown_output = doc.export_to_markdown()
    
    # Save output
    with open("output/vlm_default_output.md", "w", encoding="utf-8") as f:
        f.write(markdown_output)
    
    print(f"✅ Default method complete: {len(markdown_output)} characters")
    print("💾 Saved: output/vlm_default_output.md")
    
except Exception as e:
    print(f"❌ Default method failed: {e}")

# Method 2: Using MLX accelerator (if available)
print("\n🍎 Method 2: MLX Accelerator")
try:
    pipeline_options = VlmPipelineOptions(
        vlm_options=vlm_model_specs.SMOLDOCLING_MLX,
    )
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline,
                pipeline_options=pipeline_options,
            ),
        }
    )
    
    doc = converter.convert(source=pdf_file).document
    markdown_output = doc.export_to_markdown()
    
    # Save output
    with open("output/vlm_mlx_output.md", "w", encoding="utf-8") as f:
        f.write(markdown_output)
    
    print(f"✅ MLX method complete: {len(markdown_output)} characters")
    print("💾 Saved: output/vlm_mlx_output.md")
    
except Exception as e:
    print(f"❌ MLX method failed: {e}")

print("\n🎉 VLM Processing Complete!")
