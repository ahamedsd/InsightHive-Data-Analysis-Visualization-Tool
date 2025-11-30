import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# -------------------------------
# FILE READER FUNCTION (SAFE)
# -------------------------------
def read_file(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
            return pd.read_excel(file)
        elif file.name.endswith(".json"):
            return pd.read_json(file)
        else:
            return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="InsightHive", layout="wide")
st.title("📊 InsightHive – Data Explorer")


# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xlsx", "xls", "json"])

if uploaded_file:
    df = read_file(uploaded_file)

    if df is None:
        st.error("❌ Unsupported or invalid file. Upload CSV/Excel/JSON.")
        st.stop()

    # Safe copy
    st.session_state["df"] = df.copy()

    st.subheader("📁 Preview of Data")
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # DOWNLOAD CLEAN DATA
    # -------------------------------
    def download_excel(dataframe):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Data")
        return buffer.getvalue()

    excel_bytes = download_excel(df)
    st.download_button(
        label="⬇️ Download Excel",
        data=excel_bytes,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # -------------------------------
    # QUICK STATS
    # -------------------------------
    st.subheader("📐 Summary Statistics")
    st.write(df.describe(include="all"))


    # -------------------------------
    # VISUALIZATIONS
    # -------------------------------
    st.subheader("📈 Visual Insights")

    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_columns) >= 1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Histogram")
            col = st.selectbox("Choose column:", numeric_columns, key="hist_col")
            fig = px.histogram(df, x=col)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Box Plot")
            col = st.selectbox("Column:", numeric_columns, key="box_col")
            fig = px.box(df, y=col)
            st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    if len(numeric_columns) > 1:
        st.subheader("🔥 Correlation Heatmap")
        corr = df[numeric_columns].corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart for categorical
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if categorical_columns:
        st.subheader("🔸 Pie Chart")
        cat_col = st.selectbox("Choose category column:", categorical_columns)
        fig = px.pie(df, names=cat_col)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a dataset to begin exploring.")
