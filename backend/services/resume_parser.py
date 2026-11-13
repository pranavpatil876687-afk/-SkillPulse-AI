import fitz
import pytesseract
from PIL import Image
from pypdf import PdfReader


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# --------------------------------------------------
# Normal PDF Text Extraction
# --------------------------------------------------

def extract_with_pymupdf(file_path: str) -> str:

    document = fitz.open(file_path)

    text_parts = []

    for page in document:

        text = page.get_text("text")

        if text:
            text_parts.append(text)

    document.close()

    return "\n".join(text_parts)


# --------------------------------------------------
# OCR Extraction
# --------------------------------------------------

def extract_with_ocr(file_path: str) -> str:

    document = fitz.open(file_path)

    text_parts = []

    for page_number, page in enumerate(document):

        print(
            f"OCR processing page {page_number + 1}..."
        )

        # Render PDF page as image
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False
        )

        image = Image.frombytes(
            "RGB",
            [
                pixmap.width,
                pixmap.height
            ],
            pixmap.samples
        )

        text = pytesseract.image_to_string(
            image
        )

        if text:
            text_parts.append(text)

    document.close()

    return "\n".join(text_parts)


# --------------------------------------------------
# PyPDF Fallback
# --------------------------------------------------

def extract_with_pypdf(file_path: str) -> str:

    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            text_parts.append(text)

    return "\n".join(text_parts)


# --------------------------------------------------
# Main Resume Text Extraction
# --------------------------------------------------

def extract_text(file_path: str) -> str:

    # ----------------------------------------------
    # 1. Try PyMuPDF
    # ----------------------------------------------

    try:

        text = extract_with_pymupdf(
            file_path
        )

        print(
            f"PyMuPDF extracted {len(text)} characters."
        )

        if len(text.strip()) >= 1000:

            return text.strip()

    except Exception as error:

        print(
            f"PyMuPDF extraction failed: {error}"
        )


    # ----------------------------------------------
    # 2. Try OCR
    # ----------------------------------------------

    try:

        print(
            "Text extraction is insufficient."
        )

        print(
            "Starting OCR..."
        )

        ocr_text = extract_with_ocr(
            file_path
        )

        print(
            f"OCR extracted {len(ocr_text)} characters."
        )

        if len(ocr_text.strip()) > len(text.strip()):

            return ocr_text.strip()

    except Exception as error:

        print(
            f"OCR extraction failed: {error}"
        )


    # ----------------------------------------------
    # 3. PyPDF fallback
    # ----------------------------------------------

    try:

        fallback_text = extract_with_pypdf(
            file_path
        )

        print(
            f"PyPDF extracted {len(fallback_text)} characters."
        )

        if len(fallback_text.strip()) > len(text.strip()):

            return fallback_text.strip()

        return text.strip()

    except Exception as error:

        print(
            f"PyPDF extraction failed: {error}"
        )

        return text.strip() if text else ""