# Contracts — 001: Last Minute Study Buddy

---

## Ollama API Contract

**Endpoint:** `POST http://localhost:11434/api/generate`

### Chat (streaming)

**Request:**
```json
{
  "model": "llama3",
  "prompt": "<full prompt string>",
  "stream": true
}
```

**Response stream** (newline-delimited JSON):
```json
{ "response": "token", "done": false }
{ "response": "token", "done": false }
{ "response": "", "done": true }
```

**Error handling:**
- Connection refused → show: *"Ollama not running. Run: `ollama serve`"*
- Timeout (>120s) → show: *"Response timed out. Try a shorter question."*

---

### Quiz Generation (non-streaming)

**Request:**
```json
{
  "model": "llama3",
  "prompt": "<quiz prompt>",
  "stream": false
}
```

**Expected response text** (raw, before parsing):
```
[
  {
    "q": "What is a binary search tree?",
    "options": ["A) A tree with...", "B) A list...", "C) A graph...", "D) A stack..."],
    "answer": "A"
  },
  ...
]
```

**Parsing strategy:**
1. Strip ` ```json ` and ` ``` ` fences
2. Find first `[` and last `]`
3. `json.loads()` the slice
4. Validate each item has `q`, `options` (len 4), `answer` (A–D)
5. Truncate to 20 if more than 20 returned

**Error handling:**
- JSON parse error → show: *"Quiz generation failed. Click Regenerate to try again."*
- Fewer than 5 questions returned → show same error

---

## MongoDB Contract

**Connection:** `mongodb://localhost:27017`  
**Database:** `studybuddy`

### Insert chat message
```python
db.chats.insert_one({
    "session_id": str,      # e.g. "s_1717900000"
    "filename":   str,      # e.g. "notes.pdf"
    "role":       str,      # "user" | "assistant"
    "message":    str,
    "timestamp":  datetime  # UTC
})
```

### Fetch chat history
```python
db.chats.find(
    {"session_id": session_id},
    {"_id": 0}
).sort("timestamp", 1)
```

### Insert quiz result
```python
db.quiz_results.insert_one({
    "session_id": str,
    "filename":   str,
    "score":      int,
    "total":      int,      # always 20
    "percent":    int,      # 0–100
    "timestamp":  datetime
})
```

**Graceful degradation:** All MongoDB operations wrapped in `try/except`. If MongoDB is down, the app continues to work using `st.session_state` only. A status indicator in the sidebar shows: 🟢 Connected / 🟡 Offline.

---

## PDF Extraction Contract

**Input:** `UploadedFile` (Streamlit file object)  
**Output:** `str` (extracted plain text) or `None`

**Strategy:**
1. Try `pdfplumber` — best for layout-aware extraction
2. Fallback to `pypdf` if pdfplumber fails
3. Return `None` if both fail or text < 100 chars

**Limits:**
- Max text sent to Ollama: 5000 chars (quiz), 4000 chars (chat context)
- Text is sliced, not summarised, for speed

**Error messages:**
- No text extracted → *"Could not extract text. Is this a scanned/image PDF?"*
- File too large → *"PDF is too large. Try a shorter chapter."*
