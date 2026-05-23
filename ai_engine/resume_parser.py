# ==========================================
# Resume Parser
# Extract text from PDF safely
# ==========================================

import pdfplumber


def extract_resume_text(file_path):
    """
    Extract text from a PDF resume.
    Returns full text.
    """

    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("Resume parsing error:", e)

    return text
