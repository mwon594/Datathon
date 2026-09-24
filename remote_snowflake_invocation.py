# ==========================================
# RUN FROM YOUR LOCAL TERMINAL / APP SERVER
# ==========================================
import os

import snowflake.connector
from dotenv import load_dotenv

# 1. Load configuration from the local .env file
load_dotenv()

# 2. Establish the remote internet connection to Snowflake
print("Connecting remotely to Snowflake...")
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database="AI_DB",
    schema="BEDROCK_SCHEMA",
    role="ACCOUNTADMIN",
)

cursor = conn.cursor()

try:
    # 3. Define the SQL query that orders Snowflake to process table data through Bedrock
    sql_query = """
    SELECT 
        id, 
        review, 
        invoke_bedrock_claude(CONCAT('Is this text Positive or Negative? text: ', review)) as sentiment
    FROM raw_feedback;
    """

    print("Executing remote query. Snowflake is processing data through AWS Bedrock...")
    cursor.execute(sql_query)

    # 4. Fetch the computed data back down to your local terminal
    results = cursor.fetchall()

    print("\n--- RESULTS RECEIVED FROM REMOTE RUN ---")
    for row in results:
        print(f"ID: {row[0]} | Review: '{row[1]}' | AI Sentiment: {row[2].strip()}")

finally:
    cursor.close()
    conn.close()
    print("\nConnection closed safely.")
