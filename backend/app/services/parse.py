import chardet
import pymupdf
import pathlib
import re

def parse_doc(file_path: str ) -> str:
    file_path = pathlib.Path(file_path)
    with open(file_path, "rb") as f:
        raw_data = f.read()
    
    result = chardet.detect(raw_data)
    encoding = result.get("encoding", "utf-8")

    print(f"result: {result} and encoding detected: {encoding}") 

    if encoding is None:
        try:
            with pymupdf.open(file_path) as doc:
                text = chr(12).join([page.get_text() for page in doc])
            newFilePath = file_path.with_suffix(".txt")
            newFilePath.write_text(text, encoding="utf-8")

            return splitSent(newFilePath.read_text(encoding="utf-8")), text
        except Exception as e:
            print(f"Error processing PDF: {e}")
            encoding = "utf-8"

    with open(file_path, "r", encoding=encoding, errors="replace") as f:
            text = f.read()
    formattedText = splitSent(text)
    return formattedText, text

def splitSent(text):
    splitText = [re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9\s]', '', line.strip().lower())) 
             for line in re.split(r'[.!?]', text)]
    return splitText