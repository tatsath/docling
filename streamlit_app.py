#!/usr/bin/env python3
"""
Simple Streamlit App for Offline PDF Processing
"""

import streamlit as st
import os
import time
import tempfile
from pathlib import Path
import chromadb
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.datamodel.settings import settings
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
import uuid

# Page config
st.set_page_config(
    page_title="Offline PDF Parser",
    page_icon="📄",
    layout="wide"
)

def setup_offline_environment():
    """Setup offline environment"""
    os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

def extract_images_from_doc(doc):
    """Extract images from DoclingDocument with multiple fallback methods"""
    images = []
    
    # Method 1: Check pictures attribute
    if hasattr(doc, 'pictures') and doc.pictures:
        for i, picture in enumerate(doc.pictures):
            try:
                # Try get_image method
                if hasattr(picture, 'get_image'):
                    img = picture.get_image(doc)
                    if img is not None:
                        images.append({
                            'type': 'picture',
                            'index': i,
                            'image': img,
                            'source': 'pictures.get_image()'
                        })
                # Try direct image attribute
                elif hasattr(picture, 'image') and picture.image is not None:
                    images.append({
                        'type': 'picture',
                        'index': i,
                        'image': picture.image,
                        'source': 'pictures.image'
                    })
            except Exception as e:
                st.warning(f"Could not extract picture {i+1}: {e}")
    
    # Method 2: Check for images in markdown content
    if hasattr(doc, 'export_to_markdown'):
        markdown = doc.export_to_markdown()
        import re
        markdown_images = re.findall(r'!\[.*?\]\(.*?\)', markdown)
        for i, img_ref in enumerate(markdown_images):
            images.append({
                'type': 'markdown',
                'index': i,
                'reference': img_ref,
                'source': 'markdown_content'
            })
    
    return images

def chunk_document(doc, max_tokens=512):
    """Chunk the document using HybridChunker"""
    try:
        # Setup tokenizer for chunking
        EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
        tokenizer = HuggingFaceTokenizer(
            tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID),
            max_tokens=max_tokens
        )
        
        # Create chunker
        chunker = HybridChunker(
            tokenizer=tokenizer,
            merge_peers=True
        )
        
        # Chunk the document
        chunk_iter = chunker.chunk(dl_doc=doc)
        chunks = list(chunk_iter)
        
        # Process chunks
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            enriched_text = chunker.contextualize(chunk=chunk)
            processed_chunks.append({
                "id": str(uuid.uuid4()),
                "index": i,
                "text": chunk.text,
                "enriched_text": enriched_text,
                "tokens": tokenizer.count_tokens(chunk.text),
                "enriched_tokens": tokenizer.count_tokens(enriched_text)
            })
        
        return processed_chunks, chunker
    except Exception as e:
        st.error(f"Error during chunking: {e}")
        return [], None

def embed_and_store_chunks(chunks, collection_name, embedding_model="all-MiniLM-L6-v2"):
    """Embed chunks and store in ChromaDB"""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        try:
            collection = client.get_collection(name=collection_name)
        except:
            collection = client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize embedding model
        model = SentenceTransformer(embedding_model)
        
        # Prepare data for ChromaDB
        documents = [chunk["enriched_text"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [{
            "index": chunk["index"],
            "tokens": chunk["tokens"],
            "enriched_tokens": chunk["enriched_tokens"],
            "original_text": chunk["text"][:500] + "..." if len(chunk["text"]) > 500 else chunk["text"]
        } for chunk in chunks]
        
        # Generate embeddings
        embeddings = model.encode(documents).tolist()
        
        # Add to collection
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return True, f"Successfully embedded {len(chunks)} chunks in collection '{collection_name}'"
    except Exception as e:
        return False, f"Error embedding chunks: {e}"

def search_collection(collection_name, query, n_results=5, embedding_model="all-MiniLM-L6-v2"):
    """Search the collection for relevant chunks"""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name=collection_name)
        
        # Initialize embedding model
        model = SentenceTransformer(embedding_model)
        
        # Generate query embedding
        query_embedding = model.encode([query]).tolist()[0]
        
        # Search collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    except Exception as e:
        st.error(f"Error searching collection: {e}")
        return None

def process_pdf_ocr(pdf_path, use_gpu=True, num_threads=8):
    """Process PDF with OCR pipeline using optimized accelerator options"""
    start_time = time.time()
    
    # Configure accelerator options for maximum performance
    if use_gpu:
        accelerator_options = AcceleratorOptions(
            num_threads=num_threads, 
            device=AcceleratorDevice.CUDA
        )
    else:
        accelerator_options = AcceleratorOptions(
            num_threads=num_threads, 
            device=AcceleratorDevice.CPU
        )
    
    pipeline = PdfPipelineOptions(
        artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
        enable_remote_services=False,
        do_table_structure=True,
        do_ocr=True,
        do_chunking=True,
    )
    pipeline.accelerator_options = accelerator_options
    pipeline.ocr_options = EasyOcrOptions(use_gpu=use_gpu, lang=['en'])
    pipeline.table_structure_options.do_cell_matching = True
    
    # Enable profiling for performance monitoring
    settings.debug.profile_pipeline_timings = True
    
    converter = DocumentConverter({
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline)
    })
    
    result = converter.convert(pdf_path)
    doc = result.document
    
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Get timing information
    conversion_time = time.time() - start_time
    if hasattr(result, 'timings') and hasattr(result.timings, 'pipeline_total'):
        if hasattr(result.timings.pipeline_total, 'times') and result.timings.pipeline_total.times:
            conversion_time = result.timings.pipeline_total.times[0]
    
    return {
        "method": "OCR",
        "time": time.time() - start_time,
        "conversion_time": conversion_time,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "text": text,
        "markdown": markdown,
        "docling_document": doc  # Store the DoclingDocument object
    }

