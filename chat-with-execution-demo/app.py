import gradio as gr
from CreateLLM import createLLM
from ODMAgent import initializeLLMAgent
import os,json
from Utils import formatDecisionResponse
useRules=False
print("Creating the LLMAgent")
llm=createLLM()
def switch_computation(x):
    global useRules
    useRules=x
    return useRules
def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def bot(history):
    response = infer(history[-1][0])
    history[-1][1] = response['result']
    return history

def infer(question):
    query = f'[INST] {question}[/INST]'
    response={}
    print("Infer"+query+ " Use Rules : "+str(useRules))
    pm_agent = initializeLLMAgent(llm,useRules)
    res =  pm_agent.invoke({'input' : query});
    if useRules:
        response['result'] =formatDecisionResponse(json.loads(res['output']))
    else:
        print(str(res))
        response['result'] =str(res)
    return response
  

css="""
#col-container {max-width: 700px; auto; margin-right: auto;}
#resources{
  background-color: rgb(30, 58, 75);
  margin: 1000px 10 10 10;
}
#resources h3{
  color: white;
  font-size: 2rem;
  font-weight: lighter;
  margin: 10px;
  text-align: left;
  }
"""

title = """
        <div id="resources">
        <h3>&nbsp;Loan Validator Chat</h3>
        </div>
"""


with gr.Blocks(css=css) as demo:
    gr.HTML(title)

    chatbot = gr.Chatbot(show_copy_button=True,
                            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))       ))
    with gr.Row():                   
        question = gr.Textbox(label="Question", placeholder="Type your question and hit Enter ")
        check= gr.Checkbox(label="Use Decision Engine", info="Allow to enable the use of Decision Engine")
        check.change(fn=switch_computation, inputs=[check], outputs=[])

        question.submit(add_text, [chatbot, question], [chatbot, question]).then(
            bot, [chatbot], [chatbot]
        )
        

demo.launch(allowed_paths=[], server_name="0.0.0.0",show_api=False,favicon_path=(os.path.join(os.path.dirname(__file__), "avatar.png")))