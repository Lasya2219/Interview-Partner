import io
from pypdf import PdfReader

def extract_text_from_pdf(file_source):
    if isinstance(file_source, bytes):
        stream = io.BytesIO(file_source)
    else:
        stream = file_source

    reader = PdfReader(stream)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text.strip()