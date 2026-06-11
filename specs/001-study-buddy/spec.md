# Spec — 001: Last Minute Study Buddy (MVP)

**Status:** Active  
**Branch:** `main`  
**Created:** 2026-06-11  
**Team:** 2 members

---

## Goal

A student uploads their lecture notes or textbook chapter as a PDF and can either:
1. **Chat** with the content — ask questions, get explanations, request summaries
2. **Take a quiz** — auto-generated 10 MCQ questions to test their knowledge

The entire app runs locally with zero cost.

---

## User Scenarios

### Scenario 1 — Chat Mode (default)
> Priya uploads her Data Structures PDF and asks "Explain binary search trees simply."
> The app responds with a clear, concise explanation drawn from her notes.

### Scenario 2 — Quiz Mode
> Ravi uploads his notes and clicks "Generate 10 Questions."
> He answers all MCQs, submits, and sees his score with a full answer review.

---

## Functional Requirements

- FR-01: PDF upload with text extraction
- FR-02: Chat mode with streaming AI responses
- FR-03: Quiz mode with 10 MCQ questions
- FR-04: Model selector (llama3.2:3b / mistral:7b)

---

## Acceptance Criteria

| ID | Criteria | Priority |
|---|---|---|
| AC-01 | PDF uploads and text extracted within 5 seconds | Must |
| AC-02 | Chat responds with streamed answer under 30s | Must |
| AC-03 | Quiz generates 10 questions | Must |
| AC-04 | App runs with `streamlit run app.py` | Must |
| AC-05 | No API keys required | Must |
