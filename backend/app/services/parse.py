def parse_doc(file_path: str ) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text