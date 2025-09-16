#!/usr/bin/env python3
"""
Final Optimized Offline PDF Parser using Docling
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

def extract_text_from_item(item, level=0):
    """Recursively extract text from document items"""
    text_parts = []
    indent = "  " * level
    
    # Get the item type
    item_type = item.__class__.__name__
    
    # Extract text if available
    if hasattr(item, 'text') and item.text:
        text_parts.append(f"{indent}[{item_type}] {item.text}")
    
    # Handle different item types
    if item_type == 'TableItem':
        # Extract table data
        if hasattr(item, 'rows'):
            text_parts.append(f"{indent}[TABLE]")
            for row in item.rows:
                if hasattr(row, 'cells'):
                    row_text = []
                    for cell in row.cells:
                        if hasattr(cell, 'text') and cell.text:
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_parts.append(f"{indent}  | {' | '.join(row_text)} |")
    
    elif item_type == 'PictureItem':
        # Handle pictures
        caption = getattr(item, 'caption', '') or ''
        text_parts.append(f"{indent}[PICTURE] {caption}")
    
    elif item_type == 'HeadingItem':
        # Handle headings
        level_num = getattr(item, 'level', 1)
        heading_text = getattr(item, 'text', '') or ''
        text_parts.append(f"{indent}{'#' * level_num} {heading_text}")
    
    elif item_type == 'ListItem':
        # Handle list items
        text = getattr(item, 'text', '') or ''
        text_parts.append(f"{indent}- {text}")
    
    # Recursively process children
    if hasattr(item, 'children'):
        for child in item.children:
            child_text = extract_text_from_item(child, level + 1)
            text_parts.extend(child_text)
    
    return text_parts

def extract_document_content(document: DoclingDocument) -> dict:
    """Extract comprehensive content from the Docling document"""
    
    content = {
        "metadata": {
            "title": getattr(document, 'name', 'Unknown'),
            "page_count": len(document.pages) if hasattr(document, 'pages') else 0,
            "processing_info": "Processed offline with Docling"
        },
        "pages": [],
        "tables": [],
        "figures": [],
        "text_content": "",
        "structure": [],
        "full_text": ""
    }
    
    # Extract content from document body
    if hasattr(document, 'body') and document.body:
        print("Extracting content from document body...")
        body_text = extract_text_from_item(document.body)
        content["full_text"] = "\n".join(body_text)
        content["text_content"] = content["full_text"]
    
    # Extract page-by-page content
    if hasattr(document, 'pages') and document.pages:
        print(f"Processing {len(document.pages)} pages...")
        for page_num in sorted(document.pages.keys()):
            page = document.pages[page_num]
            page_content = {
                "page_number": page_num,
                "text": "",
                "elements": [],
                "tables": [],
                "figures": []
            }
            
            # Extract page-level content
            if hasattr(page, 'image') and page.image:
                page_content["has_image"] = True
            
            content["pages"].append(page_content)
    
    # Extract tables from document
    if hasattr(document, 'tables') and document.tables:
        print(f"Found {len(document.tables)} tables")
        for i, table in enumerate(document.tables):
            table_data = extract_table_data(table)
            content["tables"].append({
                "table_number": i + 1,
                "data": table_data
            })
    
    # Extract pictures from document
    if hasattr(document, 'pictures') and document.pictures:
        print(f"Found {len(document.pictures)} pictures")
        for i, picture in enumerate(document.pictures):
            picture_data = {
                "picture_number": i + 1,
                "caption": getattr(picture, 'caption', ''),
                "alt_text": getattr(picture, 'alt_text', '')
            }
            content["figures"].append(picture_data)
    
    # Extract text items
    if hasattr(document, 'texts') and document.texts:
        print(f"Found {len(document.texts)} text items")
        for text_item in document.texts:
            if hasattr(text_item, 'text') and text_item.text:
                content["text_content"] += text_item.text + "\n"
    
    # Use the built-in export methods for better text extraction
    try:
        print("Using built-in text export...")
        exported_text = document.export_to_text()
        if exported_text and exported_text.strip():
            content["full_text"] = exported_text
            content["text_content"] = exported_text
            print(f"✓ Exported {len(exported_text)} characters using built-in method")
    except Exception as e:
        print(f"Built-in text export failed: {e}")
    
    # Try markdown export as well
    try:
        print("Using built-in markdown export...")
        exported_markdown = document.export_to_markdown()
        if exported_markdown and exported_markdown.strip():
            content["markdown_content"] = exported_markdown
            print(f"✓ Exported {len(exported_markdown)} characters as markdown")
    except Exception as e:
        print(f"Built-in markdown export failed: {e}")
    
    return content

def extract_table_data(table_item) -> dict:
    """Extract structured data from table items"""
    table_data = {
        "rows": [],
        "headers": [],
        "caption": getattr(table_item, 'caption', '')
    }
    
    if hasattr(table_item, 'rows'):
        for row in table_item.rows:
            row_data = []
            if hasattr(row, 'cells'):
                for cell in row.cells:
                    cell_text = getattr(cell, 'text', '') if hasattr(cell, 'text') else ''
                    row_data.append(cell_text.strip())
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
        
        # Use markdown content if available, otherwise use full text
        if 'markdown_content' in content and content['markdown_content']:
            f.write(content['markdown_content'])
        else:
            # Write main text content
            f.write("## Document Content\n\n")
            f.write(content['full_text'])
            
            # Write tables
            if content['tables']:
                f.write("\n\n## Tables\n\n")
                for table in content['tables']:
                    f.write(f"### Table {table['table_number']}\n\n")
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
                for figure in content['figures']:
                    f.write(f"### Figure {figure['picture_number']}\n\n")
                    if figure['caption']:
                        f.write(f"*{figure['caption']}*\n\n")
    
    print(f"✓ Markdown output saved: {markdown_path}")
    
    # Save structured text
    text_path = os.path.join(output_dir, f"{base_name}_text.txt")
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content['full_text'])
    print(f"✓ Plain text output saved: {text_path}")

def main():
    """Main function to process the PDF offline"""
    
    # Configuration
    pdf_file = "companies_house_document.pdf"
    output_directory = "output"
    
    print("=" * 60)
    print("FINAL OPTIMIZED OFFLINE PDF PARSER USING DOCLING")
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
        print(f"Text length: {len(content['full_text'])} characters")
        print(f"Output files saved in: {output_directory}/")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
