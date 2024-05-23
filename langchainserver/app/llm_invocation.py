
# Models Support
# Ollama
from langchain_community.llms import Ollama
# Watson X
from genai.extensions.langchain import LangChainInterface
from genai import Client, Credentials
from genai.text.generation import (
    DecodingMethod,
    TextGenerationParameters,
    TextGenerationReturnOptions,
)

# Common import
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.llm_configuration import ModelConfiguration

from langserve.schema import CustomUserType
class LLMRequest(CustomUserType):
    configname: str
    prompt: str
    value: str

    
class InvocationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class LLMManager:
    def __init__(self, configManager):
        self.configManager = configManager

    def retrieveLLMModel(self,configname):
        config = self.configManager.get_config_by_name(configname)
        print("configname"+configname+str(config))
        if config.model_type is ModelConfiguration.ollama:
            print("Executing with Ollama "+config.model_name)
            return Ollama(base_url=config.url, 
                    model=config.model_name, 
                    temperature=0,
                    )
        if config.model_type is ModelConfiguration.watsonx:
            print("Executing with Watson X")
            creds = Credentials(config.api_key, api_endpoint=config.url)
            client = Client(credentials=creds)
#            params = GenerateParams(decoding_method="greedy")
            return LangChainInterface(
                    model_id=config.model_name,
                    client=client,
                    parameters=TextGenerationParameters(
                        decoding_method=DecodingMethod.SAMPLE,
                        max_new_tokens=1536,
                        min_new_tokens=1,
                        temperature=0.5,
                        top_k=50,
                        top_p=1,
                        return_options=TextGenerationReturnOptions(generated_tokens=True, token_logprobs=True, input_tokens=True),
                    ),
                )
        return None


    def invoke(self, configname):
        print("Start invoking"+configname.prompt)
        
        llm = self.retrieveLLMModel(configname.configname)
        if llm is None:
            print("Error !!!!")
            return "Error configuration name not found."
        
#        template = """Question: {question}

#        Answer: Let's think step by step."""
        prompttpl = PromptTemplate(template=configname.prompt, input_variables=["question"])

        llm_chain = LLMChain(prompt=prompttpl, llm=llm)

 #       question = "Who was the US president in the year the first Pokemon game was released?"
 #       return llm_chain.run(prompt)
        return llm_chain.run(question=configname.value)


