# Databricks notebook source
spark.sql("""
CREATE SCHEMA IF NOT EXISTS researchgpt
""")

# COMMAND ----------

spark.sql("USE researchgpt")


# COMMAND ----------

spark.sql("SELECT current_schema()").show()

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS users (
    user_id STRING,
    user_name STRING
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS learning_goals (
    goal_id STRING,
    user_id STRING,
    goal_text STRING,
    created_at TIMESTAMP
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS papers (
    paper_id STRING,
    title STRING,
    abstract STRING,
    publication_year INT,
    cited_by_count INT
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS authors (
    author_id STRING,
    author_name STRING
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id STRING,
    author_id STRING
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS collections (
    collection_id STRING,
    collection_name STRING
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS collection_papers (
    collection_id STRING,
    paper_id STRING
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS reading_progress (
    paper_id STRING,
    status STRING,
    updated_at TIMESTAMP
)
USING DELTA
""")

# COMMAND ----------

spark.sql("""
CREATE TABLE IF NOT EXISTS notes (
    note_id STRING,
    paper_id STRING,
    note_text STRING,
    created_at TIMESTAMP
)
USING DELTA
""")

# COMMAND ----------

spark.sql("SHOW TABLES").show(truncate=False)