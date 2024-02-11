from openai import OpenAI

client = OpenAI()
import json

model = "gpt-3.5-turbo"

def get_test_scripts(question):
    prompt = f"""I want to generate test scripts based on the following question. Please provide detailed steps or instructions that can be used to test the functionality related to this question.

{question}"""

    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ])

    return response.choices[0].text.strip()

def answer_question(chunk, question):
    prompt = f"""```
{chunk}

Based on the above information, what is the answer to this question?

{question}
```"""

    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "system",
            "content": "Always set test_scripts_generated to false if the test scripts could not be generated based on the provided information."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    functions=[
        {
            "name": "give_response",
            "description": "Use this function to give the response and whether or not the test scripts were generated successfully.",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_scripts_generated": {
                        "type": "boolean",
                        "description": "Set this to true only if the test scripts were successfully generated"
                    },
                    "test_scripts": {
                        "type": "string",
                        "description": "The generated test scripts"
                    }
                }
            },
            "required": ["test_scripts_generated"]
        }
    ])

    return json.loads(response.choices[0].message.function_call.arguments)

def get_keywords(question):
    prompt = f"""I want to find the answer to the following question from a PDF file. Please provide me with 10 keywords and synonyms that I can use to find the information from the PDF. Only one word per keyword. Use only lowercase letters.

{question}"""

    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "system",
            "content": "You will always provide 10 keywords that include relevant synonyms of the words in the original question"
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    functions=[
        {
            "name": "list_keywords",
            "description": "Use this function to give the user a list of keywords",
            "parameters": {
                "type": "object",
                "properties": {
                    "list": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A keyword"
                        },
                        "description": "A list of keywords"
                    }
                }
            },
            "required": ["list"]
        }
    ],
    function_call={
        "name": "list_keywords",
        "arguments": ["list"]
    })

    arguments = response.choices[0].message.function_call.arguments.lower()
    keywords = json.loads(arguments)["list"]

    return " ".join(keywords).split(" ")

