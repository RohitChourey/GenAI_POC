from flask import Flask, render_template, request
from openpyxl import Workbook
import os
import PyPDF2
from dotenv import load_dotenv
from openai import AzureOpenAI
import datetime
import gpt

#Load the environment variables

load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")        
azure_oai_key = os.getenv("AZURE_OAI_KEY")        
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT") 

client = AzureOpenAI(                
    azure_endpoint = azure_oai_endpoint,                 
    api_key=azure_oai_key,                  
    api_version="2023-05-15"                
    ) 

#Launch Flask Application

app = Flask(__name__)

if not azure_oai_key:
    print("ERROR: OpenAI API key not found.")
    exit()


#Split PDF data into Chunks


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


# Generate Test Scripts from LLM

def generate_test_scripts(chunks):
    # """
    # Generate test scripts based on the chunks of text using OpenAI.
    # """
    test_scripts = ""
    test_feature = ""
    for chunk in chunks:
        gpt_response_excel = gpt.answer_question_excel(chunk)
        get_response_feature = gpt.answer_question_feature(chunk)
        test_scripts += gpt_response_excel + "\n\n"
        test_feature += get_response_feature + "\n\n"
    return test_scripts, test_feature


# Write response into Excel

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


# Write Response to feature file

def write_to_feature_file(test_feature, feature_filename):
    """
    Write the generated test scripts to an feature file.
    
    """

    with open(feature_filename, 'w') as f:
        f.write(test_feature)


# Render page

@app.route('/')
def index():
    return render_template('index.html')

# Conversation function

@app.route('/process_conversation', methods=['POST'])
def process_conversation():
    pdf_file = request.files['pdf_file']

    # Save the uploaded file to a temporary location
    temp_file_path = "temp_upload.pdf"
    pdf_file.save(temp_file_path)

    # Split the PDF into chunks
    print('starting chunk')
    chunks = split_pdf_into_chunks(temp_file_path)

    # Generate test scripts using OpenAI
    print('starting to write test_scripts')
    test_scripts, test_feature = generate_test_scripts(chunks)


    # Write test scripts to Excel
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
    excel_filename = f"test_scripts_{timestamp}.xlsx" 
    write_to_excel(test_scripts, excel_filename)

    # Write test scripts to feature fiie
    feature_filename = f"feature_file_{timestamp}.feature" 
    write_to_feature_file(test_feature, feature_filename)

    # Clean up: remove the temporary PDF file
    os.remove(temp_file_path)

    # Render the result on the HTML page
    message = f"Test case generated. files stored as '{excel_filename}' and '{feature_filename}'"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
