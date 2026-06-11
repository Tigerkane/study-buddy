# Constitution — Last Minute Study Buddy

> The non-negotiable principles that guide every decision in this project.

---

## 1. Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend/UI | Streamlit (Python) | Fast to build, no separate frontend needed |
| AI | Ollama (local) — llama3.2:3b / mistral:7b | Free, offline, no API key required |
| PDF parsing | pdfplumber + pypdf | Best text extraction from PDFs |
| Language | Python 3.12+ | Single language across the whole app |

---

## 2. Core Principles

### 2.1 Zero Cost
The app must run entirely for free. No paid APIs, no cloud services, no subscriptions.

### 2.2 Student-First UX
Every screen must be usable under exam pressure. A student should be able to upload a PDF and get a response within 60 seconds.

### 2.3 Offline-First
The app must work without internet. Ollama + Streamlit all run on localhost.

### 2.4 Two Modes Only
- **Chat** (default): conversational Q&A over the uploaded PDF
- **Quiz**: 10-question MCQ auto-generated from the PDF

### 2.5 Single File App
`app.py` is the entire application. `streamlit run app.py` is the only command needed.

---

## 3. Out of Scope
- User authentication / login
- Cloud deployment
- Support for scanned/image-only PDFs
- Payments or subscriptions
