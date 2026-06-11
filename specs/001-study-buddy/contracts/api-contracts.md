# API Contracts — Last Minute Study Buddy

---

## Ollama Chat (Streaming)

**POST** `http://localhost:11434/api/generate`

```json
{
  "model": "llama3.2:3b",
  "prompt": "<full prompt>",
  "stream": true
}
```

Response: newline-delimited JSON tokens.

---

## Ollama Quiz (Non-streaming)

```json
{
  "model": "llama3.2:3b",
  "prompt": "<quiz prompt>",
  "stream": false
}
```

Expected output:
```json
[
  {
    "q": "Question?",
    "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"],
    "answer": "A"
  }
]
```

---

## PDF Extraction

- Input: `.pdf` file (Streamlit UploadedFile)
- Output: plain text string
- Library: pdfplumber → pypdf fallback
- Max chars sent to Ollama: 4000 (chat), 4000 (quiz)
