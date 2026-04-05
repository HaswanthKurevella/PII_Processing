# PII Processing Pipeline

**A local, modular NLP pipeline for detecting and anonymizing Personally Identifiable Information (PII) in unstructured text.**

Built with spaCy and Microsoft Presidio. Runs entirely on-device — no external API calls, no data leaves your machine.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

PII Anonymizer is a five-stage NLP pipeline that processes raw text through tokenization, part-of-speech tagging, named entity recognition, PII detection, and finally anonymization. It is available both as a command-line tool and as an interactive Streamlit web application.

---

## Features

- Tokenization of raw input text
- Part-of-speech (POS) tagging for each token
- Named entity recognition (NER) using spaCy
- PII detection powered by Microsoft Presidio Analyzer
- Automatic PII redaction via Presidio Anonymizer
- Interactive step-by-step visualization via Streamlit UI
- Fully offline — no cloud dependencies

---

## Tech Stack

| Component | Library | Version |
|---|---|---|
| NLP Engine | [spaCy](https://spacy.io/) | `en_core_web_lg` |
| PII Detection | [presidio-analyzer](https://microsoft.github.io/presidio/) | latest |
| PII Anonymization | [presidio-anonymizer](https://microsoft.github.io/presidio/) | latest |
| Web Interface | [Streamlit](https://streamlit.io/) | latest |
| Language | Python | 3.9+ |

---

## Project Structure

```
pii-anonymizer/
│
├── nlp_processor.py        # spaCy NLP wrapper: tokenization, POS tagging, NER
├── PII_analyzer.py         # Presidio AnalyzerEngine wrapper: PII span detection
├── PII_anonymizer.py       # Presidio AnonymizerEngine wrapper: PII redaction
├── Pipeline.py             # CLI entry point: sequential pipeline execution
├── test_app.py             # Streamlit web application
├── app.py                  # Alternate streamlit application
└── requirements.txt        # Python dependencies
```

---

## Prerequisites

- Python 3.9 or higher
- pip
- Virtual environment (recommended)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/HaswanthKurevella/PII_Processing.git
cd PII_Processing
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Download the spaCy language model**

```bash
python -m spacy download en_core_web_lg
```

> **Note:** The `en_core_web_lg` model is not included in `requirements.txt` and must be downloaded separately as a post-install step.

---

## Usage

### Streamlit Web Application

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser. Enter text in the input area and click **Analyze** to run the full pipeline with step-by-step output.

### Command-Line Interface

```bash
python Pipeline.py
```

You will be prompted to enter text. The pipeline executes sequentially and prints the output of each stage to stdout.

---

## Pipeline Stages

| Stage | Module | Output |
|---|---|---|
| 1. Tokenization | `NLPProcessor.getTokens()` | List of word tokens |
| 2. POS Tagging | `NLPProcessor.getPosTags()` | `(token, POS_LABEL)` pairs |
| 3. Named Entity Recognition | `NLPProcessor.getEntities()` | `(entity_text, ENTITY_TYPE)` pairs |
| 4. PII Detection | `PIIanalyzer.detectPII()` | `RecognizerResult` objects with entity type, score, and span |
| 5. PII Anonymization | `PIIanonymizer.anonymizePII()` | Redacted text with `<ENTITY_TYPE>` placeholders |

---

## Example

**Input**

```
John Smith called from +1-800-555-0199. His email is john.smith@example.com and he lives in Boston, MA.
```

**Output**

```
<PERSON> called from <PHONE_NUMBER>. His email is <EMAIL_ADDRESS> and he lives in <LOCATION>.
```

---

## Contributing

Contributions are welcome. Please follow these guidelines:

- Fork the repository and create a feature branch off `main`
- Keep each module (`nlp_processor`, `PII_analyzer`, `PII_anonymizer`) independently testable
- To add custom PII recognizers, extend `PIIanalyzer` via Presidio's `RecognizerRegistry` — avoid embedding regex directly in the pipeline
- Submit a pull request with a clear description of the change and its purpose

---

## License

This project is licensed under the [MIT License](LICENSE).
