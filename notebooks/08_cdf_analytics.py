# Databricks notebook source
spark.sql("""
DESCRIBE HISTORY researchgpt.notes
""").show(truncate=False)

# COMMAND ----------

cdf_notes = spark.sql("""
SELECT *
FROM table_changes(
    'researchgpt.notes',
    3
)
""")

display(cdf_notes)

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE TABLE researchgpt.activity_cdf AS
SELECT *
FROM table_changes(
    'researchgpt.notes',
    3
)
""")


# COMMAND ----------

display(
    spark.table("researchgpt.activity_cdf")
)