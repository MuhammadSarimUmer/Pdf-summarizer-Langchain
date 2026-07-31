<div align="center">

# 📄 PDF Summarizer — LangChain

### Upload a short PDF, get a clean summary and key points back — powered by Groq.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Pipeline-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM_Inference-F55036?style=for-the-badge&logo=lightning&logoColor=white)](https://groq.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Structured_Output-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

</div>

---

## ⚠️ Short PDFs Only

This tool reads a PDF and sends its text straight to the LLM in a single request — there's no chunking, splitting, or multi-pass summarization. It works best on **short documents** (a few pages), this project isn't built long PDF's yet — you'd want a chunk-and-combine summarization pipeline instead.

---

## ✨ What It Does

- 📤 Upload a PDF through a simple API endpoint
- 🧠 Choose between two Groq models — a fast one or a more powerful one
- 📋 Get back a structured JSON response with:
  - A short overall **summary** (3–6 sentences)
  - A list of **3–5 key points**
- 🔁 Automatically retries once if the model's output doesn't match the expected format

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **API Framework** | FastAPI |
| **PDF Reading** | LangChain `PyPDFLoader` |
| **LLM Inference** | Groq API |
| **Output Validation** | Pydantic + `PydanticOutputParser` |
| **Orchestration** | LangChain |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MuhammadSarimUmer/Pdf-summarizer-Langchain.git
cd Pdf-summarizer-Langchain
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn python-dotenv langchain-core langchain-groq langchain-community pypdf
```

### 3. Set your Groq API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_actual_key_here
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

---

## 📡 Usage

**Endpoint:** `POST /summarize`

**Query parameter:**
- `model_choice` — `fast` (Llama 8B) or `powerful` (Llama 70B). Defaults to `fast`.

**Body:** `multipart/form-data` with a `file` field containing your PDF.

**Example (curl):**

```bash
curl -X POST "http://127.0.0.1:8000/summarize?model_choice=fast" \
  -F "file=@your_document.pdf"
```

**Example response:**

```json
{
  "summary": "The document outlines...",
  "key_points": [
    "Point one",
    "Point two",
    "Point three"
  ]
}
```

---

## 📂 Project Structure

```
Pdf-summarizer-Langchain/
└── main.py
```

---

<div align="center">

Made with ☕ by **Muhammad Sarim Umer**

</div>
