# Databricks notebook source
spark.sql("""
ALTER TABLE researchgpt.learning_goals
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")

spark.sql("""
ALTER TABLE researchgpt.collections
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")

spark.sql("""
ALTER TABLE researchgpt.collection_papers
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")

spark.sql("""
ALTER TABLE researchgpt.reading_progress
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")

spark.sql("""
ALTER TABLE researchgpt.notes
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")

# COMMAND ----------

spark.sql("""
SHOW TBLPROPERTIES researchgpt.notes
""").show(truncate=False)


# COMMAND ----------

spark.sql("""
DESCRIBE DETAIL researchgpt.notes
""").show(truncate=False)

# COMMAND ----------

spark.sql("""
SHOW CREATE TABLE researchgpt.notes
""").show(truncate=False)

# COMMAND ----------

spark.sql("""
ALTER TABLE researchgpt.notes
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
)
""")


# COMMAND ----------

spark.sql("""
SHOW TBLPROPERTIES researchgpt.notes
""").show(truncate=False)


# COMMAND ----------

tables = [
    "learning_goals",
    "collections",
    "collection_papers",
    "reading_progress"
]

for table in tables:
    spark.sql(f"""
    ALTER TABLE researchgpt.{table}
    SET TBLPROPERTIES (
        delta.enableChangeDataFeed = true
    )
    """)

# COMMAND ----------

spark.sql("""
SHOW TBLPROPERTIES researchgpt.reading_progress
""").show(truncate=False)


# COMMAND ----------

spark.sql("""
CREATE OR REPLACE TABLE researchgpt.activity_analytics AS

SELECT
    'learning_goals' AS activity_type,
    COUNT(*) AS total_records
FROM researchgpt.learning_goals

UNION ALL

SELECT
    'collections',
    COUNT(*)
FROM researchgpt.collections

UNION ALL

SELECT
    'collection_papers',
    COUNT(*)
FROM researchgpt.collection_papers

UNION ALL

SELECT
    'reading_progress',
    COUNT(*)
FROM researchgpt.reading_progress

UNION ALL

SELECT
    'notes',
    COUNT(*)
FROM researchgpt.notes
""")

# COMMAND ----------

display(
    spark.table("researchgpt.activity_analytics")
)