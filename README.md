 Cross-Lingual Information Retrieval (CLIR) System
---

## 📌 Project Overview

This project implements a complete **Cross-Lingual Information Retrieval (CLIR)** system that retrieves relevant Bangla and English news articles across languages.

The system supports:

* English → Bangla retrieval
* Bangla → English retrieval
* Cross-script matching
* Hybrid ranking (Lexical + Semantic + Fuzzy)
* Full IR evaluation (Precision, Recall, MRR, nDCG)

The dataset consists of ~1000 real news articles collected from major Bangladeshi English and Bangla news portals.

---

# 🏗 System Architecture

```
User Query
    ↓
Module B: Query Processing
    ↓
Module C: Retrieval Models
    ↓
Module D: Ranking & Evaluation
    ↓
Ranked Top-K Results
```

---

# 📂 Project Structure

```
CLIR-System/
│
├── data/
│   ├── crawlers/                # News crawlers (Module A)
│   └── processed/               # Final dataset JSON files
│
├── query_processing/            # Module B
│   ├── language_detection.py
│   ├── normalization.py
│   ├── translation.py
│   ├── expansion.py
│   ├── named_entity_mapping.py
│   └── pipeline.py
│
├── retrieval/                   # Module C
│   ├── lexical_bm25.py
│   ├── semantic_embedding.py
│   ├── fuzzy_match.py
│   ├── hybrid_ranker.py
│   └── test_models.py
│
├── evaluation/                  # Module D
│   ├── ranking.py
│   ├── evaluator.py
│   ├── multi_query_runner.py
│   ├── model_comparison.py
│   ├── generate_charts.py
│   └── dataset_metadata.py
│
└── README.md
```

---

# 📦 Module A — Dataset Construction & Indexing

### ✔ Crawling

Collected articles from:

**English Sources**

* The Daily Star
* Dhaka Tribune
* New Age
* Daily Sun
* New Nation

**Bangla Sources**

* Prothom Alo
* Bangla Tribune
* Kaler Kantho

### ✔ Final Dataset

* English Articles: ~330
* Bangla Articles: ~643
* Total: ~973 articles

Stored as:

```
data/processed/english_docs.json
data/processed/bangla_docs.json
```

Each document contains:

```json
{
  "title": "...",
  "url": "...",
  "content": "...",
  "language": "en/bn",
  "source": "...",
  "category": "..."
}
```

---

# 🔎 Module B — Query Processing & Cross-Lingual Handling

Implemented pipeline:

### 1️⃣ Language Detection

Automatically detects:

* English (`en`)
* Bangla (`bn`)

### 2️⃣ Normalization

* Lowercasing
* Whitespace cleanup

### 3️⃣ Translation (Required)

* Query translated to opposite language
* Used open-source translation approach
* Both original + translated query used

### 4️⃣ Query Expansion

* English: WordNet synonyms
* Bangla: morphological/root-based expansion

### 5️⃣ Named Entity Mapping

Example:

* Bangladesh ↔ বাংলাদেশ
* Dhaka ↔ ঢাকা

This improves cross-lingual matching.

---

# 🧠 Module C — Retrieval Models

Implemented and compared:

---

## 📘 Model 1: Lexical Retrieval

### BM25

* Used `rank_bm25`
* Strong exact term matching

### TF-IDF

* Classic vector-space retrieval

🔍 Limitation:

* Fails for synonyms
* Cannot handle paraphrases
* Weak cross-lingual matching

---

## 📗 Model 2: Fuzzy / Transliteration Matching

* Levenshtein similarity
* Partial string ratio
* Handles:

  * Bangladesh ↔ Bangla Desh
  * বাংলাদেশ ↔ Bangladesh

🔍 Limitation:

* Weak semantic understanding
* Surface-level matching only

---

## 📙 Model 3: Semantic Retrieval (Mandatory)

Used:

