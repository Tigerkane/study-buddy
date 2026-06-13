# 📚 Last Minute Study Buddy

> AI-powered study assistant — upload your notes, chat with them, or take a quiz. Free, fast, multilingual.

🔗 **Live Demo:** https://study-buddy-zofymbvuwfwcuyp8bsjzsm.streamlit.app/

---

## ✨ Features

- 📄 **PDF Upload** — upload any lecture notes or textbook chapter
- 💬 **Chat Mode** — ask anything about your notes, get instant AI responses
- 📝 **Quiz Mode** — auto-generate 10 MCQ questions from your notes
- 🌐 **3 Languages** — English, हिंदी (Hindi), తెలుగు (Telugu)
- 🤖 **2 AI Models** — Llama 3.3 (fast) and Llama 3.1 (powerful)
- 📊 **Score Review** — see your score, percentage, grade and answer review

---

## 🚀 Quick Start (Cloud)

1. Open **https://study-buddy-zofymbvuwfwcuyp8bsjzsm.streamlit.app/**
2. Get a free Groq API key from **console.groq.com**
3. Paste it in the sidebar under **🔑 Groq API Key**
4. Upload your PDF and start studying!

---

## 🖥️ Run Locally (Ollama)

### Requirements
- Python 3.11 or 3.12
- Ollama installed from **ollama.com**

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download AI model (do this before hackathon — 2GB download)
ollama pull llama3.2:3b

# Start Ollama
ollama serve

# Run the app
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| AI (Cloud) | Groq API (Llama 3.3, Llama 3.1) |
| AI (Local) | Ollama (llama3.2:3b, mistral:7b) |
| PDF Parsing | pdfplumber + pypdf |
| Language | Python 3.12 |

---

## 👥 Team

- **Sai Chaitanya** — @Saichaitanya9
- **Shreyas Mogalapalli** — @ShreyasMogalapalli

---

## 📁 Project Structure

```
study-buddy/
│   .dockerignore
│   .editorconfig
│   .env.example
│   .gitignore
│   .gitlab-ci.yml
│   .pre-commit-config.yaml
│   AGENTS.md
│   app.py
│   CHANGELOG.md
│   cliff.toml
│   CODE_OF_CONDUCT.md
│   CONTRIBUTING.md
│   Dockerfile
│   git
│   LICENSE
│   README.md
│   requirements.txt
│   SECURITY.md
│   USER_MANUAL.md
│
├───.gitlab
│   ├───issue_templates
│   │       bug.md
│   │
│   └───merge_request_templates
│           default.md
│
├───.specify
│   │   settings.yml
│   │
│   ├───memory
│   │       constitution.md
│   │
│   └───templates
│           feature.md
│           plan-template.md
│           spec-template.md
│           tasks-template.md
│
├───.streamlit
│       config.toml
│       secrets.toml
│
├───docs
│   └───specs
│       │   constitution.md
│       │
│       └───001-study-buddy
│           │   data-model.md
│           │   plan.md
│           │   spec.md
│           │   tasks.md
│           │
│           └───contracts
│                   api-contracts.md
│
├───specs
│   │   constitution.md
│   │
│   └───001-study-buddy
│       │   plan.md
│       │   spec.md
│       │   tasks.md
│       │
│       └───contracts
│               api-contracts.md
│
└───tests
        test_app.py

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

---

## 📜 License

Licensed under **AGPLv3** — see [LICENSE](LICENSE) for details.