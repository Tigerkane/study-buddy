# 📚 Last Minute Study Buddy

Upload a PDF → Chat with your notes or take a 20-question quiz. Powered by Ollama (free, local AI) + MongoDB.

---

## ⚡ Setup (5 minutes)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install & start Ollama
```bash
# Install Ollama from https://ollama.com
ollama pull llama3      # download model (~4GB, do this before the hackathon!)
ollama serve            # start the Ollama server
```

### 3. Start MongoDB
```bash
# If using MongoDB locally:
mongod --dbpath ./data

# Or use Docker:
docker run -d -p 27017:27017 mongo
```

### 4. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🧑‍💻 Team Split (2 people, <12 hours)

| Person A (Frontend/UX) | Person B (Backend/AI) |
|---|---|
| Improve CSS/styling | Tune Ollama prompts |
| Add tab for past quiz scores | Add chat history from MongoDB |
| Mobile responsiveness | Better PDF chunking for large files |
| Loading animations | Handle scanned PDFs with OCR |

---

## 🗂 MongoDB Collections

- `studybuddy.chats` — all chat messages with timestamps
- `studybuddy.quiz_results` — quiz scores per session

---

## ⚙️ Config

Edit the top of `app.py`:
```python
OLLAMA_MODEL = "llama3"    # or "mistral", "phi3", etc.
MONGO_URI = "mongodb://localhost:27017"
```
