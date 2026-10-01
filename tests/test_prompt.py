import pytest
from src.chains.prompt import get_rag_prompt, DISEASE_PROMPT_TEMPLATE

def test_get_rag_prompt():
    """Test get_rag_prompt template generation and variable requirements."""
    prompt = get_rag_prompt()
    assert "context" in prompt.input_variables
    assert "input" in prompt.input_variables
    
    formatted = prompt.format(context="Konteks uji", input="Pertanyaan uji")
    assert "Konteks uji" in formatted
    assert "Pertanyaan uji" in formatted

def test_disease_prompt_template():
    """Test DISEASE_PROMPT_TEMPLATE structure and formatting."""
    assert "disease_name" in DISEASE_PROMPT_TEMPLATE.input_variables
    assert "context" in DISEASE_PROMPT_TEMPLATE.input_variables
    
    formatted = DISEASE_PROMPT_TEMPLATE.format(
        disease_name="kuning", 
        context="Infeksi Begomovirus"
    )
    assert "kuning" in formatted
    assert "Infeksi Begomovirus" in formatted
