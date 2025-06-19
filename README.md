# 🧾 Resume Parser GUI (Tkinter + NLP + PDF/DOCX)

This project is a **Resume Parser** with a user-friendly GUI built using **Tkinter**, capable of extracting useful information from DOCX and PDF resumes using **Natural Language Processing (NLP)** techniques.

---

## 🎯 Features

- 🔐 Simple login system
- 📄 Supports both `.docx` and `.pdf` file formats
- 🧠 Extracts:
  - Name
  - Skills
  - Educational Qualifications
  - Email Address
  - Phone Number
  - Experience Dates (if mentioned)
- 🎨 GUI built with Tkinter for intuitive usage

---

## 🛠 Tech Stack

- **Frontend / GUI**: Tkinter
- **Backend**: Python
- **Libraries Used**:
  - `nltk` (tokenization, POS tagging, chunking)
  - `spaCy` (NER and NLP)
  - `pdfminer.six` (PDF text extraction)
  - `docx2txt` (DOCX text extraction)
  - `pandas`, `re`, `sqlite3`, `os`, `tkinter.ttk`, etc.

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/resume-parser.git
cd resume-parser
