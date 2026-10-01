import pytest
from langchain_core.documents import Document
from src.ingestion.chunker import split_documents

def test_split_documents_basic():
    """Test splitting documents into chunks with specified size and overlap."""
    sample_text = (
        "Tanaman cabai yang terserang penyakit kuning harus ditangani dengan baik. "
        "Penyebab utamanya adalah Begomovirus yang ditularkan oleh kutu kebul. "
        "Pengendalian dapat dilakukan dengan rotasi tanaman dan penggunaan pestisida organik."
    )
    docs = [Document(page_content=sample_text, metadata={"source": "test_doc"})]
    
    chunks = split_documents(docs, chunk_size=100, chunk_overlap=20)
    
    assert len(chunks) > 0
    assert isinstance(chunks[0], Document)
    assert chunks[0].metadata["source"] == "test_doc"

def test_split_documents_empty():
    """Test splitting an empty list of documents."""
    chunks = split_documents([], chunk_size=100, chunk_overlap=20)
    assert len(chunks) == 0
