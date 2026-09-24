import os

import snowflake.connector


def delete_data():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database="ANNUAL_REPORTS_DB",
        schema="STRUCTURED",
        warehouse="COMPUTE_WH",
    )
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("TRUNCATE ANNUAL_REPORTS_DB.STRUCTURED.OUTPUT")
        cur.execute("TRUNCATE ANNUAL_REPORTS_DB.STRUCTURED.STRATEGIC_PRIORITIES")
        cur.execute("TRUNCATE ANNUAL_REPORTS_DB.STRUCTURED.KEY_RISKS")
        cur.execute("TRUNCATE ANNUAL_REPORTS_DB.STRUCTURED.KEY_OPPORTUNITIES")
        cur.execute("TRUNCATE ANNUAL_REPORTS_DB.STRUCTURED.MAJOR_PROJECTS")
        conn.commit()
    finally:
        if cur is not None:
            cur.close()

        conn.close()


if __name__ == "__main__":
    delete_data()
