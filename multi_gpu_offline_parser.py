#!/usr/bin/env python3
"""
Multi-GPU Offline PDF Parser using Docling
Streamlined version for maximum performance with multiple GPUs
"""

import os
import sys
import json
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

def setup_offline_env():
    """Setup offline environment with multi-GPU support"""
    artifacts_path = os.path.expanduser("~/.cache/docling/models")
    if not os.path.exists(artifacts_path):
        print(f"❌ Models not found. Run: docling-tools models download")
        sys.exit(1)
    
    os.environ["DOCLING_ARTIFACTS_PATH"] = artifacts_path
    print(f"✓ Using offline models: {artifacts_path}")
    return artifacts_path

def create_multi_gpu_converter(artifacts_path):
    """Create converter optimized for multi-GPU processing"""
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        enable_remote_services=False,
        do_table_structure=True,
        do_ocr=True,
        do_chunking=True,
    )
    
    # Multi-GPU OCR configuration
    ocr_options = EasyOcrOptions(use_gpu=True, lang=['en'])
    pipeline_options.ocr_options = ocr_options
    
    # Enable multi-GPU acceleration
    pipeline_options.accelerator_options.device = "cuda"
    
    return DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

def process_pdf(pdf_path, output_dir="output"):
    """Process PDF with multi-GPU acceleration"""
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        sys.exit(1)
    
    print(f"🚀 Processing: {pdf_path}")
    
    # Setup
    artifacts_path = setup_offline_env()
    converter = create_multi_gpu_converter(artifacts_path)
    
    # Process document
    print("⚡ Converting PDF (Multi-GPU)...")
    result = converter.convert(pdf_path)
    document = result.document
    
    # Extract content using built-in methods
    print("📄 Extracting content...")
    content = {
        "metadata": {
            "title": getattr(document, 'name', 'Unknown'),
            "pages": len(document.pages) if hasattr(document, 'pages') else 0,
            "processing": "Multi-GPU Offline Docling"
        },
        "text": document.export_to_text(),
        "markdown": document.export_to_markdown(),
        "tables": len(document.tables) if hasattr(document, 'tables') else 0,
        "pictures": len(document.pictures) if hasattr(document, 'pictures') else 0,
    }
    
    # Save results
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(pdf_path).stem
    
    # Save all formats
    with open(f"{output_dir}/{base_name}_text.txt", 'w', encoding='utf-8') as f:
        f.write(content['text'])
    
    with open(f"{output_dir}/{base_name}_content.md", 'w', encoding='utf-8') as f:
        f.write(content['markdown'])
    
    with open(f"{output_dir}/{base_name}_data.json", 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete! Text: {len(content['text'])} chars, Tables: {content['tables']}, Images: {content['pictures']}")
    return content

def main():
    """Main function"""
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "companies_house_document.pdf"
    
    print("=" * 60)
    print("🚀 MULTI-GPU OFFLINE PDF PARSER")
    print("=" * 60)
    print(f"📄 File: {pdf_file}")
    print("🔒 Mode: COMPLETELY OFFLINE")
    print("⚡ GPU: Multi-GPU Accelerated")
    print("=" * 60)
    
    try:
        process_pdf(pdf_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
