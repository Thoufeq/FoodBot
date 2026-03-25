---

#  FoodBot: AI-Powered PDF Cookbook Assistant

FoodBot is a high-performance **Retrieval-Augmented Generation (RAG)** chatbot. It transforms static cookbook PDFs into a dynamic, searchable, and conversational knowledge base using Pinecone and Google Gemini.

---

##  Key Features

### Dynamic Knowledge Management

* **On-the-Fly Indexing:** Upload any cookbook PDF to instantly expand the bot's expertise.
* **Semantic Search:** Uses HuggingFace embeddings to understand the *meaning* of your query, not just keywords.
* **Multi-Doc Support:** Index multiple books and query them all at once.

###  Intelligent Conversational AI

* **Context-Aware:** Gemini LLM generates responses based strictly on your uploaded recipes.
* **Memory-Enabled:** Remembers previous questions in the session for follow-up instructions.
* **Safety First:** Engineered to prioritize context over hallucinations.

###  Seamless User Experience

* **Real-Time Feedback:** Live progress bars for PDF chunking and vector embedding.
* **Modern UI:** Responsive design featuring streaming-style text animations and toast notifications.

---

##  System Architecture

The following flow represents the lifecycle of a user query and document ingestion:

**User Interface** → **Flask API** → **Document Processing** (LangChain) → **Vector Store** (Pinecone) → **LLM Synthesis** (Gemini) → **Structured Output**

---

##  Tech Stack

| Component | Technology |
| --- | --- |
| **Orchestration** | LangChain |
| **Backend** | Flask (Python) |
| **LLM** | Google Gemini |
| **Vector Database** | Pinecone |
| **Embeddings** | HuggingFace Transformers |
| **Frontend** | HTML5, CSS3, jQuery |

---

##  Project Structure

```text
project-root/
├── app.py                # Main Flask application & API routes
├── src/
│   ├── pdf_insertion.py  # PDF loading and semantic chunking logic
│   ├── store_index.py    # Pinecone vector synchronization
│   ├── embeddings.py     # HuggingFace model configuration
│   └── prompt.py         # System instructions & RAG templates
├── templates/            # UI components (chat.html)
├── static/               # Styling (style.css) & JS
├── data/pdfs/uploaded/   # Local storage for processed documents
└── README.md             # Project documentation

```

---

##  Installation & Setup

### 1. Environment Preparation

```bash
# Clone the repository
git clone <repo-url>
cd foodbot

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

```

### 2. Configuration

Create a `.env` file in the root directory:

```env
PINECONE_API_KEY=your_pinecone_key_here
GOOGLE_API_KEY=your_gemini_key_here

```

### 3. Launch

```bash
python app.py

```

Visit `http://localhost:8080` in your browser.

---

## How to Use

1. **Upload:** Click the PDF icon and select a cookbook. Wait for the **Indexing Progress Bar** to complete.
2. **Ask:** Use natural language to find recipes or tips.
* *"How do I make a classic lasagna?"*
* *"Give me three high-protein breakfast ideas from this book."*
* *"What is the baking temperature for the chocolate cake?"*



---

## Deep Dive: Core Components

* **`pdf_insertion.py`**: Handles the heavy lifting of splitting PDFs into manageable text chunks while preserving metadata for better retrieval.
* **`store_index.py`**: Manages the batch uploading process to Pinecone to ensure stability during large document processing.
* **`prompt.py`**: Contains the "personality" of FoodBot, ensuring it remains a helpful cooking assistant and doesn't invent recipes outside of the provided context.

---
