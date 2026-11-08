from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
)

texts = [
    ("short", "Reset my password."),
    ("long", "password " * 300)
]

for label, text in texts:
    token_ids = model.tokenizer(text, truncation=False)["input_ids"]
    fits = len(token_ids) <= model.max_seq_length
    print(label, "tokens:", len(token_ids),
          "limit:", model.max_seq_length, "fits:", fits)
