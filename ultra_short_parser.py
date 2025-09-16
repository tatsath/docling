#!/usr/bin/env python3
"""Ultra-short OCR & VLM parser with multiprocessing"""

import os, sys, time, multiprocessing as mp
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

# Setup
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

def process_pdf(method, pdf_path):
    """Process PDF with OCR or VLM"""
    print(f"{'🔍 OCR' if method == 'ocr' else '🧠 VLM'} processing...")
    start = time.time()
    
    if method == "ocr":
        # OCR Pipeline
        pipeline = PdfPipelineOptions(
            artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
            enable_remote_services=False, do_table_structure=True, do_ocr=True, do_chunking=True
        )
        pipeline.ocr_options = EasyOcrOptions(use_gpu=True, lang=['en'])
        converter = DocumentConverter({InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)})
        result = converter.convert(pdf_path)
    else:
        # VLM Pipeline
        converter = DocumentConverter({InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline)})
        result = converter.convert(source=pdf_path)
    
    doc = result.document
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Save files
    os.makedirs(f"output/{method}", exist_ok=True)
    base = Path(pdf_path).stem
    with open(f"output/{method}/{base}_{method}.txt", "w") as f: f.write(text)
    with open(f"output/{method}/{base}_{method}.md", "w") as f: f.write(markdown)
    
    # Stats
    stats = {
        "method": method.upper(),
        "time": time.time() - start,
        "text": len(text),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "images": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0
    }
    
    print(f"✅ {stats['method']}: {stats['time']:.1f}s, {stats['text']} chars, {stats['tables']} tables, {stats['images']} images")
    return stats

def main():
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "companies_house_document.pdf"
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    print("🚀 ULTRA-SHORT OCR & VLM PARSER")
    print(f"📄 File: {pdf_file} | ⚡ Processes: {processes}")
    print("=" * 50)
    
    start_time = time.time()
    
    if processes > 1:
        with mp.Pool(processes=processes) as pool:
            results = pool.starmap(process_pdf, [("ocr", pdf_file), ("vlm", pdf_file)])
    else:
        results = [process_pdf("ocr", pdf_file), process_pdf("vlm", pdf_file)]
    
    print("\n📊 SUMMARY:")
    for r in results:
        print(f"{r['method']:>4}: {r['time']:>5.1f}s | Text: {r['text']:>6} | Tables: {r['tables']:>2} | Images: {r['images']:>2}")
    print(f"TOTAL: {time.time() - start_time:.1f}s")
    print("📁 Output: output/ocr/ and output/vlm/")

if __name__ == "__main__":
    main()
