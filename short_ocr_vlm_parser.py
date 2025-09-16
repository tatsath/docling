#!/usr/bin/env python3
"""
Short OCR & VLM Parser with Multiprocessing
Processes PDF with both OCR and VLM, saves to separate folders
"""

import os, sys, time, multiprocessing as mp
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions, VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

def setup_offline():
    """Setup offline environment"""
    os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

def process_ocr(pdf_path):
    """OCR processing function"""
    print("🔍 Starting OCR processing...")
    start_time = time.time()
    
    # OCR Pipeline
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
    
    # Process
    result = converter.convert(pdf_path)
    doc = result.document
    
    # Extract content
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Save to OCR folder
    os.makedirs("output/ocr", exist_ok=True)
    base_name = Path(pdf_path).stem
    
    with open(f"output/ocr/{base_name}_ocr.txt", "w") as f: f.write(text)
    with open(f"output/ocr/{base_name}_ocr.md", "w") as f: f.write(markdown)
    
    # Statistics
    stats = {
        "method": "OCR",
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "time": time.time() - start_time
    }
    
    print(f"✅ OCR Complete: {stats['time']:.1f}s, {stats['text_chars']} chars, {stats['tables']} tables, {stats['pictures']} images")
    return stats

def process_vlm(pdf_path):
    """VLM processing function"""
    print("🧠 Starting VLM processing...")
    start_time = time.time()
    
    # VLM Pipeline
    converter = DocumentConverter({
        InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline)
    })
    
    # Process
    result = converter.convert(source=pdf_path)
    doc = result.document
    
    # Extract content
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Save to VLM folder
    os.makedirs("output/vlm", exist_ok=True)
    base_name = Path(pdf_path).stem
    
    with open(f"output/vlm/{base_name}_vlm.txt", "w") as f: f.write(text)
    with open(f"output/vlm/{base_name}_vlm.md", "w") as f: f.write(markdown)
    
    # Statistics
    stats = {
        "method": "VLM",
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "time": time.time() - start_time
    }
    
    print(f"✅ VLM Complete: {stats['time']:.1f}s, {stats['text_chars']} chars, {stats['tables']} tables, {stats['pictures']} images")
    return stats

def main():
    """Main function with multiprocessing"""
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "companies_house_document.pdf"
    num_processes = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    print("=" * 60)
    print("🚀 SHORT OCR & VLM PARSER WITH MULTIPROCESSING")
    print("=" * 60)
    print(f"📄 File: {pdf_file}")
    print(f"⚡ Processes: {num_processes}")
    print(f"🔒 Mode: COMPLETELY OFFLINE")
    print("=" * 60)
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF not found: {pdf_file}")
        sys.exit(1)
    
    # Setup offline environment
    setup_offline()
    
    # Start processing
    start_time = time.time()
    
    if num_processes > 1:
        print(f"🔄 Running OCR and VLM in parallel with {num_processes} processes...")
        with mp.Pool(processes=num_processes) as pool:
            results = pool.starmap(process_method, [(pdf_file, "ocr"), (pdf_file, "vlm")])
    else:
        print("🔄 Running OCR and VLM sequentially...")
        results = [process_ocr(pdf_file), process_vlm(pdf_file)]
    
    total_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 PROCESSING SUMMARY")
    print("=" * 60)
    
    for stats in results:
        print(f"{stats['method']:>4}: {stats['time']:>6.1f}s | "
              f"Text: {stats['text_chars']:>6} | "
              f"Tables: {stats['tables']:>2} | "
              f"Images: {stats['pictures']:>2} | "
              f"Pages: {stats['pages']:>2}")
    
    print(f"{'TOTAL':>4}: {total_time:>6.1f}s")
    print("=" * 60)
    print("📁 Output folders: output/ocr/ and output/vlm/")
    print("✅ All processing complete!")

def process_method(pdf_path, method):
    """Wrapper for multiprocessing"""
    if method == "ocr":
        return process_ocr(pdf_path)
    else:
        return process_vlm(pdf_path)

if __name__ == "__main__":
    main()
