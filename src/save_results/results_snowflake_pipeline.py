
import os
from pathlib import Path

import snowflake.connector


def send_snowflake(json: dict):
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
        cur.execute("""
            INSERT INTO OUTPUT
            (
                COMPANY_NAME,
                FINANCIAL_YEAR,
                REVENUE_NZD_M,
                EBITDAF_NZD_M,
                NET_PROFIT_NZD_M,
                OPERATING_CASH_FLOW_NZD_M,
                CAPITAL_EXPENDITURE_NZD_M,
                NET_DEBT_NZD_M,
                TOTAL_GENERATION_GWH,
                RENEWABLE_GENERATION_PCT,
                INSTALLED_CAPACITY_MW,
                TOTAL_CUSTOMERS,
                DEVELOPMENT_PIPELINE_MW,
                EMPLOYEES,
                SCOPE_1_EMISSIONS_TCO2E,
                SCOPE_2_EMISSIONS_TCO2E
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
                json["financial_year"],
                json["revenue_nzd_m"],
                json["ebitdaf_nzd_m"],
                json["net_profit_nzd_m"],
                json["operating_cash_flow_nzd_m"],
                json["capital_expenditure_nzd_m"],
                json["net_debt_nzd_m"],
                json["total_generation_gwh"],
                json["renewable_generation_pct"],
                json["installed_capacity_mw"],
                json["total_customers"],
                json["development_pipeline_mw"],
                json["employees"],
                json["scope_1_emissions_tco2e"],
                json["scope_2_emissions_tco2e"]
        ))
        id = cur.fetchone()[0]

        for priority in json["strategic_priorities"]:
            cur.execute("""
                INSERT INTO STRATEGIC_PRIORITIES
                (
                    REPORT_ID,
                    STRATEGIC_PRIORITY
                )
                VALUES (
                    %s, %s
                )
            """, (
                    id,
                    priority,
            ))

        for risk in json["key_risks"]:
            cur.execute("""
                INSERT INTO KEY_RISKS
                (
                    REPORT_ID,
                    KEY_RISK
                )
                VALUES (
                    %s, %s
                )
            """, (
                    id,
                    risk,
            ))

        for opportunity in json["key_opportunities"]:
            cur.execute("""
                INSERT INTO KEY_OPPORTUNITIES
                (
                    REPORT_ID,
                    KEY_OPPORTUNITY
                )
                VALUES (
                    %s, %s
                )
            """, (
                    id,
                    opportunity,
            ))

        for project in json["major_projects"]:
            cur.execute("""
                INSERT INTO MAJOR_PROJECTS
                (
                    REPORT_ID,
                    MAJOR_PROJECT
                )
                VALUES (
                    %s, %s
                )
            """, (
                    id,
                    project,
            ))

        conn.commit()
    finally:
        if cur is not None:
            cur.close()

        conn.close()        
