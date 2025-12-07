import streamlit as st
import markdown
from weasyprint import HTML, CSS
import tempfile
import os

st.title("📄 Markdown → PDF Converter")

uploaded_file = st.file_uploader("Upload your .md file", type=["md"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    if st.button("Convert to PDF"):
        # Read markdown content
        md_content = uploaded_file.read().decode('utf-8')
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['extra', 'codehilite', 'tables']
        )
        
        # Wrap in proper HTML structure with Unicode support
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'DejaVu Sans', sans-serif;
                    margin: 2cm;
                    line-height: 1.6;
                }}
                @page {{
                    size: Letter;
                    margin: 1cm;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Create temporary PDF file
        output_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        
        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(output_pdf)
        
        # Download button
        with open(output_pdf, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download Converted PDF",
                data=pdf_file,
                file_name="converted.pdf",
                mime="application/pdf"
            )
        
        # Clean up
        os.unlink(output_pdf)
        
        st.success("🎉 PDF created — Download above!")
