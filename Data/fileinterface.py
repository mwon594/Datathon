''' Upload files to snowflake'''

import os
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv

def upload_file(file_path):
    conn = snowflake.connector.connect(user = os.getenv('SNOWFLAKE_USER'),
                                password = os.getenv("PASSWORD"),
                                account = os.getenv("SNOWFLAKE_ACCOUNT"),
                                database="ANNUAL_REPORTS_DB",
                                schema="RAW")

    try:
        path = Path(file_path).resolve()
        cur = conn.cursor()

        cur.execute(f"""PUT 'file://{path.as_posix()}' 
        @ANNUAL_REPORTS_DB.RAW.ANNUAL_REPORT_FILES
        AUTO_COMPRESS = FALSE
        OVERWRITE = TRUE""")

        print(f"{path.name}")  

    finally:
        cur.close()
        conn.close()


load_dotenv()
path = r"C:\Users\mwong\OneDrive\Documents\DataEvent\Datathon\output.txt"

upload_file(path)

