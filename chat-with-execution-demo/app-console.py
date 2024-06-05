import ODMAgent,os
from langchain_community.llms import Ollama
from CreateLLM import createLLM
from ODMAgent import initializeLLMAgent
import json
from Utils import formatDecisionResponse
# ollama_server_url=os.getenv("OLLAMA_SERVER_URL","http://localhost:11434")
# ollama_model=os.getenv("MODEL_NAME","mistral")
# print("Using Ollma Server: "+str(ollama_server_url))
# llm = Ollama(base_url=ollama_server_url,model=ollama_model)
             
#              #,temperature=0.1)


llm=createLLM()
query="compute a loan validation rates with an amount of 10000$ , a duration of 10 years and an interest of 0.01."
#print ("Query : "+query)
#pm_agent = initializeLLMAgent(llm,False)
#res =  pm_agent.invoke({'input' : query});
#print("Result from the LLM : "+str(res))

#query="compute a loan validation rates with an amount of 10000$"
pm_agent = initializeLLMAgent(llm,True)
res =  pm_agent.invoke({'input' : query});
print("RES "+str(type(res)))
result=json.loads(res['output'])
for key, items in result.items():
    print("Key" +key)

total_rules_fired = result['__decisionTrace__']['totalRulesFired']
print(total_rules_fired)
print(formatDecisionResponse(result))
#formatDecisionResponse(json.loads(res['output']))
#print("Result from the LLM using Rules : "+res['output'])