def process_pdf_vlm(pdf_path, use_gpu=True, num_threads=8):
    """Process PDF with VLM pipeline using optimized accelerator options - COMPLETELY OFFLINE"""
    start_time = time.time()
    
    # Ensure offline environment is set
    setup_offline_environment()
    
    # Configure accelerator options for VLM
    if use_gpu:
        accelerator_options = AcceleratorOptions(
            num_threads=num_threads, 
            device=AcceleratorDevice.CUDA
        )
    else:
        accelerator_options = AcceleratorOptions(
            num_threads=num_threads, 
            device=AcceleratorDevice.CPU
        )
    
    # Enable profiling for performance monitoring
    settings.debug.profile_pipeline_timings = True
    
    # Create VLM pipeline with proper configuration - OFFLINE MODE
    from docling.datamodel.pipeline_options import VlmPipelineOptions
    from docling.datamodel.vlm_model_specs import SMOLDOCLING_TRANSFORMERS
    
    # Use VLM pipeline options with SmolDocling - OFFLINE
    vlm_pipeline_options = VlmPipelineOptions(
        vlm_options=SMOLDOCLING_TRANSFORMERS,
        accelerator_options=accelerator_options
    )
    
    converter = DocumentConverter({
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
            pipeline_options=vlm_pipeline_options
        )
    })
    
    result = converter.convert(source=pdf_path)
    doc = result.document
    
    text = doc.export_to_text()
    markdown = doc.export_to_markdown()
    
    # Get timing information
    conversion_time = time.time() - start_time
    if hasattr(result, 'timings') and hasattr(result.timings, 'pipeline_total'):
        if hasattr(result.timings.pipeline_total, 'times') and result.timings.pipeline_total.times:
            conversion_time = result.timings.pipeline_total.times[0]
    
    return {
        "method": "VLM",
        "time": time.time() - start_time,
        "conversion_time": conversion_time,
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "tables": len(doc.tables) if hasattr(doc, 'tables') else 0,
        "pictures": len(doc.pictures) if hasattr(doc, 'pictures') else 0,
        "pages": len(doc.pages) if hasattr(doc, 'pages') else 0,
        "text": text,
        "markdown": markdown,
        "docling_document": doc  # Store the DoclingDocument object
    }

def main():
    """Main Streamlit app"""
    st.title("📄 Offline PDF Parser with RAG")
    st.markdown("**Process PDFs with OCR or VLM, Chunk, Embed, and Chat - Completely Offline**")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📄 PDF Processing", "🧩 Chunking & Embedding", "💬 Chat"])
    
    with tab1:
        pdf_processing_tab()
    
    with tab2:
        chunking_embedding_tab()
    
    with tab3:
        chat_tab()

