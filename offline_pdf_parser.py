#!/usr/bin/env python3
"""
Offline PDF Parser using Docling
This script processes PDF documents completely offline using pre-downloaded models.
No internet connection is required during execution.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import json

# Docling imports
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.document import DoclingDocument

def setup_offline_environment():
    """Setup the environment for offline processing"""
    # Set the artifacts path to the downloaded models
    artifacts_path = os.path.expanduser("~/.cache/docling/models")
    
    if not os.path.exists(artifacts_path):
        print(f"Error: Models not found at {artifacts_path}")
        print("Please run: docling-tools models download")
        sys.exit(1)
    
    # Set environment variable for offline mode
    os.environ["DOCLING_ARTIFACTS_PATH"] = artifacts_path
    
    print(f"✓ Using offline models from: {artifacts_path}")
    return artifacts_path

def create_offline_converter(artifacts_path: str) -> DocumentConverter:
    """Create a DocumentConverter configured for offline processing"""
    
    # Configure pipeline options for offline processing
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        enable_remote_services=False,  # Explicitly disable remote services
        do_table_structure=True,       # Enable table structure recognition
        do_ocr=True,                   # Enable OCR
        do_chunking=True,              # Enable document chunking
    )
    
    # Configure table structure options for better table extraction
    pipeline_options.table_structure_options.do_cell_matching = True
    
    # Configure OCR options
    ocr_options = EasyOcrOptions(
        use_gpu=True,  # Use GPU if available
        lang=['en'],  # English language
    )
    pipeline_options.ocr_options = ocr_options
    
    # Create the document converter with offline configuration
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    print("✓ DocumentConverter configured for offline processing")
    return doc_converter

def process_pdf_offline(pdf_path: str, output_dir: str = "output") -> DoclingDocument:
    """Process a PDF document completely offline"""
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Processing PDF: {pdf_path}")
    
    # Setup offline environment
    artifacts_path = setup_offline_environment()
    
    # Create offline converter
    doc_converter = create_offline_converter(artifacts_path)
    
    # Process the document
    print("Converting PDF to Docling document...")
    try:
        result = doc_converter.convert(pdf_path)
        print("✓ PDF conversion completed successfully")
        return result.document
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
        sys.exit(1)

def extract_document_content(document: DoclingDocument) -> dict:
    """Extract comprehensive content from the Docling document"""
    
    content = {
        "metadata": {
            "title": document.name if hasattr(document, 'name') else "Unknown",
            "page_count": len(document.pages) if hasattr(document, 'pages') else 0,
            "processing_info": "Processed offline with Docling"
        },
        "pages": [],
        "tables": [],
        "figures": [],
        "text_content": "",
        "structure": []
    }
    
    # Extract page content
    for i, page in enumerate(document.pages):
        page_content = {
            "page_number": i + 1,
            "text": "",
            "elements": [],
            "tables": [],
            "figures": []
        }
        
        # Extract text and elements from each page
        if hasattr(page, 'elements'):
            for element in page.elements:
                element_info = {
                    "type": element.__class__.__name__,
                    "text": getattr(element, 'text', ''),
                    "bbox": getattr(element, 'bbox', None),
                    "label": getattr(element, 'label', None)
                }
                page_content["elements"].append(element_info)
                
                # Collect text content
                if hasattr(element, 'text') and element.text:
                    page_content["text"] += element.text + "\n"
                
                # Collect tables
                if element.__class__.__name__ == 'Table':
                    table_data = extract_table_data(element)
                    page_content["tables"].append(table_data)
                    content["tables"].append({
                        "page": i + 1,
                        "data": table_data
                    })
                
                # Collect figures
                if element.__class__.__name__ in ['Figure', 'Picture']:
                    figure_data = {
                        "page": i + 1,
                        "caption": getattr(element, 'caption', ''),
                        "bbox": getattr(element, 'bbox', None)
                    }
                    page_content["figures"].append(figure_data)
                    content["figures"].append(figure_data)
        
        content["pages"].append(page_content)
        content["text_content"] += page_content["text"]
    
    return content

def extract_table_data(table_element) -> dict:
    """Extract structured data from table elements"""
    table_data = {
        "rows": [],
        "headers": [],
        "caption": getattr(table_element, 'caption', '')
    }
    
    if hasattr(table_element, 'rows'):
        for row in table_element.rows:
            row_data = []
            if hasattr(row, 'cells'):
                for cell in row.cells:
                    cell_text = getattr(cell, 'text', '') if hasattr(cell, 'text') else ''
                    row_data.append(cell_text)
            table_data["rows"].append(row_data)
    
    return table_data

def save_results(content: dict, output_dir: str, pdf_name: str):
    """Save the extracted content in multiple formats"""
    
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(pdf_name).stem
    
    # Save as JSON
    json_path = os.path.join(output_dir, f"{base_name}_content.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON output saved: {json_path}")
    
    # Save as Markdown
    markdown_path = os.path.join(output_dir, f"{base_name}_content.md")
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(f"# {content['metadata']['title']}\n\n")
        f.write(f"**Pages:** {content['metadata']['page_count']}\n")
        f.write(f"**Processing:** {content['metadata']['processing_info']}\n\n")
        
        # Write main text content
        f.write("## Document Content\n\n")
        f.write(content['text_content'])
        
        # Write tables
        if content['tables']:
            f.write("\n\n## Tables\n\n")
            for i, table in enumerate(content['tables']):
                f.write(f"### Table {i+1} (Page {table['page']})\n\n")
                if table['data']['rows']:
                    # Create markdown table
                    for j, row in enumerate(table['data']['rows']):
                        if j == 0:  # Header row
                            f.write("| " + " | ".join(row) + " |\n")
                            f.write("| " + " | ".join(["---"] * len(row)) + " |\n")
                        else:
                            f.write("| " + " | ".join(row) + " |\n")
                    f.write("\n")
        
        # Write figures
        if content['figures']:
            f.write("\n\n## Figures\n\n")
            for i, figure in enumerate(content['figures']):
                f.write(f"### Figure {i+1} (Page {figure['page']})\n\n")
                if figure['caption']:
                    f.write(f"*{figure['caption']}*\n\n")
    
    print(f"✓ Markdown output saved: {markdown_path}")
    
    # Save structured text
    text_path = os.path.join(output_dir, f"{base_name}_text.txt")
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content['text_content'])
    print(f"✓ Plain text output saved: {text_path}")

def main():
    """Main function to process the PDF offline"""
    
    # Configuration
    pdf_file = "companies_house_document.pdf"
    output_directory = "output"
    
    print("=" * 60)
    print("OFFLINE PDF PARSER USING DOCLING")
    print("=" * 60)
    print(f"PDF File: {pdf_file}")
    print(f"Output Directory: {output_directory}")
    print("Mode: COMPLETELY OFFLINE (No Internet Required)")
    print("=" * 60)
    
    # Check if PDF exists
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found in current directory")
        print("Available files:")
        for file in os.listdir('.'):
            if file.endswith('.pdf'):
                print(f"  - {file}")
        sys.exit(1)
    
    try:
        # Process the PDF offline
        document = process_pdf_offline(pdf_file, output_directory)
        
        # Extract content
        print("Extracting document content...")
        content = extract_document_content(document)
        
        # Save results
        print("Saving results...")
        save_results(content, output_directory, pdf_file)
        
        # Print summary
        print("\n" + "=" * 60)
        print("PROCESSING COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Pages processed: {content['metadata']['page_count']}")
        print(f"Tables found: {len(content['tables'])}")
        print(f"Figures found: {len(content['figures'])}")
        print(f"Text length: {len(content['text_content'])} characters")
        print(f"Output files saved in: {output_directory}/")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
