
import os
from CreateLLMLocal import createLLMLocal
from CreateLLMWatson import  createLLMWatson

def createLLM():
    llm_type = os.getenv("LLM_TYPE","LOCAL_OLLAMA")
    if llm_type == "LOCAL_OLLAMA":
        return createLLMLocal()
    elif llm_type == "WATSONX":
        return createLLMWatson()
    else:
        print ("Env variable LLM_TYPE not defined.")
        return None
    

