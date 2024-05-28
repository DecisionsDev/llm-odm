## Introduction 
The integration of the Langchain project with ODM, a cutting-edge decision management product, signifies a significant leap forward in the realms of language processing and data-driven decision-making. By combining Langchain's advanced language analysis technology with the powerful capabilities of ODM, users can unlock a multitude of benefits that revolutionize their decision-making processes. This integration offers a seamless and robust solution for businesses looking to harness the power of multilingual data, optimize operations, and drive strategic outcomes. In the following lines, we will explore five compelling advantages that arise from this integration.

In this sample we leverage the miniloan decision service provided as a sample in IBM ODM. The [LangChain AgentExecutor Chain]([https://python.langchain.com/docs/integrations/toolkits/openapi/](https://python.langchain.com/v0.1/docs/modules/agents/)) will be used to interact with the "MiniLoan" decision service. 

<img src="chat-with-execution-demo/images/loanvalidationchat.gif"  />

## Pre-requisites
  * Python 3.8 or higher (not needed for docker uses)
  * docker 
  * A WatsonX account or a ollama (for local execution)

## Setup Pre-Requisites

## Installation Instructions

## For local execution using Ollama 
This option require a machine that have enough GPU. For example, a mac with ARM architecture is enough

### Install Ollama
[Ollama](https://ollama.ai/) allows you to run open-source large language models, such as Llama 2, locally.

Ollama bundles model weights, configuration, and data into a single package, defined by a Modelfile.

It optimizes setup and configuration details, including GPU usage.

1. [Download and run](https://ollama.ai/download) the app
2. Once Ollma is up and running, you should download a model. For this sample we will used llava:v1.6 model.
For a complete list of supported models and model variants, see the [Ollama model library](http://ollama.ai/library).
3. From command line, fetch the llava model.
   
```shell
ollama pull mistral
```

When the app is running, all models are automatically served on [localhost:11434](http://localhost:11434)
> In some OS configuration you should [allow additional web origins to access Ollama](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-allow-additional-web-origins-to-access-ollama)

### Clone the code
1. Open a new terminal
```shell
git clone https://github.com/DecisionsDev/llm-odm.git
cd llm-odm
```

### Create a virtual env and install the Python package
```shell
python3 -m venv ~/llm-exec
~/llm-exec/bin/activate
pip install -r requirements.txt
```


### Run the Chat application

Open a new terminal
```shell
python3 app.py
```

Send question to the LLM : compute a loan validation rates with an amount of 10000$ , a duration of 10 years and an interest of 0.01.


Result from the LLM : The monthly payment for a $10,000 loan with a 10-year term at an annual interest rate of 1% (0.01) is 
approximately $112.35. The total amount paid over the life of the loan would be around $13,482.16.
==> This is hallucination.


Result from the LLM using Rules agent plug-in : 
  Invoke rules engine with this this loan parameters  amount: 10000 Duration : 10 years -> The llm extract the values from the text and call the Agent function with this parameters. Then we can invoke the rule engine.
==> Compute every time the same results.
