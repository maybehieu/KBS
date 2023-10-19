from underthesea import word_tokenize
import re


def tokenizer(sentence=""):
    return [
        s
        for s in word_tokenize(sentence)
        if re.match(r"^[a-zA-Z0-9\s\u0080-\uFFFF]+$", s)
    ]
