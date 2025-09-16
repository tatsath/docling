#!/usr/bin/env python3
"""Debug image extraction to understand the structure"""

import os
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Setup
os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")

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

print("🔍 Debugging image extraction...")
result = converter.convert("companies_house_document_2.pdf")
doc = result.document

print(f"Document type: {type(doc)}")
print(f"Has pictures attribute: {hasattr(doc, 'pictures')}")

if hasattr(doc, 'pictures'):
    print(f"Number of pictures: {len(doc.pictures)}")
    
    for i, picture in enumerate(doc.pictures):
        print(f"\n--- Picture {i+1} ---")
        print(f"Type: {type(picture)}")
        print(f"Attributes: {[attr for attr in dir(picture) if not attr.startswith('_')]}")
        
        # Check for image data
        for attr in ['image', 'data', 'content', 'pil_image', 'img']:
            if hasattr(picture, attr):
                img_data = getattr(picture, attr)
                print(f"Has {attr}: {type(img_data)}")
                if hasattr(img_data, 'save'):
                    print(f"  - Can save: Yes")
                    print(f"  - Size: {getattr(img_data, 'size', 'Unknown')}")
                else:
                    print(f"  - Can save: No")
        
        # Check for other attributes
        for attr in ['caption', 'alt_text', 'description', 'text']:
            if hasattr(picture, attr):
                value = getattr(picture, attr)
                print(f"{attr}: {value}")

# Check document body for images
if hasattr(doc, 'body'):
    print(f"\n--- Document Body ---")
    print(f"Body type: {type(doc.body)}")
    
    def find_images_in_item(item, level=0):
        indent = "  " * level
        item_type = item.__class__.__name__
        
        if 'Picture' in item_type or 'Image' in item_type:
            print(f"{indent}Found image item: {item_type}")
            for attr in ['image', 'data', 'content', 'pil_image']:
                if hasattr(item, attr):
                    img_data = getattr(item, attr)
                    print(f"{indent}  Has {attr}: {type(img_data)}")
        
        if hasattr(item, 'children'):
            for child in item.children:
                find_images_in_item(child, level + 1)
    
    find_images_in_item(doc.body)
