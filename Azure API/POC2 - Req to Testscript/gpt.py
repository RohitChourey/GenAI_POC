from dotenv import load_dotenv
from openai import AzureOpenAI
import json
import os

load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")        
azure_oai_key = os.getenv("AZURE_OAI_KEY")        
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT") 

client = AzureOpenAI(                
    azure_endpoint = azure_oai_endpoint,                 
    api_key=azure_oai_key,                  
    api_version="2023-05-15"                
    )


def answer_question_excel(chunk):
    prompt = f"""```
{chunk}
```

Based on the above reuirement, generate test Script. generate test steps to Cover Negative scenarios, generate test steps to Cover Performance test, generate test steps to Cover security test,
generate test steps to Cover functional test, etc.

```
```"""

    response = client.chat.completions.create(model=azure_oai_deployment,
    messages=[
        {
            "role": "system",
            "content": "Always generate the detailed testScript based on requirement given"
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    functions=[
        {
            "name": "give_response",
            "description": "Use this function to give the response",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The full response to the requirement"
                    }
                }
            },
            #"required": ["answer_found"]
        }
    ])

    return response.choices[0].message.content

def answer_question_feature(chunk):
    prompt = f"""```
{chunk}
```

Based on the above reuirement, generate test Script feature file for cucumber automation. generate test steps to Cover Negative scenarios, generate test steps to Cover Performance test, generate test steps to Cover security test,
generate test steps to Cover functional test, etc.

```
```"""

    response = client.chat.completions.create(model=azure_oai_deployment,
    messages=[
        {
            "role": "system",
            "content": "Always generate the detailed testScript based on requirement given"
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    functions=[
        {
            "name": "give_response",
            "description": "Use this function to give the response",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The full response to the requirement"
                    }
                }
            },
            #"required": ["answer_found"]
        }
    ])

    return response.choices[0].message.content