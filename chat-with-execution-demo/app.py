import ODMAgent,os
from langchain_community.llms import Ollama
from ODMAgent import initializeLLMAgent
ollama_server_url=os.getenv("OLLAMA_SERVER_URL","http://localhost:11434")
ollama_model=os.getenv("MODEL_NAME","mistral")
print("Using Ollma Server: "+str(ollama_server_url))
llm = Ollama(base_url=ollama_server_url,model=ollama_model,temperature=0.1)

query="compute a loan validation rates with an amount of 10000$ , a duration of 10 years and an interest of 0.01."
print ("Query : "+query)
pm_agent = initializeLLMAgent(llm,False)
res =  pm_agent.invoke({'input' : query});
print("Result from the LLM : "+res['output'])

#query="compute a loan validation rates with an amount of 10000$"
pm_agent = initializeLLMAgent(llm,True)
res =  pm_agent.invoke({'input' : query});
print("Result from the LLM using Rules : "+res['output'])
