

from LoanValidationTool import LoanValidationTool
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import prompts
import langchain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory

from langchain_core.prompts import PromptTemplate

from langchain.agents import AgentExecutor, create_structured_chat_agent
# Define your desired data structure.
class Result(BaseModel):
    action: str = Field(description="Final Answer")
    action_input: str = Field(description="You should put what you want to return to use here in a human readable text.")
def initializeLLMAgent(llm,with_tool):


        if with_tool:
            tools = [LoanValidationTool()];
            memory = ConversationBufferWindowMemory(
            memory_key="chat_history", k=5, return_messages=True, output_key="output"
            )

            template = "\n\n".join(
                [
                    prompts.PREFIX,
                    "{tools}",
                    prompts.FORMAT_INSTRUCTIONS,
                    prompts.SUFFIX,
                ]
            )

            prompt = PromptTemplate.from_template(template)
       #     langchain.debug=True
            agent = create_structured_chat_agent(llm, tools,prompt=prompt)

            pm_agent = AgentExecutor(agent=agent, 
                                    tools=tools, 
    #                                 verbose=True, 
                                    handle_parsing_errors=True,
                                    early_stopping_method="generate",
                                    memory=memory)
            return pm_agent;
        else:
            template = "\n\n".join(
                [
                    prompts.PREFIX_DIRECT,

                    prompts.SUFFIX_DIRECT,
                ]
            )
            prompt = PromptTemplate.from_template(template)
            parser = JsonOutputParser(pydantic_object=Result)
            chain = prompt | llm 
            return chain

