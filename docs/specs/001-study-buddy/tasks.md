# Tasks — 001: Last Minute Study Buddy

**Branch:** `001-study-buddy-mvp`  
**Team:** Person A (Frontend) · Person B (Backend/AI)

---

## Phase 1 — Core Setup `[0–3 hrs]`

- [ ] **T-01** `[B]` Set up project repo on GitLab, push initial `app.py` + `requirements.txt`
- [ ] **T-02** `[B]` Verify `ollama serve` + `llama3` model working locally
- [ ] **T-03** `[B]` Verify MongoDB running + `pymongo` can connect
- [ ] **T-04** `[B]` Implement `extract_pdf_text()` with pdfplumber + pypdf fallback
- [ ] **T-05** `[A]` Build sidebar layout — file uploader, mode toggle, file info
- [ ] **T-06** `[A]` Build landing screen (no PDF uploaded state)

---

## Phase 2 — Chat Mode `[3–6 hrs]`

- [ ] **T-07** `[B]` Implement `build_chat_prompt()` — injects PDF context + history
- [ ] **T-08** `[B]` Implement `ollama_stream()` — generator that yields tokens
- [ ] **T-09** `[A]` Render streaming response with live updating placeholder
- [ ] **T-10** `[A]` Render chat history (user bubble + AI bubble)
- [ ] **T-11** `[A]` Add quick prompt buttons (Summarise, Key Terms, Exam Tips)
- [ ] **T-12** `[B]` Implement `save_chat()` to MongoDB with error handling
- [ ] **T-13** `[A]` Add clear chat button

---

## Phase 3 — Quiz Mode `[6–9 hrs]`

- [ ] **T-14** `[B]` Implement `generate_quiz_questions()` — Ollama call + JSON parse
- [ ] **T-15** `[B]` Add JSON error recovery (strip fences, find array bounds)
- [ ] **T-16** `[A]` Render 20 questions with radio buttons per question
- [ ] **T-17** `[A]` Add progress bar tracking answered count
- [ ] **T-18** `[A]` Disable Submit until all 20 answered
- [ ] **T-19** `[A]` Build score screen — metric cards (score, %, grade)
- [ ] **T-20** `[A]` Build answer review — correct (green) / wrong (red) with correction
- [ ] **T-21** `[B]` Implement `save_quiz_result()` to MongoDB
- [ ] **T-22** `[A]` Add Regenerate + Retake buttons

---

## Phase 4 — Polish `[9–11 hrs]`

- [ ] **T-23** `[A]` Apply custom CSS — dark theme, Space Grotesk font, chat bubbles
- [ ] **T-24** `[A]` Error state: scanned PDF (no text extracted)
- [ ] **T-25** `[B]` Error state: Ollama not running — friendly message
- [ ] **T-26** `[B]` Graceful degradation if MongoDB offline
- [ ] **T-27** `[A]` Loading spinners on PDF upload + quiz generation
- [ ] **T-28** `[A]` Check layout on narrow browser window

---

## Phase 5 — Demo Prep `[11–12 hrs]`

- [ ] **T-29** `[B]` Test with 3 different PDFs (short notes, long textbook, scanned)
- [ ] **T-30** `[A]` Screenshot key screens for slides
- [ ] **T-31** `[A+B]` Write 2-minute demo script
- [ ] **T-32** `[A+B]` Push final code to GitLab `main` branch

---

## Issue Labels

| Label | Meaning |
|---|---|
| `person-a` | Frontend / UI work |
| `person-b` | Backend / AI / DB work |
| `bug` | Something broken |
| `blocked` | Waiting on another task |
| `demo-critical` | Must be done before demo |

---

## Definition of Done

A task is done when:
1. Code is committed to the feature branch
2. Feature works end-to-end on a real PDF
3. No console errors for the happy path
4. Reviewed by the other team member (quick verbal review is fine for hackathon)
