📚 Last Minute Study Buddy
> AI-powered study assistant — upload your notes, chat with them, generate a quiz, or revise with flashcards. Free, fast, multilingual, and works offline.
🔗 Live Demo: https://study-buddy-zofymbvuwfwcuyp8bsjzsm.streamlit.app/
---
✨ Features
📄 Multi-PDF Upload — upload one or more lecture notes / textbook chapters at once
💬 Chat Mode — ask anything about your notes, get instant streamed AI responses
📝 Quiz Mode — auto-generate 10 MCQ questions, with Easy / Medium / Hard difficulty
🃏 Flashcards — auto-generated revision cards with a smooth 3D flip animation
📑 Section Selector — for long PDFs, pick which ~4000-character section to focus on
📖 Full-Document Mode (optional) — let Llama 3.3 70B (Groq) read the entire document at once instead of section-by-section
🌐 3 Languages — English, हिंदी (Hindi), తెలుగు (Telugu) — fully localized UI
🤖 Dual AI Backend — ☁️ Groq Cloud (BYOK) or 🖥️ Ollama Local (offline, private, free)
📥 Downloads — export your chat history or quiz report as a `.txt` file
📊 Score Review — see your score, percentage, grade, and full answer review after each quiz
---
🚀 Quick Start (Cloud)
Open https://study-buddy-zofymbvuwfwcuyp8bsjzsm.streamlit.app/
Get a free Groq API key from console.groq.com (starts with `gsk_`)
Paste it in the sidebar under 🔑 Groq API Key (BYOK)
Upload your PDF(s) and start studying!
---
🖥️ Run Locally (Ollama — fully offline)
Requirements
Python 3.11 or 3.12
Ollama installed from ollama.com
Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download AI model (do this once — ~2GB download)
ollama pull llama3.2:3b

# Start Ollama
ollama serve

# Run the app
python -m streamlit run app.py
```
Open http://localhost:8501 in your browser. Switch the sidebar AI Backend toggle to 🖥️ Ollama (Local) — no internet or API key required, and no data ever leaves your machine.
---
🛠️ Tech Stack
Layer	Technology
UI / Backend	Streamlit (Python, single file)
AI (Cloud)	Groq API — Llama 3.3 70B, Llama 3.1 8B (BYOK)
AI (Local)	Ollama — llama3.2:3b, mistral:7b
PDF Parsing	pdfplumber + pypdf
Language	Python 3.12
CI/CD	GitLab CI (lint, format, type-check, security, test, coverage)
Deployment	Streamlit Cloud
---
🤖 Agent Architecture (ADK-Aligned)
Our AI orchestration follows agentic design principles aligned with Google's Agent Development Kit (ADK) pattern — instructions, tool-use, reasoning loops, and memory:
Tutor Agent — handles Chat Mode: defined instructions ("answer only from provided notes, respond in the selected language"), tool: PDF context retrieval (section-based or full-document), reasoning loop: streamed multi-turn conversation with memory (session-based chat history, last 6 exchanges).
Quiz Generator Agent — handles Quiz Mode: defined instructions (generate valid JSON MCQs at the selected difficulty), tool-use capability: structured output parsing with retry-based self-correction (up to 3 attempts), memory: tracks quiz state across the user session.
Flashcard Agent — handles Flashcard Mode: generates front/back revision cards from the active document section, with the same structured-output and retry pattern as the Quiz Generator.
Backend Router — dynamically selects the inference tool (Groq cloud API or Ollama local) and context strategy (chunked section vs. full document) based on user preference and model capability.
Why not the full Google ADK SDK: Given the hackathon timeline, we implemented the same architectural pattern (instructions + tools + reasoning loop + memory) directly in Python rather than adopting the full `google-adk` dependency. This keeps the app lightweight and deployable on Streamlit Cloud's free tier. Migrating to ADK for true multi-agent orchestration is our next planned milestone.
---
📑 How Long Documents Are Handled
AI models have a limited context window, so we don't send an entire PDF on every request by default:
Section mode (default): the document is split into ~4000-character sections. Use the sidebar dropdown to pick which section to study, chat about, quiz on, or make flashcards from. Works with every model/backend.
Full-document mode (optional toggle): when using Groq's `llama-3.3-70b-versatile` model — which has a ~128K token context window — you can toggle "📖 Read entire document" to send up to 100,000 characters in one request. This option is only shown for models that can actually support it; smaller models (Ollama, Llama 3.1 8B) always use section mode to avoid errors or truncated output.
---
🌐 Internationalization & Localization
UI (i18n/l10n): every button, label, error message, and helper string is fully translated across English, Hindi, and Telugu via a `UI_TEXT` dictionary, switched live from the sidebar with no page reload.
AI output language: the app instructs the AI model to respond in the selected language. This works reliably with larger models (Llama 3.3 70B) but is best-effort with smaller local models, which may sometimes default to English regardless of the instruction.
---
👥 Team
Sai Chaitanya
Shreyas Mogalapalli — College ID: 24STUCHH010183
---
📁 Project Structure
```
study-buddy/
├── app.py                  ← Main Streamlit app (Groq + Ollama, all features)
├── requirements.txt        ← Python dependencies
├── Dockerfile               ← Container setup
├── .gitlab-ci.yml           ← CI/CD pipeline
├── .pre-commit-config.yaml  ← Local pre-commit hooks
├── specs/                  ← SpecKit documentation
│   ├── constitution.md
│   └── 001-study-buddy/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── contracts/
├── tests/
│   └── test_app.py
└── .specify/               ← SpecKit config
```
---
🧪 Run Tests
```bash
pytest tests/ -v
```
---
⚠️ Known Limitations
No OCR — scanned/image-based PDFs won't extract text (text-based PDFs only)
No persistent storage — chat history, quiz results, and flashcards reset on page refresh (no database; download buttons let you export before refreshing)
No source citation — chat answers don't point to the specific page/line they came from
Context limit in section mode — each request covers ~4000 characters unless full-document mode is enabled
AI output language is best-effort — smaller local models may not reliably follow the "respond in Hindi/Telugu" instruction
These are documented as future-work items rather than hidden — see Roadmap below.
---
🗺️ Roadmap
OCR support for scanned notes (Tesseract/PaddleOCR)
Retrieval-Augmented Generation (RAG) for smarter long-document search
Persistent chat/quiz history via a lightweight database
Source citation (page/line references) in chat answers
Additional Indic languages (Tamil, Kannada, Marathi)
Native mobile app
---
📜 License
Licensed under AGPLv3 — see LICENSE for details.