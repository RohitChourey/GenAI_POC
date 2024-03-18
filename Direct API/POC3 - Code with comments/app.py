from flask import Flask, request, jsonify, render_template
import os
import datetime
import openai

app = Flask(__name__)

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_model = "gpt-3.5-turbo-instruct"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file.filename == '':
            raise ValueError('No file selected')

        if file and file.filename.endswith('.txt'):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"comments_{timestamp}.txt"
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            comments = process_rpg_source_file(filepath)

            return comments

    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 400

def process_rpg_source_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    # Divide source code into chunks
    code_chunks = chunk_code(source_code)
    
    # Generate comments for each chunk and concatenate them
    comments = ''
    for chunk in code_chunks:
        comments += generate_comments(chunk) + '\n\n'
    
    # Add timestamp to filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"comments_{timestamp}.txt"

    # Write comments to output file
    with open(output_file, 'w') as file:
        file.write(comments)

    return output_file

def chunk_code(code):
    tokens = code.split()
    chunked_code = ['']
    chunk_index = 0
    token_count = 0
    for token in tokens:
        token_count += len(token) + 1  # Add 1 for space
        if token_count > 4000:
            chunk_index += 1
            chunked_code.append('')
            token_count = len(token) + 1
        chunked_code[chunk_index] += token + ' '
    return chunked_code

def generate_comments(code_chunk):
    prompt = """
        This is a RPG source code.
        It needs to be commented to explain the logic.
        Response should contain code and comment explaining code logic
        The code chunk is as follows:
        ```rpg
    """ + code_chunk + """
        ```
        First explain in brief about code logic in simple english. Then follow the code and comment against each code line. After that, same logic in python language.
        """
    response = openai.completions.create(
        model= gpt_model,
        prompt=prompt,
        max_tokens=1500
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(port=5002, debug=True)
