# 📁 Docling Model Structure and Folders

This document provides a comprehensive overview of all model files and folders used in the offline PDF processing solution.

## 🗂️ **Model Directory Structure**

### **Main Model Cache Location**
```
~/.cache/docling/models/
```

### **Docling Core Models**

#### 1. **`ds4sd--docling-models/`** - Main Docling Model Artifacts
```
ds4sd--docling-models/
├── config.json
└── model_artifacts/
    └── tableformer/
        ├── accurate/
        │   ├── tableformer_accurate.safetensors
        │   └── tm_config.json
        └── fast/
            ├── tableformer_fast.safetensors
            └── tm_config.json
```
- **Purpose**: Table structure recognition and extraction
- **Models**: TableFormer (accurate & fast variants)
- **Size**: ~500MB - 1GB

#### 2. **`ds4sd--docling-layout-heron/`** - Layout Analysis Model
```
ds4sd--docling-layout-heron/
├── config.json
├── preprocessor_config.json
└── model.safetensors
```
- **Purpose**: Document layout understanding and page structure recognition
- **Model**: Heron-based layout analysis
- **Size**: ~1-2GB

#### 3. **`ds4sd--DocumentFigureClassifier/`** - Figure Classification
```
ds4sd--DocumentFigureClassifier/
├── config.json
└── model.safetensors
```
- **Purpose**: Image/figure type classification and visual element recognition
- **Model**: Document figure classifier
- **Size**: ~200-500MB

#### 4. **`ds4sd--CodeFormulaV2/`** - Code and Formula Processing
```
ds4sd--CodeFormulaV2/
├── added_tokens.json
├── chat_template.json
├── config.json
├── generation_config.json
├── model.safetensors
├── preprocessor_config.json
├── processor_config.json
├── special_tokens_map.json
├── tokenizer.json
└── tokenizer_config.json
```
- **Purpose**: Mathematical formula recognition and code block processing
- **Model**: CodeFormula V2
- **Size**: ~1-2GB

#### 5. **`EasyOcr/`** - OCR Engine Models
```
EasyOcr/
└── [OCR model files]
```
- **Purpose**: Text recognition and character detection
- **Models**: EasyOCR language models
- **Size**: ~100-200MB

## 🧠 **VLM (Vision Language Model) Models**

### **SmolDocling VLM Model Location**
```
~/.cache/huggingface/hub/
└── [smol-docling model files]
```

### **Transformers Cache**
```
~/.cache/transformers/
└── [cached transformer models]
```

**Note**: SmolDocling VLM model is downloaded automatically on first VLM pipeline execution.

## 📊 **Model Size Summary**

| Model Category | Approximate Size | Purpose |
|----------------|------------------|---------|
| **Docling Core Models** | 2-4 GB | Document processing, layout analysis |
| **TableFormer Models** | 500MB - 1GB | Table structure recognition |
| **Layout Heron** | 1-2GB | Page layout understanding |
| **Document Figure Classifier** | 200-500MB | Image/figure classification |
| **CodeFormula V2** | 1-2GB | Formula and code recognition |
| **EasyOCR Models** | 100-200MB | Text recognition |
| **SmolDocling VLM** | 1-2GB | Advanced document understanding |
| **Total Estimated Size** | **6-12 GB** | Complete offline processing |

## 🔧 **Model File Types**

### **Model Weights**
- `.safetensors` - Safe tensor format (preferred)
- `.bin` - Binary model weights
- `.pt` - PyTorch model files
- `.pth` - PyTorch checkpoint files

### **Configuration Files**
- `config.json` - Model configuration
- `preprocessor_config.json` - Preprocessing settings
- `tokenizer_config.json` - Tokenizer configuration
- `generation_config.json` - Text generation settings

### **Tokenizer Files**
- `tokenizer.json` - Tokenizer vocabulary
- `vocab.json` - Vocabulary mapping
- `special_tokens_map.json` - Special token definitions

## 🚀 **Model Download Process**

### **Automatic Download**
Models are downloaded automatically when:
1. First running any docling script
2. Using the Streamlit app
3. Executing VLM processing

### **Manual Download**
```bash
# Activate conda environment
conda activate docling

# Run any processing script to trigger model download
python test_offline.py
```

## 🔍 **Model Verification**

### **Check Model Status**
```bash
# List all model directories
ls -la ~/.cache/docling/models/

# Check model file sizes
du -sh ~/.cache/docling/models/*/

# Verify specific model files
find ~/.cache/docling/models/ -name "*.safetensors" -exec ls -lh {} \;
```

### **Test Model Loading**
```python
# Test script to verify models are loaded correctly
python test_offline.py
```

## 📝 **Model Usage in Code**

### **OCR Pipeline**
```python
pipeline = PdfPipelineOptions(
    artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
    enable_remote_services=False,
    do_table_structure=True,
    do_ocr=True,
    do_chunking=True,
)
```

### **VLM Pipeline**
```python
converter = DocumentConverter({
    InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline)
})
```

## 🛠️ **Troubleshooting**

### **Missing Models**
If models are missing:
1. Check internet connection for initial download
2. Verify `DOCLING_ARTIFACTS_PATH` environment variable
3. Run model download script
4. Check disk space (need 6-12GB free)

### **Model Loading Errors**
- Ensure all model files are complete
- Check file permissions
- Verify conda environment is activated
- Clear cache and re-download if corrupted

## 📋 **Environment Variables**

```bash
# Set model cache path
export DOCLING_ARTIFACTS_PATH=~/.cache/docling/models

# Enable offline mode
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

## 🔗 **Related Files**

- `requirements.txt` - Python dependencies
- `streamlit_requirements.txt` - Streamlit app dependencies
- `test_offline.py` - Model verification script
- `streamlit_app.py` - Web interface for model usage

---

**Last Updated**: September 16, 2025  
**Total Models**: 5 core docling models + 1 VLM model  
**Total Size**: ~6-12 GB  
**Status**: ✅ All models downloaded and ready for offline use
