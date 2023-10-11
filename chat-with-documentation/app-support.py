import gradio as gr
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
# LLM
from langchain.llms import Ollama
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate

from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory

showRequest=False
def checkEnvironment():
    # TODO Verify Data vector is done
    print("Verify data vector.")
        

def initializeLLM():
    # Prompt
    template = """
    Use the following pieces of context to answer the question at the end. 
    You are an expert of the Operational Decision Manager (ODM).
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 

    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    vectordb = Chroma(persist_directory="./data", embedding_function=GPT4AllEmbeddings())
    chain_type_kwargs = {"prompt": QA_CHAIN_PROMPT}
    llm = Ollama(base_url="http://localhost:11434",
                model="mistral",
                verbose=False)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, 
                                                    vectordb.as_retriever(),
                                                    chain_type="stuff",
                                                    combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},                
                                                    memory=memory)
    return qa_chain



# Verify all is ready to use
print("Verifying the environment")
checkEnvironment()


print("Creating the LLM")
qa_chain = initializeLLM()



def show_text(x):
    global showRequest
    showRequest=x
    return showRequest
def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def bot(history):
    response = infer(history[-1][0])
    request=""

    history[-1][1] = f"{request}<span style='color:green'>{response['answer']}</span>"
    return history

def infer(question):
    query = question
#    response={'output': {'instructions': 'my name is lolo, i want to do a loan of an amount of 100000 with a credit score of 210 with a duration of 100 is it possible?', 'output': 'Based on the API response, it looks like the loan has been denied. This could be due to a low credit score, insufficient loan amount, or other factors. If you would like to explore other loan options, please contact a loan provider.', 'intermediate_steps': {'request_args': '{"borrower": {"name": "lolo", "creditScore": 210, "yearlyIncome": 0}, "loan": {"amount": 100000, "duration": 100, "yearlyInterestRate": 0, "yearlyRepayment": 0, "approved": false, "messages": []}}', 'response_text': '{"__DecisionID__":"da57adb4-1830-4d20-bc3d-ed48851308340","loan":{"amount":100000,"duration":100,"yearlyInterestRate":0.0,"yearlyRepayment":0,"approved":false,"messages":[]}}'}}}
    response={}
    response['output'] = qa_chain(
        {"question": query, "chat_history": chat_history})

    return response['output']

css="""
#col-container { margin-left: auto; margin-right: auto;}
"""

title = """
<div style="text-align: center;">
    <h1>Chat with ODM Assistant</h1>
    <p style="text-align: center;">
    Here some questions you can ask to the Decision chat system:
    <li>What are the steps to configure ODM with AWS EKS?</li>
    <li>give me more details on step 1</li>
    <li>Can ODM be installed on an iPhone?</li>
    </p>
 </div>
"""
chat_history = []

with gr.Blocks(css=css) as demo:
    with gr.Column(elem_id="col-container"):
        gr.HTML(title)
        chatbot = gr.Chatbot([], show_label=True,label="Chatbot Output",elem_id="chatbot",visible=True)
        question = gr.Textbox(label="Question", placeholder="Type your question and hit Enter ")
        submit_btn = gr.Button("Send message")
        check= gr.Checkbox(label="Display Request", info="Show request call")
        check.change(fn=show_text, inputs=[check], outputs=[])

    question.submit(add_text, [chatbot, question], [chatbot, question]).then(
        bot, chatbot, chatbot
    )
    
    submit_btn.click(add_text, [chatbot, question], [chatbot, question]).then(
        bot, chatbot, chatbot
    )

demo.launch()