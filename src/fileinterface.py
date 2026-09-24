"""Upload files to snowflake"""
from dotenv import load_dotenv

import os
from pathlib import Path

import snowflake.connector


def upload_file(file_path):
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database="ANNUAL_REPORTS_DB",
        schema="RAW",
    )
    cur = None
    try:
        path = Path(file_path).resolve()
        cur = conn.cursor()

        cur.execute(f"""PUT 'file://{path.as_posix()}' 
        @ANNUAL_REPORTS_DB.RAW.ANNUAL_REPORT_FILES
        AUTO_COMPRESS = FALSE
        OVERWRITE = TRUE""")

        print(f"{path.name}")

    finally:
        if cur is not None:
            cur.close()

        conn.close()


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

        cur.execute(f"""REMOVE @ANNUAL_REPORTS_DB.RAW.ANNUAL_REPORT_FILES;""")

    finally:
        if cur is not None:
            cur.close()
        conn.close()
load_dotenv()
delete_files()