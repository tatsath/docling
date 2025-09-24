# Docling Version 2.2.1 Model Structure and Usage

## Current Docling Version
**Version: 2.2.1**

## Key Differences from Version 2.54.0
- **Simplified Model Structure**: No complex model repository folders
- **Direct Model Loading**: Models loaded directly from artifacts_path
- **IBM Models Integration**: Uses `docling-ibm-models` package
- **Simplified Pipeline Options**: Fewer configuration options
- **Legacy Output Support**: Default `create_legacy_output=True`

## Model Cache Location
```
~/.cache/docling/models/
```

## Core Model Structure for Version 2.2.1

### 1. **TableFormer Model** (IBM Models)
```
artifacts_path/
├── fat/                    # For ACCURATE mode
│   ├── tm_config.json
│   └── tableformer model files
└── [default]/              # For FAST mode
    ├── tm_config.json
    └── tableformer model files
```
- **Purpose**: Table structure recognition and extraction
- **Model Class**: `TableStructureModel`
- **Code Usage**: `artifacts_path / "fat"` (for accurate mode)
- **Dependencies**: `docling-ibm-models.tableformer`

### 2. **Layout Model** (IBM Models)
```
artifacts_path/
└── layout_model/
    ├── config.json
    └── model files
```
- **Purpose**: Document layout understanding and page structure recognition
- **Model Class**: `LayoutModel`
- **Code Usage**: `LayoutPredictor(artifacts_path)`
- **Dependencies**: `docling-ibm-models.layoutmodel`

### 3. **EasyOCR Model**
```
EasyOCR cache/
└── [OCR model files]
```
- **Purpose**: Text recognition and character detection
- **Model Class**: `EasyOcrModel`
- **Code Usage**: Uses EasyOCR's built-in model storage
- **Dependencies**: `easyocr` package

## Model Loading Pattern for Version 2.2.1

### **Simplified Model Loading**
```python
# Table Structure Model
table_model = TableStructureModel(
    enabled=True,
    artifacts_path=artifacts_path,  # Direct path to model files
    options=table_options
)

# Layout Model
layout_model = LayoutModel(artifacts_path)  # Direct path

# OCR Model
ocr_model = EasyOcrModel(
    enabled=True,
    options=ocr_options
)
```

### **Pipeline Configuration**
```python
pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,  # Points to model directory
    do_table_structure=True,        # Uses TableFormer
    do_ocr=True,                    # Uses EasyOCR
    create_legacy_output=True,      # Legacy format support
)
```

## Model File Types for Version 2.2.1

### **TableFormer Models**
- `tm_config.json` - TableFormer configuration
- Model weight files (format depends on IBM models)

### **Layout Models**
- `config.json` - Layout model configuration
- Model weight files (format depends on IBM models)

### **OCR Models**
- EasyOCR manages its own model storage
- No direct file access needed

## Dependencies for Version 2.2.1

### **Core Dependencies**
```
docling==2.2.1
docling-core==2.2.1
docling-ibm-models==2.0.8
docling-parse==2.1.2
deepsearch-glm==0.26.2
```

### **Model Dependencies**
- `docling-ibm-models` - IBM's model implementations
- `easyocr` - OCR processing
- `torch` - Deep learning framework
- `torchvision` - Computer vision utilities

## Model Usage in Code (Version 2.2.1)

### **Standard PDF Pipeline**
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Configure for offline usage
pipeline_options = PdfPipelineOptions(
    artifacts_path="~/.cache/docling/models",
    do_table_structure=True,
    do_ocr=True,
    create_legacy_output=True
)

# Create converter
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

### **Model Initialization**
```python
# Table Structure Model
table_model = TableStructureModel(
    enabled=True,
    artifacts_path=Path("~/.cache/docling/models"),
    options=TableStructureOptions(
        do_cell_matching=True,
        mode=TableFormerMode.FAST
    )
)

# Layout Model
layout_model = LayoutModel(Path("~/.cache/docling/models"))

# OCR Model
ocr_model = EasyOcrModel(
    enabled=True,
    options=EasyOcrOptions(
        lang=["en"],
        use_gpu=True,
        download_enabled=True
    )
)
```

## Model Download Process (Version 2.2.1)

### **Automatic Download**
Models are downloaded when:
- First running any docling script
- EasyOCR downloads its models automatically
- IBM models need manual download

### **Manual Download**
```bash
# Download IBM models manually
# (No built-in CLI for model download in 2.2.1)
```

## Key Differences from Version 2.54.0

| Feature | Version 2.2.1 | Version 2.54.0 |
|---------|----------------|-----------------|
| **Model Structure** | Direct paths | Repository folders |
| **Model Download** | Manual | Built-in CLI |
| **Settings** | Basic | Advanced with cache_dir |
| **VLM Support** | Limited | Full VLM pipeline |
| **Model Management** | Manual | Automated |
| **Configuration** | Simple | Complex options |

## Model Size Estimates (Version 2.2.1)

| Model Category | Approximate Size | Purpose |
|----------------|------------------|---------|
| **TableFormer** | 500MB - 1GB | Table structure recognition |
| **Layout Model** | 1-2GB | Page layout understanding |
| **EasyOCR Models** | 100-200MB | Text recognition |
| **Total Estimated Size** | **2-4 GB** | Basic offline processing |

## Environment Variables (Version 2.2.1)

```bash
# Set model cache path
export DOCLING_ARTIFACTS_PATH=~/.cache/docling/models

# EasyOCR model storage
export EASYOCR_MODEL_STORAGE_DIR=~/.cache/easyocr
```

## Troubleshooting (Version 2.2.1)

### **Check Model Status**
```bash
# List model directories
ls -la ~/.cache/docling/models/

# Check EasyOCR models
ls -la ~/.cache/easyocr/
```

### **Model Loading Issues**
- Ensure IBM models are properly downloaded
- Check EasyOCR model storage directory
- Verify artifacts_path is correctly set

## Key Files in Codebase (Version 2.2.1)

### **Model Classes**
- `docling/models/table_structure_model.py` - Table recognition
- `docling/models/layout_model.py` - Layout analysis
- `docling/models/easyocr_model.py` - OCR processing

### **Configuration Files**
- `docling/datamodel/pipeline_options.py` - Pipeline configuration
- `docling/datamodel/settings.py` - Basic settings

### **Dependencies**
- `docling-ibm-models` - IBM model implementations
- `easyocr` - OCR engine

## Usage Example (Version 2.2.1)

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions

# Configure pipeline
pipeline_options = PdfPipelineOptions(
    artifacts_path="~/.cache/docling/models",
    do_table_structure=True,
    do_ocr=True,
    ocr_options=EasyOcrOptions(
        lang=["en"],
        use_gpu=True
    )
)

# Create converter
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

# Process document
result = converter.convert("document.pdf")
```

---

**Last Updated**: January 2025  
**Docling Version**: 2.2.1  
**Total Models**: 3 core models (TableFormer, Layout, EasyOCR)  
**Total Size**: ~2-4 GB  
**Status**: ✅ Simplified model structure for basic offline processing
