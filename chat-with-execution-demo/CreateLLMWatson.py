
import os
from genai.extensions.langchain import LangChainChatInterface
from genai.schema import TextGenerationParameters, TextGenerationReturnOptions
from genai import Client, Credentials

def createLLMWatson():
    if not 'GENAI_KEY' in os.environ:
        print('Please set env variable GENAI_KEY to your IBM Generative AI key')
        exit()
    if not 'GENAI_API' in os.environ:
        print('Please set env variable GENAI_API to your IBM Generative AI  endpoint URL')
        exit()
    watson_model=os.getenv("MODEL_NAME","meta-llama/llama-2-70b-chat")
    api_key = os.getenv("GENAI_KEY")
    api_url = os.getenv("GENAI_API")

    creds = Credentials(api_key, api_endpoint=api_url)
    params = TextGenerationParameters(decoding_method="greedy", max_new_tokens=400)
    client = Client(credentials=creds)

    llm = LangChainChatInterface(client=client,
            model_id=watson_model, parameters=params)
    return llm
