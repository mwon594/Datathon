import json
from pathlib import Path

import jsonschema.exceptions
from jsonschema import validate

from src.ai_processed_data_pipeline.awsinterface import (
    aws_call,
    get_schema,
    json_response,
)
from src.ai_processed_data_pipeline.snowflake_db_interface import send_snowflake


def main():
    unstructured_files = list(Path("unstructured_data").iterdir())
    schema = get_schema()
    for file in unstructured_files:
        print(f"Processing {file.name}")
        for _ in range(5):
            aws_response = aws_call(schema, file)
            json_text = json_response(aws_response)
            try:
                json_data = json.loads(json_text)
                validate(instance=json_data, schema=schema)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format.")
            except jsonschema.exceptions.ValidationError as e:
                print(f"Validation Error: {e.message}")
            except jsonschema.exceptions.SchemaError as e:
                print(f"Schema Error: The schema itself is invalid: {e.message}")
                raise
            else:
                break
        else:
            print("Failed to get valid JSON after 5 attempts.")
            continue

        try:
            send_snowflake(json_data)
        except:
            with open("output.json", "w", encoding="utf-8") as f:
                f.write(json_text)

            raise


if __name__ == "__main__":
    main()