def pdf_processing_tab():
    """PDF Processing Tab"""
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Processing Options")
        
        # Processing method selection
        processing_method = st.radio(
            "Processing Method",
            ["OCR (Text Recognition)", "VLM (Vision Language Model)"],
            help="OCR for text recognition, VLM for advanced document understanding"
        )
        
        # GPU option
        use_gpu = st.checkbox(
            "Use GPU Acceleration",
            value=True,
            help="Enable GPU acceleration for faster processing"
        )
        
        # Thread count option
        num_threads = st.slider(
            "Number of Threads",
            min_value=1,
            max_value=16,
            value=8,
            help="Number of threads for parallel processing (higher = faster, but more memory)"
        )
        
        # Comparison option
        compare_methods = st.checkbox(
            "Compare Both Methods",
            help="Process the same PDF with both OCR and VLM to compare outputs"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload PDF Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document for processing"
        )

    with col2:
        st.header("📊 Processing Status")
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📄 Size: {uploaded_file.size:,} bytes")
        else:
            st.warning("⚠️ Please upload a PDF file")

    # Process button
    if uploaded_file is not None:
        if st.button("🚀 Process PDF", type="primary", use_container_width=True):
            # Setup offline environment
            setup_offline_environment()

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Process the PDF
                if compare_methods:
                    with st.spinner(f"Processing with both OCR and VLM using {num_threads} threads..."):
                        # Process with both methods
                        ocr_stats = process_pdf_ocr(tmp_path, use_gpu, num_threads)
                        vlm_stats = process_pdf_vlm(tmp_path, use_gpu, num_threads)
                        
                        # Display comparison
                        st.success("✅ Both methods completed successfully!")
                        
                        # Comparison metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("🔍 OCR Results")
                            st.metric("Time", f"{ocr_stats['time']:.1f}s")
                            st.metric("Text Chars", f"{ocr_stats['text_chars']:,}")
                            st.metric("Tables", ocr_stats['tables'])
                            st.metric("Images", ocr_stats['pictures'])
                        
                        with col2:
                            st.subheader("🧠 VLM Results")
                            st.metric("Time", f"{vlm_stats['time']:.1f}s")
                            st.metric("Text Chars", f"{vlm_stats['text_chars']:,}")
                            st.metric("Tables", vlm_stats['tables'])
                            st.metric("Images", vlm_stats['pictures'])
                        
                        # Side-by-side markdown comparison
                        col1, col2 = st.columns(2)
                        with col1:
                            with st.expander("🔍 OCR Markdown", expanded=False):
                                st.code(ocr_stats['markdown'], language='markdown')
                        
                        with col2:
                            with st.expander("🧠 VLM Markdown", expanded=False):
                                st.code(vlm_stats['markdown'], language='markdown')
                        
                        # Show differences
                        if ocr_stats['text_chars'] != vlm_stats['text_chars']:
                            st.info(f"📊 **Text Length Difference**: OCR={ocr_stats['text_chars']:,} chars, VLM={vlm_stats['text_chars']:,} chars")
                        if ocr_stats['tables'] != vlm_stats['tables']:
                            st.info(f"📊 **Table Count Difference**: OCR={ocr_stats['tables']} tables, VLM={vlm_stats['tables']} tables")
                        if ocr_stats['pictures'] != vlm_stats['pictures']:
                            st.info(f"📊 **Image Count Difference**: OCR={ocr_stats['pictures']} images, VLM={vlm_stats['pictures']} images")
                        
                        # Store results in session state for chunking
                        st.session_state['processed_doc'] = vlm_stats['docling_document']  # Use VLM DoclingDocument
                        st.session_state['markdown_content'] = vlm_stats['markdown']
                        
                        return  # Exit early for comparison mode
                else:
                    with st.spinner(f"Processing with {processing_method} using {num_threads} threads..."):
                        if "OCR" in processing_method:
                            stats = process_pdf_ocr(tmp_path, use_gpu, num_threads)
                        else:
                            stats = process_pdf_vlm(tmp_path, use_gpu, num_threads)
                
                # Display results
                st.success("✅ Processing completed successfully!")
                
                # Statistics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("⏱️ Time", f"{stats['time']:.1f}s")
                with col2:
                    st.metric("📄 Pages", stats['pages'])
                with col3:
                    st.metric("📊 Tables", stats['tables'])
                with col4:
                    st.metric("🖼️ Images", stats['pictures'])
                with col5:
                    st.metric("📝 Text Chars", f"{stats['text_chars']:,}")
                
                # Additional info
                st.info(f"🔧 GPU: {'Enabled' if use_gpu else 'Disabled'} | 🧵 Threads: {num_threads} | ⚡ Conversion: {stats.get('conversion_time', stats['time']):.1f}s")
                
                # Pipeline info
                if "OCR" in processing_method:
                    st.info("🔍 **OCR Pipeline**: Text recognition and table structure analysis")
                else:
                    st.info("🧠 **VLM Pipeline**: Advanced document understanding with SmolDocling (OFFLINE MODE)")
                    
                # Offline verification
                artifacts_path = os.path.expanduser("~/.cache/docling/models")
                if os.path.exists(artifacts_path):
                    st.success(f"✅ Offline models available at: {artifacts_path}")
                else:
                    st.warning("⚠️ Offline models not found. Run 'docling-tools models download' first.")
                
                # Raw markdown output (collapsible)
                with st.expander(f"📄 Raw Markdown Output ({stats['markdown_chars']:,} characters)", expanded=False):
                    st.code(stats['markdown'], language='markdown')
                
                # Tables section
                if stats['tables'] > 0:
                    with st.expander(f"📊 Tables ({stats['tables']} found)", expanded=False):
                        # Extract tables from markdown (simplified approach)
                        markdown_lines = stats['markdown'].split('\n')
                        table_content = []
                        in_table = False

                        for line in markdown_lines:
                            if '|' in line and ('---' in line or line.strip().startswith('|')):
                                in_table = True
                                table_content.append(line)
                            elif in_table and '|' in line:
                                table_content.append(line)
                            elif in_table and '|' not in line:
                                break

                        if table_content:
                            st.code('\n'.join(table_content), language='markdown')
                        else:
                            st.info("Table content could not be extracted from markdown")
                else:
                    st.info("📊 No tables found in the document")

                # Images section
                if stats['pictures'] > 0:
                    with st.expander(f"🖼️ Images ({stats['pictures']} found)", expanded=False):
                        # Use the new image extraction function
                        doc = stats['docling_document']
                        images = extract_images_from_doc(doc)
                        
                        if images:
                            for i, img_data in enumerate(images):
                                st.markdown(f"**Image {i+1}** (Source: {img_data['source']})")
                                
                                if img_data['type'] == 'picture' and 'image' in img_data:
                                    # Display actual image
                                    try:
                                        st.image(img_data['image'], caption=f"Image {i+1}")
                                    except Exception as e:
                                        st.error(f"Could not display image {i+1}: {e}")
                                elif img_data['type'] == 'markdown':
                                    # Display markdown reference
                                    st.markdown(img_data['reference'])
                        else:
                            # Fallback to markdown extraction
                            markdown_lines = stats['markdown'].split('\n')
                            image_lines = [line for line in markdown_lines if '![' in line or '<img' in line]
                            
                            if image_lines:
                                st.code('\n'.join(image_lines), language='markdown')
                            else:
                                st.info("Images found but no extractable image data detected")
                else:
                    st.info("🖼️ No images found in the document")

                # Download buttons
                st.header("💾 Download Results")
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="📄 Download Markdown",
                        data=stats['markdown'],
                        file_name=f"{Path(uploaded_file.name).stem}_{stats['method'].lower()}.md",
                        mime="text/markdown"
                    )

                with col2:
                    st.download_button(
                        label="📝 Download Text",
                        data=stats['text'],
                        file_name=f"{Path(uploaded_file.name).stem}_{stats['method'].lower()}.txt",
                        mime="text/plain"
                    )
                
                # Store results in session state for chunking
                st.session_state['processed_doc'] = stats['docling_document']  # Store DoclingDocument object
                st.session_state['markdown_content'] = stats['markdown']
                
                # Chunking button
                st.header("🧩 Next Step: Chunking")
                if st.button("🔪 Chunk Document", type="secondary", use_container_width=True):
                    st.info("📋 Go to the 'Chunking & Embedding' tab to process the document chunks!")

            except Exception as e:
                st.error(f"❌ Error processing PDF: {e}")
                st.exception(e)
            finally:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

