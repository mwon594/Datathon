-- ==========================================
-- RUN THIS IN SNOWFLAKE SNOWSIGHT (WEB UI)
-- ==========================================
USE ROLE ACCOUNTADMIN;

-- 1. Create a dedicated database and schema for this project
CREATE DATABASE IF NOT EXISTS ai_db;
CREATE SCHEMA IF NOT EXISTS ai_db.bedrock_schema;
USE SCHEMA ai_db.bedrock_schema;

-- 2. Create the egress rule allowing traffic out to your Bedrock region
CREATE OR REPLACE NETWORK RULE bedrock_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('://amazonaws.com'); -- Change us-east-1 if needed

-- 3. Securely store your AWS credentials inside Snowflake
CREATE OR REPLACE SECRET aws_bedrock_access_key
  TYPE = GENERIC_STRING
  SECRET_STRING = 'YOUR_AWS_ACCESS_KEY_ID'; -- Replace with real AWS Key

CREATE OR REPLACE SECRET aws_bedrock_secret_key
  TYPE = GENERIC_STRING
  SECRET_STRING = 'YOUR_AWS_SECRET_ACCESS_KEY'; -- Replace with real AWS Secret

-- 4. Create the gateway bundle
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION bedrock_external_access_int
  ALLOWED_NETWORK_RULES = (bedrock_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (aws_bedrock_access_key, aws_bedrock_secret_key)
  ENABLED = TRUE;

-- 5. Build the Python engine function that queries Bedrock
CREATE OR REPLACE FUNCTION invoke_bedrock_claude(prompt_text STRING)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.10'
PACKAGES = ('boto3', 'json')
EXTERNAL_ACCESS_INTEGRATIONS = (bedrock_external_access_int)
SECRETS = ('aws_key' = aws_bedrock_access_key, 'aws_secret' = aws_bedrock_secret_key)
HANDLER = 'call_bedrock'
AS
$$
import boto3
import json
import _snowflake

def call_bedrock(prompt_text):
    aws_key = _snowflake.get_generic_secret_string('aws_key')
    aws_secret = _snowflake.get_generic_secret_string('aws_secret')
    
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )
    
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt_text}]
    }
    
    response = bedrock_runtime.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=json.dumps(payload)
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['content']['text']
$$;

-- 6. Set up a sample table with data to query later
CREATE OR REPLACE TABLE raw_feedback (
    id INT,
    review STRING
);

INSERT INTO raw_feedback VALUES 
(1, 'The product arrived broken. Terrible customer support.'),
(2, 'Incredible service! Extremely happy with my purchase.');
