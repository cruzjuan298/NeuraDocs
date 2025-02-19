import chardet

def parse_doc(file_path: str ) -> str:
    with open(file_path, "rb") as f:
        raw_data= f.read()
    
    result = chardet.detect(raw_data)
    encoding = result.get("encoding", "utf-8")

    if encoding is None:
        encoding = "utf-8"

    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1", errors="replace") as f:
            text = f.read()
    return text