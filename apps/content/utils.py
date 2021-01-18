def clean_text(text):
    words = [word.replace("\n", "").strip() for word in text.split()]
    words[0] = words[0].title()
    text = " ".join(words)
    text = text + "." if text[-1] != "." else text
    return text