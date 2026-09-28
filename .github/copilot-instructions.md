# Mutual Fund FAQ Assistant

A FAQ assistant answering factual questions about Indian mutual-fund schemes using
only official public sources. Every answer includes an official source link.

## Stack
- Python. **Streamlit** app (`streamlit_app.py`, recommended) and a Flask variant
  (`app.py`) with `templates/` + `static/`. Core logic in `mf_faq_assistant.py`.

## Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py      # recommended
# or: python app.py                 # Flask
```

## Conventions
- Answers must cite an official source link. Topics: TER, exit load, min SIP, ELSS
  lock-in, riskometer, benchmark, statements, NAV, KYC, AUM.

---
*This file works for both Claude (`CLAUDE.md`) and GitHub Copilot (`.github/copilot-instructions.md`).*
