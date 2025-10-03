import requests

BACKEND_URL = "http://localhost:8001"

# 1. Subir PDF
def upload_pdf(file_path):
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
    print("Upload response:", response.status_code, response.json())

# 2. Hacer una consulta
def query(question):
    data = {"question": question}
    response = requests.post(f"{BACKEND_URL}/query", data=data)
    print("Query response:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    # 👇 Ajusta el nombre del PDF a uno que tengas en tu proyecto
    upload_pdf("mamiferos.pdf")

    # 👇 Pregunta de ejemplo
    query("Qué son los mamíferos?")
