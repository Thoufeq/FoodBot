from langchain_community.embeddings import HuggingFaceEmbeddings



# ---------- EMBEDDINGS ----------
def download_embeddings():
    """
    Loads HuggingFace MiniLM embeddings (384D).
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print("✅ HuggingFace embeddings model loaded.")
    return embeddings
