import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

st.set_page_config(page_title="Compare Two Files", layout="wide")

st.title("📊 Upload and Compare Two Excel/CSV Files")

# Upload files
st.sidebar.header("Upload Files")
file1 = st.sidebar.file_uploader("Upload First Excel/CSV File", type=["csv", "xlsx"], key="file1")
file2 = st.sidebar.file_uploader("Upload Second Excel/CSV File", type=["csv", "xlsx"], key="file2")

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if file1 and file2:
    df1 = read_file(file1)
    df2 = read_file(file2)

    st.subheader("📁 First File Preview")
    st.dataframe(df1.head())

    st.subheader("📁 Second File Preview")
    st.dataframe(df2.head())

    st.divider()
    st.header("🔍 Select Operation")

    operation = st.selectbox("Choose an operation", [
        "Merge on Common Column",
        "Row-wise Subtraction (Same Shape)",
        "Column-wise Statistics Comparison",
        "Show Summary Stats",
        "Rows in File 1 but not in File 2",
        "Rows in File 2 but not in File 1",
        "Exact Matches",
        "Not Matching Rows",
        "Similar Rows (Fuzzy Matching)"
    ])

    if operation == "Merge on Common Column":
        common_cols = list(set(df1.columns).intersection(set(df2.columns)))
        if common_cols:
            join_col = st.selectbox("Select column to join on", common_cols)
            how = st.radio("Join type", ["inner", "left", "right", "outer"])
            merged_df = pd.merge(df1, df2, on=join_col, how=how)
            st.write(f"Merged DataFrame using `{how}` join on `{join_col}`:")
            st.dataframe(merged_df.head())
        else:
            st.warning("No common columns found for merge.")

    elif operation == "Row-wise Subtraction (Same Shape)":
        try:
            result = df1.select_dtypes(include='number') - df2.select_dtypes(include='number')
            st.write("Result of row-wise subtraction (numerical columns only):")
            st.dataframe(result.head())
        except Exception as e:
            st.error(f"Error in subtraction: {e}")

    elif operation == "Column-wise Statistics Comparison":
        st.write("Summary of statistics for both files (numeric columns only):")
        stats_df1 = df1.describe().T
        stats_df2 = df2.describe().T

        st.subheader("📘 File 1 Stats")
        st.dataframe(stats_df1)

        st.subheader("📙 File 2 Stats")
        st.dataframe(stats_df2)

        st.subheader("📗 Absolute Difference")
        try:
            diff = (stats_df1 - stats_df2).abs()
            st.dataframe(diff)
        except:
            st.warning("Mismatch in numeric columns for difference computation.")

    elif operation == "Show Summary Stats":
        st.subheader("📘 File 1 Summary")
        st.dataframe(df1.describe(include='all'))

        st.subheader("📙 File 2 Summary")
        st.dataframe(df2.describe(include='all'))

    elif operation == "Rows in File 1 but not in File 2":
        common_cols = list(set(df1.columns) & set(df2.columns))
        if common_cols:
            join_col = st.selectbox("Select column to check for differences", common_cols)
            df1_only = df1[~df1[join_col].isin(df2[join_col])]
            st.subheader("🟥 Rows in File 1 but not in File 2")
            st.dataframe(df1_only)
        else:
            st.warning("No common columns found for comparison.")

    elif operation == "Rows in File 2 but not in File 1":
        common_cols = list(set(df1.columns) & set(df2.columns))
        if common_cols:
            join_col = st.selectbox("Select column to check for differences", common_cols)
            df2_only = df2[~df2[join_col].isin(df1[join_col])]
            st.subheader("🟦 Rows in File 2 but not in File 1")
            st.dataframe(df2_only)
        else:
            st.warning("No common columns found for comparison.")

    elif operation == "Exact Matches":
        common_cols = list(set(df1.columns) & set(df2.columns))
        if common_cols:
            #join_col = st.selectbox("Select column to check for exact matches", common_cols)
            exact_matches = pd.merge(df1, df2, how='inner', validate="one_to_one")
            st.subheader("✅ Exact Matches")
            st.dataframe(exact_matches)
        else:
            st.warning("No common columns found for exact match comparison.")

    elif operation == "Not Matching Rows":
        common_cols = list(set(df1.columns) & set(df2.columns))
        if common_cols:
            #join_col = st.selectbox("Select column to check for non-matching rows", common_cols)
            not_matching = pd.merge(df1, df2, how='outer', indicator=True)
            not_matching = not_matching[not_matching['_merge'] != 'both']
            st.subheader("❌ Not Matching Rows")
            st.dataframe(not_matching)
        else:
            st.warning("No common columns found for non-matching row comparison.")

    elif operation == "Similar Rows (Fuzzy Matching)":
        common_cols = list(set(df1.columns) & set(df2.columns))
        if common_cols:
            join_col = st.selectbox("Select column to check for non-matching rows", common_cols)

            def summarize_mismatches(row1, row2, numeric_threshold=1, text_threshold=80):
                differences = {}

                for col in row1.index:
                    if pd.isna(row1[col]) or pd.isna(row2[col]):
                        continue
                    if isinstance(row1[col], str) and isinstance(row2[col], str):
                        score = fuzz.ratio(row1[col], row2[col])
                        if score < text_threshold:
                            #differences[col] = (row1[col], row2[col], score)
                            differences[col] = f"Mismatch: {row1[col]} vs {row2[col]}. Similarity Score: {score}"
                    elif isinstance(row1[col], (int, float)) and isinstance(row2[col], (int, float)):
                        score = abs(row1[col] - row2[col])
                        if score > numeric_threshold:
                            #differences[col] = (row1[col], row2[col])
                            differences[col] = f"Mismatch: {row1[col]} vs {row2[col]}. Similarity Score: {score}"

                return differences if differences else None

            mismatch_summaries = []

            for _, row_a in df1.iterrows():
                row_b = df2[df2[join_col] == row_a[join_col]].iloc[0]
                summary = summarize_mismatches(row_a, row_b)
                if summary:
                    mismatch_summaries.append({join_col: row_a[join_col], "Summary": summary})


            st.subheader("❌ Similar Rows")
            mismatch_df = pd.DataFrame(mismatch_summaries)
            st.dataframe(mismatch_df)

            st.subheader(" Using Local LLM to explain similarities/differences")
            radio = st.radio("📈 Do you want to perform analysis using local LLM?", ["Yes", "No"], index=1)
            if radio == "Yes":
                st.success("Running analysis using local LLM...")

                import ollama


                def explain_variance(df, context=""):
                    import re
                    for _, row in df.iterrows():
                        match = re.search(r'(\w+)\s+vs\s+(\w+)', str(row["Summary"]))
                        if match:
                            value_a = match.group(1)
                            value_b = match.group(2)
                            if isinstance(value_a, int):
                                if isinstance(value_b, int):
                                    difference = abs(value_a - value_b)
                                    context = ""
                            else:
                                difference = row["Summary"]
                                context = ""

                    prompt = f"""
                                I have two values:

                                Value A: {value_a}
                                Value B: {value_b}

                                The difference is: {difference}

                                Context (if any): {context}

                                Can you explain the difference and provide a possible reason for the variance? Be concise but informative.
                                """

                    response = ollama.chat(
                        model='mistral',  # Change to the model you pulled with Ollama
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    return response['message']['content']


                if not mismatch_df.empty:
                    x = explain_variance(mismatch_df)
                    st.write(x)

            else:
                st.warning("Analysis using local LLM is skipped.")





        else:
            st.warning("No common columns found for non-matching row comparison.")


else:
    st.info("Please upload both files to proceed.")