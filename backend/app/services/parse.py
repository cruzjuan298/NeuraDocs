def parse_text(file_content , encoding="utf-8"):
    try:
        text = file_content.decode(encoding)
    except UnicodeDecodeError:
        text = file_content.decode("latin-1")
    return text
