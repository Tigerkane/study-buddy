# Data Model — 001: Last Minute Study Buddy

---

## MongoDB Collections

### `chats`

Stores every message in a chat session.

```json
{
  "_id": "ObjectId (auto)",
  "session_id": "string  — e.g. s_1717900000",
  "filename":   "string  — e.g. data_structures.pdf",
  "role":       "string  — 'user' | 'assistant'",
  "message":    "string  — full message text",
  "timestamp":  "ISODate — UTC"
}
```

**Indexes:**
- `{ session_id: 1, timestamp: 1 }` — fetch ordered history per session
- Optional TTL: `{ timestamp: 1 }` with `expireAfterSeconds: 86400` (auto-delete after 24h)

---

### `quiz_results`

Stores the result of each quiz submission.

```json
{
  "_id":        "ObjectId (auto)",
  "session_id": "string  — e.g. s_1717900000",
  "filename":   "string  — e.g. networks_notes.pdf",
  "score":      "int     — number of correct answers",
  "total":      "int     — total questions (always 20)",
  "percent":    "int     — rounded percentage",
  "timestamp":  "ISODate — UTC"
}
```

**Indexes:**
- `{ session_id: 1 }` — fetch all quiz results for a session

---

## Session State (in-memory, Streamlit)

These live in `st.session_state` — not persisted to MongoDB.

| Key | Type | Description |
|---|---|---|
| `session_id` | str | Unique ID generated on first load |
| `mode` | str | `"Chat"` or `"Quiz"` |
| `pdf_text` | str | Extracted text from uploaded PDF |
| `pdf_name` | str | Filename of uploaded PDF |
| `chat_history` | list[dict] | `[{role, message}]` for current session |
| `quiz_questions` | list[dict] | Generated MCQ questions |
| `quiz_answers` | dict | `{question_index: "A"/"B"/"C"/"D"}` |
| `quiz_submitted` | bool | Whether quiz has been submitted |

---

## Ollama Prompt Contracts

### Chat Prompt Input
```
pdf_text: str       — first 4000 chars of extracted PDF
history:  list      — last 6 messages [{role, message}]
question: str       — user's current question
```

### Chat Prompt Output
```
Plain text response — streamed token by token
```

### Quiz Prompt Input
```
pdf_text: str       — first 5000 chars of extracted PDF
```

### Quiz Prompt Output (expected JSON)
```json
[
  {
    "q": "Question text?",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "answer": "A"
  }
]
```

**Validation rules:**
- Must be a JSON array
- Exactly 20 items (truncate if more)
- Each item must have `q`, `options` (array of 4), `answer` (single letter A–D)
- Strip markdown code fences before parsing
