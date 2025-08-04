import streamlit as st
from fpdf import FPDF
import openai
import os
import logging
from logging.handlers import RotatingFileHandler
import tempfile
from docx import Document
from PyPDF2 import PdfFileReader
import csv
import json
import yaml

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

def create_docx(text, summary=None):
    try:
        doc = Document()
        if summary:
            doc.add_heading("Summary", 0)
            doc.add_paragraph(summary)
            doc.add_heading("Full Text", 0)
            doc.add_paragraph(text)
        else:
            doc.add_paragraph(text)
        return doc
    except Exception as e:
        logger.error(f"Error creating DOCX: {e}")
        return None

def create_txt(text, summary=None):
    try:
        if summary:
            return f"Summary:\n{summary}\n\nFull Text:\n{text}"
        else:
            return text
    except Exception as e:
        logger.error(f"Error creating TXT: {e}")
        return None

def create_csv(text, summary=None):
    try:
        if summary:
            return f"Summary,{summary}\nFull Text,{text}"
        else:
            return text
    except Exception as e:
        logger.error(f"Error creating CSV: {e}")
        return None

def create_json(text, summary=None):
    try:
        if summary:
            return json.dumps({"Summary": summary, "Full Text": text})
        else:
            return json.dumps({"Text": text})
    except Exception as e:
        logger.error(f"Error creating JSON: {e}")
        return None

def create_yaml(text, summary=None):
    try:
        if summary:
            return yaml.dump({"Summary": summary, "Full Text": text})
        else:
            return yaml.dump({"Text": text})
    except Exception as e:
        logger.error(f"Error creating YAML: {e}")
        return None

def main():
    st.title("Text to File Converter")
    files = st.file_uploader("Upload files", type=["txt", "pdf", "docx", "csv", "json", "yaml"], accept_multiple_files=True)
    api_key = st.text_input("Enter your OpenAI API key (optional)")
    output_file = st.selectbox("Select output file", [f"output_{i}.pdf" for i in range(1, 21)])
    if st.button("Generate File"):
        try:
            for file in files:
                text = file.read().decode("utf-8")
                summary = generate_summary(text, api_key) if api_key else None
                if file.name.endswith(".pdf"):
                    pdf = PdfFileReader(file)
                    text = ""
                    for page in pdf.pages:
                        text += page.extractText()
                    pdf = create_pdf(text, summary)
                elif file.name.endswith(".docx"):
                    doc = Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text
                    doc = create_docx(text, summary)
                elif file.name.endswith(".txt"):
                    txt = create_txt(text, summary)
                elif file.name.endswith(".csv"):
                    csv = create_csv(text, summary)
                elif file.name.endswith(".json"):
                    json = create_json(text, summary)
                elif file.name.endswith(".yaml"):
                    yaml = create_yaml(text, summary)
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file_path = os.path.join(temp_dir, output_file)
                    if file.name.endswith(".pdf"):
                        pdf.output(temp_file_path)
                    elif file.name.endswith(".docx"):
                        doc.save(temp_file_path)
                    elif file.name.endswith(".txt"):
                        with open(temp_file_path, "w") as f:
                            f.write(txt)
                    elif file.name.endswith(".csv"):
                        with open(temp_file_path, "w") as f:
                            f.write(csv)
                    elif file.name.endswith(".json"):
                        with open(temp_file_path, "w") as f:
                            f.write(json)
                    elif file.name.endswith(".yaml"):
                        with open(temp_file_path, "w") as f:
                            f.write(yaml)
                    with open(temp_file_path, "rb") as f:
                        st.download_button(
                            label="Download File",
                            data=f,
                            file_name=output_file,
                            mime="application/octet-stream"
                        )
        except Exception as e:
            logger.error(f"Error generating file: {e}")
            st.error(f"Error generating file: {e}")

if __name__ == "__main__":
    main()

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
    logger.addHandler(handler)

    # Set up OpenAI API
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # Set up Streamlit
    st.set_page_config(layout="wide")