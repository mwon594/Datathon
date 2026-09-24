'''
Maybe, we need to WRITE each output of LLM to a file. ( As we call each llm for each key).

Write a function that takes outputs of AI(LLM-BEDROCK AWS) and converts it into JSON.
The return type is JSON file.
The parameters are list of keys [] and txt file of all values.

The output of LLM is a txt file. So parameter for func is the file path. NEED to open based on file path. 

Associate keys with value. 

'''
import json

def function_name (keys, filepath: str):
    # Need to open & read file (RECALL CS 101)
    with open(filepath, "r", encoding="utf-8") as file:
        values = [line.strip() for line in file]

    data = []
    # Outer loop is each company
    for i in range(0, len(values), len(keys)):
        record = {}
        for j in range(len(keys)):
            record[keys[j]] = values[i + j]
        data.append(record)

    output = filepath.replace('.txt', '.json')

    with open(output, "w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4)

    return output
    



