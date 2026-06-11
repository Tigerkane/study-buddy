# Tasks — 001: Last Minute Study Buddy

**Branch:** `main`  
**Team:** Person A (Frontend) · Person B (Backend/AI)

---

## Phase 1 — Core Setup `[0–3 hrs]`

- [x] **T-01** `[B]` Set up project repo on GitLab
- [x] **T-02** `[B]` Verify `ollama serve` + model working locally
- [x] **T-03** `[B]` Implement `extract_pdf_text()` with pdfplumber + pypdf fallback
- [x] **T-04** `[A]` Build sidebar layout — file uploader, mode toggle, file info
- [x] **T-05** `[A]` Build landing screen (no PDF uploaded state)

---

## Phase 2 — Chat Mode `[3–6 hrs]`

- [x] **T-06** `[B]` Implement `build_chat_prompt()` with PDF context + history
- [x] **T-07** `[B]` Implement `ollama_stream()` — generator that yields tokens
- [x] **T-08** `[A]` Render streaming response with live updating placeholder
- [x] **T-09** `[A]` Render chat history (user bubble + AI bubble)
- [x] **T-10** `[A]` Add quick prompt buttons
- [x] **T-11** `[A]` Add clear chat button

---

## Phase 3 — Quiz Mode `[6–9 hrs]`

- [x] **T-12** `[B]` Implement `generate_quiz_questions()` — Ollama + JSON parse
- [x] **T-13** `[B]` Add JSON error recovery + 3x retry
- [x] **T-14** `[A]` Render 10 questions with radio buttons
- [x] **T-15** `[A]` Add progress bar + submit validation
- [x] **T-16** `[A]` Build score screen + answer review
- [x] **T-17** `[A]` Add Regenerate + Retake buttons

---

## Phase 4 — Polish `[9–11 hrs]`

- [x] **T-18** `[A]` Apply custom CSS dark theme
- [x] **T-19** `[A]` Model selector (llama3.2:3b / mistral:7b) in sidebar
- [x] **T-20** `[B]` Error handling — Ollama offline, scanned PDF
- [x] **T-21** `[A]` Loading spinners + progress bar for quiz generation

---

## Phase 5 — Demo Prep `[11–12 hrs]`

- [x] **T-22** `[B]` Test with 3 different PDFs
- [x] **T-23** `[A]` Push all files to GitLab
- [x] **T-24** `[A+B]` Add compliance files + speckit docs
- [x] **T-25** `[A+B]` Final commit + git tag v1.0.0

---

## Definition of Done

A task is done when:
1. Code is committed to the branch
2. Feature works end-to-end on a real PDF
3. No console errors on happy path
4. Reviewed by other team member
