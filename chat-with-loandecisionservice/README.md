## Introduction 
The integration of the Langchain project with ODM, a cutting-edge decision management product, signifies a significant leap forward in the realms of language processing and data-driven decision-making. By combining Langchain's advanced language analysis technology with the powerful capabilities of ODM, users can unlock a multitude of benefits that revolutionize their decision-making processes. This integration offers a seamless and robust solution for businesses looking to harness the power of multilingual data, optimize operations, and drive strategic outcomes. In the following lines, we will explore five compelling advantages that arise from this integration.


## Pre-requisites
  * Python 3.8 or higher
  * docker 
  * An OpenAI account

## Setup Pre-Requisites

### Create a virtual env and install the Python package
```shell
python3 -m venv ~/llmdc
~/llmdc/bin/activate
pip install -r requirements.txt
```

## Run the demo
### Run the ODM for Developers docker image
Open a terminal
```shell
docker run -e USERS_PASSWORD=odmAdmin -e LICENSE=accept -p 9060:9060 -p 9443:9443  -m 2048M --memory-reservation 2048M  -e SAMPLE=true icr.io/cpopen/odm-k8s/odm:8.11
```

### Run the Chat application

Open a new terminal
```shell
export ODM_ADMIN_PASSWORD=odmAdmin
export OPENAI_API_KEY=<OPENAI_API_KEY>
python3 app-loan.py
```


Then open a browser to this url : http://127.0.0.1:7860

Then you can ask queston to the chat bot such as:
   * my name is joe, i want to do a loan of an amount of 100000 with a credit score of 210 with a duration of 100 is it possible?
   * Will it be possible to contract a loan of an amount of 100000 with a credit score of 210 during 10 year ?


### Code explain

1. Extract from the Decision Server the Ruleset definition.
```python
def decisionServiceOperation():

    spec = OpenAPISpec.from_url("http://localhost:9060/DecisionService/rest/v1/mydeployment/1.0/Miniloan_ServiceRuleset/1.0/OPENAPI?format=YAML")

    operation = APIOperation.from_openapi_spec(spec, '/mydeployment/1.0/Miniloan_ServiceRuleset/1.0', "post")
    return operation
operation=decisionServiceOperation()
```

2. Initialize the LLM Agent. Agent make a glue between the LLM and the backend throw LangChain
```python
def initializeLLMAgent(operation):
    llm = OpenAI() # Load a Language Model
    # Manage ODM Basic Authentication 
    message = "odmAdmin:"+os.environ["ODM_ADMIN_PASSWORD"]
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    headers = {
        "Authorization": f"Basic "+base64_message
    }
    odm_requests_wrapper=RequestsWrapper(headers=headers)
    # Load the Decision Operation Swagger definitation in the LLM Model.
    chain = OpenAPIEndpointChain.from_api_operation(
                                                    operation, 
                                                    llm, 
                                                    verify=False,
                                                    requests=odm_requests_wrapper, 
                                                    verbose=True,
                                                    return_intermediate_steps=True)
    return chain
odm_agent = initializeLLMAgent(operation)
```
3. Interact with the Agent
```python
 response['output'] = odm_agent(query) # Query is the user input.
```
