from fastapi import FastAPI, UploadFile, Form
import chromadb
import pypdf
import ollama
import os

app = FastAPI()

# Conectar a Chroma (en modo server)
chroma_client = chromadb.HttpClient(host="chroma", port=8000)
collection = chroma_client.get_or_create_collection("RAG")


def upload_pdf_to_chroma(file_path: str):
    with open(file_path, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                collection.add(
                    documents=[text],
                    ids=[f"{os.path.basename(file_path)}-{i}"]
                )

@app.post("/upload")
async def upload(file: UploadFile):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    upload_pdf_to_chroma(file_path)
    return {"status": "uploaded", "file": file.filename}

@app.post("/query")
async def query(question: str = Form(...)):
    closestPages = collection.query(
        query_texts=[question],
        n_results=3
    )
    context = "\n\n".join(closestPages["documents"][0])

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": f"Use the context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return {"answer": response["message"]["content"]}
