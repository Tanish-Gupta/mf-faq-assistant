# Mutual Fund FAQ Assistant

A modern FAQ assistant that answers factual questions about mutual fund schemes in India using only official public sources.

## Features

- Modern, minimalist web UI
- Answers common questions about mutual funds
- Every answer includes an official source link
- Topics covered:
  - Expense Ratio (TER)
  - Exit Load
  - Minimum SIP amounts
  - Lock-in period (ELSS)
  - Riskometer
  - Benchmark indices
  - How to download statements
  - NAV
  - KYC requirements
  - AUM

## Usage

### Web UI (Recommended)

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in your browser.

### Command Line

```bash
python mf_faq_assistant.py
```

Then type your question or keyword. Examples:
- `expense ratio`
- `what is exit load`
- `how to download statement`
- `elss lock-in`

### CLI Commands
- `help` - Show available topics
- `list` - List all questions
- `quit` - Exit the assistant

## Official Sources Used

- [SEBI](https://www.sebi.gov.in) - Securities and Exchange Board of India
- [AMFI](https://www.amfiindia.com) - Association of Mutual Funds in India
- [MF Central](https://www.mfcentral.com) - Consolidated MF portal
- [CAMS KRA](https://www.camskra.com) - KYC Registration Agency

## Disclaimer

This assistant provides **factual information only** from official sources. It does **NOT** provide investment advice. Always consult a SEBI-registered investment advisor for investment decisions.

## Requirements

- Python 3.6+
- Flask (for web UI)
