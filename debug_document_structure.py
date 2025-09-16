#!/usr/bin/env python3
"""
Debug script to understand the document structure
"""

import os
import sys
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

def debug_document_structure():
    """Debug the document structure to understand how to extract content"""
    
    pdf_file = "companies_house_document.pdf"
    artifacts_path = os.path.expanduser("~/.cache/docling/models")
    
    # Setup offline environment
    os.environ["DOCLING_ARTIFACTS_PATH"] = artifacts_path
    
    # Create converter
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        enable_remote_services=False,
        do_table_structure=True,
        do_ocr=True,
        do_chunking=True,
    )
    
    ocr_options = EasyOcrOptions(
        use_gpu=True,
        lang=['en'],
    )
    pipeline_options.ocr_options = ocr_options
    
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    print("Converting PDF...")
    result = doc_converter.convert(pdf_file)
    document = result.document
    
    print(f"Document type: {type(document)}")
    print(f"Document attributes: {dir(document)}")
    
    # Check if document has pages
    if hasattr(document, 'pages'):
        print(f"Number of pages: {len(document.pages)}")
        print(f"Page keys: {list(document.pages.keys())}")
        
        # Debug first page
        if document.pages:
            first_page_key = list(document.pages.keys())[0]
            first_page = document.pages[first_page_key]
            print(f"First page type: {type(first_page)}")
            print(f"First page attributes: {dir(first_page)}")
            
            # Check for elements
            if hasattr(first_page, 'elements'):
                print(f"Number of elements on first page: {len(first_page.elements)}")
                
                for i, element in enumerate(first_page.elements[:5]):  # Show first 5 elements
                    print(f"Element {i}: {type(element)}")
                    print(f"  Attributes: {[attr for attr in dir(element) if not attr.startswith('_')]}")
                    
                    if hasattr(element, 'text'):
                        print(f"  Text: '{element.text[:100]}...'")
                    if hasattr(element, 'label'):
                        print(f"  Label: {element.label}")
                    print()
            else:
                print("No elements attribute found on page")
                
            # Check for other content attributes
            for attr in ['text', 'content', 'body', 'main_content']:
                if hasattr(first_page, attr):
                    content = getattr(first_page, attr)
                    print(f"Page has {attr}: {type(content)}")
                    if hasattr(content, '__len__'):
                        print(f"  Length: {len(content)}")
                    if isinstance(content, str) and content.strip():
                        print(f"  Content preview: '{content[:100]}...'")
    else:
        print("Document has no pages attribute")
        
    # Check document-level content
    print("\nDocument-level content:")
    for attr in ['text', 'content', 'body', 'main_content', 'elements']:
        if hasattr(document, attr):
            content = getattr(document, attr)
            print(f"Document has {attr}: {type(content)}")
            if hasattr(content, '__len__'):
                print(f"  Length: {len(content)}")
            if isinstance(content, str) and content.strip():
                print(f"  Content preview: '{content[:200]}...'")

if __name__ == "__main__":
    debug_document_structure()
