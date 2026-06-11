# Plan — 001: Last Minute Study Buddy

**Stack:** Streamlit + Ollama + pdfplumber

---

## Architecture

```
┌─────────────────────────────┐
│      app.py (Streamlit)     │
│  ┌──────────┐ ┌───────────┐ │
│  │   Chat   │ │   Quiz    │ │
│  │   Mode   │ │   Mode    │ │
│  └────┬─────┘ └─────┬─────┘ │
└───────┼─────────────┼───────┘
        │             │
   ┌────▼─────────────▼────┐
   │   Ollama (localhost)  │
   │   llama3.2:3b /       │
   │   mistral:7b          │
   └───────────────────────┘
```

---

## Implementation Phases

- Phase 1 (0–3h): PDF upload + Ollama connection
- Phase 2 (3–6h): Chat mode with streaming
- Phase 3 (6–9h): Quiz mode with 10 MCQ
- Phase 4 (9–11h): Polish + error handling
- Phase 5 (11–12h): Demo prep
