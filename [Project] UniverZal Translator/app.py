import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)
openai.api_key  = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        )
    return response.choices[0].message["content"]

@app.route('/translate', methods=['POST'])
def translate():
    initial_text = request.form.get("text")
    first_language = request.form.get("from-language")
    second_language = request.form.get("to-language")

    prompt = f"""You are an expert in language translation. 
    I want you to read through through the text input from
    '''{initial_text}''' carefully, Next, you are going to translate it
    from '''{first_language}''', which is that text, to '''{second_language}'''.
    
    If the inputted text in '''{initial_text}''' does not correspond to the
    language placed in '''{first_language}''', please output: "The text does 
    not correspond to the selected language. Please try again."
     
    If the inputted text does correspond, please output the translated text
    selected in '''{second_language}'''."""

    translated_text = get_completion(prompt) 

    return render_template('translator.html', translated_text=translated_text)  

@app.route('/')
def index():
    return render_template('translator.html')

if __name__ == '__main__':
    app.run(debug=True)
