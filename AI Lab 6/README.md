# Lab 6: NLP Fundamentals

# Requirements
- Python 3.10 or newer
- Internet access for the first sentence-transformers model download
- CPU is enough; no GPU is required

# Install
```bash
python -m venv .venv
```
Windows:
```bash
.venv\\Scripts\\activate
```
macOS/Linux:
```bash
source .venv/bin/activate
```
Then:
```bash
python -m pip install -r requirements.txt
```

# Run the tasks
```bash
python task1_tokens.py
python guided_chatbot.py
python task1_chatbot_check.py
python task2_chunks.py
python guided_chunks.py
python guided_embeddings.py
python guided_limits.py
python guided_metrics.py
python guided_suggestions.py
python task3_retrieval.py
python document_chatbot.py
```

# Scenario scripts
```bash
python scenario1_handbook.py
python scenario2_support.py
python scenario3_docs.py
python scenario4_workplace.py
python scenario5_equipment.py
```

# Important
- The corpus contains synthetic example policies, not real university/company rules.
- TF-IDF is a lexical baseline. The embedding option uses the pretrained MiniLM model.
- `task3_retrieval.py` writes `retrieval_log.csv` with top-3 results, scores, IDs and offsets.
