import os
import openai

openai.api_key = "key_id"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

file_path = "theo-dumpsite_summary.txt"
with open(file_path, "r") as file:
    file_content = file.read()

prompt = f"""Summarize this text file into part so that I can understand it. \n
Provide at least 5 points that I can use when presenting and creating conversation. \n
Make sure that the summary is relevant, concise, and college-appropriate. \n

Text File: {file_content}
"""

response = get_completion(prompt)
print(response)
