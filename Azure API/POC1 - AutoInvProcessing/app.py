from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pdf_reader
import lookup
import gpt
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")        
azure_oai_key = os.getenv("AZURE_OAI_KEY")        
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")  

client = AzureOpenAI(                
    azure_endpoint = azure_oai_endpoint,                 
    api_key=azure_oai_key,                  
    api_version="2023-05-15"                
    )  


app = Flask(__name__)

#openai.api_key = os.getenv("OPENAI_API_KEY")

if not azure_oai_key:
    print("ERROR: OpenAI API key not found.")
    exit()

#gpt.model = "gpt-3.5-turbo"  # Default model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_conversation', methods=['POST'])
def process_conversation():
    pdf_file = request.files['pdf_file']
    details_needed = request.form['details_needed']

    # Save the uploaded file to a temporary location
    temp_file_path = "temp_upload.pdf"
    pdf_file.save(temp_file_path)

    print(f"Saved PDF to: {temp_file_path}")

    # PDF processing and GPT interaction code
    chunks = pdf_reader.chunk_pdf(temp_file_path, 4000, 1000)
    keywords = details_needed.split(",")  # Assuming user provides a comma-separated list of details
    matches = lookup.find_matches(chunks, keywords)

    response = {'fields_and_values': []}

    for i, chunk_id in enumerate(matches.keys()):
        chunk = chunks[chunk_id]
        gpt_response = gpt.answer_question(chunk, details_needed)

        if gpt_response.get("answer_found"):
            # Append the field name and value to the response
            response['fields_and_values'].append({
                'field': details_needed,
                'value': gpt_response['response']
            })
            break

    # Save the output to a JSON file
    output_filename = "output.json"
    with open(output_filename, "w") as json_file:
        json.dump(response, json_file, indent=2)

    # Clean up: remove the temporary file
    try:
        os.remove(temp_file_path)
        print(f"Removed temporary file: {temp_file_path}")
    except FileNotFoundError:
        print(f"FileNotFoundError: {temp_file_path} not found")

    # Render the result on the same page
    print(response)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)