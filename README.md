# Introduction
The integration of GenAI with IBM Operation Decision Manager, in collaboration with the Langchain project, represents a game-changing milestone in the realms of decision management, and data analysis. By combining the generative capabilities provided by LLMs coming from OpenAI or Watsonx with the robust decisioning features of IBM ODM and the integration technology of Langchain, users can unlock a multitude of benefits that significantly enhance their decision-making processes. This integration offers a seamless and comprehensive solution for businesses aiming to harness the power of language generation for automating your business decisions.

<img src="chat-with-loandecisionservice/images/LangChain.png" width="600px" heigh="400px" />

## LangChain
[LangChain](https://python.langchain.com/en/latest/) is a framework for developing applications powered by Large Language Models. The most powerful and differentiated applications will not only call out to a language model via an api, but will also:

  * Be data-aware: connect a language model to other sources of data
  * Be agentic: Allow a language model to interact with its environment

As such, the LangChain framework is designed with the objective in mind to enable those types of applications.

There are two main value props the LangChain framework provides:

   * Components: LangChain provides modular abstractions for the components neccessary to work with language models. LangChain also has collections of implementations for all these abstractions. The components are designed to be easy to use, regardless of whether you are using the rest of the LangChain framework or not.
   * Use-Case Specific Chains: Chains can be thought of as assembling these components in particular ways in order to best accomplish a particular use case. These are intended to be a higher level interface through which people can easily get started with a specific use case. These chains are also designed to be customizable.

# Query an IBM ODM decision service trace in natural language

In this sample we will show you how to query Decision Service data execution traces through natural language. You can select your dataset, express metrics and KPIs in plain text.
This integration uses the [Spark LangChain integration](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/spark.html?highlight=spark).

Find the installation instructions at [directory](chat-with-executions-data). 

<img src="chat-with-executions-data/images/data-query.gif"  />

# Invoke a decision service in natural language

In this sample we leverage the miniloan decision service provided as a sample in IBM ODM. The [LangChain OpenAPI Chain](https://python.langchain.com/en/latest/modules/chains/examples/api.html) will be used to interact with the "MiniLoan" decision service. Utilizing the Swagger API generated dynamically by the ODM Runtime, this integration will allow for natural language interaction with the ODM product without any changes to the product itself.

The instructions to install it can be found in this [directory](chat-with-loandecisionservice).


<img src="chat-with-loandecisionservice/images/demo_presentation.gif"  />


# Govern your Decision Automation projects in natural language

In this sample we aim to bring ODM Decision Center management features into a conversational user experience. We leverage Langchain and an LLM to provide a conversational UX to interrogate and act on the IBM ODM project repository. In this integration we reuse the Swagger REST API provided by IBM ODM Decision Center. The LLM brings natural its language processing for understanding and generating text, while LangChain offers chaining of prompts and the wrapping of any REST API in plain text, put together in the context of a bot conversation. 
Diving in more details we utilize the [LangChain Swagger Agent API](https://python.langchain.com/en/latest/modules/agents.html).

The installation instructions are available in this [directory](chat-with-businessconsole).

# Building an Interactive Chat Bot for ODM Product Installation and Usage

In the fast-paced world of technology and business, staying up-to-date with complex software like IBM's Operational Decision Management (ODM) can be a challenging task. To simplify this process and provide a user-friendly experience, we present a code sample that demonstrates the development of an interactive chat bot powered by LangChain, utilizing vector and RAG architecture.
This chat bot aims to facilitate the exploration and understanding of ODM by indexing its documentation and offering real-time assistance, all within the convenience of your local desktop, including the Apple Mac M1.

The installation instructions are available in this [directory](chat-with-documentation).
