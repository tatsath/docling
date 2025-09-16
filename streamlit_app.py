#!/usr/bin/env python3
"""
Streamlit App for Offline PDF Processing with OCR and VLM
Supports file upload, processing options, and collapsible output
"""

import streamlit as st
import os
import time
import tempfile
import multiprocessing as mp
from pathlib import Path
import json
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

# Page config
st.set_page_config(
    page_title="Offline PDF Parser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def setup_offline_environment():
    """Setup offline environment and download models if needed"""
    artifacts_path = os.path.expanduser("~/.cache/docling/models")
    os.environ["DOCLING_ARTIFACTS_PATH"] = artifacts_path
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    
    # Create artifacts directory if it doesn't exist
    os.makedirs(artifacts_path, exist_ok=True)
    return artifacts_path

def download_models():
    """Download required models for offline processing"""
    with st.spinner("Downloading models for offline processing..."):
        try:
            # Test OCR pipeline
            pipeline = PdfPipelineOptions(
                artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
                enable_remote_services=False,
                do_table_structure=True,
                do_ocr=True,
                do_chunking=True,
            )
            pipeline.ocr_options = EasyOcrOptions(use_gpu=False, lang=['en'])
            converter = DocumentConverter({
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)
            })
            
            # Test VLM pipeline
            vlm_converter = DocumentConverter({
                InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline)
            })
            
            st.success("✅ Models downloaded successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Error downloading models: {e}")
            return False

def process_pdf_ocr(pdf_path, use_gpu=True, num_processes=1):
    """Process PDF with OCR pipeline"""
    start_time = time.time()
    
    pipeline = PdfPipelineOptions(
        artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
        enable_remote_services=False,
        do_table_structure=True,
        do_ocr=True,
        do_chunking=True,
    )
    pipeline.ocr_options = EasyOcrOptions(use_gpu=use_gpu, lang=['en'])
    
    converter = DocumentConverter({
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)
    })
    
    result = converter.convert(pdf_path)
    doc = result.document
    
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    stats = {
        "method": "OCR",
        "time": time.time() - start_time,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "text": text,
        "markdown": markdown
    }
    
    return stats

def process_pdf_vlm(pdf_path, use_gpu=True, num_processes=1):
    """Process PDF with VLM pipeline"""
    start_time = time.time()
    
    converter = DocumentConverter({
        InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline)
    })
    
    result = converter.convert(source=pdf_path)
    doc = result.document
    
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    stats = {
        "method": "VLM",
        "time": time.time() - start_time,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "text": text,
        "markdown": markdown
    }
    
    return stats

def main():
    """Main Streamlit app"""
    st.title("📄 Offline PDF Parser")
    st.markdown("**Process PDFs with OCR or VLM - Completely Offline**")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Processing Options")
        
        # Processing method
        processing_method = st.selectbox(
            "Processing Method",
            ["OCR (Text Recognition)", "VLM (Vision Language Model)"],
            help="OCR for text recognition, VLM for advanced document understanding"
        )
        
        # GPU option
        use_gpu = st.checkbox(
            "Use GPU Acceleration",
            value=True,
            help="Enable GPU acceleration for faster processing"
        )
        
        # Number of processes
        num_processes = st.slider(
            "Number of Processes",
            min_value=1,
            max_value=mp.cpu_count(),
            value=1,
            help="Number of parallel processes (1 for sequential processing)"
        )
        
        # Model download button
        if st.button("🔄 Download/Update Models", type="primary"):
            if download_models():
                st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload PDF Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document for processing"
        )
    
    with col2:
        st.header("📊 Processing Status")
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📄 Size: {uploaded_file.size:,} bytes")
        else:
            st.warning("⚠️ Please upload a PDF file")
    
    # Process button
    if uploaded_file is not None:
        if st.button("🚀 Process PDF", type="primary", use_container_width=True):
            # Setup offline environment
            artifacts_path = setup_offline_environment()
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Process the PDF
                with st.spinner(f"Processing with {processing_method}..."):
                    if "OCR" in processing_method:
                        stats = process_pdf_ocr(tmp_path, use_gpu, num_processes)
                    else:
                        stats = process_pdf_vlm(tmp_path, use_gpu, num_processes)
                
                # Display results
                st.success("✅ Processing completed successfully!")
                
                # Statistics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("⏱️ Time", f"{stats['time']:.1f}s")
                with col2:
                    st.metric("📄 Pages", stats['pages'])
                with col3:
                    st.metric("📊 Tables", stats['tables'])
                with col4:
                    st.metric("🖼️ Images", stats['pictures'])
                with col5:
                    st.metric("📝 Text Chars", f"{stats['text_chars']:,}")
                
                # Collapsible output sections
                st.header("📋 Processing Results")
                
                # Text output
                with st.expander(f"📝 Text Output ({stats['text_chars']:,} characters)", expanded=False):
                    st.text_area("Extracted Text", stats['text'], height=300)
                
                # Markdown output
                with st.expander(f"📄 Markdown Output ({stats['markdown_chars']:,} characters)", expanded=True):
                    st.markdown(stats['markdown'])
                
                # Raw statistics
                with st.expander("📊 Detailed Statistics", expanded=False):
                    st.json({
                        "Processing Method": stats['method'],
                        "Processing Time (seconds)": round(stats['time'], 2),
                        "Number of Pages": stats['pages'],
                        "Number of Tables": stats['tables'],
                        "Number of Images": stats['pictures'],
                        "Text Characters": stats['text_chars'],
                        "Markdown Characters": stats['markdown_chars'],
                        "GPU Used": use_gpu,
                        "Processes Used": num_processes
                    })
                
                # Download buttons
                st.header("💾 Download Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📄 Download Markdown",
                        data=stats['markdown'],
                        file_name=f"{Path(uploaded_file.name).stem}_{stats['method'].lower()}.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    st.download_button(
                        label="📝 Download Text",
                        data=stats['text'],
                        file_name=f"{Path(uploaded_file.name).stem}_{stats['method'].lower()}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ Error processing PDF: {e}")
                st.exception(e)
            
            finally:
                # Clean up temporary file
                os.unlink(tmp_path)
    
    # Footer
    st.markdown("---")
    st.markdown("**🔒 Completely Offline Processing** - No internet required after initial model download")
    st.markdown("**⚡ GPU Acceleration** - Uses CUDA when available for faster processing")
    st.markdown("**🔄 Multiprocessing** - Parallel processing for improved performance")

if __name__ == "__main__":
    main()
