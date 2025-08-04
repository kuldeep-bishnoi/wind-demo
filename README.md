# 📁 Universal File Converter

A powerful web application that allows you to preview, convert, and export files between various formats. Built with Streamlit and Python.

## 🌟 Features

- **Wide Format Support**: Supports documents (PDF, DOCX, TXT), spreadsheets (CSV, XLSX), images (PNG, JPG, GIF, etc.), and code files.
- **File Previews**: View file contents directly in the browser before conversion.
- **AI-Powered Summaries**: Generate concise summaries of text content using OpenAI's API.
- **Batch Processing**: Upload and process multiple files simultaneously.
- **Responsive Design**: Works on both desktop and mobile devices.
- **Secure**: All processing happens locally in your browser (except for AI summaries which require an API key).

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/universal-file-converter.git
   cd universal-file-converter
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload one or more files using the file uploader

4. For AI summaries (optional):
   - Enter your OpenAI API key in the sidebar
   - Click "Generate Summary" on any text file

5. To convert files:
   - Select the target format from the dropdown
   - Click "Convert & Download"
   - The converted file will be downloaded automatically

## 📋 Supported File Types

| Category     | Supported Formats                                  |
|--------------|---------------------------------------------------|
| Documents   | PDF, DOCX, TXT, MD                                |
| Spreadsheets| CSV, XLSX, XLS                                   |
| Images      | PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP              |
| Data        | JSON, YAML, YML, XML                             |
| Code        | PY, JS, HTML, CSS, Java, C, C++, C#, Go, PHP, Ruby, Swift |

## 🔄 Conversion Options

- **To PDF**: Convert any supported file to PDF format
- **To DOCX**: Convert to Microsoft Word document
- **To TXT**: Extract and convert to plain text
- **To CSV/Excel**: Convert tabular data to spreadsheet formats
- **To JSON/YAML**: Convert data to structured formats

## 🔒 Privacy Note

- All file processing happens locally in your browser
- For AI summaries, your content is sent to OpenAI's servers
- No files are stored on any server after processing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- File type detection with [python-magic](https://github.com/ahupp/python-magic)
- PDF generation with [FPDF2](https://pyfpdf.github.io/fpdf2/)
- Document processing with [python-docx](https://python-docx.readthedocs.io/)
- AI capabilities powered by [OpenAI](https://openai.com/)

## 📬 Contact

For questions or feedback, please open an issue on GitHub.
