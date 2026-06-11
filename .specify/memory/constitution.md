# Constitution — Last Minute Study Buddy

> The non-negotiable principles that guide every decision in this project.

---

## 1. Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend/UI | Streamlit (Python) | Fast to build, single file |
| AI | Ollama (local) — llama3.2:3b / mistral:7b | Free, offline, no API key |
| PDF parsing | pdfplumber + pypdf | Best text extraction |
| Language | Python 3.12+ | Single language across whole app |

---

## 2. Core Principles

### 2.1 Zero Cost
No paid APIs, no cloud services, no subscriptions. Ollama runs locally.

### 2.2 Student-First UX
Upload a PDF → get a response within 60 seconds. No cluttered UI.

### 2.3 Offline-First
Everything runs on localhost. No internet required at runtime.

### 2.4 Two Modes Only
- **Chat** (default): conversational Q&A over the uploaded PDF
- **Quiz**: 10-question MCQ auto-generated from the PDF

### 2.5 Single File App
`app.py` is the entire application. `streamlit run app.py` is the only command.

---

## 3. Out of Scope
- User authentication / login
- Cloud deployment
- Scanned/image-only PDFs
- Payments or subscriptions
