import streamlit as st
import markdown2
from xhtml2pdf import pisa
import tempfile

st.title("📄 Markdown → PDF Converter (Cloud Compatible)")

uploaded_file = st.file_uploader("Upload your .md file", type=["md"])

if uploaded_file:
    st.success("File uploaded!")

    if st.button("Convert to PDF"):
        md_text = uploaded_file.read().decode("utf-8")

        # Convert MD → HTML
        html = markdown2.markdown(md_text)

        # Temp PDF file
        output_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        with open(output_pdf, "wb") as pdf:
            pisa.CreatePDF(html, dest=pdf)  # HTML → PDF convert

        st.success("🎉 Conversion done — download below")

        with open(output_pdf, "rb") as f:
            st.download_button("⬇ Download PDF", f, "converted.pdf", "application/pdf")
