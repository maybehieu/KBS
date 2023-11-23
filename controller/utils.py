from underthesea import word_tokenize
import re


def tokenizer(sentence=""):
    return [
        s
        for s in word_tokenize(sentence)
        if re.match(r"^[a-zA-Z0-9\s\u0080-\uFFFF]+$", s)
    ]

def removeDupListDict(lst):
    unique_dicts = []
    seen_hashes = set()
    for d in lst:
        # Create a hashable representation (frozenset of sorted tuples)
        hashable_repr = frozenset(sorted(d.items()))
        if hashable_repr not in seen_hashes:
            seen_hashes.add(hashable_repr)
            unique_dicts.append(d)
    return unique_dicts