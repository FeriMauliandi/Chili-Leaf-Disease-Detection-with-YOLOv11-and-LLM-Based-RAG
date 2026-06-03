import os
from langchain_huggingface import HuggingFaceEmbeddings
import torch


model_name = "LazarusNLP/all-indo-e5-small-v4"

def get_embedding_model(model_name: str = model_name):
    print(f"Mempersiapkan model embedding: {model_name}")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware yang digunakan untuk embedding: {device.upper()}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': True} 
    )
    
    return embeddings