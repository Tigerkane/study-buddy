# Constitution — Last Minute Study Buddy

> The non-negotiable principles that guide every decision in this project.

---

## 1. Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend/UI | Streamlit (Python) | Fast to build, no separate frontend needed |
| AI | Ollama (local) — llama3 | Free, offline, no API key required |
| Database | MongoDB (local) | Schema-flexible, easy to set up, TTL support |
| PDF parsing | pdfplumber + pypdf | Best text extraction from PDFs |
| Language | Python 3.11+ | Single language across the whole app |

---

## 2. Core Principles

### 2.1 Zero Cost
The app must run entirely for free. No paid APIs, no cloud services, no subscriptions. Ollama runs locally; MongoDB runs locally.

### 2.2 Student-First UX
Every screen must be usable under exam pressure. No cluttered UI, no long onboarding. A student should be able to upload a PDF and get a response within 60 seconds.

### 2.3 Offline-First
The app must work without internet. Ollama + MongoDB + Streamlit all run on localhost. No external dependencies at runtime.

### 2.4 Two Modes Only
- **Chat** (default): conversational Q&A over the uploaded PDF
- **Quiz**: 20-question MCQ auto-generated from the PDF

No scope creep. Every feature must serve one of these two modes.

### 2.5 Single File App
`app.py` is the entire application. No separate backend server, no build step. `streamlit run app.py` is the only command needed.

---

## 3. Quality Standards

- Python code follows PEP8 (max line length 120)
- All Ollama prompts must return parseable output (JSON where structured data is needed)
- MongoDB operations wrapped in try/except — app must still work if Mongo is offline
- PDF extraction must handle both text-based and fallback gracefully
- No user data sent to any external server

---

## 4. Out of Scope

- User authentication / login
- Multi-user sessions
- Cloud deployment
- Mobile app
- Support for scanned/image-only PDFs (OCR is a bonus)
- Payments or subscriptions
