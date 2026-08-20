# Databricks notebook source
# MAGIC %pip install sentence-transformers faiss-cpu

# COMMAND ----------

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

print("All libraries loaded successfully")

# COMMAND ----------

papers_df = spark.table("researchgpt.papers")

print(f"Total papers: {papers_df.count()}")

# COMMAND ----------

papers_pd = papers_df.toPandas()

papers_pd.head()

# COMMAND ----------

papers_pd["text_for_embedding"] = (
    papers_pd["title"].fillna("")
    + " "
    + papers_pd["abstract"].fillna("")
)

# COMMAND ----------

papers_pd["text_for_embedding"].iloc[0][:200]

# COMMAND ----------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Model loaded")

# COMMAND ----------

embeddings = model.encode(
    papers_pd["text_for_embedding"].tolist(),
    show_progress_bar=True
)

print(embeddings.shape)

# COMMAND ----------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

print(index.ntotal)

# COMMAND ----------

# DBTITLE 1,Cell 10
def search_papers(query, top_k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append({
            "paper_id": papers_pd.iloc[idx]["paper_id"],
            "title": papers_pd.iloc[idx]["title"],
            "year": papers_pd.iloc[idx]["publication_year"],
            "citations": papers_pd.iloc[idx]["cited_by_count"]
        })

    return results

# COMMAND ----------

results = search_papers(
    "retrieval augmented generation",
    top_k=5
)

results

# COMMAND ----------

for i, paper in enumerate(results, start=1):

    print(f"{i}. {paper['title']}")
    print(f"Year: {paper['year']}")
    print(f"Citations: {paper['citations']}")
    print("-" * 60)

# COMMAND ----------

search_papers(
    "evaluation of retrieval systems"
)


# COMMAND ----------

search_papers(
    "large language models with external knowledge"
)

# COMMAND ----------

search_papers(
    "beginner friendly RAG papers"
)