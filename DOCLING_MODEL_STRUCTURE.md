# Docling Model Structure and Usage

## Current Docling Version
**Version: 2.54.0**

## Model Cache Location
```
~/.cache/docling/models/
```

## Core Model Structure

### 1. **TableFormer Model** (`ds4sd--docling-models/`)
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
- **Model Class**: `TableStructureModel`
- **Code Usage**: `TableStructureModel._model_repo_folder = "ds4sd--docling-models"`
- **Path**: `artifacts_path / "ds4sd--docling-models" / "model_artifacts/tableformer"`

### 2. **Layout Model** (Heron-based)
```
ds4sd--docling-layout-heron/
├── config.json
├── preprocessor_config.json
└── model.safetensors
```
- **Purpose**: Document layout understanding and page structure recognition
- **Model Class**: `LayoutModel`
- **Code Usage**: Uses `LayoutOptions().model_spec.model_repo_folder`
- **Default Config**: `DOCLING_LAYOUT_HERON`

### 3. **Document Picture Classifier**
```
ds4sd--DocumentFigureClassifier/
├── config.json
└── model.safetensors
```
- **Purpose**: Image/figure type classification and visual element recognition
- **Model Class**: `DocumentPictureClassifier`
- **Code Usage**: `DocumentPictureClassifier._model_repo_folder`

### 4. **Code Formula Model**
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
- **Model Class**: `CodeFormulaModel`
- **Code Usage**: `CodeFormulaModel._model_repo_folder`

### 5. **EasyOCR Model**
```
EasyOcr/
└── [OCR model files]
```
- **Purpose**: Text recognition and character detection
- **Model Class**: `EasyOcrModel`
- **Code Usage**: `EasyOcrModel._model_repo_folder = "EasyOcr"`

## VLM (Vision Language Model) Structure

### SmolDocling VLM Models
```
HuggingFaceTB--SmolVLM-256M-Instruct/
├── config.json
├── model.safetensors
├── preprocessor_config.json
├── processor_config.json
└── tokenizer files
```

### GraniteDocling VLM Models
```
ibm-granite--granitedocling-3.3-2b/
├── config.json
├── model.safetensors
├── preprocessor_config.json
├── processor_config.json
└── tokenizer files
```

## How Models Are Used in Code

### 1. **Model Loading Pattern**
```python
# All models follow this pattern:
if artifacts_path is None:
    artifacts_path = self.download_models()
else:
    artifacts_path = Path(artifacts_path) / self._model_repo_folder
```

### 2. **Pipeline Configuration**
```python
pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,  # Points to ~/.cache/docling/models/
    enable_remote_services=False,   # Forces local model usage
    do_table_structure=True,        # Uses TableFormer
    do_ocr=True,                    # Uses EasyOCR
    do_chunking=True,               # Uses layout models
)
```

### 3. **Model Initialization**
```python
# Layout Model
layout_model = LayoutModel(
    enabled=True,
    artifacts_path=artifacts_path,
    options=layout_options,
    accelerator_options=accelerator_options
)

# Table Structure Model
table_model = TableStructureModel(
    enabled=True,
    artifacts_path=artifacts_path,
    options=table_options,
    accelerator_options=accelerator_options
)

# OCR Model
ocr_model = EasyOcrModel(
    enabled=True,
    artifacts_path=artifacts_path,
    options=ocr_options,
    accelerator_options=accelerator_options
)
```

## Model Download Process

### 1. **Automatic Download**
Models are downloaded when:
- First running any docling script
- Using `docling-tools models download`
- Running VLM processing

### 2. **Manual Download**
```bash
# Download all default models
docling-tools models download

# Download specific models
docling-tools models download --models layout tableformer easyocr

# Download all models
docling-tools models download --all
```

### 3. **Model Download Code**
```python
# From docling/utils/model_downloader.py
def download_models(
    output_dir: Optional[Path] = None,
    with_layout: bool = True,
    with_tableformer: bool = True,
    with_code_formula: bool = True,
    with_picture_classifier: bool = True,
    with_easyocr: bool = True,
    # ... other parameters
):
    # Downloads models to output_dir
```

## Model File Types

### **Model Weights**
- `.safetensors` - Safe tensor format (preferred)
- `.bin` - Binary model weights
- `.pt` - PyTorch model files

### **Configuration Files**
- `config.json` - Model configuration
- `preprocessor_config.json` - Preprocessing settings
- `tokenizer_config.json` - Tokenizer configuration
- `generation_config.json` - Text generation settings

### **Tokenizer Files**
- `tokenizer.json` - Tokenizer vocabulary
- `special_tokens_map.json` - Special token definitions

## Environment Variables

```bash
# Set model cache path
export DOCLING_ARTIFACTS_PATH=~/.cache/docling/models

# Enable offline mode
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

## Model Usage in Pipelines

### **Standard PDF Pipeline**
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Configure for offline usage
pipeline_options = PdfPipelineOptions(
    artifacts_path="~/.cache/docling/models",
    enable_remote_services=False,
    do_table_structure=True,
    do_ocr=True,
    do_chunking=True,
)

# Create converter
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

### **VLM Pipeline**
```python
from docling.pipeline.vlm_pipeline import VlmPipeline

# VLM models are loaded from HuggingFace cache
# ~/.cache/huggingface/hub/
```

## Model Size Estimates

| Model Category | Approximate Size | Purpose |
|----------------|------------------|---------|
| **TableFormer** | 500MB - 1GB | Table structure recognition |
| **Layout Heron** | 1-2GB | Page layout understanding |
| **Document Figure Classifier** | 200-500MB | Image/figure classification |
| **CodeFormula V2** | 1-2GB | Formula and code recognition |
| **EasyOCR Models** | 100-200MB | Text recognition |
| **SmolDocling VLM** | 1-2GB | Advanced document understanding |
| **Total Estimated Size** | **6-12 GB** | Complete offline processing |

## Troubleshooting

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

## Key Files in Codebase

### **Model Classes**
- `docling/models/layout_model.py` - Layout analysis
- `docling/models/table_structure_model.py` - Table recognition
- `docling/models/easyocr_model.py` - OCR processing
- `docling/models/document_picture_classifier.py` - Image classification
- `docling/models/code_formula_model.py` - Formula recognition

### **Configuration Files**
- `docling/datamodel/pipeline_options.py` - Pipeline configuration
- `docling/datamodel/layout_model_specs.py` - Layout model specifications
- `docling/datamodel/vlm_model_specs.py` - VLM model specifications

### **Download Management**
- `docling/cli/models.py` - CLI commands for model management
- `docling/utils/model_downloader.py` - Core download functionality
- `docling/models/utils/hf_model_download.py` - HuggingFace model download

---

**Last Updated**: January 2025  
**Docling Version**: 2.54.0  
**Total Models**: 5 core docling models + VLM models  
**Total Size**: ~6-12 GB  
**Status**: ✅ Ready for offline processing
