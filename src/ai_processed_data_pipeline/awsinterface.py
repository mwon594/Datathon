"""Interaction with AWS
Call to AWS
- JSON SCHEMA
- AWS (Bedrock) invoke
"""

import json
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()


# Get the files
def load_unstructured_files():
    path = Path("Datathon/unstructured_data")

    files = []
    for file_path in path.iterdir():
        files.append(file_path)
    return files


# Get the schema in Dict
def get_schema():
    path = Path("nn_schema.json")
    with path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    return schema


def aws_call(schema, filepath):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    text = Path(filepath).read_text()

    prompt = f"""You are extracting structured data from a New Zealand energy annual report. 
                Use this JSON schema:{json.dumps(schema, indent=2)} that defines the keys. Use the text to find value.
                Here is the unstructured annual report text {text}: Extract the values from the report according to the schema.
                Return such that: each line is the value for each key.
            """

    response = client.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )

    return response


schema = get_schema()
resp = aws_call(schema, "output.txt")


def json_to_file(resp):
    text = resp["output"]["message"]["content"][0]["text"]

    text = text.removeprefix("```json").removesuffix("```").strip()

    key_values = json.loads(text)

    with open("formatted.txt", "w", encoding="utf-8") as f:
        f.writelines(f"{key}: {value}\n" for key, value in key_values.items())


json_to_file(resp)
