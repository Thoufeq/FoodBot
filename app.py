import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory

from src.pdf_insertion import pdf_to_documents
from src.store_index import store_documents
from src.embeddings import download_embeddings
from src.prompt import prompt


# =========================
# App Setup
# =========================
app = Flask(__name__)
load_dotenv()

UPLOAD_FOLDER = "data/pdfs/uploaded"
ALLOWED_EXTENSIONS = {"pdf"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# Vector Store
# =========================
embeddings = download_embeddings()

vectorstore = PineconeVectorStore.from_existing_index(
    index_name="cooking-assistant-unified",
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


# =========================
# LLM
# =========================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    return_messages=True
)

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)


# =========================
# Helpers
# =========================
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_recipe_query(user_msg: str) -> bool:
    recipe_intents = [
        "recipe",
        "ingredients",
        "steps",
        "method",
        "how to cook",
        "how do i make",
        "instructions",
        "preheat",
        "bake",
        "fry",
        "boil",
        "serve",
        "servings"
    ]
    msg = user_msg.lower()
    return any(intent in msg for intent in recipe_intents)


# =========================
# Routes
# =========================
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["msg"]

    response = rag_chain.invoke({
        "input": user_msg,
        "chat_history": memory.load_memory_variables({})["chat_history"]
    })

    answer = response.get("answer", "")

    retrieved_docs = response.get("context", [])

    # ✅ Show sources ONLY if:
    # 1. User explicitly asked a recipe-related question
    # 2. Pinecone actually returned documents
    if is_recipe_query(user_msg) and retrieved_docs:
        sources = {
            doc.metadata.get("source_name")
            for doc in retrieved_docs
            if doc.metadata.get("source_name")
        }

        if sources:
            answer += f"\n\n**Source:** {', '.join(sorted(sources))}"

    memory.save_context(
        {"input": user_msg},
        {"output": answer}
    )

    return answer


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return "⚠️ No file received", 400

    file = request.files["pdf"]

    if file.filename == "":
        return "⚠️ No file selected", 400

    if not allowed_file(file.filename):
        return "⚠️ Only PDF files are allowed", 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    try:
        # 1️⃣ Chunk PDF
        documents = pdf_to_documents(save_path)

        # 2️⃣ Store in Pinecone
        store_documents(documents)

        return (
            f"✅ **{filename}** uploaded and indexed successfully!\n"
            "You can now ask questions from this cookbook."
        )

    except Exception as e:
        print("PDF processing error:", e)
        return "⚠️ Failed to process PDF", 500


# =========================
# Run
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=8080)