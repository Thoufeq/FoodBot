import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from src.embeddings import download_embeddings
from src.pdf_insertion import pdf_to_documents


def initialize_pinecone():
    load_dotenv()
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "cooking-assistant-unified"

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("✅ Pinecone index created")
    else:
        print("✅ Using existing Pinecone index")

    return index_name


def store_documents(documents, batch_size=100):
    embeddings = download_embeddings()
    index_name = initialize_pinecone()

    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

    total = len(documents)
    for i in range(0, total, batch_size):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
        print(f"⬆ Uploaded {min(i + batch_size, total)}/{total}")


if __name__ == "__main__":
    pdf_folder = "data/pdfs/uploaded"
    all_docs = []

    for file in os.listdir(pdf_folder):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file)
            all_docs.extend(pdf_to_documents(pdf_path))

    store_documents(all_docs)
    print("🎉 All PDFs indexed successfully!")