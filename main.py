import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

app = FastAPI(
    title="Configurable PDF Summarizer API",
    description="Upload a PDF and select which Groq model you want to summarize it with.",
    version="1.0"
)


class SummaryResponse(BaseModel):
    summary: str = Field(..., description="A clear, overall summary of the document in 3-6 sentences")
    key_points: list[str] = Field(..., description="Top 3-5 bullet points extracted from the text")


MODEL_MAPPING = {
    "fast": "llama-3.1-8b-instant",
    "powerful": "llama-3.3-70b-versatile"
}

MAX_CHARS = 15000
MAX_RETRIES = 2

parser = PydanticOutputParser(pydantic_object=SummaryResponse)


def build_chain(model_id: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an expert document summarizer. Analyze the document text provided by the user "
         "and respond with ONLY a single JSON object, no other text, matching this exact schema:\n"
         "{format_instructions}\n\n"
         "Always return a single overall 'summary' string describing what the document is and "
         "what it covers, plus a 'key_points' list of 3-5 short bullet strings highlighting the "
         "most important themes, topics, or takeaways. This applies even if the document itself "
         "contains questions, tables, code, or structured data — describe and summarize that "
         "content in prose, do not mirror its internal structure."),
        ("user", "Document content:\n\n{text}")
    ]).partial(format_instructions=parser.get_format_instructions())

    llm = ChatGroq(model=model_id, temperature=0.2, model_kwargs={"response_format": {"type": "json_object"}})
    return prompt | llm | parser


@app.post("/summarize", summary="Upload a PDF and choose a model configuration")
async def summarize_pdf(
    file: UploadFile = File(...),
    model_choice: str = Query("fast", description="Choose 'fast' (Llama 8B) or 'powerful' (Llama 70B)")
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    selected_model_id = MODEL_MAPPING.get(model_choice.lower())
    if not selected_model_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid model choice. Please choose either 'fast' or 'powerful'."
        )

    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())

    try:
        loader = PyPDFLoader(temp_filename)
        pages = loader.load()
        full_text = "\n".join([page.page_content for page in pages])

        if not full_text.strip():
            raise HTTPException(status_code=400, detail="The uploaded PDF is empty or unreadable.")

        if len(full_text) > MAX_CHARS:
            full_text = full_text[:MAX_CHARS]

        chain = build_chain(selected_model_id)

        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                result = chain.invoke({"text": full_text})
                return result
            except (ValidationError, Exception) as e:
                last_error = e
                continue

        raise HTTPException(
            status_code=500,
            detail=f"An error occurred after {MAX_RETRIES} attempts: {str(last_error)}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)