def chunking_embedding_tab():
    """Chunking and Embedding Tab"""
    st.header("🧩 Document Chunking & Embedding")
    
    if 'processed_doc' not in st.session_state:
        st.warning("⚠️ Please process a PDF first in the 'PDF Processing' tab.")
        return
    
    # Chunking options
    col1, col2 = st.columns(2)
    with col1:
        max_tokens = st.slider(
            "Max Tokens per Chunk",
            min_value=64,
            max_value=1024,
            value=512,
            help="Maximum number of tokens per chunk"
        )
    
    with col2:
        embedding_model = st.selectbox(
            "Embedding Model",
            ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "all-MiniLM-L12-v2"],
            help="Sentence transformer model for embeddings"
        )
    
    # Chunking section
    if st.button("🔪 Chunk Document", type="primary"):
        with st.spinner("Chunking document..."):
            # Get the processed document - it's already the DoclingDocument object
            doc = st.session_state['processed_doc']
            
            chunks, chunker = chunk_document(doc, max_tokens)
            
            if chunks:
                st.session_state['chunks'] = chunks
                st.session_state['chunker'] = chunker
                st.success(f"✅ Document chunked into {len(chunks)} chunks!")
                
                # Display chunk statistics
                total_tokens = sum(chunk['tokens'] for chunk in chunks)
                avg_tokens = total_tokens / len(chunks)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Chunks", len(chunks))
                with col2:
                    st.metric("Total Tokens", f"{total_tokens:,}")
                with col3:
                    st.metric("Avg Tokens/Chunk", f"{avg_tokens:.1f}")
            else:
                st.error("❌ Failed to chunk document")
    
    # Display chunks if available
    if 'chunks' in st.session_state:
        st.header("📋 Document Chunks")
        
        # Chunk display options
        display_mode = st.radio(
            "Display Mode",
            ["Collapsed", "Expanded"],
            horizontal=True
        )
        
        for i, chunk in enumerate(st.session_state['chunks']):
            with st.expander(
                f"Chunk {i+1} ({chunk['tokens']} tokens) - {chunk['text'][:100]}...",
                expanded=(display_mode == "Expanded")
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Text")
                    st.text(chunk['text'])
                
                with col2:
                    st.subheader("Enriched Text")
                    st.text(chunk['enriched_text'])
                
                st.caption(f"Tokens: {chunk['tokens']} | Enriched: {chunk['enriched_tokens']}")
    
    # Embedding section
    if 'chunks' in st.session_state:
        st.header("🔗 Embedding & Storage")
        
        collection_name = st.text_input(
            "Collection Name",
            value="pdf_documents",
            help="Name for the ChromaDB collection"
        )
        
        if st.button("💾 Embed & Store Chunks", type="primary"):
            with st.spinner("Embedding chunks and storing in ChromaDB..."):
                success, message = embed_and_store_chunks(
                    st.session_state['chunks'],
                    collection_name,
                    embedding_model
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.session_state['collection_name'] = collection_name
                else:
                    st.error(f"❌ {message}")

def chat_tab():
    """Chat Tab"""
    st.header("💬 Chat with Your Document")
    
    if 'collection_name' not in st.session_state:
        st.warning("⚠️ Please embed a document first in the 'Chunking & Embedding' tab.")
        return
    
    # Collection selection
    collection_name = st.text_input(
        "Collection Name",
        value=st.session_state.get('collection_name', 'pdf_documents'),
        help="Name of the ChromaDB collection to search"
    )
    
    # Search options
    col1, col2 = st.columns(2)
    with col1:
        n_results = st.slider("Number of Results", 1, 10, 5)
    with col2:
        embedding_model = st.selectbox(
            "Embedding Model",
            ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "all-MiniLM-L12-v2"],
            help="Must match the model used for embedding"
        )
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your document..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Search for relevant chunks
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                results = search_collection(collection_name, prompt, n_results, embedding_model)
                
                if results and results['documents']:
                    # Display search results
                    st.markdown("**Relevant document sections:**")
                    
                    for i, (doc, metadata, distance) in enumerate(zip(
                        results['documents'][0],
                        results['metadatas'][0],
                        results['distances'][0]
                    )):
                        with st.expander(f"Result {i+1} (Similarity: {1-distance:.3f})", expanded=(i==0)):
                            st.text(doc)
                            st.caption(f"Chunk {metadata['index']} | Tokens: {metadata['tokens']}")
                    
                    # Simple response (in a real app, you'd use an LLM here)
                    response = f"I found {len(results['documents'][0])} relevant sections in your document. The most relevant section is shown above with a similarity score of {1-results['distances'][0][0]:.3f}."
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("No relevant sections found. Try a different query.")
                    st.session_state.messages.append({"role": "assistant", "content": "No relevant sections found. Try a different query."})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()