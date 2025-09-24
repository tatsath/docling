#!/usr/bin/env python3
"""
Use downloaded models with Docling 2.2.1
"""

import os
import sys
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.datamodel.base_models import InputFormat, PdfFormatOption

def run_with_downloaded_models():
    """Run Docling with downloaded models"""
    print("=== DOCLING WITH DOWNLOADED MODELS ===")
    print()
    
    # Set up offline environment
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    
    current_dir = Path.cwd()
    models_dir = current_dir / "downloaded_models"
    
    if not models_dir.exists():
        print("❌ No downloaded models found. Please run simple_model_downloader.py first")
        return False
    
    print(f"📁 Using models from: {models_dir}")
    print()
    
    # Configure pipeline options with downloaded models
    pipeline_options = PdfPipelineOptions(
        artifacts_path=str(models_dir),
        do_table_structure=True,  # Enable with downloaded models
        do_ocr=True,              # Enable with downloaded models
        create_legacy_output=True,
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=True,
            download_enabled=False,  # Use local models only
            model_storage_directory=str(models_dir / "easyocr")
        )
    )
    
    print("✅ Pipeline configured with downloaded models")
    print("   - Table structure detection: Enabled")
    print("   - OCR: Enabled")
    print("   - Layout analysis: Enabled")
    print()
    
    # Create converter
    try:
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        print("✅ DocumentConverter created successfully")
    except Exception as e:
        print(f"❌ Error creating converter: {e}")
        return False
    
    # Find PDF files to process
    pdf_files = []
    for file in current_dir.iterdir():
        if file.suffix.lower() == '.pdf':
            pdf_files.append(file)
    
    if not pdf_files:
        print("⚠️ No PDF files found in current directory")
        return False
    
    # Process the first PDF
    pdf_file = pdf_files[0]
    print(f"📄 Processing: {pdf_file.name}")
    
    try:
        result = converter.convert(str(pdf_file))
        print(f"✅ Conversion successful!")
        print(f"   - Document name: {result.document.name}")
        print(f"   - Number of pages: {len(result.document.pages)}")
        
        # Try to export text
        try:
            text_content = result.document.export_to_text()
            print(f"   - Text length: {len(text_content)} characters")
            
            # Save output
            output_file = current_dir / f"{pdf_file.stem}_with_models_output.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"   - Output saved: {output_file}")
            
        except Exception as e:
            print(f"⚠️ Text export failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def main():
    """Main function"""
    print("Docling 2.2.1 with Downloaded Models")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("test_docling_2.2.1.py").exists():
        print("❌ Please run this script from the docling directory")
        sys.exit(1)
    
    # Run with downloaded models
    if run_with_downloaded_models():
        print()
        print("🚀 Success! Docling is now using downloaded models")
        print("   - Advanced layout analysis enabled")
        print("   - Table structure detection enabled")
        print("   - OCR capabilities enabled")
    else:
        print("❌ Failed to use downloaded models")
        sys.exit(1)

if __name__ == "__main__":
    main()
