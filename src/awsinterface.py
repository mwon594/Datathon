''' Interaction with AWS
    Call to AWS
    - JSON SCHEMA
    - AWS (Bedrock) invoke
'''
import json
from pathlib import Path
import boto3
import json
import os 
from dotenv import load_dotenv

load_dotenv()
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = "bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUFYTFczTzVJTUFMQ0ZENFg0JTJGMjAyNjA5MjQlMkZ1cy1lYXN0LTElMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA5MjRUMTA0NzA0WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFQXNhQ1hWekxXVmhjM1F0TVNKSU1FWUNJUUNaelJSVTNSQ1Ywb1hwTnFZbDhKYjZsQXlaOTR0MERLSlhqbzRKJTJGc05ZZXdJaEFPNDhuTCUyRld3ZCUyQlZmMXU4QVNFY3NKTlBucFo0eGFIOEpnM0lDUGxkQ2ExeEtxNERDTlQlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RVFBQm9NTlRBMk1Ua3lOalV5T0RJMElnelRlQVVWMGJDQTl2R21oSUlxZ2dNV2R0TzN3alo2d0NnNmtwVUhTaFkyJTJCalpEaVk3MmNjWUFtekNNeUdMYU9XaFhoWU44WDV6JTJGeTBnYnhSZGJ3ZjlKdnN0V2hIc0JjYUdoM1Uya051OGJRRTklMkZ4TjhIS0dGejl1Q3czaGt4WHZLcTRBU1J1RiUyQjNUczFZTWxvYks4bm1UQmQ2em5nJTJCSU9wRjhFVURkY3dqdTlmVkJoOUI2dXhWeEJxc25hdVQlMkZJaUglMkIlMkIlMkJta0hISDlGMDlxZml1ZHZHa1c2ejZ6WHBpRUlGNjZZdSUyQkVwZkdzUEZ3bzB4Q0gzSTBhalpsR3hSOTNxR0ZQanlrVjNpUjZVUzVEVDdObUx1SkE5b0d0UWZpRCUyRjN5aSUyRjV5Y2JoVk5VS0FsWjRndzFHOHFnOVM4M2FONGZMNDdEd2huOUZodGRvRnElMkJmR2hpNVRFWGQlMkYxTmoxWjh3bzR3dlhpZm1jSlprdlFqWXYwSzFuOFo2djJJSlI0YUJqVTc2SjVreUttWmFjJTJGSyUyQkVKVVVObWx0dVI5WFpCaHU5VnRTVHZqSWVIUEdBdzVnenZ4SUNKRExqWWRFTVAlMkY5aXJzUXVXbjIlMkZPNTIlMkZBWGtxWTJKSG9VSSUyRjNmVndDYXdXY0JmSHVjNGV3WkxDN1lMMklZb3hmUTU2V3gyc3dwR3pLciUyQlhQUzBiZVQwMnVab0NBejFRS1RDUSUyQk5QVkJqcmRBakJiVDQ3eHptakJqbUpoSTh6VG5ZUEhUT2lsWkpiNnFVaFZacElQd2tWQXF4WEpNS3pYaVJ1Mzc4aEtCWTVwcFB0OE1CY2o2Z0dqdnlQWEs4SlUlMkZGVXA1bll4eGU3cUdGQmdpeWp5bFRYNDh6akJoM2lxYzFMWXQ3WXA5VFolMkZMN2VXcEQ2M0dEZzdIQUkyZldkOUg1JTJGd3kzQSUyQjM4cm0wM0MlMkIzTnp0dWhTeFhpUGhjTVhHMTNRU1diTUtWbkY2dU9sUWpSTGJXZGRzdzlCTHcwRVNVcllTbkNWYmFEQSUyQmoyJTJGMkh1Z3N6QnclMkJrZkJlaEdYOTFkbFgweUxyYnhLVnBoVFREdld5dHIxdWpZcXZtTHlUSzclMkZ5OFFQeGR6Q01zSnolMkZnSEs3R1NzWUxhZmxPZGQlMkJ0S0prOFNyZE1uOE90MFJTZmJ6UmRPYnVLSjZKU21zUE52UDZJbDFSa0xZZzNVZ2pCRXBKaGlab1lHRFR2U1d3dnJhSzhjeDglMkZibHI4NnNWRUF1dGg4N2FXMSUyRmNDZ3dvRTIlMkZOdmd6RzEwQkNzN1QlMkJ6WDJOMTVPJTJCNkYwMlRhV0w0Vml6cHZtdkx3cUwwcm42bnZNVGxZVktMSmtSVUI0JTNEJlgtQW16LVNpZ25hdHVyZT1kYzUxMmE5NzgxZTkwMWRhMjk0N2EzNzQwYjcyMTg1YzJkYWZiMGU0YmVjMTZlZTM3NmMyZWEyZDFmZWQzMGQ1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZWZXJzaW9uPTE="

# Get the files
def load_unstructured_files():
    path = Path("Datathon/unstructured_data")

    files = []
    for file_path in path.iterdir():
        files.append(file_path)
    return files


# Get the schema in Dict
def get_schema():
    path = Path("nz_energy_annual_report_schema_typed.json")
    with path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    return schema

'''
def aws_call(schema, files):
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1"
    )
'''

client = boto3.client("bedrock-runtime", region_name="us-east-1")  

response = client.converse( 
    modelId="amazon.nova-lite-v1:0",
    messages=[ 
        { 
            "role": "user", 
            "content": [{"text": "Write a one-sentence bedtime story about a unicorn."}]
        } 
    ] 
)  


#print(os.getenv("AWS_BEARER_TOKEN_BEDROCK"))

print(response["output"]["message"]["content"][0]["text"])

    


