# Offline PDF Parser using Docling

This project provides a complete offline PDF processing solution using Docling, capable of extracting text, tables, and images from PDF documents without requiring an internet connection.

## Features

- **Completely Offline**: All models are pre-downloaded and stored locally
- **Comprehensive Extraction**: Extracts text, tables, images, and document structure
- **Multiple Output Formats**: JSON, Markdown, and plain text
- **GPU Acceleration**: Uses CUDA for faster processing when available
- **Table Recognition**: Advanced table structure recognition and extraction
- **OCR Support**: Optical Character Recognition for scanned documents

## Setup

### 1. Environment Setup

```bash
# Create conda environment
conda create -n docling python=3.12 -y
conda activate docling

# Install docling
pip install docling
```

### 2. Download Models (One-time setup)

```bash
# Download all required models for offline usage
docling-tools models download
```

This will download models to `~/.cache/docling/models/` (approximately 1.2GB).

## Usage

### Basic Usage

```bash
# Activate environment
conda activate docling

# Run the parser
python final_offline_parser.py
```

### Files

- `final_offline_parser.py` - Main parser script (recommended)
- `offline_pdf_parser.py` - Original parser script
- `fixed_offline_parser.py` - Fixed version
- `test_offline.py` - Test script to verify setup
- `debug_document_structure.py` - Debug script for document structure analysis

### Output

The parser creates an `output/` directory with:

- `companies_house_document_content.json` - Complete structured data
- `companies_house_document_content.md` - Markdown formatted output
- `companies_house_document_text.txt` - Plain text output

## Example Results

For the `companies_house_document.pdf`:

- **Pages processed**: 32
- **Tables found**: 20
- **Figures found**: 3
- **Text extracted**: 76,975 characters
- **Processing time**: ~4 minutes (with GPU acceleration)

## Technical Details

### Offline Configuration

The parser is configured to run completely offline:

```python
pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    enable_remote_services=False,  # No internet required
    do_table_structure=True,       # Table recognition
    do_ocr=True,                   # OCR processing
    do_chunking=True,              # Document chunking
)
```

### Model Requirements

- **Layout Model**: Document layout analysis
- **Tableformer Model**: Table structure recognition
- **Picture Classifier**: Image classification
- **Code Formula Model**: Mathematical formula recognition
- **EasyOCR Models**: Text recognition

## Troubleshooting

### Common Issues

1. **Models not found**: Run `docling-tools models download`
2. **CUDA errors**: Ensure NVIDIA drivers and CUDA are properly installed
3. **Memory issues**: Reduce batch size or use CPU-only mode

### Testing Setup

```bash
python test_offline.py
```

This will verify that all models are downloaded and the environment is properly configured.

## Performance

- **GPU Processing**: ~4 minutes for 32-page document
- **CPU Processing**: ~8-10 minutes for 32-page document
- **Memory Usage**: ~2-4GB RAM during processing
- **Storage**: ~1.2GB for all models

## License

This project uses Docling, which is licensed under the Apache License 2.0.
