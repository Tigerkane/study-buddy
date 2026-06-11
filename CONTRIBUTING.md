# Contributing to Last Minute Study Buddy

Thank you for contributing! This guide explains how to work on this project.

## Team
- Person A — Frontend / UI (Streamlit, CSS)
- Person B — Backend / AI (Ollama, PDF parsing)

## Getting Started

```bash
git clone https://code.swecha.org/Saichaitanya9/last-minute-study-buddy.git
cd last-minute-study-buddy
pip install -r requirements.txt
python -m streamlit run app.py
```

## Branch Naming
```
feature/your-feature-name
fix/bug-description
docs/what-you-documented
```

## Commit Message Format (Conventional Commits)
```
feat: add quiz timer
fix: handle scanned PDF gracefully
docs: update README with setup steps
refactor: split quiz generation into batches
test: add quiz JSON parsing tests
```

## Merge Request Checklist
- [ ] Tested with a real PDF
- [ ] No console errors on happy path
- [ ] Ollama offline shows a clear error
- [ ] Reviewed by other team member

## Code Style
- Follow PEP8 (max line length 120)
- Use `black` for formatting: `black app.py`
- Use `flake8` for linting: `flake8 app.py`
- Use `mypy` for type checking: `mypy app.py`

## Running Tests
```bash
pytest tests/ -v
```
