#!/usr/bin/env python3
"""
Download essential Docling models for offline processing
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download

def download_essential_models():
    """Download essential Docling models"""
    print("=== DOCLING MODEL DOWNLOADER ===")
    print()
    
    # Set up model directory
    current_dir = Path.cwd()
    models_dir = current_dir / "downloaded_models"
    models_dir.mkdir(exist_ok=True)
    
    print(f"📁 Downloading models to: {models_dir}")
    print()
    
    try:
        # Download essential models using HuggingFace Hub
        print("🔄 Downloading essential models...")
        print("   - TableFormer (table structure detection)")
        print("   - Layout models (advanced layout analysis)")
        print("   - EasyOCR models (optical character recognition)")
        print()
        
        # Model repositories from HuggingFace
        model_repos = {
            "TableFormer": "ibm/table-transformer-structure",
            "Layout": "ibm/layoutlmv3-base",
            "EasyOCR": "JaidedAI/EasyOCR"
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
        
    except Exception as e:
        print(f"❌ Error downloading models: {e}")
        return False

def check_downloaded_models():
    """Check what models are available"""
    print()
    print("=== MODEL AVAILABILITY CHECK ===")
    
    models_dir = Path.cwd() / "downloaded_models"
    
    if not models_dir.exists():
        print("❌ No models directory found")
        return False
    
    print(f"📁 Checking models in: {models_dir}")
    print()
    
    # Check for specific model types
    model_types = {
        "TableFormer": ["tableformer", "table"],
        "Layout": ["layout", "model.pt"],
        "EasyOCR": ["easyocr", "ocr"]
    }
    
    found_models = {}
    for model_type, keywords in model_types.items():
        found_files = []
        for keyword in keywords:
            for file in models_dir.rglob(f"*{keyword}*"):
                if file.is_file():
                    found_files.append(file.name)
        found_models[model_type] = found_files
    
    for model_type, files in found_models.items():
        if files:
            print(f"✅ {model_type}: {len(files)} files found")
            for file in files[:3]:  # Show first 3 files
                print(f"   - {file}")
            if len(files) > 3:
                print(f"   ... and {len(files) - 3} more files")
        else:
            print(f"❌ {model_type}: No files found")
    
    return True

def main():
    """Main function"""
    print("Docling Model Downloader")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("test_docling_2.2.1.py").exists():
        print("❌ Please run this script from the docling directory")
        sys.exit(1)
    
    # Download models
    if download_essential_models():
        print()
        check_downloaded_models()
        
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
