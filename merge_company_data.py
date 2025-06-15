from pyspark.sql import SparkSession
from pyspark.sql.functions import col, levenshtein, lower, trim, lit, row_number
from pyspark.sql.window import Window

# 1. Start Spark Session
spark = SparkSession.builder \
    .appName("Merge Company Data") \
    .getOrCreate()

# 2. Load Common Crawl and ABR tables from PostgreSQL
db_properties = {
    "url": "jdbc:postgresql://localhost:5432/assignment_firmable",
    "user": "postgres",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

commoncrawl_df = spark.read.jdbc(
    url=db_properties["url"],
    table="commoncrawl_companies",
    properties=db_properties
)

abr_df = spark.read.jdbc(
    url=db_properties["url"],
    table="abn_entities",
    properties=db_properties
)

# 3. Preprocess both dataframes: lowercase and trim
commoncrawl_df = commoncrawl_df.withColumn("clean_name", trim(lower(col("company_name"))))
abr_df = abr_df.withColumn("clean_name", trim(lower(col("company_name"))))

# 4. Cross-join and compute Levenshtein distance
joined_df = commoncrawl_df.crossJoin(abr_df)

joined_df = joined_df.withColumn(
    "distance", levenshtein(col("commoncrawl_df.clean_name"), col("abr_df.clean_name"))
)

# 5. Rank matches by closest distance for each commoncrawl company
window_spec = Window.partitionBy("commoncrawl_df.url").orderBy(col("distance").asc())

ranked_df = joined_df.withColumn("rank", row_number().over(window_spec))
best_matches = ranked_df.filter(col("rank") == 1).filter(col("distance") <= 5)  # adjust threshold

# 6. Select merged schema
final_df = best_matches.select(
    col("abr_df.abn").alias("abn"),
    col("commoncrawl_df.url").alias("url"),
    col("abr_df.company_name").alias("company_name"),
    col("commoncrawl_df.industry").alias("industry"),
    lit("fuzzy_match").alias("source"),
    col("distance").cast("float").alias("match_confidence")
)

# 7. Write merged records back to PostgreSQL
final_df.write.jdbc(
    url=db_properties["url"],
    table="merged_company_data",
    mode="append",
    properties=db_properties
)

print("\u2705 Merged data written to PostgreSQL.")

spark.stop()