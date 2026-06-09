# Spec — 001: Last Minute Study Buddy (MVP)

**Status:** Active  
**Branch:** `001-study-buddy-mvp`  
**Created:** 2026-06-09  
**Team:** 2 members

---

## Goal

A student uploads their lecture notes or textbook chapter as a PDF and can either:
1. **Chat** with the content — ask questions, get explanations, request summaries
2. **Take a quiz** — auto-generated 20 MCQ questions to test their knowledge

The entire app runs locally with zero cost. Designed for last-minute exam prep.

---

## User Scenarios

### Scenario 1 — Chat Mode (default)
> Priya has an exam in 3 hours. She uploads her Data Structures PDF.
> She types "Explain binary search trees simply."
> The app responds with a clear, concise explanation drawn from her notes.
> She asks follow-up questions. Each answer is based only on her uploaded content.

### Scenario 2 — Quiz Mode
> Ravi wants to test himself before his Networks exam.
> He uploads his notes PDF and clicks "Generate 20 Questions."
> He answers all 20 MCQs, submits, and sees his score with a full answer review.
> He can retake the quiz or go back to Chat mode.

### Scenario 3 — Session Persistence
> Arjun starts a chat session, closes the browser, and comes back.
> His chat history is stored in MongoDB and available in the session.

---

## Functional Requirements

### FR-01: PDF Upload
- User can upload a `.pdf` file via the sidebar
- App extracts text using `pdfplumber` (fallback: `pypdf`)
- Must handle PDFs up to 50MB
- Must show extracted character count after upload
- Must show an error if the PDF is scanned/image-only (no text layer)

### FR-02: Mode Selection
- Two modes: **Chat** and **Quiz**
- Chat is the default mode on PDF upload
- Mode toggle visible only after a PDF is uploaded
- Switching modes does not clear the uploaded PDF

### FR-03: Chat Mode
- Text input for free-form questions
- AI response streamed token-by-token (not shown all at once)
- Response must be grounded in the uploaded PDF content only
- Quick prompt buttons: "Summarise key points", "List key terms", "Give me 5 exam tips"
- Clear chat button to reset conversation
- All messages saved to MongoDB (`chats` collection)

### FR-04: Quiz Mode
- "Generate 20 Questions" button triggers Ollama
- Exactly 20 MCQ questions generated from PDF content
- Each question has 4 options (A, B, C, D) and one correct answer
- Progress bar shows how many questions answered
- Submit button disabled until all 20 answered
- After submit: show score, percentage, grade label, and full answer review
- Incorrect answers show the correct answer in green
- "Regenerate" button to get a new set of questions
- Quiz results saved to MongoDB (`quiz_results` collection)

### FR-05: MongoDB Storage
- App functions normally if MongoDB is offline (graceful degradation)
- `chats` collection stores: session_id, filename, role, message, timestamp
- `quiz_results` collection stores: session_id, filename, score, total, percent, timestamp
- MongoDB connection status shown in sidebar

---

## Acceptance Criteria

| ID | Criteria | Priority |
|---|---|---|
| AC-01 | PDF uploads and text is extracted within 5 seconds for a 20-page doc | Must |
| AC-02 | Chat responds with a streamed answer in under 30 seconds | Must |
| AC-03 | Quiz generates exactly 20 questions | Must |
| AC-04 | Quiz submit is blocked until all 20 questions are answered | Must |
| AC-05 | Score + answer review shown after submission | Must |
| AC-06 | App works with MongoDB offline | Must |
| AC-07 | App runs with single command: `streamlit run app.py` | Must |
| AC-08 | No API keys required anywhere | Must |
| AC-09 | Chat history persists within a session | Should |
| AC-10 | Quick prompt buttons visible on first load of Chat mode | Should |
| AC-11 | Switching modes does not require re-uploading PDF | Should |
| AC-12 | Scanned PDF shows clear error message | Could |
