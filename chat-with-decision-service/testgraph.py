# First we initialize the model we want to use.

import os,json, re
from genai.extensions.langchain import LangChainChatInterface
from genai.schema import TextGenerationParameters, TextGenerationReturnOptions
from genai import Client, Credentials
from typing import Literal
from LoanValidationTool import LoanValidationTool
from langchain_community.llms import Ollama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

import operator
from datetime import datetime
from typing import Annotated, TypedDict, Union

from invokeRuleServer import InvokeRuleServer
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.chat_models import ChatOllama
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain import hub

## Utility section  To be able to call LLM 
def createLLMWatson():
    if not 'GENAI_KEY' in os.environ:
        print('Please set env variable GENAI_KEY to your IBM Generative AI key')
        exit()
    if not 'GENAI_API' in os.environ:
        print('Please set env variable GENAI_API to your IBM Generative AI  endpoint URL')
        exit()
    watson_model=os.getenv("MODEL_NAME","mistralai/mixtral-8x7b-instruct-v01")
    api_key = os.getenv("GENAI_KEY")
    api_url = os.getenv("GENAI_API")

    creds = Credentials(api_key, api_endpoint=api_url)
    params = TextGenerationParameters(decoding_method="greedy", max_new_tokens=400)
    client = Client(credentials=creds)

    llm = LangChainChatInterface(client=client,
            model_id=watson_model, parameters=params)
    return llm

def createLLMLocal():
    ollama_server_url=os.getenv("OLLAMA_SERVER_URL","http://localhost:11434")
    ollama_model=os.getenv("MODEL_NAME","mistral")
    print("Using Ollma Server: "+str(ollama_server_url))
    return ChatOllama(base_url=ollama_server_url,model=ollama_model)



### Utility function to call ODM 
payload=  {
"loan": {
    "amount": 100000,
    "duration": 120,
    "yearlyInterestRate": 5,
    "yearlyRepayment": 3,
    "approved": True,
    "messages": []
},
"borrower": {
    "name": "string",
    "creditScore": 300,
    "yearlyIncome": 3000
    }

}

decisionServer=InvokeRuleServer()


### Utility function to cleanup response from LLM
## Watson X Mistral return \nObservation  so needs to remove it.
def remove_after_curly_brace(s):
    # Use regular expression to match everything up to and including the closing curly brace
    match = re.match(r'(.*?})', s)
    if match:
        return match.group(1)
    else:
        return s


def json_string_to_object(s):
    try:
        # Remove everything after the first closing curly brace
        cleaned_input = s.replace('{{', '{')
        cleaned_string = re.match(r'(.*?})',cleaned_input).group(1)
        # Convert the cleaned JSON string to a Python dictionary
        json_object = json.loads(cleaned_string)
        return json_object
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error decoding JSON: {e}")
        return None



### THE TOOLS to invoke the Rules

@tool
def loanApproval(
    parameters : str
): 
    """check the eligibilty for a loan based on the amount  . Make sure you use a input format similar to the JSON below:
    {{ "amount": "The loan amount", "duration" : "The loan duration" }} """
    print("AM : --"+remove_after_curly_brace(parameters)+"---")
    params = json_string_to_object(remove_after_curly_brace(parameters))
    # Access loan_amount from json_object
    if params:
        loan_amount = params.get('amount')
        duration = params.get('duration')
        print(f"Loan amount: {loan_amount}")  # Output: Loan amount: 12000
        print(f"Duration: {duration}")

        if(loan_amount != None):
            payload['loan']['amount']=loan_amount
        if(duration != None):
            payload['loan']['duration']=duration
        
        print(json.dumps(payload))
        response=decisionServer.invokeRules(payload)
        print("Response from Rules : "+json.dumps(response, indent=2))
        return json.dumps(response, indent=2)


    else:
        print("Failed to decode JSON object")



    # results = [dict(zip(column_names, row)) for row in rows]
    return True




## Then Langgraph
tools = [loanApproval]

tool_executor = ToolExecutor(tools)

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]



## Siwtch to use Local Ollama or Watson
model= createLLMLocal()
#model= createLLMWatson()

prompt = hub.pull("hwchase17/react")

agent_runnable = create_react_agent(model, tools, prompt)

def execute_tools(state):
    print("Called `execute_tools`")
    messages = [state["agent_outcome"]]
    last_message = messages[-1]

    tool_name = last_message.tool

    print(f"Calling tool: {tool_name}")

    action = ToolInvocation(
        tool=tool_name,
        tool_input=last_message.tool_input,
    )
    response = tool_executor.invoke(action)
    return {"intermediate_steps": [(state["agent_outcome"], response)]}


def run_agent(state):
    """
    #if you want to better manages intermediate steps
    inputs = state.copy()
    if len(inputs['intermediate_steps']) > 5:
        inputs['intermediate_steps'] = inputs['intermediate_steps'][-5:]
    """
    agent_outcome = agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


def should_continue(state):
    messages = [state["agent_outcome"]]
    last_message = messages[-1]
    if "Action" not in last_message.log:
        return "end"
    else:
        return "continue"
    
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)


workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent", should_continue, {"continue": "action", "end": END}
)


workflow.add_edge("action", "agent")
app = workflow.compile()


# The Real Call

input_text ="check the eligity for loan. The amount is 1200000$ for 12 years"


inputs = {"input": input_text, "chat_history": []}
results = []
for s in app.stream(inputs):
    result = list(s.values())[0]
    results.append(result)
    print(result)