```
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

* Multilingual embedding model
* Cosine similarity ranking
* Handles paraphrases & cross-lingual similarity

Strength:

* Captures semantic meaning
* Works across languages

Weakness:

* Slower than lexical
* Needs embedding computation

---

## 📒 Model 4: Hybrid Ranking

Combined:

```
Final Score =
0.3 × BM25 +
0.5 × Embedding +
0.2 × Fuzzy
```

All scores normalized to [0, 1].

This improved both precision and recall.

---

# 📊 Module D — Ranking, Scoring & Evaluation

---

## 🔢 Ranking & Confidence

* Outputs Top-K documents
* Scores normalized between 0 and 1
* Low-confidence warning if:

```
Top Score < 0.20
```

Example:

```
⚠ Warning: Retrieved results may not be relevant.
Matching confidence is low.
```

---

## ⏱ Performance Measurement

System reports:

* Retrieval time (ms)
* Average per query time

Average retrieval time:

```
~120 ms
```

---

# 📈 Evaluation Metrics (20 Queries)

Evaluated on 20 manually labeled queries.

Metrics:

| Metric       | Description               |
| ------------ | ------------------------- |
| Precision@10 | Relevant in top 10        |
| Recall@50    | Coverage of relevant docs |
| MRR          | Rank of first relevant    |
| nDCG@10      | Rank-sensitive relevance  |

---

# 📊 Model Comparison Results

| Model     | Precision@10 | Recall@50 | MRR      | nDCG@10  |
| --------- | ------------ | --------- | -------- | -------- |
| BM25      | 0.17         | 0.64      | 0.61     | 0.50     |
| Embedding | 0.20         | 0.81      | 0.71     | 0.63     |
| Hybrid    | **0.27**     | **1.00**  | **0.75** | **0.78** |

✅ Hybrid model performs best.

---

# 🔬 Ablation Study

| Configuration        | Result           |
| -------------------- | ---------------- |
| BM25 only            | Good exact match |
| Embedding only       | Strong semantic  |
| Hybrid without fuzzy | Slight drop      |
| Hybrid full          | Best performance |

Conclusion:
Embedding improves recall.
BM25 improves precision.
Hybrid balances both.

---

# ❌ Error Analysis

### 1️⃣ Translation Failure

Bangla query mistranslated → irrelevant English retrieval.

### 2️⃣ Named Entity Mismatch

ঢাকা vs Dhaka not matched if NE mapping disabled.

### 3️⃣ Semantic vs Lexical Win

Query: শিক্ষা
BM25: weak
Embedding: retrieves school-related docs.

### 4️⃣ Cross-Script Ambiguity

Bangla Desh vs Bangladesh

### 5️⃣ Code-Switching

Query mixing English + Bangla partially handled.

---

# 📦 Dataset Metadata

Generated using:

```
python -m evaluation.generate_dataset_metadata
```

Produces:

```
evaluation/dataset_metadata.csv
```

Includes:

* title
* url
* language
* source
* category
* word_count
* content_length

---

# ▶ How To Run

### Run Retrieval Test

```
python -m retrieval.test_models
```

### Run Multi-query Evaluation

```
python -m evaluation.multi_query_runner
```

### Compare Models

```
python -m evaluation.model_comparison
```

### Generate Charts

```
python -m evaluation.generate_charts
```

---

# 🧪 Technologies Used

* Python 3.10
* rank_bm25
* scikit-learn
* sentence-transformers
* pandas
* numpy
* matplotlib
* nltk
* fuzzywuzzy

---

# 🎯 Key Contributions

* Full end-to-end CLIR system
* Hybrid ranking model
* Cross-lingual embedding retrieval
* Evaluation with 20 queries
* Error analysis & performance study
* Professional modular architecture

---

# 📌 Final Conclusion

This project demonstrates:

* Lexical methods alone are insufficient for cross-lingual retrieval.
* Embedding-based retrieval significantly improves semantic matching.
* Hybrid ranking provides the best balance.
* Proper query processing (translation + NE mapping + expansion) is critical.

The system achieves:

* Precision@10 ≥ 0.27
* Recall@50 = 1.00
* nDCG@10 ≥ 0.78

This satisfies the assignment performance targets.

---

# 👨‍💻 Author

**Ashfak Azad Nafi**
CSE – 4th Year
Cross-Lingual Information Retrieval Assignment

---
