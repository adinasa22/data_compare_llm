
# 📊 Streamlit File Comparison Tool with Fuzzy Matching and Local LLM Integration

This project is a powerful and interactive Streamlit web application for comparing two Excel or CSV files. It provides a wide range of operations, including merging, row-wise subtraction, statistical summaries, fuzzy row matching, and even local LLM analysis of mismatches.

## 🚀 Features

- Upload and preview two Excel or CSV files.
- Select and perform one of several comparison operations.
- Operations include:
  - 🔗 Merge on common columns (with join type selection).
  - ➖ Row-wise subtraction of numeric columns (for same-shaped files).
  - 📊 Column-wise summary statistics and absolute differences.
  - 📋 Full file summary statistics.
  - 🔍 Rows in File 1 but not in File 2.
  - 🔍 Rows in File 2 but not in File 1.
  - ✅ Exact matches (all common columns).
  - ❌ Not matching rows (outer merge comparison).
  - 🤖 Fuzzy matching on selected column with highlight of differences.
- Optional analysis of mismatched rows using a **local LLM via Ollama**.

## 🧠 How the Local LLM Works

If enabled, mismatched row summaries are analyzed using an LLM model served locally with **Ollama** (e.g., `mistral`). The app constructs prompts based on value differences and asks the model to explain the variance.

## 📦 Installation

```bash
pip install streamlit pandas fuzzywuzzy python-Levenshtein openpyxl ollama
```

Make sure you also have Ollama installed and a model like `mistral` pulled:

```bash
ollama run mistral
```

## ▶️ Run the App

```bash
streamlit run app.py
```

## 📁 File Structure

```
compare_files_app/
├── app.py                 # Main Streamlit application with full logic
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## 🧪 Future Improvements

- Add export/download options for results.
- Enable LLM analysis for all mismatches.
- Allow fuzzy threshold tuning from UI.
- Add user authentication and save session history.

## 🙌 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [Ollama](https://ollama.com/) for running local LLMs

---

Built with ❤️ for data comparison use cases by Aditya Gupta.
