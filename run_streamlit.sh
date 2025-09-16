#!/bin/bash
# Streamlit App Launcher

echo "🚀 Starting Offline PDF Parser Streamlit App..."
echo "📄 Upload PDFs and process with OCR or VLM - Completely Offline!"
echo ""

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate docling

# Check if models are available
if [ ! -d "$HOME/.cache/docling/models" ]; then
    echo "⚠️  Models not found. The app will download them on first use."
    echo "📥 This may take a few minutes..."
    echo ""
fi

# Run Streamlit app
echo "🌐 Starting Streamlit server..."
echo "📱 Open your browser to: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
