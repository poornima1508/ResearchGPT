# Databricks notebook source
# MAGIC %pip install sentence-transformers faiss-cpu

# COMMAND ----------

papers_df = spark.table("researchgpt.papers")

print(papers_df.count())
display(papers_df.limit(5))


# COMMAND ----------

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Model loaded")

# COMMAND ----------

papers_pd = papers_df.toPandas()

papers_pd["text_for_embedding"] = (
    papers_pd["title"].fillna("")
    + " "
    + papers_pd["abstract"].fillna("")
)

# COMMAND ----------

embeddings = model.encode(
    papers_pd["text_for_embedding"].tolist(),
    show_progress_bar=True
)

print(embeddings.shape)

# COMMAND ----------

import faiss
import numpy as np

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

print(index.ntotal)

# COMMAND ----------

# DBTITLE 1,Cell 7
def search_papers(query, top_k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append({
            "title": papers_pd.iloc[idx]["title"],
            "year": papers_pd.iloc[idx]["publication_year"]
        })

    return results

# COMMAND ----------

search_papers(
    "beginner friendly papers about retrieval evaluation"
)

# COMMAND ----------

print(embeddings.shape)

# COMMAND ----------

print(index.ntotal)

# COMMAND ----------

search_papers(
    "beginner friendly papers about retrieval evaluation"
)

# COMMAND ----------

search_papers(
    "large language models and knowledge retrieval"
)

# COMMAND ----------

search_papers(
    "improving retrieval augmented generation"
)

# COMMAND ----------

from uuid import uuid4

user_id = str(uuid4())

spark.sql(f"""
INSERT INTO researchgpt.users
VALUES (
    '{user_id}',
    'ResearchGPT User'
)
""")

# COMMAND ----------

display(
    spark.table("researchgpt.users")
)

# COMMAND ----------

from uuid import uuid4
from datetime import datetime

goal_id = str(uuid4())

goal_text = "Learn Retrieval-Augmented Generation"

spark.sql(f"""
INSERT INTO researchgpt.learning_goals
VALUES (
    '{goal_id}',
    '{user_id}',
    '{goal_text}',
    current_timestamp()
)
""")

# COMMAND ----------

display(
    spark.table("researchgpt.learning_goals")
)

# COMMAND ----------

from uuid import uuid4

# COMMAND ----------

def add_to_collection(
        paper_id,
        collection_name="My Collection"
):
    
    collection_id = str(uuid4())

    spark.sql(f"""
    INSERT INTO researchgpt.collections
    VALUES (
        '{collection_id}',
        '{collection_name}'
    )
    """)

    spark.sql(f"""
    INSERT INTO researchgpt.collection_papers
    VALUES (
        '{collection_id}',
        '{paper_id}'
    )
    """)

    return "Paper added successfully"

# COMMAND ----------

def mark_completed(paper_id):

    spark.sql(f"""
    INSERT INTO researchgpt.reading_progress
    VALUES (
        '{paper_id}',
        'COMPLETED',
        current_timestamp()
    )
    """)

    return "Reading progress updated"

# COMMAND ----------

from uuid import uuid4

# COMMAND ----------

def save_note(
        paper_id,
        note_text
):
    
    note_id = str(uuid4())

    spark.sql(f"""
    INSERT INTO researchgpt.notes
    VALUES (
        '{note_id}',
        '{paper_id}',
        '{note_text}',
        current_timestamp()
    )
    """)

    return "Note saved"

# COMMAND ----------

def generate_study_plan(goal):

    recommendations = search_papers(
        goal,
        top_k=5
    )

    plan = []

    for i, paper in enumerate(recommendations, start=1):

        plan.append(
            f"Day {i}: {paper['title']}"
        )

    return plan

# COMMAND ----------

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

papers_df = spark.table("researchgpt.papers")
papers_pd = papers_df.toPandas()

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# COMMAND ----------

papers_pd["text_for_embedding"] = (
    papers_pd["title"].fillna("")
    + " "
    + papers_pd["abstract"].fillna("")
)

embeddings = model.encode(
    papers_pd["text_for_embedding"].tolist(),
    show_progress_bar=False
)

# COMMAND ----------

embedding_rows = []

for i, paper_id in enumerate(papers_pd["paper_id"]):

    embedding_rows.append({
        "paper_id": paper_id,
        "embedding": embeddings[i].tolist()
    })

embeddings_df = spark.createDataFrame(
    embedding_rows
)

# COMMAND ----------

embeddings_df.write.mode(
    "overwrite"
).saveAsTable(
    "researchgpt.paper_embeddings"
)

# COMMAND ----------

display(
    spark.table(
        "researchgpt.paper_embeddings"
    )
)

# COMMAND ----------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

# COMMAND ----------

search_papers("RAG evaluation")

# COMMAND ----------

generate_study_plan(
    "Learn Retrieval-Augmented Generation"
)