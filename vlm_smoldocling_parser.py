#!/usr/bin/env python3
"""
VLM SmolDocling Offline PDF Parser
Uses Vision Language Models for enhanced document understanding
"""

import os
import sys
from pathlib import Path
from docling.datamodel import vlm_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

def setup_vlm_offline():
    """Setup VLM offline environment"""
    # Set offline mode
    os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
    
    # Disable remote services
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    
    print("🔒 VLM Offline mode enabled")
    print("📁 Using local models from: ~/.cache/docling/models")

def create_vlm_converter(use_mlx=False):
    """Create VLM converter with SmolDocling model"""
    
    if use_mlx:
        print("🍎 Using macOS MLX accelerator")
        pipeline_options = VlmPipelineOptions(
            vlm_options=vlm_model_specs.SMOLDOCLING_MLX,
        )
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=VlmPipeline,
                    pipeline_options=pipeline_options,
                ),
            }
        )
    else:
        print("🔄 Using default transformers framework")
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=VlmPipeline,
                ),
            }
        )
    
    return converter

def process_pdf_with_vlm(pdf_path, use_mlx=False, output_dir="output"):
    """Process PDF using VLM SmolDocling"""
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        sys.exit(1)
    
    print(f"🚀 VLM Processing: {pdf_path}")
    
    # Setup offline environment
    setup_vlm_offline()
    
    # Create VLM converter
    converter = create_vlm_converter(use_mlx)
    
    # Process document
    print("⚡ Converting with VLM...")
    try:
        result = converter.convert(source=pdf_path)
        doc = result.document
        
        # Extract content
        print("📄 Extracting content...")
        markdown_content = doc.export_to_markdown()
        text_content = doc.export_to_text()
        
        # Save results
        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(pdf_path).stem
        
        # Save markdown
        md_path = f"{output_dir}/{base_name}_vlm.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save text
        txt_path = f"{output_dir}/{base_name}_vlm.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        # Get document stats
        stats = {
            "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
            "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
            "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
            "text_length": len(text_content),
            "markdown_length": len(markdown_content)
        }
        
        print(f"✅ VLM Processing Complete!")
        print(f"📄 Pages: {stats['pages']}")
        print(f"📊 Tables: {stats['tables']}")
        print(f"📸 Pictures: {stats['pictures']}")
        print(f"📝 Text: {stats['text_length']} characters")
        print(f"📝 Markdown: {stats['markdown_length']} characters")
        print(f"💾 Saved: {md_path}, {txt_path}")
        
        return doc, stats
        
    except Exception as e:
        print(f"❌ VLM Processing Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VLM SmolDocling Offline PDF Parser')
    parser.add_argument('pdf_file', nargs='?', default='companies_house_document_2.pdf', 
                       help='PDF file to process')
    parser.add_argument('--mlx', action='store_true', 
                       help='Use macOS MLX accelerator (requires MLX)')
    parser.add_argument('--output', default='output', 
                       help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 VLM SMOLDOCLING OFFLINE PDF PARSER")
    print("=" * 60)
    print(f"📄 File: {args.pdf_file}")
    print(f"🔒 Mode: COMPLETELY OFFLINE")
    print(f"🧠 VLM: SmolDocling Vision Language Model")
    print(f"🍎 MLX: {'Enabled' if args.mlx else 'Disabled'}")
    print("=" * 60)
    
    try:
        doc, stats = process_pdf_with_vlm(args.pdf_file, args.mlx, args.output)
        
        # Show preview of markdown content
        print("\n📖 Markdown Preview (first 500 chars):")
        print("-" * 40)
        markdown_content = doc.export_to_markdown()
        print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)
        print("-" * 40)
        
    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
