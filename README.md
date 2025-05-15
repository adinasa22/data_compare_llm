
# 📊 Compare Two Excel/CSV Files with Streamlit

This Streamlit app allows users to **upload and compare two Excel or CSV files** interactively through a web interface. It supports various comparison operations such as merging, difference checks, summary statistics, and fuzzy matching.

## 🚀 Features

- Upload Excel (`.xlsx`) or CSV files via a sidebar.
- Preview uploaded files.
- Choose from multiple operations:
  - 🔗 **Merge on Common Column**
  - ➖ **Row-wise Subtraction** (for dataframes with the same shape)
  - 📊 **Column-wise Statistics Comparison**
  - 📋 **Show Summary Stats**
  - 🔍 **Find Rows in File 1 but not in File 2**
  - 🔍 **Find Rows in File 2 but not in File 1**
  - ✅ **Exact Matches**
  - ❌ **Not Matching Rows**
  - 🤖 **Fuzzy Matching (Similarity Check)**

## 📦 Requirements

Install the required dependencies using:

```bash
pip install streamlit pandas fuzzywuzzy python-Levenshtein openpyxl
```

> `python-Levenshtein` is recommended for performance with `fuzzywuzzy`.

## 🧠 How It Works

1. Upload two Excel or CSV files using the sidebar.
2. Preview each file within the app.
3. Select an operation from the dropdown.
4. View the results interactively.

## 📁 File Structure

```
compare_files_app/
├── app.py                 # Main Streamlit application
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

## ▶️ Run the App

```bash
streamlit run app.py
```

## 🔧 To Do

- Add logic for each operation (currently just UI placeholders).
- Add download/export options for result dataframes.
- Enhance fuzzy matching with adjustable thresholds.

## 🙌 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
