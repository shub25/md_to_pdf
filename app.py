import streamlit as st
import pypandoc
import tempfile

st.title("📄 Markdown → PDF Converter")

uploaded_file = st.file_uploader("Upload your .md file", type=["md"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    if st.button("Convert to PDF"):
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_md:
            temp_md.write(uploaded_file.read())
            temp_md_path = temp_md.name

        # Temporary output PDF file
        output_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        # Convert using XeLaTeX (handles Unicode like ↔ → ✓ etc.)
        pypandoc.convert_file(
            temp_md_path,
            'pdf',
            outputfile=output_pdf,
            extra_args=[
            '--standalone',
            '--pdf-engine=xelatex',
            '-V', 'mainfont=DejaVu Sans',
            ]
        )

        # Download button
        with open(output_pdf, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download Converted PDF",
                data=pdf_file,
                file_name="converted.pdf",
                mime="application/pdf"
            )

        st.success("🎉 PDF created — Download above!")
