# User Manual — Last Minute Study Buddy

## What is this?
Last Minute Study Buddy is a local AI-powered app that lets you upload your lecture notes (PDF) and either chat with them or take a quiz — all for free, with no internet required.

---

## Requirements
- Python 3.11 or 3.12
- Ollama installed and running
- A PDF of your study notes

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Starting the App

**Step 1 — Start Ollama**
```bash
ollama serve
```

**Step 2 — Run the app**
```bash
python -m streamlit run app.py
```

**Step 3 — Open in browser**
```
http://localhost:8501
```

---

## How to Use

### Upload a PDF
1. Look at the left sidebar
2. Click **"Drop your PDF here"**
3. Select your lecture notes or textbook chapter
4. Wait for the green ✅ confirmation

### Chat Mode (Default)
1. After uploading, you'll be in **Chat** mode
2. Use the **Quick Prompt** buttons for instant summaries
3. Or type your own question in the text box and click **Send →**
4. The AI will answer based only on your uploaded notes

### Quiz Mode
1. In the sidebar, click **📝 Quiz**
2. Click **⚡ Generate 10 Questions**
3. Wait 2–4 minutes for questions to generate
4. Answer all questions using the radio buttons
5. Click **✅ Submit Quiz**
6. See your score, percentage, grade, and full answer review

### Switching Models
In the sidebar under **Model**, choose:
- `llama3.2:3b` — Faster, uses less memory
- `mistral:7b` — Slower, better quality answers

---

## Troubleshooting

| Problem | Fix |
|---|---|
| App won't start | Run `pip install -r requirements.txt` first |
| No response from AI | Make sure `ollama serve` is running |
| PDF shows no text | PDF may be scanned/image-only — use a text-based PDF |
| Quiz takes too long | Normal on CPU — wait 2–4 minutes or use `llama3.2:3b` |
| Port already in use | Ollama is already running — skip `ollama serve` |
