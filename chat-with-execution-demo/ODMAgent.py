

from LoanValidationTool import LoanValidationTool

import prompts
import langchain

from langchain.memory import ConversationBufferWindowMemory

from langchain_core.prompts import PromptTemplate

from langchain.agents import AgentExecutor, create_structured_chat_agent

def initializeLLMAgent(llm,with_tool):
        tools=[]
        if with_tool:
            tools = [LoanValidationTool()];
     #   memory = ConversationBufferWindowMemory(
     #   memory_key="chat_history", k=5, return_messages=True, output_key="output"
     #   )

        template = "\n\n".join(
            [
                prompts.PREFIX,
                "{tools}",
                prompts.FORMAT_INSTRUCTIONS,
                prompts.SUFFIX,
            ]
        )
        prompt = PromptTemplate.from_template(template)
 #       print("Template"+template)
#        langchain.debug=True
        agent = create_structured_chat_agent(llm, tools,prompt=prompt)

        pm_agent = AgentExecutor(agent=agent, 
                                 tools=tools, 
#                                 verbose=True, 
                                 early_stopping_method="generate")
#                                 memory=memory)
        return pm_agent;