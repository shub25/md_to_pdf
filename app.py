import streamlit as st
import markdown
from weasyprint import HTML
from pygments.formatters import HtmlFormatter
import tempfile
import os

st.title("📄 Markdown → PDF Converter")

# Initialize session state
if 'pdf_generated' not in st.session_state:
    st.session_state.pdf_generated = False
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None

uploaded_file = st.file_uploader("Upload your .md file", type=["md"])

# Reset state when new file is uploaded or file is removed
if uploaded_file is not None:
    current_file_name = uploaded_file.name
    if 'last_file_name' not in st.session_state or st.session_state.last_file_name != current_file_name:
        st.session_state.pdf_generated = False
        st.session_state.pdf_data = None
        st.session_state.last_file_name = current_file_name
    
    st.success("File uploaded successfully!")

    # Show convert button only if PDF not generated
    if not st.session_state.pdf_generated:
        if st.button("Convert to PDF"):
            with st.spinner("Converting to PDF..."):
                # Read markdown content
                md_content = uploaded_file.read().decode('utf-8')
                
                # Convert Markdown to HTML with syntax highlighting
                html_content = markdown.markdown(
                    md_content,
                    extensions=[
                        'extra', 
                        'codehilite',
                        'tables', 
                        'toc',
                        'fenced_code'
                    ],
                    extension_configs={
                        'codehilite': {
                            'css_class': 'highlight',
                            'linenums': False,
                            'guess_lang': True
                        }
                    }
                )
                
                # Generate Pygments CSS
                formatter = HtmlFormatter(style='default', full=True)
                pygments_css = formatter.get_style_defs('.highlight')
                
                # Enhanced HTML with improved code styling
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{
                            font-family: 'DejaVu Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                            margin: 2cm;
                            line-height: 1.6;
                            font-size: 11pt;
                            color: #333;
                        }}
                        
                        h1, h2, h3, h4, h5, h6 {{
                            margin-top: 1.5em;
                            margin-bottom: 0.5em;
                            font-weight: bold;
                        }}
                        
                        h1 {{ font-size: 2em; border-bottom: 2px solid #333; padding-bottom: 0.3em; }}
                        h2 {{ font-size: 1.5em; border-bottom: 1px solid #666; padding-bottom: 0.2em; }}
                        h3 {{ font-size: 1.25em; }}
                        
                        /* Enhanced code blocks styling */
                        .highlight {{
                            background-color: #f6f8fa;
                            border: 1px solid #d0d7de;
                            border-radius: 6px;
                            padding: 16px;
                            margin: 1em 0;
                            overflow-x: auto;
                            font-size: 10pt;
                            line-height: 1.6;
                            font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
                        }}
                        
                        .highlight pre {{
                            margin: 0;
                            padding: 0;
                            background: transparent;
                            border: none;
                            font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
                            white-space: pre-wrap;
                            word-wrap: break-word;
                        }}
                        
                        /* Inline code */
                        code {{
                            background-color: #f6f8fa;
                            padding: 3px 6px;
                            border-radius: 3px;
                            font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
                            font-size: 0.92em;
                            color: #24292f;
                            border: 1px solid #d0d7de;
                        }}
                        
                        .highlight code {{
                            background: transparent;
                            padding: 0;
                            border: none;
                            color: inherit;
                        }}
                        
                        /* Pygments syntax highlighting */
                        {pygments_css}
                        
                        /* Tables */
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            margin: 1em 0;
                        }}
                        
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 10px;
                            text-align: left;
                        }}
                        
                        th {{
                            background-color: #f5f5f5;
                            font-weight: bold;
                        }}
                        
                        /* Blockquotes */
                        blockquote {{
                            border-left: 4px solid #ddd;
                            padding-left: 16px;
                            margin-left: 0;
                            color: #666;
                            font-style: italic;
                        }}
                        
                        /* Links */
                        a {{
                            color: #0366d6;
                            text-decoration: none;
                        }}
                        
                        a:hover {{
                            text-decoration: underline;
                        }}
                        
                        @page {{
                            size: Letter;
                            margin: 1.5cm;
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
                
                # Read PDF into memory
                with open(output_pdf, "rb") as pdf_file:
                    st.session_state.pdf_data = pdf_file.read()
                
                # Clean up temp file
                os.unlink(output_pdf)
                
                # Mark as generated
                st.session_state.pdf_generated = True
                
                st.rerun()

    # Show download button if PDF is generated
    if st.session_state.pdf_generated and st.session_state.pdf_data:
        st.success("🎉 PDF created successfully!")
        
        downloaded = st.download_button(
            label="⬇ Download Converted PDF",
            data=st.session_state.pdf_data,
            file_name="converted.pdf",
            mime="application/pdf"
        )
        
        # Reset button to go back to Convert state
        if st.button("🔄 Convert Again"):
            st.session_state.pdf_generated = False
            st.session_state.pdf_data = None
            st.rerun()

else:
    # Reset state when no file is uploaded
    if st.session_state.pdf_generated:
        st.session_state.pdf_generated = False
        st.session_state.pdf_data = None
        if 'last_file_name' in st.session_state:
            del st.session_state.last_file_name
