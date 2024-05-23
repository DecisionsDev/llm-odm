from fastapi import FastAPI
from langchain.schema.runnable import RunnableLambda
from app.llm_configuration import ServerConfigManager

from app.llm_invocation import LLMManager

from app.llm_invocation import LLMRequest
from app.llm_configuration import ServerConfig

from langserve import add_routes
import json
from json import JSONEncoder

app = FastAPI()

manager = ServerConfigManager("serverconfig.json")
manager.load_configs()  # Charger les configurations existantes
configs = manager.get_configs()
for config in configs:
    print(f"Name: {config.name}, URL: {config.url}, modelName: {config.model_name} ")

llmManager = LLMManager(manager)

@app.get("/configuration/")
async def read_configuration():
    return manager.get_configs()

# This line defines a new route with the POST method and the URL "/configuration/"
@app.post("/configuration/")
# The function create_item takes one argument, an instance of ServerConfig named item
async def create_item(item: ServerConfig):
    # Check if manager successfully updates the configuration with the given item
    if manager.update_config(item) == False:
        # If update fails, add the new configuration to the configs list
        manager.add_config(item)
    # Save the updated configuration list to the file
    manager.save_configs()
    return item

################
## Invocation ##      
################

def inkokeLLM(llmrequest: LLMRequest) -> str:
    """Invoke LLM """
    assert isinstance(llmrequest, LLMRequest)
    return llmManager.invoke(llmrequest)

# Note that the input and output type are automatically inferred!
# You do not need to specify them.
#
add_routes(app, RunnableLambda(inkokeLLM), path="/llmodmservice")