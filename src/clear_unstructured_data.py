import os

import snowflake.connector
from dotenv import load_dotenv


def delete_files():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database="ANNUAL_REPORTS_DB",
        schema="RAW",
    )
    cur = None
    try:
        cur = conn.cursor()

        cur.execute("""REMOVE @ANNUAL_REPORTS_DB.RAW.ANNUAL_REPORT_FILES;""")

    finally:
        if cur is not None:
            cur.close()
        conn.close()


if __name__ == "__main__":
    load_dotenv()
    delete_files()
