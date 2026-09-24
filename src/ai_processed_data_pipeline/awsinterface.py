"""Interaction with AWS
Call to AWS
- JSON SCHEMA
- AWS (Bedrock) invoke
"""

import json
from pathlib import Path

import boto3
from dotenv import load_dotenv
from jsonschema import validate

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


def aws_call(schema, filepath: Path | str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    text = Path(filepath).read_text(encoding="utf-8")

    prompt = f"""You are extracting structured data from a New Zealand energy annual report. 
                Use this JSON schema:{json.dumps(schema, indent=2)} that defines the keys. Use the text to find value.
                Here is the unstructured annual report text {text}: Extract the values from the report according to the schema.
                Return valid json which matches the provided json schema.
            """

    response = client.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )

    return response


def json_response(aws_response):
    text: str = aws_response["output"]["message"]["content"][0]["text"]
    return text.removeprefix("```json").removesuffix("```").strip()


def validate_json(schema, json_string: str):
    json_data = json.loads(json_string)
    validate(instance=json_data, schema=schema)
