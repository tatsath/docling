#!/usr/bin/env python3
"""
Correct model downloader for Docling 2.2.1
Uses verified HuggingFace repositories
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download

def download_correct_models():
    """Download models using verified repositories"""
    print("=== DOCLING CORRECT MODEL DOWNLOADER ===")
    print()
    
    # Set up model directory
    current_dir = Path.cwd()
    models_dir = current_dir / "downloaded_models"
    models_dir.mkdir(exist_ok=True)
    
    print(f"📁 Downloading models to: {models_dir}")
    print()
    
    # Verified model repositories
    model_repos = {
        "TableFormer": "microsoft/table-transformer-structure-recognition",
        "Layout": "microsoft/layoutlm-base-uncased", 
        "EasyOCR": "remiai3/OCR_easyocr",
    }
    
    downloaded_models = {}
    
    for model_name, repo_id in model_repos.items():
        try:
            print(f"📥 Downloading {model_name} from {repo_id}...")
            model_path = models_dir / model_name.lower()
            model_path.mkdir(exist_ok=True)
            
            # Download model
            snapshot_download(
                repo_id=repo_id,
                local_dir=str(model_path),
                local_dir_use_symlinks=False
            )
            
            downloaded_models[model_name] = model_path
            print(f"✅ {model_name} downloaded successfully")
            
        except Exception as e:
            print(f"⚠️  {model_name} download failed: {e}")
            continue
    
    print()
    print("✅ Model download completed!")
    print(f"📁 Models saved to: {models_dir}")
    
    # Show what was downloaded
    print()
    print("📊 Downloaded Models:")
    for model_name, model_path in downloaded_models.items():
        if model_path.exists():
            total_size = 0
            file_count = 0
            for item in model_path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
            
            size_mb = total_size / (1024 * 1024)
            print(f"   - {model_name}: {file_count} files ({size_mb:.1f} MB)")
    
    return len(downloaded_models) > 0

def main():
    """Main function"""
    print("Docling Correct Model Downloader")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("test_docling_2.2.1.py").exists():
        print("❌ Please run this script from the docling directory")
        sys.exit(1)
    
    # Download models
    if download_correct_models():
        print()
        print("🚀 Next steps:")
        print("   1. Models are now available in ./downloaded_models/")
        print("   2. Update your offline script to use these models")
        print("   3. Set artifacts_path to ./downloaded_models/")
        print("   4. Enable do_table_structure=True and do_ocr=True")
    else:
        print("❌ Model download failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
