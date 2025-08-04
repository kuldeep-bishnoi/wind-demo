import streamlit as st
from fpdf import FPDF
import openai
import os
import logging
from logging.handlers import RotatingFileHandler
import tempfile

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
logger.addHandler(handler)

# Set up OpenAI API
openai.api_key = os.environ.get('OPENAI_API_KEY')

def validate_openai_api_key(api_key):
    try:
        openai.api_key = api_key
        openai.Model.list()
        return True
    except openai.error.AuthenticationError:
        return False

def generate_summary(text, api_key):
    try:
        if validate_openai_api_key(api_key):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Summarize the following text: {text}",
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].text
        else:
            return None
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return None

def create_pdf(text, summary=None):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        if summary:
            pdf.multi_cell(0, 5, txt="Summary:")
            pdf.multi_cell(0, 5, txt=summary)
            pdf.ln(10)
            pdf.multi_cell(0, 5, txt="Full Text:")
            pdf.multi_cell(0, 5, txt=text)
        else:
            pdf.multi_cell(0, 5, txt=text)
        return pdf
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        return None

def main():
    st.title("Text to PDF Converter")
    text = st.text_area("Enter your text here", height=200)
    api_key = st.text_input("Enter your OpenAI API key (optional)")
    if st.button("Generate PDF"):
        try:
            summary = generate_summary(text, api_key) if api_key else None
            pdf = create_pdf(text, summary)
            if pdf:
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    pdf.output(tmp.name)
                    st.download_button("Download PDF", tmp.name, file_name="output.pdf")
            else:
                st.error("Failed to generate PDF")
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            st.error("Failed to generate PDF")

if __name__ == "__main__":
    main()