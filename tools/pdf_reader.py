from pathlib import Path
from pypdf import PdfReader
def read_pdf(file_path):
    path = Path(file_path).expanduser()
    if not path.is_file():
        return "PDF not found. Check the file path."
    try:
        reader = PdfReader(str(path))
        text = " ".join((page.extract_text() or "") for page in reader.pages)
        return text[:4500] if text else "No selectable text found in this PDF."
    except Exception as exc:
        print(f"PDF error: {exc}")
        return "Could not read this PDF."
