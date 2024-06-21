from langchain.agents.structured_chat.prompt import FORMAT_INSTRUCTIONS

PREFIX = """<s><<SYS>>Assistant is a expert JSON builder designed to assist with a wide range of tasks.

 To answer the question of the user, the assistant can use tools. Tools available to Assistant are:

:<</SYS>>"""
FORMAT_INSTRUCTIONS = """RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please output a response in one of two formats:

**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:

```json
{{{{
    "action": string, \\\\ The action to take. Must be one of {tool_names}
    "action_input": string \\\\ The input to the action
}}}}
```

**Option #2:**
Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:

```json
{{{{
    "action": "Final Answer",
    "action_input": string \\\\ You should put what you want to return to use here in a human readable text.
}}}}
```"""

SUFFIX = """Begin! Remember, all actions must be formatted as markdown JSON strings.Do not add any additional comments.Do not make any greetings, like, Here your response.
  Question: {input}
  Thought:{agent_scratchpad}"""


FORMAT_INSTRUCTIONS_DIRECT=  """RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please output a response with this format:

Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:

```json
{{{{
    "action": "Final Answer",
    "action_input": string \\\\ You should put what you want to return to use here in a human readable text.
}}}}
```"""

SUFFIX_DIRECT = """Do not add any additional comments.Do not make any greetings, like, Here your response.
  Question: {input}
"""

PREFIX_DIRECT = """<s><<SYS>>Assistant is an expert in loan calculation designed to assist with a wide range of tasks.


:<</SYS>>"""

FORMAT_RESPONSE= """
You are Loan advisor. Approved is a boolean. Messages is a list of messages explaining
the loan process. Could you to generate a human response here is this :  {decisionresponse}
"""