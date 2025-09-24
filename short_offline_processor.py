#!/usr/bin/env python3
"""
Short Docling 2.2.1 Offline Processor
Processes PDF documents with downloaded models and outputs markdown
"""

import os
import sys
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions

def process_pdf_offline(pdf_file: str):
    """Process PDF with offline models and generate markdown output"""
    print(f"🔄 Processing: {pdf_file}")
    
    # Set offline environment
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    
    # Use downloaded models
    current_dir = Path.cwd()
    artifacts_path = current_dir / "downloaded_models"
    
    if not artifacts_path.exists():
        print(f"❌ Downloaded models not found: {artifacts_path}")
        return False
    
    os.environ["DOCLING_ARTIFACTS_PATH"] = str(artifacts_path)
    
    # Configure pipeline with downloaded models
    pipeline_options = PdfPipelineOptions(
        artifacts_path=str(artifacts_path),
        do_table_structure=True,
        do_ocr=True,
        create_legacy_output=True,
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=True,
            download_enabled=False,
            model_storage_directory=str(artifacts_path / "easyocr")
        )
    )
    
    # Create converter
    converter = DocumentConverter()
    
    try:
        # Process PDF
        result = converter.convert(pdf_file)
        print(f"✅ Conversion successful!")
        print(f"   - Document: {result.document.name}")
        print(f"   - Pages: {len(result.document.pages)}")
        
        # Generate outputs
        pdf_path = Path(pdf_file)
        
        # Text output
        text_content = result.document.export_to_text()
        text_file = pdf_path.stem + "_offline_text.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"📄 Text saved: {text_file} ({len(text_content)} chars)")
        
        # Markdown output
        markdown_content = result.document.export_to_markdown()
        markdown_file = pdf_path.stem + "_offline_markdown.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"📝 Markdown saved: {markdown_file} ({len(markdown_content)} chars)")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Docling 2.2.1 Short Offline Processor")
    print("=" * 50)
    
    # Process companies_house_document.pdf
    pdf_file = "companies_house_document.pdf"
    
    if not Path(pdf_file).exists():
        print(f"❌ PDF file not found: {pdf_file}")
        sys.exit(1)
    
    if process_pdf_offline(pdf_file):
        print("\n✅ Processing completed successfully!")
        print("📁 Output files generated in current directory")
    else:
        print("\n❌ Processing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
