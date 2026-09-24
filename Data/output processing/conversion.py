'''
Maybe, we need to WRITE each output of LLM to a file. ( As we call each llm for each key).

Write a function that takes outputs of AI(LLM-BEDROCK AWS) and converts it into JSON.
The return type is JSON file.
The parameters are list of keys [] and txt file of all values.

The output of LLM is a txt file. So parameter for func is the file path. NEED to open based on file path. 

Associate keys with value. 

'''

def function_name (keys,filepath ; str):
    # Need to open & read file (RECALL CS 101)