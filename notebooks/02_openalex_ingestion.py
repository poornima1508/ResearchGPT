# Databricks notebook source
import requests
import pandas as pd
from pyspark.sql import functions as F

# COMMAND ----------

import os

OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")


# COMMAND ----------

try:

    response = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": "retrieval augmented generation",
            "per-page": 5,
            "api_key": OPENALEX_API_KEY
        },
        timeout=30
    )

    response.raise_for_status()

    print(response.status_code)

except Exception as e:

    print(f"OpenAlex API Error: {e}")

    raise

# COMMAND ----------

def reconstruct_abstract(inverted_index):
    """
    Convert OpenAlex abstract_inverted_index
    into normal readable text.
    """
    
    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort()

    return " ".join([word for position, word in words])

# COMMAND ----------

data = response.json()

print(data.keys())

# COMMAND ----------

print(len(data["results"]))

# COMMAND ----------

for paper in data["results"]:
    print(paper["title"])
    print("-" * 80)

# COMMAND ----------

try:

    response = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": "retrieval augmented generation",
            "per-page": 100,
            "api_key": OPENALEX_API_KEY
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    print(
        f"Returned {len(data['results'])} papers"
    )

except Exception as e:

    print(
        f"OpenAlex API Error: {e}"
    )

    data = {"results": []}

# COMMAND ----------

paper_records = []

for paper in data["results"]:

    paper_records.append({
        "paper_id": paper.get("id"),
        "title": paper.get("title"),
        "abstract": reconstruct_abstract(
            paper.get("abstract_inverted_index")
        ),
        "publication_year": paper.get("publication_year"),
        "cited_by_count": paper.get("cited_by_count")
    })

print(len(paper_records))

# COMMAND ----------

papers_pd = pd.DataFrame(paper_records)

papers_pd.head()

# COMMAND ----------

papers_df = spark.createDataFrame(papers_pd)

display(papers_df)

# COMMAND ----------

papers_df.printSchema()

# COMMAND ----------

spark.sql("""
DESCRIBE researchgpt.papers
""").show(truncate=False)

# COMMAND ----------

from pyspark.sql.functions import col

papers_df = (
    papers_df
    .withColumn(
        "publication_year",
        col("publication_year").cast("int")
    )
    .withColumn(
        "cited_by_count",
        col("cited_by_count").cast("int")
    )
)

# COMMAND ----------

papers_df.printSchema()

# COMMAND ----------

papers_df.write \
    .mode("overwrite") \
    .saveAsTable("researchgpt.papers")

# COMMAND ----------

spark.sql("""
SELECT COUNT(*) AS total_papers
FROM researchgpt.papers
""").show()

# COMMAND ----------

display(
    spark.sql("""
    SELECT *
    FROM researchgpt.papers
    LIMIT 5
    """)
)

# COMMAND ----------

author_records = []
paper_author_records = []

for paper in data["results"]:

    paper_id = paper.get("id")

    for authorship in paper.get("authorships", []):

        author = authorship.get("author")

        if author:

            author_id = author.get("id")
            author_name = author.get("display_name")

            author_records.append({
                "author_id": author_id,
                "author_name": author_name
            })

            paper_author_records.append({
                "paper_id": paper_id,
                "author_id": author_id
            })

print(f"Authors extracted: {len(author_records)}")
print(f"Relationships extracted: {len(paper_author_records)}")

# COMMAND ----------

authors_df = spark.createDataFrame(author_records)

authors_df = authors_df.dropDuplicates(["author_id"])

display(authors_df)

# COMMAND ----------

paper_authors_df = spark.createDataFrame(
    paper_author_records
)

display(paper_authors_df)

# COMMAND ----------

authors_df.write \
    .mode("overwrite") \
    .saveAsTable("researchgpt.authors")

# COMMAND ----------

paper_authors_df.write \
    .mode("overwrite") \
    .saveAsTable("researchgpt.paper_authors")

# COMMAND ----------

spark.sql("""
SELECT COUNT(*) AS total_authors
FROM researchgpt.authors
""").show()

# COMMAND ----------

spark.sql("""
SELECT COUNT(*) AS total_relationships
FROM researchgpt.paper_authors
""").show()