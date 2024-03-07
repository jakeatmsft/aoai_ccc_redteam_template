
from promptflow import tool
from promptflow.connections import AzureOpenAIConnection
import os
from openai import AzureOpenAI



# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(modelname:str, 
                connection: AzureOpenAIConnection, 
                question: str, 
                chat_history: list, 
                metaprompt: str) -> str:
    # This is a simple tool that takes a question and returns the answer
    # The chat_history is a list of previous questions and answers
    # The metaprompt is a string that can be used to guide the model

    client = AzureOpenAI(
    azure_endpoint = connection.api_base, 
    api_key=connection.api_key,  
    api_version="2024-02-15-preview"
    )

    message_text = [
        {"role": "system", "content": metaprompt}]
    
    for chat in chat_history:
        message_text.append(chat)
    
    message_text.append({"role": "user", "content": question})
    
    try:
        completion = client.chat.completions.create(
            model=modelname, # model = "deployment_name"
            messages = message_text,
            temperature=0,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
            )
    except Exception as e:
        err = e.body
        return {"error": err['message'], 'type': err['type'], 'param': err['param'], 'code': err['code'], 'status': err['status']}
    
    return {"output":completion.choices[0].message.content}

