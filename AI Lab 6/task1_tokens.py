import re

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے"
]

print("TASK 1: TOKENIZATION")
for text in samples:
    whitespace_tokens = text.split()
    word_tokens = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    print("\nOriginal:", repr(text))
    print("Whitespace tokens:", whitespace_tokens, "Count:", len(whitespace_tokens))
    print("Word-like tokens:", word_tokens, "Count:", len(word_tokens))

print("\nOptional model subword tokenizer:")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
    )
    for text in samples[:2]:
        print(repr(text), "->", model.tokenizer.tokenize(text))
except Exception as error:
    print("Model tokenizer not available. Install sentence-transformers and try again.")
    print("Reason:", error)

print("\nTwo differences:")
print("1. Whitespace splitting keeps punctuation attached to words.")
print("2. The word-like regex removes punctuation and may split contractions.")
print("Normalization risk: changing or removing punctuation can change meaning.")
print("This regex is not a complete multilingual tokenizer.")
