# Databricks notebook source
# MAGIC %pip install sentence-transformers faiss-cpu

# COMMAND ----------

import faiss
import numpy as np
from uuid import uuid4

from sentence_transformers import SentenceTransformer

print("Agent notebook ready")

# COMMAND ----------

papers_df = spark.table("researchgpt.papers")

papers_pd = papers_df.toPandas()

# COMMAND ----------

papers_pd["text_for_embedding"] = (
    papers_pd["title"].fillna("")
    + " "
    + papers_pd["abstract"].fillna("")
)

# COMMAND ----------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# COMMAND ----------

embeddings = model.encode(
    papers_pd["text_for_embedding"].tolist(),
    show_progress_bar=False
)

# COMMAND ----------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

# COMMAND ----------

# DBTITLE 1,Cell 8
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

search_papers(
    "retrieval augmented generation"
)

# COMMAND ----------

def compare_papers(query):

    papers = search_papers(query, top_k=2)

    return {
        "paper_1": papers[0],
        "paper_2": papers[1]
    }

# COMMAND ----------

compare_papers(
    "retrieval evaluation"
)

# COMMAND ----------

USER_ID = str(uuid4())

spark.sql(f"""
INSERT INTO researchgpt.users
VALUES (
    '{USER_ID}',
    'ResearchGPT User'
)
""")

# COMMAND ----------

display(
    spark.table("researchgpt.users")
)

# COMMAND ----------

def save_learning_goal(goal_text):

    goal_id = str(uuid4())

    spark.sql(f"""
    INSERT INTO researchgpt.learning_goals
    VALUES (
        '{goal_id}',
        '{USER_ID}',
        '{goal_text}',
        current_timestamp()
    )
    """)

    return "Goal saved"

# COMMAND ----------

save_learning_goal(
    "Learn Retrieval Augmented Generation"
)


# COMMAND ----------

def add_to_collection(
    paper_id,
    collection_name="RAG Collection"
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

    return "Paper added"

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

    return "Progress updated"

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

    papers = search_papers(
        goal,
        top_k=5
    )

    plan = []

    for day, paper in enumerate(papers, start=1):

        plan.append({
            "day": day,
            "paper": paper["title"],
            "citation": paper["paper_id"]
        })

    return plan

# COMMAND ----------

generate_study_plan(
    "Learn Retrieval Augmented Generation"
)

# COMMAND ----------

results = search_papers(
    "retrieval augmented generation"
)

results

# COMMAND ----------

first_paper_id = results[0]["paper_id"]

print(first_paper_id)

# COMMAND ----------

add_to_collection(first_paper_id)

# COMMAND ----------

mark_completed(first_paper_id)

# COMMAND ----------

save_note(
    first_paper_id,
    "Important paper for understanding RAG."
)

# COMMAND ----------

display(
    spark.table("researchgpt.collections")
)

# COMMAND ----------

display(
    spark.table("researchgpt.collection_papers")
)

# COMMAND ----------

display(
    spark.table("researchgpt.reading_progress")
)


# COMMAND ----------

display(
    spark.table("researchgpt.notes")
)