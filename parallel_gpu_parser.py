#!/usr/bin/env python3
"""
Parallel Multi-GPU PDF Parser
Process multiple PDFs simultaneously across available GPUs
"""

import os
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

def process_single_pdf(pdf_path, gpu_id=0):
    """Process a single PDF on specified GPU"""
    try:
        # Set GPU device
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        
        # Setup offline environment
        artifacts_path = os.path.expanduser("~/.cache/docling/models")
        os.environ["DOCLING_ARTIFACTS_PATH"] = artifacts_path
        
        # Create converter
        pipeline_options = PdfPipelineOptions(
            artifacts_path=artifacts_path,
            enable_remote_services=False,
            do_table_structure=True,
            do_ocr=True,
            do_chunking=True,
        )
        
        ocr_options = EasyOcrOptions(use_gpu=True, lang=['en'])
        pipeline_options.ocr_options = ocr_options
        
        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )
        
        # Process document
        print(f"🚀 GPU {gpu_id}: Processing {Path(pdf_path).name}")
        start_time = time.time()
        
        result = converter.convert(pdf_path)
        document = result.document
        
        # Extract content
        content = {
            "file": Path(pdf_path).name,
            "gpu_id": gpu_id,
            "pages": len(document.pages) if hasattr(document, 'pages') else 0,
            "text_length": len(document.export_to_text()),
            "tables": len(document.tables) if hasattr(document, 'tables') else 0,
            "pictures": len(document.pictures) if hasattr(document, 'pictures') else 0,
            "processing_time": time.time() - start_time
        }
        
        # Save results
        output_dir = f"output_gpu_{gpu_id}"
        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(pdf_path).stem
        
        with open(f"{output_dir}/{base_name}_text.txt", 'w', encoding='utf-8') as f:
            f.write(document.export_to_text())
        
        with open(f"{output_dir}/{base_name}_content.md", 'w', encoding='utf-8') as f:
            f.write(document.export_to_markdown())
        
        print(f"✅ GPU {gpu_id}: Completed {Path(pdf_path).name} in {content['processing_time']:.1f}s")
        return content
        
    except Exception as e:
        print(f"❌ GPU {gpu_id}: Error processing {Path(pdf_path).name}: {e}")
        return None

def get_available_gpus():
    """Get number of available GPUs"""
    try:
        import torch
        return torch.cuda.device_count()
    except:
        return 1

def main():
    """Main function for parallel processing"""
    # Get PDF files
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in current directory")
        sys.exit(1)
    
    # Get available GPUs
    num_gpus = get_available_gpus()
    print(f"🔍 Found {num_gpus} GPU(s)")
    
    print("=" * 60)
    print("🚀 PARALLEL MULTI-GPU PDF PARSER")
    print("=" * 60)
    print(f"📄 Files: {len(pdf_files)}")
    print(f"⚡ GPUs: {num_gpus}")
    print("🔒 Mode: COMPLETELY OFFLINE")
    print("=" * 60)
    
    # Process PDFs in parallel
    start_time = time.time()
    results = []
    
    with ProcessPoolExecutor(max_workers=num_gpus) as executor:
        # Submit tasks
        futures = []
        for i, pdf_file in enumerate(pdf_files):
            gpu_id = i % num_gpus  # Distribute across GPUs
            future = executor.submit(process_single_pdf, pdf_file, gpu_id)
            futures.append(future)
        
        # Collect results
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("📊 PROCESSING SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"✅ {result['file']}: {result['pages']} pages, {result['text_length']} chars, {result['tables']} tables, {result['pictures']} images ({result['processing_time']:.1f}s)")
    
    print(f"\n⚡ Total time: {total_time:.1f}s")
    print(f"📈 Average per file: {total_time/len(results):.1f}s")
    print(f"🚀 Speedup: {sum(r['processing_time'] for r in results)/total_time:.1f}x")

if __name__ == "__main__":
    main()
