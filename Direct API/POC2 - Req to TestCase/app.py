from flask import Flask, render_template, request
from openpyxl import Workbook
import os
import PyPDF2
from openai import OpenAI
import datetime

app = Flask(__name__)
client = OpenAI()
# Set up OpenAI API key
client.api_key = os.getenv("OPENAI_API_KEY")
if not client.api_key:
    print("ERROR: OpenAI API key not found.")
    exit()

# Set up GPT model
gpt_model = "gpt-3.5-turbo-instruct"  # Change to your desired model


def split_pdf_into_chunks(pdf_file, chunk_size=4000, overlap=1000):
    """
    Split the PDF document into smaller chunks of text with a specified size limit.
    """
    chunks = []
    chunk = ""
    with open(pdf_file, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            chunk += page.extract_text()
            while len(chunk) > chunk_size:
                chunks.append(chunk[:chunk_size])
                chunk = chunk[chunk_size-overlap:]

    if len(chunk):
        chunks.append(chunk)

    return chunks


def generate_test_scripts(chunks):
    """
    Generate test scripts based on the chunks of text using OpenAI.
    """
    test_scripts = ""
    test_feature = ""
    for chunk in chunks:
        #for Excel
        prompt = craft_prompt_excel(chunk)
        response = client.completions.create(
            model=gpt_model,
            prompt=prompt,
            max_tokens=1500,  # Adjust based on the model's token limit
        )
        test_scripts += response.choices[0].text.strip() + "\n\n"
        
        #for Feature
        prompt = craft_prompt_feature(chunk)
        response = client.completions.create(
            model=gpt_model,
            prompt=prompt,
            max_tokens=1500,  # Adjust based on the model's token limit
        )
        test_feature += response.choices[0].text.strip() + "\n\n"

    return test_scripts, test_feature

def craft_prompt_excel(chunk):
    """
    Craft a prompt for generating test scripts based on the chunk of text.
    """
    # You may need to customize this based on your specific requirements
    prompt = f"Generate test scripts for the following scenario:\n\n{chunk}\n\nInclude test cases for negative testing, performance testing, etc."
    return prompt

def craft_prompt_feature(chunk):
    """
    Craft a prompt for generating test case feature file for cucumber based on the chunk of text.
    """
    # You may need to customize this based on your specific requirements
    prompt = f"Generate test case feature file for cucumber automation tool for the following scenario:\n\n{chunk}\n\nInclude test cases for negative testing, performance testing, etc."
    return prompt


def write_to_excel(test_scripts, filename):
    """
    Write the generated test scripts to an Excel file.
    
    """

    wb = Workbook()
    ws = wb.active
    ws['A1'] = "Test Scripts"
    ws.append([""])  # Empty row for spacing
    ws.append(["Test Script"])
    for line in test_scripts.split('\n'):
        ws.append([line])
    wb.save(filename)


def write_to_feature_file(test_feature, filename):
    """
    Write the generated test scripts to an feature file.
    
    """

    with open(filename, 'w') as f:
        f.write(test_feature)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_conversation', methods=['POST'])
def process_conversation():
    pdf_file = request.files['pdf_file']

    # Save the uploaded file to a temporary location
    temp_file_path = "temp_upload.pdf"
    pdf_file.save(temp_file_path)

    # Split the PDF into chunks
    chunks = split_pdf_into_chunks(temp_file_path)

    # Generate test scripts using OpenAI
    test_scripts, test_feature = generate_test_scripts(chunks)
    
    # Write test scripts to Excel
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
    excel_filename = f"test_scripts_{timestamp}.xlsx" 
    feature_filename= f"Feature_file_{timestamp}.feature"
    write_to_excel(test_scripts, excel_filename)
    write_to_feature_file(test_feature, feature_filename)

    # Clean up: remove the temporary PDF file
    os.remove(temp_file_path)

    # Render the result on the HTML page
    message = f"Test case generated. Files stored as '{excel_filename}' and '{feature_filename}'"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
