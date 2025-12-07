import streamlit as st
import markdown2
from weasyprint import HTML, CSS
import tempfile

st.title("📄 Markdown → PDF Converter (High Quality)")

uploaded_file = st.file_uploader("Upload .md file", type=["md"])

CSS_STYLE = CSS(string="""
    @page { size: A4; margin: 30px; }
    body {
        font-family: DejaVu Sans;
        font-size: 14px;
        color: #111;
        line-height: 1.6;
    }
    h1,h2,h3,h4 { font-weight: bold; margin-top: 18px; }
    code, pre {
        background: #f4f4f4;
        border-radius: 4px;
        padding: 4px;
        font-family: "JetBrains Mono", monospace;
        white-space: pre-wrap;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 6px;
    }
""")

if uploaded_file:
    st.success("File uploaded!")

    if st.button("Convert to PDF"):
        md_text = uploaded_file.read().decode("utf-8")
        html_content = markdown2.markdown(md_text, extras=["tables", "fenced-code-blocks"])

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html_content).write_pdf(pdf_file.name, stylesheets=[CSS_STYLE])

            st.download_button(
                "⬇ Download High-Quality PDF",
                data=open(pdf_file.name, "rb").read(),
                file_name="converted.pdf",
                mime="application/pdf"
            )

        st.success("📄 PDF Generated — Quality upgraded 🔥")
