
from langchain_community.llms import Ollama
import os


def createLLMLocal():
    ollama_server_url=os.getenv("OLLAMA_SERVER_URL","http://localhost:11434")
    ollama_model=os.getenv("MODEL_NAME","mistral")
    print("Using Ollma Server: "+str(ollama_server_url))
    return Ollama(base_url=ollama_server_url,model=ollama_model)


