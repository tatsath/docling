#!/usr/bin/env python3
"""
Test script to verify offline docling functionality
"""

import os
import sys
from pathlib import Path

def test_offline_setup():
    """Test if the offline setup is working correctly"""
    
    print("Testing Offline Docling Setup")
    print("=" * 40)
    
    # Check if models are downloaded
    artifacts_path = os.path.expanduser("~/.cache/docling/models")
    if not os.path.exists(artifacts_path):
        print("❌ Models not found. Please run: docling-tools models download")
        return False
    
    print(f"✅ Models found at: {artifacts_path}")
    
    # Check if PDF exists
    pdf_file = "companies_house_document.pdf"
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return False
    
    print(f"✅ PDF file found: {pdf_file}")
    
    # Test import
    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
        print("✅ Docling imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test offline converter creation
    try:
        pipeline_options = PdfPipelineOptions(
            artifacts_path=artifacts_path,
            enable_remote_services=False
        )
        
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        print("✅ Offline converter created successfully")
    except Exception as e:
        print(f"❌ Converter creation failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Ready for offline processing.")
    return True

if __name__ == "__main__":
    success = test_offline_setup()
    sys.exit(0 if success else 1)
