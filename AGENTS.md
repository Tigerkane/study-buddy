# Agents — Last Minute Study Buddy

This document describes the AI agents used in this project.

---

## Agent 1 — Chat Agent

**Name:** Study Buddy Chat  
**Model:** Ollama (llama3.2:3b or mistral:7b)  
**Endpoint:** `POST http://localhost:11434/api/generate`  
**Mode:** Streaming

### Purpose
Answers student questions based strictly on the uploaded PDF content. Acts as a knowledgeable tutor who has read the student's notes.

### Behaviour
- Responds only from the provided PDF context
- Keeps answers concise and exam-focused
- Maintains conversation history (last 6 turns)
- Streams response token by token for fast perceived response

### Prompt Structure
```
System: You are a helpful study assistant...
Context: [first 4000 chars of PDF]
History: [last 6 messages]
User: [student question]
```

---

## Agent 2 — Quiz Generator Agent

**Name:** Quiz Generator  
**Model:** Ollama (llama3.2:3b or mistral:7b)  
**Endpoint:** `POST http://localhost:11434/api/generate`  
**Mode:** Non-streaming (single response)

### Purpose
Generates 10 multiple choice questions from the uploaded PDF content for self-assessment.

### Behaviour
- Generates exactly 10 MCQ questions per call
- Each question has 4 options (A, B, C, D) and one correct answer
- Returns strictly valid JSON — no markdown, no explanation
- Retries up to 3 times if JSON is malformed
- Validates each question before displaying

### Prompt Structure
```
System: Generate 10 MCQ questions in JSON format only
Context: [first 4000 chars of PDF chunk]
Output: JSON array starting with [ and ending with ]
```

### Output Format
```json
[
  {
    "q": "Question text?",
    "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"],
    "answer": "A"
  }
]
```

---

## Local AI Infrastructure

| Component | Details |
|---|---|
| Runtime | Ollama |
| Default Model | llama3.2:3b |
| Alternate Model | mistral:7b |
| Host | http://localhost:11434 |
| Cost | Free (runs locally) |
| Internet Required | No |
