from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pdf_reader
import lookup
import gpt
import json
from openpyxl import Workbook
import openai

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

    print(f"Saved PDF to: {temp_file_path}")

    # PDF processing and GPT interaction code
    chunks = pdf_reader.chunk_pdf(temp_file_path, 4000, 1000)
    keywords = details_needed.split(",")  # Assuming user provides a comma-separated list of details
    print(f"Keywords: {keywords}")
    matches = lookup.find_matches(chunks, keywords)
    print(f"Matches: {matches}")

    response_text = None
    excel_filename = None  # Initialize excel_filename variable

    for i, chunk_id in enumerate(matches.keys()):
        chunk = chunks[chunk_id]
        gpt_response = gpt.answer_question(chunk, details_needed)
        print(f"GPT response: {gpt_response}")

        if gpt_response.get("answer_found"):
            # Store the generated response
            response_text = gpt_response['response']

            # Create a new Excel workbook
            wb = Workbook()
            ws = wb.active

            # Write the response to the Excel workbook
            ws['A1'] = response_text

            # Save the workbook to a file
            excel_filename = "openai_response.xlsx"
            wb.save(excel_filename)
            print(f"Response stored in '{excel_filename}'")
            break

    # Clean up: remove the temporary file
    try:
        os.remove(temp_file_path)
        print(f"Removed temporary file: {temp_file_path}")
    except FileNotFoundError:
        print(f"FileNotFoundError: {temp_file_path} not found")

    # Render the result with a message containing the Excel file name and location
    if excel_filename:
        message = f"Response generated. Excel file stored as '{excel_filename}' in the current directory."
    else:
        message = "Response couldn't be generated. No Excel file created."
    return message

if __name__ == '__main__':
    app.run(debug=True)