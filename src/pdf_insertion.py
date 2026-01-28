import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def pdf_to_documents(pdf_path, chunk_size=800, chunk_overlap=100):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(pages)

    pdf_name = os.path.basename(pdf_path)

    documents = []
    for i, chunk in enumerate(chunks):
        documents.append(
            Document(
                page_content=chunk.page_content,
                metadata={
                    "source_type": "pdf",
                    "source_name": pdf_name,
                    "page": chunk.metadata.get("page"),
                    "chunk_id": i
                }
            )
        )

    print(f"✅ Created {len(documents)} PDF chunks from {pdf_name}")
    return documents