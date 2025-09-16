#!/usr/bin/env python3
"""Enhanced GPU PDF parser with image extraction and display"""

import os, sys, json, base64
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Setup offline GPU processing
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")

# Create GPU-optimized converter
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

# Process PDF
print("🚀 GPU Processing with Image Extraction...")
result = converter.convert("companies_house_document_2.pdf")
doc = result.document

# Extract content
text = doc.export_to_text()
markdown = doc.export_to_markdown()

# Extract and save images
os.makedirs("output/images", exist_ok=True)
images_info = []

if hasattr(doc, 'pictures') and doc.pictures:
    print(f"📸 Found {len(doc.pictures)} images, extracting...")
    
    for i, picture in enumerate(doc.pictures):
        try:
            # Get image data
            if hasattr(picture, 'image') and picture.image:
                img_data = picture.image
                img_path = f"output/images/image_{i+1}.png"
                
                # Save image
                img_data.save(img_path)
                
                # Get image info
                img_info = {
                    "index": i+1,
                    "path": img_path,
                    "caption": getattr(picture, 'caption', ''),
                    "alt_text": getattr(picture, 'alt_text', ''),
                    "size": img_data.size if hasattr(img_data, 'size') else None
                }
                images_info.append(img_info)
                
                print(f"✅ Saved image {i+1}: {img_path}")
                
        except Exception as e:
            print(f"❌ Error saving image {i+1}: {e}")

# Create enhanced markdown with image references
enhanced_markdown = markdown
if images_info:
    enhanced_markdown += "\n\n## Extracted Images\n\n"
    for img in images_info:
        enhanced_markdown += f"### Image {img['index']}\n\n"
        if img['caption']:
            enhanced_markdown += f"**Caption:** {img['caption']}\n\n"
        enhanced_markdown += f"![Image {img['index']}]({img['path']})\n\n"

# Save all outputs
os.makedirs("output", exist_ok=True)

with open("output/companies_house_document_2_text.txt", "w") as f: 
    f.write(text)

with open("output/companies_house_document_2_content.md", "w") as f: 
    f.write(enhanced_markdown)

with open("output/companies_house_document_2_images.json", "w") as f: 
    json.dump(images_info, f, indent=2)

# Summary
print(f"\n✅ Complete!")
print(f"📄 Text: {len(text)} characters")
print(f"📊 Tables: {len(doc.tables) if hasattr(doc, 'tables') else 0}")
print(f"📸 Images: {len(images_info)} extracted")
print(f"📁 Images saved in: output/images/")
print(f"📝 Enhanced markdown: output/companies_house_document_2_content.md")
