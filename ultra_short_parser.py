#!/usr/bin/env python3
"""Minimal OCR parser with GPU and multiprocessing"""

import os, sys, time, multiprocessing as mp
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Setup offline mode
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

def process_pdf(pdf_path):
    """Process PDF with OCR on GPU"""
    print(f"🔍 OCR processing {Path(pdf_path).name}...")
    start = time.time()
    
    # OCR Pipeline with GPU
    pipeline = PdfPipelineOptions(
        artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
        enable_remote_services=False, do_table_structure=True, do_ocr=True, do_chunking=True
    )
    pipeline.ocr_options = EasyOcrOptions(use_gpu=True, lang=['en'])
    converter = DocumentConverter({InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)})
    result = converter.convert(pdf_path)
    
    doc = result.document
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Save files
    os.makedirs("output", exist_ok=True)
    base = Path(pdf_path).stem
    with open(f"output/{base}_ocr.txt", "w") as f: f.write(text)
    with open(f"output/{base}_ocr.md", "w") as f: f.write(markdown)
    
    # Stats
    stats = {
        "time": time.time() - start,
        "text": len(text),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "images": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0
    }
    
    print(f"✅ OCR: {stats['time']:.1f}s, {stats['text']} chars, {stats['tables']} tables, {stats['images']} images")
    return stats

def main():
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "companies_house_document.pdf"
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    print("🚀 MINIMAL OCR PARSER (GPU + MULTIPROCESSING)")
    print(f"📄 File: {pdf_file} | ⚡ Processes: {processes}")
    print("=" * 50)
    
    start_time = time.time()
    print(f"⏰ START TIME: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    
    if processes > 1:
        with mp.Pool(processes=processes) as pool:
            results = pool.map(process_pdf, [pdf_file] * processes)
    else:
        results = [process_pdf(pdf_file)]
    
    end_time = time.time()
    print(f"⏰ END TIME: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
    print(f"⏱️  TOTAL TIME: {end_time - start_time:.1f}s")
    print("📁 Output: output/")
    print(f"📊 Processed {len(results)} times")

if __name__ == "__main__":
    main()
