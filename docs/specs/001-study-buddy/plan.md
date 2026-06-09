# Plan — 001: Last Minute Study Buddy

**Branch:** `001-study-buddy-mvp`  
**Stack Decision:** Streamlit + Ollama (llama3) + MongoDB + pdfplumber

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   app.py (Streamlit)                │
│                                                     │
│  ┌──────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │ Sidebar  │   │  Chat Mode   │   │  Quiz Mode  │ │
│  │ PDF      │   │  Streaming   │   │  20 MCQ     │ │
│  │ Upload   │   │  Q&A         │   │  + Review   │ │
│  │ Mode     │   │              │   │             │ │
│  │ Toggle   │   └──────┬───────┘   └──────┬──────┘ │
│  └──────────┘          │                  │        │
└───────────────────────┬┴──────────────────┘────────┘
                        │
          ┌─────────────┴──────────────┐
          │                            │
   ┌──────▼──────┐              ┌──────▼──────┐
   │   Ollama    │              │   MongoDB   │
   │  (llama3)   │              │  (local)    │
   │  localhost  │              │  localhost  │
   │  :11434     │              │  :27017     │
   └─────────────┘              └─────────────┘
```

---

## File Structure

```
study-buddy/
├── app.py                  # Entire application (single file)
├── requirements.txt        # Python dependencies
├── README.md               # Setup instructions
├── Dockerfile              # Optional containerization
├── .gitlab-ci.yml          # CI/CD pipeline
├── tests/
│   ├── test_pdf.py         # PDF extraction tests
│   ├── test_quiz.py        # Quiz JSON parsing tests
│   └── test_mongo.py       # MongoDB connection tests
└── docs/
    └── specs/              # SpecKit documents
```

---

## Technology Decisions

### Why Streamlit?
- Single Python file = perfect for a 2-person hackathon
- No separate React/Node frontend to manage
- Built-in file uploader, state management, streaming support
- Deploy with one command

### Why Ollama (not OpenAI)?
- Zero cost — runs on local GPU/CPU
- No API key needed
- `llama3` is strong enough for summarisation and MCQ generation
- Works offline on venue WiFi

### Why MongoDB?
- Schema-flexible — no migrations needed during hackathon
- TTL index built-in (can auto-expire old sessions)
- Easy local setup with `mongod` or Docker
- `pymongo` is simple and well-documented

### Why pdfplumber?
- Better layout-aware text extraction than PyPDF alone
- Handles multi-column PDFs
- Pure Python, no system dependencies beyond Poppler

---

## Implementation Phases

### Phase 1 — Core (0–3 hrs)
- [ ] PDF upload + text extraction
- [ ] Ollama ping check on startup
- [ ] MongoDB connect (with graceful fallback)
- [ ] Basic Streamlit layout + sidebar

### Phase 2 — Chat Mode (3–6 hrs)
- [ ] Prompt builder with PDF context + history
- [ ] Streaming response from Ollama
- [ ] Chat history in session state
- [ ] Save messages to MongoDB
- [ ] Quick prompt buttons

### Phase 3 — Quiz Mode (6–9 hrs)
- [ ] Generate 20 MCQ via Ollama
- [ ] JSON parsing with error recovery
- [ ] Render questions with radio buttons
- [ ] Progress bar + submit validation
- [ ] Score screen + answer review
- [ ] Save quiz result to MongoDB

### Phase 4 — Polish (9–11 hrs)
- [ ] Custom CSS (dark theme)
- [ ] Error states (scanned PDF, Ollama down, Mongo down)
- [ ] Loading spinners
- [ ] Mobile responsiveness check

### Phase 5 — Demo Prep (11–12 hrs)
- [ ] Test with 3 different PDFs
- [ ] Record demo video / screenshots
- [ ] Prepare 2-minute pitch

---

## Constitution Check

| Principle | Satisfied? | Notes |
|---|---|---|
| Zero Cost | ✅ | Ollama local, MongoDB local, no APIs |
| Student-First UX | ✅ | Single upload → immediate value |
| Offline-First | ✅ | Everything on localhost |
| Two Modes Only | ✅ | Chat + Quiz, nothing else |
| Single File App | ✅ | `streamlit run app.py` |
