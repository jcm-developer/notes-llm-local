# 🦙 Notes-LLM Local con Ollama + Chroma + Backend

Este proyecto levanta un entorno local con [Ollama](https://ollama.com/), [ChromaDB](https://www.trychroma.com/) y un backend en FastAPI/Flask para hacer consultas a documentos PDF usando modelos LLaMA.

---

## 🚀 Pasos de instalación y arranque

### 1. Arrancar solo Ollama
Levanta únicamente el servicio de Ollama:
```bash
docker compose up -d ollama
```

Verifica que está escuchando en el puerto **11434**:
```bash
docker compose logs -f ollama
```
(Sal de los logs con `Ctrl + C` cuando veas algo como `listening on 0.0.0.0:11434`).

---

### 2. Descargar el modelo (solo una vez)
Descarga el modelo que utilizará el backend:
```bash
docker compose exec ollama ollama pull llama3.1:8b
```

Si ese modelo no existe en tu versión de Ollama, prueba con:
```bash
docker compose exec ollama ollama pull llama3.1:8b-instruct
```

Comprueba que se descargó correctamente:
```bash
docker compose exec ollama ollama list
```

Deberías ver en la lista `llama3.1:8b` o `llama3.1:8b-instruct`.

---

### 3. Arrancar Chroma
Levanta el servicio de Chroma:
```bash
docker compose up -d chroma
```

Verifica que está corriendo en el puerto **8000**:
```bash
docker compose logs -f chroma
```

---

### 4. Arrancar el backend
Levanta el backend (FastAPI/Flask):
```bash
docker compose up -d --build backend
```

> ⚠️ Usa `--build` la primera vez o si cambiaste el Dockerfile del backend.

Verifica los logs:
```bash
docker compose logs -f backend
```

Si todo va bien, deberías ver que expone `http://0.0.0.0:8001`.

---

### 5. Probar el endpoint
#### Desde PowerShell
Si el endpoint `/query` espera **form-data/x-www-form-urlencoded**:
```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:8001/query `
  -Body @{ question = "Qué son los animales?" } `
  -ContentType 'application/x-www-form-urlencoded'
```

#### Desde Python
Usa el cliente de ejemplo:
```bash
py test_client.py
```

---

## ⚙️ Configuración de modelos

Si tu backend **usa un nombre exacto de modelo** (ejemplo `llama3.1:8b`) y el que descargaste fue `llama3.1:8b-instruct`, tienes dos opciones:

1. Cambiar el nombre en el código del backend.  
2. Definir una variable de entorno en `docker-compose.yml`:

```yaml
environment:
  OLLAMA_HOST: http://ollama:11434
  OLLAMA_MODEL: llama3.1:8b-instruct
  CHROMA_HOST: http://chroma:8000
```

Y reconstruir:
```bash
docker compose up -d --build backend
```

---

## 🔎 Depuración

Para ver logs en tiempo real:
```bash
docker compose logs -f ollama
docker compose logs -f chroma
docker compose logs -f backend
```

---

## ✅ Resumen rápido

1. `docker compose up -d ollama`  
2. `docker compose exec ollama ollama pull llama3.1:8b` *(o `:8b-instruct`)*  
3. `docker compose up -d chroma`  
4. `docker compose up -d --build backend`  
5. Probar en `http://localhost:8001/query`
