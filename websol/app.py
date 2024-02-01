from flask import Flask, render_template, request, jsonify
import os
import pdf_reader
import gpt
import openai
import lookup

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("ERROR: OpenAI API key not found.")
    exit()

gpt.model = "gpt-3.5-turbo"  # Default model

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

    # PDF processing and GPT interaction code
    chunks = pdf_reader.chunk_pdf(temp_file_path, 4000, 1000)
    keywords = details_needed.split(",")  # Assuming user provides a comma-separated list of details
    matches = lookup.find_matches(chunks, keywords)

    response = {'answer_found': False, 'response': ''}

    for i, chunk_id in enumerate(matches.keys()):
        chunk = chunks[chunk_id]
        response = gpt.answer_question(chunk, details_needed)

        if response.get("answer_found"):
            break

    # Clean up: remove the temporary file
    os.remove(temp_file_path)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
