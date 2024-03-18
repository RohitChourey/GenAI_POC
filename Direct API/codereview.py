import openai
import os
import json

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def review_code_with_openai(code):
    response = openai.chat.completions.create(
        model="davinci-codex",
             messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "could you please review this code and give feedback on how this will impact on system performance",
                    },
                    {
                        "type": "code_review",
                        "code_review": {
                            "code": f"{code}"
                        },
                    },
                ],
            }
    ],
        #prompt=code,
        max_tokens=200,
        temperature=0,
        top_p=1.0,
        n=1
    )
    return response

def main():
    file_path = input("Enter the path to your code file: ")  
    code = get_code_from_file(file_path)

    response = review_code_with_openai(code)
    
    print("Code Review Results:")
    print(json.dumps(response['choices'][0]['text'], indent=4))

if __name__ == "__main__":
    main()
